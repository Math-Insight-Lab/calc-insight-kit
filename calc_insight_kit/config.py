# -*- coding: utf-8 -*-
"""
全局层级配置文件 V1.0.0
统一管控三层运行开关、学术校验、可视化参数
"""

# 三层运行总开关
RUN_KID_MODE = True
RUN_MIDDLE_MODE = True
RUN_UNIVERSITY_MODE = True

# 大学学术严谨模式开关
ENABLE_EPS_DELTA = True

# 全局可视化参数
FIG_SIZE = (8, 6)
DPI = 150
GRID_ALPHA = 0.3

# CAS引擎配置
DEFAULT_CAS_ENGINE = "sympy"
SUPPORT_CAS_ENGINE = ["sympy", "maxima"]
