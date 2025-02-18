



CUDA_VISIBLE_DEVICES=2 nohup torchrun --master_port 7513 run_agent.py --test_model_name Mistral-8X7B-instruct-v0.1 --mode planning action   --start_index 101 --original_correct 9 --ip http://10.166.190.82:8080 > ./log/lean/Mistral-8X7B-instruct-v0.1/no/pa_new_101.out 2>&1 &
CUDA_VISIBLE_DEVICES=2 nohup torchrun --master_port 7514 run_agent.py --test_model_name Mistral-8X7B-instruct-v0.1 --mode planning reasoning  --start_index 0 --original_correct 0  --ip http://10.166.190.82:8080 > ./log/lean/Mistral-8X7B-instruct-v0.1/no/pr_new.out 2>&1 &



