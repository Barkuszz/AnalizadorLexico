import re

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

def verifica_comentario(token):
    padrao = re.compile(r'^>>>(.*?)<<<$')
    return bool(padrao.match(token))

def verifica_Comentario(token):
    padrao = re.compile(r'^#.*$')
    return bool(padrao.match(token))

def verifica_palavra(cadeia):
    padrao = re.compile(r'^[a-zA-Z]+$')
    return bool(padrao.match(cadeia))

def verifica_padrao(token):
    padrao = re.compile(r'^[a-z][A-Z][a-zA-Z]*$')
    return bool(padrao.match(token))

def gerar_relatorio(token, linha, coluna, ListadeTokens):

    if verifica_padrao(token):
        lexema_str = "TOKEN_NOME_DE_VARIAVEL"
    elif verifica_Comentario(token):
        lexema_str = "TOKEN_COMENTARIO>>><<<"
    elif verifica_Comentario(token):
        lexema_str = "TOKEN_COMENTARIO"
    elif verifica_palavra(token):
         lexema_str = "TOKEN_PALAVRA"
    else:
        lexema_str = lexemas.get(token, "Lexema nao definido")

    with open(ListadeTokens, 'a') as relatorio:
        relatorio.write(f"| {linha:<4} | {coluna:<4} | {token:<25} | {lexema_str:<25} |\n")
        relatorio.write(f"+------+------+---------------------------+---------------------------+\n")

    return "Relatório gerado com sucesso."


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




    with open(ListadeTokens, 'w') as relatorio:

        relatorio.write(f"TOKENS RECONHECIDOS:\n\n")
        relatorio.write(f"+------+------+---------------------------+---------------------------+\n")
        relatorio.write(f"| LIN  | COL  | {'TOKEN':<25} | {'LEXEMA':<25} |\n")
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
                     
                
                
            case "Q1":
                    gerar_relatorio("|",linha ,coluna , ListadeTokens)
                    estado = "Q0"
            case "Q2":
                    gerar_relatorio("-",linha ,coluna , ListadeTokens)
                    estado = "Q0"
            case "Q3":
                    gerar_relatorio("~",linha ,coluna , ListadeTokens)
                    estado = "Q0"
            case "Q4":
                    gerar_relatorio("+",linha ,coluna , ListadeTokens)
                    estado = "Q0"
            case "Q5":
                    gerar_relatorio("*",linha ,coluna , ListadeTokens)
                    estado = "Q0"
            case "Q6":
                    gerar_relatorio("%",linha ,coluna , ListadeTokens)
                    estado = "Q0"
            case "Q7":
                    gerar_relatorio("&",linha ,coluna , ListadeTokens)
                    estado = "Q0"
            case "Q8":
                if char == ">" and entrada.read(1) !="=":
                    token += char
                    entrada.seek(entrada.tell()-1)
                    gerar_relatorio(">",linha ,coluna , ListadeTokens)
                    estado = "Q0"
                    token = ""
                elif char == ">" and entrada.read(1) ==">":
                    token += char
                    estado = "Q78"
                else:
                    token += char
                    estado = "Q11"
            case "Q9":
                if char == "<" and entrada.read(1) !="=":
                    entrada.seek(entrada.tell()-1)
                    gerar_relatorio("<",linha ,coluna , ListadeTokens)
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
                    token = ""
                    estado = "Q0"
            case "Q24":
                if entrada.read(1) !="=":
                    token += "="
                    entrada.seek(entrada.tell()-1)
                    gerar_relatorio(token,linha ,coluna , ListadeTokens)
                    token = ""
                    estado = "Q0"
                else:
                    coluna +=1
                    token += "="
                    estado = "Q26"        
            case "Q25":
                    token += "="
                    gerar_relatorio(token,linha ,coluna , ListadeTokens)
                    token = ""
                    estado = "Q0"
            case "Q26":
                    coluna += 1
                    token += "="
                    gerar_relatorio(token,linha ,coluna , ListadeTokens)
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
            case "Q70":
                gerar_relatorio(")",linha ,coluna , ListadeTokens)
                estado = "Q0"
            case "Q72":
                gerar_relatorio(":",linha ,coluna , ListadeTokens)
                estado = "Q0"
            case "QComentario":
                char = entrada.read(1)

                if char == "\n" or char == "":
                    gerar_relatorio(token,linha ,coluna , ListadeTokens)
                    estado = "Q0"
                else:
                    coluna +=1
                    token += char
                    estado = "QComentario"

            case "Q78":
                token +=">"
                char = entrada.read(1)
                if char == ">":
                    coluna += 1
                    token += ">"
                    estado = "Q79"
                else:
                    print("error")

            case "Q79":
                char = entrada.read(1)
                token += char
                if char == "<":
                    estado = "Q76"
                else:
                    estado = "Q79"
            case "Q76":
                char = entrada.read(1)
                if char == "<":
                    token += char
                    estado = "Q80"
                else:
                    print("error")
            case "Q80":
                char = entrada.read(1)
                if char == "<":
                    token += char  
            



            case "QPalavra": #estado de aceitacão de cadeia
                gerar_relatorio(token,linha ,coluna , ListadeTokens)
                token = ""
                estado = "Q0"

            case "QVariavel":
                gerar_relatorio(token,linha ,coluna , ListadeTokens)
                token = ""
                estado = "Q0"

                  

        if char == "":
            break
                             
        if char == "\n":
            linha += 1
            coluna = 1

        if char =="" or char =="/n":
            estado = "Q0"
        
        def caso_QPalavra(token, linha, coluna, ListadeTokens): #função para quando terminarmos de ler uma palavra
            gerar_relatorio(token,linha ,coluna , ListadeTokens)

        def caso_QVariaveis(token, linha, coluna, ListadeTokens):  #função para quando terminarmos de ler uma variavel
            gerar_relatorio(token,linha ,coluna , ListadeTokens)

            
   
    return f"Fim da leitura"  # Se chegamos ao final da entrada e não estamos no estado de aceitação, retorna False


# Exemplo de uso:
#entrada1 = "12/31/2023 "S

with open("Texto.txt", 'r') as arquivo:
    automato_data(arquivo)
    







