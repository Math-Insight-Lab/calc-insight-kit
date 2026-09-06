# -*- coding: utf-8 -*-
"""
中学层 - 无穷极限
使用 calc_insight_kit 后端和可视化工具
"""
import sympy as sp
import numpy as np
import matplotlib.pyplot as plt
from calc_insight_kit.config import FIG_SIZE, DPI, GRID_ALPHA
from calc_insight_kit.platform_utils import setup_matplotlib
setup_matplotlib()
from calc_insight_kit.calc_backend import get_cas_backend

def main():
    backend = get_cas_backend()
    x = sp.Symbol("x")
    
    # 使用 kit 后端计算无穷极限
    f1 = 1 / x
    lim_pos = backend.limit(f1, x, 0, dir='+')
    lim_neg = backend.limit(f1, x, 0, dir='-')
    print(f"【中学考点】1/x 在 x→0+ 时：{lim_pos}，x→0- 时：{lim_neg}")
    
    # 手动绘图
    plt.figure(figsize=FIG_SIZE)
    x_pos = np.linspace(0.05, 2, 500)
    x_neg = np.linspace(-2, -0.05, 500)
    plt.plot(x_pos, 1/x_pos, color="#d35400", linewidth=2, label="1/x (x>0)")
    plt.plot(x_neg, 1/x_neg, color="#d35400", linewidth=2, label="1/x (x<0)")
    plt.axvline(x=0, color="#2c3e50", linestyle="--", label="竖直渐近线")
    plt.title("无穷极限：靠近竖线，数值无限变大/变小")
    plt.xlabel("x")
    plt.ylabel("y")
    plt.ylim(-10, 10)
    plt.grid(alpha=GRID_ALPHA)
    plt.legend()
    plt.tight_layout()
    plt.savefig("middle_infinite_limit.png", dpi=DPI)
    plt.close()
    print("✅ 中学无穷极限演示完成")

if __name__ == "__main__":
    main()
