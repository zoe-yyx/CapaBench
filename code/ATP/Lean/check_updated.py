import paramiko
import time
from sftp_interact import sftp_download, sftp_upload
import json

def check_file_update(host, port, username, password, file_path, interval):
    # 创建SSH客户端
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(host, port=port, username=username, password=password)
    
    # 连接到SFTP
    sftp = client.open_sftp()
    
    # 获取文件的初始修改时间
    prev_mod_time = sftp.stat(file_path).st_mtime
    
    try:
        while True:
            time.sleep(interval)
            # 检查文件的当前修改时间
            current_mod_time = sftp.stat(file_path).st_mtime
            if current_mod_time != prev_mod_time:
                print("该文件已经更新")
                prev_mod_time = current_mod_time
                # sftp_download('jumper.sankuai.com', "qisiyuan02", "********", file_path, file_path)
                sftp_download('jumper.sankuai.com', username, password, file_path, file_path)
                break
               
                
                

            else:
                pass
    except KeyboardInterrupt:
        print("停止监控")
    finally:
        sftp.close()
        client.close()


