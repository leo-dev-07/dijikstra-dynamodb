from graph_algs.Dijkstra import *
import pandas as pd

if __name__ == '__main__':
    # Aqui dentro serão definidas outras funções principais para o funcionamento do programa
    # Input com CSV
    def input_por_csv(path):
        df = pd.read_csv(path, sep=';')
        df.rename(index={0: 'de_onde', 1: 'para_onde', 2: 'peso'}, inplace=True)
        resultado_dijkstra = []
        adj_list = {'TER': 0, 'MAR': 1, 'LUA': 2, 'PLU': 3, 'NET': 4}

        try:
            for row, col in df.iterrows():
                print('De onde?')
                de_onde = col['de_onde']

                print('Para onde?')
                para_onde = col['para_onde']

                de_onde_input = ''
                para_onde_input = ''

                for i, j in adj_list.items():
                    if de_onde == i:
                        de_onde_input = int(j)

                    if para_onde == i:
                        para_onde_input = int(j)
                #C:\Users\Administrador\Desktop\PLANETAS_TESTE.csv

                resultado_dijkstra = g.caminho_entre_dois_pontos(int(de_onde_input), int(para_onde_input),adj_list)
                resultado_dijkstra['de_onde_para_onde'] = '{0}-{1}'.format(col['de_onde'], col['para_onde'])
                tabela = DynamoApi()
                tabela.table_name = 'planetas-v1'
                tabela.key_schema = key_schema
                tabela.atr_def = atr_def
                tabela.insertItem(resultado_dijkstra)
        except Exception as e:
            traceback.print_exc()
            print('Os dados podem não ter sido carregados completamente')


    # Key schema
    key_schema = [
        {
            'AttributeName': 'de_onde_para_onde',
            'KeyType': 'HASH'
        },
        {
            'AttributeName': 'caminho',
            'KeyType': 'RANGE'
        }
    ]

    # Atr_def
    atr_def = [
        {
            'AttributeName': 'de_onde_para_onde',
            'AttributeType': 'S'
        },
        {
            'AttributeName': 'caminho',
            'AttributeType': 'S'
        }
    ]


    # Input manual
    def criaTabela():
        try:
            dyndb = DynamoApi()
            dyndb.table_name = 'planetas-v1'
            dyndb.key_schema = key_schema
            dyndb.atr_def = atr_def
            dyndb.createTable(dyndb.key_schema, dyndb.atr_def)
            print('Tabela criada com sucesso.')
        except Exception as e:
            print(e)
            print('A tabela não foi recriada:', e)
            pass

    criaTabela()

    def input_manual():
        print('Selecione o caminho:')

        print('De onde?')
        de_onde = input()

        print('Para onde?')
        para_onde = input()

        de_onde_input = ''
        para_onde_input = ''

        for i, j in adj_list.items():
            if de_onde == i:
                de_onde_input = int(j)

            if para_onde == i:
                para_onde_input = int(j)

        resultado_dijkstra1 = g.caminho_entre_dois_pontos(de_onde_input, para_onde_input, adj_list)
        print(resultado_dijkstra1)
        resultado_dijkstra1['de_onde_para_onde'] = '{0}-{1}'.format(de_onde, para_onde)
        tabela = DynamoApi()
        tabela.table_name = 'planetas-v1'
        tabela.key_schema = key_schema
        tabela.atr_def = atr_def
        tabela.insertItem(resultado_dijkstra1)

        tabela.getItem({'de_onde_para_onde': 'TER-PLU', 'caminho': "['TER', 'MAR', 'NET', 'LUA', 'TER']"})


    g = Grafo(7)

    # Lista de vértices nomeada
    adj_list = {'TER': 0, 'MAR': 1, 'LUA': 2, 'PLU': 3, 'NET': 4}

    # Criação da matriz de adjacências com os vértices e seus respectivos pesos
    g.adiciona_aresta(adj_list['TER'], adj_list['MAR'], 10)
    g.adiciona_aresta(adj_list['MAR'], adj_list['LUA'], 5)
    g.adiciona_aresta(adj_list['TER'], adj_list['PLU'], 75)
    g.adiciona_aresta(adj_list['TER'], adj_list['LUA'], 20)
    g.adiciona_aresta(adj_list['TER'], adj_list['NET'], 56)
    g.adiciona_aresta(adj_list['NET'], adj_list['PLU'], 5)
    g.adiciona_aresta(adj_list['LUA'], adj_list['NET'], 20)

    # Exibe a matriz de adjacências
    g.mostra_matriz()

    print('Qual tipo de entrada você deseja?')
    print('1-Manual')
    print('2-CSV')
    entrada = str(input())

    if entrada == '1':
        input_manual()
    else:
        print('Qual o caminho do arquivo?')
        csv_entrada = str(input())
        try:
            input_por_csv(csv_entrada)
        except Exception as e:
            print('Entrada errada: ', e)