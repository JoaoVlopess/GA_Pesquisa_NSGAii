import random
from problem.definitions import calcular_f1, calcular_f2, checar_restricoes

def cria_cromossomo_aleatorio(tamanho):
    """
    Gera e retorna uma string binária aleatória para um cromossomo
    """
    return ''.join(random.choice('01') for _ in range(tamanho))


class cromossomo:
    def __init__(self, n_bits=8, v_min=-2.0, v_max=4.0, lim_sup=3, lim_inf=1, binario_input=None):
        self.n_bits = n_bits
        self.v_min = v_min  
        self.v_max = v_max 
        self.lim_inf = lim_inf  
        self.lim_sup = lim_sup  

        if binario_input is None:
            self.genes_binario = cria_cromossomo_aleatorio(self.n_bits)
        else:
            self.genes_binario = binario_input

        self.recalcular_metricas()

        self.rank = 0
        self.crowding_distance = 0.0
        self.dominado_contador = 0
        self.dominado_por = []
        self.domina_lista = []


    def decodificar_binario(self):
        valor_decimal = int(self.genes_binario, 2)
        resolucao = (self.v_max - self.v_min) / (2**self.n_bits - 1)
        return self.v_min + (valor_decimal * resolucao)

    def recalcular_metricas(self):
        """
        Atualiza todos os valores de decodificação, fitness e violação
        após uma alteração (mutação) nos genes binários.
        """
        self.x_real = self.decodificar_binario()

        self.f1 = calcular_f1(self.x_real)
        self.f2 = calcular_f2(self.x_real)
        self.viol_total = checar_restricoes(self.x_real, self.lim_inf, self.lim_sup)

        self.rank = 0
        self.crowding_distance = 0.0
        self.dominado_contador = 0
        self.domina_lista = []
        self.dominado_por = []

