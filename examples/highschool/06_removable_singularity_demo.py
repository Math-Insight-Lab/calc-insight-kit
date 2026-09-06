# -*- coding: utf-8 -*-
"""
中学层 - 可去间断点
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
    
    # 使用 kit 后端计算极限（证明可去间断点）
    lim_val = backend.limit(f, x, 0)
    print(f"【中学考点】sin(x)/x 在 x=0 处的极限：{lim_val}")
    print(f"因此 x=0 是可去间断点，补充定义 f(0)={lim_val} 即可连续")
    
    # 使用 kit 可视化工具绘制
    f_np = lambda t: np.where(np.abs(t) > 1e-10, np.sin(t) / t, 1.0)
    plot_epsilon_delta_limit(f_np, (-2, 2), 0, 1.0, 0.3, 0.4, "middle_removable_singularity.png")
    print("✅ 中学可去间断点演示完成")

if __name__ == "__main__":
    main()
