from llm_agent import APIAgent
import time

agent1 = APIAgent('http://10.166.100.111:8080', 0, 0.9, 2048)
agent2 = APIAgent('http://10.166.190.82:8080', 0, 0.9, 2048)
agent3 = APIAgent('http://10.166.182.41:8080', 0, 0.9, 2048)



while True:
    
    response1 = agent1.llm_planning('You are Awesome!!!!! Print Hello World!!!', 'hello')
    response2 = agent2.llm_planning('You are Awesome!!!!! Print Hello World!!!', 'hello')
    response3 = agent2.llm_planning('You are Awesome!!!!! Print Hello World!!!', 'hello')
    print(response1)
    print(response2)
    print(response3)
    time.sleep(300)