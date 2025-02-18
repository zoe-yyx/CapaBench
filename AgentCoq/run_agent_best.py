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
from llm_agent import LLMAgent, OpenAIAgent, APIAgent
from transformers import AutoTokenizer, AutoModelForCausalLM
from transformers.generation.utils import GenerationConfig
from transformers import BitsAndBytesConfig
import torch
import pandas as pd
from tqdm import tqdm
from check_qed import qed, has_error, has_admitted
import re



from transformers import AutoTokenizer, AutoModel
import torch

from sftp_interact import *

from check_updated import check_file_update


def remove_overlapping_lines_ignore_empty(str1, str2):
    # 将字符串按行拆分
    lines1 = [line for line in str1.splitlines() if line.strip()]
    lines2 = [line for line in str2.splitlines() if line.strip()]
    
    # 寻找最大可能的重叠部分（以 lines2 为参考，最多检查 lines2 的行数）
    max_overlap = min(len(lines1), len(lines2))
    
    # 从最大重叠部分开始比较
    overlap_index = 0
    for i in range(1, max_overlap + 1):
        if lines1[-i:] == lines2[:i]:  # 比较 str1 结尾的 i 行 和 str2 开头的 i 行
            overlap_index = i
    
    # 删除第二个字符串中与第一个字符串重叠的部分
    result_lines = lines2[overlap_index:]
    
    # 将结果合并回一个字符串
    return "\n".join(result_lines)


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



    print("Initializing agents and environment...")

    ip_planning = 'http://10.140.37.146:8080'
    ip_reasoning = 'http://10.140.222.31:8080'
    ip_acting = 'http://10.140.222.31:8080'
    ip_reflecting = 'http://10.118.238.157:8080'
    p_agent = APIAgent(ip_planning, temperature, top_p, max_gen_len)
    r_agent = APIAgent(ip_reasoning, temperature, top_p, max_gen_len)
    a_agent = APIAgent(ip_acting, temperature, top_p, max_gen_len)
    f_agent = APIAgent(ip_reflecting, temperature, top_p, max_gen_len)




    



    # Create filename based on test_model_name and mode
    user_session_logs_directory = f"user_session_logs/coq/no/best"
    if not os.path.exists(user_session_logs_directory):
        os.makedirs(user_session_logs_directory)

    


    directory = f"user_session_logs/coq/no/best"
    if not os.path.exists(directory):
        os.makedirs(directory)

    filename = f"{directory}/traj_best_noTools_new_{start_index}.jsonl"

    if not os.path.exists(os.path.dirname(filename)):
        try:
            os.makedirs(os.path.dirname(filename))
        except OSError as exc:
            raise
            if exc.errno != errno.EEXIST:
                raise



 

    

    with open('./coq_data.json', 'r') as file:
        data = json.load(file)

    trajectory_json = {}
    id = start_index
    total = start_index
    correct = original_correct


    for entry in tqdm(data[start_index:], desc="Evaluating Coq dataset"):
        set_random_seed(0)
        total += 1
        full_question = entry["problem"]
        answer = entry["proof"]
        proposition = entry["proposition"]
        id += 1
        print("Problem: {}".format(full_question))
        print("Answer: {}".format(answer))
        print("Proposition: {}".format(proposition))
        

        reflection = ""
        trajectory_current = []
    
        try:

            planning_context = p_agent.llm_planning(full_question, proposition)
            planning_context = extract_purchase_strategy(planning_context, test_model_name)
            
            
        except Exception as e:
            error, error_message = True, str(e)
            print(f"An error occurred during the planning process: {e}")
            planning_context = "None"
        print("PLANNING!!!!!!!!!!!!!!!!!!!!")
        print(planning_context)
        limit = 10

        results = []
        action = ""

        while limit > 0:
            limit -= 1
            try:
        
                reasoning = r_agent.llm_reasoning("".join(results), planning_context, action, reflection, full_question, proposition)
                current_thought = extract_thought(reasoning, test_model_name)

            
                
            except Exception as e:
                error, error_message = True, str(e)
                print(f"An error occurred during the reasoning process: {e}")
                current_thought = reasoning
            print("REASONING!!!!!!!!!!!!!!!!!!!!")
            print(current_thought)

            reflection = ""


            try:
     
                action = a_agent.llm_action("".join(results), planning_context, action, current_thought, full_question, proposition)
                print("RAW ACTING!!!!!!!!!!!!!!!!!")
                print(action)
                action = extract_action(action, test_model_name)
                       
            
            except Exception as e:
                error, error_message = True, str(e)
                print(f"An error occurred during the acting process: {e}")
                continue
            print("ACTING!!!!!!!!!!!!!!!!!!!!")
            print(action)

            tmp_coq_file = f"tmp_best.v"

            with open(tmp_coq_file, 'w') as file:
                question_delete_line = full_question.replace('(**********)\n(** Fill in your proof here*)\n(**********)', '')
                file.write(question_delete_line)
                pure_proof = remove_overlapping_lines_ignore_empty(question_delete_line, action)
                file.write(pure_proof)
                print('FILE CONTENT!!!!!!!!!!!!!!!!!!')
                print(question_delete_line)
                print(pure_proof)

            sftp_upload('jumper.sankuai.com', 'qisiyuan02', '********', tmp_coq_file, tmp_coq_file)

            check_file_update('jumper.sankuai.com', 22, 'qisiyuan02', '********', f'tmp_best.json', 2)

            
            with open(f'tmp_best.json', 'r') as f:
                results = json.load(f)

            for result in results:
                print(result)
                # print("Stdout: No more goals." in result) 
                # print(f"Stderr: {proposition} <" in result)


            

            
            #### TODO: 实现coq交互
            try:
                if has_admitted(action):
                    reflection = f_agent.llm_reflection("".join(results), action, current_thought, full_question, proposition)
       
                  
                    print("REFLECTING!!!!!!!!!!!!!!!!!!!!")
                    print(reflection)  

                elif qed(results, proposition):
                    trajectory_current.append({
                        "observation": full_question,
                        "planning_context": planning_context,
                        "reasoning": current_thought,
                        "reflection": reflection,
                        "action": "Confirm final proving process: {}".format(action),
                        
                    })
                    correct += 1
                    break
                elif has_error(results, proposition):

                    reflection = f_agent.llm_reflection("".join(results), action, current_thought, full_question, proposition)
                
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
