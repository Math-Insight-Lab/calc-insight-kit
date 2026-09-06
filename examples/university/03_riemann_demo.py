# -*- coding: utf-8 -*-
"""
大学层 - 黎曼和积分收敛性与误差量化分析
适配高数/数分：左右中点黎曼和、步长收敛、积分误差衰减规律
"""
import sympy as sp
import numpy as np
import matplotlib.pyplot as plt
from calc_insight_kit.config import FIG_SIZE, DPI, GRID_ALPHA
from calc_insight_kit.calc_backend import get_cas_backend
from calc_insight_kit.visual_tools import riemann_sum_calc, plot_riemann_sum

def main():
    from calc_insight_kit.platform_utils import setup_matplotlib
    setup_matplotlib()
    backend = get_cas_backend()
    x = sp.Symbol("x")
    f = sp.cos(x) + 1
    a, b = 0, sp.pi

    # 精确积分值求解
    exact_val = float(backend.integrate(f, x, (a, b)))
    print("===== \u5927\u5b66\u5c42\u00b7\u79bb\u66fc\u79ef\u5206\u6536\u655b\u6027\u5206\u6790 =====")
    print(f"\u7cbe\u786e\u79ef\u5206\u503c\uff1a{exact_val:.6f}")

    # 三种采样方式+多步长误差对比
    modes = ["left", "right", "midpoint"]
    n_list = [10, 50, 200]
    err_records = []

    plt.figure(figsize=(12, 4))
    for idx, mode in enumerate(modes):
        for n in n_list:
            calc_res = riemann_sum_calc(f, x, float(a), float(b), n, mode)
            err = abs(calc_res["sum_val"] - exact_val)
            err_records.append((mode, n, err))
        # 绘制中点采样收敛效果
        if mode == "midpoint":
            plot_riemann_sum(sp.lambdify(x, f, "numpy"), float(a), float(b), 50, mode, f"university_riemann_{mode}.png")

    # 输出误差收敛规律
    print("\n\u5404\u91c7\u6837\u65b9\u5f0f\u8bef\u5dee\u6536\u655b\u60c5\u51b5\uff1a")
    for mode, n, err in err_records:
        print(f"{mode:8s} | \u5206\u6bb5\u6570n={n:3d} | \u8bef\u5dee={err:.8f}")
    print("\n\u2705 \u5927\u5b66\u79bb\u66fc\u79ef\u5206\u6536\u655b\u6027\u4e0e\u8bef\u5dee\u5206\u6790\u6f14\u793a\u5b8c\u6210")

if __name__ == "__main__":
    main()
