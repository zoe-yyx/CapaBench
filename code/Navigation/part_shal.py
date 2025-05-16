import os
import pandas as pd
import json
from itertools import combinations
from math import factorial

# 定义模型名称映射
model_mapping = {
    "gpt4turbo": "gpt4turbo",
    "l": "llama",
    "glm": "glm",
    "qwen": "qwen",
    "Mistral": "Mistral",
    "4omini":"4omini",
    "Mistral8*7":"Mistral8*7",
    "llama70b":"llama70b",
    "doubao":"doubao"
}
model_name="Mistral8*7"

# 定义输出文件夹路径
def decode(name):
    # 使用模型名称映射进行解码
    for key, value in model_mapping.items():
        if key == name:
            return value
    return "Unknown"

# 读取并处理数据
data = []
for i in range(0, 250):
    print(i)
    output_dir = f"output_{model_name}/{model_name}_output_" + str(i)
    ll_dir = f"outputcl"
    file_name=f"/output_{i}_c_l/planning_Pl_Rl_Al_Fl_seed{i}.out"
    if os.path.exists(ll_dir+file_name):
        with open(ll_dir+file_name, 'r') as f:
            lines = f.readlines()
            if lines:
                last_line = lines[-1].strip()
                last_line = last_line.replace("'", "\"")
                last_line = last_line.replace("True", "true")
                last_line = last_line.replace("\n", "\\n")
                try:
                    print(last_line)
                    last_line_data = json.loads(last_line)
                    print(last_line_data)
                    reward_normalized = last_line_data['info']['reward_normalized']
                except:
                    reward_normalized = 0
                
                data.append(["planning", "llama","llama", "llama", "llama", i, reward_normalized])
                print(data[-1])
    if not os.path.exists(output_dir):
        continue
    
    for root, dirs, files in os.walk(output_dir):
        for file in files:
            if file.endswith(".out"):
                file_path = os.path.join(root, file)

                with open(file_path, 'r') as f:
                    lines = f.readlines()
                    if lines:
                        last_line = lines[-1].strip()
                        last_line = last_line.replace("'", "\"")
                        last_line = last_line.replace("True", "true")
                        last_line = last_line.replace("\n", "\\n")
                        if "F" not in file:
                            continue
                        try:
                            last_line_data = json.loads(last_line)
                            reward_normalized = last_line_data['info']['reward_normalized']
                        except:
                            reward_normalized = 0
                            print(i, file)

                        parts = file.split('_')
                        game = parts[0]

                        planning = decode(parts[1][1:])
                        reasoning = decode(parts[2][1:])
                        action = decode(parts[3][1:])
                        reflection = decode(parts[4][1:])



                        seed = parts[5].replace('seed', '').replace('.out', '')

                        data.append([game, planning, reasoning, action, reflection, seed, reward_normalized])

reward_dict = {}
reward_num = {}
llama_dic={}
intls=[]
for entry in data:
    print(entry)
    game, planning, reasoning, action, reflection, seed, reward_normalized = entry
    key = str((planning, reasoning, action, reflection))
    if key not in reward_dict:
        reward_dict[key] = 0
        reward_num[key] = 0
    if key=="('llama', 'llama', 'llama', 'llama')":
        print(entry)
        llama_dic[seed]=reward_normalized
    elif key=="('Mistral8*7', 'Mistral8*7', 'Mistral8*7', 'Mistral8*7')":
        intls.append(seed)
  
    reward_dict[key] += reward_normalized
    if not reward_normalized == 0:
        reward_num[key] += 1
for key, value in reward_num.items():
    if not reward_num[key] == 0:
        reward_dict[key] = reward_dict[key] / reward_num[key]
print(llama_dic)
print(reward_dict)
llama_sum=[llama_dic[int(i)] for i in intls if int(i) in llama_dic.keys()]
reward_dict["('llama', 'llama', 'llama', 'llama')"]= sum(llama_sum)/len(intls)
df = pd.DataFrame(data, columns=['Game', 'PLAN', 'REASON', 'ACTION', 'REFLECTION', 'Seed', 'reward'])
excel_file = output_dir + 'output.xlsx'
print(reward_num)
with open('res1.json', 'w') as f:
    json.dump(reward_dict, f)


# 读取JSON数据
def read_json_from_file(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

# 替换模型名称为相应的字母
def replace_model_names(key):
    key = key.replace(model_name, "t").replace("llama", "d")
    key = key.replace("(", "").replace(")", "").replace("'", "").replace(" ", "")
    return tuple(key.split(','))

# 替换字母为特定符号
def add_prefixes(key):
    return ('P' + key[0], 'R' + key[1], 'A' + key[2], 'F' + key[3])

# 主函数
file_path = 'res1.json'
data = read_json_from_file(file_path)
contributions = {replace_model_names(k): v for k, v in data.items()}
contributions = {add_prefixes(k): v for k, v in contributions.items()}

default_features = ['Pd', 'Rd', 'Ad', 'Fd']
target_features = ['Pt', 'Rt', 'At', 'Ft']

def sort_by_praf_order(tup):
    order = {'P': 0, 'R': 1, 'A': 2, 'F': 3}
    return tuple(sorted(tup, key=lambda x: order[x[0]]))

def calculate_shapley_values(default_features, target_features, contributions):
    def calculate_shapley_value(feature):
        total_shapley_value = 0
        n = len(target_features)

        for subset_size in range(n):
            for subset in combinations([f for f in target_features if f != feature], subset_size):
                subset = list(subset)
                replaced_subset_before = [
                    default_features[target_features.index(f)] if f not in subset else f
                    for f in target_features
                ]

                replaced_subset_after = [
                    feature if f == feature else (default_features[target_features.index(f)] if f not in subset else f)
                    for f in target_features
                ]

                subset_before = sort_by_praf_order(replaced_subset_before)
                subset_after = sort_by_praf_order(replaced_subset_after)

                marginal_contribution = contributions.get(subset_after, 0) - contributions.get(subset_before, 0)

                weight = (factorial(subset_size) *
                          factorial(n - subset_size - 1) /
                          factorial(n))

                total_shapley_value += weight * marginal_contribution

        return total_shapley_value

    shapley_values = {feature: calculate_shapley_value(feature) for feature in target_features}
    return shapley_values

shapley_values_corrected = calculate_shapley_values(default_features, target_features, contributions)
print(shapley_values_corrected)
