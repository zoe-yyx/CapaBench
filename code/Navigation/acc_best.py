import os
import json
acc_num=0
acc_add=0
output_dir="/home/hadoop-aipnlp/dolphinfs_hdd_hadoop-aipnlp/EVA/fengchao/dialop/dialop/out_best"
for root, dirs, files in os.walk(output_dir):
        for file in files:
            if file.endswith(".out"):
                file_path = os.path.join(root, file)

                with open(file_path, 'r') as f:
                    lines = f.readlines()
                    if lines:
                        last_line = lines[-1].strip()
                        last_line = last_line.replace("'", "\"")
                        last_line = last_line.replace("True", "true")
                        last_line = last_line.replace("\n", "\\n")
                 
                        try:
                            last_line_data = json.loads(last_line)
                            reward_normalized = last_line_data['info']['reward_normalized']
                            acc_add+=reward_normalized
                            acc_num+=1
                        except:
                            reward_normalized = 0
print(acc_add/acc_num)