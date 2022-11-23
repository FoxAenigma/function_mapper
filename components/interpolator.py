import sympy as sym
import numpy as np

global TOL, x
TOL = 1e-5
x = sym.Symbol("x")

def newton(points):
    def ddiv(sample):
        if len(sample[:,0]) == 1:
            coef = sample[0,1]
        else:
            coef = (ddiv(sample[1:,:]) - ddiv(sample[:-1,:])) / (sample[-1,0]-sample[0,0])
        return coef

    poly = 0
    roots = 1
    for i in range(len(points[:,0])):
        poly += roots*ddiv(points[:i+1,:])
        roots = roots*(x-points[i,0])
    e = err_interpol(points, poly)
    return poly, e

def lagrange(points):
    def lx(sample, j):
        l = 1
        for i in range(len(sample)):
            if i != j:
                l = l * (x-sample[i,0])/(sample[j,0]-sample[i,0])
        return l

    poly = 0
    for j in range(len(points)):
        poly += points[j,1]*lx(points, j)
    e = err_interpol(points, poly)
    return poly, e


def linear(points):
    def err(points, poly):
        e = 0
        for k in range(len(points)):
            e += (points[k,1]-poly.evalf(subs={x: points[k,0]}))**2
        return np.sqrt(float(e/len(points)))

    def coef_msquare(points):
        n = len(points)
        xiyi = 0
        xi = 0
        yi = 0
        xi2 = 0
        for i in range(n):
            xiyi += points[i,0]*points[i,1]
            xi += points[i,0]
            yi += points[i,1]
            xi2 += points[i,0]**2
        print(xiyi, xi, yi, xi2)
        a = (n*xiyi-xi*yi)/(n*xi2-xi**2)
        b = (yi-a*xi)/n
        return a, b 

    a, b = coef_msquare(points)
    poly = a*x+b
    e = err(points, poly)
    return poly, e

def err_interpol(points, poly):
    def err(points, remain):
        e = 0
        for i in range(len(points)):
            e += abs(points[i,1]-remain.evalf(subs={x: points[i,0]}))
        return e/len(points)

    def remain(points, poly):
        f_gamma = ddiv(points)
        roots = 1
        for i in range(len(points)):
            roots *= (x-points[i,0])
        return f_gamma*roots

    def ddiv(sample):
        if len(sample[:,0]) == 1:
            coef = sample[0,1]
        else:
            coef = (ddiv(sample[1:,:]) - ddiv(sample[:-1,:])) / (sample[-1,0]-sample[0,0])
        return coef
    
    r = remain(points, poly)
    e = err(points, r)
    return e

""""
def exp_asc(points, _):
    a, b = coef_msquare(points)
    poly = sym.exp(b)*sym.exp(a*x)
    return poly

def exp_dsc(points, _):
    a, b = coef_msquare(points)
    poly = sym.exp(b)*sym.exp(-a*x)
    return poly

def ln(points, _):
    a, _ = coef_msquare(points)
    poly = sym.ln(a*x)
    return poly
"""

