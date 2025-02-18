


# CUDA_VISIBLE_DEVICES=3 nohup torchrun --master_port 5524 run_agent.py --test_model_name Mistral-7B-instruct-v0.2 --mode reasoning reflection  --start_index 65 --original_correct 0 --ip http://10.166.100.111:8080 > ./log/lean/Mistral-7B-instruct-v0.2/no/rf_new_65.out 2>&1 &


# CUDA_VISIBLE_DEVICES=3 nohup torchrun --master_port 5525 run_agent.py --test_model_name Mistral-8X7B-instruct-v0.1 --mode planning reflection  --start_index 0 --original_correct 0 --ip http://10.166.190.82:8080 > ./log/lean/Mistral-8X7B-instruct-v0.1/no/pf_new.out 2>&1 &


CUDA_VISIBLE_DEVICES=3 nohup torchrun --master_port 5526 run_agent.py --test_model_name Mistral-8X7B-instruct-v0.1 --mode reasoning reflection  --start_index 0 --original_correct 0 --ip http://10.166.190.82:8080 > ./log/lean/Mistral-8X7B-instruct-v0.1/no/rf_new.out 2>&1 &
