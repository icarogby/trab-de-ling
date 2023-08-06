def getAlphabet():
    return "\nabcdefghijklmnopqrstuvwxyz ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789()[],;*="

def getReserveds():
    return ['CREATE', 'DATABASE', ';', 'USE', 'TABLE', '(', ')', ',', 'VALUES', '*', 'INSERT', 'INTO', 'SELECT', 'FROM', 'ORDER', 'BY', 'WHERE', '=', 'UPDATE', 'SET', 'DELETE', 'TRUNCATE', 'TABLE']

def getTipos():
    return ["TEXT", "CHAR", "VARCHAR", "INT", "BIT" "BINARY", "DATETIME", "FLOAT", "DOUBLE", "DECIMAL", "DATE", "TIME"]

class sqlParser():
    tokens = [] # Lista que irá guardar os tokens
    i = -1 # Índice que irá pegar o token atual da lista de tokens

    # Lista com o alfabeto da linguagem, palavras reservadas e tipos de dados
    alphabet = getAlphabet()
    reserveds = getReserveds()
    tipos = getTipos()

    # Variável que irá guardar os tokens toda vez que chamar a função getToken()
    token = ""

    # Inicia a classe passando a String de entrada e chamando o analizador léxico
    def __init__(self, word) -> None:
        self.lexer(word)
    
    # Função que separa a String de entrada em tokens
    def lexer(self, word):
        reading = False
        begin = 0

        # loop que irá percorrer a String de entrada
        for i in range(len(word)):
            # Verifica de o caractere atual é um símbolo do alfabeto
            if word[i] not in self.alphabet:
                print(f"Erro léxico: {word[i]} não pertence ao alfabeto")
                raise Exception(f"Erro léxico: {word[i]} não pertence ao alfabeto")

            # Verifica se está lendo um token com mais de um caractere ou apenas um caractere
            if reading:
                if word[i] in "=*()[],; ":
                    self.tokens.append(word[begin:i])

                    if word[i] != " ":
                        self.tokens.append(word[i])
                    
                    reading = False

                elif i == (len(word) - 1):
                    self.tokens.append(word[begin:])
                    
                    reading = False

            else:
                if word[i] == " " or word[i] == "\n":
                    pass
                elif word[i] in "=*()[],;":
                    self.tokens.append(word[i])
                else:
                    reading = True
                    begin = i

        # Adiciona o símbolo de fim da fita que irá ser usado pelo parser
        self.tokens.append("$")

        # Transforma todos os tokens em maiúsculo para ser comparado nos ifs
        for i in range(len(self.tokens)):
            self.tokens[i] = self.tokens[i].upper()
        
        # Chama o parser
        self.parser(self.tokens)

    # Função que pega o próximo token da lista de tokens
    def getToken(self) -> str:
        self.i += 1

        if self.i < len(self.tokens):
            return self.tokens[self.i]
        else:
            print("Fim da fita")
            raise Exception("Fim da fita")
        
    def parser(self, tokens):
        # chama a função que representa a primeira regra de produção da gramática
        self.init()

        # Se não houver erros em init(), imprime que a entrada foi reconhecida
        print("Entrada Reconhecida")

    def init(self):
        self.token = self.getToken()

        if self.token == "USE":
            self.ID()

            token = self.getToken()
            
            if token != ";":
                print("Erro Sintático: \";\" era esperado")
                raise Exception("Erro Sintático: \";\" era esperado")
            
            self.init()
        
        elif self.token == "CREATE":
            self.create()
            self.init()

        elif self.token == "UPDATE":
            self.ID()

            self.token = self.getToken()

            if self.token != "SET":
                print("Erro Sintático: \"SET\" era esperado")
                raise Exception("Erro Sintático: \"SET\" era esperado")
            
            self.ID()

            self.token = self.getToken()
            if self.token != "=":
                print("Erro Sintático: \"=\" era esperado")
                raise Exception("Erro Sintático: \"=\" era esperado")

            self.VALOR()

            self.token = self.getToken()
            if self.token != "WHERE":
                print("Erro Sintático: \"WHERE\" era esperado")
                raise Exception("Erro Sintático: \"WHERE\" era esperado")
            
            self.ID()

            self.token = self.getToken()
            if self.token != "=":
                print("Erro Sintático: \"=\" era esperado")
                raise Exception("Erro Sintático: \"=\" era esperado")
            
            self.VALOR()

            self.token = self.getToken()
            if self.token != ";":
                print("Erro Sintático: \";\" era esperado")
                raise Exception("Erro Sintático: \";\" era esperado")
            
            self.init()

        elif self.token == "DELETE":
            self.token = self.getToken()
            if self.token != "FROM":
                print("Erro Sintático: \"FROM\" era esperado")
                raise Exception("Erro Sintático: \"FROM\" era esperado")
            
            self.ID()

            self.token = self.getToken()
            if self.token != "WHERE":
                print("Erro Sintático: \"WHERE\" era esperado")
                raise Exception("Erro Sintático: \"WHERE\" era esperado")
            
            self.ID()

            self.token = self.getToken()
            if self.token != "=":
                print("Erro Sintático: \"=\" era esperado")
                raise Exception("Erro Sintático: \"=\" era esperado")
            
            self.VALOR()

            self.token = self.getToken()
            if self.token != ";":
                print("Erro Sintático: \";\" era esperado")
                raise Exception("Erro Sintático: \";\" era esperado")
            
            self.init()

        elif self.token == "TRUNCATE":
            self.token = self.getToken()
            if self.token != "TABLE":
                print("Erro Sintático: \"TABLE\" era esperado")
                raise Exception("Erro Sintático: \"TABLE\" era esperado")
            
            self.ID()

            self.token = self.getToken()
            if self.token != ";":
                print("Erro Sintático: \"TABLE\" era esperado")
                raise Exception("Erro Sintático: \";\" era esperado")
            
            self.init()
        
        elif self.token == "INSERT":
            self.token = self.getToken()
            if self.token != "INTO":
                print("Erro Sintático: \"INTO\" era esperado")
                raise Exception("Erro Sintático: \"INTO\" era esperado")
            
            self.ID()

            self.token = self.getToken()
            if self.token != "(":
                print("Erro Sintático: \"(\" era esperado")
                raise Exception("Erro Sintático: \"(\" era esperado")
            
            self.listaDeId()

            self.token = self.getToken()
            if self.token != "VALUES":
                print("Erro Sintático: \"VALUES\" era esperado")
                raise Exception("Erro Sintático: \"VALUES\" era esperado")
            
            self.listaDeListaDeValor()

            self.init()

        elif self.token == "SELECT":
            self.token = self.getToken()

            if self.token == "*":
                self.asterisco()

                self.init()
            
            elif not (self.token[0].isdigit() or self.token.isdigit() or (self.token in self.reserveds)):
                self.token = self.getToken()
                if self.token == ",":
                    self.listaDeIdAberta()

                if self.token != "FROM":
                    print("Erro Sintático: \"FROM\" era esperado")
                    raise Exception("Erro Sintático: \"FROM\" era esperado")
                
                self.ID()

                self.token = self.getToken()
                if self.token != ";":
                    print("Erro Sintático: \";\" era esperado")
                    raise Exception("Erro Sintático: \";\" era esperado")
                
                self.init()
            else:
                print("Erro Sintático: \"*\" ou ID era esperado")
                raise Exception("Erro Sintático: \"*\" ou ID era esperado")

        elif self.token == "$":
            pass

        else:
            print("Erro Sintático: \"USE\", \"CREATE\", \"UPDATE\", \"DELETE\", \"TRUNCATE\", \"INSERT\", \"SELECT\" ou \"*\" era esperado")
            raise Exception("Erro Sintático: \"USE\", \"CREATE\", \"UPDATE\", \"DELETE\", \"TRUNCATE\", \"INSERT\", \"SELECT\" ou \"*\" era esperado")
    
    def create(self):
        self.token = self.getToken()

        if self.token == "TABLE":
            self.ID()

            self.token = self.getToken()

            if self.token != "(":
                print("Erro Sintático: \"(\" era esperado")
                raise Exception("Erro Sintático: \"(\" era esperado")
            
            self.listaDeTipos()

            self.token = self.getToken()

            if self.token != ";":
                print("Erro Sintático: \";\" era esperado")
                raise Exception("Erro Sintático: \";\" era esperado")

        elif self.token == "DATABASE":
            self.ID()
            
            self.token = self.getToken()

            if self.token != ";":
                print("Erro Sintático: \";\" era esperado")
                raise Exception("Erro Sintático: \";\" era esperado")
        else:
            print("Erro Sintático: \"TABLE\" ou \"DATABASE\" era esperado")
            raise Exception("Erro Sintático: \"TABLE\" ou \"DATABASE\" era esperado")
    
    def listaDeTipos(self):
        self.ID()
        self.TIPO()

        self.token = self.getToken()

        if self.token == ",":
            self.listaDeTipos()

        elif self.token != ")":
            print("Erro Sintático: \")\" era esperado")
            raise Exception("Erro Sintático: \")\" era esperado")
        
    def listaDeId(self):
        self.ID()

        self.token = self.getToken()

        if self.token == ",":
            self.listaDeId()
        
        elif self.token != ")":
            print("Erro Sintático: \")\" era esperado")
            raise Exception("Erro Sintático: \")\" era esperado")
        
    def listaDeIdAberta(self):
        self.ID()

        self.token = self.getToken()

        if self.token == ",":
            self.listaDeIdAberta()
        
    def listaDeValor(self):
        self.VALOR()

        self.token = self.getToken()

        if self.token == ",":
            self.listaDeValor()
        
        elif self.token != ")":
            print("Erro Sintático: \")\" era esperado")
            raise Exception("Erro Sintático: \")\" era esperado")
        
    def listaDeListaDeValor(self):
        self.token = self.getToken()
        if self.token != "(":
            print("Erro Sintático: \"(\" era esperado")
            raise Exception("Erro Sintático: \"(\" era esperado")
        
        self.listaDeValor()

        self.token = self.getToken()

        if self.token == ",":
            self.listaDeListaDeValor()

        elif self.token != ";":
            print("Erro Sintático: \";\" era esperado")
            raise Exception("Erro Sintático: \";\" era esperado")
        
    def asterisco(self):
        self.token = self.getToken()

        if self.token != "FROM":
            print("Erro Sintático: \"FROM\" era esperado")
            raise Exception("Erro Sintático: \"FROM\" era esperado")
        
        self.ID()

        self.token = self.getToken()

        if self.token == ";":
            pass
        elif self.token == "WHERE":
            self.ID()

            self.token = self.getToken()
            if self.token != "=":
                print("Erro Sintático: \"=\" era esperado")
                raise Exception("Erro Sintático: \"=\" era esperado")
            
            self.VALOR()

            self.token = self.getToken()
            if self.token != ";":
                print("Erro Sintático: \";\" era esperado")
                raise Exception("Erro Sintático: \";\" era esperado")
            
        elif self.token == "ORDER":
            self.token = self.getToken()
            if self.token != "BY":
                print("Erro Sintático: \"BY\" era esperado")
                raise Exception("Erro Sintático: \"BY\" era esperado")
            
            self.ID()

            self.token = self.getToken()
            if self.token != ";":
                print("Erro Sintático: \";\" era esperado")
                raise Exception("Erro Sintático: \";\" era esperado")

        else:
            print("Erro Sintático: \";\", \"WHERE\" ou \"ORDER\" era esperado")
            raise Exception("Erro Sintático: \";\", \"WHERE\" ou \"ORDER\" era esperado")
        
    def ID(self):
        self.token = self.getToken()

        if self.token[0].isdigit() or self.token.isdigit() or (self.token in self.reserveds):
            print("Erro Sintático: ID era esperado")
            raise Exception("Erro Sintático: ID era esperado")
        
    def TIPO(self):
        self.token = self.getToken()

        if self.token not in self.tipos:
            print("Erro Sintático: INR ou VARCHAR era esperado")
            raise Exception("Erro Sintático: INR ou VARCHAR era esperado")
        
    def VALOR(self):
        self.token = self.getToken()

        if not self.token.isdigit():
            print("Erro Sintático: VALOR era esperado")
            raise Exception("Erro Sintático: VALOR era esperado")

    def printTokens(self):
        for token in self.tokens:
            if token != "$":
                print(token)
