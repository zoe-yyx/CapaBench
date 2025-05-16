from thefuzz import fuzz
import traceback
from pathlib import Path
import random
import numpy as np
import json
from dialop.games import PlanningGame
dic={}

for seed in range(0,250):
    
    random.seed(seed)
    np.random.seed(seed)
    p=PlanningGame({})
    p.reset()
    dic[seed]=str(p.all_prefs)
print(dic)
with open("res.json",'w') as f:
    json.dump(dic,f)