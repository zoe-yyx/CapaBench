import argparse
from typing import Optional
from typing import List, Optional
# from llama import Dialog, Llama

import gym
# from rich import print
from rich.markup import escape

import os
import copy
import json
import queue
import random
from web_agent_site_white.envs import WebAgentTextEnv
from web_agent_site_white.models import RandomPolicy
from web_agent_site_white.utils import DEBUG_PROD_SIZE
from util import set_random_seed, extract_purchase_strategy, extract_thought, extract_action, extract_reflection, extract_content
from llm_agent import LLMAgent, OpenAIAgent, BaichuanAgent, APIAgent, DouBaoAgent
from transformers import AutoTokenizer, AutoModelForCausalLM
from transformers.generation.utils import GenerationConfig






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
    
    set_random_seed(0)
    
    print(f"Running with the following settings:")
    print(f"Mode: {modes}")
    print(f"Default Model: {default_model}")
    print(f"Default Tokenizer: {default_tokenizer}")
    print(f"Test Model Name: {test_model_name}")
    print(f"Temperature: {temperature}, Top_p: {top_p}, Max Sequence Length: {max_seq_len}")
    print("Initializing agents and environment...")


    # Initialize default and test agents
    default_agent = LLMAgent(default_model, default_tokenizer, temperature, top_p, max_gen_len)  # not support for llama2 right now
    # test_agent= OpenAIAgent(test_model_name, temperature, top_p, max_gen_len)  # Testing agent
    
    test_agent= DouBaoAgent(temperature, top_p, max_gen_len)  # Testing agent
    print("model", test_model_name)

    # api_url = "" 

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



    # Set up environment
    env = gym.make('WebAgentTextEnv-v0', observation_mode='text', num_products=DEBUG_PROD_SIZE)

    with open("./white.json", 'r') as file:
        data_ids = json.load(file)

    keys_list = list(data_ids.keys())
    keys_list_numeric = [int(key) for key in keys_list]

    try:
        policy = RandomPolicy()
        rewards = []
        trajectory_json = {}
        
        for id in keys_list_numeric:
            env.reset()
            observation = env.observation
            print("\n env.session", env.session, "observation", observation)
            count = 0
            actions_history, thoughts_history = [], []
            reflection = ""
            trajectory_current = []

            ## Step 1: planning  
            if 'planning' in modes:            # Use the specified model based on the mode
                planning_context = test_agent.llm_planning(observation)
            else:
                planning_context = default_agent.llm_planning(observation)
            planning_context = extract_purchase_strategy(planning_context)
            print("-------------------------------------")
            print("planning_context", planning_context)
            print("-------------------------------------")
            # trajectory_current['planning'] = planning_context

            recent_actions = []
            while True:
                ## Step 2: reasoning
                if 'reasoning' in modes:
                    current_thought = test_agent.llm_reasoning(observation, planning_context, actions_history, reflection, count)
                else:
                    current_thought = default_agent.llm_reasoning(observation, planning_context, actions_history, reflection, count)
                current_thought = extract_thought(current_thought)
                thoughts_history.append(current_thought)
                print("current_thought", current_thought)
                # trajectory_current['reasoning'] = current_thought

                ## Step3: action 
                available_actions = env.get_available_actions()
                if 'action' in modes:
                    action = test_agent.llm_action(observation, planning_context, actions_history, thoughts_history, current_thought, available_actions, count)
                else:
                    action = default_agent.llm_action(observation, planning_context, actions_history, thoughts_history, current_thought, available_actions, count)
                print("action", action)        
                action = extract_action(action)
                actions_history.append(action)
                recent_actions.append(action)
                if (len(recent_actions) > 3 and recent_actions[3] != ""):
                    recent_actions[0] = recent_actions[1]
                    recent_actions[1] = recent_actions[2]
                    recent_actions[2] = recent_actions[3]
                    recent_actions[3] = ""
                print("action", action)
                # trajectory_current['action'] = action


                ## Optional Step4: reflection - triggered when the agent repeated the same action for 3 times and when the cicle is over 10
                if (len(recent_actions) > 3 and recent_actions[0] == recent_actions[1] and recent_actions[1] == recent_actions[2]):
                    if 'reflection' in modes:
                        reflection = test_agent.llm_reflection(observation, actions_history, thoughts_history)
                    else:
                        reflection = default_agent.llm_reflection(observation, actions_history, thoughts_history)
                    reflection = extract_reflection(reflection)
                    print("REFLECTION: ", reflection)
                    # trajectory_current['reflection'] = reflection


                observation_next, reward, done, info = env.step(action)
                if count == 15:
                    observation_next, reward, done, info = env.step('click[Buy Now]')


                print(f'Taking action "{escape(action)}" -> Reward = {reward}')

                trajectory_current.append({
                    "observation": observation,
                    "planning_context": planning_context,
                    "reasoning": current_thought,
                    "action": action,
                    "reward": reward
                })

                observation = observation_next

                if done:
                    rewards.append(reward)
                    trajectory_json[str(id)] = trajectory_current
                    break
                count += 1
                if count > 15:
                    rewards.append(0)
                    trajectory_json[str(id)] = trajectory_current
                    break
            print("Average rewards: {}".format(sum(rewards) / len(rewards)))

    finally:
        env.close()
        # Create filename based on test_model_name and mode
        directory = f"user_session_logs/new/test/{test_model_name}"
        if not os.path.exists(directory):
            os.makedirs(directory)
        modes_str = "_".join(modes)
        filename = f"{directory}/traj_{test_model_name}_{modes_str}_Q_modified.json"
        if not os.path.exists(os.path.dirname(filename)):
            try:
                os.makedirs(os.path.dirname(filename))
            except OSError as exc:
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
    parser.add_argument('--default_model', type=str, default='./Meta-Llama-3-8B-Instruct', help='Path to the default model directory.')
    parser.add_argument('--default_tokenizer', type=str, default='./Meta-Llama-3-8B-Instruct/tokenizer.model', help='Path to the default tokenizer.')
    parser.add_argument('--test_model_name', type=str, default='gpt-4-0125-preview', help='Name of the test model.')
    parser.add_argument('--temperature', type=float, default=0, help='Temperature for generation.')
    parser.add_argument('--top_p', type=float, default=0.9, help='Top p for generation.')
    parser.add_argument('--max_seq_len', type=int, default=2048, help='Maximum sequence length.')
    parser.add_argument('--max_batch_size', type=int, default=4, help='Maximum batch size.')
    parser.add_argument('--max_gen_len', type=int, default=1024, help='Maximum generation length.')

    args = parser.parse_args()

    # Call main with all arguments
    main(args.mode, args.default_model, args.default_tokenizer, args.test_model_name,
         args.temperature, args.top_p, args.max_seq_len, args.max_batch_size, args.max_gen_len)
