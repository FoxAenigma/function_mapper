from csv import writer
from zipfile import ZipFile
from datetime import datetime as dt
from pandas import DataFrame

def make_name():
    today = str(dt.now())
    today = today.split(" ")
    file = f"measure_{today[0]}_{today[1].split('.')[0]}.zip"
    file = file.replace(":","-")
    return file

def download_zip(fig):
    image = "data/cache/image.png"
    data = "data/cache/"
    info = "data/cache/description.txt"
    fig.savefig(image)
    zipper = ZipFile(f"data/{make_name()}", "w")
    zipper.write(image)
    zipper.write(data)
    zipper.write(info)
    zipper.close()
    return

def write_summary(metadata):
    with open("data/cache/description.txt", 'w') as f:
        for key, value in metadata.items():
            f.write('%s:%s\n' % (key, value))
    return

def write_points(values, name):
    table = DataFrame(values, columns=["dataX", "dataY"])
    table.to_csv(name, index=False)
    return