# check_validity.py
import json
import sys

def check_file_validity(file_path):
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()
        
        # 检查文件是否为空
        if not lines:
            return False

        # 获取最后一行并进行基本的字符串替换
        last_line = lines[-1].strip()
        last_line = last_line.replace("'", "\"")
        last_line = last_line.replace("True", "true")
        last_line = last_line.replace("\n", "\\n")

        # 如果文件名中不包含 "F"，则跳过
        if "F" not in file_path:
            return False

        # 尝试解析最后一行的 JSON 数据
        try:
            last_line_data = json.loads(last_line)
            reward_normalized = last_line_data['info']['reward_normalized']
            return True
        except (json.JSONDecodeError, KeyError):
            return False

    except FileNotFoundError:
        return False
    except Exception:
        return False

if __name__ == "__main__":
    file_path = sys.argv[1]
    is_valid = check_file_validity(file_path)
    print(is_valid)
