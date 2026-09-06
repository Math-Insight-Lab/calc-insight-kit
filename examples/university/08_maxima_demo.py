# -*- coding: utf-8 -*-
"""
大学层 - Maxima 后端功能演示
展示 calc_insight_kit 的 Maxima 后端能力（对比 SymPy 默认后端）
"""
import sympy as sp
import numpy as np
import matplotlib.pyplot as plt
from calc_insight_kit.config import FIG_SIZE, DPI, GRID_ALPHA
from calc_insight_kit.platform_utils import setup_matplotlib
setup_matplotlib()
from calc_insight_kit.maxima_bridge import get_cas_backend


def main():
    # 获取 Maxima 后端（如果不可用则 fallback 到 SymPy）
    try:
        backend = get_cas_backend(prefer_maxima=True)
        engine = "Maxima"
    except Exception:
        backend = get_cas_backend()
        engine = "SymPy (fallback)"

    x = sp.Symbol("x")
    print(f"===== 大学层·{engine} 后端功能演示 =====\n")

    # 1. 求导
    f1 = x**3 - 2*x**2 + 3*x - 4
    d1 = backend.diff(f1, x)
    print(f"1. 求导: d/dx({f1}) = {d1}")

    # 2. 积分
    f2 = x**2 + 1
    int2 = backend.integrate(f2, x)
    print(f"2. 不定积分: int({f2})dx = {int2}")

    # 3. 定积分
    int3 = backend.definite_integral(f2, x, 0, 1)
    print(f"3. 定积分: int_0^1({f2})dx = {int3}")

    # 4. 极限
    f4 = sp.sin(x) / x
    lim4 = backend.limit(f4, x, 0)
    print(f"4. 极限: lim(x->0) sin(x)/x = {lim4}")

    # 5. 泰勒展开
    t5 = backend.taylor(sp.sin(x), x, 0, 5)
    print(f"5. 泰勒展开: sin(x) = {t5}")

    print("\n✅ Maxima 后端功能演示完成")


if __name__ == "__main__":
    main()
