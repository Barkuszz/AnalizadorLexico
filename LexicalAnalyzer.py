import re
from datetime import datetime
from collections import defaultdict
# Dicionário que mapeia tokens aos seus lexemas correspondentes
lexemas = {
    "|": "TOKEN_OR",
    "-": "TOKEN_MENOS",
    "~": "TOKEN_TIO",
    "+": "TOKEN_MAIS",
    "*": "TOKEN_ASTERISCO",
    "%": "TOKEN_PORCENTAGEM",
    "&": "TOKEN_ECOMERCIAL",
    "==": "TOKEN_IGUAL_IGUAL",
    ">": "TOKEN_MAIOR",
    ">=": "TOKEN_MAIOR_IGUAL",
    "<": "TOKEN_MENOR",
    "<=": "TOKEN_MENOR_IGUAL",
    "<==": "TOKEN_MENOR_IGUAL_IGUAL",
    '""': "TOKEN_CADEIA",
    "rotina": "TOKEN_ROTINA",
    "fim_rotina": "TOKEN_FIM_ROTINA",
    "se": "TOKEN_SE",
    "senao": "TOKEN_SE_NAO",
    "imprima": "TOKEN_IMPRIMA",
    "leia": "TOKEN_LEIA",
    "para": "TOKEN_PARA",
    "(": "TOKEN_ABRE_PARENTESES",
    ")": "TOKEN_FECHA_PARENTESES",
    ":": "TOKEN_DOIS_PONTOS",
    "#": "TOKEN_COMENTARIO",

    # Lista de palavras reservadas da linguagem: rotina, fim_rotina, se, senao, imprima, leia, para, enquanto.
    # Adicione outros mapeamentos conforme necessário
}


def verifica_data_valida_barra(data):
    try:
        datetime.strptime(data, "%d/%m/%Y")
        return True
    except ValueError:
        return False

def verifica_data_valida_underscore(data):
    try:
        datetime.strptime(data, "%d_%m_%Y")
        return True
    except ValueError:
        return False

def verifica_Int(token):
    padrao = re.compile(r'^\d+$')
    return bool(padrao.match(token))

def verifica_Endereco(token):
    padrao = re.compile(r'^([A-F0-9]+x[A-F0-9]*)$')
    return bool(padrao.match(token))

def verifica_Float(token):
    padrao = re.compile(r'^(\d+\.\d*|\.\d+)(e[-+]?\d+)?$')
    return bool(padrao.match(token))

def verifica_comentarioComMaiorEMenorDoQue(token):
    padrao = re.compile(r'^>>>.*?<<<$')
    return bool(padrao.match(token))

def verifica_Comentario(token):
    padrao = re.compile(r'^#.*$')
    return bool(padrao.match(token))

def verifica_palavra(cadeia):
    padrao = re.compile(r'^[a-zA-Z]+$')
    return bool(padrao.match(cadeia))


#para contagem de tokens utilizados de cada tipo
contagem_tokens = defaultdict(int)


def verifica_padrao(token):
    padrao = re.compile(r'^[a-z][A-Z][a-zA-Z]*$')
    return bool(padrao.match(token))

def atualizar_contagem(lexema):
    contagem_tokens[lexema] += 1

def escrever_contagem_arquivo(nome_arquivo):
    with open(nome_arquivo, 'w') as arquivo:
        arquivo.write("+-----------------------------+--------------+\n")
        arquivo.write("|            Token            |   Usos       |\n")
        arquivo.write("+-----------------------------+--------------+\n")

        for token, quantidade in contagem_tokens.items():
            arquivo.write(f"| {token:<27} | {quantidade:>12} |\n")
            arquivo.write("+-----------------------------+--------------+\n")


def gerar_relatorio(token, linha, coluna, ListadeTokens):

    if verifica_padrao(token):
        lexema_str = "TOKEN_NOME_DE_VARIAVEL"
    elif verifica_Endereco(token):
        lexema_str = "TOKEN_ENDERECO"
    elif verifica_data_valida_barra(token):
        lexema_str = "TOKEN_DATA_BARRA"
    elif verifica_data_valida_underscore(token):
        lexema_str = "TOKEN_DATA_UNDERSCORE"
    elif verifica_Int(token):
        lexema_str = "TOKEN_INT"
    elif verifica_Float(token):
        lexema_str = "TOKEN_FLOAT"
    elif verifica_comentarioComMaiorEMenorDoQue(token):
        lexema_str = "TOKEN_COMENTARIO>>><<<"
    elif verifica_Comentario(token):
        lexema_str = "TOKEN_COMENTARIO"
    elif verifica_palavra(token):
         lexema_str = "TOKEN_PALAVRA"
    else:
        lexema_str = lexemas.get(token, "Lexema nao definido")
    
    atualizar_contagem(lexema_str)
    with open(ListadeTokens, 'a') as relatorio:
        relatorio.write(f"| {linha:<4} | {coluna:<4} | {token:<25} | {lexema_str:<25} |\n")
        relatorio.write(f"+------+------+---------------------------+---------------------------+\n")

    return


def automato_data(entrada):
    token = ""
    char = ""
    # Começamos no estado Q0
    estado = "Q0" 
    i = 0
    temp = ""
    linha = 1
    coluna = 1
    ListadeTokens = 'ListadeTokens.txt'
    letras_minusculas = 'abcdefghijklmnopqrstuvwxyz'
    letras_Maiusculas = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    letras_exadecimal = 'ABCDEF'




    with open(ListadeTokens, 'w') as relatorio:

        relatorio.write(f"TOKENS RECONHECIDOS:\n\n")
        relatorio.write(f"+------+------+---------------------------+---------------------------+\n")
        relatorio.write(f"| LIN  | COL  | {'LEXEMA':<25} | {'TOKEN':<25} |\n")
        relatorio.write(f"+------+------+---------------------------+---------------------------+\n")

    
    while True:
        match estado:
            case "Q0":
                char = entrada.read(1)
                
                if char == "":
                    break
                coluna += 1
                if char == "|":
                    estado = "Q1"
                elif char == "-":
                    estado = "Q2"
                elif char == "~":
                    estado = "Q3"
                elif char == "+":
                    estado = "Q4"
                elif char == "*":
                    estado = "Q5"
                elif char == "%":
                    estado = "Q6"
                elif char == "&":
                    estado = "Q7"      
                elif char == ">":
                    estado = "Q8"
                elif char == "<":
                    estado = "Q9"
                elif char == "=":
                    estado = "Q10"
                elif char == '"':
                    token += char
                    estado = "Q62"
                elif char in letras_minusculas :
                    estado = "Q65"
                elif char == "(":
                    estado = "Q68"
                elif char == ")":
                    estado = "Q70"
                elif char == ":":
                    estado = "Q72"
                elif char == "#":
                    estado = "QComentario"
                    token += char
                elif char == ".":
                    estado = "Q28"
                    token += char
                elif char.isdigit():
                    estado = "Q59"
                    token += char
                elif char in letras_exadecimal:
                    estado = "Q54"
                    token += char
                     
                
                
            case "Q1":
                    gerar_relatorio("|",linha ,coluna , ListadeTokens)
                    estado = "Q0"
                    escrever_contagem_arquivo("Tokens_Qtd.txt")
            case "Q2":
                    gerar_relatorio("-",linha ,coluna , ListadeTokens)
                    estado = "Q0"
                    escrever_contagem_arquivo("Tokens_Qtd.txt")
            case "Q3":
                    gerar_relatorio("~",linha ,coluna , ListadeTokens)
                    estado = "Q0"
                    escrever_contagem_arquivo("Tokens_Qtd.txt")
            case "Q4":
                    gerar_relatorio("+",linha ,coluna , ListadeTokens)
                    estado = "Q0"
                    escrever_contagem_arquivo("Tokens_Qtd.txt")
            case "Q5":
                    gerar_relatorio("*",linha ,coluna , ListadeTokens)
                    estado = "Q0"
                    escrever_contagem_arquivo("Tokens_Qtd.txt")
            case "Q6":
                    gerar_relatorio("%",linha ,coluna , ListadeTokens)
                    estado = "Q0"
                    escrever_contagem_arquivo("Tokens_Qtd.txt")
            case "Q7":
                    gerar_relatorio("&",linha ,coluna , ListadeTokens)
                    estado = "Q0"
                    escrever_contagem_arquivo("Tokens_Qtd.txt")
            case "Q8":
                char1 = entrada.read(1)
                if char == ">" and char1 ==">":
                    token += char
                    estado = "Q78"
                elif char == ">" and char1 !="=":
                    token += char
                    entrada.seek(entrada.tell()-1)
                    gerar_relatorio(">",linha ,coluna , ListadeTokens)
                    escrever_contagem_arquivo("Tokens_Qtd.txt")
                    estado = "Q0"
                    token = ""
                else:
                    token += char
                    estado = "Q11"
            case "Q9":
                if char == "<" and entrada.read(1) !="=":
                    entrada.seek(entrada.tell()-1)
                    gerar_relatorio("<",linha ,coluna , ListadeTokens)
                    escrever_contagem_arquivo("Tokens_Qtd.txt")
                    token = ""
                    estado = "Q0"
                else:
                    token += char
                    estado = "Q24"
            case "Q10":
                if char == "=":
                    token = char
                    print(token)
                    gerar_relatorio(token,linha ,coluna , ListadeTokens)
                    escrever_contagem_arquivo("Tokens_Qtd.txt")
                    token = ""
                    estado = "Q0"
                elif char != "=":
                    print("error")
                else:
                    token += "="
                    estado = "Q25"
            case "Q11":
                    token += "="
                    coluna +=1
                    gerar_relatorio(token,linha ,coluna , ListadeTokens)
                    escrever_contagem_arquivo("Tokens_Qtd.txt")
                    token = ""
                    estado = "Q0"
            case "Q24":
                if entrada.read(1) !="=":
                    token += "="
                    coluna += 1
                    entrada.seek(entrada.tell()-1)
                    gerar_relatorio(token,linha ,coluna , ListadeTokens)
                    escrever_contagem_arquivo("Tokens_Qtd.txt")
                    token = ""
                    estado = "Q0"
                else:
                    coluna +=1
                    token += "="
                    estado = "Q26"        
            case "Q25":
                    token += "="
                    gerar_relatorio(token,linha ,coluna , ListadeTokens)
                    escrever_contagem_arquivo("Tokens_Qtd.txt")
                    token = ""
                    estado = "Q0"
            case "Q26":
                    coluna += 1
                    token += "="
                    gerar_relatorio(token,linha ,coluna , ListadeTokens)
                    escrever_contagem_arquivo("Tokens_Qtd.txt")
                    token = ""
                    estado = "Q0"
            
            case "Q62": 
                char = entrada.read(1)
                if temp == "\n":
                    print("error quebra de linha")
                elif char !='"':
                    coluna +=1
                    estado = "Q62"
                elif char == '"':
                    coluna +=1
                    token += char
                    estado = "QCadeia"    
                
            case "QCadeia": #estado de aceitacão de cadeia
                gerar_relatorio(token,linha ,coluna , ListadeTokens)
                escrever_contagem_arquivo("Tokens_Qtd.txt")
                token = ""
                estado = "Q0"

            case "Q65":
                token +=char
                char = entrada.read(1)
                coluna +=1
                if char in letras_Maiusculas:
                    token += char
                    estado = "Q66"
                elif char in letras_minusculas:
                    token += char
                    estado = "Q61"       
            case "Q61":
                char = entrada.read(1)
                if char not in letras_minusculas:
                    print(token)
                    estado = "QPalavra"
                    entrada.seek(entrada.tell()-1)
                elif char in letras_minusculas:
                    print(token)
                    token += char
                    estado = "Q61"

            case "Q66":
                char = entrada.read(1)
                coluna +=1
                print(char)
                if char in letras_minusculas:
                    token += char
                    estado = "Q67"
                elif char not in letras_minusculas:
                    estado = "QVariavel"
            case "Q67":
                char = entrada.read(1)
                coluna +=1
                if char in letras_Maiusculas:
                    token += char
                    estado = "Q66"
                else:
                    estado = "QVariavel"

            case "Q68":
                gerar_relatorio("(",linha ,coluna , ListadeTokens)
                estado = "Q0"     
                escrever_contagem_arquivo("Tokens_Qtd.txt")
            case "Q70":
                gerar_relatorio(")",linha ,coluna , ListadeTokens)
                estado = "Q0"
                escrever_contagem_arquivo("Tokens_Qtd.txt")
            case "Q72":
                gerar_relatorio(":",linha ,coluna , ListadeTokens)
                estado = "Q0"
                escrever_contagem_arquivo("Tokens_Qtd.txt")
            case "QComentario":
                char = entrada.read(1)

                if char == "\n" or char == "":
                    gerar_relatorio(token,linha ,coluna , ListadeTokens)
                    estado = "Q0"
                    escrever_contagem_arquivo("Tokens_Qtd.txt")
                else:
                    coluna +=1
                    token += char
                    estado = "QComentario"

            case "Q78":
                token +=">"
                char = entrada.read(1)
                coluna += 1
                if char == ">":
                    coluna += 1
                    token += ">"
                    estado = "Q79"
                else:
                    print("error")

            case "Q79":
                char = entrada.read(1)
                coluna += 1
                token += char
                if char == "<":
                    estado = "Q76"
                else:
                    estado = "Q79"
            case "Q76":
                char = entrada.read(1)
                coluna += 1
                token += char
                if char == "<":
                    estado = "Q80"
                else:
                    estado = "Q79"
            case "Q80":
                char = entrada.read(1)
                if char == "<":
                    token += char 
                    estado = "QComentario><" 
                else:
                    estado = "Q79"
            #cases do INT, possivel Endereço e possivel Floar
            case "Q59":
                char = entrada.read(1)
                if char.isdigit():
                    coluna += 1
                    estado = "Q36" #continuação para inteiro
                    token += char
                elif char == ".":
                    coluna += 1
                    estado = "Q32" #caminho para float
                    token += char
                elif char == "x":
                    coluna += 1
                    estado = "Q55" #caminho para endereço
                    token += char
                else:
                    estado = "QInteiro" #estado de aceitação do inteiro 

            case "Q36":
                char = entrada.read(1)
                if char == "/":
                    coluna += 1
                    estado = "Q38" #caminho para data
                    token += char
                elif char == "_":
                    coluna += 1
                    estado = "Q44" #caminho para data
                    token += char
                elif char.isdigit():
                    coluna += 1
                    estado = "Q15" #continua inteiro
                    token += char
                elif char == ".":
                    coluna += 1
                    estado = "Q32" #caminho float
                    token += char
                else:
                    entrada.seek(entrada.tell()-1)
                    estado = "QInteiro" #aceita Int
            case "Q38":
                char = entrada.read(1)
                if char.isdigit():
                    coluna += 1
                    token += char
                    estado = "Q39"
                else: 
                    entrada.seek(entrada.tell()-1)
                    print("ErrorDeFormataçãoDeData")
                    estado = "Q0"
            case "Q44":
                char = entrada.read(1)
                if char.isdigit():
                    coluna += 1
                    token += char
                    estado = "Q45"
                else:
                    entrada.seek(entrada.tell()-1)
                    print("ErrorDeFormataçãoDeData")
                    estado = "Q0"
            
            case "Q39":
                char = entrada.read(1)
                if char.isdigit():
                    coluna += 1
                    token += char
                    estado = "Q40"
                else:
                    entrada.seek(entrada.tell()-1)
                    print("ErrorDeFormataçãoDeData")
                    estado = "Q0"
            case "Q45":
                char = entrada.read(1)
                if char.isdigit():
                    coluna += 1
                    token += char
                    estado = "Q46"
                else:
                    entrada.seek(entrada.tell()-1)
                    print("ErrorDeFormataçãoDeData")
                    estado = "Q0"
            case "Q40":
                char = entrada.read(1)
                if char == "/":
                    coluna += 1
                    token += char
                    estado = "Q41"
                else:
                    gerar_relatorio(token,linha ,coluna , ListadeTokens)
                    entrada.seek(entrada.tell()-1)
                    print("ErrorDeFormataçãoDeData")
                    token = ""
                    estado = "Q0"
            case "Q46":
                char = entrada.read(1)
                if char == "_":
                    coluna += 1
                    token += char
                    estado = "Q47"
                else:
                    entrada.seek(entrada.tell()-1)
                    print("ErrorDeFormataçãoDeData")
                    estado = "Q0"
            case "Q41":
                char = entrada.read(1)
                if char.isdigit():
                    coluna += 1
                    token += char
                    estado = "Q42"
                else:
                    entrada.seek(entrada.tell()-1)
                    print("ErrorDeFormataçãoDeData")
                    estado = "Q0"
            case "Q47":
                char = entrada.read(1)
                if char.isdigit():
                    coluna += 1
                    token += char
                    estado = "Q48"
                else:
                    entrada.seek(entrada.tell()-1)
                    print("ErrorDeFormataçãoDeData")
                    estado = "Q0"
            case "Q42":
                char = entrada.read(1)
                if char.isdigit():
                    coluna += 1
                    token += char
                    estado = "Q43"
                else:
                    entrada.seek(entrada.tell()-1)
                    print("ErrorDeFormataçãoDeData")
                    estado = "Q0"
            case "Q48":
                char = entrada.read(1)
                if char.isdigit():
                    coluna += 1
                    token += char
                    estado = "Q49"
                else:
                    entrada.seek(entrada.tell()-1)
                    print("ErrorDeFormataçãoDeData")
                    estado = "Q0"
            case "Q43": 
                char = entrada.read(1)
                if char.isdigit():
                    coluna += 1
                    token += char
                    estado = "Q52"
                else:
                    entrada.seek(entrada.tell()-1)
                    print("ErrorDeFormataçãoDeData")
                    estado = "Q0"
            case "Q49":
                char = entrada.read(1)
                if char.isdigit():
                    coluna += 1
                    token += char
                    estado = "Q50"
                else:
                    entrada.seek(entrada.tell()-1)
                    print("ErrorDeFormataçãoDeData")
                    estado = "Q0"
            case "Q52":
                char = entrada.read(1)
                if char.isdigit():
                    coluna += 1
                    token += char
                    estado = "Q51"
                else:
                    entrada.seek(entrada.tell()-1)
                    print("ErrorDeFormataçãoDeData")
                    estado = "Q0"
            case "Q50":
                char = entrada.read(1)
                if char.isdigit():
                    coluna += 1
                    token += char
                    estado = "Q53"
                else:
                    entrada.seek(entrada.tell()-1)
                    print("ErrorDeFormataçãoDeData")
                    estado = "Q0"
            case "Q51":
                estado = "QDataBarra"      
            case "Q53": 
                estado = "QDataIfem"

                


            case "Q54":
                char = entrada.read(1)
                if char == "X":
                    estado = "Q55"
                    token += char
                else:
                    print("Error")

            case "Q55":
                char = entrada.read(1)
                if char in letras_exadecimal or char.isdigit():
                    coluna += 1
                    estado = "Q55"
                    token += char
                else:
                    entrada.seek(entrada.tell()-1)
                    estado = "QEndereco"
            
            case "Q15":
                char = entrada.read(1)
                if char == ".": #caminho para Float
                    coluna += 1
                    estado = "Q32"
                    token += char
                elif char.isdigit():
                    coluna += 1
                    estado = "Q16" #continua Int
                    token += char
                else:
                    estado = "QInteiro"
            case "Q16":
                char = entrada.read(1)
                if char.isdigit():
                    coluna += 1
                    estado = "Q16"
                    token += char
                else:
                    entrada.seek(entrada.tell()-1)
                    estado = "QInteiro"

            case "QInteiro":
                print(token)
                gerar_relatorio(token,linha ,coluna , ListadeTokens)
                estado = "Q0"
                token = ""

            case "Q32": #saindo de int para caminho do Float
                char = entrada.read(1)
                if char.isdigit():
                    estado = "Q33"
                    token += char
                else:
                    print("ERROR")

            #cases do floar
            case "Q28":
                char = entrada.read(1)
                token += char
                coluna += 1
                if char.isdigit():
                    estado = "Q33"
                else:
                    print("Error")
            case "Q33":
                char = entrada.read(1)
                if  char == "e":
                    coluna += 1
                    estado = "Q35"
                    token += char

                elif char.isdigit():
                    coluna += 1
                    estado = "Q33"
                    token += char
                else:
                    entrada.seek(entrada.tell()-1)
                    estado = "QFloat"

            case "Q35":
                char = entrada.read(1)
                if char == "-":
                    coluna += 1
                    estado = "Q34"
                    token += char
                elif char.isdigit():
                    coluna += 1
                    estado = "Q13"
                    token += char
            case "Q34":
                char = entrada.read(1)
                if char.isdigit():
                    coluna += 1
                    estado = "Q34"
                    token += char
                else:
                    entrada.seek(entrada.tell()-1)
                    estado = "QFloat"
            case "Q13":
                char = entrada.read(1)
                if char.isdigit():
                    coluna += 1
                    estado = "Q13"
                    token += char
                else:
                    entrada.seek(entrada.tell()-1)
                    estado = "QFloat"
                
            case "QDataBarra":
                print("Qfloat",token)
                gerar_relatorio(token,linha ,coluna , ListadeTokens)
                estado = "Q0"
                token = ""
                escrever_contagem_arquivo("Tokens_Qtd.txt")
            case "QDataIfem":
                print("Qfloat",token)
                gerar_relatorio(token,linha ,coluna , ListadeTokens)
                estado = "Q0"
                token = ""
                escrever_contagem_arquivo("Tokens_Qtd.txt")

            case "QEndereco":
                print("Qfloat",token)
                gerar_relatorio(token,linha ,coluna , ListadeTokens)
                estado = "Q0"
                token = ""
                escrever_contagem_arquivo("Tokens_Qtd.txt")

            case "QFloat":
                print("Qfloat",token)
                gerar_relatorio(token,linha ,coluna , ListadeTokens)
                estado = "Q0"
                token = ""
                escrever_contagem_arquivo("Tokens_Qtd.txt")
            
            case "QComentario><":
                print(token)
                gerar_relatorio(token,linha ,coluna , ListadeTokens)
                estado = "Q0"
                token = ""
                escrever_contagem_arquivo("Tokens_Qtd.txt")


            case "QPalavra": #estado de aceitacão de cadeia
                gerar_relatorio(token,linha ,coluna , ListadeTokens)
                token = ""
                estado = "Q0"
                escrever_contagem_arquivo("Tokens_Qtd.txt")

            case "QVariavel":
                gerar_relatorio(token,linha ,coluna , ListadeTokens)
                token = ""
                estado = "Q0"
                escrever_contagem_arquivo("Tokens_Qtd.txt")

                  

        if char == "":
            break
                             
        if char == "\n":
            linha += 1
            coluna = 1

        if char =="" or char =="/n":
            estado = "Q0"
        
            
   
    return f"Fim da leitura"  # Se chegamos ao final da entrada e não estamos no estado de aceitação, retorna False


# Exemplo de uso:
#entrada1 = "12/31/2023 "S

with open("Texto.txt", 'r') as arquivo:
    automato_data(arquivo)