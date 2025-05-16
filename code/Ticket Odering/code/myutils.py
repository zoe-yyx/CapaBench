import re
import time
import openai
import numpy as np
import random
import torch
from transformers import set_seed as transformers_set_seed

'''
将agent输出的用户航班组转换成数据结构
agent输出示例:
Flight for user 0: 6 | Alaska | 516 | 05/31 11:58 PM - 03:59 AM  
Flight for user 1: 6 | United | 372 | 06/01 10:57 AM - 03:57 PM
'''
def trans_agent_output(agent_output):
    # print(agent_output)
    # input("Please wait")
    pattern = r"Flight for User \d+: (\d+) \| (\w+) \| (\d+) \| (\d{2}/\d{2}\s\d{2}:\d{2}\s[APM]{2})\s-\s(\d{2}:\d{2}\s[APM]{2})"
    # print(f"pattern: {pattern}")
    # input("Please wait")
    matches = re.findall(pattern, agent_output)

    result = []
    for match in matches:
        flight_id, carrier, price, start, end = match
        result.append({
            "id": int(flight_id),
            "carrier": carrier,
            "price": int(price),
            "start": start,
            "end": end
        })
    
    # print(result)
    # input("please wait")
    
    if len(result) < 2:
        return None
    else:
        return (result[0], result[1])
    
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

def make_observation(user0_data, user1_data, long_version=False):
    obs = ""
    obs += "User 0 Information\n"
    obs += "Flights:\n"
    obs += "id | carrier | price | times\n"
    for flight in user0_data["Flights"]:
        obs += f"{flight['id']} | {flight['carrier']} | {flight['price']} | {flight['start']} - {flight['end']}\n"
    obs += "Calendar:\n"
    obs += "id | times\n"
    for calendar in user0_data["Shared calendar (visible to assistant)"]:
        obs += f"{calendar['id']} | {calendar['start']} - {calendar['end']}\n"
    obs += "User 1 Information\n"
    obs += "Flights:\n"
    obs += "id | carrier | price | times\n"
    for flight in user1_data["Flights"]:
        obs += f"{flight['id']} | {flight['carrier']} | {flight['price']} | {flight['start']} - {flight['end']}\n"
    obs += "Calendar:\n"
    obs += "id | times\n"
    for calendar in user1_data["Shared calendar (visible to assistant)"]:
        obs += f"{calendar['id']} | {calendar['start']} - {calendar['end']}\n"

    if long_version:
        obs += "\nUser 0: Here is my own calendars, and the importance part shows the importance of the corresponding calendar.\n"
        obs += "Private calendar:\nid | importance | times\n"
        for calendar in user0_data["Private calendar"]:
            obs += f"{calendar['id']} | ({calendar['importance']}) | {calendar['start']} - {calendar['end']}\n"
            
        obs += "\nUser 1: Here is my own calendars, and the importance part shows the importance of the corresponding calendar.\n"
        obs += "Private calendar:\nid | importance | times\n"
        for calendar in user1_data["Private calendar"]:
            obs += f"{calendar['id']} | ({calendar['importance']}) | {calendar['start']} - {calendar['end']}\n"

    # print(obs)
    # input("Please wait")
    return obs

def prompt_in_planning():
    prompt = ""
    with open("/home/hadoop-aipnlp/dolphinfs_hdd_hadoop-aipnlp/huhaoyi02/dialop-mediation/dialop/game_prompt/planning_prompt.txt", 'r', encoding='utf-8') as f:
        prompt = f.read()
    
    return prompt
