

# CUDA_VISIBLE_DEVICES=3 nohup torchrun --master_port 49234 run_agent.py --test_model_name Mistral-8X7B-instruct-v0.1 --mode planning reflection  --start_index 0 --original_correct 0 --ip http://10.166.180.57:8080 > ./log/coq/Mistral-8X7B-instruct-v0.1/no/pf_new.out 2>&1 
CUDA_VISIBLE_DEVICES=3 nohup torchrun --master_port 49234 run_agent.py --test_model_name Mistral-8X7B-instruct-v0.1 --mode reasoning reflection  --start_index 28 --original_correct 5 --ip http://10.166.180.109:8080 > ./log/coq/Mistral-8X7B-instruct-v0.1/no/rf_new_28.out 2>&1 