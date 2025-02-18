import sympy as sp
from latex2sympy2 import latex2sympy
from calculator import safe_eval

def _fix_fracs(string):
    substrs = string.split("\\frac")
    new_str = substrs[0]
    if len(substrs) > 1:
        substrs = substrs[1:]
        for substr in substrs:
            new_str += "\\frac"
            if substr[0] == "{":
                new_str += substr
            else:
                try:
                    assert len(substr) >= 2
                except:
                    return string
                a = substr[0]
                b = substr[1]
                if b != "{":
                    if len(substr) > 2:
                        post_substr = substr[2:]
                        new_str += "{" + a + "}{" + b + "}" + post_substr
                    else:
                        new_str += "{" + a + "}{" + b + "}"
                else:
                    if len(substr) > 2:
                        post_substr = substr[2:]
                        new_str += "{" + a + "}" + b + post_substr
                    else:
                        new_str += "{" + a + "}" + b
    string = new_str
    return string

def _fix_a_slash_b(string):
    if len(string.split("/")) != 2:
        return string
    a = string.split("/")[0]
    b = string.split("/")[1]
    try:
        a = int(a)
        b = int(b)
        assert string == "{}/{}".format(a, b)
        new_string = "\\frac{" + str(a) + "}{" + str(b) + "}"
        return new_string
    except:
        return string

def _remove_right_units(string):
    # "\\text{ " only ever occurs (at least in the val set) when describing units
    if "\\text{ " in string:
        splits = string.split("\\text{ ")
        assert len(splits) == 2
        return splits[0]
    else:
        return string

def _fix_sqrt(string):
    if "\\sqrt" not in string:
        return string
    splits = string.split("\\sqrt")
    new_string = splits[0] 
    for split in splits[1:]:
        if split[0] != "{":
            a = split[0]
            new_substr = "\\sqrt{" + a + "}" + split[1:]
        else:
            new_substr = "\\sqrt" + split
        new_string += new_substr
    return new_string

def _strip_string(string):
    # linebreaks  
    string = string.replace("\n", "")
    #print(string)

    # remove inverse spaces
    string = string.replace("\\!", "")
    #print(string)

    # replace \\ with \
    string = string.replace("\\\\", "\\")
    #print(string)

    # replace tfrac and dfrac with frac
    string = string.replace("tfrac", "frac")
    string = string.replace("dfrac", "frac")
    #print(string)

    # remove \left and \right
    string = string.replace("\\left", "")
    string = string.replace("\\right", "")
    #print(string)
    
    # Remove circ (degrees)
    string = string.replace("^{\\circ}", "")
    string = string.replace("^\\circ", "")

    # remove dollar signs
    string = string.replace("\\$", "")
    
    # remove units (on the right)
    string = _remove_right_units(string)

    # remove percentage
    string = string.replace("\\%", "")
    string = string.replace("\%", "")

    # " 0." equivalent to " ." and "{0." equivalent to "{." Alternatively, add "0" if "." is the start of the string
    string = string.replace(" .", " 0.")
    string = string.replace("{.", "{0.")
    # if empty, return empty string
    if len(string) == 0:
        return string
    if string[0] == ".":
        string = "0" + string

    # to consider: get rid of e.g. "k = " or "q = " at beginning
    if len(string.split("=")) == 2:
        if len(string.split("=")[0]) <= 2:
            string = string.split("=")[1]

    # fix sqrt3 --> sqrt{3}
    string = _fix_sqrt(string)

    # remove spaces
    string = string.replace(" ", "")

    # \frac1b or \frac12 --> \frac{1}{b} and \frac{1}{2}, etc. Even works with \frac1{72} (but not \frac{72}1). Also does a/b --> \\frac{a}{b}
    string = _fix_fracs(string)

    # manually change 0.5 --> \frac{1}{2}
    if string == "0.5":
        string = "\\frac{1}{2}"

    # NOTE: X/Y changed to \frac{X}{Y} in dataset, but in simple cases fix in case the model output is X/Y
    string = _fix_a_slash_b(string)

    return string


def is_equiv(str1, str2, verbose=False):
    try:
        if str1 is None and str2 is None:
            print("WARNING: Both None")
            return True
        if str1 is None or str2 is None:
            return False

        try:
            ss1 = _strip_string(str1)
            ss2 = _strip_string(str2)
            if verbose:
                print(ss1, ss2)
            return ss1 == ss2
        except:
            return str1 == str2
    except:
        return False

# def is_equiv(str1, str2, verbose=False):
#     try:
#         if float(str1) == float(str2) or abs(float(str1) - float(str2)) < 0.001:
       
#             return True
#         else:
#             return False
#     except Exception as e:
#         # print(1)
#         # print(e)
#         pass
    
#     try:
#         str1 = str(str1)
#         str2 = str(str2)
#         # 将 LaTeX 输入转换为 Sympy 表达式
#         sympy_expr = latex2sympy(str1)

        
#         # 化简表达式
#         simplified_expr = sp.simplify(sympy_expr)

        
#         # 将表达式的结果转换为浮点数形式
#         float_result = simplified_expr.evalf()


#         sympy_expr2 = latex2sympy(str2)

        
#         # 化简表达式
#         simplified_expr2 = sp.simplify(sympy_expr2)

        
#         # 将表达式的结果转换为浮点数形式
#         float_result2 = simplified_expr2.evalf()

        
        
#         # 返回化简后的浮点数结果
        
#         if float_result == float_result2 or abs(float_result - float_result2) < 0.001:
#             return True
#         else:
#             return False
#     except Exception as e:
#         # print(2)
#         # print(e)
#         pass
 
#     try:
#         str1 = str(str1)
#         str2 = str(str2)
#         if str1 is None and str2 is None:
#             print("WARNING: Both None")

#             return True
#         if str1 is None or str2 is None:
#             return False

#         try:
#             ss1 = _strip_string(str1)
#             ss2 = _strip_string(str2)
#             if verbose:
#                 print(ss1, ss2)
#             print(3)
#             return ss1 == ss2
#         except:
#             print(4)
#             return str1 == str2
#     except:
#         # print(4)
#         return False




# def is_equiv(str1, str2, if_base_value: bool, verbose=False):
#     if not if_base_value:
#         if str1 is None and str2 is None:
#             print("WARNING: Both None")
#             return True
#         if str1 is None or str2 is None:
#             return False

#         try:
#             ss1 = _strip_string(str1)
#             ss2 = _strip_string(str2)
#             if verbose:
#                 print(ss1, ss2)
#             return ss1 == ss2
#         except:
#             return str1 == str2 
#     else:
#         try:
#             if safe_eval(str1) == safe_eval(str2):
#                 return True
#         except:
#             pass
#         try:
#             if abs(safe_eval(str1) - safe_eval(str2)) < 0.001:
#                 return True
#         except:
#             pass
#         return False

    
# print(is_equiv('1 + i', '1.0 + 0.5*2 i', True))
# print(is_equiv('(1, 3)', '(1, 3)', True))