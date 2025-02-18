# 创建日志目录
mkdir -p ./log/coq/gpt-4-turbo-2024-04-09/no


# 测试DEFAULT结果 
CUDA_VISIBLE_DEVICES=0 nohup torchrun --master_port 5500 run_agent.py --test_model_name gpt-4-turbo-2024-04-09 --mode default > ./log/coq/no/default.out 2>&1 &

CUDA_VISIBLE_DEVICES=0,1 nohup torchrun --master_port 5500 run_agent.py --test_model_name llama3_80 --mode default --default_model /home/hadoop-aipnlp/dolphinfs_hdd_hadoop-aipnlp/BERT_TRAINING_SERVICE/platform/model/Meta-Llama-3-70B-Instruct/ --default_tokenizer /home/hadoop-aipnlp/dolphinfs_hdd_hadoop-aipnlp/yangyingxuan/webshop/repo/llama3/Meta-Llama-3-8B-Instruct/tokenizer.model > ./log/default3.out 2>&1 &

# 默认端口末尾1-4表示p,r,a,f
CUDA_VISIBLE_DEVICES=0 nohup torchrun --master_port 5501 run_agent.py --test_model_name gpt-4-turbo-2024-04-09 --mode planning > ./log/coq/no/p.out 2>&1 &
CUDA_VISIBLE_DEVICES=0 nohup torchrun --master_port 5502 run_agent.py --test_model_name gpt-4-turbo-2024-04-09 --mode reasoning > ./log/coq/no/r.out 2>&1 &
CUDA_VISIBLE_DEVICES=1 nohup torchrun --master_port 5503 run_agent.py --test_model_name gpt-4-turbo-2024-04-09 --mode action > ./log/coq/no/a.out 2>&1 &
CUDA_VISIBLE_DEVICES=1 nohup torchrun --master_port 5504 run_agent.py --test_model_name gpt-4-turbo-2024-04-09 --mode reflection > ./log/coq/no/f.out 2>&1 &


# 端口末尾12表示同时在p,r替换测试模型
CUDA_VISIBLE_DEVICES=2 nohup torchrun --master_port 5513 run_agent.py --test_model_name gpt-4-turbo-2024-04-09 --mode planning action > ./log/coq/no/pa.out 2>&1 &
CUDA_VISIBLE_DEVICES=2 nohup torchrun --master_port 5512 run_agent.py --test_model_name gpt-4-turbo-2024-04-09 --mode planning reasoning > ./log/coq/no/pr.out 2>&1 &
CUDA_VISIBLE_DEVICES=2 nohup torchrun --master_port 5514 run_agent.py --test_model_name gpt-4-turbo-2024-04-09 --mode planning reflection > ./log/coq/no/pf.out 2>&1 &

CUDA_VISIBLE_DEVICES=1 nohup torchrun --master_port 5524 run_agent.py --test_model_name gpt-4-turbo-2024-04-09 --mode reasoning reflection > ./log/coq/no/rf.out 2>&1 &
CUDA_VISIBLE_DEVICES=1 nohup torchrun --master_port 5534 run_agent.py --test_model_name gpt-4-turbo-2024-04-09 --mode action reflection > ./log/coq/no/af.out 2>&1 &
CUDA_VISIBLE_DEVICES=1 nohup torchrun --master_port 5523 run_agent.py --test_model_name gpt-4-turbo-2024-04-09 --mode reasoning action > ./log/coq/no/ra.out 2>&1 &


# 端口末尾123表示同时在p,r,a替换测试模型
CUDA_VISIBLE_DEVICES=0 nohup torchrun --master_port 55123 run_agent.py --test_model_name gpt-4-turbo-2024-04-09 --mode planning reasoning action > ./log/coq/no/pra.out 2>&1 &
CUDA_VISIBLE_DEVICES=3 nohup torchrun --master_port 55134 run_agent.py --test_model_name gpt-4-turbo-2024-04-09 --mode planning action reflection > ./log/coq/no/paf.out 2>&1 &
CUDA_VISIBLE_DEVICES=3 nohup torchrun --master_port 55124 run_agent.py --test_model_name gpt-4-turbo-2024-04-09 --mode planning reasoning reflection > ./log/coq/no/prf.out 2>&1 &
CUDA_VISIBLE_DEVICES=3 nohup torchrun --master_port 35234 run_agent.py --test_model_name gpt-4-turbo-2024-04-09 --mode reasoning action reflection > ./log/coq/no/raf.out 2>&1 &

CUDA_VISIBLE_DEVICES=1 nohup torchrun --master_port 41234 run_agent.py --test_model_name gpt-4-turbo-2024-04-09 --mode planning reasoning action reflection > ./log/coq/no/praf.out 2>&1 &



