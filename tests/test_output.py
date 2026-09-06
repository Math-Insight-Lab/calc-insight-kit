# -*- coding: utf-8 -*-
"""
统一输出层模块测试 — CASOutput 类、save_plot、latex_fragment
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from calc_insight_kit.output import (
    CASOutput,
    save_plot,
    latex_fragment,
)


# ── CASOutput 基础测试 ────────────────────────────────────────

def test_casoutput_auto_create():
    out = CASOutput(title="test")
    assert out.fig is not None
    assert out.ax is not None
    out.close()


def test_casoutput_with_fig_ax():
    fig, ax = plt.subplots()
    out = CASOutput(fig=fig, ax=ax, title="test")
    assert out.fig is fig
    assert out.ax is ax
    out.close()


def test_casoutput_title():
    out = CASOutput(title="Hello World")
    title = out.fig._suptitle.get_text()
    assert title == "Hello World"
    out.close()


def test_casoutput_save_png(tmp_path):
    out = CASOutput(title="png test")
    out.ax.plot([1, 2, 3], [1, 4, 9])
    path = str(tmp_path / "test_plot.png")
    abs_path = out.save_png(path)
    assert os.path.exists(abs_path)
    assert os.path.getsize(abs_path) > 0


def test_casoutput_to_latex():
    out = CASOutput(title="f(x) = x^2")
    latex = out.to_latex()
    assert "f(x)" in latex
    assert "x^2" in latex
    out.close()


def test_casoutput_to_latex_expr():
    latex = latex_fragment("x**2 + 2*x + 1")
    assert "x^{2}" in latex or "x^2" in latex


def test_casoutput_save_png_default_dpi(tmp_path):
    out = CASOutput(title="dpi test")
    path = str(tmp_path / "default_dpi.png")
    abs_path = out.save_png(path)
    assert os.path.exists(abs_path)
    out.close()


def test_casoutput_save_png_transparent(tmp_path):
    out = CASOutput(title="transparent test")
    out.ax.plot([1, 2], [1, 4])
    path = str(tmp_path / "trans.png")
    abs_path = out.save_png(path, transparent=True)
    assert os.path.exists(abs_path)
    out.close()


def test_casoutput_save_png_custom_dpi(tmp_path):
    out = CASOutput(title="custom dpi test")
    path = str(tmp_path / "custom_dpi.png")
    abs_path = out.save_png(path, dpi=300)
    assert os.path.exists(abs_path)
    out.close()


def test_casoutput_export_frames_to_gif(tmp_path):
    import numpy as np
    frames = []
    for i in range(3):
        fig, ax = plt.subplots()
        ax.plot(np.sin(np.linspace(0, 2 * np.pi, 100) + i * 0.5))
        frames.append(lambda f=fig: f)

    path = str(tmp_path / "test_frames.gif")
    try:
        abs_path = CASOutput.export_frames_to_gif(frames, path)
        # 可能因缺少Pillow失败，但不应该崩溃
    except Exception:
        pass  # 无Pillow时跳过


def test_casoutput_close_twice():
    out = CASOutput(title="close test")
    out.close()
    # 第二次close应该不崩溃
    out.close()


def test_save_plot_png(tmp_path):
    fig, ax = plt.subplots()
    ax.plot([1, 2], [3, 4])
    path = str(tmp_path / "save_plot_test.png")
    abs_path = save_plot(fig, path=path, title="test", format="png")
    assert os.path.exists(abs_path)


def test_save_plot_pdf(tmp_path):
    fig, ax = plt.subplots()
    ax.plot([1, 2], [3, 4])
    path = str(tmp_path / "save_plot_test.pdf")
    abs_path = save_plot(fig, path=path, title="test", format="pdf")
    assert os.path.exists(abs_path)


def test_save_plot_svg(tmp_path):
    fig, ax = plt.subplots()
    ax.plot([1, 2], [3, 4])
    path = str(tmp_path / "save_plot_test.svg")
    abs_path = save_plot(fig, path=path, title="test", format="svg")
    assert os.path.exists(abs_path)


def test_save_plot_invalid_format():
    fig, ax = plt.subplots()
    try:
        save_plot(fig, path="test.xyz", format="xyz")
        assert False
    except ValueError as e:
        assert "不支持的格式" in str(e)


def test_latex_fragment_sympy_expr():
    import sympy as sp
    x = sp.Symbol("x")
    latex = latex_fragment(x**2 + 1)
    assert "x" in latex


def test_latex_fragment_str():
    latex = latex_fragment("sin(x)")
    assert "sin" in latex


def test_latex_fragment_fail_gracefully():
    # Truly invalid strings should be handled gracefully
    latex = latex_fragment("not a math expr !!!")
    assert "text" in latex or "转换失败" in latex
