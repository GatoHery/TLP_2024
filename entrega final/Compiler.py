import sys
import rules
import tokens
import syntaxTree as st
import errors as err

debugMode = False
# Metodo para imprimir mensajes de debug
def debug(*messages):
    if debugMode:
        for m in messages:
            print(m)

ids = {}
globalScope = 0
lineTokens = []
syncTokens = ["COMMA", "SEMICOLON", "LBRACE", "RBRACE", "eof"]
tokToProcess = True
errorRecovery = False
hasErrors = 0

mainNode = st.MainNode("N", None, rules.MS)
stack = [st.crearNodo("N", None, "eof"), mainNode]
# Ingresamos el primer nodo, MAIN

debug(stack)

def main():
    if len(sys.argv) != 2 :
      print("Uso: python compiler.py <programa.c>")
      print("cmd entry:", sys.argv, len(sys.argv))
      return

    global errorRecovery
    global tokToProcess
    global hasErrors
    
    inputFile = sys.argv[1]
    f = open(inputFile,'r')
    tokens.lexer.input(f.read() + "\n$")
    f.seek(0)
    #almacena el código leido
    completeCode = f.read()
    print("Compilando", inputFile, "...")

    rulesNode=stack[-1] #primer elemento de izq a der
    tok=tokens.lexer.token() #lee el primer token
    debug(tok)
    debug(tok.type, tok.value, tok.lineno, tok.lexpos)
    while True:
        # Si se nos acabó el código fuente a analizar (ya no hay tokens)
        if not tok:
            break

        # Manejo de recuperación de errores, buscando un token de sincronización
        if errorRecovery and tok.type not in syncTokens:
            print(f"RECUPERACIÓN: Ignorando {tok.type}, {tok.value}")
            tok = tokens.lexer.token()
            continue
        else :
            #if errorRecovery == True:
                # Sincronizamos la pila hasta estar en el caracter de sincronizacion
                #while (rulesNode != tok.type):
                    #stack.pop()
            errorRecovery = False

        # Si llegamos al final del archivo y al final de la pila, hemos terminado
        # PASO: TERMINACIÓN
        if rulesNode.type == tok.type and rulesNode.type == 'eof':
            break
        else:
            # Si tenemos un símbolo TERMINAL y coincide con el token analizado
            # PASO: movimiento de SELECCIÓN
            if rulesNode.type == tok.type and rulesNode.type != 'eof':
                # Encontramos el terminal que coincide con el token que estabamos revisando (llegamos a la hoja)
                # Sacamos el símbolo de la pila (ya fue validado)
                stack.pop()
                # Obtenemos el siguiente
                rulesNode=stack[-1]
                # Leemos el siguiente token del programa para analizarlo
                tok=tokens.lexer.token()
                # Indicamos que hay un nuevo token leído para que sea incluído en el procesamiento por línea más abajo
                tokToProcess = True                
                debug(tok)
                debug(tok.type, tok.value, tok.lineno, tok.lexpos)
            # Encontramos un símbolo TERMINAL pero no coincide con el token analizado, tenemos
            # un error de sintaxis
            if  rulesNode.type in tokens.tokens and  rulesNode.type != tok.type:
                col = tokens.find_column(completeCode, tok)
                #print(inputFile, "(" + str(tok.lineno) + "," + str(col) + "): error: Se esperaba", rulesNode.type, "y se encontró ", tok.value)
                printError(inputFile, completeCode, rulesNode, tok, 1)
                if rulesNode.type == 'eof':
                    return 0
                errorRecovery = True
                hasErrors = hasErrors + 1
                stack.pop()
                rulesNode = stack[-1]
            else:
                if rulesNode.type not in tokens.tokens: # es NO-TERMINAL
                    debug("van entrar a la tabla:", rulesNode.type, tok.type)
                    # Buscamos en la tabla la celda (No Terminal - Terminal)
                    celda = buscar_en_tabla(rulesNode.type,tok.type)                      
                    # Si no la encontramos tenemos un error de sintaxis      
                    if  celda is None:
                        col = tokens.find_column(completeCode, tok)
                        #print(inputFile, "(" + str(tok.lineno) + "," + str(col) + "): error: No se esperaba encontrar", tok.value)
                        #print(completeCode[tok.lexpos - 10 : tok.lexpos + 10])
                        printError(inputFile, completeCode, rulesNode, tok, 2)

                        errorRecovery = True
                        hasErrors = hasErrors + 1
                        if tok.type == 'eof':
                            return 0
                        tok = tokens.lexer.token()
                    else:
                        # PASO: movimiento de PREDICCIÓN
                        # Si la encontramos sacamos la expresión de la pila e ingresamos su producción
                        stack.pop()
                        agregar_pila(rulesNode, celda, tok)
                        rulesNode = stack[-1]            
                        debug(stack, "------------")

        # debug(stack)

        # Construimos el arreglo de tokens de la linea actual
        if tokToProcess:
            global globalScope
            if tok.type == "LBRACE" :
                globalScope += 1
            if tok.type == "RBRACE" :
                globalScope -= 1
            addTokenToLine(tok)
            tokToProcess = False        


    if hasErrors == 0:
        print(inputFile, "compilado exitosamente.")

        print("")
        print("*****************************")
        print(">> Lista de IDs encontrados: ")
        print("*****************************")
        print(f'Nombre\t\t\tTipo\t\tValor\t\tNivel de Scope')
        print_dictionary()

        #Imprimamos el árbol sintáctico
        
      #Imprimamos el árbol sintáctico
        
        opcion = input("\n¿Desea ver el árbol sintáctico? (y/n): ").strip().lower()

        if opcion == 'y':
            print("\n*****************************")
            print(">> Árbol Sintáctico:")
            print("*****************************")
            st.walkTree(mainNode)

            #Se encuentra comentado el arbol resumido
            #st.podeTree(mainNode)
            #print("\n*****************************")
            #print(">> Árbol Sintáctico Resumido:")
            #print("*****************************")
            #st.walkTree(mainNode)
        else:
            print("\nCompilación finalizada.")

    else:
        print(f"Errores de compilación: {inputFile} tiene {hasErrors} error(es).") 
    
    
    # err.createLists()

def printError(inputFile, completeCode, rulesNode, tok, errorType):
    # Calculamos la columna donde se dio el error
    col = tokens.find_column(completeCode, tok)
    if errorType == 1 :
        print(inputFile, "(" + str(tok.lineno) + "," + str(col) + "): error: Se esperaba", rulesNode.type, "y se encontró ", tok.value)
    else :
        print(inputFile, "(" + str(tok.lineno) + "," + str(col) + "): error: No se esperaba encontrar", tok.value)
    
    # Obtenemos la línea de código donde se dio
    posIni = tok.lexpos
    posFin = tok.lexpos - 1
    while (posIni > 0 and posIni < len(completeCode) and completeCode[posIni] != '\n'):
        posIni = posIni - 1
    while (posFin > 0 and posFin < len(completeCode) and completeCode[posFin] != '\n'):
        posFin = posFin + 1
    posMark = tok.lexpos - posIni - 2
    print(completeCode[posIni + 1 : posFin])
    print(" " * posMark + "^^^")

def addTokenToLine(tok):
    print(f"Procesando token: {tok.type}, valor: {tok.value}")
    if tok.type == "LBRACE" or tok.type == "RBRACE" or tok.type == "SEMICOLON":
        # Hacemos el análisis de la línea y limpiamos el arreglo
        processLine()
        lineTokens.clear()
    else:
        lineTokens.append(tok)


def buscar_en_tabla(no_terminal, terminal):
    print(f"Buscando en tabla: No-terminal={no_terminal}, Terminal={terminal}")
    for i in range(len(rules.table)):
        if rules.table[i][0] == no_terminal and rules.table[i][1] == terminal:
            print(f"Match encontrado: {rules.table[i]}")
            return rules.table[i][2]
    print("No match found.")
    return None

def agregar_pila(parentNode, produccion, token):
    for elemento in reversed(produccion):
        if elemento != 'vacia': #la vacía no la inserta
            # Creamos el elemento (objeto) correspondiente
            # print("Creando nodo:", elemento)
            if (elemento in tokens.tokens):
                nodo = st.crearNodo("T", parentNode, elemento)
                nodo.value = token.value
                stack.append(nodo)
            else:
                stack.append(st.crearNodo("N", parentNode, elemento))

def processLine() :
    debug("******* Linea *********")
    debug(lineTokens)
    debug("******* ***** *********")
    pos = 0
    for tok in lineTokens :
        processToken(tok, pos)
        pos += 1
    debug("======= ===== =========")
        
def processToken(tok, pos) :
    if tok.type == "ID" :
        idInstance = tokens.Identifier()
        if ids.get(tok.value) != None :
            idInstance = ids[tok.value]
        else :
            idInstance.name = tok.value
            idInstance.scope = globalScope

        # Buscamos el tipo de dato
        for i in range(pos - 1, -1, -1) :
            if lineTokens[i].type == "DATATYPE" :
                idInstance.dataType = lineTokens[i].value
            else : 
                if lineTokens[i].type == "ID" and lineTokens[i].value[0] == lineTokens[i].value[0].upper() :
                    idInstance.dataType = lineTokens[i].value

        # Buscamos el valor
        value = ""
        debug(pos+1, len(lineTokens))
        if len(lineTokens) > (pos+1) and lineTokens[pos + 1].type == "ASSIGNMENT" :
            for i in range(pos + 2, len(lineTokens)) :
                debug(i, lineTokens[i])
                if lineTokens[i].type in ["COMMA", "SEMICOLON", "RPAREN", "COLON"] :
                    break
                else :
                    value += str(lineTokens[i].value)
            idInstance.value = value

        ids[idInstance.name] = idInstance

def print_dictionary():
    for key in ids.values():
        print(key)

if __name__ == "__main__":
    main()