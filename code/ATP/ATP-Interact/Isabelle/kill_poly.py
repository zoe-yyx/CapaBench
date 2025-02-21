import subprocess
import time
import os

def kill_poly_processes():
    print("开始检查poly进程！！！")
    try:
        # 使用pgrep精确查找名为'poly'的进程ID
        result = subprocess.run(['pgrep', '-x', 'poly'], stdout=subprocess.PIPE, text=True)
        pids = result.stdout.strip().split('\n')

        for pid in pids:
            if pid.isdigit():
                if int(pid) != os.getpid():  # 防止杀掉自身
                    subprocess.run(['kill', '-9', pid])
                    print(f"已杀死进程 {pid}，名称为 'poly'")
    except Exception as e:
        print(f"发生错误：{e}")

if __name__ == '__main__':
    while True:
        kill_poly_processes()
        time.sleep(180)
