#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
运行 Mihomo 更新器的单元测试
"""

import sys
import pytest
import os

if __name__ == "__main__":
    # 确保当前目录在 Python 路径中
    current_dir = os.path.dirname(os.path.abspath(__file__))
    if current_dir not in sys.path:
        sys.path.insert(0, current_dir)
    
    print("=" * 50)
    print("开始运行 Mihomo 更新器单元测试")
    print("=" * 50)
    
    # 运行测试并收集结果
    exit_code = pytest.main(['-v', 'tests'])
    
    if exit_code == 0:
        print("\n所有测试通过!")
    else:
        print("\n测试失败，请检查错误信息。")
    
    sys.exit(exit_code) 