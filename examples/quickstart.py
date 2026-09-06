# -*- coding: utf-8 -*-
"""
Quickstart: 一键运行全部示例，按学段分组执行
用法:
    python examples/quickstart.py
    python examples/quickstart.py kid    # 仅小学层
    python examples/quickstart.py highschool # 仅中学层
    python examples/quickstart.py university # 仅大学层
    python examples/quickstart.py quickstart # 快速入门（5个demo）
    python examples/quickstart.py all    # 全部层
"""
import sys
import os
import importlib.util

# 确保项目根目录在 sys.path 中
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

EXAMPLES = {
    "quickstart": [
        "01_limit_demo",
        "02_derivative_demo",
        "03_riemann_demo",
        "04_taylor_demo",
        "05_eps_delta_demo",
    ],
    "kid": [
        "01_limit_demo",
        "02_derivative_demo",
        "03_riemann_demo",
        "04_taylor_demo",
        "05_epsilon_delta_demo",
        "06_removable_singularity_demo",
        "07_infinite_limit_demo",
        "08_function_continuity_demo",
    ],
    "highschool": [
        "01_limit_demo",
        "02_derivative_demo",
        "03_riemann_demo",
        "04_taylor_demo",
        "05_epsilon_delta_demo",
        "06_removable_singularity_demo",
        "07_infinite_limit_demo",
    ],
    "university": [
        "01_limit_demo",
        "02_derivative_demo",
        "03_riemann_demo",
        "04_taylor_demo",
        "05_epsilon_delta_demo",
        "06_removable_singularity_demo",
        "07_infinite_limit_demo",
        "08_maxima_demo",
        "09_cas_compare_demo",
        "test_maxima_advantage",
        "explore_maxima_capabilities",
        "test_definite_integral",
        "explore_p0_features",
        "10_maxima_limits",
        "10_maxima_definite_integrals",
        "10_maxima_series_sum",
        "10_maxima_taylor_laurent",
        "10_maxima_simplification",
        "10_maxima_equations",
        "10_maxima_inequalities",
        "10_maxima_parametric_integrals",
    ],
}


def run_example(module_name, tier_name):
    """动态导入并运行单个示例模块"""
    module_path = os.path.join(ROOT, "examples", tier_name, f"{module_name}.py")
    if not os.path.exists(module_path):
        print(f"  [SKIP] {module_name} — 文件不存在")
        return False
    try:
        spec = importlib.util.spec_from_file_location(module_name, module_path)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        if hasattr(mod, "main"):
            mod.main()
        print(f"  [OK]   {module_name}")
        return True
    except Exception as e:
        print(f"  [FAIL] {module_name} — {e}")
        return False


def run_tier(tier_name):
    """运行指定层级的所有示例"""
    print(f"\n{'='*60}")
    print(f"  运行 {tier_name.upper()} 层示例")
    print(f"{'='*60}\n")
    modules = EXAMPLES.get(tier_name, [])
    if not modules:
        print(f"  未找到 {tier_name} 层示例")
        return
    ok = sum(1 for m in modules if run_example(m, tier_name))
    total = len(modules)
    print(f"\n✅ {tier_name} 层完成：{ok}/{total} 通过\n")


def main():
    if len(sys.argv) > 1:
        tier = sys.argv[1].lower()
        if tier == "all":
            for name in EXAMPLES:
                run_tier(name)
        elif tier in EXAMPLES:
            run_tier(tier)
        else:
            print(f"未知层级: {tier}。可选: all, kid, middle, university")
            sys.exit(1)
    else:
        # 默认运行所有层级
        for name in EXAMPLES:
            run_tier(name)


if __name__ == "__main__":
    main()
