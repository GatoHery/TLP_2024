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

def verificar_inclusion_bool(codigo):
    if 'bool' in codigo and '#include <stdbool.h>' not in codigo:
        return False
    return True

def validate_type_compatibility(var_type, value_type):
    # Definir compatibilidades
    type_map = {
        "int": ["CONSTANT_INT"],
        "float": ["CONSTANT_FLOAT", "CONSTANT_INT"],  # Los enteros pueden convertirse en flotantes
        "char": ["CONSTANT_CHAR"],
        "string": ["CONSTANT_STRING"],
        "bool": ["CONSTANT_BOOL"],
    }
    
    # Verificar compatibilidad
    if var_type in type_map and value_type in type_map[var_type]:
        return True
    return False

def check_division_by_zero():
    global hasErrors
    for i in range(len(lineTokens) - 2):
        if lineTokens[i].type == "ID" and lineTokens[i + 1].type == "DIVIDE":
            if lineTokens[i + 2].type == "CONSTANT_INT" and lineTokens[i + 2].value == 0:
                print(f"Error: División por cero detectada en la línea {lineTokens[i].lineno}.")
                hasErrors += 1
            elif lineTokens[i + 2].type == "ID":
                divisor_name = lineTokens[i + 2].value
                if divisor_name in ids and ids[divisor_name].value == "0":
                    print(f"Error: División por cero detectada en la línea {lineTokens[i].lineno}.")
                    hasErrors += 1
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

    # Verificamos si se incluye la librería stdbool.h en caso de que se utilice bool
    if not verificar_inclusion_bool(completeCode):
        print("Error: Debe incluir la librería stdbool.h si se utiliza el tipo de dato bool.")
        return

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

def processLine():
    debug("******* Linea *********")
    debug(lineTokens)
    debug("******* ***** *********")
    pos = 0
    for tok in lineTokens:
        processToken(tok, pos)
        pos += 1
    check_division_by_zero()  
    debug("======= ===== =========")        

def processToken(tok, pos):
    global hasErrors
    if tok.type == "ID":
        idInstance = tokens.Identifier()
        if ids.get(tok.value) is not None:
            idInstance = ids[tok.value]
        else:
            idInstance.name = tok.value
            idInstance.scope = globalScope

        # Check if the token is part of a declaration
        is_declaration = False
        for i in range(pos - 1, -1, -1):
            if lineTokens[i].type == "DATATYPE":
                idInstance.dataType = lineTokens[i].value
                is_declaration = True
                break
            elif lineTokens[i].type == "ID" and lineTokens[i].value[0] == lineTokens[i].value[0].upper():
                idInstance.dataType = lineTokens[i].value
                is_declaration = True
                break

        if is_declaration:
            # Check for redeclaration in the same scope
            if idInstance.name in ids and ids[idInstance.name].scope == globalScope:
                print(f"Error: existe variable repetida '{idInstance.name}' en la misma función.")
                hasErrors += 1
            else:
                ids[idInstance.name] = idInstance
        else:
            # Handle variable usage
            if idInstance.name not in ids:
                print(f"Error: variable '{idInstance.name}' no declarada.")
                hasErrors += 1

        # Assign value if it's a declaration with an assignment
        value = ""
        if is_declaration and len(lineTokens) > (pos + 1) and lineTokens[pos + 1].type == "ASSIGN":
            for i in range(pos + 2, len(lineTokens)):
                if lineTokens[i].type in ["COMMA", "SEMICOLON", "RPAREN", "COLON"]:
                    break
                else:
                    value += str(lineTokens[i].value)

            # Validate type compatibility
            assigned_token = lineTokens[pos + 2]
            if not validate_type_compatibility(idInstance.dataType, assigned_token.type):
                print(f"Error: tipos incompatibles. No se puede asignar un valor de tipo '{assigned_token.type}' a una variable de tipo '{idInstance.dataType}'.")
                hasErrors += 1
            else:
                idInstance.value = value

        ids[idInstance.name] = idInstance

    # Check for division by zero
    check_division_by_zero()

def print_dictionary():
    for key in ids.values():
        print(key)

if __name__ == "__main__":
    main()