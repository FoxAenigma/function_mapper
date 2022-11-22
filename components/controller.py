import pandas as pd
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
    sca_data = ax.collections[0]
    points = sca_data.get_offsets().data
    x = Symbol("x")
    px = getattr(polys, method)(points, n)
    domain = linspace(min(points[:,0]), max(points[:,0]), num=100)
    image = array([px.subs(x, val)  for val in domain])
    ax.plot(domain, image, color="#FFE6EA")
    chart.draw()
    write_summary({
        "method": method,
        "deg": n if n!=None else len(points)-1,
        "poly": str(simplify(px)),
        "points": len(points),
    })
    return

def set_data(ax, chart, data_file):
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
