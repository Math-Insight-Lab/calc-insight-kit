# -*- coding: utf-8 -*-
"""
大学层 - \u03b5-\u03b4 极限严格定义证明与参数推导
适配数分核心：严格定义验证、\u03b4取值推导、误差区间严格约束
"""
import sympy as sp
import numpy as np
import matplotlib.pyplot as plt
from calc_insight_kit.config import FIG_SIZE, DPI, GRID_ALPHA, ENABLE_EPS_DELTA
from calc_insight_kit.calc_backend import get_cas_backend, limit_epsilon_delta
from calc_insight_kit.visual_tools import plot_epsilon_delta_limit

def main():
    if not ENABLE_EPS_DELTA:
        print("\u5f53\u524d\u672a\u5f00\u542f\u03b5-\u03b4\u4e25\u8c28\u6821\u9a8c\u6a21\u5f0f\uff0c\u8df3\u8fc7\u6f14\u793a")
        return

    from calc_insight_kit.platform_utils import setup_matplotlib

    setup_matplotlib()
    backend = get_cas_backend()
    x = sp.Symbol("x")
    f_expr = sp.sin(x) / x
    x0 = 0
    eps_list = [0.5, 0.2, 0.1]

    print("===== \u5927\u5b66\u5c42\u00b7\u03b5-\u03b4 \u4e25\u683c\u6781\u9650\u8bc1\u660e =====")
    for eps in eps_list:
        # 严格推导\u03b4参数
        res = limit_epsilon_delta(f_expr, x, x0, eps, backend)
        print(f"\n\u8bbe\u5b9a\u7cbe\u5ea6 \u03b5 = {eps:.2f}")
        print(f"\u63a8\u5bfc\u5f97\u5bf9\u5e94 \u03b4 = {res['delta']:.4f}")
        print(f"\u7ea6\u675f\u533a\u95f4\uff1ax\u2208({res['x_left']:.4f}, {res['x_right']:.4f})")
        print(f"\u51fd\u6570\u503c\u4e25\u683c\u6536\u655b\u4e8e\uff1a{res['limit_value']}\u00b1{eps}")

    # 高精度可视化验证
    f_np = lambda t: np.where(t == 0, 1.0, np.sin(t) / t)
    plot_epsilon_delta_limit(f_np, (-2, 2), 0, 1.0, 0.2, 0.24, "university_epsilon_delta.png")
    print("\n\u2705 \u5927\u5b66\u03b5-\u03b4\u4e25\u683c\u6781\u9650\u5b9a\u4e49\u9a8c\u8bc1\u5b8c\u6210")

if __name__ == "__main__":
    main()
