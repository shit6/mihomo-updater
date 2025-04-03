#!/bin/bash

# 获取脚本所在目录的绝对路径
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

# 虚拟环境路径
VENV_PATH="${SCRIPT_DIR}/.venv"

# 检查虚拟环境是否存在
if [ ! -d "$VENV_PATH" ]; then
    echo "错误: 虚拟环境目录 (.venv) 不存在"
    echo "请先创建虚拟环境: python -m venv .venv"
    return 1 2>/dev/null || exit 1
fi

# 激活虚拟环境
echo "激活虚拟环境: $VENV_PATH"
source "${VENV_PATH}/bin/activate"

# 显示Python路径和版本
which python
python --version

echo "虚拟环境已激活，可以开始工作了！" 