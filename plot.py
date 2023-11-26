import matplotlib.pyplot as plt


def get_variable_name(variable):
    for name in locals():
        if id(variable) == id(locals()[name]):
            return name
    return None


def try_plot(x, y, title):
    plt.figure()
    plt.plot(x, y, 'ro', markersize=2)

    plt.xlabel('x')
    plt.ylabel('y')
    plt.title(title)
    plt.savefig(f'plots/{title}.png', dpi=600)
