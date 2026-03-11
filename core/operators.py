from typing import List
from core.chromosome import cromossomo
import random

def torneio(X_A: cromossomo, X_B: cromossomo):
    """
    Realiza torneio binário entre dois indivíduos.
    Critérios (em ordem de prioridade):
    1. Viabilidade (viável > inviável)
    2. Menor violação (se ambos inviáveis)
    3. Melhor rank (menor número)
    4. Maior crowding distance
    5. Aleatório (em caso de empate total)
    return:
        O indivíduo vencedor do torneio
    """
    if X_A.viol_total == 0 and X_B.viol_total > 0:
        return X_A
    if X_B.viol_total == 0 and X_A.viol_total > 0:
        return X_B

    if X_A.viol_total > 0 and X_B.viol_total > 0:
        if X_A.viol_total < X_B.viol_total:
            return X_A
        elif X_B.viol_total < X_A.viol_total:
            return X_B


    if X_A.rank < X_B.rank:
        return X_A
    elif X_B.rank < X_A.rank:
        return X_B

    if X_A.crowding_distance > X_B.crowding_distance:
        return X_A
    elif X_B.crowding_distance > X_A.crowding_distance:
        return X_B
    else:
        return random.choice([X_A, X_B])
    
def selecao_pais(populacao: list[cromossomo],tamanho_pool=None):
    """
    Seleciona pais através de torneios binários.
    Return:
        Lista de pais selecionados
    """
    if tamanho_pool is None:
        tamanho_pool = len(populacao)

    pool_pais = []

    while len(pool_pais) < tamanho_pool:
        competidores = random.sample(populacao, 2)

        vencedor = torneio(competidores[0], competidores[1])

        pool_pais.append(vencedor)

    return pool_pais

def cruzamento_dois_pontos(pais_selecionados: list[cromossomo], pc):
  """
  Faz o cruzamento de dois pontos em toda a lista de pais selecionados e recebe lista de pais selecionados e a probabilidade para cruzamanto
  return:
     nova prole/lista de cromossomos (pos cruzamento)
  """
  random.shuffle(pais_selecionados)
  nova_prole = []
  tamanho_cromossomo = len(pais_selecionados[0].genes_binario)

  num_pares = len(pais_selecionados) // 2

  for i in range(num_pares):
    pai1 = pais_selecionados[2*i]
    pai2 = pais_selecionados[2*i + 1]

    probabilidade_cruzamento = random.random()

    if probabilidade_cruzamento < pc:
      ponto1_cruzamento = random.randint(1, tamanho_cromossomo - 2)
      ponto2_cruzamento = random.randint(ponto1_cruzamento + 1, tamanho_cromossomo-1)

      cabeca_filho1 = pai1.genes_binario[:ponto1_cruzamento]
      meio_filho1 = pai2.genes_binario[ponto1_cruzamento:ponto2_cruzamento]
      cauda_filho1 = pai1.genes_binario[ponto2_cruzamento:]

      cabeca_filho2 = pai2.genes_binario[:ponto1_cruzamento]
      meio_filho2 = pai1.genes_binario[ponto1_cruzamento:ponto2_cruzamento]
      cauda_filho2 = pai2.genes_binario[ponto2_cruzamento:]

      filho1 = cabeca_filho1 + meio_filho1 + cauda_filho1
      filho2 = cabeca_filho2 + meio_filho2 + cauda_filho2

      nova_prole.append(cromossomo(binario_input=filho1))
      nova_prole.append(cromossomo(binario_input=filho2))
    else:
        nova_prole.append(cromossomo(binario_input=pai1.genes_binario))      
        nova_prole.append(cromossomo(binario_input=pai2.genes_binario))

  return nova_prole


def mutacao_bit_flip(nova_prole: list[cromossomo], pm):
    """
    Se o cromossomo for sorteado (probabilidade pm), 
    altera obrigatoriamente 1 bit aleatório de CADA um dos 5 atributos.
    """
    for cromossomo in nova_prole:
        chance_mutacao = random.random()

        if chance_mutacao < pm:
            bits = list(cromossomo.genes_binario)
            
            for inicio_bloco in range(0, len(bits), 8):
                posicao_relativa = random.randint(0, 7)
                posicao_real = inicio_bloco + posicao_relativa
                
                bits[posicao_real] = '1' if bits[posicao_real] == '0' else '0'
            
            cromossomo.genes_binario = "".join(bits)
            cromossomo.recalcular_metricas() 

    return nova_prole