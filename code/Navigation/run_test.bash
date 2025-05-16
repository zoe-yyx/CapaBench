#!/bin/bash
#!/bin/bash

# 定义其他固定参数
MODEL="doubao"
IP1="10.118.30.11"
IP2="10.166.144.9"

# 起始和结束值
START=0
END=125
STEP=15

# 循环从START到END，以STEP为步长
for (( i=START; i<END; i+=STEP )); do
    # 计算结束的索引
    j=$((i + STEP - 1))
    
    # 确保不超过END
    if [ $j -ge $END ]; then
        j=$((END - 1))
    fi
    
    # 生成输出文件名
    OUT_FILE="out_${i}_${j}.out"
    
    # 运行命令并将输出重定向到文件
    echo "Running: sh run-test.bash $i $j $MODEL $IP1 $IP2 > $OUT_FILE &"
    sh run-test.bash $i $j $MODEL $IP1 $IP2 > $OUT_FILE &
done
