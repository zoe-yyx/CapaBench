CUDA_VISIBLE_DEVICES=2 nohup torchrun --master_port 7513 run_agent.py --test_model_name Claude-3.5-Sonnet --mode planning action   --start_index 70 --original_correct 53 --ip http://10.140.9.121:8080 > ./log/isabelle/Claude-3.5-Sonnet/no/pa_new_70.out 2>&1 


CUDA_VISIBLE_DEVICES=2 nohup torchrun --master_port 7513 run_agent.py --test_model_name gpt-4-turbo-2024-04-09 --mode planning action   --start_index 3 --original_correct 3 --ip http://10.118.228.191:8080 > ./log/isabelle/gpt-4-turbo-2024-04-09/no/pa_new_3.out 2>&1 
CUDA_VISIBLE_DEVICES=2 nohup torchrun --master_port 7513 run_agent.py --test_model_name gpt-4-turbo-2024-04-09 --mode planning reasoning  --start_index 0 --original_correct 0  --ip http://10.118.228.191:8080 > ./log/isabelle/gpt-4-turbo-2024-04-09/no/pr_new.out 2>&1 
