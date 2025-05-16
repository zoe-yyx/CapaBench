from collections import defaultdict
import re
import tiktoken
import time
from dateutil.parser import parse
from pathlib import Path
from itertools import cycle
class TimeoutException(Exception):
    """自定义异常类，用于处理超时情况"""
    pass

SEP = "=" * 20
SEP1 = "-" * 20

def run(console, env, players, max_length=4000):
    obss = env.reset()
    choose_ls=["planning","reasoning","action","reasoning","propose","message"]
    choose_ls=["planning","reasoning","action","reflection"]
    n=-1
    times=0
    
    console.print(env.game.all_prefs)
    console.print(env.game.num_prefs)
    max_length=200
    propose_time=0
    start_time = time.time()
    for t in range(max_length):
        
        console.rule("environment obs")
        
        
        obss["player"]="user" if obss["agent"].startswith('\nU') else "agent"
        obs="user" if obss["agent"].startswith('\nU') else "assistant"
        console.print(obss)
        
        players["agent"].add_to_dialog(obs,obss[obss["player"]])
        [player.observe(obss[pname]) for pname, player in players.items()]
        #   if obss["turn_player"]=="agent" and not obss.get("error"):
        #     n=(n+1)%6
        #   if n==4 and not obss.get("error"):
        #       time+=1
        #   kw={"env":env,"mode":choose_ls[n],"time":time}
        #   resp = players[obss["turn_player"]].respond(kw)
        #   obss, resample = env.step(resp)
        #   if obss.get("search"):
        #       n=0
        #   if obss['user']==" [message] I want add a request":
        #       n=n-1
        #   obss["choice"]=choose_ls[n]
        #   obss["time"]=time
        #   if obss["done"]:
        #     break
        before_n=n

        if obss["turn_player"]=="agent":
            if n==1:
                n=2
            elif n==0:
                n=1
            elif n==2:
                if obss.get("error"):
                    n=2
                elif obss.get("score"):
                    score=obss['score']
                    
                    if score <  0.6 and propose_time <1:
                        n=3
                        players["agent"].add_to_dialog("user","Result is too bad.You need to reflect and reasoning again")
                        propose_time+=1
              
                else: 
                    n=1
            elif n==3:
                n=1
            else:
                n=0    
                times+=1
                propose_time=0
                
            # if n==4 and not obss.get("error"):
            #   time+=1
        end_time = time.time()

# 计算执行时间
        
        kw={"env":env,"mode":choose_ls[n],"time":times}
        try:
            execution_time = end_time - start_time
            if execution_time > 12000:  # 10 分钟 = 600 秒
                    raise TimeoutException("Execution time exceeded 20 minutes")
            resp = players[obss["turn_player"]].respond(kw)
            mode=kw["mode"] 
            obss, resample = env.step(resp,mode)
            
        except Exception as e:
    # 打印错误信息
            print(f"An error occurred: {e}")
            import traceback
            error_message = traceback.format_exc()
            print("发生错误：")
            print(error_message)
            break
        
        
        obss["choice"]=choose_ls[n]
        if obss.get("process"):
            n=before_n
        obss["time"]=times
        
        if obss.get("plan"):
            n=-1
        if obss.get("search"):
            n=1
       
            
                
                
        if obss["done"]:
            
            break
        if obss['info']['num_msgs']>=200:
            
            break
    print(obss)

def run_multiagent(console, env, players, max_length=45):
    player_cycle = cycle(players.keys())
    obss = env.reset()
    for t in range(max_length):
        console.rule("environment obs")
        console.print(obss)
        [player.observe(obss[pname]) for pname, player in players.items()]
        # Cycle through players, letting them speak if it's their turn
        next_player = next(player_cycle)
        while next_player not in obss["turn_players"]:
            next_player = next(player_cycle)
        resp = players[next_player].respond()
        obss, resample = env.step(resp, next_player)
        if obss["done"]:
            break
    print(obss)

def num_tokens(text):
  return 100
def count_words(action_log):
    count = 0
    for msg in action_log:
        if msg["type"] == "message":
            count += len(msg["message"]["data"].split(" "))
    return count

def retry(max_attempts=3, delay=60, allowed_exceptions=None):
    if allowed_exceptions is None:
        allowed_exceptions = []

    def decorator(func):
        def wrapper(*args, **kwargs):
            attempts = 0
            while attempts < max_attempts:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if type(e) in allowed_exceptions:
                        print(f"Attempt {attempts+1} failed: {type(e)} {e}")
                        attempts += 1
                        time.sleep(delay)
                    else:
                        raise e
            print(f"Max attempts reached. Giving up.")
        return wrapper
    return decorator

class Logger:

    def __init__(self, logfile):
        self.logfile = logfile
        self.buffer = ""
        self.logs = defaultdict(list)

    def write(self, title="", value=""):
        self.buffer += f"\n\n{SEP} {title} {SEP}\n\n>{value}<"

    def log(self, key, value, title=""):
        self.logs[key].append(f"\n\n{SEP1} {title} {SEP1}\n>{value}")

    def flush(self):
        with open(self.logfile, "a") as f:
            f.write(self.buffer)
        self.buffer = ""

    def flush_key(self, key, title="", joiner=""):
        with open(self.logfile, "a") as f:
            f.write(f"\n\n{SEP} {title} {SEP}\n{joiner.join(self.logs[key])}")
        self.logs[key] = []

    def close(self):
        self.flush()
