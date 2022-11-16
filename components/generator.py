from csv import writer

def make_csv():
    return

def make_image():
    return

def download_zip():
    return

def write_points(values: list, mode='a'):
    with open("data/cache/points.csv", mode) as points:
        file = writer(points)
        file.writerow(values)
        points.close()
    return