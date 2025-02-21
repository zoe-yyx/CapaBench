import re

def has_sorry(action, theorem):
    # 定位theorem在action中的位置
    index = action.find(theorem)
    
    # 如果theorem不在action中，返回False
    if index == -1:
        return False
    
    # 检查theorem之后是否有sorry出现
    # index + len(theorem) 是theorem在action中的结束位置
    return "sorry" in action[index + len(theorem):]

def qed(results):
    string_result = ", ".join(f"{k}: {v}" for k, v in results.items())
    if "error:" not in string_result:
        return True
    return False

def has_error(results):
    string_result = ", ".join(f"{k}: {v}" for k, v in results.items())
    error_pattern = r'error:(?!\s*unsolved\s*goals\b)'  
      
    # 如果正则表达式在 string_result 中找到匹配项，则返回 True  
    if re.search(error_pattern, string_result):  
        return True 
    return False

