def calcular_f1(x):
    return x**2

def calcular_f2(x):
    return (x-2)**2

def checar_restricoes(x,lim_sup,lim_inf):
    v = 0
    if x < -1: v += abs(x + lim_sup)
    if x > 3:  v += abs(x - lim_inf)
    return v