import math
import numpy as np
import os
import subprocess
import time

# Constantes
CAMINHO_ABAQUS = "abaqus" # Ou o caminho completo para o executável .bat do Abaqus
DIRETORIO_TRABALHO = r"C:\TestPython"
ARQUIVO_INPUT = os.path.join(DIRETORIO_TRABALHO, "input_params.txt")
ARQUIVO_OUTPUT = os.path.join(DIRETORIO_TRABALHO, "output_result.txt")

# DIMENSIONS
R_base = 7000
R_pedestal = 2000.0
Hi_base = 500.0
Hf_base = 2000.0
H_pedestal = 2000.0
Size_mesh = 1500

# MATERIAL
GamaC = 30  # kN/m³
GamaS = 18  # kN/m³
qd = 2406.44

#VALUES FOR ABAQUS
density = 25000.0
young_modulus = 5600 * math.sqrt(GamaC) * 1000000
poisson = 0.2

#IMPUT - LOADS
Fres = 750  # kN.m    #HORIZONTAL LOAD
Fz = 2940  # kN       #VERTICAL LOAD
Mres = 64215  # kN.m  #BENDING MOMENT
Mz = 3060  # kN.m     #TWISTING MOMENT
t = 0.6  # m - HEIGHT FROM THE GROUND TO THE POINT WHERE LOADS ARE DEFINED

#VALUES FOR ABAQUS
Load_Fx = 0           #HORIZONTAL LOAD
Load_Fy = 750000      #HORIZONTAL LOAD
Load_Fz = -2940000    #VERTICAL LOAD
Load_Mx = -64215000   #BENDING MOMENT
Load_My = 0           #BENDING MOMENT
Load_Mz = 3060000     #TWISTING MOMENT


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
    comando = f'{CAMINHO_ABAQUS} cae noGUI=IntegracaoAbaqus.py'
    
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
    """Retorna a soma das violações"""
    R_base, R_ped, Hi, Hf, H_ped = valores
    v = 0
    
    # 1. Raio da base deve ser maior que o do pedestal (margem de 500mm)
    if R_base < (R_ped + 500):
        v += abs((R_ped + 500) - R_base)
        
    # 2. Espessura no centro deve ser maior que na borda
    if Hf < Hi:
        v += abs(Hi - Hf)
        
    return v