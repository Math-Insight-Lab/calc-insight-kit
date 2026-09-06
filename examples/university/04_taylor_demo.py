# -*- coding: utf-8 -*-
"""
大学层 - 泰勒展开收敛域与阶数误差分析
适配高数/数分：麦克劳林展开、阶数递增收敛、局部/全局误差差异
"""
import sympy as sp
import numpy as np
import matplotlib.pyplot as plt
from calc_insight_kit.config import FIG_SIZE, DPI, GRID_ALPHA
from calc_insight_kit.calc_backend import get_cas_backend
from calc_insight_kit.visual_tools import taylor_expand, plot_taylor_series

def main():
    from calc_insight_kit.platform_utils import setup_matplotlib
    setup_matplotlib()
    backend = get_cas_backend()
    x = sp.Symbol("x")
    f = sp.sin(x)
    x0 = 0
    ords = [3, 5, 7, 9]

    print("===== \u5927\u5b66\u5c42\u00b7\u6cf0\u52d2\u5c55\u5f00\u4e25\u8c28\u5206\u6790 =====")
    plt.figure(figsize=FIG_SIZE)
    xs = np.linspace(-np.pi, np.pi, 600)
    true_func = sp.lambdify(x, f, "numpy")
    plt.plot(xs, true_func(xs), label="\u539f\u51fd\u6570 sin(x)", linewidth=2, color="#2c3e50")

    # 多阶泰勒展开对比+误差统计
    for order in ords:
        taylor_res = taylor_expand(f, x, x0, order, backend)
        print(f"{order}\u9636\u9ea6\u514b\u96f7\u6797\u5c55\u5f00\uff1a{taylor_res['expr']}")
        plt.plot(xs, taylor_res["taylor_func"](xs), "--", linewidth=1.5, label=f"{order}\u9636\u5c55\u5f00")
        # 量化最大误差
        err = np.max(np.abs(true_func(xs) - taylor_res["taylor_func"](xs)))
        print(f"{order}\u9636\u5c55\u5f00\u5168\u5c40\u6700\u5927\u8bef\u5dee\uff1a{err:.8f}")

    plt.grid(alpha=GRID_ALPHA)
    plt.legend()
    plt.title("\u5927\u5b66\u6cf0\u52d2\u5c55\u5f00\uff1a\u9636\u6570\u9012\u589e\u4e0e\u6536\u655b\u8bef\u5dee\u5bf9\u6bd4")
    plt.tight_layout()
    plt.savefig("university_taylor.png", dpi=DPI)
    plt.close()
    print("\n\u2705 \u5927\u5b66\u6cf0\u52d2\u5c55\u5f00\u6536\u655b\u6027\u5206\u6790\u6f14\u793a\u5b8c\u6210")

if __name__ == "__main__":
    main()
