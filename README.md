# Otimização Multiobjetivo de Fundações de Torres Eólicas via NSGA-II

Este projeto utiliza o algoritmo genético **NSGA-II (Non-dominated Sorting Genetic Algorithm II)** para otimizar a geometria de fundações de torres eólicas (onshore). O objetivo principal é encontrar o equilíbrio ideal entre a minimização do volume de concreto (**Custo**) e a minimização do deslocamento horizontal (**Rigidez Estrutural**), utilizando o software **Abaqus** como motor de simulação por elementos finitos (FEA).

---

## 🚀 Funcionalidades e Inovações

- **Integração Python-Abaqus**: Fluxo de trabalho automatizado que gera o modelo geométrico, aplica cargas, processa a malha e extrai resultados do arquivo `.odb`.
- **Codificação Binária Customizada**: Representação de 5 atributos geométricos através de genes de 8 bits (total de 40 bits por cromossomo).
- **Mutação Híbrida com Viés de Significância**: Implementação original de uma lógica de mutação que prioriza o refino de precisão (bits menos significativos) para garantir a estabilidade da Frente de Pareto.
- **Análise de Sensibilidade**: Documentação do comportamento do algoritmo sob diferentes taxas de mutação (5%, 10% e 15%).

---

## 🛠️ Operadores Genéticos Implementados

### 1. Seleção e Cruzamento
- **Seleção**: Torneio binário baseado em *Crowding Distance* para manter a diversidade.
- **Crossover**: Cruzamento de ponto único aplicado às strings binárias.

### 2. Mutação Híbrida Estocástica (Versão Final)
A mutação foi desenvolvida para ser "inteligente", evitando a destruição de boas soluções:
- **Camada de Atributo**: A probabilidade de mutação ($P_m$) é testada individualmente para cada um dos 5 genes.
- **Intensidade Ponderada**: A quantidade de bits a serem alterados segue uma distribuição de pesos (Ex: 50% de chance para apenas 1 bit).
- **Viés de Qualidade**: 70% de probabilidade de a mutação ocorrer nos bits de menor importância (bits da direita), promovendo o ajuste fino (milimétrico) da estrutura.

---

## 🏗️ Variáveis de Projeto (Estrutura do Cromossomo)

O cromossomo de 40 bits controla as seguintes dimensões:
1. **R_base**: Raio da base da fundação.
2. **R_ped**: Raio do pedestal.
3. **H_i**: Altura inicial da base de concreto.
4. **H_f**: Altura final (transição) da base.
5. **H_ped**: Altura total do pedestal.

---

## 📊 Configurações de Execução Recomendadas

Para garantir a convergência e evitar a homogeneização da população (clones), utilize:
- **Tamanho da População**: 50 indivíduos.
- **Número de Gerações**: 20 a 30 iterações.
- **Taxa de Mutação ($P_m$)**: 0.10 (10%) por atributo.
- **Modelo de Solo**: Parâmetro geotécnico $q_d = 2.406$.

---

## 📂 Estrutura do Repositório

* `main.py`: Script principal que gerencia o loop evolutivo do NSGA-II.
* `definitions.py`: Contém a classe `Cromossomo` e as funções de crossover e mutação híbrida.
* `abaqus_script.py`: Script em Python (Abaqus API) responsável pela modelagem estrutural.
* `results_parser.py`: Módulo para leitura de dados de deslocamento e volume pós-processamento.

---

## 📈 Resultados Observados

Os testes demonstraram que a **Mutação Híbrida** superou os métodos tradicionais:
- **Estabilidade**: Alcançou deslocamentos estruturais consistentes de **~0.08mm**.
- **Economia**: Redução significativa de volume (~30m³ a menos comparado à mutação agressiva) para o mesmo nível de rigidez.
- **Diversidade**: Manutenção de uma Frente de Pareto rica, oferecendo múltiplas opções de projeto ao engenheiro.

---

## 🎓 Autor

Desenvolvido por **João Victor** como parte de pesquisa em Inteligência Artificial aplicada à Engenharia de Estruturas.

---
