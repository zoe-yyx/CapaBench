## Lean文件说明
#### 关于子文件夹的说明
+ **./llama** 用于default模型，存储Llama-3-8b相关代码；
+ **./log** 存储评测日志文件(请自行创建)；
+ **./prompt** 存储prompt；
+ **./user_session_logs** 类似```./log```，存储交互轨迹(代码运行后自动创建)；


#### 关于其他文件的说明
+ **./add_trace_state.py** 为lean文件增加trace state命令，跟踪证明状态；
+ **./check_qed.py** 存储负责判断形式化证明是否正确完成的函数；
+ **./lean_data_with_trajectory.json** 存储评测数据与轨迹；
+ **./lean_data.json** 需要评测的数据；
+ **./llm_agent.py** 存储各个大模型Agent，如Llama和OpenAI系列；
+ **./shapley_lean.py** 用于计算Shapley Value；
+ **./sim_lean.py** 用于执行lean代码并返回输出信息；
+ **./util.py** 用于存储一些辅助函数，如提取大模型返回信息，设置随机种子，安全调用API等等；
+ **./run_agent.py** 评测主体文件，读取待评测文件，然后根据模式（也就是需要替换为待测试模型的部分）进行p-r-a-f评测，把运行日志存储到```./log```相应文件中，运行结束后，把每道题的交互轨迹运行到```user_session_logs```中的相应文件；
+ **./run_agent.sh** 存储了16种模式下的运行```run_agent.py```的指令
例如，```CUDA_VISIBLE_DEVICES=0 nohup torchrun --master_port 55134 run_agent.py --test_model_name gpt-4o-mini --mode planning action reflection --start_index 77 --original_correct 53 --ip http://********* > ./log/lean/gpt-4o-mini/no/paf_77.out 2>&1 &```   表示测试模型gpt-4o-mini，模式是paf， 开始测试的第一个题目索引为77， 之前测试过的题目总数为77， 其中正确数量为53，新一轮测试的log文件为paf_77.out；我们的评测利用docker部署大模型，所以要用到ip信息，请您在评测时自行在```llm_agent.py```里修改APIAgent类以进行大模型部署。

