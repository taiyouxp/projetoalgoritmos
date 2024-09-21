import json
# função para ler o arquivo json onde os filmes são armazenados
def carregarfilmes(arqfilmes): 
        try: # comando try para executar o codigo do arquivo e caso haja exceção retornar uma lista vazia
            # "with open" dá a garantia do arquivo abrir e fechar corretamente
            # parâmetros: open(caminho, 'r', encoding='utf-8)
            # caminho é pra localizar o arquivo no repositorio, 'r' é pra abrir o mesmo no modo leitura e 
            # encoding utf=8 é pra reconhecer caracteres especiais da lingua portuguesa como 'ç' e '~'
            with open(arqfilmes, 'r',  encoding='utf-8') as f: # as(como) f é só abreviação para a leitura do arquivo
                return json.load(f) # retorno com funçao de carregamento(load) do arquivo json de filme como f 
        except FileNotFoundError:
            return {}
# função para adicionar filmes ao arq .json (opcao 2)
def salvarfilmes(arqfilmes, filmes): # 'arqfilmes' é o arquivo json e 'filmes' é a função para abrir o arquivo
    # agora o parametro 'w' na função 'open' remete a 'write',
    # que vai abrir em forma de escrita 
    with open(arqfilmes, 'w') as f:
        json.dump(filmes, f, indent=4) # a funçao dump serializa o objeto e usa da funcao carregarfilmes para escrever e formatar com indent=4
        # de forma a ser mais legivel com indentação de 4 espaços

arqfilmes = 'arqfilmes.json'
filmes = carregarfilmes(arqfilmes) # durante toda a execução do codigo filmes será a funçao carregarfilmes com o parâmetro do arquivo json
# função para exibição do menu
def menu():
    print(f"\n{len(filmes)} filmes disponíveis no momento!\nEscolha uma dessas opções: ") # len(filmes) sempre retornará o numero total de chaves do dicionário
    print("1 -> Exibir dicionario de filmes completo ou trecho da mesma (ex: filmes na posicão 20-35)")
    print("2 -> Adicionar filme ao dicionario (armazenamento máximo: 50)")
    print("3 -> Remover filme do dicionario")
    print("4 -> Procurar filme por nome/diretor/ano/avaliacão")
    print("5 -> Sair do programa")
# funcões que fazem parte da opção 4 
# o primeiro parametro é pra refereciar a chave retonar os valores, o segundo parâmetro (filmes) referencia a funcao carregarfilmes(leitura do arquivo)
# for filme in filmes.values acessa todos os valores de filmes supondo que filmes é um dicionario verificando as chaves dos mesmos
# any vai retornar verdadeiro se houver qualquer elemento em filmes[chave]
def verificarnome(nome, filmes):
    return nome in filmes # nome é a chave principal por isso não há necessidade do uso da função any
def verificarano(ano, filmes):
    return any(filme['ano'] == ano for filme in filmes.values()) 
def verificardiretor(diretor, filmes): 
    return any(filme['diretor'].lower() == diretor.lower() for filme in filmes.values())
def verificaravaliacao(avaliacao, filmes):
    return any(filme['avaliacao'] == avaliacao for filme in filmes.values())
# 2 funçoes para as 2 sub-opções da opcao 1
def op1a():
    print() 
    # for posicao, chave, valor dentro da enumeração dos itens de filmes vai exibir todos os filmes
    for idx, (chave, valor) in enumerate(filmes.items()):
        print(f"{idx+1}° {chave} {valor}")
def op1b():
    posicao1 = int(input("Digite a posição inicial: "))
    posicao2 = int(input("Digite a posição final: "))
    for idx, (chave, valor) in enumerate(filmes.items()):
        if idx >= posicao1-1 and idx <= posicao2-1: # essa condicional verifica se o indice atual ta entre a 
            # posicao1 e a posicao2, e o -1 é pra voltar pra posicao 0 por que o indice começa em 0          
            print(f"\n{idx+1}° {chave} {valor}")
# função para o opcao 2 no menu            
def op2(filmes, arqfilmes):
    if len(filmes) == 50:
        print("O limite máximo de filmes foi atingido!")
    else:
        nome = str(input("nome do filme: "))
        ano = int(input("ano do filme: "))
        diretor = str(input("diretor do filme: "))
        avaliacao = float(input("avaliacao do filme (de 0 a 5): "))
        filmes[nome] = {"ano": ano, "diretor": diretor, "avaliação": avaliacao} # criacao de um novo dicionario apartir dessas definicoes
        salvarfilmes(arqfilmes, filmes) # funcao pra salvar esse novo dicionario
        print(f"{nome} adicionado com sucesso!")
# funcao para opcao 3 no menu 
# como o nome é a chave principal pode ser usar disso para deletar um conteudo inteiro do dicionario
def op3(filmes, arqfilmes): 
    nome = str(input("nome do filme a ser removido: ")).strip().lower()
    filmeremovido = False # controle de verificaçao se filme foi removido ou nao
         # lower() e strip() pra ter certeza que é igual ao nome do filme
    # iterando sobre as chaves do dicionario
    for key in list(filmes.keys()):
        if key.strip().lower() == nome: # compara chave normalizada 
            del filmes[key] # remove o filme
            salvarfilmes(arqfilmes, filmes) # salvar a alteração
            print(f"{key} removido com sucesso!") 
            filmeremovido = True
    
    if not filmeremovido:
        print(f"{nome} não encontrado!")
# 4 funcoes em complemento da opcao 4
def op4nome(filmes):
    nome = str(input("nome do filme a ser procurado: ")).strip().lower()
    if verificarnome(nome, filmes):
        print(f"\n{nome} encontrado! {filmes[nome]}")   
        posicao = -1
        for idx, chave in enumerate(filmes.keys(), start=1):
            if chave == nome:
                posicao = idx
        if posicao != -1:
            print(f"Posição: {posicao}°")
    else:
        print(f"{nome} não encontrado...")
def op4ano(filmes):
    ano = int(input("ano do(s) filme(s) a ser(em) procurado(s): "))
    if verificarano(ano, filmes):
        encontrados = []
        for idx, (nome, chave) in enumerate(filmes.items(), start=1):
            if chave['ano'] == ano:
               encontrados.append((idx, nome, chave))
        
        print(f"{len(encontrados)} filme(s) de {ano} encontrado(s):\n")
        for idx, nome, chave in encontrados:
            print(f"{idx}° {nome} {chave}")
    else:
        print(f"filme(s) de {ano} não encontrado(s)...")
def op4diretor(filmes):
    diretor = str(input("diretor do(s) filme(s) a ser(em) procurado(s): ")).strip().lower()
    if verificardiretor(diretor, filmes):
        encontrados = []
        for idx, (nome, chave) in enumerate(filmes.items(), start=1):
            if chave['diretor'].lower() == diretor:
               encontrados.append((idx, nome, chave))
    if encontrados:
        print(f"{len(encontrados)} filme(s) de {diretor.title()} encontrado(s).\n")  # Usando title() para formatar o nome
        for idx, nome, chave in encontrados:
            print(f"{idx}° {nome} {chave}")
    else:
        print(f"Nenhum filme dirigido por {diretor.title()} foi encontrado.")
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

on = True
off = False
while on:
    menu()
    opcao = int(input())
    while opcao < 1 or opcao > 8:
        print("Opção invalida, por favor escolha uma das opções acima.")
        opcao = int(input())
    if opcao == 1:
        opcao2 = str(input("exibir lista completa ou trecho? c = completo / t = trecho\n"))
        if opcao2 == "c":
            op1a()
        elif opcao2 == "t":
            op1b()
        else:
            while opcao2 != "c" and opcao2 != "t":
                print("Opção invalida, por favor escolha uma das opções acima.")
                opcao2 = str(input("exibir lista completa ou trecho? c = completo / t = trecho\n"))
                if opcao2 == "c":
                    op1a()
                elif opcao2 == "t":
                    op1b()
    elif opcao == 2:
        op2(filmes, arqfilmes)
    elif opcao == 3:
        op3(filmes, arqfilmes)
    elif opcao == 4:
        opcao2 = str(input("Selecione uma opção:\nn -> nome\na -> ano\nd -> diretor\nav -> avaliação\n"))
        if opcao2.lower() == "n":
            op4nome(filmes)
        elif opcao2.lower() == "a":
            op4ano(filmes)
        elif opcao2.lower() == "d":
            op4diretor(filmes)
        elif opcao2.lower() == "av":
            op4av(filmes)

        while opcao2.lower() not in ["n", "a", "d", "av"]:
            print("Opção inválida, por favor escolha uma das opções abaixo.")
            opcao2 = str(input("\nn -> nome\na -> ano\nd -> diretor\nav -> avaliação\n"))

            if opcao2.lower() == "n":
                op4nome(filmes)
            elif opcao2.lower() == "a":
                op4ano(filmes)
            elif opcao2.lower() == "d":
                op4diretor(filmes)
            elif opcao2.lower() == "av":
                op4av(filmes)
    elif opcao == 5:
            print("Obrigado por utilizar nosso sistema...")
            on = off 