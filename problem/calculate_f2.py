import math

def calcular_momentos_ceb70(A, B, ap, bp, Nk):
    cA = (A - ap) / 2
    cB = (B - bp) / 2
    p = Nk / (A * B)
    xA = cA + 0.15 * ap
    xB = cB + 0.15 * bp
    M1A = p * (xA ** 2) * B / 2
    M1B = p * (xB ** 2) * A / 2
    return cA, cB, p, xA, xB, M1A, M1B

def area_barra(diametro_mm):
    return math.pi * (diametro_mm / 10)**2 / 4

def peso_linear_barra(diametro_mm):
    return diametro_mm**2 / 162

def altura_util(h, cobrimento, diametro_mm):
    return h - cobrimento - (diametro_mm / 10) / 2

def calcular_area_aco(md, d, fyd):
    return md / (0.85 * d * fyd)

def calcular_resistencias_ancoragem(fck, gama_c):
    fctd = 0.21 * (fck ** (2 / 3)) / gama_c
    fbd = 2.25 * fctd
    return fctd, fbd

def calcular_comprimento_ancoragem(diametro_mm, fyd, fbd_mpa):
    fyd_mpa = fyd * 10
    lb_mm = (diametro_mm / 4) * (fyd_mpa / fbd_mpa)
    lb_limite_mm = 25 * diametro_mm
    return min(lb_mm, lb_limite_mm) / 10

def calcular_peso_armadura_direcao(md, fyd, h, cobrimento, diametro_mm,
                                   dimensao_perpendicular, dimensao_barra,
                                   espacamento, fck, gama_c):
    """
    retorna APENAS o peso.
    """
    d = altura_util(h, cobrimento, diametro_mm)
    As = calcular_area_aco(md, d, fyd)
    a_barra = area_barra(diametro_mm)

    n_barras_area = math.ceil(As / a_barra)
    largura_util = dimensao_perpendicular - 2 * cobrimento
    n_barras_espacamento = math.floor(largura_util / espacamento) + 1
    n_barras = max(n_barras_area, n_barras_espacamento)

    comprimento_reto_cm = dimensao_barra - 2 * cobrimento
    fctd, fbd = calcular_resistencias_ancoragem(fck, gama_c)
    lb_cm = calcular_comprimento_ancoragem(diametro_mm, fyd, fbd)

    comprimento_total_barra_m = (comprimento_reto_cm + 2 * lb_cm) / 100
    peso_unitario = peso_linear_barra(diametro_mm)
    
    peso_total = n_barras * comprimento_total_barra_m * peso_unitario
    return peso_total