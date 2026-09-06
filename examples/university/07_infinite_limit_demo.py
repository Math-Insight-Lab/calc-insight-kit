# -*- coding: utf-8 -*-
"""
大学层 - 无穷极限与第二类间断点严谨判定
适配数分：无穷极限定义、第二类间断点分类、渐近线数学证明
"""
import sympy as sp
import numpy as np
import matplotlib.pyplot as plt
from calc_insight_kit.config import FIG_SIZE, DPI, GRID_ALPHA
from calc_insight_kit.calc_backend import get_cas_backend

def main():
    from calc_insight_kit.platform_utils import setup_matplotlib
    setup_matplotlib()
    backend = get_cas_backend()
    x = sp.Symbol("x")
    f = 1 / (x - 1)
    x0 = 1

    print("===== \u5927\u5b66\u5c42\u00b7\u65e0\u7a77\u6781\u9650\u4e0e\u7b2c\u4e8c\u7c7b\u95f4\u65ad\u70b9\u5224\u5b9a =====")
    # 严格单侧无穷极限求解
    lim_left = backend.limit(f, x, x0, "-")
    lim_right = backend.limit(f, x, x0, "+")
    print(f"x\u21921- \u6781\u9650\uff1a{lim_left}")
    print(f"x\u21921+ \u6781\u9650\uff1a{lim_right}")
    print("\u5224\u5b9a\u7ed3\u679c\uff1a\u53cc\u4fa7\u6781\u9650\u5747\u4e3a\u65e0\u7a77\u5927\uff0c\u8be5\u70b9\u4e3a\u3010\u65e0\u7a77\u95f4\u65ad\u70b9\uff08\u7b2c\u4e8c\u7c7b\u95f4\u65ad\u70b9\uff09\u3011")
    print("\u6e10\u8fd1\u7ebf\u8bc1\u660e\uff1a\u76f4\u7ebfx=1\u4e3a\u51fd\u6570\u5782\u76f4\u6e10\u8fd1\u7ebf")

    # 可视化绘制
    x1 = np.linspace(-2, 0.95, 600)
    x2 = np.linspace(1.05, 4, 600)
    y1 = 1 / (x1 - 1)
    y2 = 1 / (x2 - 1)

    plt.figure(figsize=FIG_SIZE)
    plt.plot(x1, y1, color="#d35400", linewidth=1.8, label="f(x)=1/(x-1)")
    plt.plot(x2, y2, color="#d35400", linewidth=1.8)
    plt.axvline(x=1, color="#2c3e50", ls="--", label="\u5782\u76f4\u6e10\u8fd1\u7ebf x=1")
    plt.ylim(-15, 15)
    plt.grid(alpha=GRID_ALPHA)
    plt.legend()
    plt.title("\u6570\u5206\u4e25\u8c28\u5206\u6790\uff1a\u65e0\u7a77\u6781\u9650\u4e0e\u7b2c\u4e8c\u7c7b\u95f4\u65ad\u70b9")
    plt.tight_layout()
    plt.savefig("university_infinite_limit.png", dpi=DPI)
    plt.close()
    print("\n\u2705 \u5927\u5b66\u65e0\u7a77\u6781\u9650\u4e25\u8c28\u5224\u5b9a\u6f14\u793a\u5b8c\u6210")

if __name__ == "__main__":
    main()
