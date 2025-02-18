import json
import os

with open('./coq_data.json', 'r') as f:
    problem_list = json.load(f)
print(problem_list[0])
print(len(problem_list))

def list_files(directory):
    for entry in os.listdir(directory):
        full_path = os.path.join(directory, entry)
        if os.path.isfile(full_path):
            print(full_path)



llm_list = ['Claude-3.5-Sonnet', 'gpt-4-turbo-2024-04-09', 'qwen2.5-32B-Instruct', 'gpt-4o-mini', 'doubao-pro-4k', 'GLM-4-air', 'llama3-70B-instruct', 'Mistral-8X7B-instruct-v0.1', 'Mistral-7B-instruct-v0.2']

for llm in llm_list[0: ]:
    print(f"{llm}!!!")
    # 指定您的文件夹路径
    directory = f'./user_session_logs/coq/no/{llm}'
    cnt = 0

    for entry in os.listdir(directory):
        full_path = os.path.join(directory, entry)
        if 'planning_reasoning_action_reflection' in full_path and os.path.isfile(full_path):
            # if os.path.isfile(full_path):
            print(full_path)
            line_num = 0
            with open(full_path, 'r') as file:
                for line in file:
                    line_num += 1
                    # if llm == 'Claude-3.5-Sonnet' and line_num <= 250:
                    #     continue
                    # 将每行的字符串转换为字典
                    data = json.loads(line)
                    
                    # print(data)
                    # 获取唯一的键值对
                    key, value = next(iter(data.items()))
                    

                    
                    try:
                        final_traj = value[len(value) - 1]

                        if "Confirm final proving process: " in final_traj['action']:
                            problem_list[int(key) - 1][llm] = value
                            cnt += 1
                    except:
                        pass
            print(line_num)
    print(cnt / 250)

with open('coq_data_with_trajectory.json', 'w', encoding='utf-8') as f:
    json.dump(problem_list, f, indent=4)
                        


   