# -*- coding: utf-8 -*-
"""
09_cas_compare_demo.py — SymPy vs Maxima 双引擎对比
重点展示 Maxima 的三大优势场景：
  1. 复杂有理函数积分 1/(1+x^10) —— SymPy 截断/RootSum，Maxima 完整显式解
  2. 有理函数积分 1/(x^3+1) —— Maxima 输出更清晰
  3. 非线性方程组 —— Maxima 直接返回数值解
"""
import sympy as sp
import re
from calc_insight_kit.calc_backend import get_cas_backend as get_sympy_backend
from calc_insight_kit.maxima_bridge import get_cas_backend as get_maxima_backend


def print_separator(title):
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}")


def show_sp_result(title, sp_result, label="SymPy"):
    """格式化打印 SymPy 结果"""
    print(f"\n【{label} 结果】")
    result_str = str(sp_result)
    print(f"结果长度: {len(result_str)} 字符")
    # 长结果截断显示
    if len(result_str) > 200:
        print(f"结果: {result_str[:200]}...")
    else:
        print(f"结果: {result_str}")
    # 判断完整性
    if "RootSum" in result_str or "rootof" in result_str:
        print("⚠️  包含 RootSum，无法直接阅读！")
    elif len(result_str) < 50:
        print("⚠️  结果过短，疑似截断/超时！")
    else:
        print("✅ 返回了完整结果")
    # LaTeX
    try:
        print(f"LaTeX: {sp.latex(sp_result)[:200]}")
    except Exception:
        pass


def show_max_result(title, max_result, label="Maxima"):
    """格式化打印 Maxima 结果"""
    print(f"\n【{label} 结果】")
    result_str = max_result.strip()
    print(f"结果长度: {len(result_str)} 字符")
    if len(result_str) > 200:
        print(f"结果: {result_str[:200]}...")
    else:
        print(f"结果: {result_str}")
    if "log" in result_str.lower() and "atan" in result_str.lower():
        print("✅ 返回显式的 log + atan 闭式解！")


def case_rational_integral():
    """1/(1+x^10) —— SymPy 的 RootSum 痛点"""
    print_separator("Case 1: integrate 1/(1+x**10) dx —— SymPy 经典痛点")

    # --- SymPy ---
    sympy_be = get_sympy_backend("sympy")
    x = sp.Symbol("x")
    expr = 1 / (1 + x**10)
    try:
        sp_result = sympy_be.integrate(expr, x)
        show_sp_result("Case 1", sp_result, "SymPy")
    except Exception as e:
        print(f"❌ SymPy 错误: {e}")

    # --- Maxima 文本输出 ---
    max_be = get_maxima_backend(prefer_maxima=True)
    try:
        max_result = max_be.integrate("1/(1+x^10)", "x")
        show_max_result("Case 1", max_result, "Maxima (文本)")
    except Exception as e:
        print(f"❌ Maxima 错误: {e}")

    # --- Maxima LaTeX 输出 ---
    try:
        max_latex = max_be.integrate_tex("1/(1+x^10)", "x")
        print(f"\n【Maxima LaTeX 格式】")
        # 清理 tex() 输出的标记
        tex_lines = [l.strip() for l in max_latex.splitlines() 
                     if not l.startswith("(%i") and not l.startswith("(%o)")]
        latex_str = "\n".join(tex_lines).replace("false","").strip()
        if latex_str:
            print(f"LaTeX: {latex_str}")
        else:
            print("LaTeX 输出为空，尝试 raw 结果")
            print(f"Raw: {max_latex.strip()[:300]}")
    except Exception as e:
        print(f"❌ Maxima LaTeX 错误: {e}")


def case_cube_integral():
    """1/(x^3+1) —— 中等复杂度积分对比"""
    print_separator("Case 2: integrate 1/(x**3+1) dx —— 中等复杂度")

    print("\n【SymPy 结果】")
    sympy_be = get_sympy_backend("sympy")
    x2 = sp.Symbol("x")
    try:
        sp_result = sympy_be.integrate(1/(x2**3 + 1), x2)
        show_sp_result("Case 2", sp_result, "SymPy")
    except Exception as e:
        print(f"错误: {e}")

    print("\n【Maxima 文本结果】")
    max_be = get_maxima_backend(prefer_maxima=True)
    try:
        max_result = max_be.integrate("1/(x^3+1)", "x")
        show_max_result("Case 2", max_result, "Maxima (文本)")
    except Exception as e:
        print(f"错误: {e}")

    # --- Maxima LaTeX ---
    print("\n【Maxima LaTeX 格式】")
    try:
        max_latex = max_be.integrate_tex("1/(x^3+1)", "x")
        tex_lines = [l.strip() for l in max_latex.splitlines()
                     if not l.startswith("(%i") and not l.startswith("(%o)")]
        latex_str = "\n".join(tex_lines).replace("false","").strip()
        if latex_str:
            print(f"LaTeX: {latex_str}")
    except Exception as e:
        print(f"错误: {e}")


def case_nonlinear_system():
    """非线性方程组 —— SymPy vs Maxima"""
    print_separator("Case 3: 非线性方程组求解")

    eq1_raw = "0.144*x*y + 0.018*x**2 + 0.05*x - 1.577"
    eq2_raw = "0.072*y**2 + 0.018*x*y - 0.09*y - 0.512"

    print(f"\n方程组:")
    print(f"  {eq1_raw} = 0")
    print(f"  {eq2_raw} = 0")

    # --- SymPy ---
    print("\n【SymPy 求解结果】")
    x_sym, y_sym = sp.symbols("x y")
    eq1 = sp.Eq(0.144*x_sym*y_sym + 0.018*x_sym**2 + 0.05*x_sym - 1.577, 0)
    eq2 = sp.Eq(0.072*y_sym**2 + 0.018*x_sym*y_sym - 0.09*y_sym - 0.512, 0)
    try:
        sp_sol = sp.solve([eq1, eq2], [x_sym, y_sym], dict=True)
        print(f"解的数量: {len(sp_sol)}")
        keys = list(sp_sol[0].keys())
        for i, sol in enumerate(sp_sol[:4]):
            xv = sol[keys[0]]
            yv = sol[keys[1]]
            try:
                xv = float(xv)
            except (TypeError, ValueError):
                xv = str(xv)[:50]
            try:
                yv = float(yv)
            except (TypeError, ValueError):
                yv = str(yv)[:50]
            print(f"  解{i+1}: x={xv}, y={yv}")
    except Exception as e:
        print(f"❌ SymPy 求解失败: {e}")

    # --- Maxima ---
    print("\n【Maxima 求解结果】")
    max_be = get_maxima_backend(prefer_maxima=True)
    try:
        maxima_code = f"solve([{eq1_raw}, {eq2_raw}], [x, y]);"
        max_out = max_be.raw_eval(maxima_code)
        # 提取实际解：匹配 "[x = ..., y = ...]" 模式（支持多行）
        solution_matches = re.findall(r'\[x\s*=\s*.*?y\s*=\s*[^]]+\]', max_out, re.DOTALL)
        print(f"Maxima 返回: {max_out.strip()[:300]}...")
        if solution_matches:
            print(f"✅ Maxima 返回了 {len(solution_matches)} 个解")
            for i, m in enumerate(solution_matches[:4]):
                # 清理空格和换行
                clean = re.sub(r'\s+', ' ', m.strip())
                print(f"  解{i+1}: {clean[:120]}")
        else:
            print("⚠️  未能提取到完整解")
    except Exception as e:
        print(f"❌ Maxima 错误: {e}")


# ========== 总结 ==========
def main():
    print("🔬 SymPy vs Maxima CAS 引擎对比测试")
    print("重点展示 Maxima 在复杂符号计算上的优势")

    case_rational_integral()
    case_cube_integral()
    case_nonlinear_system()

    print(f"\n{'='*60}")
    print("  ✅ 对比测试完成")
    print("  结论：Maxima 在处理复杂有理函数积分时能给出更完整")
    print("        的符号解，且支持 LaTeX 格式导出。")
    print(f"{'='*60}\n")


if __name__ == "__main__":
    main()
