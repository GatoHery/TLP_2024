import rules
import copy

# Clase Nodo del Arbol de Sintaxis Abstracta abreviado como AST
class ASTNode:
    def __init__(self, symbol, parent, type, value = "", body = []):
        self.type = type
        self.body = body
        self.parent = parent
        self.symbol = symbol
        self.value = value
    def __str__(self):
        return self.type
    def __repr__(self):
        return f"{self.type}"

def crearNodo(symbol, parentNode, tipoNodo):
    #Crea el nodo en el arbol de sintaxis abstracta
    if tipoNodo == rules.SLib:
        nodo = LibsNode(symbol, parentNode, tipoNodo, "","", [])
    elif tipoNodo == rules.SIf:
        nodo = IfStatementNode(symbol, parentNode, tipoNodo, "", [])
    else:
        nodo = ASTNode(symbol, parentNode, tipoNodo, "", [])
    if (parentNode != None and tipoNodo != 'vacia'):
        # Si hay un nodo padre y el nodo no es vacío, lo añadimos como hijo del padre.
        parentNode.body.append(nodo)
    return nodo
    
class MainNode(ASTNode):
    def __init__(self, symbol, parent, type, value = "", body = []):
        self.parent = parent
        self.type = type
        self.body = body
        self.symbol = symbol
        self.value = value

class LibsNode(ASTNode):
    def __init__(self, symbol, parent, type, name = "", value = "", body = []):
        # Nodo que representa una biblioteca o librería.
        self.parent = parent
        self.type = type
        self.name = name
        self.body = body
        self.symbol = symbol
        self.value = value

class FunctionNode(ASTNode):
    def __init__(self, type, name = "", parameters = [], body = []):
        self.type = type
        self.name = name
        self.parameters = parameters
        self.body = body

class VariableDeclarationNode(ASTNode):
    def __init__(self, type, var_type, var_name):
        self.type = type
        self.var_type = var_type
        self.var_name = var_name

class AssignmentNode(ASTNode):
    def __init__(self, type, variable, expression):
        self.type = type
        self.variable = variable
        self.expression = expression

class IfStatementNode(ASTNode):
    def setCondition(self, condition):
        self.condition = condition

class WhileLoopNode(ASTNode):
    def __init__(self, type, condition, body):
        self.type = type
        self.condition = condition
        self.body = body

def walkTree(node, level = 0):
    # print (str(level) + "-" + "  " * level + str(node) + " (" + str(node.parent) + ") ")
    print(str(level) + "-" + "  " * level + str(node) +  (" (" + str(node.value) + ")" if node.symbol == "T" else "") + " [" + str(node.symbol) + "]")
    # print ("  -> hijos:" + str(len(node.body)))
    if (node.body != None and node.body != []):
        for element in reversed(node.body):
            walkTree(element, level+1)


# Elimina nodos vacíos y simplificando estructuras.
def podeTree(node):
    if (node.body != None and node.body != []):
        # print("Recorremos los hijos de " + node.type)
        for element in reversed(node.body):
            # if (node.type == "SCont"):
                # print(" hijo SCont:" + element.type)
            podeTree(element)

    if ((node.symbol == "N" or node.type == "SEMICOLON") and node.body == []):
        # print("Borremos NO terminal vacio " + node.type)
        cont = 0
        for element in node.parent.body:
            if (element is node):
                del node.parent.body[cont]
            cont = cont + 1

    if (node.parent != None and node.parent.type == node.type):
        childNodes = copy.deepcopy(node.body)
        for element in childNodes:
            element.parent = node.parent
            node.parent.body.append(element)
        cont = 0
        for element in node.parent.body:
            if (element is node):
                del node.parent.body[cont]
            cont = cont + 1
