# -*- coding: utf-8 -*-
"""
可视化输出有效性测试
"""
import os
from calc_insight_kit import plot_epsilon_delta_limit
import numpy as np

def test_visual_save():
    def f(x): return np.sin(x)/x
    path = "test_visual_temp.png"
    plot_epsilon_delta_limit(f, (-2,2), 0, 1.0, 0.2, 0.24, path)
    assert os.path.exists(path)
    os.remove(path)
