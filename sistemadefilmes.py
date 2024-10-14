import json
# função para ler o arquivo json onde os filmes são armazenados.
def carregarfilmes(arqfilmes): 
        try: # comando try para executar o codigo do arquivo e caso haja exceção retornar uma lista vazia.
            # "with open" dá a garantia do arquivo abrir e fechar corretamente.
            # parâmetros: open(caminho, 'r', encoding='utf-8).
            # caminho é pra localizar o arquivo no repositorio, 'r' é pra abrir o mesmo no modo leitura e 
            # encoding utf=8 é pra reconhecer caracteres especiais da lingua portuguesa como 'ç' e '~'.
            with open(arqfilmes, 'r',  encoding='utf-8') as f: # as(como) f é só abreviação para a leitura do arquivo.
                return json.load(f) # retorno com funçao de carregamento(load) do arquivo json de filme como f.
        except FileNotFoundError: # conveniencia para o comando try
            return {}
# função para adicionar filmes ao arquivo .json (opcao 2)
def salvarfilmes(arqfilmes, filmes): # 'arqfilmes' é o arquivo json e 'filmes' é a função para abrir o arquivo
    # agora o parametro 'w' na função 'open' remete a 'write',
    # que vai abrir em forma de escrita 
    with open(arqfilmes, 'w') as f:
        json.dump(filmes, f, indent=4) # a funçao dump serializa o objeto e usa da funcao carregarfilmes para escrever e formatar com indent=4,
        # de forma a ser mais legivel com indentação de 4 espaços

arqfilmes = 'arqfilmes.json'
filmes = carregarfilmes(arqfilmes) # durante toda a execução do codigo "filmes" será a funçao carregarfilmes com o parâmetro do arquivo json.
# função para exibição do menu.
def menu():
    print(f"\n{len(filmes)} filmes disponíveis no momento!\nEscolha uma dessas opções: ") # len(filmes) sempre retornará o numero total de chaves do dicionário.
    print("1 -> Exibir lista de filmes completo ou trecho (ex: filmes na posicão 20-35)")
    print("2 -> Adicionar filme a lista (armazenamento máximo: 50 filmes)")
    print("3 -> Remover filme da lista")
    print("4 -> Procurar filme por nome/diretor/ano/classificação")
    print("5 -> Sair do programa")
# funcões que fazem parte da opção 4.
# o primeiro parametro é pra referenciar a chave pra retonar os valores, o segundo parâmetro (filmes) referencia a funcao carregarfilmes(leitura do arquivo).
# for filme in filmes.values acessa todos os valores de filmes supondo que filmes é um dicionario verificando as chaves dos mesmos.
# any vai retornar verdadeiro se houver qualquer elemento em filmes[chave].
def verificarano(ano, filmes):
    return any(filme['ano'] == ano for filme in filmes.values()) 
def verificardiretor(diretor, filmes): 
    return any(filme['diretor'].lower() == diretor.lower() for filme in filmes.values())
def verificaravaliacao(avaliacao, filmes):
    return any(filme['avaliação'] == avaliacao for filme in filmes.values())
# 2 funçoes para as 2 sub-opções da opcao 1.
def op1a():
    print() 
    # for posicao, chave, valor dentro da enumeração dos itens de filmes vai exibir todos os filmes.
    print("posição/nome")
    for posicao, (chave, valor) in enumerate(filmes.items()):
        print(f"{posicao+1}° {chave} {valor}")
def op1b():
    posicao1 = int(input("Digite a posição inicial: "))
    posicao2 = int(input("Digite a posição final: "))
    for posicao, (chave, valor) in enumerate(filmes.items()):
        if posicao >= posicao1-1 and posicao <= posicao2-1: # essa condicional verifica se o indice atual ta entre a 
            # posicao1 e a posicao2, e o -1 é pra voltar pra posicao 0 por que o indice começa em 0          
            print(f"{posicao+1}° {chave} {valor}")
    else:
        print("Não há filmes neste trecho, ou trecho inicial menor que o trecho final")
def submenu1(filmes): # submenu pra primeira opcao e pra deixar o codigo mais limpo
    opcao2 = input("Exibir lista completa ou trecho? (c = completo / t = trecho / v = voltar): ").lower()
    if opcao2 == "v":
        print()
    else:
        while opcao2 not in ["c", "t"]:
            print("Opção inválida. Tente novamente.")
            opcao2 = input("Exibir lista completa ou trecho? (c = completo / t = trecho / v = voltar): ").lower()
        if opcao2 == "c":
            op1a()
        elif opcao2 == "t":
            op1b()
        elif opcao == "v":
            print()
# função para o opcao 2 no menu            
def op2(filmes, arqfilmes):
    if len(filmes) == 50:
        print("O limite máximo de filmes foi atingido! Remova algum filme para adicionar mais")
    else:
        escolha = str(input("Tem certeza de que quer adicionar um filme? s/n\n")).strip().lower()
        if escolha in ["s","sim"]:
            nome = str(input("Nome do filme: (é preferivel que se digite o nome correto) "))
            ano = int(input("Ano do filme: "))
            diretor = str(input("Diretor do filme: "))
            avaliacao = float(input("Avaliacao do filme (de 0 a 5): "))
            filmes[nome] = {"ano": ano, "diretor": diretor, "avaliação": avaliacao} # criacao de um novo dicionario apartir dessas definicoes.
            salvarfilmes(arqfilmes, filmes) # funcao pra salvar esse novo dicionario.
            print(f"{nome} adicionado com sucesso!")
        elif escolha in ["n","nao","não"]:
            print("Operação cancelada!")
        else: 
            print("Opção inválida!")
            op2(filmes, arqfilmes)
# funcao para opcao 3 no menu.
# como o nome é a chave principal, pode se usar disso para deletar um conteudo inteiro do dicionario.
def op3(filmes, arqfilmes): 
    if len(filmes) == 0:
        print("Não há filmes para deletar!") # apartir do total de chaves da lista, se tiver 0, nada poderá ser deletado
    else: 
        escolha = str(input("tem certeza que quer remover um filme? s/n\n")).strip().lower()
        if escolha in ["s","sim"]:
            for posicao, (chave, valor) in enumerate(filmes.items()):
                print(f"{posicao+1}° {chave} {valor}")
            print("esses são os filmes que você pode remover!")

            nome = str(input("nome do filme a ser removido: ")).strip().lower()
            removerchave = None # variavel pra armazenar a chave que vai ser removida
            filmeremovido = False # controle de verificaçao se filme foi removido ou nao
            # lower() e strip() pra ter certeza que é igual ao nome do filme,
            # iterando sobre as chaves do dicionario
            for chave in filmes.keys():
                if chave.strip().lower() == nome: # compara chave normalizada.
                    removerchave = chave # se encontrar, armazena a chave que vai ser removida 
                    filmeremovido = True # define como verdadeiro ao encontrar chave do filme
            
            if filmeremovido: # filme removido agora é True 
                del filmes[removerchave] # deleta o filme
                salvarfilmes(arqfilmes, filmes) # salva as alterações
                print(f"{removerchave} removido com sucesso!")
            else:
                print("Filme não encontrado!")
               
        elif escolha in ["n","nao","não"]:
            print("Operação cancelada!")
        else:
            print("Opção inválida!")
            op3(filmes, arqfilmes)
# 4 funcoes em complemento da opcao 4.
# a primeira funcao busca pelo nome do filme. 
def op4nome(filmes):
    nome = str(input("nome do filme a ser procurado: ")).strip().lower() #strip e lower é pra quando o usuario escrever.
    posicao = -1  # inicializando uma variavel posicao pra manipular condicional, printar os parametros do dicionario e tornar 'bool' encontrado verdadeiro.
    encontrado = False # variavel booleana pra parar o for quando filme  encontrado.
    for idx, (chave, valores) in enumerate(filmes.items(), start=1): # para indice(posicao), chave, valores nos itens do dicionario 'filmes' enumerado,
        # se a chave (que ta normalizada com strip() e lower()) for igual ao nome digitado pelo usuario,
        # atualize a posicao e diga que a posicao nao tem mais o valor inicial, portanto encontrado = True, fim da funcao.
        if chave.strip().lower() == nome:
            posicao = idx
            if posicao != -1:
                print(f"\nfilme encontrado!\nposição/nome\n{posicao}° {chave} {valores}")
                encontrado = True
    if not encontrado: # se encontrado = False print que o filme nao foi encontrado...
        print(f"{nome} não foi encontrado...")
# a segunda funcao vai buscar todos os filmes que possuem esse valor inteiro nos valores da chave 'ano'.
def op4ano(filmes):
    ano = int(input("ano do(s) filme(s) a ser(em) procurado(s): "))
    if verificarano(ano, filmes):
        encontrados = [] # inicializa uma lista para armazenar os filmes encontrados.
        for posicao, (nome, chave) in enumerate(filmes.items(), start=1): 
            if chave['ano'] == ano: # comparando variavel do usuario com a chave 'ano' em filmes.
               encontrados.append((posicao, nome, chave)) # armazenando os filmes encontrados na lista 'encontrados'.
        print(f"{len(encontrados)} filme(s) de {ano} encontrado(s):\nposição / nome") # retornando o total de filmes encontrados a partir da lista.
        for posicao, nome, chave in encontrados: # printando todos os elementos da lista 'encontrados'.
            print(f"{posicao}° {nome} {chave}")
    else:
        print(f"filme(s) de {ano} não encontrado(s)...")
# funcao pra encontrar os filmes de um diretor (tem a mesma estrutura da anterior)
def op4diretor(filmes):
    diretor = str(input("diretor do(s) filme(s) a ser(em) procurado(s): ")).strip().lower()
    if verificardiretor(diretor, filmes):
        encontrados = []
        for posicao, (nome, chave) in enumerate(filmes.items(), start=1):
            if chave['diretor'].lower() == diretor:
               encontrados.append((posicao, nome, chave))
    if encontrados:
        print(f"{len(encontrados)} filme(s) de {diretor.title()} encontrado(s).\nposição / nome")  # Usando title() para formatar o nome digitado pelo usuario. 
        for posicao, nome, chave in encontrados:
            print(f"{posicao}° {nome} {chave}")
    else:
        print(f"Nenhum filme dirigido por {diretor.title()} foi encontrado.")
# funcao pra achar filmes com a mesma avaliacao.
def op4av(filmes):
    av = float(input("Nota do(s) filme(s) a ser(em) procurado(s): "))
    if verificaravaliacao(av, filmes):
        encontrados = []
        for posicao, (nome, chave) in enumerate(filmes.items(), start=1):
            if chave['avaliação'] == av:
               encontrados.append((posicao, nome, chave))
        
        print(f"{len(encontrados)} filme(s) com nota {av} encontrado(s):\nposição / nome")
        for posicao, nome, chave in encontrados:
            print(f"{posicao}° {nome} {chave}")
    else:
        print(f"Filme(s) de nota {av} não encontrado(s)...")
def submenu4(filmes): # submenu para alocar as 4 funcoes de busca nas chaves do dicionario 'submenu' 
    opcoesvalidas = {"n": op4nome, "a": op4ano, "d": op4diretor, "c": op4av}
    opcao2 = input("Selecione uma opção:\n(n) nome\n(a) ano\n(d) diretor\n(c) classificação\n(v) voltar\n").lower()
    if opcao2 == "v":
        return False # cancelando a funcao retornando false
    else:
        while opcao2 not in opcoesvalidas:
            print("Opção inválida. Tente novamente.")
            opcao2 = input("Selecione uma opção:\n(n) nome\n(a) ano\n(d) diretor\n(c) classificação\n(v) voltar\n").lower()
        opcoesvalidas[opcao2](filmes)

opcao = 0 
# while pro menu, que dá 5 opcoes pro usuario, cada uma com funcoes diferentes, que foram definidas anteriormente.
while opcao != 5:
    menu()
    opcao = int(input())
    while opcao < 1 or opcao > 5: # enquanto a opcao for menor menor que 1 ou maior que 5, a pergunta continua.
        print("Opção invalida, por favor escolha uma das opções acima.")
        opcao = int(input())
    
    if opcao == 1:
        submenu1(filmes)
    
    elif opcao == 2:
        op2(filmes, arqfilmes)
        
    elif opcao == 3:
        op3(filmes, arqfilmes)

    elif opcao == 4:
        submenu4(filmes)
    
    elif opcao == 5:
        print("Obrigado por utilizar nosso sistema...")
        exit()