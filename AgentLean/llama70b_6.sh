CUDA_VISIBLE_DEVICES=1 nohup torchrun --master_port 55123 run_agent.py --test_model_name llama3-70B-instruct --mode planning reasoning action  --start_index 106 --original_correct 8 --ip http://10.166.184.90:8080 > ./log/lean/llama3-70B-instruct/no/pra_new_106.out 2>&1 
CUDA_VISIBLE_DEVICES=1 nohup torchrun --master_port 55123 run_agent.py --test_model_name llama3-70B-instruct --mode planning action reflection  --start_index 77 --original_correct 12 --ip http://10.166.184.90:8080 > ./log/lean/llama3-70B-instruct/no/paf_new_77.out 2>&1 


CUDA_VISIBLE_DEVICES=1 nohup torchrun --master_port 55123 run_agent.py --test_model_name Mistral-8X7B-instruct-v0.1 --mode planning reasoning action  --start_index 0 --original_correct 0 --ip http://10.166.182.41:8080 > ./log/lean/Mistral-8X7B-instruct-v0.1/no/pra_new.out 2>&1 
CUDA_VISIBLE_DEVICES=1 nohup torchrun --master_port 55123 run_agent.py --test_model_name Mistral-8X7B-instruct-v0.1 --mode planning action reflection  --start_index 0 --original_correct 0 --ip http://10.166.182.41:8080 > ./log/lean/Mistral-8X7B-instruct-v0.1/no/paf_new.out 2>&1 
