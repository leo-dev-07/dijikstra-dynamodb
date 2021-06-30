# dijikstra-dynamodb
Algorítmo de dijikstra implementado com heap mínimo para achar o caminho mais curto em um grafo, salvando o resultado em uuma tabela no DynamoDB usando a SDK da AWS. Ele suporta entradas manuais e entradas de CSV separadas por ';'

<!--ts-->
   * 
      Este é o algorítmo de Dijkstra implementado com um heap mínimo para achar o caminho mais curto entre vértices de um grafo.
      Ele faz parte de um jogo de seleção de caminhos entre 2 planetas, onde o algorítmo te retornará o melhorr caminho a ser feito e o custo para faze-lo.
      Para deixar mais divertido, ele grava os resultados em um DynamoDB. Por tanto, recomendo que tenham uma conta na AWS, configurem o CLI e as configurações de segurança para         que absolutamente tudo dê certo.
      
   * 
      Simplesmente inicie o arquivo main.py e escolha o tipo de input utilizado para o início do arquivo. Depois ele te solicitará um caminho que você deseja fazer, e depois te
      retornará o resultado no terminal e salvará o resultado no seu DynamoDB em uma tabela já pré configurada.
      * [Pre Requisitos](#pre-requisitos)
        Python, AWS DynamoDB
  
