# -*- coding: utf-8 -*-
"""
小学层 - 导数切线演示启蒙
使用 calc_insight_kit 后端和可视化工具
"""
import numpy as np
import matplotlib.pyplot as plt
from calc_insight_kit.config import FIG_SIZE, DPI, GRID_ALPHA
from calc_insight_kit.platform_utils import setup_matplotlib
setup_matplotlib()
from calc_insight_kit.calc_backend import get_cas_backend
from calc_insight_kit.visual_tools import derivative_plot_data, plot_derivative_tangent

def main():
    backend = get_cas_backend()
    import sympy as sp
    x = sp.Symbol("x")
    f = sp.sin(x)
    
    # 使用 kit 后端和可视化工具
    data = derivative_plot_data(f, x, np.pi / 2)
    print(f"【小学启蒙】sin(x) 在 x=π/2 处: f={data['f_x0']:.4f}, f'={data['df_x0']:.4f}")
    plot_derivative_tangent(data["f_func"], data["df_func"], data["x0"], data["f_x0"], data["df_x0"], (0, 2*np.pi), "kid_derivative.png")
    print("✅ 小学导数切线启蒙图生成完成")

if __name__ == "__main__":
    main()
