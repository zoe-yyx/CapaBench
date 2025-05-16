
eva0_ports_291_0 = [5103, 5104]
eva0_ports_291_1 = [50113, 50114]

mis_ports_474_0 = [5102, 5103, 5104, 5105]
mis_ports_474_1 = [50112, 50113, 50114, 50115]
mis_ports_474_2 = [5111, 5112, 5113, 5114]
mis_ports_474_3 = [51112, 51113, 51114]

qwen_ports_474_0 = [4102, 4103, 4104, 4105]
qwen_ports_474_1 = [40112, 40113, 40114, 40115]
qwen_ports_474_2 = [4111, 4112, 4113, 4114]
qwen_ports_474_3 = [41112, 41113, 41114]

import random

def get_random_ports(ports_num) -> list:
    ports = []
    for _ in range(ports_num):
        ports.append(random.randint(4000, 50000))
    return ports