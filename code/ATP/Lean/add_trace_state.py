
def add_trace_state_after_theorem(filename: str):
    with open(filename, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    new_lines = []
    inside_proof = False
    last_theorem_index = -1
    by_line_index = -1

    # 查找最后一个 theorem 语句的索引
    for i, line in enumerate(lines):
        if line.strip().startswith("theorem"):
            last_theorem_index = i

    # 从最后一个 theorem 之后查找 := by
    if last_theorem_index != -1:
        for i in range(last_theorem_index, len(lines)):
            if ":= by" in lines[i]:
                by_line_index = i
                break

    last_line = None

    # 如果找到了 := by 行，开始插入 trace_state
    if by_line_index != -1:
        for i, line in enumerate(lines):
            
            
            if i > by_line_index:
                # 获取当前行的缩进
                stripped_line = line.lstrip()
                indent = len(line) - len(stripped_line)

                # 检查当前行是否以 '｜' 开头（忽略前面的空格）
                if stripped_line and not stripped_line.startswith("|"):
                    if i == by_line_index + 1:
                        init_line = ' ' * indent + 'trace "Init State:"\n'
                        new_lines.append(init_line)
                    if last_line != None and i > by_line_index + 1:
                        new_lines.append(' ' * indent + f'trace "After executing statement: {last_line[: -1]}"\n')
                    # 如果不是以 ｜ 开头，插入 trace_state
                    trace_state_line = ' ' * indent + 'trace_state\n'
                    new_lines.append(trace_state_line)
                    
            
            new_lines.append(line)
            last_line = line
            
        stripped_line = line.lstrip()
        indent = len(line) - len(stripped_line)

        # 检查当前行是否以 '｜' 开头（忽略前面的空格）
        if stripped_line and not stripped_line.startswith("|"):
            if last_line != None and i > by_line_index + 1:
                new_lines.append(' ' * indent + f'trace "After executing statement: {last_line[: -1]}"\n')
            # 如果不是以 ｜ 开头，插入 trace_state
            trace_state_line = ' ' * indent + 'trace_state\n'
            new_lines.append(trace_state_line)

    else:
        # 如果没有找到 theorem 或 := by，就直接返回原文件
        new_lines = lines

    with open(filename, 'w', encoding='utf-8') as file:
        file.writelines(new_lines)


