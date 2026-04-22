import numpy as np
from problem.calculate_f2 import calcular_momentos_ceb70,calcular_peso_armadura_direcao
import config as cfg

def calcular_f1(valores):
    """Minimizar Volume de Concreto (m³) para Sapata Retangular"""
    A, B, h = valores
    # A, B, h estão em cm, convertemos para metros (/100)
    vol_m3 = (A/100) * (B/100) * (h/100)
    return vol_m3

def calcular_f2(valores):
    """
    Minimiza o Peso Total da Armadura de Aço (kg).
    valores = [A, B, h] em cm.
    """
    A, B, h = valores
    
    # --- Parâmetros de Projeto (Centralizados no Config) ---
    ap, bp = cfg.AP, cfg.BP
    nk = cfg.NK
    fck, fyd, gama_c = cfg.FCK, cfg.FYD, cfg.GAMMA_C
    cobrimento = cfg.COBRIMENTO
    
    diam_x, esp_x = cfg.DIAMETRO_X, cfg.ESPACAMENTO_X
    diam_y, esp_y = cfg.DIAMETRO_Y, cfg.ESPACAMENTO_Y

    # 1. Cálculo dos Momentos
    cA, cB, p, xA, xB, md_x, md_y = calcular_momentos_ceb70(A, B, ap, bp, nk)

    # 2. Peso da Armadura em X
    peso_x = calcular_peso_armadura_direcao(
        md=md_x, fyd=fyd, h=h, cobrimento=cobrimento, diametro_mm=diam_x,
        dimensao_perpendicular=B, dimensao_barra=A, espacamento=esp_x,
        fck=fck, gama_c=gama_c
    )

    # 3. Peso da Armadura em Y
    peso_y = calcular_peso_armadura_direcao(
        md=md_y, fyd=fyd, h=h, cobrimento=cobrimento, diametro_mm=diam_y,
        dimensao_perpendicular=A, dimensao_barra=B, espacamento=esp_y,
        fck=fck, gama_c=gama_c
    )

    return peso_x + peso_y

