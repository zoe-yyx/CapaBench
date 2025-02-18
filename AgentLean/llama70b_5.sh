
CUDA_VISIBLE_DEVICES=0 nohup torchrun --master_port 5734 run_agent.py --test_model_name Mistral-8X7B-instruct-v0.1 --mode action reflection  --start_index 85 --original_correct 8 --ip http://10.166.190.82:8080 > ./log/lean/Mistral-8X7B-instruct-v0.1/no/af_new_85.out 2>&1 &
CUDA_VISIBLE_DEVICES=0 nohup torchrun --master_port 5735 run_agent.py --test_model_name Mistral-8X7B-instruct-v0.1 --mode reasoning action  --start_index 0 --original_correct 0 --ip http://10.166.190.82:8080 > ./log/lean/Mistral-8X7B-instruct-v0.1/no/ra_new.out 2>&1 &
