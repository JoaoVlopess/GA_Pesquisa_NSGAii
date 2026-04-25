from core.nsga2_logic import criar_populacao_inicial, classificar_populacao_rank, calcular_crowding_distance_todas_frentes, selecao_elitista
from core.operators import selecao_pais, cruzamento_dois_pontos, mutacao_bit_flip
import matplotlib.pyplot as plt
import os

TAMANHO_POP = 50
GERACOES = 50
PC = 0.8 
PM = 0.15

if __name__ == '__main__':
    populacao = criar_populacao_inicial(TAMANHO_POP)
    classificar_populacao_rank(populacao)
    calcular_crowding_distance_todas_frentes(populacao)

    print(f"Executando NSGA-II...")

    historico_geraçoes = list(range(1, GERACOES + 1))
    historico_f1_medio = []
    historico_f2_medio = []

    for g in range(1, GERACOES + 1):
        pais = selecao_pais(populacao)
        filhos = cruzamento_dois_pontos(pais, PC)
        filhos = mutacao_bit_flip(filhos, PM)

        populacao = selecao_elitista(populacao, filhos, TAMANHO_POP)
        media_f1 = sum(ind.f1 for ind in populacao) / len(populacao)
        media_f2 = sum(ind.f2 for ind in populacao) / len(populacao)
        historico_f1_medio.append(media_f1)
        historico_f2_medio.append(media_f2)

        if g % 10 == 0:
            rank1 = [ind for ind in populacao if ind.rank == 1]
            print(f"Geração {g:3d} | Indivíduos no Rank 1: {len(rank1)}")

    frente_pareto = [ind for ind in populacao if ind.rank == 1]
    frente_pareto.sort(key=lambda x: x.f1) 


print("\n--- Top 10 Soluções na Frente de Pareto ---")
for i, ind in enumerate(frente_pareto[:10], 1):
    # Agora descompactamos apenas 3 valores: A, B, h
    a_sap, b_sap, h_sap = ind.valores 
    print(f"{i}. A={a_sap:7.1f}cm | B={b_sap:7.1f}cm | h={h_sap:7.1f}cm | f1={ind.f1:8.2f}m³ | f2={ind.f2:8.2f}kg | Viol={ind.viol_total:.2f}")

# --- Gráfico de Evolução (Convergência) ---
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))

ax1.plot(historico_geraçoes, historico_f1_medio, color='blue', marker='o', label='Média f1 (Volume)')
ax1.set_title('Evolução da Convergência - NSGA-II')
ax1.set_ylabel('Volume de Concreto (m³)')
ax1.legend()
ax1.grid(True)

ax2.plot(historico_geraçoes, historico_f2_medio, color='red', marker='s', label='Média f2 (Peso do Aço)')
ax2.set_xlabel('Geração')
ax2.set_ylabel('Peso Total de Aço (kg)')
ax2.legend()
ax2.grid(True)

plt.tight_layout()
plt.show()

# --- Gráfico da Frente de Pareto Final ---
plt.figure(figsize=(8, 6))
volumes_pareto = [ind.f1 for ind in frente_pareto]
pesos_aco_pareto = [ind.f2 for ind in frente_pareto]

plt.scatter(volumes_pareto, pesos_aco_pareto, color='green', edgecolors='black', s=80, label='Soluções Ótimas (Rank 1)')

plt.title('Frente de Pareto Final - Sapata Retangular')
plt.xlabel('Volume de Concreto (m³)')
plt.ylabel('Peso Total de Aço (kg)')
plt.grid(True, linestyle='--', alpha=0.7)
plt.legend()

plt.tight_layout()
plt.show()