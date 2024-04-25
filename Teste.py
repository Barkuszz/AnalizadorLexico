import re
import sys
from typing import TextIO
import chardet

#Variaveis globais

##Controla a posição da linha e coluna atual no arquivo
col = 0         #Coluna atual
line = 1        #Linha atual

##Controla a posição da ultima coluna da linha anterior no arquivo
tam_linha = 0   #Tamanho da linha atual
tam_linha_ant = 0   #Tamanho da linha anterior


def analisadorLex(file_path: str) -> list:
    """
    Função que simula o analisador
    Chama o proximo token do arquivo

    Recebe como parametro o caminho de um arquivo, que deve ser um arquivo .cic
    Retorna uma lista de tokens
    """

    tokens = []
    errors = []
    global col, line
    encoding_type = ""

    if file_path.endswith(".cic"):
        try:
            #Detecta o encoding do arquivo
            with open(file_path, "rb") as file:
                result = chardet.detect(file.read())
                encoding_type = result['encoding']

            #Chama o proximo token do arquivo até o fim do arquivo
            with open(file_path, "r", encoding = encoding_type) as file:
                while True:
                    token = next_token(file)

                    if not token:
                        break
                    elif token['token'] == "ERROR":
                        errors.append(token)
                    else:
                        tokens.append(token)
                
                #Imprime os erros encontrados, se houver
                if errors != []:
                    print_errors(file_path, errors)

                #Retorna a lista de tokens
                return tokens

        except FileNotFoundError:
            print("Arquivo não encontrado.")
    else:
        print("Por favor, forneça um arquivo com extensão .cic.")


def next_token(file: TextIO) -> dict:
    """
    Função que retorna o próximo token do arquivo
    Feita baseada no automato finito deterministico
    Passa o arquivo caracter por caracter, enquanto analisa pelo estado atual seguindo o automato
    e no fim retorna o token

    Estado 0: Estado inicial - Primeiro estado do automato
    Estado 18: Estado de rejeição - Estado que indica que o token não foi reconhecido e chama a função handle_errors que lida com os erros

    Recebe como parametro o arquivo
    Retorna um dicionario com o token, lexema, linha e coluna
    """

    state = 0
    lexema = ""
    error_code = -1
    line_token = 0
    col_token = 0
    
    global col, line
    
    while True:
        char = next_char(file)

        #Identificando o inicio do token
        if char not in [' ', '\n'] and state == 0:
            line_token = line
            col_token = col

        #Implementação do automato finito deterministico
        match state:
            case 0:                             #Estado inicial
                if char == ')':
                    state = 13
                elif char == '(':
                    state = 14
                elif char == ',':
                    state = 15
                elif char == '+':
                    state = 26
                elif char == '-':
                    state = 27
                elif char == '/':
                    state = 29
                elif char == '|':
                    state = 30
                elif char == '*':
                    state = 31
                elif char == '~':
                    state = 32
                elif char == '=':
                    state = 33
                elif char == '!':
                    state = 34
                elif char == ':':
                    state = 36
                elif char == '>':
                    state = 40
                elif char == '"':
                    lexema += char
                    state = 16
                elif ver_lower_case(char):
                    lexema += char
                    state = 1
                elif char == '<':
                    lexema += char
                    state = 10
                elif char == '#':
                    state = 19
                elif char == '\'':
                    state = 21
                elif ver_GZ(char):
                    lexema += char
                    state = 4
                elif ver_AF(char):
                    lexema += char
                    state = 43
                elif ver_number(char):
                    lexema += char
                    state = 44
            case 1:
                if ver_lower_case(char):
                    lexema += char
                    state = 2
                else:
                    previous_char(file)
                    error_code = 7
                    state = 18
            case 2:
                if ver_lower_case(char) or char == '_':
                    lexema += char
                    state = 2
                else:
                    previous_char(file)
                    state = 3
            case 3:
                reserved_word = is_reserved_word(lexema)
                previous_char(file)
                if reserved_word != -1:
                    return {"token":reserved_word, "lexema":"", "linha":line_token, "coluna":col_token}
                else:
                    error_code = 7
                    state = 18
            case 4:
                if char == "$":
                    lexema += char
                    state = 5
                else:
                    previous_char(file)
                    error_code = 5
                    state = 18
            case 5:
                if ver_number(char):
                    lexema += char
                    state = 6
                else:
                    previous_char(file)
                    error_code = 5
                    state = 18
            case 6:
                if ver_number(char):
                    lexema += char
                    state = 6
                elif char == ".":
                    lexema += char
                    state = 7
                else:
                    previous_char(file)
                    error_code = 5
                    state = 18
            case 7:
                if ver_number(char):
                    lexema += char
                    state = 8
                else:
                    previous_char(file)
                    error_code = 5
                    state = 18
            case 8:
                if ver_number(char):
                    lexema += char
                    state = 9
                else:
                    previous_char(file)
                    error_code = 5
                    state = 18
            case 9:
                previous_char(file)
                return {"token":"TK_MOEDA", "lexema":lexema, "linha":line_token, "coluna":col_token}
            case 10:
                if char == '=':
                    state = 38
                elif ver_lower_case(char):
                    lexema += char
                    state = 11
                else:
                    previous_char(file)
                    state = 39
            case 11:
                if ver_lower_case(char) or ver_number(char):
                    lexema += char
                    state = 11
                elif char == '>':
                    lexema += char
                    state = 12
                else:
                    previous_char(file)
                    error_code = 4
                    state = 18
            case 12:
                previous_char(file)
                return {"token":"TK_IDENTIFICADOR", "lexema":lexema, "linha":line_token, "coluna":col_token}
            case 13:
                previous_char(file)
                return {"token":"TK_FECHA_PARENTESES", "lexema":"", "linha":line_token, "coluna":col_token}
            case 14:
                previous_char(file)
                return {"token":"TK_ABRE_PARENTESES", "lexema":"", "linha":line_token, "coluna":col_token}
            case 15:
                previous_char(file)
                return {"token":"TK_VIRGULA", "lexema":"", "linha":line_token, "coluna":col_token}
            case 16:
                if char == '"':
                    lexema += char
                    state = 17
                elif char == '\n':
                    previous_char(file)
                    error_code = 2
                    state = 18
                else:
                    lexema += char
                    state = 16
            case 17:
                previous_char(file)
                return {"token":"TK_CADEIA", "lexema":lexema, "linha":line_token, "coluna":col_token}
            

            case 18:                             #Estado de rejeição
                previous_char(file)
                return handle_errors(error_code, file, char)
            

            case 19:
                if char == '\n':
                    previous_char(file)
                    state = 20
                else:
                    state = 19
            case 20:
                previous_char(file)
                return {"token":"TK_COMENTARIO", "lexema":"", "linha":line_token, "coluna":col_token}
            case 21:
                if char == "'":
                    state = 22
                else:
                    previous_char(file)
                    error_code = 1
                    state = 18
            case 22:
                if char == "'":
                    state = 23
                else:
                    previous_char(file)
                    error_code = 1
                    state = 18
            case 23:
                if char == "'":
                    state = 24
                elif not char:
                    previous_char(file)
                    error_code = 1
                    state = 18

                    #evitar que o loop termine antes de retornar o token
                    previous_char(file)
                    char = next_char(file)
                else:
                    state = 23
            case 24:
                if char == "'":
                    state = 25
                else:
                    state = 23
            case 25:
                if char == "'":
                    state = 20
                else:
                    state = 23
            case 26:
                previous_char(file)
                return {"token":"TK_MAIS", "lexema":"", "linha":line_token, "coluna":col_token}
            case 27:
                previous_char(file)
                return {"token":"TK_MENOS", "lexema":"", "linha":line_token, "coluna":col_token}
            case 29:
                previous_char(file)
                return {"token":"TK_DIV", "lexema":"", "linha":line_token, "coluna":col_token}
            case 30:
                previous_char(file)
                return {"token":"TK_OU", "lexema":"", "linha":line_token, "coluna":col_token}
            case 31:
                previous_char(file)
                return {"token":"TK_MULT", "lexema":"", "linha":line_token, "coluna":col_token}
            case 32:
                previous_char(file)
                return {"token":"TK_NEGACAO", "lexema":"", "linha":line_token, "coluna":col_token}
            case 33:
                previous_char(file)
                return {"token":"TK_IGUAL", "lexema":"", "linha":line_token, "coluna":col_token}
            case 34:
                if char == '=':
                    state = 35
                else:
                    previous_char(file)
                    error_code = 6
                    state = 18
            case 35:
                previous_char(file)
                return {"token":"TK_DIFERENTE", "lexema":"", "linha":line_token, "coluna":col_token}
            case 36:
                if char == '=':
                    state = 37
                else:
                    previous_char(file)
                    error_code = 6
                    state = 18
            case 37:
                previous_char(file)
                return {"token":"TK_ATRIBUICAO", "lexema":"", "linha":line_token, "coluna":col_token}
            case 38:
                previous_char(file)
                return {"token":"TK_MENOR_IGUAL", "lexema":"", "linha":line_token, "coluna":col_token}
            case 39:
                previous_char(file)
                return {"token":"TK_MENOR", "lexema":"", "linha":line_token, "coluna":col_token}
            case 40:
                if char == '=':
                    state = 41
                else:
                    previous_char(file)
                    state = 42
            case 41:
                previous_char(file)
                return {"token":"TK_MAIOR_IGUAL", "lexema":"", "linha":line_token, "coluna":col_token}
            case 42:
                previous_char(file)
                return {"token":"TK_MAIOR", "lexema":"", "linha":line_token, "coluna":col_token}
            case 43:
                if char == "$":
                    lexema += char
                    state = 5
                elif ver_number(char) or ver_AF(char):
                    lexema += char
                    state = 44
                elif char == ".":
                    lexema += char
                    state = 46
                elif char == "e":
                    lexema += char
                    state = 49
                else:
                    previous_char(file)
                    state = 45
            case 44:
                if ver_number(char) or ver_AF(char):
                    lexema += char
                    state = 44
                elif char == ".":
                    lexema += char
                    state = 46
                elif char == "e":
                    lexema += char
                    state = 49
                else:
                    state = 45
                    previous_char(file)
            case 45:
                previous_char(file)
                return {"token":"TK_NUMERO", "lexema":lexema, "linha":line_token, "coluna":col_token}
            case 46:
                if ver_number(char) or ver_AF(char):
                    lexema += char
                    state = 47
                else:
                    previous_char(file)
                    error_code = 3
                    state = 18
            case 47:
                if ver_number(char) or ver_AF(char):
                    lexema += char
                    state = 47
                elif char == "e":
                    lexema += char
                    state = 49
                else:
                    previous_char(file)
                    state = 48
            case 48:
                previous_char(file)
                return {"token":"TK_NUMERO", "lexema":lexema, "linha":line_token, "coluna":col_token}
            case 49:
                if char == "-":
                    lexema += char
                    state = 50
                elif ver_number(char) or ver_AF(char):
                    lexema += char
                    state = 51
                else:
                    previous_char(file)
                    error_code = 3
                    state = 18
            case 50:
                if ver_number(char) or ver_AF(char):
                    lexema += char
                    state = 51
                else:
                    previous_char(file)
                    error_code = 3
                    state = 18
            case 51:
                if ver_number(char) or ver_AF(char):
                    lexema += char
                    state = 51
                else:
                    previous_char(file)
                    state = 52                
            case 52:
                previous_char(file)
                return {"token":"TK_NUMERO", "lexema":lexema, "linha":line_token, "coluna":col_token}
        
        if not char:
            return None


def next_char(file: TextIO) -> str:
    """
    Função que retorna o proximo caracter do arquivo

    Recebe como parametro o arquivo
    Retorna um str, sendo o proximo caracter
    """

    global col, line, tam_linha, tam_linha_ant

    char = file.read(1)

    col += 1
    tam_linha += 1

    if char == '\n':
        line += 1
        col = 0
        tam_linha_ant = tam_linha
        tam_linha = 0

    return char


def previous_char(file: TextIO) -> None:
    """
    Função que volta para o caracter anterior do arquivo

    Recebe como parametro o arquivo
    """

    global col, line, tam_linha, tam_linha_ant

    file.seek(file.tell() - 1, 0)
    
    col -= 1
    tam_linha -= 1
    
    if col < 0:     
        line -= 1
        col = tam_linha_ant
        tam_linha = tam_linha_ant


def is_reserved_word(token: str) -> str:
    """
    Função que verifica se o lexema do token é uma palavra reservada

    Recebe como parametro o lexema do token
    Retorna o token da palavra reservada ou -1 caso não seja
    """

    reserved_words = {
        "programa": "TK_PROGRAMA",
        "fim_programa": "TK_FIM_PROGRAMA",
        "se": "TK_SE",
        "senao": "TK_SENAO",
        "entao": "TK_ENTAO",
        "imprima": "TK_IMPRIMA",
        "leia": "TK_LEIA",
        "enquanto": "TK_ENQUANTO"
    }

    if token in reserved_words:
        return reserved_words[token]
    else:
        return -1
    

def ver_lower_case(char: str) -> bool:
    """Função que verifica se o caracter é uma letra minuscula utilizando expressão regular"""
    return bool(re.match(r'[a-z]', char))

def ver_number(char: str) -> bool:
    """Função que verifica se o caracter é um numero utilizando expressão regular"""
    return bool(re.match(r'[0-9]', char))

def ver_AF(char: str) -> bool:
    """Função que verifica se o caracter é uma letra entre A e F utilizando expressão regular"""
    return bool(re.match(r'[A-F]', char))

def ver_GZ(char: str) -> bool:
    """Função que verifica se o caracter é uma letra entre G e Z utilizando expressão regular"""
    return bool(re.match(r'[G-Z]', char))


def handle_errors(error_code: int, file: TextIO, char: str) -> dict:
    """
    Função que lida com os erros encontrados no arquivo

    Recebe como parametro o codigo do erro, o arquivo e o caracter
    Retorna um dicionario com o token, lexema, linha e coluna (apenas para verificação de erro)
    """

    global col, line
    col_error = col
    line_error = line

    #Lista de erros possiveis
    errors_list = {
        1: "Comentário mal formado.",
        2: "Cadeia mal formada.",
        3: "Número mal formado.",
        4: "Identificador mal formado.",
        5: "Moeda mal formada.",
        6: "Operador não reconhecido",
        7: "Palavra reservada não reconhecida"
    }

    #Ajusta a posição do erro para palavras reservadas
    if error_code == 7:
        col_error += 1
    
    # #Opicional: Metodo de desespero
    # #Lista de tokens de sincronização
    # tokens_sync = {
    #     ",",
    #     "(",
    #     ")"
    # }    

    # #Aplicando o metodo de desespero, descartando tudo até o proximo token de sincronização
    # while char not in tokens_sync:
    #     char = next_char(file)

    # previous_char(file)

    return {"token":"ERROR", "lexema":errors_list[error_code], "linha":line_error, "coluna":col_error}
    

def print_errors(file_path: str, errors: list) -> None:  #####Fazer
    """
    Função que imprime os erros encontrados no arquivo
    """

    with open(file_path, 'r') as file:
        lines = file.readlines()

    #Adiciona a numeração de linhas
    numbered_lines = []
    for i, line in enumerate(lines, start=1):
        number = str(i).rjust(4)    #4 espaços para a numeração de linha
        numbered_lines.append(f"[{number}] {line}")
    
    #Adiciona os indicadores de erro
    for erro in errors:
        line = erro['linha']
        col = erro['coluna']
        indic_erro = '-' * (col + 5) + '^'  # espaços = (6 da numeração de linha + numero da coluna - 1) + '^'
        numbered_lines[line - 1] += f"{indic_erro}\nErro: {erro['lexema']} na linha {line}, coluna {col}\n"
    
    #Escreve no arquivo
    error_path = 'erro_' + file_path.split('/')[-1].split('.')[0] + '.txt'
    with open(error_path, 'w') as file:
        for line in numbered_lines:
            file.write(line)
    

def gerar_relatorio(tokens: list, file_path: str) -> None:
    """
    Função que gera os relatorios do analisador lexico
    Imprime em um arquivo uma lista de tokens reconhecidos com suas respectivas localizações
    e um somatorio de tokens reconhecidos ordenados por frequencia

    Recebe como parametro a lista de tokens e o caminho do arquivo
    """

    #Cria o caminho do arquivo de relatorio com o padrao: relatorio_<nome_do_arquivo>.txt
    relatorio_path = 'relatorio_' + file_path.split('/')[-1].split('.')[0] + '.txt'
    
    #Conta a frequencia de cada token
    cont_tokens = {}
    for token_info in tokens:
        token = token_info['token']
        if token in cont_tokens:
            cont_tokens[token] += 1
        else:
            cont_tokens[token] = 1
    
    #Ordena os tokens por frequencia
    tokens_order = sorted(cont_tokens.items(), key=lambda x: x[1], reverse=True)

    #Escreve no arquivo de relatorio
    with open(relatorio_path, 'w') as relatorio:
        #Cabeçalho do relatorio de tokens reconhecidos
        relatorio.write(f"TOKENS RECONHECIDOS:\n\n")
        relatorio.write(f"+------+------+---------------------------+---------------------------+\n")
        relatorio.write(f"| LIN  | COL  | {'TOKEN':<25} | {'LEXEMA':<25} |\n")
        relatorio.write(f"+------+------+---------------------------+---------------------------+\n")
        
        #Escreve os tokens reconhecidos no arquivo formatados
        for token_info in tokens:
            linha = token_info['linha']
            coluna = token_info['coluna']
            token = token_info['token']
            lexema = token_info['lexema']
            
            linha_str = str(linha).rjust(4)     #4 espaços para a numeração de linha
            coluna_str = str(coluna).rjust(4)   #4 espaços para a numeração de coluna
            token_str = token.ljust(25)         #25 espaços para o token
            lexema_str = lexema.ljust(25)       #25 espaços para o lexema
            
            relatorio.write(f"| {linha_str} | {coluna_str} | {token_str} | {lexema_str} |\n")
            relatorio.write(f"+------+------+---------------------------+---------------------------+\n")

        #Cabeçalho do somatorio de tokens reconhecidos
        relatorio.write(f"\n\nSOMATÓRIO DE TOKENS RECONHECIMENTOS:\n\n")
        relatorio.write(f"+---------------------------+-------+\n")
        relatorio.write(f"| {'TOKEN':<25} | {'USOS':<5} |\n")
        relatorio.write(f"+---------------------------+-------+\n")
        
        total = 0
        #Escreve o somatorio de tokens reconhecidos no arquivo formatados
        for token, frequencia in tokens_order:
            token_str = token.ljust(25)
            frequencia_str = str(frequencia).rjust(5)   #5 espaços para a frequencia
            total += frequencia

            relatorio.write(f"| {token_str} | {frequencia_str} |\n")
            relatorio.write(f"+---------------------------+-------+\n")
            
        total_token = "TOTAL".ljust(25)
        total_str = str(total).rjust(5)
        relatorio.write(f"| {total_token} | {total_str} |\n")
        relatorio.write(f"+---------------------------+-------+\n")


def main(argv, argc):
    if argc > 1:
        file_path = argv[1]        
    else:
        file_path = input("Digite o caminho do arquivo: ")
    
    tokens = analisadorLex(file_path)

    gerar_relatorio(tokens, file_path)


if __name__ == '__main__':
    main(sys.argv, len(sys.argv))