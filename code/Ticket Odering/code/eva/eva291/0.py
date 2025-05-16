import sys
import os

# print(sys.path)
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
# print(sys.path)
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..'))
# print(sys.path)

from eva.eva291.test_model_name import test_model_name
print(test_model_name)
print(type(test_model_name))

# 创建日志文件夹
log_path = f"./log_new_{test_model_name}"
os.makedirs(log_path, exist_ok=True)

from eva.assign_modes import modes_00_8X7B
# 训练modes
modes = modes_00_8X7B
from eva.ports import get_random_ports
# 端口
ports = get_random_ports(4)

myNUM = len(modes)

def trans_mode(mode):
    mode = mode.split()
    for i in range(len(mode)):
        if mode[i] == "planning":
            mode[i] = "p"
        elif mode[i] == "reasoning":
            mode[i] = "r"
        elif mode[i] == "action":
            mode[i] = "a"
        elif mode[i] == "reflection":
            mode[i] = "f"
    return "_".join(mode)

for i in range(myNUM):
    mode = modes[i]
    port = ports[i]
    os.system(f"nohup torchrun --master_port {port} dialop/run_agent.py --test_model_name {test_model_name} --mode {mode} > {log_path}/{trans_mode(mode)}.out 2>&1")