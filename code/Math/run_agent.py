import argparse
import os
import json
from util import set_random_seed, extract_purchase_strategy, extract_thought, extract_action, extract_reflection, find_first_bracket_content_with_braces
from llm_agent import LLMAgent, APIAgent
from transformers import AutoTokenizer, AutoModelForCausalLM
from transformers.generation.utils import GenerationConfig
from transformers import BitsAndBytesConfig
import torch
from tqdm import tqdm
from math_equivalence import is_equiv
from dataset.util import clean_numbers, last_boxed_only, last_boxed_only_string
from calculator import safe_eval
from transformers import AutoTokenizer, AutoModel
import torch



def remove_boxed(s):
    left = "\\boxed{"
    try:
        assert s[:len(left)] == left
        assert s[-1] == "}"
        return s[len(left):-1]
    except:
        return None
    

## 启动“搜索引擎”
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
tokenizer = AutoTokenizer.from_pretrained('./Bert')
model = AutoModel.from_pretrained('./Bert').to(device)


# 函数：计算两个句子的相似度
def get_similarity(sentence1, sentence2):
    # 对两个句子进行编码，并将数据移动到GPU
    tokens1 = tokenizer(sentence1, return_tensors='pt', padding=True, truncation=True).to(device)
    tokens2 = tokenizer(sentence2, return_tensors='pt', padding=True, truncation=True).to(device)
    
    # 获取句子的embeddings
    with torch.no_grad():
        embeddings1 = model(**tokens1).last_hidden_state.mean(dim=1)
        embeddings2 = model(**tokens2).last_hidden_state.mean(dim=1)
    
    # 计算余弦相似度
    similarity = torch.nn.functional.cosine_similarity(embeddings1, embeddings2)
    return similarity.item()

def call_search_engine(key, theorems):
    ## TODO: call search engine like bing to retrive key, 
    ##       then return the most relavant result.
    # 计算每个定理与问题的相似度，并排序
    similarities = [(theorem, get_similarity(key, theorem)) for theorem in theorems]
    similarities.sort(key=lambda x: x[1], reverse=True)  # 按相似度降序排序

    # 输出最相关的三个定理
    top_theorems = similarities[:3]
    for theorem, sim in top_theorems:
        print(f"{theorem}: 相似度 = {sim}")
    return top_theorems


def read_and_concatenate_json_lists(folder_path):  
    # 初始化一个空列表来存储所有JSON文件中的列表  
    all_lists = []  
  
    # 遍历指定文件夹  
    for filename in os.listdir(folder_path):  
        # 检查文件是否以.json结尾  
        if filename.endswith('.json'):  
            # 构造文件的完整路径  
            file_path = os.path.join(folder_path, filename)  
              
            # 尝试打开并读取JSON文件  
            try:  
                with open(file_path, 'r', encoding='utf-8') as file:  
                    # 加载JSON数据  
                    data = json.load(file)  
                      
                    # 检查数据是否为列表，如果是，则添加到all_lists中  
                    if isinstance(data, list):  
                        all_lists.extend(data)  
                    else:  
                        print(f"Warning: {filename} does not contain a list, skipping.")  
            except json.JSONDecodeError:  
                print(f"Error decoding JSON in {filename}, skipping.")  
            except Exception as e:  
                print(f"An error occurred while processing {filename}: {e}")  
  
    # 返回拼接后的列表  
    return all_lists  
  


def main(
    modes: list,
    default_model: str,
    default_tokenizer: str,
    test_model_name: str,
    temperature: float,
    top_p: float,
    max_seq_len: int,
    max_batch_size: int,
    category: str,
    start_index: int,
    original_correct: int,
    ip: str,
    max_gen_len: int
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
    api_url = ip
    test_agent= APIAgent(api_url, temperature, top_p, max_gen_len)

    directory = f"user_session_logs/new_{category}/multi/{test_model_name}"
    if not os.path.exists(directory):
        os.makedirs(directory)


    modes_str = "_".join(modes)
    filename = f"{directory}/traj_{test_model_name}_{modes_str}_multiTools_new_{start_index}.jsonl"

    if not os.path.exists(os.path.dirname(filename)):
        try:
            os.makedirs(os.path.dirname(filename))
        except OSError as exc:
            raise
            if exc.errno != errno.EEXIST:
                raise
    
    if category == 'algebra':
        with open('./algebra_knowledge.json','r') as f:
            theorems = json.load(f)
        
        # 调用函数并打印结果  
        with open('new_algebra_total.json', 'r') as f:
            data = json.load(f)
    else:
        with open('./geometry_knowledge.json','r') as f:
            theorems = json.load(f)
        
        # 调用函数并打印结果  
        with open('new_geometry_total.json', 'r') as f:
            data = json.load(f)

    trajectory_json = {}
    id = start_index

    total = start_index
    correct = original_correct


    for entry in tqdm(data[start_index :], desc="Evaluating Algebra dataset"):
        total += 1
        full_question = entry["problem"]
        answer = remove_boxed(last_boxed_only_string(entry["solution"]))
        print("Problem: {}".format(full_question))
        print("Answer: {}".format(answer))
        result, calculator, expression = None, None, None

        actions_history, thoughts_history = [], []
        reflection = ""
        trajectory_current = []
        recent_actions = []
        try:
            if 'planning' in modes:    # Use the specified model based on the mode
                planning_context = test_agent.llm_planning(full_question)
                planning_context = extract_purchase_strategy(planning_context, test_model_name)
            else:
                planning_context = default_agent.llm_planning(full_question)
                planning_context = extract_purchase_strategy(planning_context, 'llama')

        except Exception as e:
            error, error_message = True, str(e)
            print(f"An error occurred during the planning process: {e}")
            planning_context = "None"
        print("PLANNING!!!!!!!!!!!!!!!!!!!!")
        print(planning_context)
        limit = 10

        while limit > 0:
            limit -= 1
            try:
                if 'reasoning' in modes:
                    reasoning = test_agent.llm_reasoning(full_question, planning_context, actions_history, reflection)
                    current_thought = extract_thought(reasoning, test_model_name)
                else:
                    reasoning = default_agent.llm_reasoning(full_question, planning_context, actions_history, reflection)
                    current_thought = extract_thought(reasoning, 'llama')
            
                
            except Exception as e:
                error, error_message = True, str(e)
                print(f"An error occurred during the reasoning process: {e}")
                current_thought = reasoning
            print("REASONING!!!!!!!!!!!!!!!!!!!!")
            print(current_thought)
            thoughts_history.append(current_thought)

            try:
                # action = test_agent.llm_action(full_question , planning_context, actions_history, thoughts_history, current_thought)
                if 'action' in modes:
                    action = test_agent.llm_action(full_question, planning_context, actions_history, thoughts_history, current_thought, limit)
                    print("RAW ACTING!!!!!!!!!!!!!!!!!")
                    print(action)
                    action = extract_action(action, test_model_name)
                else:
                    action = default_agent.llm_action(full_question, planning_context, actions_history, thoughts_history, current_thought, limit)
                    print("RAW ACTING!!!!!!!!!!!!!!!!!")
                    print(action)
                    action = extract_action(action, 'llama')            
            
            except Exception as e:
                error, error_message = True, str(e)
                print(f"An error occurred during the acting process: {e}")
                continue
            print("ACTING!!!!!!!!!!!!!!!!!!!!")
            print(action)

            if not isinstance(action, dict):
                continue
            try:

                if action["Answer"] != None and is_equiv(action["Answer"], answer):
                    reflection = ""
                    trajectory_current.append({
                        "observation": full_question,
                        "planning_context": planning_context,
                        "reasoning": current_thought,
                        "reflection": reflection,
                        "action": "Based on current thought {}, take action: Confirm final answer: {}".format(current_thought, action["Answer"]),
                        
                    })
                    break
                elif action["Answer"] != None and not is_equiv(action["Answer"], answer):
                    current_action = "Based on current thought {}, take action: Confirm final answer(which is wrong): {}".format(current_thought, action["Answer"])
                    actions_history.append(current_action)
                    if 'reflection' in modes:
                        reflection = test_agent.llm_reflection(full_question, actions_history, thoughts_history)
                        # reflection = extract_reflection(reflection, test_model_name)
                    else:
                        reflection = default_agent.llm_reflection(full_question, actions_history, thoughts_history)
                        # reflection = extract_reflection(reflection, 'llama')
                    print("REFLECTING!!!!!!!!!!!!!!!!!!!!")
                    print(reflection)
                elif "tool" in action:
                    reflection = ""
                    if action["tool"] == "Calculator":
                        try:
                            current_value = safe_eval(action['algebraic expression'])
                            current_action = "Based on current thought {}, take action: Use calculator to calculate {}, and result is {}".format(current_thought, action['algebraic expression'], current_value)
                        except Exception as e:
                            print(e)
                            current_action = "Invalid action!"
                    elif action["tool"] == "Search engine":
                        try:
                            current_action = "Based on current thought {}, take action: Use search engine to retrive {}, and the most relavant result is {}".format(current_thought, action['key words'], call_search_engine(action['key words'], theorems))
                        except:
                            current_action = "Invalid action!"
                    else:
                        current_action = action['action']
                    actions_history.append(current_action)
                else:
                    continue
            except:
                current_action = "Invalid action!!!"
            print("current_action!!!!!!!!!!!!!!!!")
            print(current_action)
            trajectory_current.append({
                "observation": full_question,
                "planning_context": planning_context,
                "reasoning": current_thought,
                "reflection": reflection,
                "action": current_action,
                
            })
        id += 1

        try:
            if is_equiv(action['Answer'], answer):
                correct += 1
        except:
            pass

        
        
        print(f"Current accuracy: {correct} / {total} = {correct / total * 100}%")
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
    parser.add_argument('--category', type=str, choices=['algebra', 'geometry'], help='Evaluation category')
    parser.add_argument('--start_index', type=int, default=0, help='Start index of data.')
    parser.add_argument('--original_correct', type=int, default=0, help='Original correct num of data.')
    parser.add_argument('--ip', type=str, default=None, help='IP address of API Agent.')

    args = parser.parse_args()

    # Call main with all arguments
    main(args.mode, args.default_model, args.default_tokenizer, args.test_model_name,
         args.temperature, args.top_p, args.max_seq_len, args.max_batch_size, args.category,
         args.start_index, args.original_correct, args.ip, args.max_gen_len)

