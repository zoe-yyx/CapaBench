



# CUDA_VISIBLE_DEVICES=2 nohup torchrun --master_port 52124 run_agent.py --test_model_name Mistral-7B-instruct-v0.2 --mode reasoning action reflection  --start_index 108 --original_correct 0 --ip http://10.166.100.111:8080 > ./log/lean/Mistral-7B-instruct-v0.2/no/raf_new_108.out 2>&1 



# CUDA_VISIBLE_DEVICES=1 nohup torchrun --master_port 52125 run_agent.py --test_model_name Mistral-8X7B-instruct-v0.1 --mode planning reasoning reflection  --start_index 0 --original_correct 0 --ip http://10.166.182.41:8080 > ./log/lean/Mistral-8X7B-instruct-v0.1/no/prf_new.out 2>&1 &
CUDA_VISIBLE_DEVICES=0 nohup torchrun --master_port 52126 run_agent.py --test_model_name Mistral-8X7B-instruct-v0.1 --mode reasoning action reflection  --start_index 0 --original_correct 0 --ip http://10.166.182.41:8080 > ./log/lean/Mistral-8X7B-instruct-v0.1/no/raf_new.out 2>&1 &
