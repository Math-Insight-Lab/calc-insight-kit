# -*- coding: utf-8 -*-
"""
中学层 - 函数极限可视化 + 数值计算
使用 calc_insight_kit 后端和可视化工具
"""
import sympy as sp
import numpy as np
import matplotlib.pyplot as plt
from calc_insight_kit.config import FIG_SIZE, DPI, GRID_ALPHA
from calc_insight_kit.platform_utils import setup_matplotlib
setup_matplotlib()
from calc_insight_kit.calc_backend import get_cas_backend
from calc_insight_kit.visual_tools import plot_epsilon_delta_limit

def main():
    backend = get_cas_backend()
    x = sp.Symbol("x")
    f = sp.sin(x) / x
    
    # 使用 kit 后端计算极限
    limit_res = backend.limit(f, x, 0)
    print(f"【中学考点】sin(x)/x 在 x→0 的极限值：{limit_res}")
    
    # 使用 kit 可视化工具
    f_np = lambda t: np.where(np.abs(t) > 1e-10, np.sin(t) / t, 1.0)
    plot_epsilon_delta_limit(f_np, (-2, 2), 0, float(limit_res), 0.1, 0.2, "middle_limit.png")
    print("✅ 中学极限计算演示完成")

if __name__ == "__main__":
    main()
