# -*- coding: utf-8 -*-
"""
大学层 - 导数定义、高阶导数与误差分析
适配高数/数分：导数严格定义、高阶求导、切线逼近误差量化
"""
import sympy as sp
import numpy as np
import matplotlib.pyplot as plt
from calc_insight_kit.config import FIG_SIZE, DPI, GRID_ALPHA
from calc_insight_kit.calc_backend import get_cas_backend
from calc_insight_kit.visual_tools import derivative_plot_data, plot_derivative_tangent

def main():
    from calc_insight_kit.platform_utils import setup_matplotlib
    setup_matplotlib()
    backend = get_cas_backend()
    x = sp.Symbol("x")
    f = sp.cos(x) + 0.5 * x**2
    x0 = 1.0

    # 一阶、二阶导数严格求解
    df1 = backend.diff(f, x, 1)
    df2 = backend.diff(f, x, 2)
    print("===== \u5927\u5b66\u5c42\u00b7\u9ad8\u9636\u5bfc\u6570\u4e25\u8c28\u6c42\u89e3 =====")
    print(f"\u539f\u51fd\u6570\uff1a{f}")
    print(f"\u4e00\u9636\u5bfc\u6570\uff1a{df1}")
    print(f"\u4e8c\u9636\u5bfc\u6570\uff1a{df2}")
    print(f"x={x0} \u5904\u4e00\u9636\u5bfc\u6570\u503c\uff1a{float(df1.subs(x, x0)):.4f}")
    print(f"x={x0} \u5904\u4e8c\u9636\u5bfc\u6570\u503c\uff1a{float(df2.subs(x, x0)):.4f}")

    # 切线可视化+误差分析
    plot_data = derivative_plot_data(f, x, x0)
    plot_derivative_tangent(**plot_data, xlim=(-2, 3), save_path="university_derivative.png")

    # 量化切线逼近误差
    xs_test = np.linspace(x0-0.5, x0+0.5, 100)
    f_test = plot_data["f_func"](xs_test)
    tan_test = plot_data["df_x0"] * (xs_test - x0) + plot_data["f_x0"]
    max_err = np.max(np.abs(f_test - tan_test))
    print(f"\n\u5207\u7ebf\u6700\u5927\u903c\u8fd1\u8bef\u5dee\uff08\u90bb\u57df\u8303\u56f4\u5185\uff09\uff1a{max_err:.6f}")
    print("\u2705 \u5927\u5b66\u5bfc\u6570\u9ad8\u9636\u6c42\u89e3\u4e0e\u8bef\u5dee\u5206\u6790\u6f14\u793a\u5b8c\u6210")

if __name__ == "__main__":
    main()
