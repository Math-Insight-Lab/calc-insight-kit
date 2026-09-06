# -*- coding: utf-8 -*-
"""
小学层 - 可去间断点启蒙
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
    
    # 使用 kit 可视化工具绘制可去间断点
    f_np = lambda t: np.where(np.abs(t) > 1e-10, np.sin(t) / t, 1.0)
    plot_epsilon_delta_limit(f_np, (-2, 2), 0, 1.0, 0.5, 0.8, "kid_removable_singularity.png")
    print("✅ 小学可去间断点启蒙图生成完成")

if __name__ == "__main__":
    main()
