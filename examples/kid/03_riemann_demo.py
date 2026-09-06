# -*- coding: utf-8 -*-
"""
小学层 - 黎曼和积分启蒙
使用 calc_insight_kit 后端和可视化工具
"""
import numpy as np
import matplotlib.pyplot as plt
from calc_insight_kit.config import FIG_SIZE, DPI, GRID_ALPHA
from calc_insight_kit.platform_utils import setup_matplotlib
setup_matplotlib()
from calc_insight_kit.calc_backend import get_cas_backend
from calc_insight_kit.visual_tools import riemann_sum_calc, plot_riemann_sum

def main():
    backend = get_cas_backend()
    import sympy as sp
    x = sp.Symbol("x")
    f = sp.sin(x)
    
    # 使用 kit 后端和可视化工具
    n = 15
    result = riemann_sum_calc(f, x, 0, np.pi, n, mode="midpoint")
    print(f"【小学启蒙】sin(x) 在 [0,π] 上的 {n} 等分黎曼和: {result['sum_val']:.4f}")
    f_np = lambda t: np.sin(t)
    plot_riemann_sum(f_np, 0, np.pi, n, "midpoint", "kid_riemann.png")
    print("✅ 小学黎曼和积分启蒙图生成完成")

if __name__ == "__main__":
    main()
