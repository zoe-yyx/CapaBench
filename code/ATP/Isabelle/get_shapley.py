import os  
import re  

# 你给出的contributions字典
contributions = {
    ('Pd', 'Rd', 'Ad', 'Fd'): 0.09,
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


  
def find_accuracy_lines(directory):  
    # 正则表达式模式，用于匹配形如 "Current accuracy: {xxx} / 250 =" 的行  
    pattern = re.compile(r'Current accuracy:\s*\d+\s*/\s*111\s*=')  
  
    # 遍历指定目录中的所有文件  
    for root, dirs, files in os.walk(directory):  
        for file in files:  
            file_path = os.path.join(root, file)  
              
            try:  
                with open(file_path, 'r', encoding='utf-8') as f:  
                    for line_num, line in enumerate(f, start=1):  
                        if pattern.match(line):  
                            print(f'文件名: {file}')  
                            print(f'行号: {line_num}, 内容: {line.strip()}') 
                            prefix = get_prefix(file)
                            accuracy = get_accuracy(line.strip())
                            # print(prefix)
                            # print(accuracy)
                            contributions[file_key_map[prefix]] = max(accuracy, contributions[file_key_map[prefix]])
            except Exception as e:  
                print(f'无法读取文件 {file_path}: {e}')  
  
if __name__ == "__main__":  
    # 指定你要读取的文件夹路径  
    directory_path = './log/isabelle/gpt-4o-mini/no'  # 替换为你的文件夹路径  
    find_accuracy_lines(directory_path)
    print(directory_path)
    for key, value in contributions.items():
        print(f"{key}: {value},")