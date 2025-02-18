#!/bin/bash

HOME_DIR="$HOME"

# 设置备份文件名（使用当前日期和时间）
BACKUP_FILE="$HOME_DIR/齐思远.tar.gz"

# 创建临时目录
TEMP_DIR=$(mktemp -d)

# 复制需要备份的文件夹到临时目录
cp -R "$HOME_DIR/.lcpr/process" "$TEMP_DIR/" 2>/dev/null
cp -R "$HOME_DIR/.lcpr/src" "$TEMP_DIR/" 2>/dev/null
cp -R "$HOME_DIR/.continue/sessions" "$TEMP_DIR/" 2>/dev/null

# 创建压缩文件
tar -czf "$BACKUP_FILE" -C "$TEMP_DIR" .

# 清理临时目录
rm -rf "$TEMP_DIR"

echo "备份已完成：$BACKUP_FILE"