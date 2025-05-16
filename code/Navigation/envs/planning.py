from thefuzz import fuzz
import traceback
from pathlib import Path
import re
from dialop.games import PlanningGame
from dialop.envs import DialogueEnv, GameError
from dialop.templates import (
    PlanningUserPromptTemplate,
    PlanningProposalTemplate,
    PlanningAgentPromptTemplate,
)
from dialop.planning_query_executor import (
  StaticQueryExecutor, SearchError,GPT3QueryExecutor
)

class PlanningEnv(DialogueEnv):

    def __init__(self, generator,query_executor="gpt3"):
        self.players = ["user", "agent"]
        self.search_time=0
        self.generator=generator
        datapath = Path(__file__).parent / "data"
        self.instructions = [
            (datapath / "planning_user.txt").read_text(),
            (datapath / "planning_agent.txt").read_text()
            ]
        self.query_executor = query_executor
        if query_executor == "static":
            self._search_cls = StaticQueryExecutor
        elif query_executor == "gpt3":
            self._search_cls = GPT3QueryExecutor
        else:
            raise NotImplementedError

    def partical_add(self, game_state=None):
        self.game.add_preferece()
        self.preferences=[(p.readable, p.weight, type(p).__name__, p.__dict__) for p in self.game.prefs]
        
        all_scores = self.game._compute_all_solutions(sample=False)
        self.best_score = max(all_scores)
        self.worst_score = min(all_scores)
    
    def reset(self, game_state=None):
        if game_state is not None:
            self.game = PlanningGame.create_from_game_state(game_state)
            self.preferences = game_state["preferences"]
            self.events = game_state["events"]
        else:
            self.game = PlanningGame({})
            self.game.reset()
            info = self.game.get_game_info()
            self.preferences = info["preferences"]
            self.events = info["events"]
        self.search = self._search_cls(self.events,self.generator)
        # Compute score range
        all_scores = self.game._compute_all_solutions(sample=False)
        self.best_score = max(all_scores)
        self.worst_score = min(all_scores)
        self.num_msgs = 0
        obss = self._init_from_action_log()
        return {**obss,
                "turn_player": self.players[self.game.turn_player],
                "done": False}

    def step(self, message,mode="none"):
        """Step the game state with a message.

        Errors from game logic (e.g. incorrect search syntax, searching by
        fields we don't support, invalid proposal lengths) will be caught
        and added to the prompt, allowing the LM to regenerate. For all other
        errors, resample from the LM.

        Return:
            obss: Dict with obs for each player and game info
            resample: bool indicating whether we need to resample
        """
        done = False
        reward = 0
        info = {"num_msgs": self.num_msgs}
        player = self.players[self.game.turn_player]
        Tag=False
        search_tag=False
        plan_tag=False
        score_tag=False
        process_tag=False
        obss=["",""]
            
        try:

            m = self._parse_message(
                message,
                can_propose=(player == "agent"),
                can_respond=(player != "agent"),
                must_respond=(player != "agent" and  self.game.is_full_proposal),
            )
            if not m:
                raise GameError(f"Invalid message: {message}."
                            "Messages must be formatted with a type like '[message]"
                            "<content here>'")
            else:
                type_ = m["mtype"]
                content = m["msg"]
            
            if type_ == "message":
                self.num_msgs += 1
                if player == "agent":
                    obss = [f"\nAgent: {message}", message]
                else:
                    obss = [message, f"\nUser: {message}"]
                self.game.message({
                        "data": content,
                        "from_player": self.game.turn_player,
                        "type": "utterance"})
             
#                self._take_turn()
            elif type_ == "think":
                match = re.match(r"\[(\w+)\]", content.strip())
                try:
                    match=match.group(1)
                except:
                    raise GameError("think error. think again")
                message_temp=""
                if match!=mode:
                    message_temp=f"You should {mode},However you {match},please {mode} directly"
                    obss = ["", message+message_temp]
                    raise ValueError("process")
                if player == "agent":
                    
                    obss = ["", message+message_temp]

                else:
                    obss = [message+message_temp, ""]
                
            elif type_ == "tool":
                
                assert player == "agent", "User cannot use tool."
                match="action"
                
                if self.search_time>4:
                    raise SearchError("You have searched too many times, please give a proposal according to results based on information gived")
                
                self.search_time+=1
                result = self._call_tool(content)
                if mode!="action":
                    obss = ["",f"\n Error,You should {mode},However You action,please {mode} directly"]
                    raise ValueError("process")
                else:
                    obss = ["", f"{message}\n"+"---searching---\n"+f"{result}"]
              


            elif type_ == "propose":
                
                    
                self.num_msgs += 1
                
                if player != "agent":
                    raise GameError("Only the agent can make proposals.")
                self.search_time=0
                _, proposal_info = self._propose(content)
                total_score=_['total_score']
                score_nomarlized=self._normalize(total_score)
                score_tag=True
                obss = [f"\nAgent: [propose] {proposal_info}", message]
                if self.last_time=="propose" and self.last_true==True:
                    obss = ["","Error,you have propse yet,please send message"]
                if self.game.is_full_proposal:
                    obss[0] += (f"\nYou can [think], or output one of these choices:\n"
                                f"(1) [accept] Accept\n(2) [reject] Reject")
#                self._take_turn()
            elif type_ == "accept" or type_ == "reject":
                self.num_msgs += 1
                done, game_infos = self._proposal_response(
                    type_ == "accept",
                    self.game.turn_player)
                info.update({
                    "best_score": self.best_score,
                    "worst_score": self.worst_score,
                    "reward_normalized": self._normalize(game_infos[0]["reward"])
                })
                reward = game_infos[0]["reward"]
                obss = [f"[{type_}]", f"\nUser: [{type_}]"]

            elif type_ == "add":
                self.partical_add()
                p=self.game.new_add

                obss = [p,""]
            elif type_ == "reflection":
                obss = [f"\nAgent: {message}", message]

            else:
                obss = ["",""]
                raise ValueError(f"Message type not found for: {message}.")
        except (GameError, SearchError) as e:
           
             
            if isinstance(e,SearchError):
                search_tag=True
            else:
                Tag=True
            obss=["",""]
            obss[self.game.turn_player] = f"{message}\nError: {str(e)}"
        except ValueError as e:
            if str(e)=="message":
                
                plan_tag=True
            if str(e)=="process":
                process_tag=True
                now=match
            
        except Exception as e:
            obss=["",""]
            print(f"!!! {traceback.format_exc()}")
            import pdb; pdb.set_trace()
            return {
                **{p: "error" for p in self.players},
                "done": False,
                "reward": 0,
                "turn_player": self.players[self.game.turn_player]
            }, True
        obss = {self.players[i]: obs for i, obs in enumerate(obss)}
        obss["turn_player"] = self.players[self.game.turn_player]
        obss["done"] = done
        obss["reward"] = reward
        obss["info"] = info
        if score_tag:
            obss['score']=score_nomarlized
        if search_tag:
            obss["search"] = True
        if Tag:
            obss["error"]=True
        if plan_tag:
            obss["plan"]=True
        if process_tag:
            obss["process"]=True
            obss["now"]=now
        try:
            self.last_time=type_
            self.last_true=not Tag
        except:
            pass
        return obss, False

    def _propose(self, message):
        try:
            proposal = self._parse_events(message)
            if len(proposal) < 5:
                raise GameError("You must have 3 events in your proposal. "
                                "Put 'NULL' for a slot to make a partial "
                                "proposal.")
            pinfo = self.game.propose(proposal, self.game.turn_player)
            pinfo_prompt = self._format_proposal(
                pinfo["proposal_data"],
                pinfo["itinerary_scores"],
                pinfo["evt_scores"],
                pinfo["total_score"])
            self.proposal_info = pinfo
            return pinfo, pinfo_prompt
        except:
            raise GameError(f"Messages must be formatted with [propose][place1,place2,place3]")

    def _call_tool(self, message: str):
        return self.search(message)

    def _init_from_action_log(self):
        obss = {}
        obss["user"] = PlanningUserPromptTemplate.render(
            travel_doc="\n".join([p[0] for p in self.preferences]),
            messages=self.game.action_log,
            player_id=0,
            format_proposal=self._format_proposal,
            any=any, # to call any() in template
        ).rstrip()
        obss["agent"] = PlanningAgentPromptTemplate.render(
            messages=self.game.action_log,
            player_id=1,
            format_proposal=self._format_proposal_agent,
        ).rstrip()
        obss[self.players[self.game.turn_player]] += "\nYou:"
        return obss

    def _format_proposal(self, proposal, it_scores, evt_scores, tot_score):
        all_scores = evt_scores + [s["score"] for s in it_scores]
        if round(sum(all_scores)) != tot_score:
            import pdb; pdb.set_trace()
        score_calculation = "".join(
            f"+{s}" if s >= 0 else f"{s}" for s in all_scores) + f"={tot_score}"
        proposal_msg = "[" + ", ".join([
            proposal[0]["name"] if proposal[0] else "NULL",
            proposal[2]["name"] if proposal[2] else "NULL",
            proposal[4]["name"] if proposal[4] else "NULL",
        ]) + "]"
        return PlanningProposalTemplate.render(
            proposal_msg=proposal_msg,
            proposal=proposal,
            itinerary_scores=it_scores,
            evt_scores=evt_scores,
            score_calculation=score_calculation,
        )

    def _format_proposal_agent(self, proposal):
        proposal_msg = "[" + ", ".join([
            proposal[0]["name"] if proposal[0] else "NULL",
            proposal[2]["name"] if proposal[2] else "NULL",
            proposal[4]["name"] if proposal[4] else "NULL",
        ]) + "]"
        return proposal_msg

    def _parse_events(self, message):
        """Parses a proposal message to a list of event dicts as a structured
        proposal to pass to the game."""
        names = message[message.index("[") + 1 :
                        message.index("]")].split(",")
        names = [e.strip() for e in names]
        if len(names) > 3:
            raise GameError("You can only propose up to three events."
                            "Try re-proposing with three events.")
        events = []
        site_names = [site["name"] for site in self.events]
        proposal = []
        for e in names:
            found = False
            if e == "NULL":
                proposal.append(None)
                found = True
            elif e in site_names:
                proposal.append({
                    **self.events[site_names.index(e)],
                    "type": "event"
                })
                found = True
            # Fall back to fuzzy search
            else:
                for i, evt in enumerate(site_names):
                    if fuzz.ratio(evt, e) > 80:
                        proposal.append({
                            **self.events[i],
                            "type": "event"
                        })
                        found = True
                        break
            if not found:
                raise GameError(f"{e} is not a valid destination please propose again and fix the error")
        # Populate distances
        proposal_with_dists = []
        for i in range(len(proposal) - 1):
            proposal_with_dists.append(proposal[i])
            if proposal[i] and proposal[i + 1]:
                dist = self.search.distance(proposal[i], proposal[i+1])
                proposal_with_dists.append({
                    "data": dist,
                     "name": (f"Travel from {proposal[i]['name']} to "
                              f"{proposal[i+1]['name']}, {dist}mi"),
                     "type": "travel"})
            else:
                proposal_with_dists.append(None)
        if len(proposal) == 0:
            import pdb; pdb.set_trace()
        proposal_with_dists.append(proposal[-1])
        return proposal_with_dists

    def _normalize(self, score):
        return (score - self.worst_score) / (self.best_score - self.worst_score)

