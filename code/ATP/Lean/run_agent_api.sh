CUDA_VISIBLE_DEVICES=0 nohup torchrun --master_port 7501 run_agent.py --test_model_name Mistral-8X7B-instruct-v0.1 --mode planning  --start_index 0 --original_correct 0 --ip http://10.166.190.82:8080 > ./log/lean/Mistral-8X7B-instruct-v0.1/no/p_new.out 2>&1 
CUDA_VISIBLE_DEVICES=0 nohup torchrun --master_port 7501 run_agent.py --test_model_name Mistral-8X7B-instruct-v0.1 --mode reasoning  --start_index 0 --original_correct 0 --ip http://10.166.190.82:8080 > ./log/lean/Mistral-8X7B-instruct-v0.1/no/r_new.out 2>&1 

CUDA_VISIBLE_DEVICES=1 nohup torchrun --master_port 7504 run_agent.py --test_model_name Mistral-8X7B-instruct-v0.1 --mode action  --start_index 0 --original_correct 0 --ip http://10.166.190.82:8080 > ./log/lean/Mistral-8X7B-instruct-v0.1/no/a_new.out 2>&1 
CUDA_VISIBLE_DEVICES=1 nohup torchrun --master_port 7504 run_agent.py --test_model_name Mistral-8X7B-instruct-v0.1 --mode reflection  --start_index 0 --original_correct 0 --ip http://10.166.190.82:8080 > ./log/lean/Mistral-8X7B-instruct-v0.1/no/f_new.out 2>&1 

CUDA_VISIBLE_DEVICES=2 nohup torchrun --master_port 7513 run_agent.py --test_model_name Mistral-8X7B-instruct-v0.1 --mode planning action   --start_index 0 --original_correct 0 --ip http://10.166.190.82:8080 > ./log/lean/Mistral-8X7B-instruct-v0.1/no/pa_new.out 2>&1 
CUDA_VISIBLE_DEVICES=2 nohup torchrun --master_port 7513 run_agent.py --test_model_name Mistral-8X7B-instruct-v0.1 --mode planning reasoning  --start_index 0 --original_correct 0  --ip http://10.166.190.82:8080 > ./log/lean/Mistral-8X7B-instruct-v0.1/no/pr_new.out 2>&1 

CUDA_VISIBLE_DEVICES=3 nohup torchrun --master_port 5524 run_agent.py --test_model_name Mistral-8X7B-instruct-v0.1 --mode planning reflection  --start_index 0 --original_correct 0 --ip http://10.166.190.82:8080 > ./log/lean/Mistral-8X7B-instruct-v0.1/no/pf_new.out 2>&1 
CUDA_VISIBLE_DEVICES=3 nohup torchrun --master_port 5524 run_agent.py --test_model_name Mistral-8X7B-instruct-v0.1 --mode reasoning reflection  --start_index 0 --original_correct 0 --ip http://10.166.190.82:8080 > ./log/lean/Mistral-8X7B-instruct-v0.1/no/rf_new.out 2>&1 

CUDA_VISIBLE_DEVICES=0 nohup torchrun --master_port 5734 run_agent.py --test_model_name Mistral-8X7B-instruct-v0.1 --mode action reflection  --start_index 0 --original_correct 0 --ip http://10.166.190.82:8080 > ./log/lean/Mistral-8X7B-instruct-v0.1/no/af_new.out 2>&1 
CUDA_VISIBLE_DEVICES=0 nohup torchrun --master_port 5734 run_agent.py --test_model_name Mistral-8X7B-instruct-v0.1 --mode reasoning action  --start_index 0 --original_correct 0 --ip http://10.166.190.82:8080 > ./log/lean/Mistral-8X7B-instruct-v0.1/no/ra_new.out 2>&1 

CUDA_VISIBLE_DEVICES=1 nohup torchrun --master_port 55123 run_agent.py --test_model_name Mistral-8X7B-instruct-v0.1 --mode planning reasoning action  --start_index 0 --original_correct 0 --ip http://10.166.182.41:8080 > ./log/lean/Mistral-8X7B-instruct-v0.1/no/pra_new.out 2>&1 
CUDA_VISIBLE_DEVICES=1 nohup torchrun --master_port 55123 run_agent.py --test_model_name Mistral-8X7B-instruct-v0.1 --mode planning action reflection  --start_index 0 --original_correct 0 --ip http://10.166.182.41:8080 > ./log/lean/Mistral-8X7B-instruct-v0.1/no/paf_new.out 2>&1 

CUDA_VISIBLE_DEVICES=2 nohup torchrun --master_port 52124 run_agent.py --test_model_name Mistral-8X7B-instruct-v0.1 --mode planning reasoning reflection  --start_index 0 --original_correct 0 --ip http://10.166.182.41:8080 > ./log/lean/Mistral-8X7B-instruct-v0.1/no/prf_new.out 2>&1 
CUDA_VISIBLE_DEVICES=2 nohup torchrun --master_port 52124 run_agent.py --test_model_name Mistral-8X7B-instruct-v0.1 --mode reasoning action reflection  --start_index 0 --original_correct 0 --ip http://10.166.182.41:8080 > ./log/lean/Mistral-8X7B-instruct-v0.1/no/raf_new.out 2>&1 


CUDA_VISIBLE_DEVICES=3 nohup torchrun --master_port 41234 run_agent.py --test_model_name Mistral-8X7B-instruct-v0.1 --mode planning reasoning action reflection  --start_index 0 --original_correct 0 --ip http://10.166.182.41:8080 > ./log/lean/Mistral-8X7B-instruct-v0.1/no/praf_new.out 2>&1 
CUDA_VISIBLE_DEVICES=3 nohup torchrun --master_port 41234 run_agent.py --test_model_name Mistral-8X7B-instruct-v0.1 --mode default --start_index 0 --original_correct 0 --ip http://10.166.190.82:8080 > ./log/lean/Mistral-8X7B-instruct-v0.1/no/default_new.out 2>&1 

