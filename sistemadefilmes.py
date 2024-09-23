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
        except FileNotFoundError:
            return {}
# função para adicionar filmes ao arq .json (opcao 2)
def salvarfilmes(arqfilmes, filmes): # 'arqfilmes' é o arquivo json e 'filmes' é a função para abrir o arquivo
    # agora o parametro 'w' na função 'open' remete a 'write',
    # que vai abrir em forma de escrita 
    with open(arqfilmes, 'w') as f:
        json.dump(filmes, f, indent=4) # a funçao dump serializa o objeto e usa da funcao carregarfilmes para escrever e formatar com indent=4,
        # de forma a ser mais legivel com indentação de 4 espaços

arqfilmes = 'arqfilmes.json'
filmes = carregarfilmes(arqfilmes) # durante toda a execução do codigo filmes será a funçao carregarfilmes com o parâmetro do arquivo json.
# função para exibição do menu.
def menu():
    print(f"\n{len(filmes)} filmes disponíveis no momento!\nEscolha uma dessas opções: ") # len(filmes) sempre retornará o numero total de chaves do dicionário.
    print("1 -> Exibir dicionario de filmes completo ou trecho da mesma (ex: filmes na posicão 20-35)")
    print("2 -> Adicionar filme ao dicionario (armazenamento máximo: 50)")
    print("3 -> Remover filme do dicionario")
    print("4 -> Procurar filme por nome/diretor/ano/avaliacão")
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
    return any(filme['avaliacao'] == avaliacao for filme in filmes.values())
# 2 funçoes para as 2 sub-opções da opcao 1.
def op1a():
    print() 
    # for posicao, chave, valor dentro da enumeração dos itens de filmes vai exibir todos os filmes.
    for idx, (chave, valor) in enumerate(filmes.items()):
        print(f"{idx+1}° {chave} {valor}")
def op1b():
    posicao1 = int(input("Digite a posição inicial: "))
    posicao2 = int(input("Digite a posição final: "))
    for idx, (chave, valor) in enumerate(filmes.items()):
        if idx >= posicao1-1 and idx <= posicao2-1: # essa condicional verifica se o indice atual ta entre a 
            # posicao1 e a posicao2, e o -1 é pra voltar pra posicao 0 por que o indice começa em 0          
            print(f"\n{idx+1}° {chave} {valor}")
def submenu1(): # submenu para primeira opcao pra deixar o codigo mais limpo
    opcao2 = input("Exibir lista completa ou trecho? (c = completo / t = trecho): ").lower()
    while opcao2 not in ["c", "t"]:
        print("Opção inválida. Tente novamente.")
        opcao2 = input("Exibir lista completa ou trecho? (c = completo / t = trecho): ").lower()
    if opcao2 == "c":
        op1a()
    elif opcao2 == "t":
        op1b()
# função para o opcao 2 no menu            
def op2(filmes, arqfilmes):
    if len(filmes) == 50:
        print("O limite máximo de filmes foi atingido!")
    else:
        nome = str(input("nome do filme: (é preferivel que se digite o nome correto)"))
        ano = int(input("ano do filme: "))
        diretor = str(input("diretor do filme: "))
        avaliacao = float(input("avaliacao do filme (de 0 a 5): "))
        filmes[nome] = {"ano": ano, "diretor": diretor, "avaliação": avaliacao} # criacao de um novo dicionario apartir dessas definicoes.
        salvarfilmes(arqfilmes, filmes) # funcao pra salvar esse novo dicionario.
        print(f"{nome} adicionado com sucesso!")
# funcao para opcao 3 no menu 
# como o nome é a chave principal, pode se usar disso para deletar um conteudo inteiro do dicionario
def op3(filmes, arqfilmes): 
    nome = str(input("nome do filme a ser removido: ")).strip().lower()
    filmeremovido = False # controle de verificaçao se filme foi removido ou nao
    # lower() e strip() pra ter certeza que é igual ao nome do filme,
    # iterando sobre as chaves do dicionario
    for chave in list(filmes.keys()):
        if chave.strip().lower() == nome: # compara chave normalizada.
            del filmes[chave] # remove o filme.
            salvarfilmes(arqfilmes, filmes) # salva a alteração a partir da funcao .
            print(f"{chave} removido com sucesso!") 
            filmeremovido = True
    if not filmeremovido:
        print(f"{nome} não encontrado!")
# 4 funcoes em complemento da opcao 4.
# a primeira funcao busca pelo nome do filme. 
def op4nome(filmes):
    nome = str(input("nome do filme a ser procurado: ")).strip().lower() #strip e lower é pra quando o usuario escrever.
    posicao = -1  # inicializando uma variavel posicao pra manipular condicional, printar os parametros do dicionario e tornar 'bool' encontrado verdadeiro.
    encontrado = False # variavel booleana pra parar o for quando filme encontrado.
    for idx, (chave, valores) in enumerate(filmes.items(), start=1): # para indice(posicao), chave, valores nos itens do dicionario 'filmes' enumerado,
        # se a chave (que ta normalizada com strip() e lower()) for igual ao nome digitado pelo usuario,
        # atualize a posicao e diga que a posicao nao tem mais o valor inicial, portanto encontrado = True, fim da funcao.
        if chave.strip().lower() == nome:
            posicao = idx
            if posicao != -1:
                print(f"filme encontrado!\n{posicao}° {chave} {valores}")
                encontrado = True
    if not encontrado: # se encontrado = False print que o filme nao foi encontrado...
        print(f"{nome} não foi encontrado...")
# a segunda funcao vai buscar todos os filmes que possuem esse valor inteiro nos valores da chave 'ano'.
def op4ano(filmes):
    ano = int(input("ano do(s) filme(s) a ser(em) procurado(s): "))
    if verificarano(ano, filmes):
        encontrados = [] # inicializa uma lista para armazenar os filmes encontrados.
        for idx, (nome, chave) in enumerate(filmes.items(), start=1): 
            if chave['ano'] == ano: # comparando variavel do usuario com a chave 'ano' em filmes.
               encontrados.append((idx, nome, chave)) # armazenando os filmes encontrados na lista 'encontrados'.
        print(f"{len(encontrados)} filme(s) de {ano} encontrado(s):\n") # retornando o total de filmes encontrados a partir da lista.
        for idx, nome, chave in encontrados: # printando todos os elementos da lista 'encontrados'.
            print(f"{idx}° {nome} {chave}")
    else:
        print(f"filme(s) de {ano} não encontrado(s)...")
# funcao pra encontrar os filmes de um diretor (tem a mesma estrutura da anterior)
def op4diretor(filmes):
    diretor = str(input("diretor do(s) filme(s) a ser(em) procurado(s): ")).strip().lower()
    if verificardiretor(diretor, filmes):
        encontrados = []
        for idx, (nome, chave) in enumerate(filmes.items(), start=1):
            if chave['diretor'].lower() == diretor:
               encontrados.append((idx, nome, chave))
    if encontrados:
        print(f"{len(encontrados)} filme(s) de {diretor.title()} encontrado(s).\n")  # Usando title() para formatar o nome digitado pelo usuario. 
        for idx, nome, chave in encontrados:
            print(f"{idx}° {nome} {chave}")
    else:
        print(f"Nenhum filme dirigido por {diretor.title()} foi encontrado.")
# funcao pra achar filmes com a mesma avaliacao.
def op4av(filmes):
    av = float(input("nota do(s) filme(s) a ser(em) procurado(s): "))
    if verificaravaliacao(av, filmes):
        encontrados = []
        for idx, (nome, chave) in enumerate(filmes.items(), start=1):
            if chave['avaliacao'] == av:
               encontrados.append((idx, nome, chave))
        
        print(f"{len(encontrados)} filme(s) com nota {av} encontrado(s):\n")
        for idx, nome, chave in encontrados:
            print(f"{idx}° {nome} {chave}")
    else:
        print(f"filme(s) de nota {av} não encontrado(s)...")
def submenu4(filmes): # funcao pra evitar repeticao.
    opcoesvalidas = {"n": op4nome, "a": op4ano, "d": op4diretor, "av": op4av}
    opcao2 = input("Selecione uma opção:\nn -> nome\na -> ano\nd -> diretor\nav -> avaliação\n").lower()
    while opcao2 not in opcoesvalidas:
        print("Opção inválida. Tente novamente.")
        opcao2 = input("\nn -> nome\na -> ano\nd -> diretor\nav -> avaliação\n").lower()
    opcoesvalidas[opcao2](filmes)
# on = começa o loop do menu
# off = termina o loop do menu
on = True
off = False
# while pro menu, que dá 5 opcoes pro usuario, cada uma com funcoes diferentes, que foram definidas anteriormente.
while on:
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
        on = off 
        # kkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkk