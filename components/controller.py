import pandas as pd
import numpy as np
import components.interpolator as polys
import matplotlib.pyplot as plt
from numpy import linspace, array
from sympy import Symbol, simplify
from tkinter import filedialog as fd
from components.generator import write_points, write_summary
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def init_setup(window):
    ax, chart, fig = make_plot(window)
    data_file = ""
    return ax, chart, fig, data_file

def make_plot(window):
    plt.ion()
    fig = Figure(figsize = (7.6, 5.5), dpi = 100, facecolor="#131626")
    fig.add_subplot(111)
    ax = fig.get_axes()[0]
    ax.grid()
    ax.spines['bottom'].set_color("#FFE6EA")
    ax.spines['top'].set_color("#FFE6EA") 
    ax.spines['right'].set_color("#FFE6EA")
    ax.spines['left'].set_color("#FFE6EA")
    ax.tick_params(axis='x', colors="#FFE6EA")
    ax.tick_params(axis='y', colors="#FFE6EA")
    ax.yaxis.label.set_color("#FFE6EA")
    ax.xaxis.label.set_color("#FFE6EA")
    ax.set(
        xlabel = "Variable X",
        ylabel = "Imagen Y",
        facecolor = "#131626",
    )
    chart = FigureCanvasTkAgg(fig, master = window)  
    chart.get_tk_widget().place(x=220, y=20)
    chart.draw()
    return ax, chart, fig

def clean_plot(ax, chart, points=True, curve=True):
    if points:
        for point in ax.collections:
            point.remove()
    if curve:
        for line in ax.lines:
            line.remove()
    chart.draw()
    return

def resize_plot(ax, x_data, y_data):
    beta = 0.2
    x_min = min(x_data)
    y_min = min(y_data)
    x_max = max(x_data)
    y_max = max(y_data)
    x_prom = abs(x_max+x_min)/2
    y_prom = abs(y_max+y_min)/2
    ax.set_xlim([x_min-beta*x_prom, x_max+beta*x_prom])
    ax.set_ylim([y_min-beta*y_prom, y_max+beta*y_prom])
    return

def update_points(ax, chart, x_point, y_point):
    ax.scatter(x_point, y_point, marker="x", color="#FFE6EA")
    resize_plot(ax, x_point, y_point)
    chart.draw()
    return

def update_curve(ax, chart, data_file, method, n):
    clean_plot(ax, chart, points=False)
    try:
        n = int(n)
    except:
        n = None
    sca_data = ax.collections[0]
    points = sca_data.get_offsets().data
    write_points(points, "data/cache/points.csv")
    copy = np.copy(points)
    points = random_sample(points, n)
    write_points(points, "data/cache/sample.csv")
    x = Symbol("x")
    px, e_method = getattr(polys, method)(points)
    domain = linspace(min(points[:,0]), max(points[:,0]), num=100)
    image = array([px.subs(x, val)  for val in domain])
    ax.plot(domain, image, color="#FFE6EA")
    chart.draw()
    write_summary({
        "function": f"{ax.get_ylabel()}({ax.get_xlabel()})",
        "variables": f"{ax.get_xlabel()} -- {ax.get_ylabel()}",
        "method": method,
        "poly": str(simplify(px)),
        "points": len(points),
        "err_sample": err_sample(copy,px),
        "err_method": e_method,
    })
    return

def set_data(ax, chart, data_file):
    clean_plot(ax, chart)
    data_file = fd.askopenfilename()
    data = pd.read_csv(data_file)
    x_points = data.iloc[:,0]
    y_points = data.iloc[:,1]
    ax.set(
        xlabel = data.columns[0],
        ylabel = data.columns[1],
    )
    update_points(ax, chart, x_points, y_points)
    return


def random_sample(points, n):
    #n is poly deg
    if n == None:
        return points
    if len(points) < n+1:
        return points
    sample = np.zeros((n+1,2))
    dim = n+1
    n_old = len(points) - 1
    chunk = int((n_old+1)//(n+1) + ((n_old+1)%(n+1))/(abs((n_old+1)%(n+1) - 1) + 1))
    for chip in range(0,dim):
        if chip == 0:
            sample[chip] = points[0]
        elif chip == dim-1:
            sample[chip] = points[-1]
        else:
            sample[chip] = points[chunk*(chip):chunk*(chip+1)][np.random.randint(0,chunk-1)]
    return sample

def err_sample(points, poly):
    x = Symbol("x")
    e = 0
    for k in range(len(points)):
        e += abs(points[k,1]-poly.subs({x: points[k,0]}))
    return e/len(points)