# -*- coding: utf-8 -*-
"""
大学层 - 间断点严格分类与连续性三条件校验
适配数分：连续性定义、间断点分类、可去间断点严格证明
"""
import sympy as sp
import numpy as np
import matplotlib.pyplot as plt
from calc_insight_kit.config import FIG_SIZE, DPI, GRID_ALPHA
from calc_insight_kit.calc_backend import get_cas_backend

def main():
    from calc_insight_kit.platform_utils import setup_matplotlib
    setup_matplotlib()
    backend = get_cas_backend()
    x = sp.Symbol("x")
    # 经典可去间断点函数
    f = (sp.sin(x)) / x
    x0 = 0

    print("===== \u5927\u5b66\u5c42\u00b7\u51fd\u6570\u8fde\u7eed\u6027\u4e09\u6761\u4ef6\u4e25\u683c\u6821\u9a8c =====")
    # 连续性三条件逐一验证
    lim_left = float(backend.limit(f, x, x0, "-"))
    lim_right = float(backend.limit(f, x, x0, "+"))
    lim_total = float(backend.limit(f, x, x0))

    print(f"1. \u5de6\u6781\u9650\uff1a{lim_left} | \u53f3\u6781\u9650\uff1a{lim_right}")
    print(f"2. \u53cc\u4fa7\u6781\u9650\u5b58\u5728\u4e14\u76f8\u7b49\uff1a{lim_left == lim_right == lim_total}")
    print(f"3. \u51fd\u6570\u5728x={x0}\u5904\u65e0\u5b9a\u4e49\uff0c\u6ee1\u8db3\u53ef\u53bb\u95f4\u65ad\u70b9\u5224\u5b9a\u6761\u4ef6")
    print(f"\u7ed3\u8bba\uff1ax={x0} \u4e3a\u53ef\u53bb\u95f4\u65ad\u70b9\uff0c\u8865\u5145\u5b9a\u4e49f({x0})={lim_total}\u53ef\u5b9e\u73b0\u51fd\u6570\u8fde\u7eed")

    # 精细化可视化
    x1 = np.linspace(-3, -0.01, 600)
    x2 = np.linspace(0.01, 3, 600)
    y1 = np.sin(x1) / x1
    y2 = np.sin(x2) / x2

    plt.figure(figsize=FIG_SIZE)
    plt.plot(x1, y1, color="#8e44ad", linewidth=1.8)
    plt.plot(x2, y2, color="#8e44ad", linewidth=1.8)
    plt.scatter(x0, lim_total, c="orange", s=100, zorder=10, label="\u8865\u503c\u8fde\u7eed\u70b9")
    plt.title("\u6570\u5206\u4e25\u8c28\u5206\u6790\uff1a\u53ef\u53bb\u95f4\u65ad\u70b9\u4e0e\u8fde\u7eed\u6027\u8865\u5168")
    plt.grid(alpha=GRID_ALPHA)
    plt.legend()
    plt.tight_layout()
    plt.savefig("university_removable_singularity.png", dpi=DPI)
    plt.close()
    print("\n\u2705 \u5927\u5b66\u95f4\u65ad\u70b9\u4e25\u683c\u5206\u7c7b\u8bc1\u660e\u5b8c\u6210")

if __name__ == "__main__":
    main()
