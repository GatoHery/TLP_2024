import rules

# Diccionarios de Terminales, No-Terminales y Producciones
terminales = dict()
noTerminales = dict()
producciones = dict()

# Clase Produccion
class Produccion:
    def __init__(self, key, noTerm, prod, len):
        self.key = key
        self.noTerm = noTerm
        self.prod = prod
        self.len = len
    def __str__(self) -> str:
         #Representación texto a consola de la produccion 
        return self.noTerm + " (" + self.key +") (" + str(self.len) + ")" # + str(self.prod)

def createLists():
    #Creamos la lista de Terminales y No-Terminales
    for element in rules.table:
        # Asignamos un valor inicial alto a los no-terminales.
        noTerminales[element[0]] = 9999999999
        terminales[element[1]] = 1
        if element[2] != None:
            len = 0
            if element[2] == ['vacia']:
                len = 0
            else:
                len = 9999999999
            key = element[0] + "->" + str(element[2])
            p = Produccion(key, element[0], element[2], len)
            # Añadimos la producción al diccionario de producciones.
            producciones[key] = p
    
    print("Terminales")
    print(terminales)
    print("NO Terminales")
    print(noTerminales)
    print()
    print("Producciones")
    for element in producciones.values():
        # Imprimimos cada producción utilizando su representación en texto.
        print(element)
