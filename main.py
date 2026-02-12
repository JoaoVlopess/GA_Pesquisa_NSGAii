from core.nsga2_logic import criar_populacao_inicial, classificar_populacao_rank, calcular_crowding_distance_todas_frentes, selecao_elitista
from core.operators import selecao_pais, cruzamento_dois_pontos, mutacao_bit_flip
import matplotlib.pyplot as plt

TAMANHO_POP = 20
GERACOES = 10
PC = 0.8 
PM = 0.1

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


print("\n--- Top 5 Soluções na Frente de Pareto ---")
for i, ind in enumerate(frente_pareto[:5], 1):
    # ind.valores contém [R_base, R_ped, Hi, Hf, H_ped]
    r_b, r_p, hi, hf, hp = ind.valores 
    print(f"{i}. R_base={r_b:7.1f} | R_ped={r_p:7.1f} | f1={ind.f1:8.2f} | f2={ind.f2:.8f}")

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))
ax1.plot(historico_geraçoes, historico_f1_medio, color='blue', label='Média f1 (Volume)')
ax1.set_title('Evolução da Convergência - NSGA-II')
ax1.set_ylabel('Volume de Concreto (m³)')
ax1.legend()
ax1.grid(True)

ax2.plot(historico_geraçoes, historico_f2_medio, color='red', label='Média f2 (Deslocamento)')
ax2.set_xlabel('Geração')
ax2.set_ylabel('Deslocamento Máximo (mm)')
ax2.legend()
ax2.grid(True)

plt.tight_layout()
plt.show()

plt.figure(figsize=(8, 6))
volumes_pareto = [ind.f1 for ind in frente_pareto]
deslocamentos_pareto = [ind.f2 for ind in frente_pareto]

plt.scatter(volumes_pareto, deslocamentos_pareto, color='green', edgecolors='black', s=80, label='Soluções Ótimas')

plt.title('Frente de Pareto Final (Rank 1)')
plt.xlabel('Volume de Concreto (m³)')
plt.ylabel('Deslocamento Máximo (mm)')
plt.grid(True, linestyle='--', alpha=0.7)
plt.legend()

plt.tight_layout()
plt.show()
