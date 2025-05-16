#!/bin/bash

num_begin=$1
num_end=$2
model_name=$3
api_key=$4
llama_key=$5
# 默认数组值
default_numbers=(0 1)

numbers=(${default_numbers[@]})  # 使用默认值

# 定义所有可能的 model_ls 组合

#!/bin/bash

# 定义数字集合

# 初始化一个空数组，用于存储组合
combinations=()

# 生成长度为4的全排列，并存储到数组中
for i in "${numbers[@]}"; do
  for j in "${numbers[@]}"; do
    for k in "${numbers[@]}"; do
      for l in "${numbers[@]}"; do
        if [[ $i -eq 0 && $j -eq 0 && $k -eq 0 && $l -eq 0 ]]; then
          continue
        fi
        combinations+=("$i $j $k $l")
      done
    done
  done
done

# 打印组合数组中的所有元素

convert_combo() {
    local combo=$1
    local converted=""

    local labels=("P" "R" "A" "F")
    local index=0

    for num in $combo; do
        case $num in
            0) converted+="${labels[$index]}l_" ;;
            1) converted+="${labels[$index]}${model_name}_" ;;
        esac
        index=$((index + 1))
    done

    # 去掉末尾的下划线
    converted=${converted%_}

    echo $converted
}
# 循环运行脚本并重定向输出
for (( i=num_begin; i<=num_end; i++ )); do
    output_dir="output_${model_name}/${model_name}_output_${i}"
    mkdir -p $output_dir
    for combo in "${combinations[@]}"; do
        # 运行 Python 脚本并将输出重定向到文件
        converted_combo=$(convert_combo "$combo")
        file_name="planning_${converted_combo}_seed${i}.out"
        output_file="${output_dir}/${file_name}"
        start_time=$(date +%s)

        if [[ -f "$output_file" ]]; then
            is_valid=$(python check_useful.py "$output_file")

            if [[ "$is_valid" == "True" ]]; then
                echo "Output file ${output_file} already exists and is valid. Skipping..."
                continue
            fi
        fi
        output=$(python  play_test.py --game planning --random_seed $i --partial --model_ls $combo --api_key ${api_key} --llama_key ${llama_key})
        end_time=$(date +%s)
        execution_time=$((end_time - start_time))
        execution_time_minutes=$(echo "scale=2; $execution_time / 60" | bc)
        # 生成文件名
       
        
        # 生成文件名
        file_name="planning_${converted_combo}_seed${i}.out"
    
        # 保存输出到文件
        echo "$output" > "${output_dir}/${file_name}"
        echo "Execution time: $execution_time_minutes minutes"
        
        echo "Run $i with model_ls $combo completed, output saved to ${output_dir}/${file_name}"
    done
done

echo "All runs completed."
