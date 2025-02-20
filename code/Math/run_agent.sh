CUDA_VISIBLE_DEVICES=0 nohup torchrun --master_port 7709 run_agent.py --test_model_name TEST_MODEL --mode default --category algebra --start_index 0 --original_correct 0 --ip http://********* > ./log/new_algebra/TEST_MODEL/multi/default.out 2>&1 &

CUDA_VISIBLE_DEVICES=0 nohup torchrun --master_port 7710 run_agent.py --test_model_name TEST_MODEL --mode planning --category algebra --start_index 0 --original_correct 0 --ip http://********* > ./log/new_algebra/TEST_MODEL/multi/p.out 2>&1 &
CUDA_VISIBLE_DEVICES=0 nohup torchrun --master_port 7711 run_agent.py --test_model_name TEST_MODEL --mode reasoning --category algebra --start_index 0 --original_correct 0 --ip http://********* > ./log/new_algebra/TEST_MODEL/multi/r.out 2>&1 &
CUDA_VISIBLE_DEVICES=0 nohup torchrun --master_port 7712 run_agent.py --test_model_name TEST_MODEL --mode action --category algebra --start_index 0 --original_correct 0 --ip http://********* > ./log/new_algebra/TEST_MODEL/multi/a.out 2>&1 &
CUDA_VISIBLE_DEVICES=0 nohup torchrun --master_port 7713 run_agent.py --test_model_name TEST_MODEL --mode reflection --category algebra --start_index 0 --original_correct 0 --ip http://********* > ./log/new_algebra/TEST_MODEL/multi/f.out 2>&1 & 

CUDA_VISIBLE_DEVICES=0 nohup torchrun --master_port 7714 run_agent.py --test_model_name TEST_MODEL --mode planning action  --category algebra --start_index 0 --original_correct 0 --ip http://********* > ./log/new_algebra/TEST_MODEL/multi/pa.out 2>&1 &
CUDA_VISIBLE_DEVICES=0 nohup torchrun --master_port 7715 run_agent.py --test_model_name TEST_MODEL --mode planning reasoning --category algebra --start_index 0 --original_correct 0 --ip http://********* > ./log/new_algebra/TEST_MODEL/multi/pr.out 2>&1 &
CUDA_VISIBLE_DEVICES=0 nohup torchrun --master_port 7716 run_agent.py --test_model_name TEST_MODEL --mode planning reflection --category algebra --start_index 0 --original_correct 0 --ip http://********* > ./log/new_algebra/TEST_MODEL/multi/pf.out 2>&1 &
CUDA_VISIBLE_DEVICES=0 nohup torchrun --master_port 7717 run_agent.py --test_model_name TEST_MODEL --mode reasoning reflection --category algebra --start_index 0 --original_correct 0 --ip http://********* > ./log/new_algebra/TEST_MODEL/multi/rf.out 2>&1 &
CUDA_VISIBLE_DEVICES=0 nohup torchrun --master_port 7718 run_agent.py --test_model_name TEST_MODEL --mode action reflection --category algebra --start_index 0 --original_correct 0 --ip http://********* > ./log/new_algebra/TEST_MODEL/multi/af.out 2>&1 &
CUDA_VISIBLE_DEVICES=0 nohup torchrun --master_port 7719 run_agent.py --test_model_name TEST_MODEL --mode reasoning action --category algebra --start_index 0 --original_correct 0 --ip http://********* > ./log/new_algebra/TEST_MODEL/multi/ra.out 2>&1 &


CUDA_VISIBLE_DEVICES=0 nohup torchrun --master_port 7720 run_agent.py --test_model_name TEST_MODEL --mode planning reasoning action --category algebra --start_index 0 --original_correct 0 --ip http://********* > ./log/new_algebra/TEST_MODEL/multi/pra.out 2>&1 &
CUDA_VISIBLE_DEVICES=0 nohup torchrun --master_port 7721 run_agent.py --test_model_name TEST_MODEL --mode planning action reflection --category algebra --start_index 0 --original_correct 0 --ip http://********* > ./log/new_algebra/TEST_MODEL/multi/paf.out 2>&1 &
CUDA_VISIBLE_DEVICES=0 nohup torchrun --master_port 7722 run_agent.py --test_model_name TEST_MODEL --mode planning reasoning reflection --category algebra --start_index 0 --original_correct 0 --ip http://********* > ./log/new_algebra/TEST_MODEL/multi/prf.out 2>&1 & 
CUDA_VISIBLE_DEVICES=0 nohup torchrun --master_port 7723 run_agent.py --test_model_name TEST_MODEL --mode reasoning action reflection --category algebra --start_index 0 --original_correct 0 --ip http://********* > ./log/new_algebra/TEST_MODEL/multi/raf.out 2>&1 &

CUDA_VISIBLE_DEVICES=0 nohup torchrun --master_port 7724 run_agent.py --test_model_name TEST_MODEL --mode planning reasoning action reflection --category algebra --start_index 0 --original_correct 0 --ip http://********* > ./log/new_algebra/TEST_MODEL/multi/praf.out 2>&1 &
