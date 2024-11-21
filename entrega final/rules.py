#Non-terminal identificators
MS = "MS"
SCont = "SCont"
Body = "Body"
IdType = "IdType"
IdTypeBody = "IdTypeBody"
IdTypeBodyVar = "IdTypeBodyVar"
IdTypeBodyFnc = "IdTypeBodyFnc"
BodyAux = "BodyAux"
SBlq = "SBlq"
Blq = "Blq"
ContBlq = "ContBlq"
BlqAux = "BlqAux"
SPar = "SPar"
ParAux = "ParAux"
ParOtr = "ParOtr"
SFnc = "SFnc"
FBody = "FBody"
DvS = "DvS"
DvOtr = "DvOtr"
DvAsg = "DvAsg"
DvVal = "DvVal"
SAsig = "SAsig"
OpAA = "OpAA"
OpAB = "OpAB"
OpAA2 = "OpAA2"
Opr = "Opr"
OpAA1 = "OpAA1"
SLib = "SLib"
SIf = "SIf"
Else = "Else"
Else2 = "Else2"
SWhl = "SWhl"
SCond = "SCond"
Cond = "Cond"
CondB = "CondB"
OpC = "OpC"
CondA = "CondA"

# '''
table = [
    [MS, 'INCLUDE', [SLib, SCont]],
    [MS, 'LPAREN', None],
    [MS, 'RPAREN', None],
    [MS, 'TIMES', None],
    [MS, 'PLUS', None],
    [MS, 'MINUS', None],
    [MS, 'DIVIDE', None],
    [MS, 'COMMA', None],
    [MS, 'SEMICOLON', None],
    [MS, 'ASSIGNMENT', None],
    [MS, 'CONSTANT', None],
    [MS, 'DATATYPE', [SLib, SCont]],
    [MS, 'ID', None],
    [MS, 'LBRACE', None],
    [MS, 'RBRACE', None],
    [MS, 'NOTEQUALS', None],
    [MS, 'LESS', None],
    [MS, 'GREATER', None],
    [MS, 'AND', None],
    [MS, 'OR', None],
    [MS, 'IF', None],
    [MS, 'ELSE', None],
    [MS, 'WHILE', None],
    [MS, 'eof', [SLib, SCont]],
    [SLib, 'INCLUDE', ['INCLUDE', SLib]],
    [SLib, 'LPAREN', None],
    [SLib, 'RPAREN', None],
    [SLib, 'TIMES', None],
    [SLib, 'PLUS', None],
    [SLib, 'MINUS', None],
    [SLib, 'DIVIDE', None],
    [SLib, 'COMMA', None],
    [SLib, 'SEMICOLON', None],
    [SLib, 'ASSIGNMENT', None],
    [SLib, 'CONSTANT', None],
    [SLib, 'DATATYPE', ['vacia']],
    [SLib, 'ID', None],
    [SLib, 'LBRACE', None],
    [SLib, 'RBRACE', None],
    [SLib, 'NOTEQUALS', None],
    [SLib, 'LESS', None],
    [SLib, 'GREATER', None],
    [SLib, 'AND', None],
    [SLib, 'OR', None],
    [SLib, 'IF', None],
    [SLib, 'ELSE', None],
    [SLib, 'WHILE', None],
    [SLib, 'eof', ['vacia']],
    [SCont, 'INCLUDE', None],
    [SCont, 'LPAREN', None],
    [SCont, 'RPAREN', None],
    [SCont, 'TIMES', None],
    [SCont, 'PLUS', None],
    [SCont, 'MINUS', None],
    [SCont, 'DIVIDE', None],
    [SCont, 'COMMA', None],
    [SCont, 'SEMICOLON', None],
    [SCont, 'ASSIGNMENT', None],
    [SCont, 'CONSTANT', None],
    [SCont, 'DATATYPE', [Body, BodyAux]],
    #nuevas reglas
    [SCont, 'ID', [SFnc]],
    [SFnc, 'LPAREN', ['LPAREN', SPar, 'RPAREN', 'LBRACE', Blq, 'RBRACE']],
    [SPar, 'DATATYPE', ['DATATYPE', 'ID', ParAux]],
    [SPar, 'ID', ['OpAA', ParAux]],                 # Procesar argumentos (expresiones)
    [SPar, 'ID', ['ID', ParAux]],                  # Identificador como argumento
    [SPar, 'RPAREN', ['vacia']],                    # Sin argumentos
    [SPar, 'CONSTANT', ['OpAA', ParAux]],          # Procesar constantes como argumentos
    [SPar, 'CONSTANT', ['CONSTANT', ParAux]],      # Constante como argumento
    [ParAux, 'COMMA', ['COMMA', SPar]],              # Separador de parámetros
    [ParAux, 'RPAREN', ['vacia']],                   # Cierre de parámetros
    [Blq, 'RETURN', ['RETURN', OpAA, 'SEMICOLON', BlqAux]],  # Procesar 'return'
    [OpAA, 'ID', ['ID', OpAB]],                             # Operando inicial
    [OpAA, 'ID', ['ID']],
    [OpAA, 'ID', ['ID', 'LPAREN', SPar, 'RPAREN']],  # ID con paréntesis y argumentos
    [OpAA, 'CONSTANT', ['CONSTANT']],              # Constantes como operandos
    [OpAA, 'CONSTANT', ['CONSTANT', OpAB]],
    [OpAB, 'PLUS', ['PLUS', OpAA]],                         # Operación aritmética
    [OpAB, 'TIMES', ['TIMES', OpAA]],
    [OpAB, 'SEMICOLON', ['vacia']],                         # Fin de expresión
    [OpAB, 'LPAREN', ['LPAREN', SPar, 'RPAREN']],   # Llamada a función con argumentos
    [OpAB, 'vacia', ['vacia']],                     # Simple identificador
    [BlqAux, 'RBRACE', ['vacia']],                          # Fin del bloque
    [DvAsg, 'DATATYPE', ['DATATYPE', 'ID', 'ASSIGN', OpAA, 'SEMICOLON']],  # Asignación directa
    [Blq, 'DATATYPE', ['DvAsg', BlqAux]],  # Declaración y asignación
    [Blq, 'ID', ['OpAA', 'SEMICOLON', BlqAux]],  # Llamada a función como expresión
    [BlqAux, 'RBRACE', ['vacia']],  # Fin del bloque
    [SCont, 'RETURN', ['RETURN', 'expression', 'SEMICOLON']],
    [MS, 'RETURN', None],
    [MS, 'RETURN', ['RETURN', SCont]],  # 'RETURN' seguido por lo que quieras procesar en SCont
    [MS, 'IF', [SIf]],  # Agrega una regla para 'if'
    [MS, 'ELSE', [Else]],  # Agrega una regla para 'else'
    [MS, 'ID', [IdType]],  # Para identificar un ID

    # Fin del bloque
    [SCont, 'ID', [Body, BodyAux]],
    [SCont, 'LBRACE', None],
    [SCont, 'RBRACE', None],
    [SCont, 'NOTEQUALS', None],
    [SCont, 'LESS', None],
    [SCont, 'GREATER', None],
    [SCont, 'AND', None],
    [SCont, 'OR', None],
    [SCont, 'IF', None],
    [SCont, 'ELSE', None],
    [SCont, 'WHILE', None],
    [SCont, 'eof', None],
    [Body, 'INCLUDE', None],
    [Body, 'LPAREN', None],
    [Body, 'RPAREN', None],
    [Body, 'TIMES', None],
    [Body, 'PLUS', None],
    [Body, 'MINUS', None],
    [Body, 'DIVIDE', None],
    [Body, 'COMMA', None],
    [Body, 'SEMICOLON', None],
    [Body, 'ASSIGNMENT', None],
    [Body, 'CONSTANT', None],
    [Body, 'DATATYPE', [IdType]],
    [Body, 'ID', [SAsig]],
    [Body, 'LBRACE', None],
    [Body, 'RBRACE', None],
    [Body, 'NOTEQUALS', None],
    [Body, 'LESS', None],
    [Body, 'GREATER', None],
    [Body, 'AND', None],
    [Body, 'OR', None],
    [Body, 'IF', None],
    [Body, 'ELSE', None],
    [Body, 'WHILE', None],
    [Body, 'eof', None],
    [IdType, 'INCLUDE', None],
    [IdType, 'LPAREN', None],
    [IdType, 'RPAREN', None],
    [IdType, 'TIMES', None],
    [IdType, 'PLUS', None],
    [IdType, 'MINUS', None],
    [IdType, 'DIVIDE', None],
    [IdType, 'COMMA', None],
    [IdType, 'SEMICOLON', None],
    [IdType, 'ASSIGNMENT', None],
    [IdType, 'CONSTANT', None],
    [IdType, 'DATATYPE', ['DATATYPE','ID',IdTypeBody]],
    [IdType, 'ID', None],
    [IdType, 'LBRACE', None],
    [IdType, 'RBRACE', None],
    [IdType, 'NOTEQUALS', None],
    [IdType, 'LESS', None],
    [IdType, 'GREATER', None],
    [IdType, 'AND', None],
    [IdType, 'OR', None],
    [IdType, 'IF', None],
    [IdType, 'ELSE', None],
    [IdType, 'WHILE', None],
    [IdType, 'eof', None],
    [IdTypeBody, 'INCLUDE', None],
    [IdTypeBody, 'LPAREN', [IdTypeBodyFnc]],
    [IdTypeBody, 'RPAREN', None],
    [IdTypeBody, 'TIMES', None],
    [IdTypeBody, 'PLUS', None],
    [IdTypeBody, 'MINUS', None],
    [IdTypeBody, 'DIVIDE', None],
    [IdTypeBody, 'COMMA', [IdTypeBodyVar]],
    [IdTypeBody, 'SEMICOLON', [IdTypeBodyVar]],
    [IdTypeBody, 'ASSIGNMENT', [IdTypeBodyVar]],
    [IdTypeBody, 'CONSTANT', None],
    [IdTypeBody, 'DATATYPE', [IdTypeBodyVar]],
    [IdTypeBody, 'ID', None],
    [IdTypeBody, 'LBRACE', None],
    [IdTypeBody, 'RBRACE', None],
    [IdTypeBody, 'NOTEQUALS', None],
    [IdTypeBody, 'LESS', None],
    [IdTypeBody, 'GREATER', None],
    [IdTypeBody, 'AND', None],
    [IdTypeBody, 'OR', None],
    [IdTypeBody, 'IF', None],
    [IdTypeBody, 'ELSE', None],
    [IdTypeBody, 'WHILE', None],
    [IdTypeBody, 'eof', [IdTypeBodyVar]],
    [IdTypeBodyFnc, 'INCLUDE', None],
    [IdTypeBodyFnc, 'LPAREN', ['LPAREN',SPar,'RPAREN', FBody]],
    [IdTypeBodyFnc, 'RPAREN', None],
    [IdTypeBodyFnc, 'TIMES', None],
    [IdTypeBodyFnc, 'PLUS', None],
    [IdTypeBodyFnc, 'MINUS', None],
    [IdTypeBodyFnc, 'DIVIDE', None],
    [IdTypeBodyFnc, 'COMMA', None],
    [IdTypeBodyFnc, 'SEMICOLON', None],
    [IdTypeBodyFnc, 'ASSIGNMENT', None],
    [IdTypeBodyFnc, 'CONSTANT', None],
    [IdTypeBodyFnc, 'DATATYPE', None],
    [IdTypeBodyFnc, 'ID', None],
    [IdTypeBodyFnc, 'LBRACE', None],
    [IdTypeBodyFnc, 'RBRACE', None],
    [IdTypeBodyFnc, 'NOTEQUALS', None],
    [IdTypeBodyFnc, 'LESS', None],
    [IdTypeBodyFnc, 'GREATER', None],
    [IdTypeBodyFnc, 'AND', None],
    [IdTypeBodyFnc, 'OR', None],
    [IdTypeBodyFnc, 'IF', None],
    [IdTypeBodyFnc, 'ELSE', None],
    [IdTypeBodyFnc, 'WHILE', None],
    [IdTypeBodyFnc, 'eof', None],
    [IdTypeBodyVar, 'INCLUDE', None],
    [IdTypeBodyVar, 'LPAREN', None],
    [IdTypeBodyVar, 'RPAREN', None],
    [IdTypeBodyVar, 'TIMES', None],
    [IdTypeBodyVar, 'PLUS', None],
    [IdTypeBodyVar, 'MINUS', None],
    [IdTypeBodyVar, 'DIVIDE', None],
    [IdTypeBodyVar, 'COMMA', [DvAsg, DvOtr]],
    [IdTypeBodyVar, 'SEMICOLON', [DvAsg, DvOtr]],
    [IdTypeBodyVar, 'ASSIGNMENT', [DvAsg, DvOtr]],
    [IdTypeBodyVar, 'CONSTANT', None],
    [IdTypeBodyVar, 'DATATYPE', [DvAsg, DvOtr]],
    [IdTypeBodyVar, 'ID', None],
    [IdTypeBodyVar, 'LBRACE', None],
    [IdTypeBodyVar, 'RBRACE', [DvAsg, DvOtr]],
    [IdTypeBodyVar, 'NOTEQUALS', None],
    [IdTypeBodyVar, 'LESS', None],
    [IdTypeBodyVar, 'GREATER', None],
    [IdTypeBodyVar, 'AND', None],
    [IdTypeBodyVar, 'OR', None],
    [IdTypeBodyVar, 'IF', [DvAsg, DvOtr]],
    [IdTypeBodyVar, 'ELSE', None],
    [IdTypeBodyVar, 'WHILE', [DvAsg, DvOtr]],
    [IdTypeBodyVar, 'eof', [DvAsg, DvOtr]],
    [DvAsg, 'INCLUDE', None],
    [DvAsg, 'LPAREN', None],
    [DvAsg, 'RPAREN', None],
    [DvAsg, 'TIMES', None],
    [DvAsg, 'PLUS', None],
    [DvAsg, 'MINUS', None],
    [DvAsg, 'DIVIDE', None],
    [DvAsg, 'COMMA', ['vacia']],
    [DvAsg, 'SEMICOLON', ['vacia']],
    [DvAsg, 'ASSIGNMENT', ['ASSIGNMENT',DvVal]],
    [DvAsg, 'CONSTANT', None],
    [DvAsg, 'DATATYPE', ['vacia']],
    [DvAsg, 'ID', None],
    [DvAsg, 'LBRACE', None],
    [DvAsg, 'RBRACE', ['vacia']],
    [DvAsg, 'NOTEQUALS', None],
    [DvAsg, 'LESS', None],
    [DvAsg, 'GREATER', None],
    [DvAsg, 'AND', None],
    [DvAsg, 'OR', None],
    [DvAsg, 'IF', ['vacia']],
    [DvAsg, 'ELSE', None],
    [DvAsg, 'WHILE', ['vacia']],
    [DvAsg, 'eof', ['vacia']],
    [DvVal, 'INCLUDE', None],
    [DvVal, 'LPAREN', None],
    [DvVal, 'RPAREN', None],
    [DvVal, 'TIMES', None],
    [DvVal, 'PLUS', None],
    [DvVal, 'MINUS', None],
    [DvVal, 'DIVIDE', None],
    [DvVal, 'COMMA', None],
    [DvVal, 'SEMICOLON', None],
    [DvVal, 'ASSIGNMENT', None],
    [DvVal, 'CONSTANT', ['CONSTANT']],
    [DvVal, 'DATATYPE', None],
    [DvVal, 'ID', ['ID']],
    [DvVal, 'LBRACE', None],
    [DvVal, 'RBRACE', None],
    [DvVal, 'NOTEQUALS', None],
    [DvVal, 'LESS', None],
    [DvVal, 'GREATER', None],
    [DvVal, 'AND', None],
    [DvVal, 'OR', None],
    [DvVal, 'IF', None],
    [DvVal, 'ELSE', None],
    [DvVal, 'WHILE', None],
    [DvVal, 'eof', None],
    [DvOtr, 'INCLUDE', None],
    [DvOtr, 'LPAREN', None],
    [DvOtr, 'RPAREN', None],
    [DvOtr, 'TIMES', None],
    [DvOtr, 'PLUS', None],
    [DvOtr, 'MINUS', None],
    [DvOtr, 'DIVIDE', None],
    [DvOtr, 'COMMA', ['COMMA', 'ID', IdTypeBodyVar]],
    [DvOtr, 'SEMICOLON', ['SEMICOLON']],
    [DvOtr, 'ASSIGNMENT', None],
    [DvOtr, 'CONSTANT', None],
    [DvOtr, 'DATATYPE', ['vacia']],
    [DvOtr, 'ID', None],
    [DvOtr, 'LBRACE', None],
    [DvOtr, 'RBRACE', ['vacia']],
    [DvOtr, 'NOTEQUALS', None],
    [DvOtr, 'LESS', None],
    [DvOtr, 'GREATER', None],
    [DvOtr, 'AND', None],
    [DvOtr, 'OR', None],
    [DvOtr, 'IF', ['vacia']],
    [DvOtr, 'ELSE', None],
    [DvOtr, 'WHILE', ['vacia']],
    [DvOtr, 'eof', ['vacia']],
    [BodyAux, 'INCLUDE', None],
    [BodyAux, 'LPAREN', None],
    [BodyAux, 'RPAREN', None],
    [BodyAux, 'TIMES', None],
    [BodyAux, 'PLUS', None],
    [BodyAux, 'MINUS', None],
    [BodyAux, 'DIVIDE', None],
    [BodyAux, 'COMMA', None],
    [BodyAux, 'SEMICOLON', None],
    [BodyAux, 'ASSIGNMENT', None],
    [BodyAux, 'CONSTANT', None],
    [BodyAux, 'DATATYPE', [SCont]],
    [BodyAux, 'ID', [SCont]],
    [BodyAux, 'LBRACE', None],
    [BodyAux, 'RBRACE', None],
    [BodyAux, 'NOTEQUALS', None],
    [BodyAux, 'LESS', None],
    [BodyAux, 'GREATER', None],
    [BodyAux, 'AND', None],
    [BodyAux, 'OR', None],
    [BodyAux, 'IF', None],
    [BodyAux, 'ELSE', None],
    [BodyAux, 'WHILE', None],
    [BodyAux, 'eof', ['vacia']],
    [SBlq, 'INCLUDE', None],
    [SBlq, 'LPAREN', None],
    [SBlq, 'RPAREN', None],
    [SBlq, 'TIMES', None],
    [SBlq, 'PLUS', None],
    [SBlq, 'MINUS', None],
    [SBlq, 'DIVIDE', None],
    [SBlq, 'COMMA', None],
    [SBlq, 'SEMICOLON', None],
    [SBlq, 'ASSIGNMENT', None],
    [SBlq, 'CONSTANT', None],
    [SBlq, 'DATATYPE', None],
    [SBlq, 'ID', None],
    [SBlq, 'LBRACE', ['LBRACE', Blq, 'RBRACE']],
    [SBlq, 'RBRACE', None],
    [SBlq, 'NOTEQUALS', None],
    [SBlq, 'LESS', None],
    [SBlq, 'GREATER', None],
    [SBlq, 'AND', None],
    [SBlq, 'OR', None],
    [SBlq, 'IF', None],
    [SBlq, 'ELSE', None],
    [SBlq, 'WHILE', None],
    [SBlq, 'eof', None],
    [Blq, 'INCLUDE', None],
    [Blq, 'LPAREN', None],
    [Blq, 'RPAREN', None],
    [Blq, 'TIMES', None],
    [Blq, 'PLUS', None],
    [Blq, 'MINUS', None],
    [Blq, 'DIVIDE', None],
    [Blq, 'COMMA', None],
    [Blq, 'SEMICOLON', None],
    [Blq, 'ASSIGNMENT', None],
    [Blq, 'CONSTANT', None],
    [Blq, 'DATATYPE', [ContBlq, BlqAux]],
    [Blq, 'ID', [SAsig]],
    [Blq, 'LBRACE', None],
    [Blq, 'RBRACE', None],
    [Blq, 'NOTEQUALS', None],
    [Blq, 'LESS', None],
    [Blq, 'GREATER', None],
    [Blq, 'AND', None],
    [Blq, 'OR', None],
    [Blq, 'IF', [ContBlq, BlqAux]],
    [Blq, 'ELSE', None],
    [Blq, 'WHILE', [ContBlq, BlqAux]],
    [Blq, 'eof', None],
    [ContBlq, 'INCLUDE', None],
    [ContBlq, 'LPAREN', None],
    [ContBlq, 'RPAREN', None],
    [ContBlq, 'TIMES', None],
    [ContBlq, 'PLUS', None],
    [ContBlq, 'MINUS', None],
    [ContBlq, 'DIVIDE', None],
    [ContBlq, 'COMMA', None],
    [ContBlq, 'SEMICOLON', None],
    [ContBlq, 'ASSIGNMENT', None],
    [ContBlq, 'CONSTANT', None],
    [ContBlq, 'DATATYPE', [DvS]],
    [ContBlq, 'ID', None],
    [ContBlq, 'LBRACE', None],
    [ContBlq, 'RBRACE', None],
    [ContBlq, 'NOTEQUALS', None],
    [ContBlq, 'LESS', None],
    [ContBlq, 'GREATER', None],
    [ContBlq, 'AND', None],
    [ContBlq, 'OR', None],
    [ContBlq, 'IF', [SIf]],
    [ContBlq, 'ELSE', None],
    [ContBlq, 'WHILE', [SWhl]],
    [ContBlq, 'eof', None],
    [DvS, 'INCLUDE', None],
    [DvS, 'LPAREN', None],
    [DvS, 'RPAREN', None],
    [DvS, 'TIMES', None],
    [DvS, 'PLUS', None],
    [DvS, 'MINUS', None],
    [DvS, 'DIVIDE', None],
    [DvS, 'COMMA', None],
    [DvS, 'SEMICOLON', None],
    [DvS, 'ASSIGNMENT', None],
    [DvS, 'CONSTANT', None],
    [DvS, 'DATATYPE', ['DATATYPE', 'ID', IdTypeBodyVar]],
    [DvS, 'ID', None],
    [DvS, 'LBRACE', None],
    [DvS, 'RBRACE', None],
    [DvS, 'NOTEQUALS', None],
    [DvS, 'LESS', None],
    [DvS, 'GREATER', None],
    [DvS, 'AND', None],
    [DvS, 'OR', None],
    [DvS, 'IF', None],
    [DvS, 'ELSE', None],
    [DvS, 'WHILE', None],
    [DvS, 'eof', None],
    [BlqAux, 'INCLUDE', None],
    [BlqAux, 'LPAREN', None],
    [BlqAux, 'RPAREN', None],
    [BlqAux, 'TIMES', None],
    [BlqAux, 'PLUS', None],
    [BlqAux, 'MINUS', None],
    [BlqAux, 'DIVIDE', None],
    [BlqAux, 'COMMA', None],
    [BlqAux, 'SEMICOLON', None],
    [BlqAux, 'ASSIGNMENT', None],
    [BlqAux, 'CONSTANT', None],
    [BlqAux, 'DATATYPE', [Blq]],
    [BlqAux, 'ID', None],
    [BlqAux, 'LBRACE', None],
    [BlqAux, 'RBRACE', ['vacia']],
    [BlqAux, 'NOTEQUALS', None],
    [BlqAux, 'LESS', None],
    [BlqAux, 'GREATER', None],
    [BlqAux, 'AND', None],
    [BlqAux, 'OR', None],
    [BlqAux, 'IF', [Blq]],
    [BlqAux, 'ELSE', None],
    [BlqAux, 'WHILE', [Blq]],
    [BlqAux, 'eof', None],
    [SPar, 'INCLUDE', None],
    [SPar, 'LPAREN', None],
    [SPar, 'RPAREN', ['vacia']],
    [SPar, 'TIMES', None],
    [SPar, 'PLUS', None],
    [SPar, 'MINUS', None],
    [SPar, 'DIVIDE', None],
    [SPar, 'COMMA', None],
    [SPar, 'SEMICOLON', None],
    [SPar, 'ASSIGNMENT', None],
    [SPar, 'CONSTANT', None],
    [SPar, 'DATATYPE', [ParAux]],
    [SPar, 'ID', None],
    [SPar, 'LBRACE', None],
    [SPar, 'RBRACE', None],
    [SPar, 'NOTEQUALS', None],
    [SPar, 'LESS', None],
    [SPar, 'GREATER', None],
    [SPar, 'AND', None],
    [SPar, 'OR', None],
    [SPar, 'IF', None],
    [SPar, 'ELSE', None],
    [SPar, 'WHILE', None],
    [SPar, 'eof', None],
    [ParAux, 'INCLUDE', None],
    [ParAux, 'LPAREN', None],
    [ParAux, 'RPAREN', None],
    [ParAux, 'TIMES', None],
    [ParAux, 'PLUS', None],
    [ParAux, 'MINUS', None],
    [ParAux, 'DIVIDE', None],
    [ParAux, 'COMMA', None],
    [ParAux, 'SEMICOLON', None],
    [ParAux, 'ASSIGNMENT', None],
    [ParAux, 'CONSTANT', None],
    [ParAux, 'DATATYPE', ['DATATYPE', 'ID', ParOtr]],
    [ParAux, 'ID', None],
    [ParAux, 'LBRACE', None],
    [ParAux, 'RBRACE', None],
    [ParAux, 'NOTEQUALS', None],
    [ParAux, 'LESS', None],
    [ParAux, 'GREATER', None],
    [ParAux, 'AND', None],
    [ParAux, 'OR', None],
    [ParAux, 'IF', None],
    [ParAux, 'ELSE', None],
    [ParAux, 'WHILE', None],
    [ParAux, 'eof', None],
    [ParOtr, 'INCLUDE', None],
    [ParOtr, 'LPAREN', None],
    [ParOtr, 'RPAREN', ['vacia']],
    [ParOtr, 'TIMES', None],
    [ParOtr, 'PLUS', None],
    [ParOtr, 'MINUS', None],
    [ParOtr, 'DIVIDE', None],
    [ParOtr, 'COMMA', ['COMMA', ParAux]],
    [ParOtr, 'SEMICOLON', None],
    [ParOtr, 'ASSIGNMENT', None],
    [ParOtr, 'CONSTANT', None],
    [ParOtr, 'DATATYPE', None],
    [ParOtr, 'ID', None],
    [ParOtr, 'LBRACE', None],
    [ParOtr, 'RBRACE', None],
    [ParOtr, 'NOTEQUALS', None],
    [ParOtr, 'LESS', None],
    [ParOtr, 'GREATER', None],
    [ParOtr, 'AND', None],
    [ParOtr, 'OR', None],
    [ParOtr, 'IF', None],
    [ParOtr, 'ELSE', None],
    [ParOtr, 'WHILE', None],
    [ParOtr, 'eof', None],
    [FBody, 'INCLUDE', None],
    [FBody, 'LPAREN', None],
    [FBody, 'RPAREN', None],
    [FBody, 'TIMES', None],
    [FBody, 'PLUS', None],
    [FBody, 'MINUS', None],
    [FBody, 'DIVIDE', None],
    [FBody, 'COMMA', None],
    [FBody, 'SEMICOLON', ['SEMICOLON']],
    [FBody, 'ASSIGNMENT', None],
    [FBody, 'CONSTANT', None],
    [FBody, 'DATATYPE', None],
    [FBody, 'ID', None],
    [FBody, 'LBRACE', [SBlq]],
    [FBody, 'RBRACE', None],
    [FBody, 'NOTEQUALS', None],
    [FBody, 'LESS', None],
    [FBody, 'GREATER', None],
    [FBody, 'AND', None],
    [FBody, 'OR', None],
    [FBody, 'IF', None],
    [FBody, 'ELSE', None],
    [FBody, 'WHILE', None],
    [FBody, 'eof', None],
    [SAsig, 'INCLUDE', None],
    [SAsig, 'LPAREN', None],
    [SAsig, 'RPAREN', None],
    [SAsig, 'TIMES', None],
    [SAsig, 'PLUS', None],
    [SAsig, 'MINUS', None],
    [SAsig, 'DIVIDE', None],
    [SAsig, 'COMMA', None],
    [SAsig, 'SEMICOLON', None],
    [SAsig, 'ASSIGNMENT', None],
    [SAsig, 'CONSTANT', None],
    [SAsig, 'DATATYPE', None],
    [SAsig, 'ID', ['ID', 'ASSIGNMENT', OpAA, 'SEMICOLON']],
    [SAsig, 'LBRACE', None],
    [SAsig, 'RBRACE', None],
    [SAsig, 'NOTEQUALS', None],
    [SAsig, 'LESS', None],
    [SAsig, 'GREATER', None],
    [SAsig, 'AND', None],
    [SAsig, 'OR', None],
    [SAsig, 'IF', None],
    [SAsig, 'ELSE', None],
    [SAsig, 'WHILE', None],
    [SAsig, 'eof', None],
    [OpAA, 'INCLUDE', None],
    [OpAA, 'LPAREN', ['LPAREN', OpAA, 'RPAREN', OpAA1]],
    [OpAA, 'RPAREN', None],
    [OpAA, 'TIMES', None],
    [OpAA, 'PLUS', None],
    [OpAA, 'MINUS', None],
    [OpAA, 'DIVIDE', None],
    [OpAA, 'COMMA', None],
    [OpAA, 'SEMICOLON', None],
    [OpAA, 'ASSIGNMENT', None],
    [OpAA, 'CONSTANT', [OpAB, OpAA2]],
    [OpAA, 'DATATYPE', None],
    [OpAA, 'ID', [OpAB, OpAA2]],
    [OpAA, 'LBRACE', None],
    [OpAA, 'RBRACE', None],
    [OpAA, 'NOTEQUALS', None],
    [OpAA, 'LESS', None],
    [OpAA, 'GREATER', None],
    [OpAA, 'AND', None],
    [OpAA, 'OR', None],
    [OpAA, 'IF', None],
    [OpAA, 'ELSE', None],
    [OpAA, 'WHILE', None],
    [OpAA, 'eof', None],
    [OpAB, 'INCLUDE', None],
    [OpAB, 'LPAREN', ['LPAREN', OpAA, 'RPAREN', OpAA1]],
    [OpAB, 'RPAREN', None],
    [OpAB, 'TIMES', None],
    [OpAB, 'PLUS', None],
    [OpAB, 'MINUS', None],
    [OpAB, 'DIVIDE', None],
    [OpAB, 'COMMA', None],
    [OpAB, 'SEMICOLON', None],
    [OpAB, 'ASSIGNMENT', None],
    [OpAB, 'CONSTANT', ['CONSTANT']],
    [OpAB, 'DATATYPE', None],
    [OpAB, 'ID', ['ID']],
    [OpAB, 'LBRACE', None],
    [OpAB, 'RBRACE', None],
    [OpAB, 'NOTEQUALS', None],
    [OpAB, 'LESS', None],
    [OpAB, 'GREATER', None],
    [OpAB, 'AND', None],
    [OpAB, 'OR', None],
    [OpAB, 'IF', None],
    [OpAB, 'ELSE', None],
    [OpAB, 'WHILE', None],
    [OpAB, 'eof', None],
    [OpAA2, 'INCLUDE', None],
    [OpAA2, 'LPAREN', None],
    [OpAA2, 'RPAREN', ['vacia']],
    [OpAA2, 'TIMES', [Opr, OpAB, OpAA1]],
    [OpAA2, 'PLUS', [Opr, OpAB, OpAA1]],
    [OpAA2, 'MINUS', [Opr, OpAB, OpAA1]],
    [OpAA2, 'DIVIDE', [Opr, OpAB, OpAA1]],
    [OpAA2, 'COMMA', None],
    [OpAA2, 'SEMICOLON', ['vacia']],
    [OpAA2, 'ASSIGNMENT', None],
    [OpAA2, 'CONSTANT', None],
    [OpAA2, 'DATATYPE', None],
    [OpAA2, 'ID', None],
    [OpAA2, 'LBRACE', None],
    [OpAA2, 'RBRACE', None],
    [OpAA2, 'NOTEQUALS', None],
    [OpAA2, 'LESS', None],
    [OpAA2, 'GREATER', None],
    [OpAA2, 'AND', None],
    [OpAA2, 'OR', None],
    [OpAA2, 'IF', None],
    [OpAA2, 'ELSE', None],
    [OpAA2, 'WHILE', None],
    [OpAA2, 'eof', None],
    [Opr, 'INCLUDE', None],
    [Opr, 'LPAREN', None],
    [Opr, 'RPAREN', None],
    [Opr, 'TIMES', ['TIMES']],
    [Opr, 'PLUS', ['PLUS']],
    [Opr, 'MINUS', ['MINUS']],
    [Opr, 'DIVIDE', ['DIVIDE']],
    [Opr, 'COMMA', None],
    [Opr, 'SEMICOLON', None],
    [Opr, 'ASSIGNMENT', None],
    [Opr, 'CONSTANT', None],
    [Opr, 'DATATYPE', None],
    [Opr, 'ID', None],
    [Opr, 'LBRACE', None],
    [Opr, 'RBRACE', None],
    [Opr, 'NOTEQUALS', None],
    [Opr, 'LESS', None],
    [Opr, 'GREATER', None],
    [Opr, 'AND', None],
    [Opr, 'OR', None],
    [Opr, 'IF', None],
    [Opr, 'ELSE', None],
    [Opr, 'WHILE', None],
    [Opr, 'eof', None],
    [OpAA1, 'INCLUDE', None],
    [OpAA1, 'LPAREN', None],
    [OpAA1, 'RPAREN', ['vacia']],
    [OpAA1, 'TIMES', [Opr, OpAA]],
    [OpAA1, 'PLUS', [Opr, OpAA]],
    [OpAA1, 'MINUS', [Opr, OpAA]],
    [OpAA1, 'DIVIDE', [Opr, OpAA]],
    [OpAA1, 'COMMA', None],
    [OpAA1, 'SEMICOLON', ['vacia']],
    [OpAA1, 'ASSIGNMENT', None],
    [OpAA1, 'CONSTANT', None],
    [OpAA1, 'DATATYPE', None],
    [OpAA1, 'ID', None],
    [OpAA1, 'LBRACE', None],
    [OpAA1, 'RBRACE', None],
    [OpAA1, 'NOTEQUALS', None],
    [OpAA1, 'LESS', None],
    [OpAA1, 'GREATER', None],
    [OpAA1, 'AND', None],
    [OpAA1, 'OR', None],
    [OpAA1, 'IF', None],
    [OpAA1, 'ELSE', None],
    [OpAA1, 'WHILE', None],
    [OpAA1, 'eof', None],
    [SCond, 'INCLUDE', None],
    [SCond, 'LPAREN', [Cond]],
    [SCond, 'RPAREN', None],
    [SCond, 'TIMES', None],
    [SCond, 'PLUS', None],
    [SCond, 'MINUS', None],
    [SCond, 'DIVIDE', None],
    [SCond, 'COMMA', None],
    [SCond, 'SEMICOLON', None],
    [SCond, 'ASSIGNMENT', None],
    [SCond, 'CONSTANT', [Cond]],
    [SCond, 'DATATYPE', None],
    [SCond, 'ID', [Cond]],
    [SCond, 'LBRACE', None],
    [SCond, 'RBRACE', None],
    [SCond, 'NOTEQUALS', None],
    [SCond, 'LESS', None],
    [SCond, 'GREATER', None],
    [SCond, 'AND', None],
    [SCond, 'OR', None],
    [SCond, 'IF', None],
    [SCond, 'ELSE', None],
    [SCond, 'WHILE', None],
    [SCond, 'eof', None],
    [Cond, 'INCLUDE', None],
    [Cond, 'LPAREN', ['LPAREN', Cond, 'RPAREN']],
    [Cond, 'RPAREN', ['vacia']],
    [Cond, 'TIMES', [Opr, OpAA]],
    [Cond, 'PLUS', [Opr, OpAA]],
    [Cond, 'MINUS', [Opr, OpAA]],
    [Cond, 'DIVIDE', [Opr, OpAA]],
    [Cond, 'COMMA', None],
    [Cond, 'SEMICOLON', ['vacia']],
    [Cond, 'ASSIGNMENT', None],
    [Cond, 'CONSTANT', [CondB, OpC, CondB, CondA]],
    [Cond, 'DATATYPE', None],
    [Cond, 'ID', [CondB, OpC, CondB, CondA]],
    [Cond, 'LBRACE', None],
    [Cond, 'RBRACE', None],
    [Cond, 'NOTEQUALS', None],
    [Cond, 'LESS', None],
    [Cond, 'GREATER', None],
    [Cond, 'AND', None],
    [Cond, 'OR', None],
    [Cond, 'IF', None],
    [Cond, 'ELSE', None],
    [Cond, 'WHILE', None],
    [Cond, 'eof', None],
    [CondB, 'INCLUDE', None],
    [CondB, 'LPAREN', None],
    [CondB, 'RPAREN', ['vacia']],
    [CondB, 'TIMES', None],
    [CondB, 'PLUS', None],
    [CondB, 'MINUS', None],
    [CondB, 'DIVIDE', None],
    [CondB, 'COMMA', None],
    [CondB, 'SEMICOLON', None],
    [CondB, 'ASSIGNMENT', None],
    [CondB, 'CONSTANT', ['CONSTANT']],
    [CondB, 'DATATYPE', None],
    [CondB, 'ID', ['ID']],
    [CondB, 'LBRACE', None],
    [CondB, 'RBRACE', None],
    [CondB, 'NOTEQUALS', None],
    [CondB, 'LESS', None],
    [CondB, 'GREATER', None],
    [CondB, 'AND', None],
    [CondB, 'OR', None],
    [CondB, 'IF', None],
    [CondB, 'ELSE', None],
    [CondB, 'WHILE', None],
    [CondB, 'eof', None],
    [OpC, 'INCLUDE', None],
    [OpC, 'LPAREN', None],
    [OpC, 'RPAREN', None],
    [OpC, 'TIMES', None],
    [OpC, 'PLUS', None],
    [OpC, 'MINUS', None],
    [OpC, 'DIVIDE', None],
    [OpC, 'COMMA', None],
    [OpC, 'SEMICOLON', None],
    [OpC, 'ASSIGNMENT', None],
    [OpC, 'CONSTANT', None],
    [OpC, 'DATATYPE', None],
    [OpC, 'ID', None],
    [OpC, 'LBRACE', None],
    [OpC, 'RBRACE', None],
    [OpC, 'EQUALS', ['EQUALS']],
    [OpC, 'NOTEQUALS', ['NOTEQUALS']],
    [OpC, 'LESS', ['LESS']],
    [OpC, 'GREATER', ['GREATER']],
    [OpC, 'AND', None],
    [OpC, 'OR', None],
    [OpC, 'IF', None],
    [OpC, 'ELSE', None],
    [OpC, 'WHILE', None],
    [OpC, 'eof', None],
    [CondA, 'INCLUDE', None],
    [CondA, 'LPAREN', None],
    [CondA, 'RPAREN', ['vacia']],
    [CondA, 'TIMES', None],
    [CondA, 'PLUS', None],
    [CondA, 'MINUS', None],
    [CondA, 'DIVIDE', None],
    [CondA, 'COMMA', None],
    [CondA, 'SEMICOLON', None],
    [CondA, 'ASSIGNMENT', None],
    [CondA, 'CONSTANT', None],
    [CondA, 'DATATYPE', None],
    [CondA, 'ID', None],
    [CondA, 'LBRACE', None],
    [CondA, 'RBRACE', None],
    [CondA, 'NOTEQUALS', None],
    [CondA, 'LESS', None],
    [CondA, 'GREATER', None],
    [CondA, 'AND', ['AND', Cond]],
    [CondA, 'OR', ['OR', Cond]],
    [CondA, 'IF', None],
    [CondA, 'ELSE', None],
    [CondA, 'WHILE', None],
    [CondA, 'eof', None],
    [SIf, 'INCLUDE', None],
    [SIf, 'LPAREN', None],
    [SIf, 'RPAREN', None],
    [SIf, 'TIMES', None],
    [SIf, 'PLUS', None],
    [SIf, 'MINUS', None],
    [SIf, 'DIVIDE', None],
    [SIf, 'COMMA', None],
    [SIf, 'SEMICOLON', None],
    [SIf, 'ASSIGNMENT', None],
    [SIf, 'CONSTANT', None],
    [SIf, 'DATATYPE', None],
    [SIf, 'ID', None],
    [SIf, 'LBRACE', None],
    [SIf, 'RBRACE', None],
    [SIf, 'NOTEQUALS', None],
    [SIf, 'LESS', None],
    [SIf, 'GREATER', None],
    [SIf, 'AND', None],
    [SIf, 'OR', None],
    [SIf, 'IF', ['IF', 'LPAREN', SCond, 'RPAREN', SBlq, Else]],
    [SIf, 'ELSE', None],
    [SIf, 'WHILE', None],
    [SIf, 'eof', None],
    [Else, 'INCLUDE', None],
    [Else, 'LPAREN', None],
    [Else, 'RPAREN', None],
    [Else, 'TIMES', None],
    [Else, 'PLUS', None],
    [Else, 'MINUS', None],
    [Else, 'DIVIDE', None],
    [Else, 'COMMA', None],
    [Else, 'SEMICOLON', None],
    [Else, 'ASSIGNMENT', None],
    [Else, 'CONSTANT', None],
    [Else, 'DATATYPE', ['vacia']],
    [Else, 'ID', ['vacia']],
    [Else, 'LBRACE', None],
    [Else, 'RBRACE', ['vacia']],
    [Else, 'NOTEQUALS', None],
    [Else, 'LESS', None],
    [Else, 'GREATER', None],
    [Else, 'AND', None],
    [Else, 'OR', None],
    [Else, 'IF', ['vacia']],
    [Else, 'ELSE', ['ELSE', Else2]],
    [Else, 'WHILE', ['vacia']],
    [Else, 'eof', None],
    [Else2, 'INCLUDE', None],
    [Else2, 'LPAREN', None],
    [Else2, 'RPAREN', None],
    [Else2, 'TIMES', None],
    [Else2, 'PLUS', None],
    [Else2, 'MINUS', None],
    [Else2, 'DIVIDE', None],
    [Else2, 'COMMA', None],
    [Else2, 'SEMICOLON', None],
    [Else2, 'ASSIGNMENT', None],
    [Else2, 'CONSTANT', None],
    [Else2, 'DATATYPE', None],
    [Else2, 'ID', None],
    [Else2, 'LBRACE', [SBlq]],
    [Else2, 'RBRACE', None],
    [Else2, 'NOTEQUALS', None],
    [Else2, 'LESS', None],
    [Else2, 'GREATER', None],
    [Else2, 'AND', None],
    [Else2, 'OR', None],
    [Else2, 'IF', [SIf]],
    [Else2, 'ELSE', None],
    [Else2, 'WHILE', None],
    [Else2, 'eof', None],
    [SWhl, 'INCLUDE', None],
    [SWhl, 'LPAREN', None],
    [SWhl, 'RPAREN', None],
    [SWhl, 'TIMES', None],
    [SWhl, 'PLUS', None],
    [SWhl, 'MINUS', None],
    [SWhl, 'DIVIDE', None],
    [SWhl, 'COMMA', None],
    [SWhl, 'SEMICOLON', None],
    [SWhl, 'ASSIGNMENT', None],
    [SWhl, 'CONSTANT', None],
    [SWhl, 'DATATYPE', None],
    [SWhl, 'ID', None],
    [SWhl, 'LBRACE', None],
    [SWhl, 'RBRACE', None],
    [SWhl, 'NOTEQUALS', None],
    [SWhl, 'LESS', None],
    [SWhl, 'GREATER', None],
    [SWhl, 'AND', None],
    [SWhl, 'OR', None],
    [SWhl, 'IF', None],
    [SWhl, 'ELSE', None],
    [SWhl, 'WHILE', ['WHILE', 'LPAREN', SCond, 'RPAREN', SBlq]],
    [SWhl, 'eof', None]
]