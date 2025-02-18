
# 创建日志目录
mkdir -p ./log/coq/gpt-4-turbo-2024-04-09/no


# 测试DEFAULT结果 
CUDA_VISIBLE_DEVICES=1 nohup torchrun --master_port 7500 run_agent.py --test_model_name claude_3.5_sonnet --mode default  --start_index 0 --original_correct 0 --ip http://10.140.187.72:8080 > ./log/coq/claude_3.5_sonnet/no/default_new.out 2>&1 &

CUDA_VISIBLE_DEVICES=0,1 nohup torchrun --master_port 5500 run_agent.py --test_model_name llama3_80 --mode default --default_model /home/hadoop-aipnlp/dolphinfs_hdd_hadoop-aipnlp/BERT_TRAINING_SERVICE/platform/model/Meta-Llama-3-70B-Instruct/ --default_tokenizer /home/hadoop-aipnlp/dolphinfs_hdd_hadoop-aipnlp/yangyingxuan/webshop/repo/llama3/Meta-Llama-3-8B-Instruct/tokenizer.model  --start_index 0 --original_correct 0 --ip http://10.140.187.72:8080 > ./log/default3_0.out 2>&1 &

# 默认端口末尾1-4表示p,r,a,f
CUDA_VISIBLE_DEVICES=0 nohup torchrun --master_port 7501 run_agent.py --test_model_name claude_3.5_sonnet --mode planning  --start_index 0 --original_correct 0 --ip http://10.140.187.72:8080 > ./log/coq/claude_3.5_sonnet/no/p_0.out 2>&1 &
CUDA_VISIBLE_DEVICES=1 nohup torchrun --master_port 7502 run_agent.py --test_model_name claude_3.5_sonnet --mode reasoning  --start_index 0 --original_correct 0 --ip http://10.140.187.72:8080 > ./log/coq/claude_3.5_sonnet/no/r_0.out 2>&1 &
CUDA_VISIBLE_DEVICES=1 nohup torchrun --master_port 7503 run_agent.py --test_model_name claude_3.5_sonnet --mode action  --start_index 0 --original_correct 0 --ip http://10.140.187.72:8080 > ./log/coq/claude_3.5_sonnet/no/a_0.out 2>&1 &
CUDA_VISIBLE_DEVICES=2 nohup torchrun --master_port 7504 run_agent.py --test_model_name claude_3.5_sonnet --mode reflection  --start_index 0 --original_correct 0 --ip http://10.140.187.72:8080 > ./log/coq/claude_3.5_sonnet/no/f_0.out 2>&1 &


# 端口末尾12表示同时在p,r替换测试模型
CUDA_VISIBLE_DEVICES=2 nohup torchrun --master_port 7513 run_agent.py --test_model_name claude_3.5_sonnet --mode planning action   --start_index 0 --original_correct 0 --ip http://10.140.187.72:8080 > ./log/coq/claude_3.5_sonnet/no/pa_0.out 2>&1 &
CUDA_VISIBLE_DEVICES=3 nohup torchrun --master_port 7512 run_agent.py --test_model_name claude_3.5_sonnet --mode planning reasoning  --start_index 0 --original_correct 0 --ip http://10.140.187.72:8080 > ./log/coq/claude_3.5_sonnet/no/pr_0.out 2>&1 &
CUDA_VISIBLE_DEVICES=3 nohup torchrun --master_port 7514 run_agent.py --test_model_name claude_3.5_sonnet --mode planning reflection  --start_index 0 --original_correct 0 --ip http://10.140.187.72:8080 > ./log/coq/claude_3.5_sonnet/no/pf_0.out 2>&1 &

CUDA_VISIBLE_DEVICES=0 nohup torchrun --master_port 5524 run_agent.py --test_model_name claude_3.5_sonnet --mode reasoning reflection  --start_index 0 --original_correct 0 --ip http://10.140.187.72:8080 > ./log/coq/claude_3.5_sonnet/no/rf_0.out 2>&1 &
CUDA_VISIBLE_DEVICES=0 nohup torchrun --master_port 5534 run_agent.py --test_model_name claude_3.5_sonnet --mode action reflection  --start_index 0 --original_correct 0 --ip http://10.140.187.72:8080 > ./log/coq/claude_3.5_sonnet/no/af_0.out 2>&1 &
CUDA_VISIBLE_DEVICES=1 nohup torchrun --master_port 5523 run_agent.py --test_model_name claude_3.5_sonnet --mode reasoning action  --start_index 0 --original_correct 0 --ip http://10.140.187.72:8080 > ./log/coq/claude_3.5_sonnet/no/ra_0.out 2>&1 &

# CUDA_VISIBLE_DEVICES=2 nohup torchrun --master_port 12224 run_agent.py --test_model_name claude_3.5_sonnet --mode reasoning reflection  --start_index 0 --original_correct 0 --ip http://10.140.222.31:8080 > ./log/coq/claude_3.5_sonnet/no/rf_new.out 2>&1 &


# 端口末尾123表示同时在p,r,a替换测试模型
CUDA_VISIBLE_DEVICES=1 nohup torchrun --master_port 55123 run_agent.py --test_model_name claude_3.5_sonnet --mode planning reasoning action  --start_index 0 --original_correct 0 --ip http://10.140.187.72:8080 > ./log/coq/claude_3.5_sonnet/no/pra_0.out 2>&1 &
CUDA_VISIBLE_DEVICES=2 nohup torchrun --master_port 55134 run_agent.py --test_model_name claude_3.5_sonnet --mode planning action reflection  --start_index 0 --original_correct 0 --ip http://10.140.187.72:8080 > ./log/coq/claude_3.5_sonnet/no/paf_0.out 2>&1 &
CUDA_VISIBLE_DEVICES=2 nohup torchrun --master_port 55124 run_agent.py --test_model_name claude_3.5_sonnet --mode planning reasoning reflection  --start_index 0 --original_correct 0 --ip http://10.140.187.72:8080 > ./log/coq/claude_3.5_sonnet/no/prf_0.out 2>&1 &
CUDA_VISIBLE_DEVICES=3 nohup torchrun --master_port 55234 run_agent.py --test_model_name claude_3.5_sonnet --mode reasoning action reflection  --start_index 0 --original_correct 0 --ip http://10.140.187.72:8080 > ./log/coq/claude_3.5_sonnet/no/raf_0.out 2>&1 &

CUDA_VISIBLE_DEVICES=3 nohup torchrun --master_port 15234 run_agent.py --test_model_name claude_3.5_sonnet --mode reasoning action reflection  --start_index 0 --original_correct 0 --ip http://10.140.222.31:8080 > ./log/coq/claude_3.5_sonnet/no/raf_new.out 2>&1 &


CUDA_VISIBLE_DEVICES=3 nohup torchrun --master_port 41234 run_agent.py --test_model_name claude_3.5_sonnet --mode planning reasoning action reflection  --start_index 0 --original_correct 0 --ip http://10.140.187.72:8080 > ./log/coq/claude_3.5_sonnet/no/praf_0.out 2>&1 &



CUDA_VISIBLE_DEVICES=3 nohup torchrun --master_port 5524 run_agent.py --test_model_name gpt-4-turbo-2024-04-09 --mode planning reasoning action reflection  --start_index 0 --original_correct 0 --ip http://10.166.171.102_gpt4:8080 > ./log/coq/gpt-4-turbo-2024-04-09/no/praf_new.out 2>&1 