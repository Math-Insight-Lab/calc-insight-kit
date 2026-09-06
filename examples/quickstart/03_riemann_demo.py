# -*- coding: utf-8 -*-
"""
示例 03：黎曼和 — 一行代码出图

绘制 f(x)=sin(x) 在 [0, π] 上的黎曼和矩形，展示数值积分。

运行：python 03_riemann_demo.py
输出：riemann_demo.png
"""
from calc_insight_kit import plot_riemann_demo, use_theme

use_theme("teaching")

# 一行代码：绘制黎曼和，自动计算精确积分值对比
plot_riemann_demo("sin(x)", 0, 3.14159, n=20, save="riemann_demo.png", show=True)
print("  图表已保存为 riemann_demo.png")