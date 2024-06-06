import re
import sys

def main():
    """
    Função main que chama o gerenciador com o caminho do arquivo fornecido.
    """
    caminho_arquivo = "exemplo.txt"  # Pega o caminho do arquivo dos argumentos da linha de comando ou usa "exemplo.txt" por padrão
    try:
        gerenciador(caminho_arquivo)  # Chama a função gerenciador com o caminho do arquivo
    except FileNotFoundError:
        print(f"ERRO: Arquivo '{caminho_arquivo}' não encontrado.")  # Captura e imprime erro se o arquivo não for encontrado

def gerenciador(caminho_arquivo: str):
    """
    Gerencia a leitura do arquivo e execução dos comandos.
    """
    pilha = []  # Inicializa a pilha de escopos
    palavras, linhas = obter_palavras(caminho_arquivo)  # Obtém listas de palavras e linhas do arquivo
    i = 0  # Inicializa o índice para percorrer as palavras

    while i < len(palavras):
        palavra = palavras[i]  # Pega a palavra atual
        
        if palavra == "BLOCO":
            i = tratar_bloco(palavras, linhas, i, pilha)  # Trata o início de um bloco
        elif palavra == "NUMERO":
            i = tratar_declaracao(palavras, linhas, i, pilha, "NUMERO")  # Trata a declaração de uma variável numérica
        elif palavra == "CADEIA":
            i = tratar_declaracao(palavras, linhas, i, pilha, "CADEIA")  # Trata a declaração de uma variável de cadeia (string)
        elif palavra == "PRINT":
            i = tratar_impressao(palavras, linhas, i, pilha)  # Trata o comando de impressão
        elif palavra == "FIM":
            i = tratar_fim_bloco(palavras, linhas, i, pilha)  # Trata o fim de um bloco
        elif verificar_Lexema(palavra, 'identificador'):
            i = tratar_atribuicao(palavras, linhas, i, pilha)  # Trata a atribuição de valores a variáveis
        else:
            print(f"ERRO linha {linhas[i]}: comando desconhecido '{palavra}'")  # Imprime erro para comando desconhecido
        
        i += 1  # Incrementa o índice para a próxima palavra

def tratar_bloco(palavras, linhas, i, pilha):
    """
    Trata o início de um bloco de código.
    """
    try:
        if verificar_Lexema(palavras[i+1], 'bloco'):
            i += 1
            escopo = []  # Cria um novo escopo (bloco) vazio
            pilha.append(escopo)  # Adiciona o novo escopo à pilha
        else:
            print(f"ERRO linha {linhas[i]}: nome de bloco inválido")
    except IndexError:
        print(f"ERRO linha {linhas[i]}: bloco sem nome")  # Imprime erro se o bloco não tiver nome
    return i

def tratar_declaracao(palavras, linhas, i, pilha, tipo):
    """
    Trata a declaração de variáveis do tipo NUMERO ou CADEIA.
    """
    while True:
        i += 1
        try:
            if verificar_Lexema(palavras[i], 'identificador'):
                if verificar_Lexema(palavras[i], 'var_no_escopo', pilha):
                    print(f"ERRO linha {linhas[i]}: Variável já declarada!")
                    break

                var = palavras[i]
                if palavras[i+1] == "=":
                    i += 2
                    if (tipo == "NUMERO" and verificar_Lexema(palavras[i], 'numero')) or (tipo == "CADEIA" and verificar_Lexema(palavras[i], 'cadeia')):
                        pilha[-1].append({'token': 'tk_identificador','lexema': var,'tipo': tipo, 'valor': palavras[i]})
                    else:
                        print(f"ERRO linha {linhas[i]}: {tipo.lower()} mal formatado!")
                else:
                    pilha[-1].append({'token': 'tk_identificador','lexema': var, 'tipo': tipo, 'valor': 0})
            else:
                print(f"ERRO linha {linhas[i]}: Identificador mal formatado!")
            
            if palavras[i+1] != ',':
                break
            else:
                i += 1
        except IndexError:
            break
    return i

def tratar_impressao(palavras, linhas, i, pilha):
    """
    Trata o comando PRINT que imprime o valor de uma variável.
    """
    cont = len(pilha) - 1  # Inicia a contagem do topo da pilha
    flag = True  # Flag para indicar se a variável foi encontrada
    i += 1

    while cont >= 0 and flag:
        topo = pilha[cont]  # Obtém o escopo atual da pilha
        for dic in topo:
            if palavras[i] == dic['lexema']:
                print(dic['lexema'], ":", dic['valor'])  # Imprime o nome e valor da variável
                flag = False  # Variável encontrada
                break
        cont -= 1

    if flag:
        print(f"ERRO linha {linhas[i]}: Não é possível exibir variável não declarada! ( {palavras[i]} )")
    
    return i

def tratar_fim_bloco(palavras, linhas, i, pilha):
    """
    Trata o comando FIM que encerra um bloco.
    """
    i += 1
    if len(pilha) > 0:
        pilha.pop()  # Remove o escopo do topo da pilha
    else:
        print(f"ERRO linha {linhas[i]}: Fim sem bloco")  # Imprime erro se não houver bloco para finalizar
    return i

def tratar_atribuicao(palavras, linhas, i, pilha):
    """
    Trata a atribuição de valores a variáveis.
    """
    var = obter_variavel(palavras[i], pilha)  # Obtém a variável da pilha de escopos
    if var is None:
        try:
            if palavras[i+1] == "=":
                var2 = obter_variavel(palavras[i+2], pilha)
                if var2:
                    pilha[-1].append({'token': 'tk_identificador','lexema': palavras[i],'tipo': var2['tipo'],'valor': var2['valor']})
                else:
                    i += 2
                    if verificar_Lexema(palavras[i], 'numero'):
                        pilha[-1].append({'token': 'tk_identificador','lexema': palavras[i-2],'tipo': "NUMERO",'valor': palavras[i]})
                    elif verificar_Lexema(palavras[i], 'cadeia'):
                        pilha[-1].append({'token': 'tk_identificador','lexema': palavras[i-2],'tipo': "CADEIA",'valor': palavras[i]})
                    else:
                        print(f"ERRO linha {linhas[i]}: Tipo inexistente!")
            else:
                print(f"ERRO linha {linhas[i]}: Declaração inválida! ({palavras[i]})")
        except IndexError:
            pass
    else:
        tipo = var['tipo']
        try:
            if palavras[i+1] == "=":
                i += 2
                var2 = obter_variavel(palavras[i], pilha)
                if var2:
                    if var2['tipo'] == tipo:
                        var['valor'] = var2['valor']
                    else:
                        i -= 1
                        print(f"ERRO linha {linhas[i]}: tipos incompatíveis!")
                else:
                    if tipo == "NUMERO" and verificar_Lexema(palavras[i], 'numero'):
                        var['valor'] = palavras[i]
                    elif tipo == "CADEIA" and verificar_Lexema(palavras[i], 'cadeia'):
                        var['valor'] = palavras[i]
                    else:
                        print(f"ERRO linha {linhas[i]}: {tipo.lower()} mal formatado!")
        except IndexError:
            pass
    return i

def obter_palavras(caminho_arquivo: str):
    """
    Lê o arquivo e retorna duas listas: uma com as palavras e outra com os números das linhas.
    """
    palavras = []  # Lista de palavras
    linhas = []  # Lista de números de linhas
    palavra = ""
    linha_atual = 1
    with open(caminho_arquivo, 'r') as f:
        while True:
            char = f.read(1)
            if not char:
                break
            if char == "\n":
                linha_atual += 1  # Incrementa o contador de linhas
            if char in [" ", "\n"]:
                if palavra:
                    palavras.append(palavra)
                    linhas.append(linha_atual)
                    palavra = ""
            elif char in ["=", ","]:
                if palavra:
                    palavras.append(palavra)
                    linhas.append(linha_atual)
                    palavra = ""
                palavras.append(char)
                linhas.append(linha_atual)
            elif char == '"':
                if palavra:
                    palavras.append(palavra)
                    linhas.append(linha_atual)
                    palavra = ""
                palavra += char
                while True:
                    char = f.read(1)
                    if not char:
                        break
                    palavra += char
                    if char == '"':
                        break
                palavras.append(palavra)
                linhas.append(linha_atual)
                palavra = ""
            else:
                palavra += char
    return palavras, linhas  # Retorna as listas de palavras e linhas

def obter_variavel(lexema: str, pilha: list) -> dict:
    """
    Procura uma variável na pilha de escopos e a retorna se encontrada.
    """
    for escopo in reversed(pilha):  # Percorre a pilha de escopos de cima para baixo
        for dic in escopo:
            if lexema == dic['lexema']:
                return dic  # Retorna a variável se encontrada
    return None  # Retorna None se a variável não for encontrada

def verificar_Lexema(lexema: str, tipo: str, pilha: list = None) -> bool:
    """
    Verifica diferentes tipos de lexemas: identificador, número, cadeia, bloco ou variável no escopo.
    """
    if tipo == 'identificador':
        return bool(re.match(r'^[a-zA-Z][a-zA-Z_]*$', lexema))  # Verifica se é um identificador válido
    elif tipo == 'numero':
        return bool(re.match(r'[+-]?\d+(\.\d+)?$', lexema))  # Verifica se é um número válido
    elif tipo == 'cadeia':
        return bool(re.match(r'"[^"]*"', lexema))  # Verifica se é uma cadeia válida
    elif tipo == 'bloco':
        return bool(re.match(r'^_[a-zA-Z0-9]+_$', lexema))  # Verifica se é um nome de bloco válido
    elif tipo == 'var_no_escopo' and pilha is not None:
        for dic in pilha[-1]:
            if lexema == dic['lexema']:
                return True  # Verifica se a variável está no escopo atual
        return False
    return False

main() # Chama a função main
