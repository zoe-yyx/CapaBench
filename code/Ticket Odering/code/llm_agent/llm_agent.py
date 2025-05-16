import re
import sys
# 添加想要导入模块的目录
# sys.path.append('/home/hadoop-aipnlp/dolphinfs_hdd_hadoop-aipnlp/yangyingxuan/zhaohaoran05/repo/sjtu_eva')
# from llama import Dialog, Llama
from dialop.llama import Dialog, Llama

import copy
import openai
import torch
import random
import numpy as np
import json
from typing import Any, Dict, List, Optional
from dialop.myutils import safe_openai_chat_call, refine_prompt
# from prompt.few_shot import build_prompt
from dialop.prompts.prompt_collection import prompt_system_planning, prompt_user_planning, prompt_system_reasoning, prompt_user_reasoning, prompt_system_action, prompt_user_action, prompt_system_reflection, prompt_user_reflection
import requests



class LLMAgent_Base:
    def __init__(self, **kwargs):
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
        # BobHuangC(TODO) : here rudely fix the seed before each llm_content
        # future to improve this
        torch.manual_seed(0)
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
        # print("results", results)

        dialogs[0].append(results[0]['generation'])
        try:
            content = results[0]['generation']['content']
        except json.JSONDecodeError as e:
            print("JSON decoding failed:", e)
            return None  # Or handle the error differently

        return content

    

    # def llm_planning(self, obs):   
    #     # """
    #     # ------------------
    #     # INSTRUCTIONS:
    #     # $objective
    #     # ------------------
    #     # GENERATE PLANNING:
    #     # """
    #     prompt_user= refine_prompt(
    #         self.prompt_user_planning,
    #         objective=obs,
    #     )
    #     planning = self.llm_content(self.prompt_system_planning, prompt_user)
        
    #     return planning
    def llm_planning(self):
        prompt_user= self.prompt_user_planning
        # prompt_user= refine_prompt(
        #     self.prompt_user_planning,
        #     objective=obs,
        # )
        # print(f"prompt_user: {prompt_user}")
        # input("Press Enter to continue...")
        planning = self.llm_content(self.prompt_system_planning, prompt_user)
        
        return planning


    def llm_reasoning(self, obs, planning_context, actions_history ,reflection):     
        # """
        # $improvements
        # ------------------
        # PLANNING:
        # $planning
        # ------------------
        # PAST ACTIONS:
        # $past_actions
        # ------------------
        # CURRENT OBSERVATION:
        # $browser_content
        # ------------------
        # GENERATE REASONING:
        # """
        actions_history =  f"{actions_history}"
        prompt_user = refine_prompt(
            self.prompt_user_reasoning,
            improvements = reflection,
            planning = planning_context,
            past_actions = actions_history,
            browser_content = obs

        )
        # print("prompt_user", prompt_user)
        thought = self.llm_content(self.prompt_system_reasoning, prompt_user)
        
        return thought

    
    # def llm_action(self, obs, planning_context, actions_history, thoughts_history, current_thought, available_actions): 
    #     # """
    #     # ------------------
    #     # CURRENT OBSERVATION:
    #     # $browser_content
    #     # ------------------
    #     # PLANNING:
    #     # $planning
    #     # ------------------
    #     # PAST ACTIONS:
    #     # $past_actions
    #     # ------------------
    #     # CURRENT REASONING:
    #     # $thought
    #     # ------------------
    #     # AVAILABLE ACTIONS:
    #     # $available_actions
    #     # ------------------
    #     # GENERATE ACTION:
    #     # """

    #     # actions_history =  ",".join(actions_history)
    #     actions_history =  f"{actions_history}"
    #     available_actions = f"{available_actions}"
    #     prompt_user = refine_prompt(            
    #         self.prompt_user_action,
    #         planning = planning_context,
    #         browser_content = obs,
    #         past_actions = actions_history,
    #         thought = current_thought,
    #         available_actions = available_actions
    #     )


    #     # print("prompt_user", prompt_user)
    #     action = self.llm_content(self.prompt_system_action, prompt_user)

    #     return action
    def llm_action(self, obs, planning_context, current_thought): 
        # actions_history =  f"{actions_history}"
        # available_actions = f"{available_actions}"
        prompt_user = refine_prompt(            
            self.prompt_user_action,
            planning = planning_context,
            browser_content = obs,
            thought = current_thought,
        )

        # print("prompt_user", prompt_user)
        action = self.llm_content(self.prompt_system_action, prompt_user)

        return action
    

    def llm_reflection(self, obs, actions_history, thoughts_history):   
 
        actions_history =  f"{actions_history}"
        thoughts_history =  f"{thoughts_history}"
        # prompt_user= refine_prompt(
        #     self.prompt_user_reflection,
        #     past_actions = actions_history,
        #     past_thoughts = thoughts_history,
        #     browser_content = obs,
        # )   
        prompt_user= refine_prompt(
            self.prompt_user_reflection,
            past_thoughts = thoughts_history,
            past_actions = actions_history,
            browser_content = obs,
        )   
        reflection_content = self.llm_content(self.prompt_system_reflection, prompt_user)

        return reflection_content


openai.api_key = '1790715889671905303'
openai.api_base = "https://aigc.sankuai.com/v1/openai/native"

class OpenAIAgent(LLMAgent_Base):
    def __init__(self, model_name, temperature, top_p, max_gen_len, **kwargs):
        super().__init__(**kwargs)
        self.model_name = model_name
        self.temperature = temperature
        self.top_p = top_p
        self.max_gen_len = max_gen_len
        
    def llm_content(self, prompt_system, prompt, stop=[]):
        response, err_num = safe_openai_chat_call(
            model=self.model_name,
            messages=[
                {'role': 'system', 'content': prompt_system},
                {'role': 'user', 'content': prompt}
            ],
            max_gen_len=self.max_gen_len,
            temperature=self.temperature,
            top_p=self.top_p,
            stop=stop,
            seed=0,
        )
        # print("results", response)
        try:
            content = response["choices"][0]["message"]["content"]
        except Exception as e:
            print("error:", e)
            return None  
        
        return content

    # def llm_planning(self, obs):
    def llm_planning(self):
        prompt_user= self.prompt_user_planning
        # prompt_user= refine_prompt(
        #     self.prompt_user_planning,
        #     objective=obs,
        # )
        # print(f"prompt_user: {prompt_user}")
        # input("Press Enter to continue...")
        planning = self.llm_content(self.prompt_system_planning, prompt_user)
        
        return planning

    def llm_reasoning(self, obs, planning_context, actions_history ,reflection):     
        actions_history =  f"{actions_history}"
        prompt_user = refine_prompt(
            self.prompt_user_reasoning,
            improvements = reflection,
            planning = planning_context,
            past_actions = actions_history,
            browser_content = obs
        )
        # print("PROMPT_USER", prompt_user)
        thought = self.llm_content(self.prompt_system_reasoning, prompt_user)
        
        return thought

    
    def llm_action(self, obs, planning_context, current_thought): 
        # actions_history =  f"{actions_history}"
        # available_actions = f"{available_actions}"
        prompt_user = refine_prompt(            
            self.prompt_user_action,
            planning = planning_context,
            browser_content = obs,
            thought = current_thought,
        )

        # print("prompt_user", prompt_user)
        action = self.llm_content(self.prompt_system_action, prompt_user)

        return action


    def llm_reflection(self, obs, actions_history, thoughts_history):   
 
        actions_history =  f"{actions_history}"
        thoughts_history =  f"{thoughts_history}"
        # prompt_user= refine_prompt(
        #     self.prompt_user_reflection,
        #     past_actions = actions_history,
        #     past_thoughts = thoughts_history,
        #     browser_content = obs,
        # )   
        prompt_user= refine_prompt(
            self.prompt_user_reflection,
            past_thoughts = thoughts_history,
            past_actions = actions_history,
            browser_content = obs,
        )   
        reflection_content = self.llm_content(self.prompt_system_reflection, prompt_user)

        return reflection_content



class BaichuanAgent(LLMAgent_Base):
    def __init__(self, model, tokenizer, temperature, top_p, max_gen_len, **kwargs):
        super().__init__(**kwargs)
        self.model = model
        self.tokenizer = tokenizer
        self.temperature = temperature
        self.top_p = top_p
        self.max_gen_len = max_gen_len


    def llm_content(self, prompt_system, prompt):
        response = self.model.chat(
            self.tokenizer,
            messages=[
                {'role': 'system', 'content': prompt_system},
                {'role': 'user', 'content': prompt}
            ],
            # temperature=self.temperature,
            # top_p=self.top_p
        )
        # print("response",response)
        return response


    def llm_planning(self, obs):   
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
        )
        planning = self.llm_content(self.prompt_system_planning, prompt_user)
        
        return planning


    def llm_reasoning(self, obs, planning_context, actions_history, reflection):     
        # """
        # $improvements
        # ------------------
        # PLANNING:
        # $planning
        # ------------------
        # PAST ACTIONS:
        # $past_actions
        # ------------------
        # CURRENT OBSERVATION:
        # $browser_content
        # ------------------
        # GENERATE REASONING:
        # """
        actions_history =  f"{actions_history}"
        prompt_user = refine_prompt(
            self.prompt_user_reasoning,
            improvements = reflection,
            planning = planning_context,
            past_actions = actions_history,
            browser_content = obs

        )
        # print("prompt_user", prompt_user)
        thought = self.llm_content(self.prompt_system_reasoning, prompt_user)
        
        return thought

    
    def llm_action(self, obs, planning_context, actions_history, thoughts_history, current_thought, available_actions): 
        # """
        # ------------------
        # CURRENT OBSERVATION:
        # $browser_content
        # ------------------
        # PLANNING:
        # $planning
        # ------------------
        # PAST ACTIONS:
        # $past_actions
        # ------------------
        # CURRENT REASONING:
        # $thought
        # ------------------
        # AVAILABLE ACTIONS:
        # $available_actions
        # ------------------
        # GENERATE ACTION:
        # """

        # actions_history =  ",".join(actions_history)
        actions_history =  f"{actions_history}"
        available_actions = f"{available_actions}"
        prompt_user = refine_prompt(            
            self.prompt_user_action,
            planning = planning_context,
            browser_content = obs,
            past_actions = actions_history,
            thought = current_thought,
            available_actions = available_actions
        )


        # print("prompt_user", prompt_user)
        action = self.llm_content(self.prompt_system_action, prompt_user)

        return action
    

    def llm_reflection(self, obs, actions_history, thoughts_history):   
        actions_history =  f"{actions_history}"
        thoughts_history =  f"{thoughts_history}"
        # prompt_user= refine_prompt(
        #     self.prompt_user_reflection,
        #     past_actions = actions_history,
        #     past_thoughts = thoughts_history,
        #     browser_content = obs,
        # ) 
        prompt_user= refine_prompt(
            self.prompt_user_reflection,
            past_thoughts = thoughts_history,
            past_actions = actions_history,
            browser_content = obs,
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

    # def call_model_api(self, api_url, prompt, max_gen_len):
    #     payload = json.dumps({
    #             "prompt": prompt,
    #             "max_new_tokens": max_gen_len
    #         })
    #     headers = {
    #         'Content-Type': 'application/json'
    #         }
    #     response = requests.request("POST", api_url, headers=headers, data=payload)
    #     return response.text

    # def llm_content(self, prompt_system, prompt):
    #     torch.manual_seed(0)
    #     message = prompt_system + prompt
    #     max_retries = 3  # Set a limit for the number of retries
    #     attempt = 0
    #     while attempt < max_retries:
    #         try:
    #             response = self.call_model_api(self.api_url, message, self.max_gen_len)
    #             response = json.loads(response)
    #             if "completions" in response and response["completions"]:
    #                 content = response["completions"][0]["text"]  # Get the text of the first completion
    #                 if content:
    #                     return content  # Return the generated content
    #                 else:
    #                     print("No content generated.")
    #                     return None
    #             # If no completions found, retry
    #             print("No completions found in the response, retrying...")
    #             attempt += 1
    #         except Exception as e:
    #             print(f"An error occurred: {e}")
    #             return None
    #     print("Max retries reached. No completions found.")
    #     return None

    def call_model_api(self, api_url, prompt, max_gen_len):
        payload = json.dumps({
            "prompt": prompt,
            "max_new_tokens": max_gen_len
        })
        headers = {
            'Content-Type': 'application/json'
        }
        attempt = 0
        try:
            # 这里设置timeout为self.timeout秒
            response = requests.request("POST", api_url, headers=headers, data=payload, timeout=self.timeout)
            return response.text
        except requests.exceptions.Timeout:
            # 捕获超时异常并重新请求
            print(f"Request timed out. Retrying... (Attempt {attempt + 1}/{self.max_retries})")
            return None
        except requests.exceptions.RequestException as e:
            # 捕获所有其他请求异常
            print(f"An error occurred during the request: {e}")
            return None
        return None

    def llm_content(self, prompt_system, prompt):
        torch.manual_seed(0)
        message = prompt_system + prompt
        attempt = 0
        
        while attempt < self.max_retries:
            try:
                response = self.call_model_api(self.api_url, message, self.max_gen_len)
                if response is None:
                    print("No response received. Retrying...")
                    attempt += 1
                    continue
                response = json.loads(response)

                if "completions" in response and response["completions"]:
                    content = response["completions"][0]["text"]  # 获取第一个completion的文本
                    if content:
                        return content  # 返回生成的内容
                    else:
                        print("No content generated.")
                        return None
                # 如果没有找到completions，重试
                print("No completions found in the response, retrying...")
                attempt += 1

            except Exception as e:
                print(f"An error occurred: {e}")
                return None

        print("Max retries reached. No completions found.")
        return None


    def llm_planning(self):   
        prompt_user= self.prompt_user_planning
        # prompt_user = refine_prompt(
        #     self.prompt_user_planning,
        #     objective=obs,
        # )
        planning = self.llm_content(self.prompt_system_planning, prompt_user)
        
        return planning

    def llm_reasoning(self, obs, planning_context, actions_history ,reflection):     
        actions_history =  f"{actions_history}"
        prompt_user = refine_prompt(
            self.prompt_user_reasoning,
            improvements = reflection,
            planning = planning_context,
            past_actions = actions_history,
            browser_content = obs
        )
        # print("PROMPT_USER", prompt_user)
        thought = self.llm_content(self.prompt_system_reasoning, prompt_user)
        
        return thought

    def llm_action(self, obs, planning_context, current_thought): 
        # actions_history =  f"{actions_history}"
        # available_actions = f"{available_actions}"
        prompt_user = refine_prompt(            
            self.prompt_user_action,
            planning = planning_context,
            browser_content = obs,
            thought = current_thought,
        )

        # print("prompt_user", prompt_user)
        action = self.llm_content(self.prompt_system_action, prompt_user)

        return action
    
    def llm_reflection(self, obs, actions_history, thoughts_history):   
        actions_history = f"{actions_history}"
        thoughts_history = f"{thoughts_history}"
        prompt_user= refine_prompt(
            self.prompt_user_reflection,
            past_thoughts = thoughts_history,
            past_actions = actions_history,
            browser_content = obs,
        )   
        reflection_content = self.llm_content(self.prompt_system_reflection, prompt_user)

        return reflection_content