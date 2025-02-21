CUDA_VISIBLE_DEVICES=0 nohup torchrun --master_port 8501 run_agent.py --test_model_name doubao-pro-4k --mode planning  --start_index 0 --original_correct 0  > ./log/lean/doubao-pro-4k/no/p_new.out 2>&1 &
CUDA_VISIBLE_DEVICES=0 nohup torchrun --master_port 8502 run_agent.py --test_model_name doubao-pro-4k --mode reasoning  --start_index 0 --original_correct 0  > ./log/lean/doubao-pro-4k/no/r_new.out 2>&1 &

CUDA_VISIBLE_DEVICES=1 nohup torchrun --master_port 8504 run_agent.py --test_model_name doubao-pro-4k --mode action  --start_index 0 --original_correct 0  > ./log/lean/doubao-pro-4k/no/a_new.out 2>&1 &
CUDA_VISIBLE_DEVICES=1 nohup torchrun --master_port 8508 run_agent.py --test_model_name doubao-pro-4k --mode reflection  --start_index 0 --original_correct 0  > ./log/lean/doubao-pro-4k/no/f_new.out 2>&1 &

CUDA_VISIBLE_DEVICES=1 nohup torchrun --master_port 8513 run_agent.py --test_model_name doubao-pro-4k --mode planning action   --start_index 0 --original_correct 0  > ./log/lean/doubao-pro-4k/no/pa_new.out 2>&1 &
CUDA_VISIBLE_DEVICES=0 nohup torchrun --master_port 8513 run_agent.py --test_model_name doubao-pro-4k --mode planning reasoning  --start_index 0 --original_correct 0   > ./log/lean/doubao-pro-4k/no/pr_new.out 2>&1 &

CUDA_VISIBLE_DEVICES=3 nohup torchrun --master_port 6524 run_agent.py --test_model_name doubao-pro-4k --mode planning reflection  --start_index 0 --original_correct 0  > ./log/lean/doubao-pro-4k/no/pf_new.out 2>&1 &
CUDA_VISIBLE_DEVICES=0 nohup torchrun --master_port 8513 run_agent.py --test_model_name doubao-pro-4k --mode planning reasoning  --start_index 0 --original_correct 0   > ./log/lean/doubao-pro-4k/no/pr_new.out 2>&1 &
CUDA_VISIBLE_DEVICES=0 nohup torchrun --master_port 6524 run_agent.py --test_model_name doubao-pro-4k --mode reasoning reflection  --start_index 0 --original_correct 0  > ./log/lean/doubao-pro-4k/no/rf_new.out 2>&1 &

CUDA_VISIBLE_DEVICES=1 nohup torchrun --master_port 5734 run_agent.py --test_model_name doubao-pro-4k --mode action reflection  --start_index 0 --original_correct 0  > ./log/lean/doubao-pro-4k/no/af_new.out 2>&1 &
CUDA_VISIBLE_DEVICES=1 nohup torchrun --master_port 5735 run_agent.py --test_model_name doubao-pro-4k --mode reasoning action  --start_index 0 --original_correct 0  > ./log/lean/doubao-pro-4k/no/ra_new.out 2>&1 &

CUDA_VISIBLE_DEVICES=3 nohup torchrun --master_port 55123 run_agent.py --test_model_name doubao-pro-4k --mode planning reasoning action  --start_index 0 --original_correct 0  > ./log/lean/doubao-pro-4k/no/pra_new.out 2>&1 &
CUDA_VISIBLE_DEVICES=0 nohup torchrun --master_port 55124 run_agent.py --test_model_name doubao-pro-4k --mode planning action reflection  --start_index 0 --original_correct 0  > ./log/lean/doubao-pro-4k/no/paf_new.out 2>&1 &

CUDA_VISIBLE_DEVICES=3 nohup torchrun --master_port 52124 run_agent.py --test_model_name doubao-pro-4k --mode planning reasoning reflection  --start_index 0 --original_correct 0  > ./log/lean/doubao-pro-4k/no/prf_new.out 2>&1 &
CUDA_VISIBLE_DEVICES=3 nohup torchrun --master_port 52125 run_agent.py --test_model_name doubao-pro-4k --mode reasoning action reflection  --start_index 0 --original_correct 0  > ./log/lean/doubao-pro-4k/no/raf_new.out 2>&1 &


CUDA_VISIBLE_DEVICES=2 nohup torchrun --master_port 51234 run_agent.py --test_model_name doubao-pro-4k --mode planning reasoning action reflection  --start_index 0 --original_correct 0  > ./log/lean/doubao-pro-4k/no/praf_new.out 2>&1 &
CUDA_VISIBLE_DEVICES=3 nohup torchrun --master_port 41234 run_agent.py --test_model_name doubao-pro-4k --mode default --start_index 0 --original_correct 0  > ./log/lean/doubao-pro-4k/no/default_new.out 2>&1 &

