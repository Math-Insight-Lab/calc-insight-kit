# -*- coding: utf-8 -*-
"""
10_maxima_inequalities.py — Maxima 不等式求解演示

演示 Maxima 在以下不等式求解问题上的能力：
  - 多项式不等式：(x-1)(x+2)>0
  - 有理不等式：(x+1)/(x-2) <= 0
  - 绝对值不等式
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
    print("  Maxima 不等式求解演示")
    print("=" * 60)

    # 1. 多项式不等式
    print("\n=== 1. 多项式不等式 ===")
    run_maxima("load(solve_ineq); solve_ineq(x^2-5*x+6>0);", "x²-5x+6>0 → x<2 或 x>3")
    run_maxima("load(solve_ineq); solve_ineq(x^2-4<0);", "x²-4<0 → -2<x<2")
    run_maxima("load(solve_ineq); solve_ineq(x^2-4*x+4>=0);", "x²-4x+4>=0 → 所有实数")

    # 2. 三次不等式
    print("\n=== 2. 三次不等式 ===")
    run_maxima("load(solve_ineq); solve_ineq(x*(x-1)*(x+2)>0);", "x(x-1)(x+2)>0")

    # 3. 有理不等式
    print("\n=== 3. 有理不等式 ===")
    run_maxima("load(solve_ineq); solve_ineq((x+1)/(x-2)<=0);", "(x+1)/(x-2)<=0 → -1<=x<2")
    run_maxima("load(solve_ineq); solve_ineq((x-1)/(x+2)>1);", "(x-1)/(x+2)>1")

    # 4. 绝对值不等式
    print("\n=== 4. 绝对值不等式 ===")
    run_maxima("load(solve_ineq); solve_ineq(abs(x-3)<5);", "|x-3|<5 → -2<x<8")
    run_maxima("load(solve_ineq); solve_ineq(abs(2*x+1)>=3);", "|2x+1|>=3")
    run_maxima("load(solve_ineq); solve_ineq(abs(x)<=2);", "|x|<=2 → -2<=x<=2")

    # 5. 二次不等式组
    print("\n=== 5. 二次不等式组 ===")
    run_maxima(
        "load(solve_ineq); solve_ineq([x^2-1>=0, x^2-9<=0], x);",
        "x²-1>=0 且 x²-9<=0",
    )

    # 6. 更复杂的有理不等式
    print("\n=== 6. 更复杂的有理不等式 ===")
    run_maxima(
        "load(solve_ineq); solve_ineq((2*x-1)/(x+3)>0);",
        "(2x-1)/(x+3)>0",
    )
    run_maxima(
        "load(solve_ineq); solve_ineq((x^2-4)/(x-1)<=0);",
        "(x²-4)/(x-1)<=0",
    )

    # 7. 含参数的不等式
    print("\n=== 7. 含参数的不等式 ===")
    run_maxima("load(solve_ineq); solve_ineq(x^2-a*x>0, x);", "x²-ax>0 关于 x")

    # 8. 实际应用中的不等式
    print("\n=== 8. 实际应用中的不等式 ===")
    run_maxima(
        "load(solve_ineq); solve_ineq((x+2)*(x-3)^2>0);",
        "(x+2)(x-3)²>0",
    )

    print(f"\n{'='*60}")
    print("  ✅ 不等式求解演示完成")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()
