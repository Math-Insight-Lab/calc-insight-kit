# -*- coding: utf-8 -*-
"""
全局样式预设 — 解决 Matplotlib 中文乱码、负号、配色混乱等高频踩坑。

提供两套主题：
  - "teaching"（教学课件风格）：大字号、粗边框、高对比度，适合 PPT / 投影
  - "paper"（论文风格）：紧凑、黑白友好、细线条，适合打印 / 论文插图

用法：
    from calc_insight_kit.styles import use_theme
    use_theme("teaching")   # 全局切换
    # 或使用上下文管理器，不影响全局：
    with use_theme("paper"):
        plot_some_math()    # 此块内使用 paper 主题
"""
import matplotlib
import matplotlib.pyplot as plt
from contextlib import contextmanager
import sys

# ── 跨平台中文字体回退 ──────────────────────────────────────────────
def _get_cjk_fonts():
    """根据操作系统返回最佳中文字体族，与 platform_utils 保持一致。"""
    plat = sys.platform.lower()
    if plat.startswith("linux"):
        return [
            "Noto Sans CJK SC", "Noto Sans CJK TC", "Noto Sans CJK HK",
            "Noto Sans CJK JP", "Noto Sans CJK KR", "WenQuanYi Micro Hei",
            "WenQuanYi Zen Hei", "Droid Sans Fallback", "DejaVu Sans",
        ]
    elif plat.startswith("darwin"):
        return [
            "PingFang SC", "PingFang TC", "PingFang HK", "Heiti SC",
            "STHeiti", "SimHei", "Arial Unicode MS", "Helvetica Neue",
        ]
    else:
        return [
            "Microsoft YaHei", "SimHei", "Microsoft JhengHei",
            "FangSong", "KaiTi", "Arial Unicode MS", "DejaVu Sans",
        ]

# ── 主题定义 ────────────────────────────────────────────────────────

THEMES = {
    "teaching": {
        # 字号
        "font.size": 14,
        "axes.titlesize": 18,
        "axes.labelsize": 14,
        "xtick.labelsize": 12,
        "ytick.labelsize": 12,
        "legend.fontsize": 12,
        "figure.titlesize": 20,
        # 字体
        "font.sans-serif": _get_cjk_fonts(),
        "axes.unicode_minus": False,
        # 线条
        "lines.linewidth": 2.5,
        "lines.markersize": 8,
        "patch.linewidth": 2,
        # 网格
        "grid.alpha": 0.4,
        "grid.linestyle": "--",
        # 边框
        "axes.linewidth": 1.5,
        "axes.spines.top": True,
        "axes.spines.right": True,
        # 颜色（高对比度，适合投影）
        "axes.prop_cycle": plt.cycler("color", [
            "#1f77b4",  # 蓝
            "#ff7f0e",  # 橙
            "#2ca02c",  # 绿
            "#d62728",  # 红
            "#9467bd",  # 紫
            "#e377c2",  # 粉
            "#8c564b",  # 棕
            "#7f7f7f",  # 灰
        ]),
        # 画布
        "figure.dpi": 120,
        "savefig.dpi": 150,
        "savefig.bbox": "tight",
        "savefig.pad_inches": 0.3,
    },
    "paper": {
        # 字号
        "font.size": 11,
        "axes.titlesize": 13,
        "axes.labelsize": 11,
        "xtick.labelsize": 10,
        "ytick.labelsize": 10,
        "legend.fontsize": 10,
        "figure.titlesize": 14,
        # 字体
        "font.sans-serif": _get_cjk_fonts(),
        "axes.unicode_minus": False,
        # 线条（细，适合打印）
        "lines.linewidth": 1.5,
        "lines.markersize": 5,
        "patch.linewidth": 1,
        # 网格
        "grid.alpha": 0.2,
        "grid.linestyle": ":",
        # 边框
        "axes.linewidth": 1.0,
        "axes.spines.top": False,
        "axes.spines.right": False,
        # 颜色（黑白友好）
        "axes.prop_cycle": plt.cycler("color", [
            "#000000", "#555555", "#888888", "#aaaaaa",
            "#1f77b4", "#ff7f0e", "#2ca02c", "#d62728",
        ]),
        # 画布（紧凑）
        "figure.dpi": 100,
        "savefig.dpi": 200,
        "savefig.bbox": "tight",
        "savefig.pad_inches": 0.15,
    },
}

# ── 当前状态 ────────────────────────────────────────────────────────

_active_theme = "teaching"   # 默认教学主题

# ── 公共 API ────────────────────────────────────────────────────────

def use_theme(theme_name: str):
    """全局切换绘图主题。

    参数
    ------
    theme_name : str
        "teaching"（教学课件风格，默认）或 "paper"（论文风格）。

    示例
    ----
    >>> from calc_insight_kit.styles import use_theme
    >>> use_theme("teaching")          # 后续所有 plot 都使用教学风格
    """
    global _active_theme
    if theme_name not in THEMES:
        raise ValueError(
            f"未知主题 '{theme_name}'，可选: {', '.join(sorted(THEMES))}"
        )
    _active_theme = theme_name
    _apply(_active_theme)


def get_active_theme() -> str:
    """返回当前活跃的主题名称。"""
    return _active_theme


def reset_theme():
    """恢复 matplotlib 默认参数，取消任何主题设置。"""
    global _active_theme
    _active_theme = "default"
    plt.rcdefaults()


@contextmanager
def use_theme_context(theme_name: str):
    """上下文管理器：临时切换主题，退出后恢复。

    示例
    ----
    >>> with use_theme_context("paper"):
    ...     plot_figure()
    # 这里恢复为教学主题
    """
    global _active_theme
    old = _active_theme
    use_theme(theme_name)
    try:
        yield
    finally:
        use_theme(old)


def _apply(theme_name: str):
    """将指定主题应用到 matplotlib 全局 rcParams。"""
    import matplotlib.pyplot as plt
    params = THEMES[theme_name]
    for key, value in params.items():
        plt.rcParams[key] = value
    # 自动设置后端（避免无显示器时报错）
    try:
        matplotlib.use("Agg")
    except ImportError:
        pass
