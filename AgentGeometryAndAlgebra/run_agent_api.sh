
CUDA_VISIBLE_DEVICES=1 nohup torchrun --master_port 9911 run_agent_api_default.py --test_model_name Mistral-8X7B-instruct-v0.1 --mode reasoning --category geometry --start_index 147 --original_correct 19 --ip http://10.166.180.109:8080 > ./log/new_geometry/Mistral-8X7B-instruct-v0.1/multi/r_new_147.out 2>&1 &
CUDA_VISIBLE_DEVICES=1 nohup torchrun --master_port 9912 run_agent_api_default.py --test_model_name Mistral-8X7B-instruct-v0.1 --mode action --category geometry --start_index 160 --original_correct 48 --ip http://10.166.180.109:8080 > ./log/new_geometry/Mistral-8X7B-instruct-v0.1/multi/a_new_160.out 2>&1 &

CUDA_VISIBLE_DEVICES=1 nohup torchrun --master_port 9914 run_agent_api_default.py --test_model_name Mistral-8X7B-instruct-v0.1 --mode planning action  --category geometry --start_index 65 --original_correct 22 --ip http://10.166.180.109:8080 > ./log/new_geometry/Mistral-8X7B-instruct-v0.1/multi/pa_new_65.out 2>&1 &


CUDA_VISIBLE_DEVICES=1 nohup torchrun --master_port 9915 run_agent_api_default.py --test_model_name Mistral-8X7B-instruct-v0.1 --mode planning reasoning --category geometry --start_index 55 --original_correct 8 --ip http://10.166.180.109:8080 > ./log/new_geometry/Mistral-8X7B-instruct-v0.1/multi/pr_new_55.out 2>&1 &
CUDA_VISIBLE_DEVICES=1 nohup torchrun --master_port 9916 run_agent_api_default.py --test_model_name Mistral-8X7B-instruct-v0.1 --mode planning reflection --category geometry --start_index 41 --original_correct 5 --ip http://10.166.180.109:8080 > ./log/new_geometry/Mistral-8X7B-instruct-v0.1/multi/pf_new_41.out 2>&1 &
CUDA_VISIBLE_DEVICES=1 nohup torchrun --master_port 9917 run_agent_api_default.py --test_model_name Mistral-8X7B-instruct-v0.1 --mode reasoning reflection --category geometry --start_index 37 --original_correct 3 --ip http://10.166.180.109:8080 > ./log/new_geometry/Mistral-8X7B-instruct-v0.1/multi/rf_new_37.out 2>&1 &
CUDA_VISIBLE_DEVICES=1 nohup torchrun --master_port 9918 run_agent_api_default.py --test_model_name Mistral-8X7B-instruct-v0.1 --mode action reflection --category geometry --start_index 45 --original_correct 20 --ip http://10.166.180.109:8080 > ./log/new_geometry/Mistral-8X7B-instruct-v0.1/multi/af_new_45.out 2>&1 &
CUDA_VISIBLE_DEVICES=1 nohup torchrun --master_port 9919 run_agent_api_default.py --test_model_name Mistral-8X7B-instruct-v0.1 --mode reasoning action --category geometry --start_index 43 --original_correct 19 --ip http://10.166.180.109:8080 > ./log/new_geometry/Mistral-8X7B-instruct-v0.1/multi/ra_new_43.out 2>&1 &


CUDA_VISIBLE_DEVICES=1 nohup torchrun --master_port 9920 run_agent_api_default.py --test_model_name Mistral-8X7B-instruct-v0.1 --mode planning reasoning action --category geometry --start_index 106 --original_correct 41 --ip http://10.166.131.59:8080 > ./log/new_geometry/Mistral-8X7B-instruct-v0.1/multi/pra_new_106.out 2>&1 &
CUDA_VISIBLE_DEVICES=1 nohup torchrun --master_port 9921 run_agent_api_default.py --test_model_name Mistral-8X7B-instruct-v0.1 --mode planning action reflection --category geometry --start_index 133 --original_correct 39 --ip http://10.166.131.59:8080 > ./log/new_geometry/Mistral-8X7B-instruct-v0.1/multi/paf_new_133.out 2>&1 &
CUDA_VISIBLE_DEVICES=1 nohup torchrun --master_port 9922 run_agent_api_default.py --test_model_name Mistral-8X7B-instruct-v0.1 --mode planning reasoning reflection --category geometry --start_index 129 --original_correct 19 --ip http://10.166.131.59:8080 > ./log/new_geometry/Mistral-8X7B-instruct-v0.1/multi/prf_new_129.out 2>&1 & 
CUDA_VISIBLE_DEVICES=1 nohup torchrun --master_port 9923 run_agent_api_default.py --test_model_name Mistral-8X7B-instruct-v0.1 --mode reasoning action reflection --category geometry --start_index 103 --original_correct 34 --ip http://10.166.131.59:8080 > ./log/new_geometry/Mistral-8X7B-instruct-v0.1/multi/raf_new_103.out 2>&1 &
CUDA_VISIBLE_DEVICES=1 nohup torchrun --master_port 9924 run_agent_api_default.py --test_model_name Mistral-8X7B-instruct-v0.1 --mode planning reasoning action reflection --category geometry --start_index 55 --original_correct 24 --ip http://10.166.131.59:8080 > ./log/new_geometry/Mistral-8X7B-instruct-v0.1/multi/praf_new_55.out 2>&1 &




