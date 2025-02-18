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

from util import set_random_seed, extract_purchase_strategy, extract_thought, extract_action, extract_reflection
from llm_agent import LLMAgent, OpenAIAgent
from transformers import AutoTokenizer, AutoModelForCausalLM
from transformers.generation.utils import GenerationConfig
from transformers import BitsAndBytesConfig
import torch
import pandas as pd
from tqdm import tqdm
from prompt.prompt_collection import prompt_few_shot, prompt_system, prompt_system_planning
import re

def extract_first_number(text):
    try:
        match = re.search(r'\d+', text)
        if match:
            return match.group()
        return None
    except:
        return None

def is_equiv(a, b):
    try:
        if a is None or b is None:
            return False
        return float(a) == float(b)
    except:
        return False


def main(
    modes: list,
    default_model: str,
    default_tokenizer: str,
    test_model_name: str,
    temperature: float,
    top_p: float,
    max_seq_len: int,
    max_batch_size: int,
    max_gen_len: Optional[int] = None,
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
    test_agent= OpenAIAgent(test_model_name, temperature, top_p, max_gen_len)  # Testing agent


    


    


    # Create filename based on test_model_name and mode
    directory = f"user_session_logs/create_data/{test_model_name}"
    if not os.path.exists(directory):
        os.makedirs(directory)

    modes_str = "_".join(modes)
    filename = f"{directory}/traj_{test_model_name}_{modes_str}.json"

    if not os.path.exists(os.path.dirname(filename)):
        try:
            os.makedirs(os.path.dirname(filename))
        except OSError as exc:
            if exc.errno != errno.EEXIST:
                raise

    
    
    with open('./evaluation/sampled_SVAMP.json', 'r') as file:
        data = json.load(file)


    header = ["Question", "Correct Answer", "Predicted Answer", "Calculator", "Generated Expression"]
    df = pd.DataFrame(columns=header)

    trajectory_json = {}
    id = 0

    for entry in tqdm(data, desc="Evaluating SVAMP dataset"):
        full_question = entry["Body"] + " " + entry["Question"]
        result, calculator, expression = None, None, None

        
        try:
            response = test_agent.llm_content(prompt_system, full_question)
            print(response)
        except Exception as e:
            error, error_message = True, str(e)
            print(f"An error occurred during the verification process: {e}")

    

        
            
                
        
        try:
            if response['calculator'] == "True":
                calculator = True
                expression = response['algebraic expression']
                result = eval(expression)
            else:
                calculator = False
                result = response['result']
                

        except:
            pass


        data_row = pd.DataFrame([{
            "Question": full_question, 
            "Correct Answer": entry["Answer"], 
            "Predicted Answer": result,
            "Calculator": calculator,
            "Generated Expression": expression
        }])
        
        df = pd.concat([df, data_row], ignore_index=True)
        df.to_csv("output_SVAMP_eval_single.csv", encoding='utf-8', index=False)

    directory = f"user_session_logs/{test_model_name}"
    if not os.path.exists(directory):
        os.makedirs(directory)

    modes_str = "_".join(modes)
    filename = f"{directory}/traj_{test_model_name}_{modes_str}_single.json"

    if not os.path.exists(os.path.dirname(filename)):
        try:
            os.makedirs(os.path.dirname(filename))
        except OSError as exc:
            raise
            if exc.errno != errno.EEXIST:
                raise

    with open(filename, 'w', encoding='utf-8') as file:
        trajectory_str = json.dumps(trajectory_json, indent=4)
        file.write(trajectory_str)

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
    parser.add_argument('--max_gen_len', type=Optional[int], help='Maximum generation length.')

    args = parser.parse_args()

    # Call main with all arguments
    main(args.mode, args.default_model, args.default_tokenizer, args.test_model_name,
         args.temperature, args.top_p, args.max_seq_len, args.max_batch_size, args.max_gen_len)
