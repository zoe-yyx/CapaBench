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

def trim_string_to_100_lines(string):
    lines = string.split('\n')  # 将字符串按换行符分割成行
    if len(lines) > 100:
        trimmed_lines = lines[:100]  # 只保留前 100 行
        trimmed_lines.append('```')  # 添加包含三个反引号的行
        return '\n'.join(trimmed_lines)  # 将行重新拼接成一个字符串
    else:
        return string  # 如果行数不超过 100，直接返回原字符串


def extract_purchase_strategy(text, model):
    pattern = r'```(.*?)```'

    # 使用re.DOTALL标志
    matches = re.findall(pattern, text, re.DOTALL)

    # 打印匹配结果
    try:
        return matches[0] if matches[0] != "" else text
    except:
        return "".join(matches) if "".join(matches) != "" else text


def extract_thought(text, model):
    pattern = r'```(.*?)```'

    # 使用re.DOTALL标志
    matches = re.findall(pattern, text, re.DOTALL)

    # 打印匹配结果
    try:
        return matches[0] if matches[0] != "" else text
    except:
        return "".join(matches) if "".join(matches) != "" else text


def extract_action(text, model):
    text = trim_string_to_100_lines(text)

    pattern = r'```(.*?)```'

    # 使用re.DOTALL标志
    matches = re.findall(pattern, text, re.DOTALL)

    # 打印匹配结果
    try:
        return matches[0]
    except:
        return text
    

    ### TODO: stdout, stderr, coq_data
    
   


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

