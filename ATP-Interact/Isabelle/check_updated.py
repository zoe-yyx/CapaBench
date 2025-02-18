import paramiko
import time
from sftp_interact import sftp_download, sftp_upload
from sim_isabelle import run_isabelle_commands
import json
import argparse
import shutil
import os

def check_file_update(host, port, username, password, file_mode, interval):
    # 创建SSH客户端
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(host, port=port, username=username, password=password)
    
    # 连接到SFTP
    sftp = client.open_sftp()
    
    # 获取文件的初始修改时间
    prev_mod_time = sftp.stat(f"tmp_{file_mode}.thy").st_mtime
    First = True
    try:
        while True:
            time.sleep(interval)
            # 检查文件的当前修改时间
            current_mod_time = sftp.stat(f"tmp_{file_mode}.thy").st_mtime
            if current_mod_time != prev_mod_time or First:
                if First:
                    First = False
                print("该文件已经更新")
                prev_mod_time = current_mod_time
                sftp_download('jumper.sankuai.com', "qisiyuan02", "12345678qwe!", f"tmp_{file_mode}.thy", f"./{file_mode}/tmp_{file_mode}.thy")
                # shutil.move(f"tmp_{file_mode}.thy", f'./{file_mode}')
                coq_result = run_isabelle_commands(file_mode)
                # 检查文件是否存在，避免引发异常  
                # if os.path.exists(f'./{file_mode}/tmp_{file_mode}.thy'):  
                #     os.remove(f'./{file_mode}/tmp_{file_mode}.thy')  # 或者使用 os.unlink(file_path)  
                #     print(f"{f'./{file_mode}/tmp_{file_mode}.thy'} 已成功删除。")  
                # else:  
                #     print(f"{f'./{file_mode}/tmp_{file_mode}.thy'} 不存在。")

                with open(f"tmp_{file_mode}_isabelle.json", 'w') as f:
                    json.dump(coq_result, f, indent=4)
                sftp_upload('jumper.sankuai.com', "qisiyuan02", "12345678qwe!", f"tmp_{file_mode}_isabelle.json", f"tmp_{file_mode}_isabelle.json")

            else:
                pass
    except KeyboardInterrupt:
        print("停止监控")
    finally:
        sftp.close()
        client.close()


if __name__ == "__main__":
    print("Hello!!!!!")
    # 创建 ArgumentParser 对象
    parser = argparse.ArgumentParser(description='处理输入参数的示例脚本。')

    # 添加参数
    parser.add_argument('--file_mode', type=str, help='输入文件的路径')
    

    # 解析参数
    args = parser.parse_args()

    

    # 使用示例
    while True:
        try:
            check_file_update('jumper.sankuai.com', 22, 'qisiyuan02', '12345678qwe!', args.file_mode, 2)
        except Exception as e:
            time.sleep(5)
            print(f"error: {e}")
            pass
