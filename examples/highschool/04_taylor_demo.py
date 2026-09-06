# -*- coding: utf-8 -*-
"""
中学层 - 泰勒展开与误差分析
使用 calc_insight_kit 后端和可视化工具
"""
import sympy as sp
import numpy as np
import matplotlib.pyplot as plt
from calc_insight_kit.config import FIG_SIZE, DPI, GRID_ALPHA
from calc_insight_kit.platform_utils import setup_matplotlib
setup_matplotlib()
from calc_insight_kit.calc_backend import get_cas_backend
from calc_insight_kit.visual_tools import taylor_expand, plot_taylor_series

def main():
    backend = get_cas_backend()
    x = sp.Symbol("x")
    f = sp.sin(x)
    
    # 使用 kit 后端和可视化工具绘制不同阶数的泰勒展开
    orders = [1, 3, 5]
    for order in orders:
        result = taylor_expand(f, x, 0, order, backend)
        print(f"【中学考点】sin(x) 的 {order} 阶泰勒展开：{result['expr']}")
    
    # 使用 kit 可视化工具绘制 5 阶泰勒展开
    result = taylor_expand(f, x, 0, 5, backend)
    plot_taylor_series(result["orig_func"], result["taylor_func"], 0, (-np.pi, np.pi), 5, "middle_taylor.png")
    print("✅ 中学泰勒展开演示完成")

if __name__ == "__main__":
    main()
