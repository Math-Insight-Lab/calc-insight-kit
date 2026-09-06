# -*- coding: utf-8 -*-
"""
Calc Insight Kit 核心库入口
三层差异化微积分可视化工具库 V1.0.0

用法
----
# 底层 CAS
>>> from calc_insight_kit import get_cas_backend
>>> backend = get_cas_backend()
>>> backend.diff("x**2", "x")

# 教学薄包装 API（一行出图）
>>> from calc_insight_kit import plot_limit_demo
>>> plot_limit_demo("sin(x)/x", x0=0, save="limit.png")

# 统一输出层
>>> from calc_insight_kit.output import CASOutput
>>> out = CASOutput(title="Hello")
>>> out.ax.plot([1,2,3], [1,4,9])
>>> out.save_png("output.png")
>>> out.save_gif("anim.gif", frames=20)

# 主题预设
>>> from calc_insight_kit.styles import use_theme
>>> use_theme("teaching")  # 或 "paper"

# 教学报错
>>> from calc_insight_kit.errors import validate_positive
>>> validate_positive(-1, "epsilon")  # 抛出 CASValidationError 并附教学提示
"""

__version__ = "1.0.0"

# ── 底层 CAS ─────────────────────────────────────────────────────────
from .calc_backend import get_cas_backend, limit_epsilon_delta
from .calc_backend import SympyBackend, MaximaBackend

# ── CAS 子包 ─────────────────────────────────────────────────────────
from .cas import CASSymbol, CASExpr

# ── 可视化底层 ───────────────────────────────────────────────────────
from .visual_tools import (
    derivative_plot_data,
    plot_derivative_tangent,
    riemann_sum_calc,
    plot_riemann_sum,
    taylor_expand,
    plot_taylor_series,
    plot_epsilon_delta_limit,
)

# ── 配置 ─────────────────────────────────────────────────────────────
from .config import (
    RUN_KID_MODE,
    RUN_MIDDLE_MODE,
    RUN_UNIVERSITY_MODE,
    ENABLE_EPS_DELTA,
    FIG_SIZE,
    DPI,
)

# ── 主题预设 ─────────────────────────────────────────────────────────
from .styles import (
    use_theme,
    use_theme_context,
    get_active_theme,
    _apply,
)

# ── 统一输出层 ───────────────────────────────────────────────────────
from .output import (
    CASOutput,
    save_plot,
    latex_fragment,
)

# ── 教学报错 ─────────────────────────────────────────────────────────
from .errors import (
    CASBaseError,
    CASValidationError,
    CASComputationalError,
    CASVisualizationError,
    CASBackendError,
    validate_positive,
    validate_non_negative,
    validate_range,
    validate_limit_context,
    validate_derivative_context,
    validate_riemann_params,
    validate_taylor_params,
    validate_integral_bounds,
    validate_epsilon_delta_demo_params,
    validate_plot_bounds,
    handle_cas_errors,
)

# ── 教学薄包装 API（一行出图）────────────────────────────────────────
from .teacher_api import (
    # 极限 / 导数 / 积分
    plot_limit_demo,
    plot_derivative_demo,
    plot_integral_demo,
    # 级数
    plot_taylor_demo,
    animate_taylor,
    # 黎曼和
    plot_riemann_demo,
    animate_riemann,
    # ε-δ 严格定义
    show_epsilon_delta_demo,
    # LaTeX
    to_latex,
    # 统一入口
    plot_math,
)

__all__ = [
    # 版本
    "__version__",
    # 底层 CAS
    "get_cas_backend",
    "limit_epsilon_delta",
    "SympyBackend",
    "MaximaBackend",
    # CAS 子包
    "CASSymbol",
    "CASExpr",
    # 可视化底层
    "derivative_plot_data",
    "plot_derivative_tangent",
    "riemann_sum_calc",
    "plot_riemann_sum",
    "taylor_expand",
    "plot_taylor_series",
    "plot_epsilon_delta_limit",
    # 配置
    "RUN_KID_MODE",
    "RUN_MIDDLE_MODE",
    "RUN_UNIVERSITY_MODE",
    "ENABLE_EPS_DELTA",
    "FIG_SIZE",
    "DPI",
    # 主题
    "use_theme",
    "use_theme_context",
    "get_active_theme",
    "_apply",
    # 输出层
    "CASOutput",
    "save_plot",
    "latex_fragment",
    # 报错
    "CASBaseError",
    "CASValidationError",
    "CASComputationalError",
    "CASVisualizationError",
    "CASBackendError",
    "validate_positive",
    "validate_non_negative",
    "validate_range",
    "validate_limit_context",
    "validate_derivative_context",
    "validate_riemann_params",
    "validate_taylor_params",
    "validate_integral_bounds",
    "validate_epsilon_delta_demo_params",
    "validate_plot_bounds",
    "handle_cas_errors",
    # 教学薄包装 API
    "plot_limit_demo",
    "plot_derivative_demo",
    "plot_integral_demo",
    "plot_taylor_demo",
    "animate_taylor",
    "plot_riemann_demo",
    "animate_riemann",
    "show_epsilon_delta_demo",
    "to_latex",
    "plot_math",
]
