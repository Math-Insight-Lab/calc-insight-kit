# -*- coding: utf-8 -*-
"""
教师薄包装 API — 一行调用，一键出图。

核心理念：
  - 简单场景一行搞定：plot_limit_demo("sin(x)/x", x0=0)
  - 复杂场景完全开放底层能力：backend.diff(f, x, order=2)
  - 免调 matplotlib 参数、字体、配色、动画逻辑
  - 统一输出：PNG / GIF / LaTeX / Jupyter 内联

使用方式：
    # 导入薄包装 API
    from calc_insight_kit.teacher_api import (
        plot_limit_demo,
        plot_derivative_demo,
        plot_riemann_demo,
        plot_taylor_demo,
        show_epsilon_delta_demo,
    )

    # 一行出图
    plot_limit_demo("sin(x)/x", x0=0, save="limit.png")
"""
import os
import sys
import numpy as np
import sympy as sp

from .styles import use_theme, use_theme_context, get_active_theme
from .output import CASOutput, latex_fragment
from .errors import (
    CASValidationError,
    CASComputationalError,
    validate_limit_context,
    validate_derivative_context,
    validate_riemann_params,
    validate_taylor_params,
    validate_integral_bounds,
    validate_epsilon_delta_demo_params,
    handle_cas_errors,
)

# ── 统一自动配置 ─────────────────────────────────────────────────────
from .platform_utils import setup_matplotlib
setup_matplotlib()
from .config import FIG_SIZE, DPI, GRID_ALPHA

# 默认使用教学主题
use_theme("teaching")


def _parse_expr(expr_str):
    """解析表达式字符串为 SymPy 对象。"""
    try:
        return sp.sympify(expr_str)
    except Exception:
        raise CASValidationError(
            message=f"无法解析表达式: {expr_str}",
            teaching_hint="请检查表达式语法是否正确。支持 Python 数学语法：x**2, sin(x), exp(x) 等",
            solution="参考 SymPy 文档: https://docs.sympy.org/latest/tutorials/intro-tutorial/symbols.html",
        )


def _to_numpy_func(expr_or_str, var_name="x"):
    """将表达式或字符串转换为 numpy 可调用函数。"""
    try:
        if isinstance(expr_or_str, str):
            expr = _parse_expr(expr_or_str)
        else:
            expr = expr_or_str
        x = sp.Symbol(var_name)
        return sp.lambdify(x, expr, "numpy")
    except Exception as e:
        raise CASComputationalError(
            message=f"无法创建数值函数: {e}",
            teaching_hint="请确保表达式是 x 的有效函数",
            solution="检查表达式是否包含未定义的符号",
        )


def _default_x_range(x0, x_range=None):
    """根据极限点自动推断合理的默认 x 范围。"""
    if x_range:
        return x_range
    # 根据 x0 自动推断范围
    if abs(x0) < 1:
        return (-3, 3)
    elif abs(x0) < 5:
        return (x0 - 4, x0 + 4)
    else:
        return (x0 - 6, x0 + 6)


# ══════════════════════════════════════════════════════════════════════
# 1. 极限演示
# ══════════════════════════════════════════════════════════════════════

def plot_limit_demo(
    expr_str: str,
    x0: float,
    x_range: tuple = None,
    lim_val=None,
    save: str = None,
    show: bool = True,
    title: str = None,
    theme: str = "teaching",
):
    """绘制函数在 x→x0 处的极限行为。

    一行出图，自动处理字体、配色、坐标范围。

    参数
    ------
    expr_str : str
        函数表达式字符串，如 "sin(x)/x"
    x0 : float
        极限趋近的点
    x_range : tuple, optional
        x 轴显示范围 (xmin, xmax)。默认自动推断
    lim_val : float, optional
        极限值。默认由 SymPy 自动计算
    save : str, optional
        输出 PNG 路径
    show : bool
        是否在 Jupyter 中内联显示
    title : str, optional
        图表标题
    theme : str
        "teaching" 或 "paper"

    示例
    ----
    >>> plot_limit_demo("sin(x)/x", x0=0)
    >>> plot_limit_demo("1/(x-1)", x0=1, save="singularity.png")
    """
    f_np = _to_numpy_func(expr_str)
    x_sym = sp.Symbol("x")
    f_sym = _parse_expr(expr_str)
    xr = _default_x_range(x0, x_range)

    # 自动计算极限值
    if lim_val is None:
        try:
            lim_val = float(sp.limit(f_sym, x_sym, x0))
        except Exception:
            lim_val = None

    if title is None:
        title = f"$\\lim_{{x \\to {x0}}}$ {expr_str}"

    out = CASOutput(title=title, figsize=(10, 7))
    ax = out.ax

    xs = np.linspace(*xr, 2000)
    # 避免除以零
    ys = np.where(np.isnan(f_np(xs)), np.nan, f_np(xs))
    ax.plot(xs, ys, color="#2563eb", linewidth=2.5, label=f"$f(x) = {expr_str}$")
    ax.axvline(x0, color="#f59e0b", linestyle="--", alpha=0.7, linewidth=1.5, label=f"$x \\to {x0}$")

    if lim_val is not None and np.isfinite(lim_val):
        ax.axhline(lim_val, color="#ef4444", linestyle="--", alpha=0.7, linewidth=1.5, label=f"$\\lim = {lim_val:.4f}$")
        ax.scatter([x0], [lim_val], c="#ef4444", s=100, zorder=10)

    ax.set_xlim(*xr)
    ax.set_ylim(bottom=min(ys[ys != np.inf]) * 0.9 if len(ys[ys != np.inf]) > 0 else -5,
                top=max(ys[ys != np.inf]) * 1.1 if len(ys[ys != np.inf]) > 0 else 5)
    ax.grid(alpha=GRID_ALPHA)
    ax.legend(loc="best", fontsize=11)
    ax.set_xlabel("$x$", fontsize=13)
    ax.set_ylabel("$f(x)$", fontsize=13)

    if save:
        out.save_png(save)
        print(f"  图表已保存: {os.path.abspath(save)}")
    if show:
        out.show_jupyter()

    return out


# ══════════════════════════════════════════════════════════════════════
# 2. 导数与切线演示
# ══════════════════════════════════════════════════════════════════════

def plot_derivative_demo(
    expr_str: str,
    x0: float,
    x_range: tuple = None,
    save: str = None,
    show: bool = True,
    title: str = None,
    theme: str = "teaching",
):
    """绘制函数及其在 x=x0 处的切线。

    一行出图，自动计算导数、斜率、切线方程。

    参数
    ------
    expr_str : str
        函数表达式字符串
    x0 : float
        求导点
    x_range : tuple, optional
    save : str, optional
    show : bool
    title : str, optional
    theme : str

    示例
    ----
    >>> plot_derivative_demo("x**2", x0=1)
    >>> plot_derivative_demo("x**3 - 3*x", x0=2, save="cubic_tangent.png")
    """
    validate_derivative_context(expr_str, "x")
    f_sym = _parse_expr(expr_str)
    x = sp.Symbol("x")
    f_np = _to_numpy_func(expr_str)
    df_sym = sp.diff(f_sym, x)
    df_np = sp.lambdify(x, df_sym, "numpy")

    f_x0 = f_np(x0)
    df_x0 = df_np(x0)

    if title is None:
        title = f"切线: $f(x)={expr_str}$ at $x={x0}$"

    out = CASOutput(title=title, figsize=(10, 7))
    ax = out.ax

    xr = _default_x_range(x0, x_range)
    xs = np.linspace(*xr, 800)
    ax.plot(xs, f_np(xs), color="#2563eb", linewidth=2.5, label=f"$f(x) = {expr_str}$")

    # 切线
    tangent = df_x0 * (xs - x0) + f_x0
    ax.plot(xs, tangent, color="#ef4444", linestyle="--", linewidth=2,
            label=f"切线: $y={df_x0:.2f}(x-{x0})+{f_x0:.2f}$")

    ax.scatter([x0], [f_x0], c="#f59e0b", s=100, zorder=10, label=f"点 ({x0}, {f_x0:.2f})")
    ax.axhline(0, color="#000", linewidth=0.5)
    ax.axvline(0, color="#000", linewidth=0.5)
    ax.grid(alpha=GRID_ALPHA)
    ax.legend(loc="best", fontsize=11)
    ax.set_xlabel("$x$", fontsize=13)
    ax.set_ylabel("$f(x)$", fontsize=13)
    print(f"  导数: f'({x0}) = {df_x0:.4f}")
    print(f"  切线方程: y = {df_x0:.4f}(x - {x0}) + {f_x0:.4f}")

    if save:
        out.save_png(save)
        print(f"  图表已保存: {os.path.abspath(save)}")
    if show:
        out.show_jupyter()

    return out


# ══════════════════════════════════════════════════════════════════════
# 3. 黎曼和演示
# ══════════════════════════════════════════════════════════════════════

def plot_riemann_demo(
    expr_str: str,
    a: float,
    b: float,
    n: int = 10,
    mode: str = "midpoint",
    save: str = None,
    show: bool = True,
    title: str = None,
):
    """绘制黎曼和近似积分，矩形高亮显示。

    一行出图，自动计算精确积分值并对比误差。

    参数
    ------
    expr_str : str
        被积函数
    a, b : float
        积分上下限
    n : int
        矩形分割数
    mode : str
        "left", "right", "midpoint"
    save : str, optional
    show : bool
    title : str, optional

    示例
    ----
    >>> plot_riemann_demo("sin(x)", 0, 3.14159, n=10)
    >>> plot_riemann_demo("x**2", 0, 2, n=20, mode="right", save="riemann_right.png")
    """
    validate_riemann_params(a, b, n, mode)
    f_sym = _parse_expr(expr_str)
    x = sp.Symbol("x")
    f_np = _to_numpy_func(expr_str)
    xr = (a, b)

    # 精确积分
    exact = float(sp.integrate(f_sym, (x, a, b)))
    dx = (b - a) / n

    if title is None:
        title = f"$\\int_{{{a}}}^{{{b}}}$ {expr_str} dx  (n={n}, {mode})"

    out = CASOutput(title=title, figsize=(10, 7))
    ax = out.ax

    xs = np.linspace(a, b, 1000)
    ax.plot(xs, f_np(xs), color="#2563eb", linewidth=2.5, label="$f(x)$")

    colors = ["#10b981", "#34d399", "#6ee7b7", "#a7f3d0"]
    for i in range(n):
        if mode == "left":
            xi = a + i * dx
        elif mode == "right":
            xi = a + (i + 1) * dx
        else:
            xi = a + (i + 0.5) * dx
        yi = f_np(xi)
        if np.isfinite(yi):
            rect_x = [a + i * dx, a + (i + 1) * dx, a + (i + 1) * dx, a + i * dx]
            rect_y = [0, 0, yi, yi]
            color = colors[i % len(colors)]
            ax.fill(rect_x, rect_y, color=color, alpha=0.5)

    ax.axhline(0, color="#000", linewidth=0.5)
    ax.grid(alpha=GRID_ALPHA)
    ax.legend(loc="best", fontsize=11)
    ax.set_xlabel("$x$", fontsize=13)
    ax.set_ylabel("$f(x)$", fontsize=13)

    # 打印信息
    approx = np.sum(f_np(np.array([a + (i + 0.5) * dx for i in range(n)])) * dx) if mode == "midpoint" else None
    if approx is not None:
        err = abs(approx - exact)
        ax.text(0.02, 0.95,
                f"精确值: {exact:.6f}\n近似值: {approx:.6f}\n误差:   {err:.6f}",
                transform=ax.transAxes, fontsize=10,
                verticalalignment="top",
                bbox=dict(boxstyle="round", facecolor="wheat", alpha=0.5))

    if save:
        out.save_png(save)
        print(f"  图表已保存: {os.path.abspath(save)}")
    if show:
        out.show_jupyter()

    return out


# ══════════════════════════════════════════════════════════════════════
# 4. 泰勒展开演示
# ══════════════════════════════════════════════════════════════════════

def plot_taylor_demo(
    expr_str: str,
    x0: float,
    order: int = 5,
    x_range: tuple = None,
    save: str = None,
    show: bool = True,
    title: str = None,
):
    """绘制原函数与不同阶泰勒多项式的拟合对比。

    一行出图，自动对比 1/3/5 阶拟合效果。

    参数
    ------
    expr_str : str
        函数表达式
    x0 : float
        展开中心
    order : int
        最高展开阶数
    x_range : tuple, optional
    save : str, optional
    show : bool
    title : str, optional

    示例
    ----
    >>> plot_taylor_demo("exp(x)", x0=0, order=5)
    >>> plot_taylor_demo("cos(x)", x0=0, order=8, save="cos_taylor.png")
    """
    validate_taylor_params(order, x0)
    f_sym = _parse_expr(expr_str)
    x = sp.Symbol("x")
    f_np = _to_numpy_func(expr_str)

    if x_range is None:
        if abs(x0) < 1:
            xr = (-4, 4)
        elif abs(x0) < 3:
            xr = (x0 - 5, x0 + 5)
        else:
            xr = (x0 - 8, x0 + 8)
    else:
        xr = x_range

    if title is None:
        title = f"泰勒展开: $f(x)={expr_str}$ at $x={x0}$"

    out = CASOutput(title=title, figsize=(10, 7))
    ax = out.ax

    xs = np.linspace(*xr, 1000)
    orig_ys = f_np(xs)
    ax.plot(xs, orig_ys, color="#2563eb", linewidth=3, label="$f(x)$ (原函数)")

    # 计算并绘制各阶泰勒多项式
    taylor_colors = ["#ef4444", "#f59e0b", "#10b981"]
    for o in [1, 3, min(order, 9)]:
        taylor_expr = sp.series(f_sym, x, x0, n=o + 1).removeO()
        taylor_np = sp.lambdify(x, taylor_expr, "numpy")
        try:
            taylor_ys = taylor_np(xs)
            ax.plot(xs, taylor_ys, color=taylor_colors[0] if o == 1 else (taylor_colors[1] if o == 3 else taylor_colors[2]),
                    linestyle="--", linewidth=1.8, label=f"{o}阶泰勒")
        except (ValueError, ZeroDivisionError, OverflowError):
            pass

    ax.scatter([x0], [f_np(x0)], c="black", s=80, zorder=10)
    ax.grid(alpha=GRID_ALPHA)
    ax.legend(loc="best", fontsize=10)
    ax.set_xlabel("$x$", fontsize=13)
    ax.set_ylabel("$f(x)$", fontsize=13)

    if save:
        out.save_png(save)
        print(f"  图表已保存: {os.path.abspath(save)}")
    if show:
        out.show_jupyter()

    return out


# ══════════════════════════════════════════════════════════════════════
# 5. ε-δ 极限严格定义演示
# ══════════════════════════════════════════════════════════════════════

def show_epsilon_delta_demo(
    expr_str: str,
    x0: float,
    eps: float = 0.2,
    x_range: tuple = None,
    delta=None,
    save: str = None,
    show: bool = True,
):
    """绘制 ε-δ 极限定义的几何解释。

    红框 = ε 范围，绿框 = δ 范围，直观展示极限严格定义。

    参数
    ------
    expr_str : str
        函数表达式
    x0 : float
        极限趋近点
    eps : float
        ε 值（误差范围）
    x_range : tuple, optional
    delta : float, optional
        δ 值。默认自动推导
    save : str, optional
    show : bool

    示例
    ----
    >>> show_epsilon_delta_demo("sin(x)/x", x0=0, eps=0.2)
    >>> show_epsilon_delta_demo("(x**2 - 1)/(x - 1)", x0=1, eps=0.1, save="eps_delta.png")
    """
    f_sym = _parse_expr(expr_str)
    x = sp.Symbol("x")
    f_np = _to_numpy_func(expr_str)

    # 自动计算极限
    try:
        lim_val = float(sp.limit(f_sym, x, x0))
    except Exception:
        raise CASComputationalError(
            message=f"无法计算极限值",
            teaching_hint=f"函数在 x0={x0} 处的极限可能不存在或为无穷",
            solution="请检查函数在该点是否有确定的极限，或手动指定 lim_val 参数",
        )

    # 验证参数
    validate_limit_context(x0, lim_val, eps)
    if eps > 10:
        raise CASValidationError(
            message=f"epsilon={eps} 过大，极限定义失去意义",
            teaching_hint="ε 通常取 0.1, 0.01, 0.001 这样的小数",
            solution="请减小 epsilon，例如 epsilon=0.1",
        )

    # 自动推导 δ
    if delta is None:
        # 数值方法推导 δ: 找到最大的 δ 使得 |f(x) - L| < ε 在 (x0-δ, x0+δ) 内成立
        delta = _numerical_delta(f_np, x0, lim_val, eps)

    validate_epsilon_delta_demo_params(f_np, x0, lim_val, eps)

    xr = _default_x_range(x0, x_range)
    # 确保 x_range 覆盖 δ 区间
    xr = (min(xr[0], x0 - delta * 2 - 0.1), max(xr[1], x0 + delta * 2 + 0.1))

    out = CASOutput(title=f"$\\varepsilon$-$\\delta$ 极限定义: $f(x)={expr_str}$",
                    figsize=(12, 8))
    ax = out.ax

    xs = np.linspace(*xr, 2000)
    ys = np.where(np.isnan(f_np(xs)), np.nan, f_np(xs))
    ax.plot(xs, ys, color="#4299e1", linewidth=2.5, label="$f(x)$")

    # ε 范围（红色水平带）
    ax.axhline(lim_val + eps, color="#ef4444", linestyle="--", alpha=0.6, linewidth=1.5)
    ax.axhline(lim_val - eps, color="#ef4444", linestyle="--", alpha=0.6, linewidth=1.5)
    ax.axvline(x0 + delta, color="#22c55e", linestyle="--", alpha=0.6, linewidth=1.5)
    ax.axvline(x0 - delta, color="#22c55e", linestyle="--", alpha=0.6, linewidth=1.5)

    # 标记极限点
    ax.scatter([x0], [lim_val], c="#f59e0b", s=120, zorder=10)

    ax.grid(alpha=GRID_ALPHA)
    ax.legend(loc="best", fontsize=11)
    ax.set_xlabel("$x$", fontsize=13)
    ax.set_ylabel("$f(x)$", fontsize=13)

    # 标注信息
    info_text = (
        f"$\\varepsilon = {eps:.2f}$\n"
        f"$\\delta = {delta:.4f}$\n"
        f"$\\lim_{{x \\to {x0}}}$ $f(x) = {lim_val:.4f}$\n"
    )
    ax.text(0.02, 0.95, info_text, transform=ax.transAxes, fontsize=11,
            verticalalignment="top",
            bbox=dict(boxstyle="round", facecolor="wheat", alpha=0.6))

    print(f"  ε = {eps:.4f}  推导 δ = {delta:.6f}")
    print(f"  x ∈ ({x0 - delta:.4f}, {x0 + delta:.4f})  ⟹  f(x) ∈ ({lim_val - eps:.4f}, {lim_val + eps:.4f})")

    if save:
        out.save_png(save)
        print(f"  图表已保存: {os.path.abspath(save)}")
    if show:
        out.show_jupyter()

    return out


def _numerical_delta(f_np, x0, lim_val, eps, step=0.001, max_delta=10):
    """数值方法推导 δ: 找到最大的 δ 使得 |f(x) - L| < ε 在 (x0-δ, x0+δ) 内成立。"""
    # 从大到小搜索
    for d in np.arange(max_delta, step, -step):
        left_ok = True
        right_ok = True
        # 检查左侧
        for sign in [-1, 1]:
            test_x = x0 + sign * d * 0.5
            try:
                fy = f_np(test_x)
                if not np.isfinite(fy) or abs(fy - lim_val) >= eps:
                    if sign == -1:
                        left_ok = False
                    else:
                        right_ok = False
            except (ValueError, OverflowError):
                if sign == -1:
                    left_ok = False
                else:
                    right_ok = False
        if left_ok and right_ok:
            return max(d * 0.9, step)
    return step


# ══════════════════════════════════════════════════════════════════════
# 6. 积分演示
# ══════════════════════════════════════════════════════════════════════

def plot_integral_demo(
    expr_str: str,
    a: float,
    b: float,
    n: int = 50,
    mode: str = "midpoint",
    save: str = None,
    show: bool = True,
    title: str = None,
):
    """绘制定积分的几何解释：曲线下面积 + 黎曼和矩形。

    参数
    ------
    expr_str : str
        被积函数
    a, b : float
        积分上下限
    n : int
        分割数
    mode : str
        求和模式
    save : str, optional
    show : bool
    title : str, optional

    示例
    ----
    >>> plot_integral_demo("x**2", 0, 1)
    >>> plot_integral_demo("sin(x)", 0, 3.14159, n=20, save="sin_integral.png")
    """
    validate_integral_bounds(a, b)
    f_sym = _parse_expr(expr_str)
    x = sp.Symbol("x")
    f_np = _to_numpy_func(expr_str)

    exact = float(sp.integrate(f_sym, (x, a, b)))
    dx = (b - a) / n

    if title is None:
        title = f"$\\int_{{{a}}}^{{{b}}}$ {expr_str} dx = {exact:.4f}"

    out = CASOutput(title=title, figsize=(10, 7))
    ax = out.ax

    xs = np.linspace(a, b, 1000)
    ys = f_np(xs)
    ax.plot(xs, ys, color="#2563eb", linewidth=2.5)

    # 填充面积
    ax.fill_between(xs, ys, alpha=0.3, color="#2563eb")

    # 黎曼和矩形
    for i in range(n):
        if mode == "left":
            xi = a + i * dx
        elif mode == "right":
            xi = a + (i + 1) * dx
        else:
            xi = a + (i + 0.5) * dx
        yi = f_np(xi)
        if np.isfinite(yi):
            rect_x = [a + i * dx, a + (i + 1) * dx, a + (i + 1) * dx, a + i * dx]
            rect_y = [0, 0, yi, yi]
            ax.fill(rect_x, rect_y, color="#10b981", alpha=0.3, linewidth=0.5, edgecolor="#059669")

    ax.axhline(0, color="#000", linewidth=0.5)
    ax.grid(alpha=GRID_ALPHA)
    ax.legend(loc="best", fontsize=11)
    ax.set_xlabel("$x$", fontsize=13)
    ax.set_ylabel("$f(x)$", fontsize=13)

    # 标注信息
    ax.text(0.02, 0.95, f"精确值: {exact:.6f}\nn={n}, mode={mode}",
            transform=ax.transAxes, fontsize=10,
            verticalalignment="top",
            bbox=dict(boxstyle="round", facecolor="wheat", alpha=0.5))

    if save:
        out.save_png(save)
        print(f"  图表已保存: {os.path.abspath(save)}")
    if show:
        out.show_jupyter()

    return out


# ══════════════════════════════════════════════════════════════════════
# 7. 动画演示（GIF）
# ══════════════════════════════════════════════════════════════════════

def animate_taylor(
    expr_str: str,
    x0: float,
    max_order: int = 10,
    x_range: tuple = None,
    save: str = None,
    frames: int = None,
    title: str = None,
):
    """生成泰勒展开阶数递增的动画 GIF。

    自动展示 1阶 → 2阶 → ... → max_order 阶的拟合效果变化。

    参数
    ------
    expr_str : str
        函数表达式
    x0 : float
        展开中心
    max_order : int
        最高阶数
    x_range : tuple, optional
    save : str
        输出 GIF 路径
    frames : int, optional
        总帧数。默认 = max_order + 1
    title : str, optional

    示例
    ----
    >>> animate_taylor("exp(x)", x0=0, max_order=10, save="taylor_anim.gif")
    >>> animate_taylor("sin(x)", x0=0, max_order=15, save="sin_taylor.gif")
    """
    f_sym = _parse_expr(expr_str)
    x = sp.Symbol("x")
    f_np = _to_numpy_func(expr_str)
    xr = _default_x_range(x0, x_range) if x_range else _default_x_range(x0)

    if frames is None:
        frames = min(max_order, 20) + 1

    if title is None:
        title = f"泰勒展开动画: {expr_str} at x={x0}"

    # 准备帧函数
    def make_frame(order):
        fig, ax = plt.subplots(figsize=(10, 7))
        from .styles import _apply
        _apply(get_active_theme())

        xs = np.linspace(*xr, 1000)
        orig_ys = f_np(xs)
        ax.plot(xs, orig_ys, color="#2563eb", linewidth=3, label="$f(x)$")

        if order > 0:
            taylor_expr = sp.series(f_sym, x, x0, n=order + 1).removeO()
            taylor_np = sp.lambdify(x, taylor_expr, "numpy")
            try:
                taylor_ys = taylor_np(xs)
                ax.plot(xs, taylor_ys, color="#ef4444", linewidth=2,
                        linestyle="--", label=f"{order}阶泰勒")
            except (ValueError, ZeroDivisionError, OverflowError):
                pass

        ax.scatter([x0], [f_np(x0)], c="black", s=80, zorder=10)
        ax.set_xlim(*xr)
        try:
            ax.set_ylim(min(orig_ys) * 0.9, max(orig_ys) * 1.1)
        except (ValueError, TypeError):
            ax.set_ylim(-5, 5)
        ax.set_title(f"$f(x)={expr_str}$, $x_0={x0}$, order={order}")
        ax.grid(alpha=GRID_ALPHA)
        ax.legend(loc="best", fontsize=11)

        fig.suptitle(f"泰勒展开动画: {expr_str} at x={x0} (阶数={order})")
        fig.tight_layout()
        return fig

    frames_list = [make_frame(i % (max_order + 1)) for i in range(frames)]

    out = CASOutput(title=title)
    result_path = out.export_frames_to_gif(frames_list, save or "taylor_anim.gif", interval_ms=500)
    print(f"  动画已保存: {os.path.abspath(result_path)}")

    return out


def animate_riemann(
    expr_str: str,
    a: float,
    b: float,
    n_list: list = None,
    mode: str = "midpoint",
    save: str = None,
    title: str = None,
):
    """生成 n 递增的黎曼和动画 GIF。

    参数
    ------
    expr_str : str
        被积函数
    a, b : float
        积分上下限
    n_list : list of int
        各帧使用的分割数。默认 [5, 10, 20, 50, 100, 200]
    mode : str
    save : str
    title : str, optional

    示例
    ----
    >>> animate_riemann("sin(x)", 0, 3.14159, save="riemann_anim.gif")
    >>> animate_riemann("x**2", 0, 1, n_list=[4, 8, 16, 32, 64], save="x2_riemann.gif")
    """
    if n_list is None:
        n_list = [5, 10, 20, 50, 100, 200]

    f_sym = _parse_expr(expr_str)
    x = sp.Symbol("x")
    f_np = _to_numpy_func(expr_str)
    exact = float(sp.integrate(f_sym, (x, a, b)))

    if title is None:
        title = f"黎曼和动画: \\int_{{{a}}}^{{{b}}} {expr_str} dx"

    def make_frame(n):
        fig, ax = plt.subplots(figsize=(10, 7))
        from .styles import _apply
        _apply(get_active_theme())

        xs = np.linspace(a, b, 1000)
        ax.plot(xs, f_np(xs), color="#2563eb", linewidth=2.5)
        ax.fill_between(xs, f_np(xs), alpha=0.2, color="#2563eb")

        dx = (b - a) / n
        colors = ["#10b981", "#34d399", "#6ee7b7", "#a7f3d0"]
        for i in range(n):
            if mode == "left":
                xi = a + i * dx
            elif mode == "right":
                xi = a + (i + 1) * dx
            else:
                xi = a + (i + 0.5) * dx
            yi = f_np(xi)
            if np.isfinite(yi):
                rect_x = [a + i * dx, a + (i + 1) * dx, a + (i + 1) * dx, a + i * dx]
                rect_y = [0, 0, yi, yi]
                ax.fill(rect_x, rect_y, color=colors[i % len(colors)], alpha=0.5)

        approx = np.sum(f_np(np.array([a + (i + 0.5) * dx for i in range(n)])) * dx)
        ax.set_title(f"n={n:4d}, 近似值={approx:.6f}, 精确值={exact:.6f}, 误差={abs(approx-exact):.6f}")
        ax.set_xlim(a, b)
        ax.grid(alpha=GRID_ALPHA)
        ax.set_xlabel("$x$")
        ax.set_ylabel("$f(x)$")
        fig.suptitle(title)
        fig.tight_layout()
        return fig

    frames_list = [make_frame(n) for n in n_list]

    out = CASOutput(title=title)
    result_path = out.export_frames_to_gif(frames_list, save or "riemann_anim.gif", interval_ms=400)
    print(f"  动画已保存: {os.path.abspath(result_path)}")

    return out


# ══════════════════════════════════════════════════════════════════════
# 8. 快捷 LaTeX 导出
# ══════════════════════════════════════════════════════════════════════

def to_latex(expr_str: str) -> str:
    """将表达式转换为 LaTeX 字符串。

    参数
    ------
    expr_str : str
        数学表达式字符串

    返回
    ------
    str
        LaTeX 代码片段

    示例
    ----
    >>> to_latex("x**2 + 2*x + 1")
    'x^{2} + 2 x + 1'
    >>> to_latex("sin(x)/x")
    '\\frac{\\sin{\\left(x \\right)}}{x}'
    """
    return latex_fragment(expr_str)


# ══════════════════════════════════════════════════════════════════════
# 9. 统一绘图接口
# ══════════════════════════════════════════════════════════════════════

def plot_math(
    kind: str,
    *args,
    save: str = None,
    show: bool = True,
    **kwargs,
):
    """统一数学绘图入口。根据 kind 自动路由到对应函数。

    参数
    ------
    kind : str
        "limit", "derivative", "riemann", "integral", "taylor", "eps_delta"
    *args
        传递给对应函数的位置参数
    save : str, optional
        输出路径（传递给对应函数）
    show : bool
        是否显示（传递给对应函数）
    **kwargs
        传递给对应函数的其余参数

    示例
    ----
    >>> plot_math("limit", "sin(x)/x", x0=0, save="limit.png")
    >>> plot_math("taylor", "exp(x)", x0=0, order=5, save="taylor.png")
    >>> plot_math("eps_delta", "sin(x)/x", x0=0, eps=0.1, save="eps_delta.png")
    """
    routing = {
        "limit": plot_limit_demo,
        "derivative": plot_derivative_demo,
        "riemann": plot_riemann_demo,
        "integral": plot_integral_demo,
        "taylor": plot_taylor_demo,
        "eps_delta": show_epsilon_delta_demo,
    }
    func = routing.get(kind.lower())
    if func is None:
        raise CASValidationError(
            message=f"未知的绘图类型: {kind}",
            teaching_hint=f"支持的类型: {', '.join(sorted(routing.keys()))}",
            solution="请使用支持的绘图类型，例如 'limit', 'taylor', 'eps_delta'",
        )
    return func(*args, save=save, show=show, **kwargs)
