import math
import numpy as np
import os
import subprocess
import time

# Caminhos

# Pega a pasta onde o arquivo atual (definitions.py) está salvo
DIRETORIO_ATUAL = os.path.dirname(os.path.abspath(__file__))
# Pega a pasta principal do projeto 
RAIZ_PROJETO = os.path.dirname(DIRETORIO_ATUAL)

# Caminhos Dinâmicos baseados na estrutura de pastas
CAMINHO_SCRIPT_ABAQUS = os.path.join(RAIZ_PROJETO, "IntegracaoAbaqus.py")
DIRETORIO_TRABALHO = os.path.join(RAIZ_PROJETO, "TempAbaqus")

# Cria a pasta temporária automaticamente se não existir no PC do professor
if not os.path.exists(DIRETORIO_TRABALHO):
    os.makedirs(DIRETORIO_TRABALHO)

ARQUIVO_INPUT = os.path.join(DIRETORIO_TRABALHO, "input_params.txt")
ARQUIVO_OUTPUT = os.path.join(DIRETORIO_TRABALHO, "output_result.txt")
CAMINHO_ABAQUS = "abaqus"

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
    # Escreve os genes para o Abaqus ler
    with open(ARQUIVO_INPUT, 'w') as f:
        f.write(",".join(map(str, valores)))

    # Chama o Abaqus em modo noGUI para rodar o script 
    # O comando abaixo assume que o script foi adaptado para ler o TXT
    comando = f'{CAMINHO_ABAQUS} cae noGUI="{CAMINHO_SCRIPT_ABAQUS}"'
    
    try:
        #Executa e espera terminar
        subprocess.check_call(comando, shell=True, cwd=DIRETORIO_TRABALHO)
        
        # Lê o resultado gerado pelo Abaqus
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
    
    # Restrições Geométricas 
    if R_base < (R_ped + 500): v += abs((R_ped + 500) - R_base)
    if Hf < Hi: v += abs(Hi - Hf)
    
    # Restrição de Pressão no Solo (Usando qd)
    # Pressão = Força Vertical / Área da Base
    area_base = math.pi * (R_base**2)
    forca_total = abs(2940 * 1000) # Fz em Newtons
    pressao_solo = forca_total / area_base
    
    if pressao_solo > QD_LIMITE:
        v += (pressao_solo - QD_LIMITE) * 1000 

    return v