#!/bin/bash

# 切换到当前脚本所在目录
cd "$(dirname "$0")"

# 激活虚拟环境（可选，如果你有 .venv 或 venv）
# source .venv/bin/activate

# 运行 Streamlit 应用主入口
streamlit run app/main.py