# TRABALHO DE LINGUAGENS DE PROGRAMAÇÃO
# Alunos: Ícaro Gabryel de Araujo Silva e Claudiney Ryan da Silva
# Parser SQL

from Parser import sqlParser

def main():
    entrada = input("Digite um ou mais comandos SQL: ")
    obj = sqlParser()
    
    try:
        obj.parse(entrada)
    except Exception as e:
        print(e)

    del obj


if __name__ == "__main__":
    while True:
        main()