# -*- coding: utf-8 -*-
"""
示例 05：ε-δ 极限严格定义 — 一行代码出图

用 ε-δ 语言直观展示极限定义：红色水平带为 ε 范围，绿色竖条为 δ 范围。

运行：python 05_eps_delta_demo.py
输出：eps_delta_demo.png
"""
from calc_insight_kit import show_epsilon_delta_demo, use_theme

use_theme("teaching")

# 一行代码：绘制 ε-δ 极限定义几何解释
show_epsilon_delta_demo("sin(x)/x", x0=0, eps=0.2, save="eps_delta_demo.png", show=True)
print("  图表已保存为 eps_delta_demo.png")