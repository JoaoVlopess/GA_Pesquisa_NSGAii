from operator import attrgetter
from typing import List
from core.chromosome import cromossomo

def criar_populacao_inicial(tamanho):
    populacao = []
    
    limites_reais = [
            (50, 500), # Limites para A (Comprimento)
            (50, 500),  # Limites para B (Largura)
            (15, 200)   # Limites para h (Altura) 
    ]
    for _ in range(tamanho):
        
        populacao.append(cromossomo(n_bits_por_gene=8, limites=limites_reais))
    return populacao


def domina(X_A: cromossomo, X_B: cromossomo):
  """
  Verifica se o indivíduo X_A domina X_B com base na hierarquia de Restrições e Pareto.
  Return:
     True se X_A domina X_B, False caso contrário.
  """
  if X_A.viol_total == 0 and X_B.viol_total > 0:
        return True

  if X_B.viol_total == 0 and X_A.viol_total > 0:
        return False

  if X_A.viol_total > 0 and X_B.viol_total > 0:
        return X_A.viol_total < X_B.viol_total

  tao_bom_ou_melhor = (X_A.f1 <= X_B.f1) and (X_A.f2 <= X_B.f2)
  estritamente_melhor = (X_A.f1 < X_B.f1) or (X_A.f2 < X_B.f2)

  return tao_bom_ou_melhor and estritamente_melhor

def classificar_populacao_rank(populacao: list[cromossomo]):
  """
  Implementa o processo de Classificação de Não-Dominação (Ranking) do NSGA-II.
  """

  for C_i in populacao:
    C_i.domina_lista = []
    C_i.dominado_contador = 0
    C_i.rank = 0

    for C_j in populacao:
      if C_i is C_j: 
        continue
      if  domina(C_i,C_j):
        C_i.domina_lista.append(C_j)
      elif domina(C_j, C_i):
                C_i.dominado_contador += 1

  Frente_k = [p for p in populacao if p.dominado_contador == 0]
  rank_atual = 1

  while Frente_k:
    Frente_k_proxima = [] 
    for C_i in Frente_k:
            C_i.rank = rank_atual

            for C_j in C_i.domina_lista:
                C_j.dominado_contador -= 1

                if C_j.dominado_contador == 0: 
                    Frente_k_proxima.append(C_j)

    rank_atual += 1
    Frente_k = Frente_k_proxima 

  print(f"Classificação concluída. Ranks encontrados até: {rank_atual - 1}")


def calcular_crowding_distance(frente: list[cromossomo]):
  """
  Calcula a Crowding Distance para todos os indivíduos de uma frente.
  Indivíduos nas extremidades recebem distância infinita.
  """
  infinito = float('inf')

  if len(frente) <= 2:
      for ind in frente:
          ind.crowding_distance = infinito
      return

  menor_f1 = calcular_menor(frente, 'f1')
  maior_f1 = calcular_maior(frente, 'f1')
  menor_f2 = calcular_menor(frente, 'f2')
  maior_f2 = calcular_maior(frente, 'f2')

  menor_f1.crowding_distance = infinito
  maior_f1.crowding_distance = infinito
  menor_f2.crowding_distance = infinito
  maior_f2.crowding_distance = infinito

  min_amplitude = 1e-10 

  amplitude_f1 = max(maior_f1.f1 - menor_f1.f1, min_amplitude)
  amplitude_f2 = max(maior_f2.f2 - menor_f2.f2, min_amplitude)

  objetivos_a_processar = [
        ('f1', amplitude_f1),
        ('f2', amplitude_f2)
      ]

  for objetivo_nome, amplitude in objetivos_a_processar:
    frente_ordenada = sorted(frente, key=attrgetter(objetivo_nome))

    for i in range(1, len(frente_ordenada) - 1):
      C_i = frente_ordenada[i]
      C_anterior = frente_ordenada[i - 1]
      C_posterior = frente_ordenada[i + 1]

      valor_posterior = getattr(C_posterior, objetivo_nome)
      valor_anterior = getattr(C_anterior, objetivo_nome)

      C_i.crowding_distance += (valor_posterior - valor_anterior) / amplitude


def calcular_crowding_distance_todas_frentes(populacao: list[cromossomo]):
    """
    Calcula crowding distance para todas as frentes da população.
    """
    frentes = {}
    for ind in populacao:
        if ind.rank not in frentes:
            frentes[ind.rank] = []
        frentes[ind.rank].append(ind)

    for rank in sorted(frentes.keys()):
        calcular_crowding_distance(frentes[rank])

    print(f"Crowding distance calculada para {len(frentes)} frentes.")


def calcular_maior(lista, objetivo):
    return max(lista, key=attrgetter(objetivo))
def calcular_menor(lista, objetivo):

    return min(lista, key=attrgetter(objetivo))


def selecao_elitista(populacao_antiga, nova_prole, tamanho_pop):
  """
  Une a população antiga e sua prole
  return:
     retorna uma nova população baseada no calculo do elitismo nesse pool(pais + filhos)
  """
  pool = populacao_antiga + nova_prole

  classificar_populacao_rank(pool)
  calcular_crowding_distance_todas_frentes(pool)

  frentes = {}
  for crom in pool:
      if crom.rank not in frentes:
          frentes[crom.rank] = []
      frentes[crom.rank].append(crom)

  proxima_geracao = []
  ranks_ordenados = sorted(frentes.keys())

  for rank in ranks_ordenados:
      if len(proxima_geracao) >= tamanho_pop:
          break

      vagas_restantes = tamanho_pop - len(proxima_geracao)
      frente_atual = frentes[rank]

      if len(frente_atual) <= vagas_restantes:
            proxima_geracao.extend(frente_atual)
      else:
          frente_ordenada_cd = sorted(frente_atual, key=attrgetter('crowding_distance'), reverse=True)
          proxima_geracao.extend(frente_ordenada_cd[:vagas_restantes])

  return proxima_geracao
