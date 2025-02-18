
CUDA_VISIBLE_DEVICES=1 nohup torchrun --master_port 7504 run_agent.py --test_model_name Mistral-8X7B-instruct-v0.1 --mode reflection  --start_index 31 --original_correct 0 --ip http://10.166.190.82:8080 > ./log/lean/Mistral-8X7B-instruct-v0.1/no/f_new_31.out 2>&1 &
