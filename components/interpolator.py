import sympy as sym

global TOL
TOL = 1e-5

def newton(points, _):
    def ddiv(sample):
        if len(sample[:,0]) == 1:
            coef = sample[0,1]
        else:
            coef = (ddiv(sample[1:,:]) - ddiv(sample[:-1,:])) / (sample[-1,0]-points[0,0])
        return coef

    x = sym.Symbol("x")
    poly = 0
    roots = 1
    for i in range(len(points)):
        poly += roots*ddiv(points[:i+1,:])
        roots = roots*(x-points[i,1])
    return poly

def lagrange(points, _):
    def lx(sample, j):
        x = sym.Symbol("x")
        l = 1
        for i in range(len(sample)):
            if i != j:
                l = l * (x-sample[i,0])/(sample[j,0]-sample[j,0])
        return

    poly = 0
    for j in range(len(points)):
        poly += points[j,1]*lx(points, j) 
    return poly 


def min_square():
    return

def exponetial_asc():
    return

def exponetial_dsc():
    return

def ln():
    return 
