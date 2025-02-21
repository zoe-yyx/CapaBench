

# 测试DEFAULT结果 
CUDA_VISIBLE_DEVICES=0 nohup torchrun --master_port 7500 run_agent.py --test_model_name TEST_MODEL --mode default  --start_index 0 --original_correct 0 --ip http://******** > ./log/coq/TEST_MODEL/no/default.out 2>&1 &


# 默认端口末尾1-4表示p,r,a,f
CUDA_VISIBLE_DEVICES=0 nohup torchrun --master_port 7501 run_agent.py --test_model_name TEST_MODEL --mode planning  --start_index 0 --original_correct 0 --ip http://******** > ./log/coq/TEST_MODEL/no/p.out 2>&1 &
CUDA_VISIBLE_DEVICES=0 nohup torchrun --master_port 7502 run_agent.py --test_model_name TEST_MODEL --mode reasoning  --start_index 0 --original_correct 0 --ip http://******** > ./log/coq/TEST_MODEL/no/r.out 2>&1 &
CUDA_VISIBLE_DEVICES=0 nohup torchrun --master_port 7503 run_agent.py --test_model_name TEST_MODEL --mode action  --start_index 0 --original_correct 0 --ip http://******** > ./log/coq/TEST_MODEL/no/a.out 2>&1 &
CUDA_VISIBLE_DEVICES=0 nohup torchrun --master_port 7504 run_agent.py --test_model_name TEST_MODEL --mode reflection  --start_index 0 --original_correct 0 --ip http://******** > ./log/coq/TEST_MODEL/no/f.out 2>&1 &


# 端口末尾12表示同时在p,r替换测试模型
CUDA_VISIBLE_DEVICES=0 nohup torchrun --master_port 7513 run_agent.py --test_model_name TEST_MODEL --mode planning action   --start_index 0 --original_correct 0 --ip http://******** > ./log/coq/TEST_MODEL/no/pa.out 2>&1 &
CUDA_VISIBLE_DEVICES=0 nohup torchrun --master_port 7512 run_agent.py --test_model_name TEST_MODEL --mode planning reasoning  --start_index 0 --original_correct 0 --ip http://******** > ./log/coq/TEST_MODEL/no/pr.out 2>&1 &
CUDA_VISIBLE_DEVICES=0 nohup torchrun --master_port 7514 run_agent.py --test_model_name TEST_MODEL --mode planning reflection  --start_index 0 --original_correct 0 --ip http://******** > ./log/coq/TEST_MODEL/no/pf.out 2>&1 &
CUDA_VISIBLE_DEVICES=0 nohup torchrun --master_port 5524 run_agent.py --test_model_name TEST_MODEL --mode reasoning reflection  --start_index 0 --original_correct 0 --ip http://******** > ./log/coq/TEST_MODEL/no/rf.out 2>&1 &
CUDA_VISIBLE_DEVICES=0 nohup torchrun --master_port 5534 run_agent.py --test_model_name TEST_MODEL --mode action reflection  --start_index 0 --original_correct 0 --ip http://******** > ./log/coq/TEST_MODEL/no/af.out 2>&1 &
CUDA_VISIBLE_DEVICES=0 nohup torchrun --master_port 5523 run_agent.py --test_model_name TEST_MODEL --mode reasoning action  --start_index 0 --original_correct 0 --ip http://******** > ./log/coq/TEST_MODEL/no/ra.out 2>&1 &


# 端口末尾123表示同时在p,r,a替换测试模型
CUDA_VISIBLE_DEVICES=0 nohup torchrun --master_port 55123 run_agent.py --test_model_name TEST_MODEL --mode planning reasoning action  --start_index 0 --original_correct 0 --ip http://******** > ./log/coq/TEST_MODEL/no/pra.out 2>&1 &
CUDA_VISIBLE_DEVICES=0 nohup torchrun --master_port 55134 run_agent.py --test_model_name TEST_MODEL --mode planning action reflection  --start_index 0 --original_correct 0 --ip http://******** > ./log/coq/TEST_MODEL/no/paf.out 2>&1 &
CUDA_VISIBLE_DEVICES=0 nohup torchrun --master_port 55124 run_agent.py --test_model_name TEST_MODEL --mode planning reasoning reflection  --start_index 0 --original_correct 0 --ip http://******** > ./log/coq/TEST_MODEL/no/prf.out 2>&1 &
CUDA_VISIBLE_DEVICES=0 nohup torchrun --master_port 55234 run_agent.py --test_model_name TEST_MODEL --mode reasoning action reflection  --start_index 0 --original_correct 0 --ip http://******** > ./log/coq/TEST_MODEL/no/raf.out 2>&1 &


CUDA_VISIBLE_DEVICES=0 nohup torchrun --master_port 41234 run_agent.py --test_model_name TEST_MODEL --mode planning reasoning action reflection  --start_index 0 --original_correct 0 --ip http://******** > ./log/coq/TEST_MODEL/no/praf.out 2>&1 &


