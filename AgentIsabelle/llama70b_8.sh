CUDA_VISIBLE_DEVICES=3 nohup torchrun --master_port 41234 run_agent.py --test_model_name Claude-3.5-Sonnet --mode planning reasoning action reflection  --start_index 63 --original_correct 51 --ip http://10.114.38.7:8080 > ./log/isabelle/Claude-3.5-Sonnet/no/praf_new_63.out 2>&1 
CUDA_VISIBLE_DEVICES=3 nohup torchrun --master_port 41234 run_agent.py --test_model_name Claude-3.5-Sonnet --mode default --start_index 89 --original_correct 7 --ip http://10.140.9.121:8080 > ./log/isabelle/Claude-3.5-Sonnet/no/default_new_89.out 2>&1 


CUDA_VISIBLE_DEVICES=3 nohup torchrun --master_port 41234 run_agent.py --test_model_name gpt-4-turbo-2024-04-09 --mode planning reasoning action reflection  --start_index 0 --original_correct 0 --ip http://10.146.183.115:8080 > ./log/isabelle/gpt-4-turbo-2024-04-09/no/praf_new.out 2>&1 
CUDA_VISIBLE_DEVICES=3 nohup torchrun --master_port 41234 run_agent.py --test_model_name gpt-4-turbo-2024-04-09 --mode default --start_index 0 --original_correct 0 --ip http://10.118.228.191:8080 > ./log/isabelle/gpt-4-turbo-2024-04-09/no/default_new.out 2>&1 
