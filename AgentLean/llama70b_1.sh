

CUDA_VISIBLE_DEVICES=0 nohup torchrun --master_port 7501 run_agent.py --test_model_name llama3-70B-instruct --mode reasoning  --start_index 82 --original_correct 6 --ip http://10.166.161.7:8080 > ./log/lean/llama3-70B-instruct/no/r_new_82.out 2>&1 


CUDA_VISIBLE_DEVICES=0 nohup torchrun --master_port 7501 run_agent.py --test_model_name Mistral-8X7B-instruct-v0.1 --mode planning  --start_index 0 --original_correct 0 --ip http://10.166.190.82:8080 > ./log/lean/Mistral-8X7B-instruct-v0.1/no/p_new.out 2>&1 
CUDA_VISIBLE_DEVICES=0 nohup torchrun --master_port 7501 run_agent.py --test_model_name Mistral-8X7B-instruct-v0.1 --mode reasoning  --start_index 0 --original_correct 0 --ip http://10.166.190.82:8080 > ./log/lean/Mistral-8X7B-instruct-v0.1/no/r_new.out 2>&1 



