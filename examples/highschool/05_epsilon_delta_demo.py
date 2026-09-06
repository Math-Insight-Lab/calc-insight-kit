# -*- coding: utf-8 -*-
"""
中学层 - ε-δ 极限直观验证
使用 calc_insight_kit 后端和可视化工具
"""
import sympy as sp
import numpy as np
import matplotlib.pyplot as plt
from calc_insight_kit.config import FIG_SIZE, DPI, GRID_ALPHA, ENABLE_EPS_DELTA
from calc_insight_kit.platform_utils import setup_matplotlib
setup_matplotlib()
from calc_insight_kit.calc_backend import get_cas_backend, limit_epsilon_delta
from calc_insight_kit.visual_tools import plot_epsilon_delta_limit

def main():
    if not ENABLE_EPS_DELTA:
        print("当前未开启 ε-δ 严谨校验模式，跳过演示")
        return
    
    backend = get_cas_backend()
    x = sp.Symbol("x")
    f_expr = sp.sin(x) / x
    x0 = 0
    eps_list = [0.5, 0.2, 0.1]
    
    print("===== 中学层·ε-δ 极限直观验证 =====")
    for eps in eps_list:
        res = limit_epsilon_delta(f_expr, x, x0, eps, backend)
        print(f"设定精度 ε = {eps:.2f}")
        print(f"推导得对应 δ = {res['delta']:.4f}")
        print(f"约束区间：x∈({res['x_left']:.4f}, {res['x_right']:.4f})")
        print(f"函数值严格收敛于：{res['limit_value']}±{eps}")
    
    # 使用 kit 可视化工具绘制
    f_np = lambda t: np.where(np.abs(t) > 1e-10, np.sin(t) / t, 1.0)
    plot_epsilon_delta_limit(f_np, (-2, 2), 0, 1.0, 0.2, 0.24, "middle_epsilon_delta.png")
    print("✅ 中学ε-δ极限直观验证演示完成")

if __name__ == "__main__":
    main()
