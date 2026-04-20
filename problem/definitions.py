import math
import numpy as np
import os
import subprocess
import time
from problem.calculate_f2 import calcular_momentos_ceb70,calcular_peso_armadura_direcao


def calcular_f1_sapata(valores):
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
    
    # --- ALERTA DE CONSTANTES ---
    # Atenção: Verifique se estes valores batem com o do arquivo de restrições!
    ap = 30.0   # comprimento do pilar
    bp = 20.0   # largura do pilar
    nk = 800.0  # carga normal (kN)
    cobrimento = 5.0
    fck = 25.0
    gama_c = 1.4
    fyd = 43.5

    # Armadura Direção X
    diametro_x = 12.5
    espacamento_x = 15.0

    # Armadura Direção Y
    diametro_y = 10.0
    espacamento_y = 15.0

    # 1. Cálculo dos Momentos
    cA, cB, p, xA, xB, md_x, md_y = calcular_momentos_ceb70(A, B, ap, bp, nk)

    # 2. Peso da Armadura em X
    peso_x = calcular_peso_armadura_direcao(
        md=md_x, fyd=fyd, h=h, cobrimento=cobrimento, diametro_mm=diametro_x,
        dimensao_perpendicular=B, dimensao_barra=A, espacamento=espacamento_x,
        fck=fck, gama_c=gama_c
    )

    # 3. Peso da Armadura em Y
    peso_y = calcular_peso_armadura_direcao(
        md=md_y, fyd=fyd, h=h, cobrimento=cobrimento, diametro_mm=diametro_y,
        dimensao_perpendicular=A, dimensao_barra=B, espacamento=espacamento_y,
        fck=fck, gama_c=gama_c
    )

    return peso_x + peso_y

