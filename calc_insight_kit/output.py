# -*- coding: utf-8 -*-
"""
统一输出层 — 一套调用，多种输出格式。

支持：
  - 静态 PNG
  - GIF 动画
  - LaTeX 公式片段
  - Jupyter notebook 内联渲染

用法：
    from calc_insight_kit.output import CASOutput

    out = CASOutput("sin(x)")
    out.save_png("output.png")           # 保存为图片
    out.save_gif("anim.gif", frames=30)  # 保存为动画
    latex_str = out.to_latex()            # 获取 LaTeX
    out.show_jupyter()                    # 在 Jupyter 中内联显示
"""
import io
import base64
import os
from pathlib import Path
from typing import Optional, List, Union, Callable

try:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import matplotlib.animation as animation
    _HAS_MPL = True
except ImportError:
    _HAS_MPL = False

try:
    from IPython.display import display, Image, Latex
    _HAS_IPYTHON = True
except ImportError:
    _HAS_IPYTHON = False


def _ensure_matplotlib():
    if not _HAS_MPL:
        raise ImportError(
            "matplotlib is required for output features. "
            "Install it: pip install matplotlib"
        )


class CASOutput:
    """统一输出对象。封装 matplotlib 图形，提供 PNG / GIF / LaTeX / Jupyter 四种输出方式。

    参数
    ------
    fig : matplotlib.figure.Figure, optional
        已有的 Figure 对象。如果为 None，将自动创建新 Figure。
    ax : matplotlib.axes.Axes, optional
        已有的 Axes 对象。
    title : str, optional
        图表标题。

    示例
    ----
    >>> from calc_insight_kit.output import CASOutput
    >>> import numpy as np
    >>> out = CASOutput(title="y = sin(x)")
    >>> ax = out.ax
    >>> ax.plot(np.linspace(-3, 3, 200), np.sin(np.linspace(-3, 3, 200)))
    >>> out.save_png("sin_plot.png")
    """

    def __init__(
        self,
        fig=None,
        ax=None,
        title: str = "",
        figsize=None,
    ):
        _ensure_matplotlib()
        if fig is not None and ax is not None:
            self.fig = fig
            self.ax = ax
        else:
            import matplotlib.pyplot as plt
            if figsize is None:
                from .config import FIG_SIZE
                figsize = FIG_SIZE
            self.fig, self.ax = plt.subplots(figsize=figsize)
        if title:
            self.fig.suptitle(title, fontsize=16)

    # ── PNG ───────────────────────────────────────────────────────────

    def save_png(
        self,
        path: str,
        dpi: Optional[int] = None,
        transparent: bool = False,
    ) -> str:
        """保存为 PNG 图片，返回绝对路径。

        参数
        ------
        path : str
            输出文件路径（.png）。
        dpi : int, optional
            分辨率。默认为当前主题设置值。
        transparent : bool
            是否使用透明背景。
        """
        _ensure_matplotlib()
        if dpi is None:
            from .config import DPI
            dpi = DPI
        self.fig.tight_layout()
        self.fig.savefig(
            path, dpi=dpi, transparent=transparent,
            bbox_inches="tight",
        )
        plt.close(self.fig)
        return os.path.abspath(path)

    # ── GIF 动画 ──────────────────────────────────────────────────────

    def save_gif(
        self,
        path: str,
        frame_func,
        frames: int = 30,
        interval_ms: int = 50,
        dpi: Optional[int] = None,
    ) -> str:
        """生成 GIF 动画并保存。

        参数
        ------
        path : str
            输出文件路径（.gif）。
        frame_func : callable
            接受帧索引 (int) -> None 的函数。
            应在内部操作 self.ax 进行绘图，不调用 plt.show()。
        frames : int
            总帧数。
        interval_ms : int
            每帧间隔（毫秒）。
        dpi : int, optional
            分辨率。

        示例
        ----
        >>> def draw_frame(i):
        ...     ax = out.ax
        ...     ax.clear()
        ...     x = np.linspace(0, 2*np.pi, 200)
        ...     ax.plot(x, np.sin(x + i*0.2))
        >>> out.save_gif("wave.gif", frame_func=draw_frame, frames=20)
        """
        _ensure_matplotlib()
        if dpi is None:
            from .config import DPI
            dpi = DPI

        if isinstance(path, str) and not path.endswith(".gif"):
            path = path + ".gif"

        anim = animation.FuncAnimation(
            self.fig,
            frame_func,
            frames=frames,
            interval=interval_ms,
            repeat=True,
        )
        anim.save(path, writer="pillow", fps=1000 // max(interval_ms, 1))
        plt.close(self.fig)
        return os.path.abspath(path)

    # ── LaTeX ─────────────────────────────────────────────────────────

    def to_latex(self, expr=None) -> str:
        """将表达式转换为 LaTeX 字符串。

        参数
        ------
        expr : str, optional
            数学表达式。如果为 None，尝试从当前 Axes 中读取数据
            并返回占位符描述。

        返回
        ------
        str
            LaTeX 代码片段。
        """
        try:
            import sympy as sp
            if expr is not None:
                sym_expr = sp.sympify(expr)
                return sp.latex(sym_expr)
            else:
                # 尝试从 Axes 标题中提取信息
                title = self.fig._suptitle.get_text() if self.fig._suptitle else ""
                return f"\\text{{{title}}}"
        except Exception:
            return "\\text{LaTeX 转换失败}"

    # ── Jupyter 内联 ──────────────────────────────────────────────────

    def show_jupyter(self) -> None:
        """在 Jupyter notebook 中内联渲染图表。

        仅在 Jupyter 环境中生效，非 Jupyter 环境自动降级为静默。
        """
        if not _HAS_IPYTHON:
            print("IPython 未安装，跳过 Jupyter 内联渲染。")
            print("调用 save_png() 保存为图片文件。")
            return
        from io import BytesIO
        buf = BytesIO()
        self.fig.savefig(buf, format="png", bbox_inches="tight")
        buf.seek(0)
        display(Image(data=buf.read()))

    # ── 工具 ──────────────────────────────────────────────────────────

    def close(self):
        """关闭图形，释放内存。"""
        _ensure_matplotlib()
        plt.close(self.fig)

    @staticmethod
    def export_frames_to_gif(
        frames: List[Callable[[], None]],
        path: str,
        interval_ms: int = 50,
        dpi: Optional[int] = None,
    ) -> str:
        """从帧函数列表生成 GIF。

        参数
        ------
        frames : list of callables
            每个 callable 返回一个 matplotlib Figure。
        path : str
            输出路径（.gif）。
        interval_ms : int
            帧间隔。
        dpi : int
            分辨率。

        示例
        ----
        >>> frames = []
        >>> for i in range(10):
        ...     fig, ax = plt.subplots()
        ...     ax.plot(np.sin(x + i*0.3))
        ...     frames.append(lambda: None)  # 实际应操作 fig
        >>> CASOutput.export_frames_to_gif(frames, "anim.gif")
        """
        _ensure_matplotlib()
        from .styles import get_active_theme
        theme = get_active_theme()

        if isinstance(path, str) and not path.endswith(".gif"):
            path = path + ".gif"
        if dpi is None:
            from .config import DPI
            dpi = DPI

        # 将每帧保存为临时 PNG，再用 Pillow 合成 GIF
        tmp_dir = os.path.join(os.path.dirname(path), ".tmp_frames")
        os.makedirs(tmp_dir, exist_ok=True)
        try:
            from PIL import Image
            tmp_paths = []
            for i, frame_func in enumerate(frames):
                fig = frame_func()
                tmp_path = os.path.join(tmp_dir, f"frame_{i:04d}.png")
                fig.savefig(tmp_path, dpi=dpi, bbox_inches="tight")
                plt.close(fig)
                tmp_paths.append(tmp_path)

            if tmp_paths:
                imgs = [Image.open(p) for p in tmp_paths]
                if len(imgs) > 1:
                    imgs[0].save(
                        path, save_all=True, append_images=imgs[1:],
                        duration=interval_ms, loop=0,
                    )
                else:
                    imgs[0].save(path)
        finally:
            # 清理临时文件
            for p in tmp_paths:
                try:
                    os.remove(p)
                except OSError:
                    pass
            try:
                os.rmdir(tmp_dir)
            except OSError:
                pass

        return os.path.abspath(path)


def save_plot(
    fig,
    ax=None,
    path: str = None,
    title: str = "",
    format: str = "png",
    dpi: Optional[int] = None,
) -> str:
    """快捷函数：直接保存一个 matplotlib 图形。

    参数
    ------
    fig : matplotlib.figure.Figure
        要保存的 Figure。
    path : str
        输出路径。
    title : str
        标题。
    format : str
        "png", "pdf", "svg", "gif"。
    dpi : int, optional

    返回
    ------
    str
        输出文件的绝对路径。
    """
    _ensure_matplotlib()
    if dpi is None:
        from .config import DPI
        dpi = DPI

    if format == "png":
        fig.savefig(path, dpi=dpi, bbox_inches="tight")
    elif format == "pdf":
        fig.savefig(path, bbox_inches="tight")
    elif format == "svg":
        fig.savefig(path, bbox_inches="tight")
    else:
        raise ValueError(f"不支持的格式: {format}，支持: png, pdf, svg, gif")
    plt.close(fig)
    return os.path.abspath(path)


def latex_fragment(expr) -> str:
    """将 sympy 表达式或字符串转换为 LaTeX 片段。

    用法：
        latex_fragment("x**2 + 1")
        latex_fragment(sp.sin(sp.Symbol("x")))
    """
    try:
        import sympy as sp
        sym = sp.sympify(expr)
        return sp.latex(sym)
    except Exception:
        return "\\text{转换失败}"
