import os  
import re  
  
def process_file(file_path, mode):  
    matches = []  
    with open(file_path, 'r', encoding='utf-8') as file:  
        lines = file.readlines()  
  
        in_section = False  
        current_section = []  
  
        for line in lines:  
            if mode == 'p':
                if "PLANNING!!!!!!!!!!!!!!!!!!!!" in line:  
                    in_section = True  
                    current_section = []  
                elif "REASONING!!!!!!!!!!!!!!!!!!!!" in line:  
                    if in_section and current_section:  
                        matches.append(current_section)  
                    in_section = False  
                elif in_section:  
                    current_section.append(line.strip())  
            elif mode == 'r':
                if "REASONING!!!!!!!!!!!!!!!!!!!!" in line:  
                    in_section = True  
                    current_section = []  
                elif "RAW ACTING!!!!!!!!!!!!!!!!!" in line:  
                    if in_section and current_section:  
                        matches.append(current_section)  
                    in_section = False  
                elif in_section:  
                    current_section.append(line.strip())  
            elif mode == 'a':
                if "RAW ACTING!!!!!!!!!!!!!!!!!" in line:  
                    in_section = True  
                    current_section = []  
                elif "ACTING!!!!!!!!!!!!!!!!!!!!" in line:  
                    if in_section and current_section:  
                        matches.append(current_section)  
                    in_section = False  
                elif in_section:  
                    current_section.append(line.strip())  
            elif mode == 'f':
                if "REFLECTING!!!!!!!!!!!!!!!!!!!!" in line:  
                    in_section = True  
                    current_section = []  
                elif "REASONING!!!!!!!!!!!!!!!!!!!!" in line:  
                    if in_section and current_section:  
                        matches.append(current_section)  
                    in_section = False  
                elif in_section:  
                    current_section.append(line.strip())  
  
    return matches  
  
def count_words_and_average(matches):  
    total_words = 0  
    num_sections = len(matches)  
  
    for section in matches:  
        words = ' '.join(section).split()  
        total_words += len(words)  
  
    if num_sections > 0:  
        avg_words_per_section = total_words / num_sections  
    else:  
        avg_words_per_section = 0  
  
    return num_sections, avg_words_per_section  
  
def main(folder_path, mode):  
    total_matches = 0  
    total_words = 0  
    total_sections = 0  
  
    for root, dirs, files in os.walk(folder_path):  
        for file in files:  
            file_path = os.path.join(root, file)  
            if 'praf' not in file_path:
                continue
            matches = process_file(file_path, mode)  
            num_sections, avg_words_per_section = count_words_and_average(matches)  
  
            total_matches += num_sections  
            total_sections += num_sections  
            if num_sections > 0:  
                total_words += avg_words_per_section * num_sections  # This line is actually redundant here  
                # But we keep it for clarity in terms of the final average calculation  
  
    if total_sections > 0:  
        overall_avg_words_per_section = total_words / total_sections  
    else:  
        overall_avg_words_per_section = 0  

    if mode == 'p':
        # print(f"Total number of PLANNING sections found: {total_matches}")  
        # print(f"Average number of words per PLANNING: {overall_avg_words_per_section:.2f}")  
        print(f"({total_matches}, {overall_avg_words_per_section:.2f})", end=" ")
    elif mode == 'r':
        # print(f"Total number of REASONING sections found: {total_matches}")  
        # print(f"Average number of words per REASONING: {overall_avg_words_per_section:.2f}")  
        print(f"({total_matches}, {overall_avg_words_per_section:.2f})", end=" ")
    elif mode == 'a':
        # print(f"Total number of ACTING sections found: {total_matches}")  
        # print(f"Average number of words per ACTING: {overall_avg_words_per_section:.2f}")  
        print(f"({total_matches}, {overall_avg_words_per_section:.2f})", end=" ")
    elif mode == 'f':
        # print(f"Total number of REFLECTING sections found: {total_matches}")  
        # print(f"Average number of words per REFLECTING: {overall_avg_words_per_section:.2f}") 
        print(f"({total_matches}, {overall_avg_words_per_section:.2f})", end=" ")

    return total_matches, overall_avg_words_per_section 
  
if __name__ == "__main__":  
    folder_path = "/home/hadoop-aipnlp/dolphinfs_hdd_hadoop-aipnlp/qisiyuan02/AgentLean/log/lean/claude_3.5_sonnet/no"
    p1, p2 = main(folder_path, 'p')
    r1, r2 = main(folder_path, 'r')
    a1, a2 = main(folder_path, 'a')
    f1, f2 = main(folder_path, 'f')
    print(f"{(p1 * p2 + r1 * r2 + a1 * a2 + f1 * f2) / (p1 + r1 + a1 + f1)}") 
    111 * 8 * (223.61 * 1 + (224.41 + 222.46 + 272.48) *10)/ 1000000
    