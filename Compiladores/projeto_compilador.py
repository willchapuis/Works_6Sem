import shelve
import sys
import pickle

#   ALTERAÇÕES
#   '#' Como Diretiva -> Ignore a linha (simbolo especial)
#   '==' Como simbolo composto
#   'main' Como palavra reservada
#   'printf' Como palavra reservada
#   '"' Como simbolo especial

# ANOTAÇÕES / DUVIDAS
#   identificador como por exemplo: log_a       PS: se puder ta safe
#   identificador como por exemplo: log0a       PS: se puder ta safe
#   identificador como por exemplo: log0a0      PS: se puder ta safe
#   linha com: printf("int a ==> %d");   -- eu pego o token de " até " ? caso contrario pegaria os tokens: ['PRINTF', '(', '"', 'INT', 'A', '==', '>', '%', 'D' '"', ')', ';']

#   eu verifico as letras até aonde ? exemplo: se eu verificar letra por letra, formando o token com as palavras reservadas, se eu encontrar 'DO' ele vai colocar como token, porem nunca vai conseguir completar o 'DOUBLE'
#   outro exemplo: 'int eiro = 5', tirando os espaços ficaria 'INTEIRO=5', oq impede de isso ser 3 tokens: ['INTEIRO', '=', '5'] ou ser 4 tokens: ['INT', 'EIRO', '=', '5']

with shelve.open('letras') as db:
    dictLetras = dict(db)
with shelve.open('digitos') as db:
    dictDigitos = dict(db)
with shelve.open('especiais') as db:
    dictEspeciais = dict(db)
with shelve.open('compostos') as db:
    dictCompostos = dict(db)
with shelve.open('palavras') as db:
    dictPalavras = dict(db)

def split(string):                                          #   Recebe uma string e retorna uma lista com os char dessa string
    return [char for char in string]

def union(list1, list2):                                    #   Recebe 2 listas e junta/concatena elas em uma só
    return list1 + list2

def inverte(string):                                        #   Recebe uma string e retorna ela ao contrario
    return string[::-1]

def carregar():
    filename = 'analise.txt'
    with open(filename) as file:
        linhas = file.readlines()                           #   coloca as linhas como strings em uma lista
        linhas = [x.strip('\n') for x in linhas]            #   retirar \n do final das strings
        linhas = [x.strip() for x in linhas]                #   retirar espaços no começo das strings
        linhas = [x.upper() for x in linhas]                #   coloca a string toda com caracteres em maiusculo
    return linhas

def carregarTabela():
    filename = 'tabela'
    with open(filename, 'rb') as file:
        tabela = pickle.load(file)
    return tabela
    # filename = 'tabela'
    # dict = {
    #     0: {'id': '', 'num': '', '+': '', '-': '', '*': '', '/': '', '(': '', ')': '', '$': ''},
    #     'E': {'id': 'TS', 'num': 'TS', '+': ' ', '-': ' ', '*': ' ', '/': ' ', '(': 'TS', ')': ' ', '$': ' '},
    #     'T': {'id': 'FG', 'num': 'FG', '+': ' ', '-': ' ', '*': ' ', '/': ' ', '(': 'FG', ')': ' ', '$': ' '},
    #     'S': {'id': ' ', 'num': ' ', '+': '+TS', '-': '-TS', '*': ' ', '/': ' ', '(': ' ', ')': '!', '$': '!'},
    #     'G': {'id': ' ', 'num': ' ', '+': '!', '-': '!', '*': '*FG', '/': '/FG', '(': ' ', ')': '!', '$': '!'},
    #     'F': {'id': 'id', 'num': 'num', '+': '', '-': '', '*': '', '/': '', '(': '(E)', ')': ' ', '$': ' '}
    # }
    # with open(filename, 'wb') as file:
    #     pickle.dump(dict, file)

def lexico(linhas):
    lLinha = []
    lToken = []
    lSimb = []

    linha = 0
    token = ''
    cont = 0

    while(linha < len(linhas)):
        aux = split(linhas[linha - 1])
        # print(f'while 1 -> {linha} < {len(linhas)} ?')
        while(cont < len(aux)):
            # print(f'while 2 -> {cont} < {len(aux)} ?')
            while(aux[cont] == ' '):
                # print(f'while de espaço')
                cont += 1
            token = token + aux[cont]
            # print(f'token inicial/aux[cont] -> {token}')
            if token in dictLetras:                         # Tratamento com inicio de letra
                # print(f'letra')
                if cont + 1 < len(aux):
                    while((aux[cont+1] in dictLetras) or (aux[cont+1] in dictDigitos)): # erro qd termina com letra
                        # print(f'while letra -> {aux[cont+1]} é letra ou digito ?')
                        cont += 1
                        token = token + aux[cont]
                        # print(f'{token} -- {aux[cont]}')
                        if cont+1 == len(aux):
                            break
                lLinha.append(linha)
                lToken.append(token)
                if token in dictPalavras:
                    # print(f'detectou palavra -> {linha} | {token} | {dictPalavras[token]}')
                    lSimb.append(dictPalavras[token])
                else:
                    # print(f'detectou identificador -> {linha} | {token} | "Identificador"')
                    lSimb.append('Identificador')
                token = ''
            elif token in dictDigitos:                      # Tratamento com inicio de digito
                # print(f'digito')
                if cont+1 < len(aux):
                    while(aux[cont+1] in dictDigitos):
                        # print(f'while digito -> {aux[cont + 1]} é digito ?')
                        cont += 1
                        token = token + aux[cont]
                        # print(f'{token} -- {aux[cont]}')
                        if cont+1 == len(aux):
                            break
                lLinha.append(linha)
                lToken.append(token)
                lSimb.append(dictDigitos[aux[cont]])
                # print(f'detectou digito -> {linha} | {token} | {dictDigitos[aux[cont]]}')
                token = ''
            elif token in dictEspeciais:                    # Tratamento com inicio de especial
                # print(f'especial')
                if token == '#':
                    lLinha.append(linha)
                    lToken.append(token)
                    lSimb.append(dictEspeciais[token])
                    # print(f'detectou comentario -> {linha} | {token} | {dictEspeciais[token]}')
                    token = ''
                    break
                elif (cont+1 < len(aux)) and ((aux[cont] + aux[cont+1]) in dictCompostos):
                    # print(f'composto')
                    cont += 1
                    token = token + aux[cont]
                    # print(f'{token} -- {aux[cont]}')
                    lLinha.append(linha)
                    lToken.append(token)
                    lSimb.append(dictCompostos[token])
                    # print(f'detectou composto -> {linha} | {token} | {dictCompostos[token]}')
                    token = ''
                else:
                    lLinha.append(linha)
                    lToken.append(token)
                    lSimb.append(dictEspeciais[token])
                    # print(f'detectou especial -> {linha} | {token} | {dictEspeciais[token]}')
                    token = ''
            else:
                # print(f'Erro encontrado na linha {linha})')
                sys.exit()
            cont += 1
        linha += 1
        cont = 0

    # print(lLinha)
    # print(lToken)
    # print(lSimb)
    return lToken

def sintatico(tokens):
    tabela = carregarTabela()
    C = list(tabela[0].keys())
    L = list(tabela.keys())
    pilha = ['$', 'E']
    lpilha = []
    lcadeia = []
    lregra = []
    seta = ' -> '

    continua = True
    while continua:
        lpilha.append(' '.join(pilha.copy()))
        lcadeia.append(' '.join(tokens.copy()))
        if pilha[len(pilha)-1] in tabela:
            if tokens[0] in tabela[0]:
                lregra.append(pilha[len(pilha) - 1] + seta + tabela[pilha[len(pilha) - 1]][tokens[0]])
                str = tabela[pilha[len(pilha) - 1]][tokens[0]]
                b = False
                for c in str:
                    if c.islower():
                        b = True
                        break
                if b:
                    aux = [str]
                else:
                    aux = inverte(split(str))
                pilha.pop()
                pilha = union(pilha, aux)
        elif (pilha[len(pilha)-1] in tabela[0]) and (pilha[len(pilha)-1] == tokens[0]):
            if tokens[0] == '$':
                lregra.append('Sucesso')
                continua = False
            else:
                lregra.append('----')
            pilha.pop()
            tokens.pop(0)
        else:
            lregra.append('ERRO')
            break
        if len(pilha) > 0:
            if pilha[len(pilha) - 1] == '!':
                pilha.pop()

    print('{:50s}\t{:50s}\t{:50s}'.format('PILHA', 'CADEIA', 'REGRA'))
    print()
    for i in range (len(lpilha)):
        print(f'{lpilha[i]:50s}\t{lcadeia[i]:50s}\t{lregra[i]:50s}')

if __name__ == '__main__':
    ## Carregar do arquivo:
    # linhas = carregar()
    ## Carregamento rapido:
    linhas = []
    # linhas.append((input(f'Digite a cadeia -> ')).upper())
    linhas.append('id*(id+num)'.upper())
    tokens = lexico(linhas)

    for i in range(len(tokens)):
        tokens[i] = tokens[i].lower()
    tokens.append('$')

    sintatico(tokens)
