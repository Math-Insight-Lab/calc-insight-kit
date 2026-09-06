# -*- coding: utf-8 -*-
"""
中学层 - 黎曼和积分近似计算
使用 calc_insight_kit 后端和可视化工具
"""
import sympy as sp
import numpy as np
import matplotlib.pyplot as plt
from calc_insight_kit.config import FIG_SIZE, DPI, GRID_ALPHA
from calc_insight_kit.platform_utils import setup_matplotlib
setup_matplotlib()
from calc_insight_kit.calc_backend import get_cas_backend
from calc_insight_kit.visual_tools import riemann_sum_calc, plot_riemann_sum

def main():
    backend = get_cas_backend()
    x = sp.Symbol("x")
    f = sp.sin(x)
    a, b = 0, sp.pi
    exact = float(backend.integrate(f, x, (a, b)))
    
    # 使用 kit 后端和可视化工具计算不同精度的黎曼和
    n_list = [5, 20, 50]
    print(f"精确积分值：{exact:.4f}")
    
    for n in n_list:
        result = riemann_sum_calc(f, x, 0, float(sp.pi), n, mode="midpoint")
        print(f"n={n} 近似值：{result['sum_val']:.4f}（误差：{abs(result['sum_val']-exact):.4f}）")
    
    # 使用 kit 可视化工具绘制 n=20 的情况
    plot_riemann_sum(np.sin, 0, np.pi, 20, "midpoint", "middle_riemann.png")
    print("✅ 中学黎曼和积分近似演示完成")

if __name__ == "__main__":
    main()
