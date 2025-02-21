import argparse
from typing import Optional
from typing import List, Optional
from llama import Dialog, Llama

import gym
# from rich import print
from rich.markup import escape

import os
import copy
import json
import queue
import random

from util import set_random_seed, extract_purchase_strategy, extract_thought, extract_action, extract_reflection, find_first_bracket_content_with_braces
from llm_agent import LLMAgent, OpenAIAgent, APIAgent, DouBaoAgent
from transformers import AutoTokenizer, AutoModelForCausalLM
from transformers.generation.utils import GenerationConfig
from transformers import BitsAndBytesConfig
import torch
import pandas as pd
from tqdm import tqdm
from check_qed import qed, has_sorry
import re



from transformers import AutoTokenizer, AutoModel
import torch

from sftp_interact import *

from check_updated import check_file_update


def main(
    modes: list,
    default_model: str,
    default_tokenizer: str,
    test_model_name: str,
    temperature: float,
    top_p: float,
    max_seq_len: int,
    max_batch_size: int,
    start_index: int,
    original_correct: int,
    ip: str,
    max_gen_len: int,
):
    
    set_random_seed(0)
    
    print(f"Running with the following settings:")
    print(f"Mode: {modes}")
    print(f"Default Model: {default_model}")
    print(f"Default Tokenizer: {default_tokenizer}")
    print(f"Test Model Name: {test_model_name}")
    print(f"Temperature: {temperature}, Top_p: {top_p}, Max Sequence Length: {max_seq_len}")


    print("Initializing agents and environment...")



    # Initialize default and test agents
    default_agent = LLMAgent(default_model, default_tokenizer, temperature, top_p, max_gen_len)
    

    if ip != None:    
        api_url = ip
        test_agent= APIAgent(api_url, temperature, top_p, max_gen_len)
    elif test_model_name == 'doubao-pro-4k':
        test_agent = DouBaoAgent(temperature, top_p, max_gen_len)
        print('测试豆包！！！！！！！！！')
    else:
        test_agent= OpenAIAgent(test_model_name, temperature, top_p, max_gen_len)  # Testing agent

    # Create filename based on test_model_name and mode
    user_session_logs_directory = f"user_session_logs/isabelle/no/{test_model_name}"
    if not os.path.exists(user_session_logs_directory):
        os.makedirs(user_session_logs_directory)

    modes_str = "_".join(modes)


    tmp_mode = ""
    if 'planning' in modes:
        tmp_mode += 'p'
    if 'reasoning' in modes:
        tmp_mode += 'r'
    if 'action' in modes:
        tmp_mode += 'a'
    if 'reflection' in modes:
        tmp_mode += 'f'
    if tmp_mode == "":
        tmp_mode = "default"
    
    directory = f"user_session_logs/isabelle/no/{test_model_name}"
    if not os.path.exists(directory):
        os.makedirs(directory)

    modes_str = "_".join(modes)
    filename = f"{directory}/traj_{test_model_name}_{modes_str}_noTools_new_{start_index}.jsonl"

    if not os.path.exists(os.path.dirname(filename)):
        try:
            os.makedirs(os.path.dirname(filename))
        except OSError as exc:
            raise
            if exc.errno != errno.EEXIST:
                raise



 

    

    with open('./isabelle_data.json', 'r') as file:
        data = json.load(file)

    trajectory_json = {}
    id = start_index
    total = start_index
    correct = original_correct


    for entry in tqdm(data[start_index:], desc="Evaluating isabelle dataset"):
        set_random_seed(0)
        total += 1
        full_question = entry["problem"]
        answer = entry["solution"]
        theorem = entry["theorem"]
        id += 1
        print("Problem: {}".format(full_question))
        print("Answer: {}".format(answer))
        print("Proposition: {}".format(theorem))
        

        reflection = ""
        trajectory_current = []
    
        try:
            if 'planning' in modes:    # Use the specified model based on the mode
                planning_context = test_agent.llm_planning(full_question, theorem)
                planning_context = extract_purchase_strategy(planning_context, test_model_name)
            else:
                planning_context = default_agent.llm_planning(full_question, theorem)
                planning_context = extract_purchase_strategy(planning_context, 'llama')
            
        except Exception as e:
            error, error_message = True, str(e)
            print(f"An error occurred during the planning process: {e}")
            planning_context = "None"
        print("PLANNING!!!!!!!!!!!!!!!!!!!!")
        print(planning_context)
        limit = 10

        results = {}
        action = ""

        while limit > 0:
            limit -= 1
            try:
                if 'reasoning' in modes:
                    reasoning = test_agent.llm_reasoning(", ".join(f"{k}: {v}" for k, v in results.items()), planning_context, action, reflection, full_question, theorem)
                    current_thought = extract_thought(reasoning, test_model_name)
                else:
                    reasoning = default_agent.llm_reasoning(", ".join(f"{k}: {v}" for k, v in results.items()), planning_context, action, reflection, full_question, theorem)
                    current_thought = extract_thought(reasoning, 'llama')
            
                
            except Exception as e:
                error, error_message = True, str(e)
                print(f"An error occurred during the reasoning process: {e}")
                current_thought = reasoning
            print("REASONING!!!!!!!!!!!!!!!!!!!!")
            print(current_thought)

            reflection = ""


            try:
                if 'action' in modes:
                    action = test_agent.llm_action(", ".join(f"{k}: {v}" for k, v in results.items()), planning_context, action, current_thought, full_question, theorem)
                    print("RAW ACTING!!!!!!!!!!!!!!!!!")
                    print(action)
                    action = extract_action(action, test_model_name)
                else:
                    action = default_agent.llm_action(", ".join(f"{k}: {v}" for k, v in results.items()), planning_context, action, current_thought, full_question, theorem)
                    print("RAW ACTING!!!!!!!!!!!!!!!!!")
                    print(action)
                    action = extract_action(action, 'llama')            
            
            except Exception as e:
                error, error_message = True, str(e)
                print(f"An error occurred during the acting process: {e}")
                continue
            print("ACTING!!!!!!!!!!!!!!!!!!!!")
            print(action)

            tmp_isabelle_file = f"tmp_{tmp_mode}.thy"

            with open(tmp_isabelle_file, 'w') as file:
                # 去除action开头的空白字符（包括空格、换行符等）
                action = action.lstrip()
                
                # 检查去除空白字符后的action是否以“lean”开头
                if action.lower().startswith("isabelle"):
                    if action[8:] != None and action[8:] != "":
                        # 如果存在，则去除“lean”再写入文件
                        file.write(action[8:])  # 从第5个字符开始写入，因为“lean”有4个字符
                        print('FILE CONTENT!!!!!!!!!!!!!!!!!!')
                        print(action[8:])  # 这里打印的是去除空白字符后，可能已经修改过的action
                    else:
                        # 如果存在，则去除“lean”再写入文件
                        file.write("None")  # 从第5个字符开始写入，因为“lean”有4个字符
                        print('FILE CONTENT!!!!!!!!!!!!!!!!!!')
                        print("None")  # 这里打印的是去除空白字符后，可能已经修改过的action
                else:
                    # # 如果不存在，则直接写入action
                    # file.write(action)
                    # print('FILE CONTENT!!!!!!!!!!!!!!!!!!')
                    # print(action)  # 这里打印的是去除空白字符后，可能已经修改过的action
                    if action != None and action != "":
                        # 如果存在，则去除“lean”再写入文件
                        file.write(action)  # 从第5个字符开始写入，因为“lean”有4个字符
                        print('FILE CONTENT!!!!!!!!!!!!!!!!!!')
                        print(action)  # 这里打印的是去除空白字符后，可能已经修改过的action
                    else:
                        # 如果存在，则去除“lean”再写入文件
                        file.write("None")  # 从第5个字符开始写入，因为“lean”有4个字符
                        print('FILE CONTENT!!!!!!!!!!!!!!!!!!')
                        print("None")  # 这里打印的是去除空白字符后，可能已经修改过的action

            sftp_upload('jumper.sankuai.com', 'qisiyuan02', '********', tmp_isabelle_file, tmp_isabelle_file)

            check_file_update('jumper.sankuai.com', 22, 'qisiyuan02', '********', f'tmp_{tmp_mode}_isabelle.json', 2)

            
            try:  
                with open(f'tmp_{tmp_mode}_isabelle.json', 'r') as f:  
                    results = json.load(f)  
            except (FileNotFoundError, json.JSONDecodeError) as e:  
                # 初始化一个空字典  
                results = {}  
                
                # 尝试打开文件并读取第2, 3, 4行  
                try:  
                    with open(f'tmp_{tmp_mode}_isabelle.json', 'r') as f:  
                        lines = f.readlines()  
                        
                        # 确保有足够的行  
                        if len(lines) >= 4:  
                            results['StdOut'] = lines[1].strip()  # 第2行  
                            results['StdError'] = lines[2].strip()  # 第3行  
                            results['ReturnCode'] = lines[3].strip()  # 第4行  
                        else:  
                            # 如果不足4行，用空字符串填充  
                            results['StdOut'] = lines[1].strip() if len(lines) > 1 else ''  
                            results['StdError'] = lines[2].strip() if len(lines) > 2 else ''  
                            results['ReturnCode'] = lines[3].strip() if len(lines) > 3 else ''  
                except Exception as file_error:  
                    # 如果在读取文件行时发生任何错误，使用全空字符串  
                    print(f"Error reading file lines: {file_error}")  
                    results = {'StdOut': '', 'StdError': '', 'ReturnCode': ''}  

            # 这里results是一包含StdOut, StdError, ReturnCode三个key的字典

            for k, v in results.items():
                print(f"{k}: {v}")
                # print("Stdout: No more goals." in result) 
                # print(f"Stderr: {proposition} <" in result)


            

            
            #### TODO: 实现isabelle交互;增添参数控制评测开始位置;改进细节
            try:
                if has_sorry(action, theorem):
                    if 'reflection' in modes:
                        reflection = test_agent.llm_reflection(", ".join(f"{k}: {v}" for k, v in results.items()), action, current_thought, full_question, theorem)
                        # reflection = extract_reflection(reflection, test_model_name)
                    else:
                        reflection = default_agent.llm_reflection(", ".join(f"{k}: {v}" for k, v in results.items()), action, current_thought, full_question, theorem)
                        # reflection = extract_reflection(reflection, 'llama')
                    print("REFLECTING!!!!!!!!!!!!!!!!!!!!")
                    print(reflection)  
                elif qed(results, action, full_question, theorem):
                    trajectory_current.append({
                        "observation": full_question,
                        "planning_context": planning_context,
                        "reasoning": current_thought,
                        "reflection": reflection,
                        "action": "Confirm final proving process: {}".format(action),
                        
                    })
                    correct += 1
                    break
                else:
                    if 'reflection' in modes:
                        reflection = test_agent.llm_reflection(", ".join(f"{k}: {v}" for k, v in results.items()), action, current_thought, full_question, theorem)
                        # reflection = extract_reflection(reflection, test_model_name)
                    else:
                        reflection = default_agent.llm_reflection(", ".join(f"{k}: {v}" for k, v in results.items()), action, current_thought, full_question, theorem)
                        # reflection = extract_reflection(reflection, 'llama')
                    print("REFLECTING!!!!!!!!!!!!!!!!!!!!")
                    print(reflection)  
            except:
                action = "Invalid action!!!"
            
            trajectory_current.append({
                "observation": full_question,
                "planning_context": planning_context,
                "reasoning": current_thought,
                "reflection": reflection,
                "action": action,
                
            })
       
        print(f"Current accuracy: {correct} / {total} = {correct / total}")
        new_data = dict()
        new_data[str(id)] = trajectory_current
        with open(filename, 'a') as f:
            # 使用 json.dumps 将字典转换为 JSON 字符串并写入文件
            f.write(json.dumps(new_data) + '\n')
        

            
                
        


    print(f"Data has been saved to {filename}")





if __name__ == "__main__":
    # Setup argument parser
    parser = argparse.ArgumentParser(description='Control the model through CLI.')
    parser.add_argument('--mode', 
                        type=str, 
                        nargs='+', 
                        choices=['planning', 'reasoning', 'action', 'reflection', 'default'], 
                        help='The operational mode(s) to use. Choose 1 to 4 modes.')
    parser.add_argument('--default_model', type=str, default='/home/hadoop-aipnlp/dolphinfs_hdd_hadoop-aipnlp/yangyingxuan/webshop/repo/llama3/Meta-Llama-3-8B-Instruct', help='Path to the default model directory.')
    parser.add_argument('--default_tokenizer', type=str, default='/home/hadoop-aipnlp/dolphinfs_hdd_hadoop-aipnlp/yangyingxuan/webshop/repo/llama3/Meta-Llama-3-8B-Instruct/tokenizer.model', help='Path to the default tokenizer.')
    parser.add_argument('--test_model_name', type=str, default='gpt-4-0125-preview', help='Name of the test model.')
    parser.add_argument('--temperature', type=float, default=0, help='Temperature for generation.')
    parser.add_argument('--top_p', type=float, default=0.9, help='Top p for generation.')
    # parser.add_argument('--max_seq_len', type=int, default=1000, help='Maximum sequence length.')
    parser.add_argument('--max_seq_len', type=int, default=2048, help='Maximum sequence length.')
    parser.add_argument('--max_batch_size', type=int, default=4, help='Maximum batch size.')
    parser.add_argument('--max_gen_len', type=int, default=1024, help='Maximum generation length.')
    parser.add_argument('--start_index', type=int, default=0, help='Start index of data.')
    parser.add_argument('--original_correct', type=int, default=0, help='Original correct num of data.')
    parser.add_argument('--ip', type=str, default=None, help='IP address of API Agent.')

    args = parser.parse_args()

    # Call main with all arguments
    main(args.mode, args.default_model, args.default_tokenizer, args.test_model_name,
         args.temperature, args.top_p, args.max_seq_len, args.max_batch_size, args.start_index, args.original_correct, args.ip, args.max_gen_len)
