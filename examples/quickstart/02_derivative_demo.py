# -*- coding: utf-8 -*-
"""
示例 02：导数与切线 — 一行代码出图

绘制函数 f(x)=x^2 及其在 x=1 处的切线，自动计算斜率。

运行：python 02_derivative_demo.py
输出：derivative_demo.png
"""
from calc_insight_kit import plot_derivative_demo, use_theme

use_theme("teaching")

# 一行代码：绘制 f(x)=x^2 在 x=1 处的切线
plot_derivative_demo("x**2", x0=1, save="derivative_demo.png", show=True)
print("  图表已保存为 derivative_demo.png")