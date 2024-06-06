def inteiro(Conteudo):
    for each in Conteudo:
        try:
            if each == "/":
                return data(Conteudo)
              
            if not((0<= int(each) <=9)):
                return 
             
        except:
            return "Error-Int"  
          
    return f"Inteiro"
    
def data(Conteudo):
    
    cont = 0

    for each in Conteudo:
        if cont == 2 or cont == 5:  
            if each != "/": 
                return "Erro-Data1"
            
        elif not each.isdigit(): 
            return "Erro-Data2"
        
        cont += 1 

    if cont != 10 or int(Conteudo[:2]) > 31 or int(Conteudo[3:5]) > 12 or int(Conteudo[6:]) < 1900:
        return "Erro-Data3"
    
    return f"DATA"

def ler_arquivo(nome_arquivo):
    with open(nome_arquivo, 'r') as arquivo:
        conteudo = arquivo.read()
    return conteudo
    
nome_do_arquivo = 'Texto.txt' 
conteudo_do_arquivo = ler_arquivo(nome_do_arquivo)

print(inteiro(conteudo_do_arquivo))
