CUDA_VISIBLE_DEVICES=3 nohup torchrun --master_port 41234 run_agent.py --test_model_name TEST_MODEL --mode default --start_index 0 --original_correct 0 --ip http://********* > ./log/lean/TEST_MODEL/no/default.out 2>&1 


CUDA_VISIBLE_DEVICES=0 nohup torchrun --master_port 7501 run_agent.py --test_model_name TEST_MODEL --mode planning  --start_index 0 --original_correct 0 --ip http://********* > ./log/lean/TEST_MODEL/no/p.out 2>&1 
CUDA_VISIBLE_DEVICES=0 nohup torchrun --master_port 7501 run_agent.py --test_model_name TEST_MODEL --mode reasoning  --start_index 0 --original_correct 0 --ip http://********* > ./log/lean/TEST_MODEL/no/r.out 2>&1 
CUDA_VISIBLE_DEVICES=1 nohup torchrun --master_port 7504 run_agent.py --test_model_name TEST_MODEL --mode action  --start_index 0 --original_correct 0 --ip http://********* > ./log/lean/TEST_MODEL/no/a.out 2>&1 
CUDA_VISIBLE_DEVICES=1 nohup torchrun --master_port 7504 run_agent.py --test_model_name TEST_MODEL --mode reflection  --start_index 0 --original_correct 0 --ip http://********* > ./log/lean/TEST_MODEL/no/f.out 2>&1 

CUDA_VISIBLE_DEVICES=2 nohup torchrun --master_port 7513 run_agent.py --test_model_name TEST_MODEL --mode planning action   --start_index 0 --original_correct 0 --ip http://********* > ./log/lean/TEST_MODEL/no/pa.out 2>&1 
CUDA_VISIBLE_DEVICES=2 nohup torchrun --master_port 7513 run_agent.py --test_model_name TEST_MODEL --mode planning reasoning  --start_index 0 --original_correct 0  --ip http://********* > ./log/lean/TEST_MODEL/no/pr.out 2>&1 
CUDA_VISIBLE_DEVICES=3 nohup torchrun --master_port 5524 run_agent.py --test_model_name TEST_MODEL --mode planning reflection  --start_index 0 --original_correct 0 --ip http://********* > ./log/lean/TEST_MODEL/no/pf.out 2>&1 
CUDA_VISIBLE_DEVICES=3 nohup torchrun --master_port 5524 run_agent.py --test_model_name TEST_MODEL --mode reasoning reflection  --start_index 0 --original_correct 0 --ip http://********* > ./log/lean/TEST_MODEL/no/rf.out 2>&1 
CUDA_VISIBLE_DEVICES=0 nohup torchrun --master_port 5734 run_agent.py --test_model_name TEST_MODEL --mode action reflection  --start_index 0 --original_correct 0 --ip http://********* > ./log/lean/TEST_MODEL/no/af.out 2>&1 
CUDA_VISIBLE_DEVICES=0 nohup torchrun --master_port 5734 run_agent.py --test_model_name TEST_MODEL --mode reasoning action  --start_index 0 --original_correct 0 --ip http://********* > ./log/lean/TEST_MODEL/no/ra.out 2>&1 

CUDA_VISIBLE_DEVICES=1 nohup torchrun --master_port 55123 run_agent.py --test_model_name TEST_MODEL --mode planning reasoning action  --start_index 0 --original_correct 0 --ip http://********* > ./log/lean/TEST_MODEL/no/pra.out 2>&1 
CUDA_VISIBLE_DEVICES=1 nohup torchrun --master_port 55123 run_agent.py --test_model_name TEST_MODEL --mode planning action reflection  --start_index 0 --original_correct 0 --ip http://********* > ./log/lean/TEST_MODEL/no/paf.out 2>&1 
CUDA_VISIBLE_DEVICES=2 nohup torchrun --master_port 52124 run_agent.py --test_model_name TEST_MODEL --mode planning reasoning reflection  --start_index 0 --original_correct 0 --ip http://********* > ./log/lean/TEST_MODEL/no/prf.out 2>&1 
CUDA_VISIBLE_DEVICES=2 nohup torchrun --master_port 52124 run_agent.py --test_model_name TEST_MODEL --mode reasoning action reflection  --start_index 0 --original_correct 0 --ip http://********* > ./log/lean/TEST_MODEL/no/raf.out 2>&1 


CUDA_VISIBLE_DEVICES=3 nohup torchrun --master_port 41234 run_agent.py --test_model_name TEST_MODEL --mode planning reasoning action reflection  --start_index 0 --original_correct 0 --ip http://********* > ./log/lean/TEST_MODEL/no/praf.out 2>&1 

