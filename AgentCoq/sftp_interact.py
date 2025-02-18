import paramiko



def sftp_download(hostname, username, password, remote_file_path, local_file_path):
    port = 22  # 默认SSH端口为22
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        client.connect(hostname, port, username, password)
        sftp = client.open_sftp()
        sftp.get(remote_file_path, local_file_path)
        print("文件下载成功")
        return True
    except Exception as e:
        print(f"连接或文件传输失败: {e}")
        return False
    finally:
        client.close()

def sftp_upload(hostname, username, password, remote_file_path, local_file_path):    
    port = 22  # 默认SSH端口为22
 

    # 初始化SSH客户端
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        # 连接到SFTP服务器
        client.connect(hostname, port, username, password)
        
        # 创建SFTP客户端
        sftp = client.open_sftp()
        
        # 上传文件
        sftp.put(local_file_path, remote_file_path)
        print(f"{local_file_path}文件上传成功")
        
        # 关闭SFTP连接
        sftp.close()
        
    except Exception as e:
        print(f"连接或文件传输失败: {e}")

    finally:
        # 关闭SSH客户端连接
        client.close()


sftp_upload('jumper.sankuai.com', "qisiyuan02", "********", "tmp.v", "tmp.v")