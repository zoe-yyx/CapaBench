## 代数/几何文件说明
#### 关于子文件夹的说明
+ **/Bert** 存储Bert模型，在Agent调用搜索引擎时，会把关键词和提前准备好的代数/几何知识点做相似度计算，选最高的三个知识点模拟搜索引擎的效果；
+ **./dataset** 作用不是很大，只确定其中的```util.py```中的一个函数在```run_agent.py```中要用到；
+ **./llama** 用于default模型，存储Llama-3-8b相关代码；
+ **./log** 存储评测日志文件，```./geometry```存储的是在MATH中几何新题的评测日志，另外两个（```./new_algebra```和```./new_geometry```）存储的是改写新数据的评测日志; 再下一级目录是不同评测模型的日志结果，再下一级包含三个子文件夹，分别对应Agent不使用/使用单/使用多工具；例如，```./log/new_geometry/gpt-4-turbo-2024-04-09/multi/paf.out```表示在几何新数据上测试gpt-4，使用多工具，待测部分为p、a、f；
+ **./prompt** 存储prompt，分别对于无/单/多工具，其中```prompt_collection_multiTools_copy.py```是一个备份，在某次修改prompt前的版本；
+ **./user_session_logs** 类似```./log```，存储交互轨迹；


#### 关于其他文件的说明
+ **./algebra_knowledge.json和./geometry_knowledge.json** 分别存储代数和几何在使用搜索引擎时，用来做比对的定理、知识点等信息；
+ **./algebra_test ./algebra_train ./geometry_test ./geometry_train** 分别存储MATH原数据集中的数据，在评测时用不到，评测新生成数据即可；
+ **./new_algebra_total.json和./new_geometry_total.json** 需要评测的新数据；
+ **./calculator.py** 存储Agent的计算器工具；
+ **./llm_agent.py** 存储各个大模型Agent，如Llama和OpenAI系列；
+ **./math_equivalence.py** 存储判断两个表达式是否等价的函数，用于判断某道题目结果是否做对；
+ **./shapley.py** 用于计算Shapley Value；
+ **./util.py** 用于存储一些辅助函数，如提取大模型返回信息，设置随机种子，安全调用API等等；
+ **./run_agent.py** 评测主体文件，读取待评测文件（```new_algrbra_total.json或new_geometry_total.json```），然后根据模式（也就是需要替换为待测试模型的部分）进行p-r-a-f评测，把运行日志存储到```./log```相应文件中，运行结束后，把每道题的交互轨迹运行到```user_session_logs```中的相应文件；
+ **./run_agent.sh** 存储了16种模式下的运行```run_agent.py```的指令
例如，```CUDA_VISIBLE_DEVICES=0 nohup torchrun --master_port 55134 run_agent.py --test_model_name gpt-4o-mini --mode planning action reflection --category algebra --start_index 209 --original_total 209 --original_correct 153 > ./log/new_algebra/gpt-4o-mini/multi/paf_209.out 2>&1 &```   表示测试模型gpt-4o-mini，模式是paf, 待测类别为代数， 开始测试的第一个题目索引为209， 之前测试过的题目总数为209， 其中正确数量为153，新一轮测试的log文件为paf_209.out

