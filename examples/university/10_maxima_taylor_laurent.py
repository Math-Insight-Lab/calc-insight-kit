# -*- coding: utf-8 -*-
"""
10_maxima_taylor_laurent.py — Maxima 泰勒展开与洛朗展开演示

演示 Maxima 在以下展开问题上的能力：
  - 泰勒展开：函数在一点的多项式近似
  - 洛朗展开：包含负幂次的广义展开
  - 常见函数的级数展开
"""
import subprocess


def _clean_maxima_result(raw: str) -> str:
    import re
    cleaned = re.sub(r'^(\S+)\s+[─▬─]+\s*(\S+)$', r'\1/\2', raw)
    cleaned = re.sub(r'\s+', ' ', cleaned).strip()
    return cleaned


def run_maxima(code: str, label: str = ""):
    """运行一条 Maxima 命令并打印结果。"""
    print(f"\n{'─'*60}")
    print(f"  {label}")
    print(f"  cmd: {code.strip()}")
    print(f"{'─'*60}")
    try:
        code = "display2d: false;\n" + code
        proc = subprocess.Popen(
            ["maxima", "--very-quiet"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        stdout, stderr = proc.communicate(code.strip() + "\n", timeout=15)
        lines = [
            l.strip()
            for l in stdout.splitlines()
            if l.strip() and l.strip() not in ("false", '"lisp"')
        ]
        raw_result = " ".join(lines).strip()
        display_result = _clean_maxima_result(raw_result)
        print(f"  结果: {display_result[:300]}")
        if stderr.strip():
            print(f"  警告: {stderr.strip()[:200]}")
    except subprocess.TimeoutExpired:
        print("  [超时]")
    except Exception as e:
        print(f"  [错误: {e}]")


def main():
    print("=" * 60)
    print("  Maxima 泰勒展开与洛朗展开演示")
    print("=" * 60)

    # 1. 基本泰勒展开
    print("\n=== 1. 基本泰勒展开 ===")
    run_maxima("taylor(exp(x), x, 0, 5);", "e^x 在 x=0 处 5 阶泰勒展开")
    run_maxima("taylor(sin(x), x, 0, 7);", "sin(x) 在 x=0 处 7 阶泰勒展开")
    run_maxima("taylor(cos(x), x, 0, 6);", "cos(x) 在 x=0 处 6 阶泰勒展开")

    # 2. 非原点展开
    print("\n=== 2. 非原点展开 ===")
    run_maxima("taylor(log(x), x, 1, 5);", "ln(x) 在 x=1 处 5 阶展开")
    run_maxima("taylor(1/(1-x), x, 0, 5);", "1/(1-x) 在 x=0 处 5 阶展开")

    # 3. 复合函数
    print("\n=== 3. 复合函数展开 ===")
    run_maxima("taylor(exp(-x^2), x, 0, 6);", "e^(-x²) 在 x=0 处 6 阶展开")
    run_maxima("taylor(sin(x^2), x, 0, 7);", "sin(x²) 在 x=0 处展开")

    # 4. 洛朗展开
    print("\n=== 4. 洛朗展开 ===")
    run_maxima("taylor(1/x, x, 0, -3, 5);", "1/x 在 x=0 处的洛朗展开")
    run_maxima("taylor(sin(x)/x, x, 0, -1, 6);", "sin(x)/x 在 x=0 处的洛朗展开")
    run_maxima("taylor(1/(x*(x-1)), x, 0, -2, 4);", "1/(x(x-1)) 在 x=0 处的洛朗展开")

    # 5. 更复杂的函数
    print("\n=== 5. 更复杂的函数 ===")
    run_maxima("taylor(exp(x)*sin(x), x, 0, 6);", "e^x·sin(x) 在 x=0 处 6 阶展开")
    run_maxima("taylor(log(1+x)/x, x, 0, -1, 5);", "ln(1+x)/x 在 x=0 处展开")

    # 6. 三角函数复合
    print("\n=== 6. 三角函数复合 ===")
    run_maxima("taylor(sin(x)*cos(x), x, 0, 7);", "sin(x)·cos(x) 在 x=0 处 7 阶展开")
    run_maxima("taylor(1/cos(x), x, 0, 6);", "sec(x) 在 x=0 处 6 阶展开")

    print(f"\n{'='*60}")
    print("  ✅ 泰勒/洛朗展开演示完成")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()
