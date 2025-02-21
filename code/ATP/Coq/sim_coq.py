import subprocess
import time
import os
import sys

def run_coq_commands(file_path, timeout=2):
    commands = read_v_file(file_path)
    coqtop = subprocess.Popen(['coqtop'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=False, bufsize=0)
    # 设置为非阻塞模式
    os.set_blocking(coqtop.stdout.fileno(), False)
    os.set_blocking(coqtop.stderr.fileno(), False)

    time.sleep(2)

    tmp = ""

    try:
        line = coqtop.stdout.read()
        if line:
            line = line.decode('utf-8').strip()
            # print("Stdout:", line)
            tmp += f"Stdout: {line}\n"
          
    except IOError:
        pass  # 当没有可读数据时

    try:
        error_line = coqtop.stderr.read()
        if error_line:
            error_line = error_line.decode('utf-8').strip()
            # print("Stderr:", error_line)
            tmp += f"Stderr: {error_line}\n"
   
    except IOError:
        pass
    
    results = [tmp]
    for command in commands:
        tmp = ""
        tmp += "---------------------------------------------\n"
        tmp += f"Sending command to coqtop: {command}\n"
        coqtop.stdin.write(command.encode('utf-8') + b"\n")
        coqtop.stdin.flush()
        
        output = []
        error_output = []
        start_time = time.time()

        end_stdout = False
        end_stderr = False

        while True:
            # 给足够时间以便输出能够完整
            if time.time() - start_time > timeout:
                # print("Timeout reached, proceeding to next command.")
                break

            try:
                line = coqtop.stdout.read()
            
                if line:
                    line = line.decode('utf-8').strip()
                    # print("Stdout:", line)
                    tmp += f"Stdout: {line}\n"
                    output.append(line)
                else:
                    end_stdout = True
                    
            except IOError:
                pass  # 当没有可读数据时

            try:
                error_line = coqtop.stderr.read()
                if error_line:
                    error_line = error_line.decode('utf-8').strip()
                    # print("Stderr:", error_line)
                    tmp += f"Stderr: {error_line}\n"
                    if error_line == "forall_forall <":
                        print(1)
                    error_output.append(error_line)
                else:
                    end_stderr = True
            except IOError:
                pass

            if not line and not error_line:
                time.sleep(0.1)  # 短暂等待更多数据
                # break

        results.append(tmp)
    
    coqtop.stdin.write(b"Quit.\n")
    coqtop.stdin.flush()
    coqtop.terminate()
    coqtop.wait()
    
    return results

def read_v_file(filepath):
    commands = []
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            for line in file:
                # Strip to remove any leading/trailing whitespace
                cleaned_line = line.strip()
                # Optional: Skip empty lines or comments
                if cleaned_line and not cleaned_line.startswith(("(*", "//", "#")):
                    commands.append(cleaned_line)
    except FileNotFoundError:
        print(f"Error: The file {filepath} was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")
    
    return commands

