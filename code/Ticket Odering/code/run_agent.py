import argparse
from typing import Optional
from typing import List, Optional
# from llama import Dialog, Llama

# from rich import print
from rich.markup import escape
from rich.progress import track

import os
import copy
import json
import queue
import random

import sys
import os
import copy
import time

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# from dialop import myutils
# from dialop.llm_agent.llm_agent import *
import myutils
from dialop import myevaluate
from llm_agent.llm_agent import *


def main(
    modes: list,
    default_model: str,
    default_tokenizer: str,
    test_model_name: str,
    temperature: float,
    top_p: float,
    max_seq_len: int,
    max_batch_size: int,
    max_gen_len: int,
):
    
    myutils.set_random_seed(0)
    
    print(f"Running with the following settings:")
    print(f"Mode: {modes}")
    print(f"Default Model: {default_model}")
    print(f"Default Tokenizer: {default_tokenizer}")
    print(f"Test Model Name: {test_model_name}")
    print(f"Temperature: {temperature}, Top_p: {top_p}, Max Sequence Length: {max_seq_len}")
    print("Initializing agents and environment...")


    # Initialize default and test agents
    # default_agent = APIAgent("http://10.166.170.87:8090", temperature, top_p, max_gen_len)  # Default agent
    # default_agent = LLMAgent(default_model, default_tokenizer, temperature, top_p, max_gen_len)  # not support for llama2 right now
    # default_agent = OpenAIAgent(default_model, temperature, top_p, max_gen_len)  # not support for llama2 right now
    # test_agent= OpenAIAgent(test_model_name, temperature, top_p, max_gen_len)  # Testing agent

    # test_agent = APIAgent("http://10.114.254.149:8080", temperature, top_p, max_gen_len)

    ### claude_3.5_sonnet··
    # print("model", test_model_name)
    # api_url = "http://10.114.60.40:8080" 

    ### GLM4
    # print("model", test_model_name)
    # api_url = "http://10.166.111.83:8080" 

    ### Mistral_8x7B_MOE
    # print("model", test_model_name)
    # api_url = "http://10.166.154.27:8080" 
    
    
    # print("model", test_model_name)
    # api_url = "http://10.166.173.84:8080" 

    

    # Qwen2.5-32b-ins
    if test_model_name == "qwen":
        default_agent = APIAgent("http://10.166.146.78:8080", temperature, top_p, max_gen_len)
        test_agent = APIAgent("http://10.166.172.96:8080", temperature, top_p, max_gen_len)
    # gpt4-turbo
    elif test_model_name == "gpt4-turbo":
        test_agent = APIAgent("http://10.114.254.149:8080", temperature, top_p, max_gen_len)
    # llama3-70b 
    elif test_model_name == "llama3-70B":
        test_agent = APIAgent("http://10.166.179.58:8080", temperature, top_p, max_gen_len)
    # Mistral-7B
    elif test_model_name == "Mistral-7B":
        test_agent = APIAgent("http://10.166.184.49:8080", temperature, top_p, max_gen_len)
    # doubao
    elif test_model_name == "doubao":
        default_agent = APIAgent("http://10.166.185.104:8080", temperature, top_p, max_gen_len)
        test_agent = APIAgent("http://10.140.208.42:8080", temperature, top_p, max_gen_len)
    # 
    elif test_model_name == "Mistral-8X7B":
        default_agent = APIAgent("http://10.166.185.104:8080", temperature, top_p, max_gen_len)
        test_agent = APIAgent("http://10.166.154.8:8080", temperature, top_p, max_gen_len)
        
    # # mixtral-8X7b
    # planning_agent = APIAgent("http://10.166.159.8:8080", temperature, top_p, max_gen_len)
    # # gpt4-turbo
    # reasoning_agent = APIAgent("http://10.146.197.63:8080", temperature, top_p, max_gen_len)
    # reflection_agent = APIAgent("http://10.146.197.63:8080", temperature, top_p, max_gen_len)
    # # claude
    # action_agent = APIAgent("http://10.243.83.69:8080", temperature, top_p, max_gen_len)

    # print("model", test_model_name)
    # api_url = "http://10.166.178.72:8080" 
        

    # test_agent= APIAgent(api_url, temperature, top_p, max_gen_len)

    # default_tokenizer = AutoTokenizer.from_pretrained(default_model,trust_remote_code=True)
    # default_model = AutoModelForCausalLM.from_pretrained(default_model,                                                 
    #                                             trust_remote_code=True,
    #                                             use_cache=False,
    #                                             device_map="auto")
    # config = GenerationConfig(**{
    #     "assistant_token_id": 196,
    #     "bos_token_id": 1,
    #     "do_sample": True,
    #     "eos_token_id": 2,
    #     "max_new_tokens": 500,
    #     "pad_token_id": 0,
    #     "repetition_penalty": 1.05,
    #     "temperature": 0.3,
    #     "top_k": 5,
    #     "top_p": 0.85,
    #     "user_token_id": 195
    #     })
    # default_model.generation_config = config
    # default_agent = BaichuanAgent(default_model, default_tokenizer, temperature, top_p, max_gen_len)



    user0_datas = None
    user1_datas = None

    # Load user data
    with open("dialop/game_prompt/user0.json", 'r', encoding='utf-8') as f:
        user0_datas = json.load(f)
    with open("dialop/game_prompt/user1.json", 'r', encoding='utf-8') as f:
        user1_datas = json.load(f)

    # choose the user data randomly
    user_data_comb = [(random.choice(user0_datas), random.choice(user1_datas)) for _ in range(150)]
    
    rewards = []   # 记录agent产生航班组的排名得分(1-rank/total_rank)，数值越高，航班组质量越好
    errors = []    # 记录agent产生虚假航班的次数
    # trajectory_json = {}  # 记录PRAF迭代过程中的数据

    try:
        start_time = time.time()

        for (user0_data, user1_data) in track(user_data_comb):
            iter_start_time = time.time()

            # 创建评价框架，并为航班组排序
            eva_flame = myevaluate.EvaluateFlame(copy.deepcopy(user0_data), copy.deepcopy(user1_data))
            eva_flame.get_final_rank()

            count = 0     # 记录PRAF迭代次数
            error = 0     # 存储agent产生虚假航班的次数
            reward = 0    # 存储agent产生航班组的排名得分(rank/total_rank)，数值越低，航班组质量越好

            actions_history, thoughts_history = [], []
            reflection = ""
            # trajectory_current = []

            ## Step 1: planning
            planning_start_time = time.time()
            # planning_context = planning_agent.llm_planning()
            if 'planning' in modes:            # Use the specified model based on the mode
                # planning_context = test_agent.llm_planning(observation)
                planning_context = test_agent.llm_planning()
            else:
                # planning_context = default_agent.llm_planning(observation)
                planning_context = default_agent.llm_planning()
            planning_end_time = time.time()
            print(f"Planning time: {planning_end_time - planning_start_time} seconds")

            print("-------------------------------------")
            print(f"planning: \n{planning_context}")
            print("-------------------------------------")

            observation = myutils.make_observation(user0_data, user1_data, long_version=True)
            while True:
                ## Step 2: reasoning
                reasoning_start_time = time.time()
                # current_thought = reasoning_agent.llm_reasoning(observation, planning_context, actions_history, reflection)
                if 'reasoning' in modes:
                    current_thought = test_agent.llm_reasoning(observation, planning_context, actions_history, reflection)
                    # current_thought = test_agent.llm_reasoning(observation, planning_context, reflection)
                else:
                    current_thought = default_agent.llm_reasoning(observation, planning_context, actions_history, reflection)
                    # current_thought = default_agent.llm_reasoning(observation, planning_context, reflection)
                reasoning_end_time = time.time()
                print(f"Reasoning time: {reasoning_end_time - reasoning_start_time} seconds")
                
                
                thoughts_history.append(current_thought)
                # 避免thoughts_history过长
                thoughts_history = thoughts_history[-2:]
                print("-------------------------------------")
                print(f"reasoning: \n{current_thought}")
                print("-------------------------------------")


                ## Step3: action 
                action_start_time = time.time()
                # action = action_agent.llm_action(observation, planning_context, current_thought)
                if 'action' in modes:
                    # action = test_agent.llm_action(observation, planning_context, actions_history, thoughts_history, current_thought, available_actions)
                    action = test_agent.llm_action(observation, planning_context, current_thought)
                else:
                    action = default_agent.llm_action(observation, planning_context, current_thought)
                    # action = default_agent.llm_action(observation, planning_context, actions_history, thoughts_history, current_thought)
                action_end_time = time.time()
                print(f"Action time: {action_end_time - action_start_time} seconds")
                
                # actions_history.append(action)
                # 避免actions_history过长
                # actions_history = actions_history[-2:]
                print("-------------------------------------")
                print(f"action: \n{action}")
                print("-------------------------------------")
                

                # 计算动作reward
                try:
                    agent_flight_comb = myutils.trans_agent_output(action)
                    # 将agent产生的航班组加入到actions_history中
                    actions_history.append(agent_flight_comb)
                    print("-------------------------------------")
                    print(f"my actions_history: \n{actions_history}")
                    print("-------------------------------------")
                    reward = 1 - eva_flame.get_agent_rank(agent_flight_comb)/len(eva_flame.all_flight_combs)
                except Exception as e:
                    print(f"Error: {e}")
                    error += 1
                    reward = 0


                # refletion - triggered when the agent chooses the bad flight that is not in the top 20% of the rank
                reflection = ""
                if reward < 0.8:
                    reflection_start_time = time.time()
                    # reflection = reflection_agent.llm_reflection(observation, actions_history, thoughts_history)
                    if 'reflection' in modes:
                        reflection = test_agent.llm_reflection(observation, actions_history, thoughts_history)
                    else:
                        reflection = default_agent.llm_reflection(observation, actions_history, thoughts_history)
                    reflection_end_time = time.time()
                    print(f"Reflection time: {reflection_end_time - reflection_start_time} seconds")
                    
                    print("-------------------------------------")
                    print(f"reflection: \n{reflection}")
                    print("-------------------------------------")

                    if not reflection:
                        reflection = ""



                if count > 10:
                    rewards.append(reward)
                    errors.append(error)
                    break

                count += 1
            
            iter_end_time = time.time()
            print(f"One iteration time: {iter_end_time - iter_start_time} seconds")

        end_time = time.time()
        print(f"Total time: {end_time - start_time} seconds")
        
    finally:
        
        comb = ["Pd", "Rd", "Ad", "Fd"]
        if 'planning' in modes:
            comb[0] = "Pt"
        if 'reasoning' in modes:
            comb[1] = "Rt"
        if 'action' in modes:
            comb[2] = "At"
        if 'reflection' in modes:
            comb[3] = "Ft"
        comb = (comb[0], comb[1], comb[2], comb[3])
        average_reward = sum(rewards) / len(rewards)
        shapley_values_path = f"dialop/shapley_values_new_{test_model_name}.json"
        if os.path.exists(shapley_values_path) and os.path.getsize(shapley_values_path) > 0:
            with open(shapley_values_path, 'r', encoding='utf-8') as f:
                shapley_values = json.load(f)
        else:
            shapley_values = {}

        shapley_values[str(comb)] = average_reward

        with open(shapley_values_path, 'w', encoding='utf-8') as f:
            json.dump(shapley_values, f, indent=4)
        

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
    # parser.add_argument('--default_model', type=str, default='gpt-3.5-turbo', help='Path to the default model directory.')
    # parser.add_argument('--default_tokenizer', type=str, default='/home/hadoop-aipnlp/dolphinfs_hdd_hadoop-aipnlp/yangyingxuan/webshop/repo/llama3/Meta-Llama-3-8B-Instruct/tokenizer.model', help='Path to the default tokenizer.')
    parser.add_argument('--test_model_name', type=str, default='gpt4-turbo', help='Name of the test model.')
    parser.add_argument('--temperature', type=float, default=0, help='Temperature for generation.')
    parser.add_argument('--top_p', type=float, default=0.9, help='Top p for generation.')
    parser.add_argument('--max_seq_len', type=int, default=2048, help='Maximum sequence length.')
    parser.add_argument('--max_batch_size', type=int, default=4, help='Maximum batch size.')
    parser.add_argument('--max_gen_len', type=int, default=1024, help='Maximum generation length.')

    args = parser.parse_args()

    # Call main with all arguments
    main(args.mode, args.default_model, args.default_tokenizer, args.test_model_name,
         args.temperature, args.top_p, args.max_seq_len, args.max_batch_size, args.max_gen_len)
