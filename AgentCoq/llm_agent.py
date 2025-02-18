import re
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
# from prompt.prompt_collection_noTools import prompt_few_shot, prompt_system, prompt_system_planning, prompt_user_planning, prompt_system_action,\
#         prompt_user_action, prompt_system_reasoning, prompt_user_reasoning, prompt_system_reflection, prompt_user_reflection
# from prompt.prompt_collection_singleTools
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
        # try:
        #     content = json.loads(response)
        # except json.JSONDecodeError as e:
        #     print("JSON decoding failed:", e)
        #     # return json.loads(find_first_bracket_content_with_braces(response))
        #     dict_str = find_first_bracket_content_with_braces(response)
        #     fixed_str = re.sub(r"(?<=\{|\,)\s*'([^']+?)'\s*:", r' "\1":', dict_str)  # 替换键的单引号
        #     fixed_str = re.sub(r":\s*'([^']+?)'\s*(?=\,|\})", r': "\1"', fixed_str)  # 替换值的单引号
        #     try:
        #         return json.loads(fixed_str)
        #     except Exception as e:
        #         print("Final JSON decoding failed:", e)
        #         return {}
        # print(response)
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

        response = response["choices"][0]["message"]["content"]
        # print("response", response, type(response))
        
        # try:
        #     content = json.loads(response)
        # except json.JSONDecodeError as e:
        #     # print("JSON decoding failed:", e)
        #     dict_str = find_first_bracket_content_with_braces(response)
        #     fixed_str = re.sub(r"(?<=\{|\,)\s*'([^']+?)'\s*:", r' "\1":', dict_str)  # 替换键的单引号
        #     fixed_str = re.sub(r":\s*'([^']+?)'\s*(?=\,|\})", r': "\1"', fixed_str)  # 替换值的单引号
        #     return json.loads(fixed_str)
        
        # return content
        return response
    
    def llm_planning(self, obs, theorem):   
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

    # def call_model_api(self, api_url, prompt, max_gen_len):
    #     payload = json.dumps({
    #             "prompt": prompt,
    #             "max_new_tokens": max_gen_len
    #         })
    #     headers = {
    #         'Content-Type': 'application/json'
    #         }
    #     response = requests.request("POST", api_url, headers=headers, data=payload)
    #     print("response", response)
    #     return response

    # def llm_content(self, prompt_system, prompt):
    #     torch.manual_seed(0)
    #     message = prompt_system+prompt
    #     try:    
    #         response = self.call_model_api(self.api_url, message, self.max_gen_len)
    #         content = response.text
    #         content = json.loads(content)
    #         content = content['completions']
    #         content = content[0]['text']
    #         if content is None:
    #             print("No content generated.")
    #             return None
    #         return content

    #     except requests.RequestException as e:
    #         print("HTTP request failed:", e)
    #         return None  
    #     except json.JSONDecodeError as e:
    #         print("JSON decoding failed:", e)
    #         return None  

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



class DouBaoAgent(LLMAgent_Base):
    def __init__(self, temperature, top_p, max_gen_len, **kwargs):
        super().__init__(**kwargs)
        self.temperature = temperature
        self.top_p = top_p
        self.max_gen_len = max_gen_len
        self.max_retries = 5 # Set a limit for the number of retries
        self.timeout = 600  # 设置超时时间10min
        self.api_key = "1790715889671905303"
        self.url = "https://aigc.sankuai.com/v1/openai/native/chat/completions"
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer {}".format(self.api_key) # api_key
        }

    def seed(self, seed: int):
        self._seed = seed
        random.seed(seed)
        np.random.seed(seed)
        torch.manual_seed(seed)
        torch.cuda.manual_seed(seed)
        torch.backends.cudnn.deterministic = True

    
        
    def call_model_api(self, api_url, prompt, max_gen_len):
        data = {
            "model": 'doubao-pro-4k',
            "messages": [
                {
                    "role": "user",
                    "content": f"{prompt}"
                }
            ],
            "tools": None,
            "tool_choice": None,
            "max_tokens": max_gen_len * 2,
            "top_p": self.top_p,
            "temperature": self.temperature,
            "seed": 42
        }
        
        attempt = 0
        try:
            # 这里设置timeout为self.timeout秒
            response = requests.post(api_url, json=data, headers=self.headers, timeout=self.timeout)
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
                response = self.call_model_api(self.url, message, self.max_gen_len)
                if response is None:
                    print("No response received. Retrying...")
                    attempt += 1
                    continue
                response = json.loads(response)

                if "choices" in response and response["choices"]:
                    content = response["choices"][0]["message"]['content']  # 获取第一个completion的文本
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
