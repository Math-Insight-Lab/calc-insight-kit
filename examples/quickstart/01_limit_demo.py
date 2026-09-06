# -*- coding: utf-8 -*-
"""
示例 01：极限演示 — 一行代码出图

展示函数在 x→0 处的极限行为，自动绘制极限线。

运行：python 01_limit_demo.py
输出：limit_demo.png
"""
from calc_insight_kit import plot_limit_demo, use_theme

# 使用教学主题（大字号、高对比度）
use_theme("teaching")

# 一行代码：绘制 sin(x)/x 在 x→0 处的极限
# 极限值为 1，图中自动标注
plot_limit_demo("sin(x)/x", x0=0, save="limit_demo.png", show=True)
print("  图表已保存为 limit_demo.png")