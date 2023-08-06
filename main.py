# TRABALHO DE LINGUAGENS DE PROGRAMAÇÃO
# Alunos: Ícaro Gabryel de Araujo Silva e Claudiney Ryan da Silva
# Parser SQL

from Parser import sqlParser

def main():
    while True:
        entrada = input("Digite um ou mais comandos SQL: ")

        try:
            sqlParser(entrada)
        except:
            continue

if __name__ == "__main__":
    main()
