import math
import heapq
import random
import copy

class no:
    x: int
    y: int
    capacidade: int
    ocupado: int
    peso: int
    ligacoes: []
    key: int

    def __init__(self, x, y, capacidade, ocupado, peso, ligacoes, key):
        self.x = x
        self.y = y
        self.capacidade = capacidade
        self.peso = peso
        self.ligacoes = ligacoes
        self.key = key
        self.ocupado = ocupado

    def __gt__(self, other):
        if not isinstance(other, no):
            # don't attempt to compare against unrelated types
            return NotImplemented
        return self.key > other.key

    def __lt__(self, other):
        if not isinstance(other, no):
            # don't attempt to compare against unrelated types
            return NotImplemented
        return self.key < other.key

    def toString(self):
        print(
            "{ x : %d, y : %d, capacidade : %d, ocupado : %d, peso : %d, indice : %d }"
            % (self.x, self.y, self.capacidade, self.ocupado, self.peso, self.key)
        )


def calculaDistancia(x1, y1, x2, y2):
    return math.sqrt(math.pow((x2 - x1), 2) + math.pow((y2 - y1), 2))


def montaConjuto(nos):
    lido = input().split(" ")
    lido = [num for num in lido if num]
    qtdvertice, qtdmedianas = int(lido[0]), int(lido[1])
    for i in range(qtdvertice):
        lido = input().split(" ")
        lido = [num for num in lido if num]
        nos.update(
            {
                str(i): no(
                    int(lido[0]),
                    int(lido[1]),
                    int(lido[2]),
                    int(lido[3]),
                    int(lido[3]),
                    [],
                    i,
                )
            }
        )
    return qtdvertice, qtdmedianas

def calculaIndividuos(nos,qtdvertice): #calcula a quantidade de individuos a serem gerados
    func_value = 17.5 * math.log(qtdvertice)
    resto = func_value/2
    if resto > 1:
        quantidade = math.ceil(func_value)
    elif resto < 1:
        quantidade = math.floor(func_value)
    elif resto == 1:
        quantidade = func_value - 1
    return quantidade

def montaPopulacao(nos, quantidade, medianas, qtdmedianas, populacao):
        for i in range(quantidade):
            nos_copy = copy.deepcopy(nos)
            medianas_copy = copy.deepcopy(medianas)
            sortMedianas(nos_copy, medianas_copy, qtdmedianas)
            fitness = montaIndividuo(nos_copy, medianas_copy)
            x = []
            for y in medianas_copy:
                x.append(str(y.key))
            populacao[str(x)] = fitness

def sortMedianas(nos, medianas, qtdmedianas):
    selecionados = []
    selecionados.append(random.randrange(0, len(nos)))
    for i in range(qtdmedianas):
        r = random.randrange(0, len(nos))
        while r in selecionados:
            r = random.randrange(0, len(nos))
        selecionados.append(r)
        element = nos[str(r)]
        medianas.append(element)
        nos.pop(str(element.key))


def montaIndividuo(nos, medianas):
    fitness = 0
    for i in nos:
        menorDistancia = []
        for (indice, j) in enumerate(medianas):
            heapq.heappush(
                menorDistancia, (calculaDistancia(nos[i].x, nos[i].y, j.x, j.y), j)
            )
        while menorDistancia != []:
            aux = heapq.heappop(menorDistancia)
            if aux[1].ocupado + nos[i].peso < aux[1].capacidade:
                fitness += calculaDistancia(nos[i].x, nos[i].y, aux[1].x, aux[1].y)
                aux[1].ligacoes.append(nos[i].key)
                aux[1].ocupado += nos[i].peso
                menorDistancia = []
            else:
                aux = heapq.heappop(menorDistancia)
    return fitness    

nos = {}
medianas = []
individuos = []
populacao = {}
qtdvertice, qtdmedianas = montaConjuto(nos)
montaPopulacao(nos,calculaIndividuos(nos,qtdvertice),medianas,qtdmedianas,populacao)
print(populacao)