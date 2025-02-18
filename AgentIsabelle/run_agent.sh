# 创建日志目录
mkdir -p ./log/gpt-4o-mini/


# 测试DEFAULT结果 
CUDA_VISIBLE_DEVICES=0 nohup torchrun --master_port 5500 run_agent.py --test_model_name gpt-4o-mini --mode default --start_index 0  --original_correct 0 > ./log/isabelle/gpt-4o-mini/no/default.out 2>&1 &

CUDA_VISIBLE_DEVICES=0,1 nohup torchrun --master_port 5500 run_agent.py --test_model_name llama3_80 --mode default --default_model /home/hadoop-aipnlp/dolphinfs_hdd_hadoop-aipnlp/BERT_TRAINING_SERVICE/platform/model/Meta-Llama-3-70B-Instruct/ --default_tokenizer /home/hadoop-aipnlp/dolphinfs_hdd_hadoop-aipnlp/yangyingxuan/webshop/repo/llama3/Meta-Llama-3-8B-Instruct/tokenizer.model --start_index 0  --original_correct 0 > ./log/default3.out 2>&1 &

# 默认端口末尾1-4表示p,r,a,f
CUDA_VISIBLE_DEVICES=0 nohup torchrun --master_port 5501 run_agent.py --test_model_name gpt-4o-mini --mode planning --start_index 0  --original_correct 0 > ./log/isabelle/gpt-4o-mini/no/p.out 2>&1 &
CUDA_VISIBLE_DEVICES=2 nohup torchrun --master_port 5502 run_agent.py --test_model_name gpt-4o-mini --mode reasoning --start_index 0  --original_correct 0 > ./log/isabelle/gpt-4o-mini/no/r.out 2>&1 &
CUDA_VISIBLE_DEVICES=1 nohup torchrun --master_port 5503 run_agent.py --test_model_name gpt-4o-mini --mode action --start_index 0  --original_correct 0 > ./log/isabelle/gpt-4o-mini/no/a.out 2>&1 &
CUDA_VISIBLE_DEVICES=2 nohup torchrun --master_port 5504 run_agent.py --test_model_name gpt-4o-mini --mode reflection --start_index 0  --original_correct 0 > ./log/isabelle/gpt-4o-mini/no/f.out 2>&1 &


# 端口末尾12表示同时在p,r替换测试模型
CUDA_VISIBLE_DEVICES=0 nohup torchrun --master_port 5513 run_agent.py --test_model_name gpt-4o-mini --mode planning action --start_index 0  --original_correct 0 > ./log/isabelle/gpt-4o-mini/no/pa.out 2>&1 &
CUDA_VISIBLE_DEVICES=0 nohup torchrun --master_port 5512 run_agent.py --test_model_name gpt-4o-mini --mode planning reasoning --start_index 0  --original_correct 0 > ./log/isabelle/gpt-4o-mini/no/pr.out 2>&1 &
CUDA_VISIBLE_DEVICES=0 nohup torchrun --master_port 5514 run_agent.py --test_model_name gpt-4o-mini --mode planning reflection --start_index 0  --original_correct 0 > ./log/isabelle/gpt-4o-mini/no/pf.out 2>&1 &

CUDA_VISIBLE_DEVICES=0 nohup torchrun --master_port 5524 run_agent.py --test_model_name gpt-4o-mini --mode reasoning reflection --start_index 0  --original_correct 0 > ./log/isabelle/gpt-4o-mini/no/rf.out 2>&1 &
CUDA_VISIBLE_DEVICES=0 nohup torchrun --master_port 5534 run_agent.py --test_model_name gpt-4o-mini --mode action reflection --start_index 0  --original_correct 0 > ./log/isabelle/gpt-4o-mini/no/af.out 2>&1 &
CUDA_VISIBLE_DEVICES=0 nohup torchrun --master_port 5523 run_agent.py --test_model_name gpt-4o-mini --mode reasoning action --start_index 0  --original_correct 0 > ./log/isabelle/gpt-4o-mini/no/ra.out 2>&1 &


# 端口末尾123表示同时在p,r,a替换测试模型
CUDA_VISIBLE_DEVICES=0 nohup torchrun --master_port 55123 run_agent.py --test_model_name gpt-4o-mini --mode planning reasoning action --start_index 0  --original_correct 0 > ./log/isabelle/gpt-4o-mini/no/pra.out 2>&1 &
CUDA_VISIBLE_DEVICES=0 nohup torchrun --master_port 55134 run_agent.py --test_model_name gpt-4o-mini --mode planning action reflection --start_index 0  --original_correct 0 > ./log/isabelle/gpt-4o-mini/no/paf.out 2>&1 &
CUDA_VISIBLE_DEVICES=1 nohup torchrun --master_port 55124 run_agent.py --test_model_name gpt-4o-mini --mode planning reasoning reflection --start_index 0  --original_correct 0 > ./log/isabelle/gpt-4o-mini/no/prf.out 2>&1 &
CUDA_VISIBLE_DEVICES=1 nohup torchrun --master_port 35234 run_agent.py --test_model_name gpt-4o-mini --mode reasoning action reflection --start_index 0  --original_correct 0 > ./log/isabelle/gpt-4o-mini/no/raf.out 2>&1 &

CUDA_VISIBLE_DEVICES=1 nohup torchrun --master_port 41234 run_agent.py --test_model_name gpt-4o-mini --mode planning reasoning action reflection --start_index 0  --original_correct 0 > ./log/isabelle/gpt-4o-mini/no/praf.out 2>&1 &



