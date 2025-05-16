import json
import openai
import os
import pathlib
from rich.prompt import IntPrompt, Prompt
from rich.markup import escape
from llama3.llama import Dialog, Llama
from envs import DialogueEnv
from utils import num_tokens
import random
from prompt.prompt_collection import prompt_system_planning, prompt_user_planning, prompt_system_reasoning, prompt_user_reasoning, prompt_system_action, prompt_user_action,prompt_system_proposal,prompt_system_reflection
try:
    with open(pathlib.Path(__file__).parent / ".api_key") as f:
        x = json.load(f)
        openai.organization = x["organization"]
        openai.api_key = x["api_key"]
    print("Loaded .api_key")
except:
    openai.api_key = os.getenv("OPENAI_API_KEY")

if not openai.api_key:
    print("Warning: no OpenAI API key loaded.")

class OutOfContextError(Exception):
    pass

class DryRunPlayer:

    def __init__(self, prompt, role, console, task="planning"):
        self.prompt = prompt
        self.role = role
        self.console = console
        self.calls = 0
        self.task = task

    def observe(self, obs):
        self.prompt += obs

    def respond(self):
        self.calls += 1
        if self.role == "agent" and self.calls == 5:
            if self.task == "planning":
                return f" [propose] [Saul's, Cookies Cream, Mad Seoul]"
            elif self.task == "mediation":
                return f" [propose] User 0: [1], User 1: [15]"
        elif self.role == "user" and self.calls == 6:
            return f" [reject]"
        return f" [message] {self.calls}"
import re

def parse_dialog(text):
    # 定义正则表达式模式来匹配用户和助手的发言
    pattern = re.compile(r"(User|You): (.+?)(?=(User:|You:|$))", re.DOTALL)
    
    # 查找所有匹配的发言
    matches = pattern.findall(text)
    
    # 创建对话列表
    dialog = []
    
    # 添加发言到对话列表
    for match in matches:
        role = "user" if match[0] == "User" else "assistant"
        content = match[1].strip()
        dialog.append({"role": role, "content": content})
    
    return dialog



class LLMPlayer:

    def __init__(self,generator, prompt, role, console, model_kwargs=None,
                 prefix="\nYou:", optional=None,partial=False,generator_ls=None):
        self.prompt = prompt
        self.example=self.prompt
        dialog=parse_dialog(self.prompt)
        
        self.dialog_history=[]
        # self.prompt=prompt
        # self.prompt=""
        self.prompt_system_proposal=prompt_system_proposal
        self.prompt_system_planning = prompt_system_planning
        self.prompt_system_reflection = prompt_system_reflection
        self.prompt_user_planning = prompt_user_planning
        self.prompt_system_reasoning = prompt_system_reasoning
        self.prompt_user_reasoning = prompt_user_reasoning
        self.prompt_system_action = prompt_system_action
        self.prompt_user_action = prompt_user_action
        self.dialog_history.append({"role":"system"})
        self.dialog_history.extend(dialog)
        self.partial=partial
        if partial:
            self.planning_generator=generator_ls[0]
            self.reasoning_generator=generator_ls[1]
            self.action_generator=generator_ls[2]
            self.reflection_generator=generator_ls[3]
            self.generator=None
        else:
            self.generator=generator
        self.role = role
        self.console = console
        self.search_time=0
        self.init_dialog=self.dialog_history
        self.optional = optional
        self.removed_optional = False
        if self.role in ["user", "agent", "user0", "user1"]:
            stop_tokens = ["User", "Agent", "You","\n\n","---"]
        elif self.role in ["player-1", "player-2"]:
            stop_tokens = ["Partner", "You", "\n"]
        else:
            raise NotImplementedError
        self.model_kwargs = dict(
            temperature=0,
            top_p=.95,
            #presence_penalty=0,
            stop=stop_tokens,
        )
        if model_kwargs is not None:
            self.model_kwargs.update(**model_kwargs)
        self.prefix = prefix
        
        self.action_remain=[]
    #    self.model = "gpt-3.5-turbo"

    def observe(self, obs):
        self.prompt += obs
    def add_to_dialog(self,user,content):
        dia={'role':user,'content':content}
        self.dialog_history.append(dia)
        # self.prompt=self.turn_dialog_to_prompt()
    def turn_dialog_to_prompt(self):
        transformed_dialog = self.example
    
        for entry in self.dialog_history[1:]:
            role = entry['role']
            content = entry['content']
            
            if role == 'user':
                transformed_dialog += f"User: {content}\n"
            elif role == 'assistant':
                # 处理空内容的情况
                if content.strip():
                    transformed_dialog += f"You: {content}\n"
            else:
                transformed_dialog+=f"system:{content}"

        # transformed_dialog+="\nYou:"
        return transformed_dialog

    def respond(self,kwarg):
        self.console.rule(f"{self.role}'s turn")
        
        if not self.prompt.endswith(self.prefix):
            self.prompt += self.prefix
        #self.console.print(escape(self.prompt))
        # remaining = 4096 - num_tokens(self.prompt)
        # if remaining < 0 and self.optional:
        #     self._remove_optional_context()
        #     remaining = 4096 - num_tokens(self.prompt)
        # # Still out of context after removing
        # if remaining < 0:
        #     print("OUT OF CONTEXT! Remaining ", remaining)
        #     raise OutOfContextError()
        if kwarg["mode"]=="planning":
            prompts=self.prompt_system_planning+self.prompt
            # self.dialog_history.extend([{"role":"system","content":self.prompt_system_planning}]) 

            # self.dialog_history[self.remain_to_add]["content"]=self.prompt_system_planning
            
            if len(self.dialog_history)>28:
                list_justice=[i for i in range(-6,0)]
                self.action_remain.extend([self.dialog_history[i] for i in list_justice])
                self.dialog_history=self.init_dialog
                self.dialog_history.extend(self.action_remain)
                self.prompt=self.turn_dialog_to_prompt()
            
            prompts_end="[think][planning]"
            if self.partial:
                self.generator=self.planning_generator
        elif kwarg["mode"]=="reasoning":
            prompts=self.prompt_system_reasoning+self.prompt
            # self.dialog_history.extend([{"role":"system","content":self.prompt_system_reasoning}])
            self.dialog_history[0]["content"]=self.prompt_system_reasoning
            prompts_end="[think][reasoning]"
            if self.partial:
                self.generator=self.reasoning_generator
        elif kwarg["mode"]=="action":
            prompts=self.prompt_system_action+self.prompt
            self.dialog_history[0]["content"]=self.prompt_system_action
            # self.dialog_history.extend([{"role":"system","content":self.prompt_system_action}]) 
            prompts_end=""
            if self.partial:
                self.generator=self.action_generator
        elif kwarg["mode"]=="reflection":
            prompts=self.prompt_system_reflection+self.prompt
            # self.dialog_history.extend([{"role":"system","content":self.prompt_system_reflection}]) 
            prompts_end="[reflection]"
            if self.partial:
                self.generator=self.reflection_generator
        else:
            prompts=self.prompt
            prompts_end=""
            if self.partial:
                self.generator=self.reasoning_generator

        
        prompts=prompts+prompts_end
        # import pdb;pdb.set_trace()
        prompt=[]
        prompt.append(prompts)
        kwargs = dict(
            prompts=prompt,
            dialog=self.dialog_history
        )
        kwargs.update(**self.model_kwargs)
        # response = openai.Completion.create(**kwargs)
        # import pdb;pdb.set_trace()

        response = self.generator.text_completion(**kwargs)
        # respeonse= self.generator
        answer=response[0]['generation'].strip()
        # self.dialog_history=self.dialog_history[:-1]
        if not answer.startswith('['):
            answer=prompts_end+answer

        self.console.print("Response:",answer)
        # return response["choices"][0]["text"].strip()
        return answer

    def _remove_optional_context(self):
        print("Cutting out optional context from prompt.")
        if self.removed_optional:
            print("!! already removed.")
            return
        self.prompt = (
            self.prompt[:self.prompt.index(self.optional)] +
            self.prompt[self.prompt.index(self.optional) + len(self.optional):])
        self.removed_optional = True

class HumanPlayer:

    def __init__(self, prompt, role, console, prefix="\nYou:"):
        self.prompt = prompt
        self.role = role
        self.console = console
        self.prefix = prefix

    def observe(self, obs):
        self.prompt += obs

    def respond(self):
        if not self.prompt.endswith(self.prefix):
            self.prompt += self.prefix
        self.console.rule(f"Your turn ({self.role})")
        # self.console.print(escape(self.prompt))
        resp = ""
        if self.prefix.strip().endswith("You to"):
            id_ = Prompt.ask(
                escape(f"Choose a player to talk to"),
                choices=["0","1","all"])
            resp += f" {id_}:"
        mtypes = ["[message]", "[propose]", "[accept]", "[reject]","[add]"]
        choices = " ".join(
                [f"({i}): {type_}" for i, type_ in enumerate(mtypes)])
        type_ = IntPrompt.ask(
                escape(
                    f"Choose one of the following message types:"
                    f"\n{choices}"),
                choices=["0","1","2","3","4"])
        message_type = mtypes[type_]
        if message_type not in ("[accept]", "[reject]"):
            content = Prompt.ask(escape(f"{message_type}"))
        else:
            content = ""
        resp += f" {message_type} {content}"
        return resp

class FixedPlayer:

    def __init__(self, prompt, role, console, prefix="\nYou:"):
        self.prompt = prompt
        self.role = role
        self.console = console
        self.prefix = prefix
        self.add_new= False
        self.first_time=True
        self.add_finish=False
        self.has_full=False

    def observe(self, obs):
        self.prompt += obs

    def respond(self,kwargs):
        env=kwargs["env"]
        if self.first_time:
            type_=0
            content="Here is a new request:"+".".join([p[0] for p in env.preferences])
            self.first_time=False
        else:
            receive_proposal=random.random()>0.5
            if kwargs["time"]>2:
                receive_proposal=True
            if self.add_new:
                type_=4
                self.add_new=False
                self.add_finish=True
                content="I want to add a new request."
            elif self.add_finish:
                type_=0
                content="I add a request "+[p [0] for p in env.preferences][-2]
                self.add_finish=False 
            # else:
            #     if receive_proposal:
            #         type_=2
            #     else:
            #         type_=3
            #         self.add_new=True
            # elif env.game.is_full_proposal:
            #     self.has_full=True
            #     if receive_proposal:
            #         type_=2
            #     else:
            #         type_=3
            #         self.add_new=True
            # elif not self.has_full:
            #     type_=0
            #     self.add_new=True
            #     content="I want add a request"
            # else:
            #     type_=0
            #     content="I want a full proposal"
            else:
                if receive_proposal:
                    type_=2
                else:
                    type_=3
                    self.add_new=True
            # else:
            #     type_=0
            #     content="I want a full proposal"
        if not self.prompt.endswith(self.prefix):
            self.prompt += self.prefix
        self.console.rule(f"Your turn ({self.role})")
        # self.console.print(escape(self.prompt))
        resp = ""
        if self.prefix.strip().endswith("You to"):
            id_ = Prompt.ask(
                escape(f"Choose a player to talk to"),
                choices=["0","1","all"])
            resp += f" {id_}:"
        mtypes = ["[message]", "[propose]", "[accept]", "[reject]","[add]"]
        choices = " ".join(
                [f"({i}): {type_}" for i, type_ in enumerate(mtypes)])
        # type_ = IntPrompt.ask(
        #         escape(
        #             f"Choose one of the following message types:"
        #             f"\n{choices}"),
        #         choices=["0","1","2","3","4"])
        
        message_type = mtypes[type_]
        if message_type  in ("[accept]", "[reject]"):
        #     # content = Prompt.ask(escape(f"{message_type}"))
        # else:
            content = ""
        resp += f" {message_type} {content}"
        self.console.print("Response:",resp)
        return resp
