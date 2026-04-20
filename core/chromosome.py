import random
from problem.definitions import calcular_f1, calcular_f2
from problem.restrictions import checar_restricoes_sapata

def cria_cromossomo_aleatorio(tamanho):
    """
    Gera e retorna uma string binária aleatória para um cromossomo
    """
    return ''.join(random.choice('01') for _ in range(tamanho))


class cromossomo:
    def __init__(self, n_bits_por_gene=8, limites=None, binario_input=None):
        self.n_bits_por_gene = n_bits_por_gene
        self.limites = limites if limites else [
            (100, 500), # Limites para A (Comprimento)
            (100, 500),  # Limites para B (Largura)
            (30, 150)   # Limites para h (Altura)
        ] 

        self.total_bits = len(self.limites) * self.n_bits_por_gene

        if binario_input is None:
            self.genes_binario = cria_cromossomo_aleatorio(self.total_bits)
        else:
            self.genes_binario = binario_input

        self.rank = 0
        self.crowding_distance = 0.0
        self.dominado_contador = 0
        self.dominado_por = []
        self.domina_lista = []

        self.recalcular_metricas()
        

    def decodificar_binario(self):
        """Transforma a string com todos os genes delimitado por uma quantidade de bits para cada gene em uma lista de 5 valores reais"""
        valores_reais = []
        
        for i in range(len(self.limites)):
            # Corta a string (ex: 0-8, 8-16, 16-24...)
            inicio = i * self.n_bits_por_gene
            fim = inicio + self.n_bits_por_gene
            segmento_binario = self.genes_binario[inicio:fim]
            
            valor_decimal = int(segmento_binario, 2)
            
            v_min, v_max = self.limites[i]
            resolucao = (v_max - v_min) / (2**self.n_bits_por_gene - 1)
            v_real = v_min + (valor_decimal * resolucao)
            
            valores_reais.append(v_real)
            
        return valores_reais

    def recalcular_metricas(self):
        """
        Atualiza todos os valores de decodificação, fitness e violação
        após uma alteração (mutação) nos genes binários.
        """
        self.valores = self.decodificar_binario()

        self.f1 = calcular_f1(self.valores)
        self.f2 = calcular_f2(self.valores)
        self.viol_total = checar_restricoes_sapata(self.valores)

        self.rank = 0
        self.crowding_distance = 0.0
        self.dominado_contador = 0
        self.domina_lista = []
        self.dominado_por = []

