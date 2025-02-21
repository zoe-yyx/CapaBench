import subprocess
import re

def delete_trace_info(input_string):
    try:
        # 定义要查找的模式
        trace_pattern = r"unknown identifier 'trace'"
        trace_state_pattern = r"unknown identifier 'trace_state'"
        
        # 定义匹配到这两个标记时前向查找 tmp 的模式
        def remove_tmp_to_pattern(input_string, pattern):
            # 查找所有匹配模式的位置
            matches = [(m.start(), m.end()) for m in re.finditer(pattern, input_string)]
            
            # 从后向前处理删除，避免影响索引
            for start, end in reversed(matches):
                # 从匹配位置向前查找最靠近的 'tmp'
                tmp_pos = input_string[:start].rfind("tmp")
                if tmp_pos != -1:
                    # 删除从 tmp 到匹配项之间的内容
                    input_string = input_string[:tmp_pos] + input_string[end:]
            
            return input_string

        # 先处理 trace 的情况
        input_string = remove_tmp_to_pattern(input_string, trace_pattern)
        
        # 再处理 trace_state 的情况
        input_string = remove_tmp_to_pattern(input_string, trace_state_pattern)
        
        return input_string
    except Exception as e:
        return input_string


def run_lean_commands(filename):
    my_result = {
        "StdOut": "",
        "StdError": "",
        "ReturnCode": ""
    }
    # 执行 'lake build' 命令
    try:
        result = subprocess.run(
            ['lake', 'env', 'lean', filename],
            capture_output=True,
            text=True,
            check=True  # 如果命令返回非零退出状态，抛出 CalledProcessError 异常
        )
    except subprocess.CalledProcessError as e:
        print("构建过程中出现错误：")
        my_result["StdOut"] = delete_trace_info(e.stdout)
        my_result["StdError"] = delete_trace_info(e.stderr)
        my_result["ReturnCode"] = delete_trace_info(e.returncode)
        # my_result["StdOut"] = e.stdout
        # print(type(e.stdout))
        # my_result["StdError"] = e.stderr
        # my_result["ReturnCode"] = e.returncode
        return my_result

    my_result["StdOut"] = delete_trace_info(result.stdout)
    my_result["StdError"] = delete_trace_info(result.stderr)
    my_result["ReturnCode"] = delete_trace_info(result.returncode)
    # my_result["StdOut"] = result.stdout
    # my_result["StdError"] = result.stderr
    # my_result["ReturnCode"] = result.returncode

    print(type(result.stdout))

    # 检查返回码
    if result.returncode == 0:
        print("构建成功")
    else:
        print("构建失败，返回码：", result.returncode)
    return my_result

# print(run_lean_commands('tmp_raf.lean'))

# if __name__ == '__main__':
#     main("./new.lean")


# # 示例用法
# input_string = """
# some code here
# tmp intermediate data
# unknown identifier 'trace'
# more code
# tmp another data
# unknown identifier 'trace_state'
# """

# cleaned_string = delete_trace_info(input_string)
# print(cleaned_string)

# run_lean_commands('./tmp_praf.lean')