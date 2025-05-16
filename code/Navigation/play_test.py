from pathlib import Path
from typing import Literal,List
from rich import print
from rich.console import Console
import tyro
from dialop.envs import (
    OptimizationEnv, PlanningEnv, MediationEnv
    )
import time
import torch
from dialop.players import HumanPlayer, LLMPlayer,FixedPlayer
from dialop.utils import run, run_multiagent
import os
import random
import numpy as np
import torch
import logging
import json
import sys

import requests
def set_random_seed(seed: int):
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)

    if torch.cuda.is_available():
        torch.cuda.manual_seed(seed)
        torch.cuda.manual_seed_all(seed)

    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = False




class Generator():
    def __init__(self,type,api_key,llama_key) -> None:
        self.type=type
        self.api_key="http://"+api_key
        self.llama_key="http://"+llama_key
        self.mode="remote"
    def text_completion(self,prompts,dialog,temperature=0.1,top_p=.95,stop=["\n\n", "Query", "Query:","\n"]):
        start_time=time.time()
        if self.type=="llama":
            if self.mode=="local":
                url = 'http://localhost:20522/generate'
                data = {
                    'prompts': prompts,
                    'temperature': temperature,
                    'top_p': top_p,
                    'stop': stop,
                    'max_gen_len':200
                }

                response = requests.post(url, json=data)
                return response.json()['response']
            else:
                headers = {
                "Content-Type": "application/json",
                }

                data={"prompt":[dialog],"temperature":0,"stop_word":stop,"max_tokens":300,"multi_turn":True}
                # data={"messages":dialog,"temperature":0.1,"stop":stop,"max_tokens":300}
                url=self.llama_key+":8080"

                response = requests.post(url, json=data, headers=headers)

                retry_times = 0
                answer = ""
                while retry_times < 2:
                    try:
                        resp = response.json()

                        if 'completions' in resp:
                            answer = resp['completions'][0]['text']

                            import re
                            match = re.search(r"Search Results(.+)", answer, re.DOTALL)

                            if match  and "[think]" not in prompts[0]:
                                answer = match.group(0)


                            for i in stop:
                                if i in answer:
                                    answer=answer.split(i)[0]
                            break
                    except:
                        pass
                    logging.info(f"触发限流or模型没有返回结果 重试次数:{retry_times} 等待10秒后重试...")
                    time.sleep(1)
                    retry_times += 1
                    response = requests.post(url, data=data, headers=headers)
                end_time=time.time()
                print("此次回复时间",end_time-start_time)
                return [{'generation':answer}]
        
        else:

            headers = {
            "Content-Type": "application/json",
            }

            prompts=str(prompts)
            data={"prompt":prompts,"temperature":0.1,"stop_word":stop,"max_new_tokens":120}


            import json
            data=json.dumps(data)

            # data={"messages":dialog,"temperature":0.1,"stop":stop,"max_tokens":300}
            url=self.api_key+":8080"

            response = requests.request("POST",url, data=data, headers=headers)
            retry_times = 0
            answer = ""
            while retry_times < 3:
                try:
                    resp = response.json()

                    if 'completions' in resp:
                        answer = resp['completions'][0]['text']
                        import re
                        match = re.search(r"Search Results(.+)", answer, re.DOTALL)
                        if match  and "[think]" not in prompts[0]:
                            answer = match.group(0)

                        match = re.search(r"\[.*?\]", answer)

# 如果找到匹配，将其之前的内容删除
                        if match:
                            answer = answer[match.start():].strip()
                        for i in stop:
                            if i in answer:
                                answer=answer.split(i)[0]
                        break
                except:
                    pass
                logging.info(f"触发限流or模型没有返回结果 重试次数:{retry_times} 等待10秒后重试...")
                time.sleep(1)
                retry_times += 1
                response = requests.post(url, data=data, headers=headers)
            end_time=time.time()
            print("此次回复时间",end_time-start_time)
            return [{'generation':answer}]

def load_prompt(game, player):
    fname = f"{game}_{player}.txt" if game != "optimization" else f"{game}.txt"
    return (Path(__file__).parent / f"prompt/{fname}").read_text()

def main(
    game: Literal["optimization", "planning", "mediation"],
    max_length: int = 30,
    random_seed: int =-1,
    model: Literal["llama","baichuan","gpt4","gpt3","qwen"]="llama",
    partial: bool = False,
    model_ls: List = [0,0,0,0],
    api_key:str = None,
    llama_key:str = None
    ):
    console = Console()
    
    if partial:
        # 定义模型列表
        model_list = ["llama", "other"]
        # 初始化生成器字典
        assert api_key is not None, "API key is not provided"
        generators = {}

        # 创建生成器对象并存储在字典中
        for index, model_name in enumerate(model_list):
            if str(index) in model_ls:
                generators[str(index)] = Generator(model_name,api_key,llama_key)

        # 初始化生成器列表
        generator_ls = [generators[i] for i in model_ls if i in generators]
        generator=None
                
    else:
        generator=Generator(model)
        generator_ls=None


    if  not random_seed==-1:
        import random
        random.seed(random_seed)
        import numpy as np
        np.random.seed(random_seed)
        set_random_seed(random_seed)

    if game == "optimization":
        env = OptimizationEnv()
    elif game == "planning":
        if partial:
            env = PlanningEnv(generator=generator_ls[2])
        else:
            env= PlanningEnv(generator=generator)

    else:
        env = MediationEnv()
    
    # players = {
    #     p: (HumanPlayer(env.instructions[i], p, console) if i == 0 \
    #         else LLMPlayer(generator,load_prompt(game, p), p, console))
    #     for i, p in enumerate(env.players)
    # }
    
    players = {
        p: (FixedPlayer(env.instructions[i], p, console) if i == 0 \
            else LLMPlayer(generator,load_prompt(game, p), p, console,partial=partial,generator_ls=generator_ls))
        for i, p in enumerate(env.players)
    }
    # players = {
    #     p: (
    #        LLMPlayer(generator,load_prompt(game, p), p, console))
    #     for i, p in enumerate(env.players)
    # }
    if game == "mediation":
        players["agent"].prefix = "\nYou to"
        run_multiagent(console, env, players, max_length)
    else:
        
        run(console, env, players, max_length)


tyro.cli(main)
