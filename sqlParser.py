def getAlphabet():
    return "\nabcdefghijklmnopqrstuvwxyz ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789()[],;*="

def getReserveds():
    return ['CREATE', 'DATABASE', ';', 'USE', 'TABLE', '(', ')', ',', 'VALUES', '*', 'INSERT', 'INTO', 'SELECT', 'FROM', 'ORDER', 'BY', 'WHERE', '=', 'UPDATE', 'SET', 'DELETE', 'TRUNCATE', 'TABLE']

def getTipos():
    return ["TEXT", "CHAR", "VARCHAR", "INT", "BIT" "BINARY", "DATETIME", "FLOAT", "DOUBLE", "DECIMAL", "DATE", "TIME"]

class sqlParser():
    tokens = []
    i = -1
    alphabet = getAlphabet()
    reserveds = getReserveds()
    tipos = getTipos()
    token = ""

    def __init__(self, word) -> None:
        self.lexer(word)
    
    def lexer(self, word):
        reading = False
        begin = 0

        for i in range(len(word)):
            if word[i] not in self.alphabet:
                raise Exception("Symbol not in alphabet")

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

        self.tokens.append("$")

        for i in range(len(self.tokens)):
            self.tokens[i] = self.tokens[i].upper()
        
        self.parser(self.tokens)

    def getToken(self) -> str:
        self.i += 1

        if self.i < len(self.tokens):
            return self.tokens[self.i]
        else:
            raise Exception("No more tokens")
        
    def parser(self, tokens):
        self.init()
        print("Entrada Reconhecida")

    def init(self):
        self.token = self.getToken()

        if self.token == "USE":
            self.ID()

            token = self.getToken()
            
            if token != ";":
                raise Exception("; expected")
            
            self.init()
        
        elif self.token == "CREATE":
            self.create()
            self.init()

        elif self.token == "UPDATE":
            self.ID()

            self.token = self.getToken()
            if self.token != "SET":
                raise Exception("SET expected")
            
            self.ID()

            self.token = self.getToken()
            if self.token != "=":
                raise Exception("= expected")

            self.VALOR()

            self.token = self.getToken()
            if self.token != "WHERE":
                raise Exception("WHERE expected")
            
            self.ID()

            self.token = self.getToken()
            if self.token != "=":
                raise Exception("= expected")
            
            self.VALOR()

            self.token = self.getToken()
            if self.token != ";":
                raise Exception("; expected")
            
            self.init()

        elif self.token == "DELETE":
            self.token = self.getToken()
            if self.token != "FROM":
                raise Exception("FROM expected")
            
            self.ID()

            self.token = self.getToken()
            if self.token != "WHERE":
                raise Exception("WHERE expected")
            
            self.ID()

            self.token = self.getToken()
            if self.token != "=":
                raise Exception("= expected")
            
            self.VALOR()

            self.token = self.getToken()
            if self.token != ";":
                raise Exception("; expected")
            
            self.init()

        elif self.token == "TRUNCATE":
            self.token = self.getToken()
            if self.token != "TABLE":
                raise Exception("TABLE expected")
            
            self.ID()

            self.token = self.getToken()
            if self.token != ";":
                raise Exception("; expected")
            
            self.init()
        
        elif self.token == "INSERT":
            self.token = self.getToken()
            if self.token != "INTO":
                raise Exception("INTO expected")
            
            self.ID()

            self.token = self.getToken()
            if self.token != "(":
                raise Exception("( expected")
            
            self.listaDeId()

            self.token = self.getToken()
            if self.token != "VALUES":
                raise Exception("VALUES expected")
            
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
                    raise Exception("FROM expected")
                
                self.ID()

                self.token = self.getToken()
                if self.token != ";":
                    raise Exception("; expected")
                
                self.init()
            else:
                raise Exception("* or id expected")

        elif self.token == "$":
            pass

        else:
            raise Exception("SELECT, USE, CREATE, UPDATE, DELETE, TRUNCATE or INSERT expected")
    
    def create(self):
        self.token = self.getToken()

        if self.token == "TABLE":
            self.ID()

            self.token = self.getToken()

            if self.token != "(":
                raise Exception("( expected")
            
            self.listaDeTipos()

            self.token = self.getToken()

            if self.token != ";":
                raise Exception("; expected")

        elif self.token == "DATABASE":
            self.ID()
            
            self.token = self.getToken()

            if self.token != ";":
                raise Exception("; expected")
        else:
            raise Exception("TABLE or DATABASE expected")
    
    def listaDeTipos(self):
        self.ID()
        self.TIPO()

        self.token = self.getToken()

        if self.token == ",":
            self.listaDeTipos()

        elif self.token != ")":
            raise Exception(") expected")
        
    def listaDeId(self):
        self.ID()

        self.token = self.getToken()

        if self.token == ",":
            self.listaDeId()
        
        elif self.token != ")":
            raise Exception(") expected")
        
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
            raise Exception(") expected")
        
    def listaDeListaDeValor(self):
        self.token = self.getToken()
        if self.token != "(":
            raise Exception("( expected")
        
        self.listaDeValor()

        self.token = self.getToken()

        if self.token == ",":
            self.listaDeListaDeValor()

        elif self.token != ";":
            raise Exception("; expected")
        
    def asterisco(self):
        self.token = self.getToken()

        if self.token != "FROM":
            raise Exception("FROM expected")
        
        self.ID()

        self.token = self.getToken()

        if self.token == ";":
            pass
        elif self.token == "WHERE":
            self.ID()

            self.token = self.getToken()
            if self.token != "=":
                raise Exception("= expected")
            
            self.VALOR()

            self.token = self.getToken()
            if self.token != ";":
                raise Exception("; expected")
            
        elif self.token == "ORDER":
            self.token = self.getToken()
            if self.token != "BY":
                raise Exception("BY expected")
            
            self.ID()

            self.token = self.getToken()
            if self.token != ";":
                raise Exception("; expected")

        else:
            raise Exception(";, WHERE or ORDER expected")
        
    def ID(self):
        self.token = self.getToken()

        if self.token[0].isdigit() or self.token.isdigit() or (self.token in self.reserveds):
            raise Exception("id expected")
        
    def TIPO(self):
        self.token = self.getToken()

        if self.token not in self.tipos:
            raise Exception("INT or VARCHAR expected") #TODO mudar tipos
        
    def VALOR(self):
        self.token = self.getToken()

        if not self.token.isdigit():
            raise Exception("valor expected")

    def printTokens(self):
        for token in self.tokens:
            if token != "$":
                print(token)
