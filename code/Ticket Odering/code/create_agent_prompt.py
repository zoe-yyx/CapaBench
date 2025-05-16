import json
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from llm_agent import llm_agent


def mywrite(flight_data, user_shared_calendar, user_id, target_path):
    with open(target_path, 'a', encoding='utf-8') as f:
        f.write(f"User {user_id} Information\nFlights:\n")
        f.write("id | carrier | price | times\n")
        for flight in flight_data:
            f.write(f"{flight['id']} | {flight['carrier']} | {flight['price']} | {flight['start']} - {flight['end']}\n")
        
        f.write("Calendar:\n")
        f.write("id | times\n")
        for calendar in user_shared_calendar:
            f.write(f"{calendar['id']} | {calendar['start']} - {calendar['end']}\n")

def mywrite2(flight_data, user_data, user_id, target_path):
    with open(target_path, 'a', encoding='utf-8') as f:
        # f.write("\nThe information Users given is below.\n")
        f.write(f"\nUser {user_id}: Here is my own calendars, and the importance part shows the importance of the corresponding calendar.\n")
        f.write("Private calendar:\nid | importance | times\n")
        for private_calendar in user_data["Private calendar"]:
            f.write(f"{private_calendar['id']} | ({private_calendar['importance']}) | {private_calendar['start']} - {private_calendar['end']}\n")
        f.write("Shared calendar (visible to assistant):\nid | importance | times\n")
        for shared_calendar in user_data["Shared calendar (visible to assistant)"]:
            f.write(f"{shared_calendar['id']} | ({shared_calendar['importance']}) | {shared_calendar['start']} - {shared_calendar['end']}\n")


# 函数功能: 将用户数据转换为prompt,并返回用户信息索引
def trans_userdata_to_prompt():
    # user_basic_path = "./dialop/game_prompt"
    user_basic_path = os.path.join('dialop', 'game_prompt')
    # agent_prompt_path = "./dialop/prompts/mediation_agent.txt"
    agent_prompt_path = os.path.join('dialop', 'prompts', 'mediation_agent.txt')
    # target_prompt_path = "./dialop/game_prompt/agent.txt"
    target_prompt_path = os.path.join('dialop', 'game_prompt', 'agent.txt')

    user0_flight = None
    user0_Shared_calendar = None
    user1_flight = None
    user1_Shared_calendar = None

    print(os.path.join(user_basic_path, "user0.json"))
    input("Press Enter to continue...")

    # 获取json文件
    with open(os.path.join(user_basic_path, "user0.json"), 'r', encoding='utf-8') as f:
        user0_datas = json.load(f)
        user0_flight = user0_datas[0]["Flights"]
        user0_data = user0_datas[0] 
        user0_Shared_calendar = user0_datas[0]["Shared calendar (visible to assistant)"]

    with open(os.path.join(user_basic_path, "user1.json"), 'r', encoding='utf-8') as f:
        user1_datas = json.load(f)
        user1_flight = user1_datas[0]["Flights"]
        user1_data = user1_datas[0]
        user1_Shared_calendar = user1_datas[0]["Shared calendar (visible to assistant)"]

    # 生成prompt
    with open(agent_prompt_path, 'r', encoding='utf-8') as prompt_f, open(target_prompt_path, 'w', encoding='utf-8') as target_f:
        for line in prompt_f:
            target_f.write(line)

    with open(target_prompt_path, 'a', encoding='utf-8') as f:
        f.write("\nTRIP 2.\n\n")

    mywrite(user0_flight, user0_Shared_calendar, 0, target_prompt_path)
    mywrite(user1_flight, user1_Shared_calendar, 1, target_prompt_path)

    with open(target_prompt_path, 'a', encoding='utf-8') as f:
        f.write("\nThe information Users given is below.\n")
    mywrite2(user0_flight, user0_data, 0, target_prompt_path)
    mywrite2(user1_flight, user1_data, 1, target_prompt_path)

    with open(target_prompt_path, 'a', encoding='utf-8') as f:
        f.write("\nAnd here is the content you should give to me:\n")

    return (0, 0)

def get_respond():
    prompt = None
    with open('./dialop/game_prompt/agent.txt', 'r', encoding='utf-8') as f:
        prompt = f.read()

    print(prompt)
    input("Press Enter to continue...")

    agent = llm_agent.OpenAIAgent(api_key="1790715889671905303",
                                  api_base="https://aigc.sankuai.com/v1/openai/native",
                                  model_name="gpt-4o-mini"
    )

    content = agent.get_response(prompt)
    # from openai import OpenAI
    # client = OpenAI(
    #     api_key="sk-proj-QuZ4HQTpciSHcyTwC7WOT3BlbkFJhaW0HEVCWFTwDWUGvXpk",
    # )

    # completion = client.chat.completions.create(
    #     messages=[
    #         {
    #             "role": "assistant",
    #             "content": prompt
    #         }
    #     ],
    #     model="gpt-4o-mini",
    # )

    return content

# def creat_agent_prompt():
#     pass

# with open('./dialop/game_prompt/agent.txt', 'r', encoding='utf-8') as f:
#     agent = f.read()

# print(agent)
if __name__ == "__main__":
    trans_userdata_to_prompt()
    print(get_respond())