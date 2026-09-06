# -*- coding: utf-8 -*-
"""
三层层级差异化校验测试
"""
from calc_insight_kit.config import RUN_KID_MODE, RUN_MIDDLE_MODE, RUN_UNIVERSITY_MODE

def test_layer_switch():
    assert isinstance(RUN_KID_MODE, bool)
    assert isinstance(RUN_MIDDLE_MODE, bool)
    assert isinstance(RUN_UNIVERSITY_MODE, bool)
