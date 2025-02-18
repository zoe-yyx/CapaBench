
# CUDA_VISIBLE_DEVICES=1 nohup torchrun --master_port 7504 run_agent.py --test_model_name Mistral-8X7B-instruct-v0.1 --mode action  --start_index 0 --original_correct 0 --ip http://10.166.180.57:8080 > ./log/coq/Mistral-8X7B-instruct-v0.1/no/a_new.out 2>&1 
CUDA_VISIBLE_DEVICES=1 nohup torchrun --master_port 7504 run_agent.py --test_model_name Mistral-8X7B-instruct-v0.1 --mode reflection  --start_index 11 --original_correct 2 --ip http://10.166.180.57:8080 > ./log/coq/Mistral-8X7B-instruct-v0.1/no/f_new_11.out 2>&1 
