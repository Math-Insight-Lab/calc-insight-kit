# -*- coding: utf-8 -*-
"""
跨平台配置工具 V1.2.0
自动适配 Windows/Linux/macOS 的字体、后端、路径
"""
import sys
import matplotlib

# ===== 自动设置 matplotlib 后端（避免无显示器时报错）=====
try:
    import matplotlib
    matplotlib.use("Agg")
except ImportError:
    pass

# ===== 跨平台字体自动选择 =====
def get_font_family():
    """根据操作系统返回最佳中文字体族"""
    plat = sys.platform.lower()
    
    if plat.startswith("linux"):
        return [
            "Noto Sans CJK SC",
            "Noto Sans CJK TC",
            "Noto Sans CJK HK",
            "Noto Sans CJK JP",
            "Noto Sans CJK KR",
            "WenQuanYi Micro Hei",
            "WenQuanYi Zen Hei",
            "Droid Sans Fallback",
            "DejaVu Sans",
        ]
    elif plat.startswith("darwin"):
        # macOS
        return [
            "PingFang SC",
            "PingFang TC",
            "PingFang HK",
            "Heiti SC",
            "STHeiti",
            "SimHei",
            "Arial Unicode MS",
            "Helvetica Neue",
        ]
    else:
        # Windows (win32 / cygwin)
        return [
            "Microsoft YaHei",    # 微软雅黑
            "SimHei",             # 黑体
            "Microsoft JhengHei", # 微软正黑
            "FangSong",           # 仿宋
            "KaiTi",              # 楷体
            "Arial Unicode MS",
            "DejaVu Sans",
        ]

def setup_matplotlib():
    """配置 matplotlib 全局参数（跨平台）"""
    import matplotlib.pyplot as plt
    
    fonts = get_font_family()
    plt.rcParams["font.sans-serif"] = fonts
    plt.rcParams["axes.unicode_minus"] = False
    plt.rcParams["figure.dpi"] = 100
    plt.rcParams["savefig.dpi"] = 100
    plt.rcParams["font.size"] = 12
    plt.rcParams["axes.titlesize"] = 14
    plt.rcParams["axes.labelsize"] = 12

