from core.nsga2_logic import criar_populacao_inicial, classificar_populacao_rank, calcular_crowding_distance_todas_frentes, selecao_elitista
from core.operators import selecao_pais, cruzamento_dois_pontos, mutacao_bit_flip

TAMANHO_POP = 2
GERACOES = 1
PC = 0.8 
PM = 0.1

if __name__ == '__main__':
    populacao = criar_populacao_inicial(TAMANHO_POP)
    classificar_populacao_rank(populacao)
    calcular_crowding_distance_todas_frentes(populacao)

    print(f"Executando NSGA-II...")

    for g in range(1, GERACOES + 1):
        pais = selecao_pais(populacao)
        filhos = cruzamento_dois_pontos(pais, PC)
        filhos = mutacao_bit_flip(filhos, PM)

        populacao = selecao_elitista(populacao, filhos, TAMANHO_POP)

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
