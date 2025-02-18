CUDA_VISIBLE_DEVICES=0 nohup torchrun --master_port 7501 run_agent.py --test_model_name gpt-4-turbo-2024-04-09 --mode planning  --start_index 0 --original_correct 0 --ip http://10.118.228.191:8080 > ./log/isabelle/gpt-4-turbo-2024-04-09/no/p_new.out 2>&1 
CUDA_VISIBLE_DEVICES=0 nohup torchrun --master_port 7501 run_agent.py --test_model_name gpt-4-turbo-2024-04-09 --mode reasoning  --start_index 0 --original_correct 0 --ip http://10.118.228.191:8080 > ./log/isabelle/gpt-4-turbo-2024-04-09/no/r_new.out 2>&1 

CUDA_VISIBLE_DEVICES=1 nohup torchrun --master_port 7504 run_agent.py --test_model_name gpt-4-turbo-2024-04-09 --mode action  --start_index 0 --original_correct 0 --ip http://10.118.228.191:8080 > ./log/isabelle/gpt-4-turbo-2024-04-09/no/a_new.out 2>&1 
CUDA_VISIBLE_DEVICES=1 nohup torchrun --master_port 7504 run_agent.py --test_model_name gpt-4-turbo-2024-04-09 --mode reflection  --start_index 0 --original_correct 0 --ip http://10.118.228.191:8080 > ./log/isabelle/gpt-4-turbo-2024-04-09/no/f_new.out 2>&1 

CUDA_VISIBLE_DEVICES=2 nohup torchrun --master_port 7513 run_agent.py --test_model_name gpt-4-turbo-2024-04-09 --mode planning action   --start_index 0 --original_correct 0 --ip http://10.118.228.191:8080 > ./log/isabelle/gpt-4-turbo-2024-04-09/no/pa_new.out 2>&1 
CUDA_VISIBLE_DEVICES=2 nohup torchrun --master_port 7513 run_agent.py --test_model_name gpt-4-turbo-2024-04-09 --mode planning reasoning  --start_index 0 --original_correct 0  --ip http://10.118.228.191:8080 > ./log/isabelle/gpt-4-turbo-2024-04-09/no/pr_new.out 2>&1 

CUDA_VISIBLE_DEVICES=3 nohup torchrun --master_port 5524 run_agent.py --test_model_name gpt-4-turbo-2024-04-09 --mode planning reflection  --start_index 0 --original_correct 0 --ip http://10.118.228.191:8080 > ./log/isabelle/gpt-4-turbo-2024-04-09/no/pf_new.out 2>&1 
CUDA_VISIBLE_DEVICES=3 nohup torchrun --master_port 5524 run_agent.py --test_model_name gpt-4-turbo-2024-04-09 --mode reasoning reflection  --start_index 0 --original_correct 0 --ip http://10.118.228.191:8080 > ./log/isabelle/gpt-4-turbo-2024-04-09/no/rf_new.out 2>&1 

CUDA_VISIBLE_DEVICES=0 nohup torchrun --master_port 5734 run_agent.py --test_model_name gpt-4-turbo-2024-04-09 --mode action reflection  --start_index 0 --original_correct 0 --ip http://10.118.228.191:8080 > ./log/isabelle/gpt-4-turbo-2024-04-09/no/af_new.out 2>&1 
CUDA_VISIBLE_DEVICES=0 nohup torchrun --master_port 5734 run_agent.py --test_model_name gpt-4-turbo-2024-04-09 --mode reasoning action  --start_index 0 --original_correct 0 --ip http://10.118.228.191:8080 > ./log/isabelle/gpt-4-turbo-2024-04-09/no/ra_new.out 2>&1 

CUDA_VISIBLE_DEVICES=1 nohup torchrun --master_port 55123 run_agent.py --test_model_name gpt-4-turbo-2024-04-09 --mode planning reasoning action  --start_index 0 --original_correct 0 --ip http://10.146.183.115:8080 > ./log/isabelle/gpt-4-turbo-2024-04-09/no/pra_new.out 2>&1 
CUDA_VISIBLE_DEVICES=1 nohup torchrun --master_port 55123 run_agent.py --test_model_name gpt-4-turbo-2024-04-09 --mode planning action reflection  --start_index 0 --original_correct 0 --ip http://10.146.183.115:8080 > ./log/isabelle/gpt-4-turbo-2024-04-09/no/paf_new.out 2>&1 

CUDA_VISIBLE_DEVICES=2 nohup torchrun --master_port 52124 run_agent.py --test_model_name gpt-4-turbo-2024-04-09 --mode planning reasoning reflection  --start_index 0 --original_correct 0 --ip http://10.146.183.115:8080 > ./log/isabelle/gpt-4-turbo-2024-04-09/no/prf_new.out 2>&1 
CUDA_VISIBLE_DEVICES=2 nohup torchrun --master_port 52124 run_agent.py --test_model_name gpt-4-turbo-2024-04-09 --mode reasoning action reflection  --start_index 0 --original_correct 0 --ip http://10.146.183.115:8080 > ./log/isabelle/gpt-4-turbo-2024-04-09/no/raf_new.out 2>&1 


CUDA_VISIBLE_DEVICES=3 nohup torchrun --master_port 41234 run_agent.py --test_model_name gpt-4-turbo-2024-04-09 --mode planning reasoning action reflection  --start_index 0 --original_correct 0 --ip http://10.146.183.115:8080 > ./log/isabelle/gpt-4-turbo-2024-04-09/no/praf_new.out 2>&1 
CUDA_VISIBLE_DEVICES=3 nohup torchrun --master_port 41234 run_agent.py --test_model_name gpt-4-turbo-2024-04-09 --mode default --start_index 0 --original_correct 0 --ip http://10.118.228.191:8080 > ./log/isabelle/gpt-4-turbo-2024-04-09/no/default_new.out 2>&1 

