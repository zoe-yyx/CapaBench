
import copy
import openai
import torch
import random
import numpy as np
import json
from typing import Any, Dict, List, Optional
from llama import Dialog, Llama
from util import safe_openai_chat_call, refine_prompt, find_first_bracket_content_with_braces
import requests

from prompt.prompt_collection_noTools import prompt_few_shot, prompt_system, prompt_system_planning, prompt_user_planning, prompt_system_action,\
        prompt_user_action, prompt_system_reasoning, prompt_user_reasoning, prompt_system_reflection, prompt_user_reflection

class LLMAgent_Base:
    def __init__(self, **kwargs):
        self.prompt_system = prompt_system
        self.prompt_few_shot = prompt_few_shot
        self.prompt_system_planning = prompt_system_planning
        self.prompt_user_planning = prompt_user_planning
        self.prompt_system_reasoning = prompt_system_reasoning
        self.prompt_user_reasoning = prompt_user_reasoning
        self.prompt_system_action = prompt_system_action
        self.prompt_user_action = prompt_user_action
        self.prompt_system_reflection = prompt_system_reflection
        self.prompt_user_reflection = prompt_user_reflection
    
    def __call__(self, *args: Any, **kwds: Any) -> Any:
        return self.forward(*args, **kwds)
        
    
    def forward(self, obs: Dict) -> str:
        pass
    
    
    def llm_content(self, prompt):
        pass
    


class LLMAgent(LLMAgent_Base):
    def __init__(self, model, tokenizer, temperature, top_p, max_gen_len, **kwargs):
        super().__init__(**kwargs)
        self.model = model
        self.tokenizer = tokenizer
        self.temperature = temperature
        self.top_p = top_p
        self.max_gen_len = max_gen_len
        self.generator = Llama.build(
            ckpt_dir = self.model,
            tokenizer_path = self.tokenizer,
            max_seq_len = 8192,
            max_batch_size = 1
        )
            
    def seed(self, seed: int):
        self._seed = seed
        random.seed(seed)
        np.random.seed(seed)
        torch.manual_seed(seed)
        torch.cuda.manual_seed(seed)
        torch.backends.cudnn.deterministic = True
    

    def decision_formatter(self, action_space):
        schema = {
            "type": "object",
            "properties": {
                "element": {
                    "type": "string",
                    "enum": action_space + ['SEARCH']
                }
            },
            "required": ["element"]
        }
        
        return schema


    def llm_content(self, prompt_system, prompt):
        init_dialogs: List[Dialog] = [
            [
                {"role": "system", "content": prompt_system},
            ]
        ]
        dialogs: List[Dialog] = copy.deepcopy(init_dialogs)

        dialogs[0].append({"role": "user", "content": prompt})
        results = self.generator.chat_completion(
            dialogs,
            max_gen_len=self.max_gen_len,
            temperature=self.temperature,
            top_p=self.top_p
        )

        dialogs[0].append(results[0]['generation'])
        response = results[0]['generation']['content']
        return response

    
    
    def llm_planning(self, obs, theorem):   
        # """
        # ------------------
        # INSTRUCTIONS:
        # $objective
        # ------------------
        # GENERATE PLANNING:
        # """
        prompt_user= refine_prompt(
            self.prompt_user_planning,
            objective=obs,
            theorem = theorem
        )
        planning = self.llm_content(self.prompt_system_planning, prompt_user)
        
        return planning
    
    def llm_reasoning(self, obs, planning_context, actions_history, reflection, problem, theorem):     
        # """
        # $improvements
        # ------------------
        # PLANNING:
        # $planning

        # ------------------
        # HISTORICAL ACTIONS:
        # $past_actions

        # ------------------
        # CURRENT OBSERVATION:
        # $current_observation

        # ------------------
        # GENERATE REASONING:
        # """
        actions_history =  f"{actions_history}"
        prompt_user = refine_prompt(
            self.prompt_user_reasoning,
            improvements = reflection,
            planning = planning_context,
            past_actions = actions_history,
            current_observation = obs,
            original_problem = problem,
            theorem = theorem

        )
        # print("prompt_user", prompt_user)
        thought = self.llm_content(self.prompt_system_reasoning, prompt_user)
        
        return thought

    
    def llm_action(self, obs, planning_context, actions_history, current_thought, problem, theorem): 
        # """
        # ------------------
        # CURRENT OBSERVATION:
        # $current_observation

        # ------------------
        # PLANNING:
        # $planning

        # ------------------
        # CURRENT REASONING:
        # $thought

        # ------------------
        # HISTORICAL ACTIONS:
        # $past_actions

        # ------------------
        # GENERATE ACTION:
        # """

        # actions_history =  ",".join(actions_history)
        actions_history =  f"{actions_history}"
    
        prompt_user = refine_prompt(            
            self.prompt_user_action,
            planning = planning_context,
            current_observation = obs,
            past_actions = actions_history,
            thought = current_thought,
            original_problem = problem,
            theorem = theorem
        )


        # print("prompt_user", prompt_user)
        action = self.llm_content(self.prompt_system_action, prompt_user)

        return action
    
    def llm_reflection(self, obs, actions_history, thoughts_history, problem, theorem):   
 
        actions_history =  f"{actions_history}"
        thoughts_history =  f"{thoughts_history}"
        prompt_user= refine_prompt(
            self.prompt_user_reflection,
            past_actions = actions_history,
            past_thoughts = thoughts_history,
            current_observation = obs,
            original_problem = problem,
            theorem = theorem
        )   
        reflection_content = self.llm_content(self.prompt_system_reflection, prompt_user)

        return reflection_content
    


class APIAgent(LLMAgent_Base):
    def __init__(self, api_url, temperature, top_p, max_gen_len, **kwargs):
        super().__init__(**kwargs)
        self.temperature = temperature
        self.top_p = top_p
        self.max_gen_len = max_gen_len
        self.api_url = api_url  
        self.max_retries = 5 # Set a limit for the number of retries
        self.timeout = 600  # 设置超时时间10min

    def seed(self, seed: int):
        self._seed = seed
        random.seed(seed)
        np.random.seed(seed)
        torch.manual_seed(seed)
        torch.cuda.manual_seed(seed)
        torch.backends.cudnn.deterministic = True

    def llm_content(self, prompt_system, prompt):
        ### TODO: implement your function here to ask llm for something
        return prompt_system + prompt + "HERE IS RESPONSE OF LLM"
        
    

    def llm_planning(self, obs, theorem):   
        prompt_user = refine_prompt(
            self.prompt_user_planning,
            objective=obs,
            theorem = theorem
        )
        planning = self.llm_content(self.prompt_system_planning, prompt_user)
        
        return planning

    def llm_reasoning(self, obs, planning_context, actions_history, reflection, problem, theorem):     
        actions_history = f"{actions_history}"
        prompt_user = refine_prompt(
            self.prompt_user_reasoning,
            improvements=reflection,
            planning=planning_context,
            past_actions=actions_history,
            current_observation = obs,
            original_problem = problem,
            theorem = theorem
        )
        thought = self.llm_content(self.prompt_system_reasoning, prompt_user)
        return thought

    def llm_action(self, obs, planning_context, actions_history, current_thought, problem, theorem): 
        actions_history = f"{actions_history}"

        prompt_user = refine_prompt(            
            self.prompt_user_action,
            planning = planning_context,
            current_observation = obs,
            past_actions = actions_history,
            thought = current_thought,
            original_problem = problem,
            theorem = theorem

        )
        action = self.llm_content(self.prompt_system_action, prompt_user)
        return action
    
    def llm_reflection(self, obs, actions_history, thoughts_history, problem, theorem):   
 
        actions_history =  f"{actions_history}"
        thoughts_history =  f"{thoughts_history}"
        prompt_user= refine_prompt(
            self.prompt_user_reflection,
            past_actions = actions_history,
            past_thoughts = thoughts_history,
            current_observation = obs,
            original_problem = problem,
            theorem = theorem
        )   
        reflection_content = self.llm_content(self.prompt_system_reflection, prompt_user)

        return reflection_content

