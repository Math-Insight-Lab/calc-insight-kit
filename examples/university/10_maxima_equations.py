# -*- coding: utf-8 -*-
"""
10_maxima_equations.py — Maxima 方程求解演示

演示 Maxima 在以下方程求解问题上的能力：
  - 一元二次方程：x²-5x+6=0
  - 非线性方程组：x+y=3, xy=2
  - 三角方程、指数方程
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
    print("  Maxima 方程求解演示")
    print("=" * 60)

    # 1. 一元二次方程
    print("\n=== 1. 一元二次方程 ===")
    run_maxima("solve(x^2-5*x+6=0, x);", "x²-5x+6=0 → x=2,3")
    run_maxima("solve(x^2-4=0, x);", "x²-4=0 → x=±2")
    run_maxima("solve(x^2+1=0, x);", "x²+1=0 → x=±i（复数根）")

    # 2. 一元三次方程
    print("\n=== 2. 一元三次方程 ===")
    run_maxima("solve(x^3-6*x^2+11*x-6=0, x);", "x³-6x²+11x-6=0")
    run_maxima("solve(x^3-1=0, x);", "x³-1=0 → x=1 及复数根")

    # 3. 高次方程
    print("\n=== 3. 高次方程 ===")
    run_maxima("solve(x^4-1=0, x);", "x⁴-1=0 → x=±1,±i")

    # 4. 有理方程
    print("\n=== 4. 有理方程 ===")
    run_maxima("solve(1/x=2, x);", "1/x=2 → x=1/2")
    run_maxima("solve((x+1)/(x-1)=3, x);", "(x+1)/(x-1)=3 → x=2")

    # 5. 三角方程
    print("\n=== 5. 三角方程 ===")
    run_maxima("solve(sin(x)=0, x);", "sin(x)=0 → x=nπ")
    run_maxima("solve(cos(x)=1, x);", "cos(x)=1 → x=2nπ")
    run_maxima("solve(tan(x)=1, x);", "tan(x)=1 → x=π/4+nπ")

    # 6. 指数与对数方程
    print("\n=== 6. 指数与对数方程 ===")
    run_maxima("solve(exp(x)=2, x);", "e^x=2 → x=ln(2)")
    run_maxima("solve(log(x)=1, x);", "ln(x)=1 → x=e")
    run_maxima("solve(2^x=8, x);", "2^x=8 → x=3")

    # 7. 方程组
    print("\n=== 7. 方程组 ===")
    run_maxima("solve([x+y=3, x-y=1], [x,y]);", "x+y=3, x-y=1 → x=2,y=1")
    run_maxima("solve([x+y=3, x*y=2], [x,y]);", "x+y=3, xy=2 → x=1,2; y=2,1")
    run_maxima("solve([2*x+3*y=12, x-y=1], [x,y]);", "2x+3y=12, x-y=1")

    # 8. 非线性方程组
    print("\n=== 8. 非线性方程组 ===")
    run_maxima("solve([x^2+y^2=25, x+y=7], [x,y]);", "x²+y²=25, x+y=7")

    print(f"\n{'='*60}")
    print("  ✅ 方程求解演示完成")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()
