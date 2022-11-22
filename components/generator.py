from csv import writer
from zipfile import ZipFile
from datetime import datetime as dt

def make_name():
    today = str(dt.now())
    today = today.split(" ")
    file = f"{today[0]}_{today[1].split('.')[0]}.zip"
    file = file.replace(":","-")
    return file

def download_zip(fig):
    image = "data/cache/image.png"
    data = "data/cache/points.csv"
    info = "data/cache/description.txt"
    fig.savefig(image)
    zipper = ZipFile(f"data/{make_name()}", "w")
    zipper.write(image)
    zipper.write(data)
    zipper.write(info)
    zipper.close()
    return

def write_summary(metadata):
    info = f""" 
method: {metadata["method"]}
poly: {metadata["poly"]}
deg: {metadata["deg"]}
points: {metadata["points"]} 
"""
    with open("data/cache/description.txt", "w") as file:
        file.write(info)
    return

def write_points(values: list, mode='a'):
    with open("data/cache/points.csv", mode) as points:
        file = writer(points)
        file.writerow(values)
        points.close()
    return