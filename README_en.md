# Calc-Insight-Kit: 3-Tier Differentiated Calculus Visualization Toolkit

## Introduction
A full-layer calculus visualization project with **homogeneous core knowledge and differentiated presentation**, covering primary school intuitive perception, middle school exam-oriented calculation, and university rigorous mathematical proof.

## Tier Architecture
- **Kid Tier (8 demos)**: Pure visualization, no formula, no calculation, intuitive mathematical observation
- **Middle Tier (8 demos)**: Formula calculation, geometric interpretation, middle school exam-oriented
- **University Tier (22 demos)**: Strict mathematical definition, error analysis, convergence proof, dual-CAS comparison

## Key Features
- Homogeneous core logic for basic calculus knowledge
- Academic exclusive dual-CAS engine verification module
- Full automated test suite & complete teaching documents
- Out-of-the-box batch execution support

## Installation
```bash
pip install -e .
```

## Quick Start
```bash
python main.py
```

## License

This project is licensed under the **MIT License** (see [LICENSE](LICENSE)). You are free to use, modify, and distribute it for any purpose.

### Third-Party Dependencies & License Notice

This project uses the following third-party libraries, all compatible with the MIT License:

| Dependency | License | Notes |
|------------|---------|-------|
| SymPy | BSD 3-Clause | Default CAS backend, MIT compatible |
| NumPy | BSD 3-Clause | Numerical computing foundation |
| Matplotlib | Matplotlib License | Visualization engine |
| **Maxima** | **GPL v3** | **Optional CAS backend, only used in university-level dual-CAS comparison demos** |

> **Maxima GPL Compatibility Note**: Maxima is distributed under the GNU GPL v3 license. This project uses Maxima as an **optional external dependency**, invoked via command-line process (not Python import), which does not trigger GPL "linking" requirements. After `pip install -e .`, the core functionality (SymPy backend + visualization) works fully without Maxima. Maxima is only required when explicitly calling `get_cas_backend("maxima")` or running the `university/10_maxima_*.py` series.
>
> Under [GPL Section 13 compatibility](https://www.gnu.org/licenses/gpl-faq.html#GPLINCOMPAT), invoking a GPL program via isolated processes is considered a separate work, and does not require the calling project to adopt GPL. Therefore, this MIT-licensed project can safely use Maxima as an optional backend.

### Usage Restrictions

1. **SymPy Backend** (default): Fully MIT licensed — free for commercial, educational, and research use.
2. **Maxima Backend** (optional): If you choose to use Maxima, ensure compliance with the GPL v3 license.
3. **Generated Charts**: Visualizations created with this project are free for teaching and academic use.
