import time
import json
import openai
import random
import torch
import re
import numpy as np
from transformers import set_seed as transformers_set_seed


def safe_openai_chat_call(**kwargs):
    err_num = 0
    while True:
        try:
            response = openai.ChatCompletion.create(**kwargs)
            return response, err_num
        except:
            time.sleep(0.5)
            err_num += 1



def refine_prompt(prompt, **kwargs):
    for key, value in kwargs.items():
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



def extract_purchase_strategy(text):
    pattern = r'```(.*?)```'
    matches = re.findall(pattern, text, re.DOTALL)

    try:
        return matches[0]
    except:
        return "".join(matches)


def extract_thought(text):
    pattern = r'```(.*?)```'
    matches = re.findall(pattern, text, re.DOTALL)

    try:
        return matches[0]
    except:
        return "".join(matches)




def extract_content(text):
    # Use regex to find content inside two triple single quotes
    pattern = r'```(.*?)```'
    matches = re.findall(pattern, text, re.DOTALL)  # re.DOTALL allows '.' to match newlines
    return matches



def extract_action(text):
    extracted_content = extract_content(text)
    if not extracted_content:
        return "None"
    text = extracted_content[0]

    search_pattern = r"search\[(.*?)\]"
    click_pattern = r"click\[(.*?)\]"
    search_pattern1 = r"search\s*(.*)"
    click_pattern1 = r"click\s*(.*)"
    search_pattern2 = r"search \[(.*?)\]"
    click_pattern2 = r"click \[(.*?)\]"
    search_pattern3 = r"search (.*)"
    click_pattern3 = r"click (.*)"
    search_pattern4 = r"search\[\[(.*?)\]\]"
    click_pattern4 = r"click\[\[(.*?)\]\]"
    search_pattern5 = r"search \[\[(.*?)\]\]"
    click_pattern5 = r"click \[\[(.*?)\]\]"
    none_pattern = r"action\s*None"

    # Search for the search pattern
    search_match = re.search(search_pattern, text, re.IGNORECASE)
    click_match = re.search(click_pattern, text, re.IGNORECASE)
    search_match1 = re.search(search_pattern1, text, re.IGNORECASE)
    click_match1 = re.search(click_pattern1, text, re.IGNORECASE)
    search_match2 = re.search(search_pattern2, text, re.IGNORECASE)
    click_match2 = re.search(click_pattern2, text, re.IGNORECASE)
    search_match3 = re.search(search_pattern3, text, re.IGNORECASE)
    click_match3 = re.search(click_pattern3, text, re.IGNORECASE)
    search_match4 = re.search(search_pattern4, text, re.IGNORECASE)
    click_match4 = re.search(click_pattern4, text, re.IGNORECASE)
    search_match5 = re.search(search_pattern5, text, re.IGNORECASE)
    click_match5 = re.search(click_pattern5, text, re.IGNORECASE)
    none_match = re.search(none_pattern, text, re.IGNORECASE)

    # Process the matches
    if search_match4:
        return "search[" + search_match4.group(1) + "]"
    elif click_match4:
        return "click[" + click_match4.group(1) + "]"
    elif search_match5:
        return "search[" + search_match5.group(1) + "]"
    elif click_match5:
        return "click[" + click_match5.group(1) + "]"
    elif search_match:
        return "search[" + search_match.group(1) + "]"
    elif click_match:
        return "click[" + click_match.group(1) + "]"
    elif search_match2:
        return "search[" + search_match2.group(1) + "]"
    elif click_match2:
        return "click[" + click_match2.group(1) + "]"
    elif search_match3:
        return "search[" + search_match3.group(1) + "]"
    elif click_match3:
        return "click[" + click_match3.group(1) + "]"
    elif search_match1:
        return "search[" + search_match1.group(1) + "]"
    elif click_match1:
        return "click[" + click_match1.group(1) + "]"
        
    elif none_match:
        print("text",text)
        return "None"
    
    return "None"


def extract_reflection(text):
    pattern = r'```(.*?)```'

    matches = re.findall(pattern, text, re.DOTALL)

    try:
        return matches[0]
    except:
        return "".join(matches)