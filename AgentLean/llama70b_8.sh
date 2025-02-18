
CUDA_VISIBLE_DEVICES=3 nohup torchrun --master_port 41234 run_agent.py --test_model_name Mistral-8X7B-instruct-v0.1 --mode planning reasoning action reflection  --start_index 0 --original_correct 0 --ip http://10.166.182.41:8080 > ./log/lean/Mistral-8X7B-instruct-v0.1/no/praf_new.out 2>&1 
CUDA_VISIBLE_DEVICES=3 nohup torchrun --master_port 41234 run_agent.py --test_model_name Mistral-8X7B-instruct-v0.1 --mode default --start_index 0 --original_correct 0 --ip http://10.166.182.41:8080 > ./log/lean/Mistral-8X7B-instruct-v0.1/no/default_new.out 2>&1 
