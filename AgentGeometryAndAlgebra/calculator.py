# import math

# def safe_eval(expression):
#     # 限制 eval 的环境，只允许使用 math 模块中的方法和属性
#     allowed_functions = {k: getattr(math, k) for k in dir(math) if not k.startswith("__")}
    
#     # 第一步：尝试计算表达式
#     try:
#         # 使用局部环境，只包括数学函数和常量
#         return eval(expression, {"__builtins__": {}}, allowed_functions)
#     except Exception as e:
#         # 如果第一次计算失败，尝试处理表达式中的三角函数
#         try:
#             # 替换常见的三角函数为 math 模块中的对应函数
#             expression = expression.replace("sin", "math.sin")
#             expression = expression.replace("cos", "math.cos")
#             expression = expression.replace("tan", "math.tan")
#             expression = expression.replace("sqrt", "math.sqrt")
            
#             # 再次尝试计算处理后的表达式
#             return eval(expression, {"__builtins__": {}}, allowed_functions)
#         except Exception as e2:
#             # 如果处理后仍然出错，返回 None
#             return None

import sympy as sp
from latex2sympy2 import latex2sympy


def safe_eval(latex_input):
    try:
        # 将 LaTeX 输入转换为 Sympy 表达式
        sympy_expr = latex2sympy(latex_input)
        
        # 化简表达式
        simplified_expr = sp.simplify(sympy_expr)
        
        # 将表达式的结果转换为浮点数形式
        float_result = simplified_expr.evalf()
        
        # 返回化简后的浮点数结果
        return float_result
    except:
        return latex_input

# print(safe_eval('4x^4 - 6x^3'))
# print(safe_eval('4^4') - safe_eval(256) < 0.001)
# print((safe_eval('4x^4 - 6x^3 + 8x^2') - safe_eval('y') < 0.0001) == True)
# print(safe_eval('4x^4 - 6x^3 + 8x^2') == 'y')


# # 示例输入
# latex_input = r"\frac{1}{2} + 3 * 7 + \sin(2/3 * \pi)"
# latex_input = r"\frac{1}{3a} + b + \pi + 3"
# latex_input2 = "\\frac{180 - 42}{2}"

# # 调用函数
# try:
    
#     result2 = safe_eval(latex_input2)
#     print(result2 == None)
#     print("输入的 LaTeX 表达式:", latex_input2)
#     print("化简后的浮点数形式的结果:", type(result2))
#     print(float(result2))
#     print(result2 == 54)
#     print(None and True)
# except Exception as e:
#     print("发生错误:", e)


