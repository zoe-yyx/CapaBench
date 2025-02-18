CUDA_VISIBLE_DEVICES=0 nohup torchrun --master_port 5734 run_agent.py --test_model_name Claude-3.5-Sonnet --mode action reflection  --start_index 61 --original_correct 51 --ip http://10.140.9.121:8080 > ./log/isabelle/Claude-3.5-Sonnet/no/af_new_61.out 2>&1 


CUDA_VISIBLE_DEVICES=0 nohup torchrun --master_port 5734 run_agent.py --test_model_name gpt-4-turbo-2024-04-09 --mode action reflection  --start_index 73 --original_correct 51 --ip http://10.118.228.191:8080 > ./log/isabelle/gpt-4-turbo-2024-04-09/no/af_new_73.out 2>&1 
CUDA_VISIBLE_DEVICES=0 nohup torchrun --master_port 5734 run_agent.py --test_model_name gpt-4-turbo-2024-04-09 --mode reasoning action  --start_index 0 --original_correct 0 --ip http://10.118.228.191:8080 > ./log/isabelle/gpt-4-turbo-2024-04-09/no/ra_new.out 2>&1 
