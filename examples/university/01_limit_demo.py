# -*- coding: utf-8 -*-
"""
大学层 - 极限严谨求解与左右极限分析
适配高数/数分：双侧极限、单侧极限、极限存在性严格判定
"""
import sympy as sp
import numpy as np
import matplotlib.pyplot as plt
from calc_insight_kit.config import FIG_SIZE, DPI, GRID_ALPHA
from calc_insight_kit.calc_backend import get_cas_backend

def main():
    from calc_insight_kit.platform_utils import setup_matplotlib
    setup_matplotlib()
    # 初始化CAS计算后端
    backend = get_cas_backend()
    x = sp.Symbol("x")

    # 多案例严谨极限分析
    cases = [
        (sp.sin(x)/x, x, 0, "\u91cd\u8981\u6781\u9650 sin(x)/x"),
        ((sp.exp(x)-1)/x, x, 0, "\u6307\u6570\u6781\u9650 (e^x-1)/x"),
        ((x**2-4)/(x-2), x, 2, "\u5206\u5f0f\u53ef\u53bb\u6781\u9650")
    ]

    print("===== \u5927\u5b66\u5c42\u00b7\u4e25\u683c\u6781\u9650\u6c42\u89e3\uff08\u53cc\u4fa7+\u5355\u4fa7\uff09=====")
    for expr, var, point, desc in cases:
        lim_all = backend.limit(expr, var, point)
        lim_left = backend.limit(expr, var, point, dir="-")
        lim_right = backend.limit(expr, var, point, dir="+")
        print(f"\n\u3010{desc}\u3011")
        print(f"\u53cc\u4fa7\u6781\u9650\uff1a{lim_all}")
        print(f"\u5de6\u6781\u9650\uff1a{lim_left} | \u53f3\u6781\u9650\uff1a{lim_right}")
        print(f"\u6781\u9650\u5b58\u5728\u5224\u5b9a\uff1a{lim_left == lim_right}")

    # 核心案例可视化
    plt.figure(figsize=FIG_SIZE)
    x_vals = np.linspace(-2, 2, 800)
    y_vals = np.sin(x_vals) / x_vals
    plt.plot(x_vals, y_vals, color="#3498db", linewidth=1.8, label="f(x)=sin(x)/x")
    plt.axhline(1, c="#e74c3c", ls="--", label="\u6781\u9650\u503c L=1")
    plt.grid(alpha=GRID_ALPHA)
    plt.legend()
    plt.title("\u5927\u5b66\u4e25\u8c28\u6781\u9650\uff1a\u5355\u4fa7/\u53cc\u4fa7\u6781\u9650\u5b58\u5728\u6027\u5224\u5b9a")
    plt.tight_layout()
    plt.savefig("university_limit.png", dpi=DPI)
    plt.close()
    print("\n\u2705 \u5927\u5b66\u6781\u9650\u4e25\u8c28\u5206\u6790\u6f14\u793a\u5b8c\u6210")

if __name__ == "__main__":
    main()
