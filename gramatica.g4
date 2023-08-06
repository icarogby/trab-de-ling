init: "USE" ID ";"
    | "CREATE" create
    | "UPDATE" ID "SET" ID "=" VALOR "WHERE" ID "=" VALOR ";"
    | "DELETE" "FROM" ID "WHERE" ID "=" VALOR
    | "TRUNCATE" "TABLE" ID ";" 
    | "INSERT" "INTO" ID "(" listaDeId ")" "VALUES" listaDeListaDeValor ";"
    | "SELECT" [asterisco | listaDeId "FROM" ID ";"]

create: "TABLE" ID "(" listaDeTipos ")" ";"
      | "DATABASE" ID ";"

ListaDeTipos: ID TIPO ["," ID TIPO]*
listaDeId: ID ["," ID]*
listaDeListaDeValor: "(" listaDeValor ")" ["," "(" listaDeValor ")"]*
listaDeValor: VALOR ["," VALOR]*
asterisco: "*" "FROM" ID [";" | "OTHER" "BY" ID ";" | "WHERE" ID "=" VALOR ";"]

ID: [a-zA-Z][a-zA-Z0-9]
VALOR: [0-9]+
TIPO: "INT"
    | "VARCHAR"
    | "DATE"
    | Outros tipos