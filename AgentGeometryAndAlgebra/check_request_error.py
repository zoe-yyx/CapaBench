import os
 
def find_error_lines(directory):
    search_strings = [
        "Request timed out. Retrying... (Attempt",
        "An error occurred during the request:",
        'No response received. Retrying...',
        'No content generated.',
        'No completions found in the response, retrying...',
        'An error occurred: ',
        'Max retries reached. No completions found.'
    ]
 
    for root, _, files in os.walk(directory):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            # print(file_path)
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    file_content_list = file.readlines()
                    # print(file_name)
                    # print(len(file_content_list))
                    for i in range(len(file_content_list)):
                        if any(search_string in file_content_list[i] for search_string in search_strings):
                            print(file_path)
                            print(f"发现第一次开始出现请求出错的行！！！ 行{i + 1}")
                            for j in range(i - 1, -1, -1):
                                if "Current accurac" in file_content_list[j]:
                                    print(file_content_list[j])
                                    break
                            break
            except Exception as e:
                print(f"Error reading file {file_path}: {e}")
 
if __name__ == "__main__":
    ## 代数
    # llm_list = ['claude_3.5_sonnet', 'gpt-4o-mini', 'llama3-70b-instruct', 'Qwen2.5-32b-instruct']
    # for llm in llm_list:
    #     directory_to_search = f'/home/hadoop-aipnlp/dolphinfs_hdd_hadoop-aipnlp/qisiyuan02/Geometry/log/new_algebra/{llm}/multi'
    #     print(llm)
    #     find_error_lines(directory_to_search)

    ## 几何
    # llm_list = ['claude_3.5_sonnet', 'gpt-4o-mini', 'llama3-70b-instruct', 'Qwen2.5-32b-instruct']
    # for llm in llm_list:
    #     directory_to_search = f'/home/hadoop-aipnlp/dolphinfs_hdd_hadoop-aipnlp/qisiyuan02/Geometry/log/new_geometry/{llm}/multi'
    #     print(llm)
    #     find_error_lines(directory_to_search)

    ## Coq
    llm_list = ['Claude-3.5-Sonnet', 'gpt-4-turbo-2024-04-09', 'qwen2.5-32B-Instruct', 'gpt-4o-mini', 'doubao-pro-4k', 'GLM-4-air', 'llama3-70B-instruct', 'Mistral-8X7B-instruct-v0.1', 'Mistral-7B-instruct-v0.2']

    for llm in llm_list:
        directory_to_search = f'/home/hadoop-aipnlp/dolphinfs_hdd_hadoop-aipnlp/qisiyuan02/Geometry/log/new_algebra/{llm}/multi'
        print(llm)
        find_error_lines(directory_to_search)