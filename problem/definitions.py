import math
import numpy as np
import os
import subprocess
import time

# Caminhos
CAMINHO_SCRIPT_ABAQUS = r"C:\Users\caioj\OneDrive\Área de Trabalho\pesquisa\nsga2_first\IntegracaoAbaqus.py"
CAMINHO_ABAQUS = "abaqus" 
DIRETORIO_TRABALHO = r"C:\TestPython"
ARQUIVO_INPUT = os.path.join(DIRETORIO_TRABALHO, "input_params.txt")
ARQUIVO_OUTPUT = os.path.join(DIRETORIO_TRABALHO, "output_result.txt")

QD_LIMITE = 2.406


def calcular_f1(valores):
    """Minimizar Volume de Concreto (m³)"""
    R_base, R_ped, Hi, Hf, H_ped = valores
    
    # Convertendo de mm para m 
    rb, rp, hi, hf, hp = [v/1000 for v in valores]
    
    vol_pedestal = math.pi * (rp**2) * hp
    vol_base = math.pi * (rb**2) * ((hi + hf) / 2)
    
    return vol_pedestal + vol_base

def calcular_f2(valores):
    """Interface com Abaqus via Arquivo TXT"""
    # 1. Escreve os genes para o Abaqus ler
    with open(ARQUIVO_INPUT, 'w') as f:
        f.write(",".join(map(str, valores)))

    # 2. Chama o Abaqus em modo noGUI para rodar o script do professor
    # O comando abaixo assume que o script do professor foi adaptado para ler o TXT
    comando = f'{CAMINHO_ABAQUS} cae noGUI="{CAMINHO_SCRIPT_ABAQUS}"'
    
    try:
        # Executa e espera terminar
        subprocess.check_call(comando, shell=True, cwd=DIRETORIO_TRABALHO)
        
        # 3. Lê o resultado gerado pelo Abaqus
        time.sleep(1) # Pequena pausa para garantir que o arquivo fechou
        with open(ARQUIVO_OUTPUT, 'r') as f:
            max_u3 = float(f.read().strip())
        return max_u3
    
    except Exception as e:
        print(f"Erro ao rodar Abaqus: {e}")
        return 999999.0 # Penalidade alta se a simulação falhar

def checar_restricoes(valores):
    R_base, R_ped, Hi, Hf, H_ped = valores
    v = 0
    
    # 1. Restrições Geométricas (Já tínhamos)
    if R_base < (R_ped + 500): v += abs((R_ped + 500) - R_base)
    if Hf < Hi: v += abs(Hi - Hf)
    
    # 2. Restrição de Pressão no Solo (Usando qd)
    # Pressão = Força Vertical / Área da Base
    area_base = math.pi * (R_base**2)
    forca_total = abs(2940 * 1000) # Fz em Newtons
    pressao_solo = forca_total / area_base
    
    if pressao_solo > QD_LIMITE:
        # Se a pressão no solo for maior que o qd, temos uma violação!
        v += (pressao_solo - QD_LIMITE) * 1000 

    return v