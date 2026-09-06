# -*- coding: utf-8 -*-
"""
小学层 - ε-δ 基础可视化启蒙
使用 calc_insight_kit 后端和可视化工具
"""
import numpy as np
import matplotlib.pyplot as plt
from calc_insight_kit.config import FIG_SIZE, DPI, GRID_ALPHA
from calc_insight_kit.platform_utils import setup_matplotlib
setup_matplotlib()
from calc_insight_kit.calc_backend import get_cas_backend
from calc_insight_kit.visual_tools import plot_epsilon_delta_limit

def main():
    backend = get_cas_backend()
    
    # 使用 kit 可视化工具绘制 ε-δ 图
    f_np = lambda t: np.where(np.abs(t) > 1e-10, np.sin(t) / t, 1.0)
    plot_epsilon_delta_limit(f_np, (-2, 2), 0, 1.0, 0.2, 0.3, "kid_epsilon_delta.png")
    print("✅ 小学ε-δ启蒙图生成完成")

if __name__ == "__main__":
    main()
