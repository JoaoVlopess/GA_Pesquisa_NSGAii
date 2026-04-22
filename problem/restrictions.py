from math import pi, tan, radians
import config as cfg

def fcd_kN_cm2(fck, gamma_c):
    return (fck / gamma_c) * 0.1

def fctd_aprox_kN_cm2(fck, gamma_c):
    fctm = 0.3 * (fck ** (2 / 3))
    return (fctm / gamma_c) * 0.1

def alfa_v(fck):
    return 1 - fck / 250

def checar_restricoes_sapata(valores):
    """
    Avalia a segurança da sapata segundo NBR 6118 e retorna a penalidade (v).
    valores = [A, B, h] em cm.
    v = 0 significa que atende a todas as normas.
    """
    A, B, h = valores

    ap, bp = cfg.AP, cfg.BP
    N, H, M = cfg.NK, cfg.H, cfg.M
    P, h_H = cfg.P_SOLO_SOBRE, 0.0 # braço h_H considerado 0
    padm = cfg.PADM
    fck, gamma_c, gamma_f = cfg.FCK, cfg.GAMMA_C, cfg.GAMMA_F
    cobrimento = cfg.COBRIMENTO

    # Derivando a altura útil 'd'
    d = h - cobrimento
    v = 0.0

    # Penalidade Multiplicadora (Para colocar os erros na mesma grandeza)
    # Tensões são valores pequenos (ex: 0.04), então multiplicamos a diferença por 10000
    PESO_TENSAO = 10000 
    PESO_FATOR = 100

   
    # 1) CLASSIFICAÇÃO DA SAPATA (Rígida ou Flexível)
    limite_A = (A - ap) / 3
    limite_B = (B - bp) / 3
    sapata_rigida = (h >= limite_A) and (h >= limite_B)
    
    # if not  sapata_rigida: v += 500 

    # 2) TENSÃO DO SOLO
    Nd = N * gamma_f
    Md = M * gamma_f
    area_total = A * B

    if Nd > 0:
        e = Md / Nd
        nucleo = A / 6

        if abs(e) < nucleo:
            sigma_max = (Nd / area_total) * (1 + 6 * abs(e) / A)
        elif abs(e) == nucleo:
            sigma_max = 2 * Nd / area_total
        else:
            if (A / 2 - abs(e)) > 0:
                sigma_max = 2 * Nd / (3 * B * (A / 2 - abs(e)))
            else:
                sigma_max = float("inf")
                
        frac_area = area_total / area_total if abs(e) <= nucleo else (3 * (A / 2 - abs(e)) * B) / area_total

        # PENALIZAÇÃO: Se a tensão ultrapassar o admissível
        if sigma_max > padm:
            v += (sigma_max - padm) * PESO_TENSAO
            
        # PENALIZAÇÃO: Se a área comprimida for menor que 50%
        if frac_area < 0.50:
            v += (0.50 - frac_area) * PESO_FATOR


    # 3) TOMBAMENTO E DESLIZAMENTO
    Mtomb = abs(M) + abs(H) * h_H
    Mestab = (N + P) * A / 2

    if Mtomb > 0:
        gamma_tomb = Mestab / Mtomb
        if gamma_tomb < 1.5:
            v += (1.5 - gamma_tomb) * PESO_FATOR


    # 4) COMPRESSÃO DIAGONAL
    u0 = 2 * (ap + bp)
    Fsd = Nd
    tau_sd = Fsd / (u0 * d)
    tau_rd2 = 0.27 * alfa_v(fck) * fcd_kN_cm2(fck, gamma_c)

    if tau_sd > tau_rd2:
        v += (tau_sd - tau_rd2) * PESO_TENSAO


    # 5) BIELA DE COMPRESSÃO (Se Rígida)
    if sapata_rigida:
        theta = radians(63.435)
        A1 = ap * bp
        A2 = (ap + 2 * d * tan(theta)) * (bp + 2 * d * tan(theta))
        
        sigma_atuante_pilar = Nd / A1
        sigma_atuante_X = Nd / A2
        fcd = fcd_kN_cm2(fck, gamma_c)
        
        sigma_lim_pilar = min(fcd * (A2 / A1) ** 0.5, 3.0 * fcd)
        sigma_lim_X = fcd

        if sigma_atuante_pilar > sigma_lim_pilar:
            v += (sigma_atuante_pilar - sigma_lim_pilar) * PESO_TENSAO
        if sigma_atuante_X > sigma_lim_X:
            v += (sigma_atuante_X - sigma_lim_X) * PESO_TENSAO

    return v