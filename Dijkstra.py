import math
import pandas as pd
import boto3
import traceback

#Algoritimo de dijkstra implementado com HeapMin.
class HeapMin:

    def __init__(self):
        self.nos = 0
        self.heap = []
    #Adiciona um nó ao grafo com seus respectivo peso e índice
    def adiciona_no(self, u, indice):
        self.heap.append([u, indice])
        self.nos += 1
        f = self.nos
        while True:
            if f == 1:
                break
            p = f // 2
            #Faz o heap para classificar em qual nó está o grafo dentro do nível de da árvore
            if self.heap[p-1][0] <= self.heap[f-1][0]:
                break
            else:
            #Heap fy down para os heaps que não estiverem dentro da condição
                self.heap[p-1], self.heap[f-1] = self.heap[f-1], self.heap[p-1]
                f = p
    #Exibe o heap
    def mostra_heap(self):
        print('A estrutura heap é a seguinte:')
        nivel = int(math.log(self.nos, 2))
        a = 0
        for i in range(nivel):
            for j in range(2 ** i):
                print(f'{self.heap[a]}', end='  ')
                a += 1
            print('')
        for i in range(self.nos-a):
            print(f'{self.heap[a]}', end='  ')
            a += 1
        print('')
    #Muda o nóde posição dentro do grafo
    def remove_no(self):
        x = self.heap[0]
        self.heap[0] = self.heap[self.nos - 1]
        self.heap.pop()
        self.nos -= 1
        p = 1
        while True:
            f = 2 * p
            if f > self.nos:
                break
            if f + 1 <= self.nos:
                if self.heap[f][0] < self.heap[f-1][0]:
                    f += 1
            if self.heap[p-1][0] <= self.heap[f-1][0]:
                break
            else:
                self.heap[p-1], self.heap[f-1] = self.heap[f-1], self.heap[p-1]
                p = f
        return x

    def tamanho(self):
        return self.nos
    #Check de menor elemento
    def menor_elemento(self):
        if self.nos != 0:
            return self.heap[0]
        return 'A árvore está vazia'

    #Check do nó filho da esquerda
    def filho_esquerda(self, u):
        if self.nos >= 2*u:
            return self.heap[2*u-1]
        return 'Esse nó não tem filho'

    #Check do nó filho da direita
    def filho_direita(self, u):
        if self.nos >= 2*u+1:
            return self.heap[2*u]
        return 'Esse nó não tem filho da direita'
    #Check do nó pai
    def pai(self, u):
        return self.heap[u // 2]

#Implementação do grapho usando o conseito do de lista de adjacências
class Grafo:

    def __init__(self, vertices):
        self.vertices = vertices
        self.grafo = [[0] * self.vertices for i in range(self.vertices)]

    #Adiciona aresta com suas respectivas conexões e seu pesos de ida e volta
    def adiciona_aresta(self, u, v, peso):
        self.grafo[u-1][v-1] = peso
        self.grafo[v-1][u-1] = peso

    #Adiciona aresta com suas respectivas conexões e seu pesos de ida e volta
    def mostra_matriz(self):
        print('A matriz de adjacências é:')
        for i in range(self.vertices):
            print(self.grafo[i])

    #Implementação do algoritmo de Djkstra
    def dijkstra(self, origem):
        #Inicia o gráfo colocando ifinito em todos os nós
        custo_vem = [[-1, 0] for i in range(self.vertices)]

        #Coloca
        custo_vem[origem - 1] = [0, origem]
        h = HeapMin()
        h.adiciona_no(0, origem)
        while h.tamanho() > 0:
            dist, v = h.remove_no()
            for i in range(self.vertices):
                if self.grafo[v-1][i] != 0:
                    if custo_vem[i][0] == -1 or custo_vem[i][0] > dist + self.grafo[v-1][i]:
                        custo_vem[i] = [dist + self.grafo[v-1][i], v]
                        h.adiciona_no(dist + self.grafo[v-1][i], i+1)
        return custo_vem

    def formata_dijkstra(self, dic, list, para_onde):
        soma_caminho=0
        caminho_formatado=[]

        for i in list:
            soma_caminho += i[0]
            print(i)
            for k, v in dic.items():
                if i[1] == v:
                    print('KKKKKKKK',k,v,i[1])
                    caminho_formatado.append(k)
                    if i[1] == para_onde:
                        return {'caminho': str(caminho_formatado),
                                'peso_final': soma_caminho}


            if i[0] == -1:
                return {'caminho': str(caminho_formatado),
                        'peso_final': soma_caminho}

    def caminho_entre_dois_pontos(self, de_onde, para_onde, dic):
        adj_list = self.dijkstra(de_onde)
        print(adj_list)
        index=0

        print('Resultado final:')
        caminho=self.formata_dijkstra(dic,adj_list,para_onde)
        return caminho

#Descrição do comportamento da API
class DynamoApi:
    def __init__(self):
        self.table_name = ''
        self.key_schema = []
        self.atr_def = []
        self.prov_thr = {'ReadCapacityUnits': 10,
                         'WriteCapacityUnits': 10}
        self.dynamodb = boto3.resource('dynamodb')

    #Cria tabela
    def createTable(self,key_schema,att_def):
        table = self.dynamodb.create_table(
            TableName=self.table_name,
            KeySchema=key_schema,
            AttributeDefinitions=att_def,
            ProvisionedThroughput=self.prov_thr
        )
        table.meta.client.get_waiter('table_exists').wait(TableName=self.table_name)
        print(table.item_count)
        print('Create Table')

        return table
    #Insere item no banco de dados
    def insertItem(self,item):
        try:
            table = self.dynamodb.Table(self.table_name)
            table.put_item(Item=item)

            print('Item Inserido')
        except Exception as e:
            print('Item Não inserido: ',e)
            traceback.print_exc()

    #Pega item no banco de dados
    def getItem(self, item):
        table = self.dynamodb.Table(self.table_name)
        return table.get_item(Key=item)


