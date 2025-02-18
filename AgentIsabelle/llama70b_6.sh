CUDA_VISIBLE_DEVICES=1 nohup torchrun --master_port 55123 run_agent.py --test_model_name Claude-3.5-Sonnet --mode planning reasoning action  --start_index 66 --original_correct 52 --ip http://10.114.38.7:8080 > ./log/isabelle/Claude-3.5-Sonnet/no/pra_new_66.out 2>&1 
CUDA_VISIBLE_DEVICES=1 nohup torchrun --master_port 55123 run_agent.py --test_model_name Claude-3.5-Sonnet --mode planning action reflection  --start_index 4 --original_correct 4 --ip http://10.114.38.7:8080 > ./log/isabelle/Claude-3.5-Sonnet/no/paf_new_4.out 2>&1 


CUDA_VISIBLE_DEVICES=1 nohup torchrun --master_port 55123 run_agent.py --test_model_name gpt-4-turbo-2024-04-09 --mode planning action reflection  --start_index 91 --original_correct 60 --ip http://10.146.183.115:8080 > ./log/isabelle/gpt-4-turbo-2024-04-09/no/paf_new_91.out 2>&1 
