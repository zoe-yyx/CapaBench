'''
定义mediation的评价指标
mediation原任务:
在该任务中，每个用户都希望选择一个价格便宜且避免与用户的日历承诺冲突的航班，但该航班的到达时间接近其他用户的到达时间。助理可以访问每个用户的航班选项和工作日历，但不会观察用户的个人日历，也不会观察用户对哪些会议最重要的偏好
影响因素:
1. 航班价格
2. 航班与用户calendar的冲突程度
3. 航班所影响的calendar的重要性
4. 航班的到达时间与其他用户的到达时间的接近程度
'''

'''
框架构建思路：
1. 先加载agent获取的prompt以及agent的response
2. 通过agent的prompt,确定所选择的用户信息索引,从而获取到用户的日历信息,航班信息
3. 将两个用户的航班信息进行组合,产生所有可能的航班组,并基于上面的影响因素进行评价,从四个方面对航班组进行排名
4. 将每个航班组在四个方面的评价排名进行求和,然后基于求和的结果进行排序,得到最终的航班组排名
5. 将最终的航班组排名与agent的response进行对比,得到评价结果
'''
import os
import json
import sys
from datetime import datetime, timedelta
from typing import Tuple

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from dialop.create_agent_prompt import *

class EvaluateFlame:
    def __init__(self, user0_data, user1_data):
        self.user0_flight_set = user0_data["Flights"]
        self.user1_flight_set = user1_data["Flights"]
        self.user0_calendar = user0_data["Private calendar"] + user0_data["Shared calendar (visible to assistant)"]
        self.user1_calendar = user1_data["Private calendar"] + user1_data["Shared calendar (visible to assistant)"]
        self.all_flight_combs = [(user0_flight, user1_flight) for user0_flight in self.user0_flight_set for user1_flight in self.user1_flight_set]


        # (flight, conflict_importance, price)
        self.user0_flight_set_for_rank = [[flight, 0, flight["price"]] for flight in user0_data["Flights"]]
        self.user1_flight_set_for_rank = [[flight, 0, flight["price"]] for flight in user1_data["Flights"]]
        # (user0_flight, user1_flight, arrival_time_difference)
        self.all_flight_combs_for_rank = [[user0_flight, user1_flight, 0, 0, 0] for user0_flight in self.user0_flight_set for user1_flight in self.user1_flight_set]
        # the final rank of all flight combinations
        self.combs_rank = []

    
    def parse_time(self, date_str, start_date=None):
        time = datetime.strptime(date_str, "%m/%d %I:%M %p")
        if start_date and time < start_date:
            time += timedelta(days=1)
        return time
    

    """
    @brief: 判断航班与日历事件是否冲突
    @param flight: 航班信息
    @param calendar: 日历事件信息
    @return: (是否冲突, 最大重要性)
    """    
    def if_conflict(self, flight, calendars) -> Tuple[bool, int]:
        flight_start = self.parse_time(flight["start"])
        flight_end = self.parse_time(flight["start"][:6] + flight["end"], flight_start)
        
        max_importance = 0

        for event in calendars:
            event_start = self.parse_time(event["start"])
            event_end = self.parse_time(event["start"][:6] + event["end"], event_start)
            
            if (flight_start < event_end and flight_end > event_start) and event["importance"] > max_importance:
                max_importance = event["importance"]
    
        return (max_importance > 0, max_importance)
    

    """
    @brief: 获取与航班冲突的calendar最大重要性
    """
    def factor1(self):
        for i, flight in enumerate(self.user0_flight_set):
            conflict, importance = self.if_conflict(flight, self.user0_calendar)
            self.user0_flight_set_for_rank[i][1] = importance

        for i, flight in enumerate(self.user1_flight_set):
            conflict, importance = self.if_conflict(flight, self.user1_calendar)
            self.user1_flight_set_for_rank[i][1] = importance

    
    """
    @brief: 计算航班抵达时间差
    @param flight1: 航班1
    @param flight2: 航班2
    @return: 航班抵达时间差
    """
    def arrival_time_difference(self, flight1, flight2) -> int:
        flight1_end = self.parse_time(flight1["start"][:6] + flight1["end"], self.parse_time(flight1["start"]))
        flight2_end = self.parse_time(flight2["start"][:6] + flight2["end"], self.parse_time(flight2["start"]))
        
        time_difference = abs((flight1_end - flight2_end).seconds // 60)  # 以分钟为单位
        return time_difference

    def factor3(self):
        

        for i, comb in enumerate(self.all_flight_combs):
            self.all_flight_combs_for_rank[i][4] = self.arrival_time_difference(comb[0], comb[1])

    
    def get_final_rank(self):
        self.factor1()
        self.factor3()

        for i, comb in enumerate(self.all_flight_combs_for_rank):
            user0_flight, user1_flight = comb[0], comb[1]
            for _, flight_for_rank in enumerate(self.user0_flight_set_for_rank):
                if user0_flight == flight_for_rank[0]:
                    self.all_flight_combs_for_rank[i][2] += flight_for_rank[1]
                    self.all_flight_combs_for_rank[i][3] += flight_for_rank[2]
            for _, flight_for_rank in enumerate(self.user1_flight_set_for_rank):
                if user1_flight == flight_for_rank[0]:
                    self.all_flight_combs_for_rank[i][2] += flight_for_rank[1]
                    self.all_flight_combs_for_rank[i][3] += flight_for_rank[2]
        
        # 排序优先级: comb[2] > comb[3] > comb[4]
        self.all_flight_combs_for_rank.sort(key=lambda comb: (comb[2], comb[3], comb[4]))

        for _, comb in enumerate(self.all_flight_combs_for_rank):
            self.combs_rank.append((comb[0], comb[1]))

    def get_agent_rank(self, agent_comb):
        # print(f"agent_comb: {agent_comb}")
        # input("Press Enter to continue...")
        return self.combs_rank.index(agent_comb)


if __name__ == "__main__":
    # users_index = trans_userdata_to_prompt()
    # agent_response = get_respond()
    # print(f"agent_response: {agent_response}")
    # input("Press Enter to continue...")
    # agent_flight_comb = myutils.trans_agent_output(agent_response)

    user0_data = None
    user1_data = None

    # 根据索引获取用户信息
    user_basic_path = "./dialop/game_prompt"
    with open(os.path.join(user_basic_path, "user0.json"), 'r', encoding='utf-8') as f:
        user0_datas = json.load(f)
        user0_data = user0_datas[0]
        # user0_data = user0_datas[users_index[0]]
    with open(os.path.join(user_basic_path, "user1.json"), 'r', encoding='utf-8') as f:
        user1_datas = json.load(f)
        user1_data = user1_datas[0]

    my_flame = EvaluateFlame(user0_data, user1_data)
    my_flame.get_final_rank()
    # print(my_flame.all_flight_combs)
    print(f"Here is the ranked flight combinations:")
    for i, comb in enumerate(my_flame.all_flight_combs_for_rank):
        print(f"importance: {comb[2]}, price: {comb[3]}, arrival time difference: {comb[4]}") 
    input("Press Enter to continue...")
    print(f"len(my_flame.all_flight_combs): {len(my_flame.all_flight_combs)}")
    # print(f"agent_comb's rank: {my_flame.get_agent_rank(agent_flight_comb)}")

    # # 产生所有的航班组
    # user0_flight_set = []
    # all_flight_sets = []
    # for user0_flight in user0_data["Flights"]:
    #     for user1_flight in user1_data["Flights"]:
    #         all_flight_sets.append((user0_flight, user1_flight))
    
    # print(all_flight_sets)
    # input("Press Enter to continue...")