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


def calculaIndividuos(qtdvertice):  # calcula a quantidade de individuos a serem gerados
    func_value = 17.5 * math.log(qtdvertice)
    resto = func_value / 2
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
        fitness, alocado = montaIndividuo(nos_copy, medianas_copy)
        while (alocado == False):
            nos_copy = copy.deepcopy(nos)
            medianas_copy = copy.deepcopy(medianas)
            sortMedianas(nos_copy, medianas_copy, qtdmedianas)
            fitness, alocado = montaIndividuo(nos_copy, medianas_copy)
        heapq.heappush(populacao, (fitness, medianas_copy))


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


def fazCruzamento(populacao, nos, qtdmedianas):
    filho = []
    selecionado = []
    possiveis = []
    pai = heapq.heappop(populacao)[1]
    mae = heapq.heappop(populacao)[1]
    for i in pai:
        possiveis.append(str(i.key))
        for j in mae:
            if i.key == j.key:
                filho.append(i)
                selecionado.append(str(i.key))
                break
    for j in mae:
        possiveis.append(str(j.key))
    for i in range(qtdmedianas - len(filho)):
        r = random.choice(possiveis)
        while r in selecionado:
            r = random.choice(possiveis)
        filho.append(nos[r])
        selecionado.append(r)
        possiveis.remove(r)
        nos.pop(str(r))
    fitness, alocado = montaIndividuo(nos, filho)
    return filho, fitness, alocado


def fazMutacao(populacao, nos, qtdmedianas):
    qtdIndividuosMutados = math.ceil(len(populacao) * 0.2)
    qtdElite = math.ceil(len(populacao) * 0.1)
    for i in range(qtdIndividuosMutados):
        original = random.choice(list(populacao)[qtdElite+1:])
        individuo = original[1]
        qtdMutacoes = random.randrange(
            1, qtdmedianas
        ) 
        nos_copy = copy.deepcopy(nos)
        for j in range(qtdMutacoes):
            escolhido = nos[random.choice(list(nos_copy))]
            nos_copy.pop(str(escolhido.key))
            nos_copy.update(
                {
                    str(individuo[j].key): no(
                        individuo[j].x,
                        individuo[j].y,
                        individuo[j].capacidade,
                        individuo[j].peso,
                        individuo[j].peso,
                        [],
                        individuo[j].key,
                    )
                }
            )
            individuo[j] = escolhido  # trocar elementos de no com individuo
            individuo[j].ligacoes = []
            individuo[j].ocupado = escolhido.peso
        newFitness, alocado = montaIndividuo(
            nos_copy, copy.deepcopy(individuo)
        )
        if(alocado and newFitness <= populacao[len(populacao)-1][0]):
            populacao.remove(original)
            heapq.heappush(populacao, (newFitness, individuo))
        else:
            i = i -1

def buscaLocal(populacao, nos, qtdmedianas, qtdvertice):
    for i in range (qtdmedianas):
        original = populacao[0]
        individuo = original[1]
        fitness = original[0]
        randomNos = []
        for k in range(qtdmedianas):
            aux = random.choice(list(nos))
            while aux in randomNos:
                aux = random.choice(list(nos))
            randomNos.append(aux)
        for index,j in enumerate(randomNos):
            nos_copy =  copy.deepcopy(nos)
            mediana_copy = copy.deepcopy(individuo)
            nos_copy[individuo[i].key] = copy.deepcopy(individuo[i])
            mediana_copy[i] = nos_copy.pop(randomNos[index])
            newFitness, alocado = montaIndividuo(nos_copy,mediana_copy)
            if (alocado and newFitness <= fitness):
                populacao[0] = (newFitness, mediana_copy)
                i = 0
                break

def montaIndividuo(nos, medianas):
    fitness = 0
    alocado = False
    for i in nos:
        alocado = False
        menorDistancia = []
        for (indice, j) in enumerate(medianas):
            heapq.heappush(
                menorDistancia, (calculaDistancia(nos[i].x, nos[i].y, j.x, j.y), j)
            )
        while menorDistancia != []:
            aux = heapq.heappop(menorDistancia)
            if aux[1].ocupado + nos[i].peso <= aux[1].capacidade:
                fitness += calculaDistancia(nos[i].x, nos[i].y, aux[1].x, aux[1].y)
                aux[1].ligacoes.append(nos[i].key)
                aux[1].ocupado += nos[i].peso
                menorDistancia = []
                alocado=True
            else:
                if(menorDistancia == []):
                    break
                aux = heapq.heappop(menorDistancia)
        if(alocado == False):
            break
    return fitness, alocado


nos = {}
medianas = []
individuos = []
populacao = []
qtdvertice, qtdmedianas = montaConjuto(nos)
montaPopulacao(copy.deepcopy(nos), calculaIndividuos(qtdvertice), medianas, qtdmedianas, populacao)
for i in range(100):
    nos_copy = copy.deepcopy(nos)
    filho, filho_fitness, normal = fazCruzamento(
        copy.deepcopy(populacao), nos_copy, qtdmedianas
    )
    if filho_fitness <= populacao[len(populacao) - 1][0] and normal:
        populacao.remove(populacao[len(populacao) - 1])
        heapq.heappush(populacao, (filho_fitness, filho))
    nos_copy = copy.deepcopy(nos)
    buscaLocal(populacao,nos_copy,qtdmedianas,qtdvertice)
    fazMutacao(populacao, nos_copy, qtdmedianas)
    print(populacao[0][0])
print(populacao[0][0])
