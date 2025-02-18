CUDA_VISIBLE_DEVICES=3 nohup torchrun --master_port 1924 run_agent.py --test_model_name Mistral-8X7B-instruct-v0.1 --mode planning reasoning action reflection  --start_index 100 --original_correct 29 --ip http://10.166.180.109:8080 > ./log/coq/Mistral-8X7B-instruct-v0.1/no/praf_new_100.out 2>&1 

