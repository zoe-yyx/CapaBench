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




