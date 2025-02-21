
## Algebra/Geometry File Description

#### Subfolder Descriptions
+ **/Bert** stores the Bert model. When the Agent calls the search engine, it calculates the similarity between the query keywords and pre-prepared algebra/geometry knowledge points, selects the top three highest, and simulates the search engine effect (requires manual deployment).
+ **./dataset** is of minimal importance. It just ensures that a function in `util.py` is used in `run_agent.py`.
+ **./llama** is used for the default model, storing code related to Llama-3-8b.
+ **./log** stores evaluation log files (please create them yourself). The `./geometry` folder stores evaluation logs for new geometry questions in MATH, while the other two (`./new_algebra` and `./new_geometry`) store logs for evaluations of newly modified data. The next level of directories corresponds to the log results of different evaluation models, with three subfolders under each: corresponding to the cases when the Agent does not use any tools, uses a single tool, or uses multiple tools. For example, `./log/new_geometry/gpt-4-turbo-2024-04-09/multi/paf.out` indicates that the geometry new data was tested with GPT-4, using multiple tools, and the task being tested was p, a, f.
+ **./prompt** stores prompts, organized for no tools, single tool, and multiple tools. The `prompt_collection_multiTools_copy.py` is a backup of the prompt version before modifications.
+ **./user_session_logs** is similar to `./log`, storing interactive session logs (automatically created after code execution).

#### Other Files Description
+ **./algebra_knowledge.json and ./geometry_knowledge.json** store the algebra and geometry knowledge points (theorems, etc.) used for comparison when searching with the engine.
+ **./new_algebra_total.json and ./new_geometry_total.json** contain new data for evaluation.
+ **./calculator.py** stores the Agent's calculator tool.
+ **./llm_agent.py** contains various large model Agents, such as Llama and OpenAI models.
+ **./math_equivalence.py** stores functions used to determine if two expressions are equivalent, to verify if a problem has been solved correctly.
+ **./shapley_algebra/geometry.py** calculates the Shapley Value.
+ **./util.py** stores utility functions, such as extracting information from large model responses, setting random seeds, safely calling APIs, and more.
+ **./run_agent.py** is the main evaluation script. It reads evaluation files (`new_algebra_total.json` or `new_geometry_total.json`), and based on the mode (which needs to be replaced with the part for the model to be tested), it performs p-r-a-f evaluation. The log files are stored in the corresponding folder under `./log`. After the evaluation, the interactive logs for each problem are stored in the `user_session_logs` folder.
+ **./run_agent.sh** stores commands for running `run_agent.py` in 16 different modes. For example, `CUDA_VISIBLE_DEVICES=0 nohup torchrun --master_port 55134 run_agent.py --test_model_name gpt-4o-mini --mode planning action reflection --category algebra --start_index 209 --original_correct 153 --ip http://********* > ./log/new_algebra/gpt-4o-mini/multi/paf_209.out 2>&1 &` means testing the `gpt-4o-mini` model in the `paf` mode, with the category set to algebra. The test starts from the 209th problem, where the previous total number of tests was 209, with 153 correct. The log file for the new round of testing will be `paf_209.out`. Our evaluation uses Docker to deploy the large models, so the IP information is required. Please modify the `APIAgent` class in `llm_agent.py` to configure the large model deployment when performing the evaluation.

