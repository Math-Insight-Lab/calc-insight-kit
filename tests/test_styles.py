# -*- coding: utf-8 -*-
"""
全局样式预设模块测试
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from calc_insight_kit.styles import (
    use_theme,
    get_active_theme,
    reset_theme,
    use_theme_context,
    THEMES,
    _apply,
)


def test_themes_exist():
    assert "teaching" in THEMES
    assert "paper" in THEMES


def test_use_theme_applies():
    reset_theme()
    use_theme("teaching")
    assert get_active_theme() == "teaching"
    assert plt.rcParams["font.size"] == 14

    use_theme("paper")
    assert get_active_theme() == "paper"
    assert plt.rcParams["font.size"] == 11
    reset_theme()


def test_use_theme_invalid():
    try:
        use_theme("nonexistent")
        assert False, "Should have raised ValueError"
    except ValueError as e:
        assert "nonexistent" in str(e)
    reset_theme()


def test_reset_theme():
    use_theme("teaching")
    reset_theme()
    # matplotlib defaults
    default_fontsize = plt.rcParamsOrig.get("font.size", 10)
    # Just check it doesn't raise
    plt.rcdefaults()


def test_use_theme_context():
    use_theme("teaching")
    assert get_active_theme() == "teaching"
    with use_theme_context("paper"):
        assert get_active_theme() == "paper"
    assert get_active_theme() == "teaching"


def test_teaching_theme_properties():
    use_theme("teaching")
    params = THEMES["teaching"]
    assert params["font.size"] == 14
    assert params["axes.titlesize"] == 18
    assert params["lines.linewidth"] == 2.5
    assert params["figure.dpi"] == 120


def test_paper_theme_properties():
    use_theme("paper")
    params = THEMES["paper"]
    assert params["font.size"] == 11
    assert params["lines.linewidth"] == 1.5
    assert params["figure.dpi"] == 100
    assert params["axes.spines.top"] is False
    assert params["axes.spines.right"] is False
