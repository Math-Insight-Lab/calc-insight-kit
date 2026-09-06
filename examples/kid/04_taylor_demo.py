# -*- coding: utf-8 -*-
"""
小学层 - 泰勒展开逼近启蒙
使用 calc_insight_kit 后端和可视化工具
"""
import numpy as np
import matplotlib.pyplot as plt
from calc_insight_kit.config import FIG_SIZE, DPI, GRID_ALPHA
from calc_insight_kit.platform_utils import setup_matplotlib
setup_matplotlib()
from calc_insight_kit.calc_backend import get_cas_backend
from calc_insight_kit.visual_tools import taylor_expand, plot_taylor_series

def main():
    backend = get_cas_backend()
    import sympy as sp
    x = sp.Symbol("x")
    f = sp.sin(x)
    
    # 使用 kit 后端和可视化工具
    order = 5
    result = taylor_expand(f, x, 0, order, backend)
    print(f"【小学启蒙】sin(x) 的 {order} 阶泰勒展开: {result['expr']}")
    plot_taylor_series(result["orig_func"], result["taylor_func"], 0, (-np.pi, np.pi), order, "kid_taylor.png")
    print("✅ 小学泰勒展开启蒙图生成完成")

if __name__ == "__main__":
    main()
