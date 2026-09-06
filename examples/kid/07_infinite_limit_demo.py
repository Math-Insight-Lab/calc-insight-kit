# -*- coding: utf-8 -*-
"""
小学层 - 无穷极限、竖直渐近线启蒙
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
    f = 1 / x
    
    # 使用 kit 后端计算无穷极限
    lim_pos = backend.limit(f, x, 0, dir='+')
    lim_neg = backend.limit(f, x, 0, dir='-')
    print(f"【小学启蒙】1/x 在 x→0+ 时: {lim_pos}, x→0- 时: {lim_neg}")
    
    # 手动绘图（无穷极限可视化）
    plt.figure(figsize=FIG_SIZE)
    x_pos = np.linspace(0.05, 2, 500)
    x_neg = np.linspace(-2, -0.05, 500)
    plt.plot(x_pos, 1/x_pos, color="#d35400", linewidth=2)
    plt.plot(x_neg, 1/x_neg, color="#d35400", linewidth=2)
    plt.axvline(x=0, color="#2c3e50", linestyle="--", label="竖直渐近线")
    plt.title("无穷极限：靠近竖线，数值无限变大/变小")
    plt.xlabel("x")
    plt.ylabel("y")
    plt.ylim(-10, 10)
    plt.grid(alpha=GRID_ALPHA)
    plt.legend()
    plt.tight_layout()
    plt.savefig("kid_infinite_limit.png", dpi=DPI)
    plt.close()
    print("✅ 小学无穷极限启蒙图生成完成")

if __name__ == "__main__":
    main()
