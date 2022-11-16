import pandas as pd
import components.interpolator as polys
import matplotlib.pyplot as plt
from numpy import linspace, array
from sympy import Symbol
from components.connection import get_data
from components.generator import write_points
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def init_setup(window):
    reset()
    ax, chart = make_plot(window)
    return ax, chart

def reset():
    write_points(["sensorX", "sensorY"], mode='w')
    return

def make_plot(window):
    plt.ion()
    fig = Figure(figsize = (7.6, 4.5), dpi = 100, facecolor="#131626")
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
        xlabel = "Tension (V)",
        ylabel = "Corriente (A)",
        facecolor = "#131626",
    )
    ax.set_xlabel("Tension (V)")
    ax.set_ylabel("Corriente (A)")
    chart = FigureCanvasTkAgg(fig, master = window)  
    chart.get_tk_widget().place(x=220, y=120)
    chart.draw()
    return ax, chart

def update_plot(ax, chart, x_point, y_point):
    ax.scatter(x_point, y_point, marker="x", color="#FFE6EA")
    chart.draw()
    return

def update_curve(ax, chart, method="newton", n=3):
    points = pd.read_csv("data/cache/points.csv")
    points.sort_values(by=["sensorX"], inplace=True)
    points.dropna(inplace=True)
    points.drop_duplicates(subset=["sensorX"], inplace=True)

    x = Symbol("x")
    px = getattr(polys, method)(points.to_numpy(), n)
    domain = linspace(points["sensorX"].min(), points["sensorX"].max(), num=100)
    print(domain)
    image = array([px.subs(x, val)  for val in domain])
    ax.plot(domain, image)
    chart.draw()
    return

def clean_points(ax, chart):
    reset()
    for point in ax.collections:
        point.remove()
    for line in ax.lines:
        line.remove()
    chart.draw()
    return

def set_point(ax, chart):
    data = get_data()
    x_point = data["sensorX"]
    y_point = data["sensorY"]
    write_points([x_point, y_point])
    update_plot(ax, chart, x_point, y_point)
    return
