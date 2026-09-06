# -*- coding: utf-8 -*-
"""
示例 04：泰勒展开 — 一行代码出图

展示 e^x 在 x=0 处不同阶泰勒多项式的拟合效果。

运行：python 04_taylor_demo.py
输出：taylor_demo.png
"""
from calc_insight_kit import plot_taylor_demo, use_theme

use_theme("teaching")

# 一行代码：绘制泰勒展开，自动对比 1/3/5 阶拟合
plot_taylor_demo("exp(x)", x0=0, order=5, save="taylor_demo.png", show=True)
print("  图表已保存为 taylor_demo.png")