# -*- coding: utf-8 -*-
"""
全局统一可视化工具 V1.0.0
三层共用绘图内核，自动适配各学段展示风格
"""
import numpy as np
import sympy as sp
import matplotlib.pyplot as plt
from typing import Dict
from .config import FIG_SIZE, DPI, GRID_ALPHA

# 使用跨平台字体配置
from .platform_utils import setup_matplotlib
setup_matplotlib()


def derivative_plot_data(f_sym, x_sym, x0: float) -> Dict:
    df_sym = sp.diff(f_sym, x_sym)
    f_x0 = float(f_sym.subs(x_sym, x0))
    df_x0 = float(df_sym.subs(x_sym, x0))
    return {
        "f_func": sp.lambdify(x_sym, f_sym, "numpy"),
        "df_func": sp.lambdify(x_sym, df_sym, "numpy"),
        "x0": x0,
        "f_x0": f_x0,
        "df_x0": df_x0
    }


def plot_derivative_tangent(f_func, df_func, x0, f_x0, df_x0, xlim, save_path: str):
    xs = np.linspace(*xlim, 400)
    def tangent(x):
        return df_x0 * (x - x0) + f_x0
    plt.figure(figsize=FIG_SIZE)
    plt.plot(xs, f_func(xs), label="原函数曲线", linewidth=1.5)
    plt.plot(xs, tangent(xs), "r--", label="切线", linewidth=1.5)
    plt.scatter(x0, f_x0, c="orange", s=60, zorder=10)
    plt.grid(alpha=GRID_ALPHA)
    plt.legend()
    plt.tight_layout()
    plt.savefig(save_path, dpi=DPI)
    plt.close()


def riemann_sum_calc(f_sym, x_sym, a: float, b: float, n: int, mode: str = "midpoint") -> Dict:
    f_np = sp.lambdify(x_sym, f_sym, "numpy")
    dx = (b - a) / n
    total = 0.0
    for i in range(n):
        if mode == "left":
            x = a + i * dx
        elif mode == "right":
            x = a + (i + 1) * dx
        else:
            x = a + (i + 0.5) * dx
        total += f_np(x) * dx
    return {"sum_val": total, "dx": dx, "n": n}


def plot_riemann_sum(f_func, a, b, n, mode, save_path):
    dx = (b - a) / n
    xs = np.linspace(a, b, 1000)
    plt.figure(figsize=FIG_SIZE)
    plt.plot(xs, f_func(xs), color="#2563eb", linewidth=2)
    for i in range(n):
        if mode == "left": x = a + i * dx
        elif mode == "right": x = a + (i + 1) * dx
        else: x = a + (i + 0.5) * dx
        y = f_func(x)
        rect_x = [a+i*dx, a+(i+1)*dx, a+(i+1)*dx, a+i*dx]
        rect_y = [0,0,y,y]
        plt.fill(rect_x, rect_y, color="#10b981", alpha=0.4)
    plt.grid(alpha=GRID_ALPHA)
    plt.tight_layout()
    plt.savefig(save_path, dpi=DPI)
    plt.close()


def taylor_expand(f_sym, x_sym, x0, order: int, backend) -> Dict:
    expr = backend.taylor(f_sym, x_sym, x0, order)
    return {
        "expr": str(expr),
        "orig_func": sp.lambdify(x_sym, f_sym, "numpy"),
        "taylor_func": sp.lambdify(x_sym, expr, "numpy")
    }


def plot_taylor_series(orig_func, taylor_func, x0, xlim, order, save_path):
    xs = np.linspace(*xlim, 600)
    plt.figure(figsize=FIG_SIZE)
    plt.plot(xs, orig_func(xs), label="原函数", linewidth=2)
    plt.plot(xs, taylor_func(xs), "r--", label=f"{order}阶泰勒拟合", linewidth=1.8)
    plt.scatter(x0, orig_func(x0), c="orange", zorder=10)
    plt.grid(alpha=GRID_ALPHA)
    plt.legend()
    plt.tight_layout()
    plt.savefig(save_path, dpi=DPI)
    plt.close()


def plot_epsilon_delta_limit(f_func, xlim, x0, lim_val, eps, delta, save_path):
    xs = np.linspace(*xlim, 800)
    plt.figure(figsize=FIG_SIZE)
    plt.plot(xs, f_func(xs), color="#4299e1", linewidth=1.5)
    plt.axhline(lim_val+eps, c="#ef4444", ls="--", alpha=0.7, label="ε误差范围")
    plt.axhline(lim_val-eps, c="#ef4444", ls="--", alpha=0.7)
    plt.axvline(x0+delta, c="#22c55e", ls="--", alpha=0.7, label="δ区间范围")
    plt.axvline(x0-delta, c="#22c55e", ls="--", alpha=0.7)
    plt.scatter(x0, lim_val, c="orange", s=80, zorder=10)
    plt.grid(alpha=GRID_ALPHA)
    plt.legend()
    plt.tight_layout()
    plt.savefig(save_path, dpi=DPI)
    plt.close()
