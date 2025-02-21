

## 计算函数
from itertools import combinations
from math import comb
import re
import os

def calculate_shapley_values(contributions, default_features, target_features):
    # 定义一个函数来按照PRAF顺序对组合进行排序
    def sort_by_praf_order(tup):
        order = {'P': 0, 'R': 1, 'A': 2, 'F': 3}
        return tuple(sorted(tup, key=lambda x: order[x[0]]))

    # 计算单个特征的Shapley值
    def calculate_shapley_value(feature):
        total_shapley_value = 0
        n = len(target_features)

        for subset_size in range(n):  # 考虑从0到n-1的所有子集
            for subset in combinations([f for f in target_features if f != feature], subset_size):
                subset = list(subset)

                # 用默认特征替换目标特征
                replaced_subset_before = [
                    default_features[target_features.index(f)] if f not in subset else f
                    for f in target_features
                ]
                replaced_subset_after = [
                    feature if f == feature else (default_features[target_features.index(f)] if f not in subset else f)
                    for f in target_features
                ]

                # 对组合进行排序以确保顺序一致
                subset_before = sort_by_praf_order(replaced_subset_before)
                subset_after = sort_by_praf_order(replaced_subset_after)

                # 计算边际贡献
                marginal_contribution = contributions.get(subset_after, 0) - contributions.get(subset_before, 0)

                # 根据组合的数量更新边际贡献
                weight = 1 / (2 ** (n-1))
                total_shapley_value += weight * marginal_contribution

        # Shapley值是总贡献的平均值
        return total_shapley_value

    # 计算每一个特征的Shapley值
    shapley_values = {feature: calculate_shapley_value(feature) for feature in target_features}

    return shapley_values


# # 文件名和key的对应关系
file_key_map = {
    'default': ('Pd', 'Rd', 'Ad', 'Fd'),
    'praf': ('Pt', 'Rt', 'At', 'Ft'),
    'p': ('Pt', 'Rd', 'Ad', 'Fd'),
    'r': ('Pd', 'Rt', 'Ad', 'Fd'),
    'a': ('Pd', 'Rd', 'At', 'Fd'),
    'f': ('Pd', 'Rd', 'Ad', 'Ft'),
    'pr': ('Pt', 'Rt', 'Ad', 'Fd'),
    'pa': ('Pt', 'Rd', 'At', 'Fd'),
    'pf': ('Pt', 'Rd', 'Ad', 'Ft'),
    'ra': ('Pd', 'Rt', 'At', 'Fd'),
    'rf': ('Pd', 'Rt', 'Ad', 'Ft'),
    'af': ('Pd', 'Rd', 'At', 'Ft'),
    'pra': ('Pt', 'Rt', 'At', 'Fd'),
    'prf': ('Pt', 'Rt', 'Ad', 'Ft'),
    'paf': ('Pt', 'Rd', 'At', 'Ft'),
    'raf': ('Pd', 'Rt', 'At', 'Ft'),
    # 添加其他的文件名和对应的key
}

def get_prefix(file: str) -> str:  
    # 首先检查是否包含下划线 "_"  
    if '_' in file:  
        # 返回下划线之前的全部内容  
        return file.split('_')[0]  
    else:  
        # 否则返回点号 "." 之前的全部内容  
        return file.rsplit('.', 1)[0] 
    
def get_accuracy(line: str) -> str:  
    # 使用正则表达式匹配位于=和%之间的内容  
    match = re.search(r'=([^%]*)', line)  
    if match:  
        # 返回匹配的内容（第一个括号内的内容）  
        return eval(match.group(1))  
    else:  
        # 如果没有找到匹配项，返回空字符串或None（根据需求选择）  
        # 这里返回空字符串  
        return 0


  
def find_accuracy_lines(directory, contributions):  
    # 正则表达式模式，用于匹配形如 "Current accuracy: {xxx} / 250 =" 的行  
    pattern = re.compile(r'Current accuracy:\s*\d+\s*/\s*111\s*=')  
  
    # 遍历指定目录中的所有文件  
    for root, dirs, files in os.walk(directory):  
        for file in files:  
            file_path = os.path.join(root, file)  

            if "old_version" in file_path:
                continue
            
              
            try:  
                with open(file_path, 'r', encoding='utf-8') as f:  
                    for line_num, line in enumerate(f, start=1):  
                        if pattern.match(line):  
                            print(f'文件名: {file_path}')  
                            print(f'行号: {line_num}, 内容: {line.strip()}') 
                            prefix = get_prefix(file)
                            if prefix == 'default':
                                continue
                            accuracy = get_accuracy(line.strip()) 
                            # print(prefix)
                            # print(accuracy)
                            contributions[file_key_map[prefix]] = max(accuracy, contributions[file_key_map[prefix]])
            except Exception as e:  
                print(f'无法读取文件 {file_path}: {e}')  

def get_textbf_and_underline(data):
    # 步骤1: 将值存储在一个列表中  
    values = list(data.values())  
    
    # 步骤2: 对列表进行排序，并找到最大值和第二大值  
    values.sort(reverse=True)  
    max_value = values[0]  
    second_max_value = values[1]  
    
    # 步骤3: 遍历字典，替换对应的值  
    for key, value in data.items():  
        if value == max_value:  
            data[key] = f'\\textbf{{{value}}}'  
        elif value == second_max_value:  
            data[key] = f'\\underline{{{value}}}'  

if __name__ == '__main__':
    # 函数输入
    # 给定基础和替代特征的组合情况和它们的贡献值
    # 特征组合
    default_features = ['Pd', 'Rd', 'Ad', 'Fd']
    target_features = ['Pt', 'Rt', 'At', 'Ft']

    # llm_list = ['claude_3.5_sonnet', 'GLM4-air', 'gpt-4o-mini', 'Llama3-70B-instruct', 'Qwen2.5-32b-instruct']

    llm_list = ['Claude-3.5-Sonnet', 'gpt-4-turbo-2024-04-09', 'qwen2.5-32B-Instruct', 'gpt-4o-mini', 'doubao-pro-4k', 'GLM-4-air', 'llama3-70B-instruct', 'Mistral-8X7B-instruct-v0.1', 'Mistral-7B-instruct-v0.2']


    total_latex = ""
    pt_dic = {}
    rt_dic = {}
    at_dic = {}
    ft_dic = {}
    accuracy_dic = {}
    for llm in llm_list:
        print(llm)
        contributions = {
            ('Pd', 'Rd', 'Ad', 'Fd'): 0.02702702702702703,
            ('Pt', 'Rt', 'At', 'Ft'): 0,
            ('Pt', 'Rd', 'Ad', 'Fd'): 0,
            ('Pd', 'Rt', 'Ad', 'Fd'): 0,
            ('Pd', 'Rd', 'At', 'Fd'): 0,
            ('Pd', 'Rd', 'Ad', 'Ft'): 0,
            ('Pt', 'Rt', 'Ad', 'Fd'): 0,
            ('Pt', 'Rd', 'At', 'Fd'): 0,
            ('Pt', 'Rd', 'Ad', 'Ft'): 0,
            ('Pd', 'Rt', 'At', 'Fd'): 0,
            ('Pd', 'Rt', 'Ad', 'Ft'): 0,
            ('Pd', 'Rd', 'At', 'Ft'): 0,
            ('Pd', 'Rt', 'At', 'Ft'): 0,
            ('Pt', 'Rd', 'At', 'Ft'): 0,
            ('Pt', 'Rt', 'Ad', 'Ft'): 0,
            ('Pt', 'Rt', 'At', 'Fd'): 0
        }
        # directory_path = f'./log/new_geometry/{llm}/multi'
        directory_path = f'/home/hadoop-aipnlp/dolphinfs_hdd_hadoop-aipnlp/qisiyuan02/AgentLean/log/lean/{llm}/no'
        find_accuracy_lines(directory_path, contributions)
        for k in contributions:
            print(f"{k}: {contributions[k]}")

        shapley_value = calculate_shapley_values(contributions, default_features, target_features)
        # latex_string = fr"\texttt{{{llm}}} & {round(shapley_value['Pt'], 4)} & {round(shapley_value['Rt'], 4)} & {round(shapley_value['At'], 4)} & {round(shapley_value['Ft'], 4)}\\"
        pt_dic[llm] = round(shapley_value['Pt'], 4)
        rt_dic[llm] = round(shapley_value['Rt'], 4)
        at_dic[llm] = round(shapley_value['At'], 4)
        ft_dic[llm] = round(shapley_value['Ft'], 4)
        accuracy_dic[llm] = round(contributions[('Pt', 'Rt', 'At', 'Ft')], 4) * 100
        
    
    get_textbf_and_underline(pt_dic)
    get_textbf_and_underline(rt_dic)
    get_textbf_and_underline(at_dic)
    get_textbf_and_underline(ft_dic)
    get_textbf_and_underline(accuracy_dic)
    for llm in llm_list:
        if llm == 'claude_3.5_sonnet':
            llm_claude = 'claude\\_3.5\\_sonnet'
        
            latex_string = fr"\texttt{{{llm_claude}}} & {pt_dic[llm]} & {rt_dic[llm]} & {at_dic[llm]} & {ft_dic[llm]} & {accuracy_dic[llm]}\\"
        elif llm == 'Mistral-7B_instruct-v0.2':
            llm_claude = 'Mistral-7B\\_instruct-v0.2'
        
            latex_string = fr"\texttt{{{llm_claude}}} & {pt_dic[llm]} & {rt_dic[llm]} & {at_dic[llm]} & {ft_dic[llm]} & {accuracy_dic[llm]}\\"

        else:
            latex_string = fr"\texttt{{{llm}}} & {pt_dic[llm]} & {rt_dic[llm]} & {at_dic[llm]} & {ft_dic[llm]} & {accuracy_dic[llm]}\\"
        total_latex += latex_string
        total_latex += '\n'
    print(total_latex)

    


