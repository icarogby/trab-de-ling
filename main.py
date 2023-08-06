from sqlParser import sqlParser

def main():
    with open ("comandos.txt", "r") as file:
        comandos = file.read()

    teste = sqlParser(comandos)


if __name__ == "__main__":
    main()
