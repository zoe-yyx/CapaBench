from itertools import combinations
from math import comb, factorial
import re
import os


def calculate_shapley_values(contributions, default_features, target_features):
    def sort_by_praf_order(tup):
        order = {'P': 0, 'R': 1, 'A': 2, 'F': 3}
        return tuple(sorted(tup, key=lambda x: order[x[0]]))

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

                # Shapley weight：|S|! * (n - |S| - 1)! / n!
                weight = (factorial(subset_size) *
                          factorial(n - subset_size - 1) /
                          factorial(n))

                total_shapley_value += weight * marginal_contribution

        return total_shapley_value

    shapley_values = {feature: calculate_shapley_value(feature) for feature in target_features}
    return shapley_values


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
    'raf': ('Pd', 'Rt', 'At', 'Ft')
}

def get_prefix(file: str) -> str:  
    if '_' in file:  
        return file.split('_')[0]  
    else:  
        return file.rsplit('.', 1)[0] 
    
def get_accuracy(content: str) -> float:
    # matches = re.findall(r'Average rewards:.*?=\s*([\d.]+)', content)
    # matches = re.findall(r'Average rewards:\s*([\d.]+)', content)
    matches = re.findall(r'Combined Accuracy: \s*([\d.]+)', content)
    
    # print("matches",matches)
    if matches:
        return float(matches[-1])
    return 0

def find_accuracy_lines(directory, contributions):  
    for root, dirs, files in os.walk(directory):  
        for file in files:
            if not file.endswith('.out'):  
                continue
                
            file_path = os.path.join(root, file)  
            if "old_version" in file_path:
                continue
              
            try:  
                with open(file_path, 'r', encoding='utf-8') as f:  
                    # print(file_path)
                    content = f.read()
                    prefix = get_prefix(file)
                    if prefix == 'default':
                        continue
                    accuracy = get_accuracy(content)
                    if prefix in file_key_map:
                        contributions[file_key_map[prefix]] = max(accuracy, contributions[file_key_map[prefix]])
                        print(f"File: {file}, Prefix: {prefix}, Accuracy: {accuracy}") 
            except Exception as e:  
                print(f'Cannot read {file_path}: {e}')

def get_textbf_and_underline(data):
    values = list(data.values())  
    values.sort(reverse=True)  
    max_value = values[0]  
    second_max_value = values[1] if len(values) > 1 else None
    
    for key, value in data.items():  
        if value == max_value:  
            data[key] = f'\\textbf{{{value}}}'  
        elif second_max_value is not None and value == second_max_value:  
            data[key] = f'\\underline{{{value}}}'  



if __name__ == '__main__':
    default_features = ['Pd', 'Rd', 'Ad', 'Fd']
    target_features = ['Pt', 'Rt', 'At', 'Ft']
    
    llm_list = ['claude_3.5_sonnet', 'gpt-4o-mini','glm-4-airx',"gpt-4-turbo-0409","qwen2.5-32b-ins","Mistral-7B-Instruct","Llama-3-70B-Instruct","doubao-pro-4k","Mistral-8X7B-instruct"]

    total_latex = ""
    pt_dic = {}
    rt_dic = {}
    at_dic = {}
    ft_dic = {}
    accuracy_dic = {}
    
    for llm in llm_list:
        print(f"\nProcessing {llm}...")
        contributions = {
            ('Pd', 'Rd', 'Ad', 'Fd'): 0.2627543948102375,
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
        
        directory_path = f'./log/{llm}/comb/'
        find_accuracy_lines(directory_path, contributions)
        
        print(f"\nContributions for {llm}:")
        for k, v in contributions.items():
            print(f"{k}: {v}")

        shapley_value = calculate_shapley_values(contributions, default_features, target_features)
        
        print(f"\nShapley values for {llm}:")
        for k, v in shapley_value.items():
            print(f"{k}: {v}")
            
        pt_dic[llm] = round(shapley_value['Pt'], 4)
        rt_dic[llm] = round(shapley_value['Rt'], 4)
        at_dic[llm] = round(shapley_value['At'], 4)
        ft_dic[llm] = round(shapley_value['Ft'], 4)
        accuracy_dic[llm] = f"{round(contributions[('Pt', 'Rt', 'At', 'Ft')], 4) * 100}\\%"

    llm_list_2 = ['claude_3.5_sonnet', 'gpt-4o-mini','glm-4-airx',"gpt-4-turbo-0409","qwen2.5-32b-ins","Mistral-7B-Instruct","Llama-3-70B-Instruct","doubao-pro-4k","Mistral-8X7B-instruct"]

    print(accuracy_dic)
    p_list = [pt_dic[key] for key in llm_list_2]
    r_list = [rt_dic[key] for key in llm_list_2]
    a_list = [at_dic[key] for key in llm_list_2]
    f_list = [ft_dic[key] for key in llm_list_2]
    print(float(accuracy_dic['doubao-pro-4k'][0 : -2]))
    deltacc_list = [float(accuracy_dic[key][0 : -2]) / 100 - 0.2627 for key in llm_list_2]

    print(f'Pt = {p_list}')
    print(f'Rt = {r_list}')
    print(f'At = {a_list}')
    print(f'Ft = {f_list}')
    print(f'DeltaAcc = {deltacc_list}')
    
    get_textbf_and_underline(pt_dic)
    get_textbf_and_underline(rt_dic)
    get_textbf_and_underline(at_dic)
    get_textbf_and_underline(ft_dic)
    get_textbf_and_underline(accuracy_dic)
    
    for llm in llm_list:
        latex_string = fr"\texttt{{{llm}}} & {pt_dic[llm]} & {rt_dic[llm]} & {at_dic[llm]} & {ft_dic[llm]} & {accuracy_dic[llm]}\\"
        total_latex += latex_string + '\n'
    
    print("\nGenerated LaTeX table rows:")
    print(total_latex)