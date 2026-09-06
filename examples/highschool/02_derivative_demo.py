# -*- coding: utf-8 -*-
"""
中学层 - 导数切线 + 斜率计算
使用 calc_insight_kit 后端和可视化工具
"""
import sympy as sp
import numpy as np
import matplotlib.pyplot as plt
from calc_insight_kit.config import FIG_SIZE, DPI, GRID_ALPHA
from calc_insight_kit.platform_utils import setup_matplotlib
setup_matplotlib()
from calc_insight_kit.calc_backend import get_cas_backend
from calc_insight_kit.visual_tools import derivative_plot_data, plot_derivative_tangent

def main():
    backend = get_cas_backend()
    x = sp.Symbol("x")
    f = x**2 + 2*x
    
    # 使用 kit 后端求导
    df = backend.diff(f, x, 1)
    x0 = 1
    f_x0 = float(f.subs(x, x0))
    df_x0 = float(df.subs(x, x0))
    
    print(f"原函数：{f}")
    print(f"导函数：{df}")
    print(f"x={x0} 处函数值：{f_x0}")
    print(f"x={x0} 处切线斜率：{df_x0}")
    print(f"切线方程：y-{f_x0}={df_x0}(x-{x0})")
    
    # 使用 kit 可视化工具
    plot_derivative_tangent(lambda t: t**2 + 2*t, lambda t: 2*t + 2, x0, f_x0, df_x0, (-2, 3), "middle_derivative.png")
    print("✅ 中学导数切线演示完成")

if __name__ == "__main__":
    main()
