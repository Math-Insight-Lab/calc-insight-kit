# -*- coding: utf-8 -*-
"""
10_maxima_simplification.py — Maxima 代数化简演示

演示 Maxima 在以下化简问题上的能力：
  - radcan：完全有理化化简
  - ratsimp：有理函数化简
  - trigsimp：三角函数化简
  - 常见化简场景：约分、合并同类项、三角恒等式
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
    print("  Maxima 代数化简演示")
    print("=" * 60)

    # 1. 基本代数化简
    print("\n=== 1. 基本代数化简 ===")
    run_maxima("ratsimp((x^2-1)/(x-1));", "(x²-1)/(x-1) → x+1")
    run_maxima("ratsimp((x^3-1)/(x-1));", "(x³-1)/(x-1) → x²+x+1")
    run_maxima("ratsimp((2*x^2+4*x)/(2*x));", "(2x²+4x)/(2x) → x+2")

    # 2. 根式化简
    print("\n=== 2. 根式化简 ===")
    run_maxima("radcan(sqrt(8)+sqrt(18));", "√8+√18 → 5√2")
    run_maxima("radcan(sqrt(12)*sqrt(3));", "√12·√3 → 6")
    run_maxima("radcan(sqrt(x^2));", "√(x²) → |x|")

    # 3. 有理函数化简
    print("\n=== 3. 有理函数化简 ===")
    run_maxima("ratsimp((x^2+2*x+1)/(x^2+4*x+4));", "(x²+2x+1)/(x²+4x+4) → (x+1)²/(x+2)²")
    run_maxima("ratsimp(1/x+1/(x+1));", "1/x + 1/(x+1) → (2x+1)/(x(x+1))")

    # 4. 三角函数化简
    print("\n=== 4. 三角函数化简 ===")
    run_maxima("trigsimp(sin(x)^2+cos(x)^2);", "sin²(x)+cos²(x) → 1")
    run_maxima("trigsimp(2*sin(x)*cos(x));", "2·sin(x)·cos(x) → sin(2x)")
    run_maxima("trigsimp(sin(3*x));", "sin(3x) → 3sin(x)-4sin³(x)")
    run_maxima("trigsimp(cos(2*x));", "cos(2x) → cos²(x)-sin²(x)")

    # 5. 对数与指数化简
    print("\n=== 5. 对数与指数化简 ===")
    run_maxima("radcan(exp(log(x)));", "e^(ln(x)) → x")
    run_maxima("radcan(log(x^2));", "ln(x²) → 2·ln(x)")
    run_maxima("radcan(exp(a+b));", "e^(a+b) → e^a·e^b")
    run_maxima("radcan((exp(x))^2/exp(x));", "e^(2x)/e^x → e^x")

    # 6. 多项式展开
    print("\n=== 6. 多项式展开 ===")
    run_maxima("expand((x+1)^3);", "(x+1)³ → x³+3x²+3x+1")
    run_maxima("expand((x-2)*(x+3)*(x-4));", "(x-2)(x+3)(x-4) 展开")

    # 7. 部分分式分解
    print("\n=== 7. 部分分式分解 ===")
    run_maxima("partfrac(1/(x^2-1), x);", "1/(x²-1) → 部分分式")
    run_maxima("partfrac((3*x+5)/(x^2+3*x+2), x);", "部分分式分解")

    # 8. 更复杂的化简
    print("\n=== 8. 更复杂的化简 ===")
    run_maxima("ratsimp((x^2-4)/(x^2-2*x));", "(x²-4)/(x²-2x) → (x+2)/x")
    run_maxima("ratsimp((x^2+3*x+2)/(x^2+5*x+6));", "(x²+3x+2)/(x²+5x+6) → (x+1)/(x+2)")

    print(f"\n{'='*60}")
    print("  ✅ 代数化简演示完成")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()
