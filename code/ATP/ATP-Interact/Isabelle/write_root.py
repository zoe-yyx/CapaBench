import os

def writeRoot(theorem, file_mode):


    # 创建 ROOT 文件内容
    with open(f"./{file_mode}/ROOT", 'w', encoding='utf-8') as root_file:
        # 写入固定的部分
        root_file.write("session MyProofs = HOL +\n")
        root_file.write("  options [document = true]\n")
        root_file.write("  theories\n")
        root_file.write(f"    {theorem}\n")


