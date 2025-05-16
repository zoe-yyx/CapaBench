# modes_474_0 = ["planning", "planning reasoning reflection", "reasoning action reflection", "reasoning"]
# modes_474_1 = ["reasoning action", "reasoning reflection", "planning action", "planning reasoning action"]
# modes_474_2 = ["reflection", "planning action reflection", "action reflection", "planning reasoning action reflection"]
# modes_474_3 = ["planning reasoning", "planning reflection", "action"]

# modes_81_0 = ["planning", "planning reasoning reflection", "reasoning action reflection", "reasoning"]
# modes_81_1 = ["reasoning action", "reasoning reflection", "planning action", "planning reasoning action"]
# modes_81_2 = ["reflection", "planning action reflection", "action reflection", "planning reasoning action reflection"]
# modes_81_3 = ["planning reasoning", "planning reflection", "action"]

# modes_291_00 = ["planning", "planning reasoning reflection", "reasoning action reflection", "reasoning"]
# modes_291_01 = ["reasoning action", "reasoning reflection", "planning action", "planning reasoning action"]
# modes_291_10 = ["reflection", "planning action reflection", "action reflection", "planning reasoning action reflection"]
# modes_291_11 = ["planning reasoning", "planning reflection", "action"]

modes_00 = ["planning", "planning reasoning reflection", "reasoning action reflection", "reasoning"]
modes_01 = ["reasoning action", "reasoning reflection", "planning action", "planning reasoning action"]
modes_10 = ["reflection", "planning action reflection", "action reflection", "planning reasoning action reflection"]
modes_11 = ["planning reasoning", "planning reflection", "action"]

# modes_00_qwen = ["reasoning action reflection"]
# modes_01_qwen = ["planning reasoning action"]
# modes_10_qwen = ["planning reasoning action reflection"]
# modes_11_qwen = ["reasoning"]

# modes_00_doubao = ["reasoning action reflection"]
# modes_01_doubao = ["planning reasoning action reflection"]
# modes_10_doubao = ["reasoning"]
# modes_11_doubao = []


# modes_00_8X7B = ["reasoning action reflection"]
# modes_01_8X7B = ["reasoning reflection"]
# modes_10_8X7B = ["action reflection", "planning reasoning action reflection"]
# modes_10_8X7B = ["planning reasoning action reflection"]
# modes_11_8X7B = ["planning reasoning action"]

# extra_8X7B_00 = ["reasoning"]
# extra_8X7B_01 = ["planning action"]

if __name__ == "__main__":
    
    def check(*args):
        modes = set()
        for mode in args:
            modes.update(mode)
        modes = list(modes)

        if len(modes) == 15:
            print("That's right!")
        else:
            print("Something wrong!")

    check(modes_474_0, modes_474_1, modes_474_2, modes_474_3)
