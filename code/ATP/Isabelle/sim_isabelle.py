import subprocess
from write_root import writeRoot
import os
import re

def replace_theory_name(file_path, new_name):
    # 正则表达式匹配 'theory xxx'，捕获 xxx 部分
    pattern = r'(theory\s+)(\w+)'
    
    # 打开文件，读取其内容
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    # 使用正则表达式查找并替换首次出现的 'theory xxx'
    # 只替换第一次匹配到的
    new_content, count = re.subn(pattern, r'\1' + new_name, content, count=1)
    
    if count > 0:
        # 如果找到并替换了内容，则将新的内容写回文件
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(new_content)
        # print(f"'theory xxx' replaced with 'theory {new_name}' in {file_path}")
    else:
        # print("No 'theory xxx' statement found in the file.")
        pass



def extract_first_theorem(file_path):
    # 正则表达式匹配 'theorem xxx'，捕获 xxx 部分
    pattern = r'theory\s+(\w+)'
    
    # 打开并读取文件
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    # 使用正则表达式查找首次出现的 theorem xxx
    match = re.search(pattern, content)
    
    if match:
        # 返回匹配的 xxx 部分
        return match.group(1)
    else:
        return ""  # 如果没有找到匹配的内容，返回 None


def extract_star_lines(text):
    # 使用splitlines()将文本按行分割，并通过startswith检查每行是否以"***"开头
    star_lines = [line for line in text.splitlines() if line.strip().startswith('***')]
    return "\n".join(star_lines)


def run_isabelle_commands(file_mode):

    
    
    writeRoot(f'tmp_{file_mode}', file_mode)
    theorem = extract_first_theorem(f'./{file_mode}/tmp_{file_mode}.thy')

    replace_theory_name(f'./{file_mode}/tmp_{file_mode}.thy', f'tmp_{file_mode}')
    my_result = {
        "StdOut": "",
        "StdError": "",
        "ReturnCode": ""
    }

    try:

        process = subprocess.Popen(
            ['isabelle', 'build', '-d', '.', '-v', '-o', 'quick_and_dirty=true', 'MyProofs'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            cwd=f'./{file_mode}'
        )

        # 使用 communicate 来获取输出并等待进程结束
        stdout, stderr = process.communicate(timeout=30)
        returncode = process.returncode
        stdout = stdout.decode()
        stderr = stderr.decode()
        
    except subprocess.TimeoutExpired as e:
        print("Command timed out after 30 seconds")
        my_result["StdOut"] = "Build Failed, Timeout!!!"
        my_result["StdError"] = "Build Failed, Timeout!!!"

        print(my_result['StdOut'])
        return my_result
    except subprocess.CalledProcessError as e:
        print("构建过程中出现错误：")
        my_result["StdOut"] = extract_star_lines(e.stdout.decode()).replace(f"~/Desktop/agent_isabelle/{file_mode}/tmp_{file_mode}", theorem)
        my_result["StdError"] = e.stderr.decode().replace(f"/Users/qisiyuan/Desktop/agent_isabelle/{file_mode}/", "").replace(f'tmp_{file_mode}', theorem)
        my_result["ReturnCode"] = e.returncode
        print(my_result['StdOut'])
        return my_result

    my_result["StdError"] = stderr.replace(f"/Users/qisiyuan/Desktop/agent_isabelle/{file_mode}/", "").replace(f'tmp_{file_mode}', theorem)
    my_result["ReturnCode"] = returncode

    # 检查返回码
    if returncode == 0:
        my_result["StdOut"] = "Buile Successfully!"
    
        print("构建成功")
    else:
        my_result["StdOut"] = extract_star_lines(stdout).replace(f"~/Desktop/agent_isabelle/{file_mode}/tmp_{file_mode}", theorem)
        print("构建失败，返回码：", returncode)

    print(my_result['StdOut'])
    
    return my_result


