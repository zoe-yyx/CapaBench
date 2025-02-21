def has_sorry(action, theorem):
    # 定位theorem在action中的位置
    index = action.find(theorem)
    
    # 如果theorem不在action中，返回False
    if index == -1:
        return False
    
    # 检查theorem之后是否有sorry出现
    # index + len(theorem) 是theorem在action中的结束位置
    return "sorry" in action[index + len(theorem):]

def qed(results, action, problem, theorem):
    return (results['StdOut'] == "Buile Successfully!") and (problem in action or theorem in action)

### 没用，因为Isabelle没证明完成就一定显示error
def has_error(results):
    string_result = ", ".join(f"{k}: {v}" for k, v in results.items())
    if "error: unsolved goals" not in string_result and "error:" in string_result:
        return True
    return False