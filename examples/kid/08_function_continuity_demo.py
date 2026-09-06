# -*- coding: utf-8 -*-
"""
小学层 - 函数连续/间断对比启蒙
使用 calc_insight_kit 后端和可视化工具
"""
import numpy as np
import matplotlib.pyplot as plt
from calc_insight_kit.config import FIG_SIZE, DPI, GRID_ALPHA
from calc_insight_kit.platform_utils import setup_matplotlib
setup_matplotlib()
from calc_insight_kit.calc_backend import get_cas_backend

def main():
    backend = get_cas_backend()
    import sympy as sp
    x = sp.Symbol("x")
    
    # 使用 kit 后端验证连续性
    f_cont = x**2
    lim_left = backend.limit(f_cont, x, 0)
    lim_right = backend.limit(f_cont, x, 0)
    print(f"【小学启蒙】x² 在 x=0 处连续: lim={lim_left}={lim_right}")
    
    # 手动绘制连续/间断对比图
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4))
    
    # 左侧：连续函数
    x1 = np.linspace(-2, 2, 500)
    ax1.plot(x1, x1**2, color="#27ae60", linewidth=2)
    ax1.set_title("连续函数：顺滑无断开")
    ax1.grid(alpha=GRID_ALPHA)
    
    # 右侧：间断函数
    x2_1 = np.linspace(-2, -0.01, 300)
    x2_2 = np.linspace(0.01, 2, 300)
    ax2.plot(x2_1, 1/x2_1, color="#e74c3c", linewidth=2)
    ax2.plot(x2_2, 1/x2_2, color="#e74c3c", linewidth=2)
    ax2.set_title("间断函数：中间断开不连贯")
    ax2.grid(alpha=GRID_ALPHA)
    
    plt.tight_layout()
    plt.savefig("kid_function_continuity.png", dpi=DPI)
    plt.close()
    print("✅ 小学函数连续性对比图生成完成")

if __name__ == "__main__":
    main()
