import time
import json
import openai
import random
import torch
import numpy as np
from transformers import set_seed as transformers_set_seed
import re


def check_and_adjust_prompt(prompt, max_seq_len):
    prompt_len = len(prompt) 
    if prompt_len > max_seq_len:
        print(f"Original prompt length: {prompt_len}, exceeding max allowed length: {max_seq_len}")
        prompt = prompt[:max_seq_len]
    return prompt
    

def safe_openai_chat_call(**kwargs):
    err_num = 0
    while True:
        try:
            response = openai.ChatCompletion.create(**kwargs)
            return response, err_num
        except:
            time.sleep(0.5)
            err_num += 1


def safe_openai_call(**kwargs):
    err_num = 0
    while True:
        try:
            response = openai.Completion.create(**kwargs)
            return response, err_num
        except:
            time.sleep(0.5)
            err_num += 1


def refine_prompt(prompt, **kwargs):
    for key, value in kwargs.items():
        # print("KEY:")
        # print(key)
        # print("VALUE:")
        # print(value)
        prompt = prompt.replace('$'+key, value)
    return prompt


def set_random_seed(seed: int):
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)

    if torch.cuda.is_available():
        torch.cuda.manual_seed(seed)
        torch.cuda.manual_seed_all(seed)
    
    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = False

    transformers_set_seed(seed)




# def extract_purchase_strategy(text, model):
#     try:
#         if model == 'baichuan':
#             data = json.loads(text)
#         else:
#             data = text
#         if "solution strategy" in data:
#             return data["solution strategy"]
        
        
#     except json.JSONDecodeError:
#         pattern = r"solution strategy:\s*(.*)"
#         match = re.search(pattern, text, re.IGNORECASE)
#         if match:
#             return match.group(1)
#     except:
#         return text
#     return str(text)

def extract_purchase_strategy(text, model):
    pattern = r'```(.*?)```'

    # 使用re.DOTALL标志
    matches = re.findall(pattern, text, re.DOTALL)

    # 打印匹配结果
    try:
        return matches[0]
    except:
        return "".join(matches)




# def extract_thought(text, model):
#     try:
#         # data = json.loads(text)
#         if model == 'baichuan':
#             return text
#             # data = json.loads(text)
#         else:
#             data = text
#         if text:
#             if "thought" in data:
#                 return data["thought"]
#         else:
#             return text
#     except json.JSONDecodeError:
#         pattern = r"thought:\s*(.*)"
#         match = re.search(pattern, text, re.IGNORECASE)
#         if match:
#             return match.group(1)
#     except:
#         pattern = r"thought:\s*(.*)"
#         match = re.search(pattern, text, re.IGNORECASE)
#         if match:
#             return match.group(1)
#     return str(text)

def extract_thought(text, model):
    pattern = r'```(.*?)```'

    # 使用re.DOTALL标志
    matches = re.findall(pattern, text, re.DOTALL)

    # 打印匹配结果
    try:
        return matches[0]
    except:
        return "".join(matches)


# def extract_action(text, model):
#     try:
#         # data = json.loads(text)
#         if model == 'baichuan':
#             data = json.loads(text)
#         else:
#             data = text
#         if text:
#             if ("action" in data) and ("action_params" in data):
#                 return str(data['action']) + '[' + str(data['action_params']) + ']'
#         else:
#             return text
#     except json.JSONDecodeError:
#         pattern = r"action:\s*(.*)"
#         match = re.search(pattern, text, re.IGNORECASE)
#         if match:
#             return match.group(1)
#     except:
#         return text
#     return str(text)

def extract_action(text, model):
    # code_block_pattern = r"```(.*?)```"
    # code_block_match = re.search(code_block_pattern, text, re.DOTALL)  # 使用re.DOTALL来包括换行符

    res = {}
    res["Answer"] = None
    res["tool"] = None
    res["algebraic expression"] = None
    res["key words"] = None
    res["action"] = None
    
    
    code_block = text
    
    # 在提取的代码块中查找Flaw和Improvement
    answer_pattern = r"(?<=Answer: ).*"
    tool_pattern = r"(?<=Tool: ).*"
    algebra_pattern = r"(?<=Algebraic expression: ).*"
    key_pattern = r"(?<=Key words: ).*"
    action_pattern = r"(?<=Action: ).*"
    
    # 使用正则表达式查找内容
    answer_match = re.search(answer_pattern, code_block)
    tool_match = re.search(tool_pattern, code_block)
    algebra_match = re.search(algebra_pattern, code_block)
    key_match = re.search(key_pattern, code_block)
    action_match = re.search(action_pattern, code_block)
    
    # 提取匹配结果，如果没有匹配，则返回 None
    answer = answer_match.group(0) if answer_match else None
    tool = tool_match.group(0) if tool_match else None
    algebra = algebra_match.group(0) if algebra_match else None
    key = key_match.group(0) if key_match else None
    action = action_match.group(0) if action_match else None

    res["Answer"] = answer
    res["tool"] = tool
    res["algebraic expression"] = algebra
    res["key words"] = key
    res["action"] = action
    
    return res
    
   


def extract_reflection(text, model):
    try:
        # data = json.loads(text)
        if model == 'baichuan':
            data = json.loads(text)
        else:
            data = text
        if text:
            if "flaw" in data:
                return data["flaw"]
        else:
            return text
    except json.JSONDecodeError:
        pattern = r"flaw:\s*(.*)"
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            return match.group(1)
    except:
        return text
    return str(text)

def find_first_bracket_content_with_braces(text):
    match = re.search(r'\{[^{}]*\}', text)
    if match:
        return match.group(0)
    return text

