from datetime import datetime

def verifica_data_valida(data):
    try:
        formato = "%d/%m/%Y" if '/' in data else "%d_%m_%Y"
        datetime.strptime(data, formato)
        return True
    except ValueError:
        return False

# Exemplos de uso
print(verifica_data_valida("12/04/2022"))   # Saída: True
print(verifica_data_valida("12_04_2022"))   # Saída: True
print(verifica_data_valida("31/02/2022"))   # Saída: False (fevereiro não tem 31 dias)
print(verifica_data_valida("31_02_2022"))   # Saída: False (fevereiro não tem 31 dias)
print(verifica_data_valida("29/02/2021"))   # Saída: False (2021 não é um ano bissexto)
