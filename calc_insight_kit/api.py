# -*- coding: utf-8 -*-
"""
calc_insight_kit.api - 高层统一API
供 kid/university 示例使用
"""
import numpy as np
import sympy as sp
import matplotlib.pyplot as plt
from typing import Dict, Any, Optional

from .config import FIG_SIZE, DPI, RUN_KID_MODE
from .platform_utils import setup_matplotlib
setup_matplotlib()


class LimitResult:
    """极限计算结果的简单封装"""
    def __init__(self, x_range, f_func, x0, lim_val, epsilon_delta=None):
        self.x_range = x_range
        self.f_func = f_func
        self.x0 = x0
        self.lim_val = lim_val
        self.epsilon_delta = epsilon_delta

    @property
    def latex(self) -> str:
        if self.lim_val is None:
            return f"lim_({self.x0}) f(x) = undefined"
        return f"lim_({self.x0}) f(x) = {float(self.lim_val)}"

    def save_fig(self, path: str):
        xs = np.linspace(*self.x_range, 600)
        plt.figure(figsize=FIG_SIZE)
        plt.plot(xs, self.f_func(xs), color="#2563eb", linewidth=2, label="f(x)")
        plt.axvline(self.x0, color="orange", linestyle="--", alpha=0.7, label=f"x→{self.x0}")
        if self.lim_val is not None:
            plt.axhline(self.lim_val, color="red", linestyle="--", alpha=0.7, label=f"lim={float(self.lim_val)}")
            plt.scatter(self.x0, self.lim_val, c="red", s=80, zorder=10)
        plt.grid(alpha=0.3)
        plt.legend()
        plt.tight_layout()
        plt.savefig(path, dpi=DPI)
        plt.close()

    def close(self):
        pass


def show_limit(expr_str: str, x0: float, x_range: tuple = (-5, 5)) -> LimitResult:
    """
    展示极限函数 f(x) 在 x→x0 时的行为。

    用法:
        res = show_limit("sin(x)/x", x0=0.0, x_range=(-3,3))
        res.save_fig("limit_sinx_x.png")
        print(res.latex)
    """
    x_sym = sp.Symbol("x")
    f_sym = sp.sympify(expr_str)
    f_func = sp.lambdify(x_sym, f_sym, "numpy")

    # 计算双侧极限
    try:
        lim_val = sp.limit(f_sym, x_sym, x0)
    except Exception:
        lim_val = None

    return LimitResult(x_range, f_func, x0, lim_val)
