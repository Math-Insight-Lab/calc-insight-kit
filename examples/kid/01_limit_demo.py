from calc_insight_kit.api import show_limit

def main():
    res = show_limit("sin(x)/x", x0=0.0, x_range=(-3,3))
    res.save_fig("limit_sinx_x.png")
    print(res.latex)
    res.close()

if __name__ == "__main__":
    main()
