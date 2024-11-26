#validaciones logicas
import re

count = 0
debug = False

# Diccionarios para almacenar las variables y funciones
variables = {}
funciones = {}

def analizar_codigo(codigo):
    # Definir patrones de expresión regular para analizar el código
    patron_funcion = r'^\s*(?:\w+\s+)?(\w+)\s*\(([^)]*)\)\s*\{'
    patron_prototipo = r'(\w+)\s+(\w+)\s*\((.*?)\)\s*;'
    patron_variable_linea = r'(?:(\w+)\s+)?(\w+)(?:\s*=\s*([^;]+))?\s*;'
    patron_variable_multilinea = r'(\w+)\s+(\w+)\s*;\s*'
    patron_if = r'if\s*\((.*?)\)\s*{?'
    patron_for = r'for\s*\((.*?);(.*?);(.*?)\)\s*{'
    patron_while = r'while\s*\((.*?)\)\s*{'
    patron_include = r'#include\s*<(.+?)>'
    patron_fin = r'}'
    patron_return = r'\s*return\s+(.*);'

    # Buscar coincidencias en el código
    coincidencias_funcion = re.match(patron_funcion, codigo)
    coincidencias_prototipo = re.match(patron_prototipo, codigo)
    coincidencias_variable_linea = re.match(patron_variable_linea, codigo)
    coincidencias_variable_multilinea = re.match(patron_variable_multilinea, codigo)
    coincidencias_if = re.match(patron_if, codigo)
    coincidencias_for = re.match(patron_for, codigo)
    coincidencias_while = re.match(patron_while, codigo)
    coincidencias_include = re.match(patron_include, codigo)
    coincidencias_fin = re.match(patron_fin, codigo)
    coincidencias_return = re.match(patron_return, codigo)



    # Análisis de funciones
    if coincidencias_funcion:
        tipo_retorno = coincidencias_funcion.group(1)
        nombre_funcion = coincidencias_funcion.group(2)
        parametros = coincidencias_funcion.group(3)

        lista_parametros = [param.strip() for param in parametros.split(',')]

        # Guardar la función en el diccionario de funciones
        funciones[nombre_funcion] = {
            'tipo_retorno': tipo_retorno,
            'parametros': lista_parametros
        }

        return {
            'tipo_retorno': tipo_retorno,
            'nombre_funcion': nombre_funcion,
            'cantidad_parametros': len(lista_parametros),
            'lista_parametros': lista_parametros
        }

    # Análisis de prototipos de funciones
    elif coincidencias_prototipo:
        tipo_retorno = coincidencias_prototipo.group(1)
        nombre_funcion = coincidencias_prototipo.group(2)
        parametros = coincidencias_prototipo.group(3)

        lista_parametros = [param.strip() for param in parametros.split(',')]

        return {
            'tipo_retorno': tipo_retorno,
            'nombre_funcion': nombre_funcion,
            'cantidad_parametros': len(lista_parametros),
            'lista_parametros': lista_parametros
        }

    # Análisis de declaraciones de variables en una línea
    # Análisis de declaraciones de variables en una línea
    # Análisis de declaraciones de variables en una línea
    elif coincidencias_variable_linea:
        tipo_variable = coincidencias_variable_linea.group(1)
        nombre_variable = coincidencias_variable_linea.group(2)
        valor_asignado = coincidencias_variable_linea.group(3)

        if tipo_variable not in ["int", "float", "char"]:  # Agrega otros tipos permitidos
            return {
                'error': f"Tipo de variable no reconocido: {tipo_variable}"
            }

        if not re.match(r'^[_a-zA-Z]\w*$', nombre_variable):  # Validar identificador válido
            return {
                'error': f"Nombre de variable inválido: {nombre_variable}"
            }

        # Verificar si valor_asignado es una constante y convertirla al tipo adecuado
        if valor_asignado:
            # Si el valor es una constante, verificar el tipo
            if tipo_variable == "int":
                try:
                    valor_asignado = int(valor_asignado)  # Convertir a entero
                except ValueError:
                    return {'error': f"Valor '{valor_asignado}' no es un entero válido"}
            elif tipo_variable == "float":
                try:
                    valor_asignado = float(valor_asignado)  # Convertir a flotante
                except ValueError:
                    return {'error': f"Valor '{valor_asignado}' no es un flotante válido"}
            elif tipo_variable == "char":
                if len(valor_asignado) == 3 and valor_asignado.startswith("'") and valor_asignado.endswith("'"):
                    valor_asignado = valor_asignado[1]  # Eliminar las comillas simples
                else:
                    return {'error': f"Valor '{valor_asignado}' no es un carácter válido"}

        variables[nombre_variable] = {
            'valor': valor_asignado,
            'tipo': tipo_variable
        }

        return {
            'tipo_variable': tipo_variable,
            'nombre_variable': nombre_variable,
            'valor_asignado': valor_asignado
        }


    # Análisis de declaraciones de variables en varias líneas
    elif coincidencias_variable_multilinea:
        tipo_variable = coincidencias_variable_multilinea.group(1)
        nombre_variable = coincidencias_variable_multilinea.group(2)

        variables[nombre_variable] = {'valor': None, 'tipo': tipo_variable}  # Solo declaración

        return {
            'tipo_variable': tipo_variable,
            'nombre_variable': nombre_variable,
            'valor_asignado': None,
            'declaracion': True
        }

    # Análisis de estructuras de control 'if'
    elif coincidencias_if:
        condicion = coincidencias_if.group(1)

        return {
            'tipo_estructura': 'if',
            'condicion': condicion,
        }

    # Análisis de estructuras de control 'for'
    elif coincidencias_for:
        inicializacion = coincidencias_for.group(1)
        condicion = coincidencias_for.group(2)
        actualizacion = coincidencias_for.group(3)
        bloque_for = coincidencias_for.group(4)

        return {
            'tipo_estructura': 'for',
            'inicializacion': inicializacion,
            'condicion': condicion,
            'actualizacion': actualizacion,
            'bloque_for': bloque_for
        }

    # Análisis de estructuras de control 'while'
    elif coincidencias_while:
        condicion = coincidencias_while.group(1)
        return {
            'tipo_estructura': 'while',
            'condicion': condicion
        }

    # Fin de una función o bloque
    elif coincidencias_fin:
        return 'FIN'

    # Análisis de inclusiones de archivos
    elif coincidencias_include:
        archivo_incluido = coincidencias_include.group(1)

        return {
            'tipo_inclusion': 'header',
            'archivo_incluido': archivo_incluido
        }

    # Análisis de instrucciones 'return'
    elif coincidencias_return:
        expresion = coincidencias_return.group(1)

        # Verificar si la expresión es una variable declarada
        if expresion not in variables:
            return {'error': f'La variable {expresion} no está declarada'}
        
        # Verificar el tipo de la variable y el tipo de retorno de la función
        if funciones:  # Verificar que estamos dentro de una función
            # Obtener la función actual (supongamos que estamos procesando la función main por ahora)
            funcion_actual = list(funciones.values())[0]  # Esto debe ser más dinámico en el código real
            tipo_retorno_funcion = funcion_actual['tipo_retorno']
            tipo_variable = variables[expresion]['tipo']
            if tipo_retorno_funcion != tipo_variable:
                return {'error': f'El tipo de retorno no coincide con el tipo de la variable {expresion}'}

        return {
            'tipo_estructura': 'return',
            'expresion': expresion
        }

    # Verificación de errores si falta el punto y coma
    else:
        if ';' not in codigo and not any([
            re.match(patron_if, codigo),
            re.match(patron_for, codigo),
            re.match(patron_while, codigo),
            re.match(patron_include, codigo),
            re.match(patron_fin, codigo),
        ]):
            return {
                'error': 'Se esperaba un punto y coma al final de la declaración',
                'linea': codigo
            }

        return None


def analizar_codigo_desde_archivo():
    count = 0  # Inicializar el contador

    try:
        # Usar un administrador de contexto para abrir el archivo
        with open('ptest.c', 'r') as file1:
            while True:
                # Leer la siguiente línea
                line = file1.readline()

                # Si la línea está vacía, hemos llegado al final del archivo
                if not line:
                    break

                count += 1  # Incrementar el contador
                print(f"Línea {count}: {line.strip()}")  # Procesar la línea (ejemplo: imprimir)
                
    except FileNotFoundError:
        print("Error: El archivo 'ptest.c' no existe.")
    except Exception as e:
        print(f"Error inesperado: {e}")
    else:
        print(f"Análisis completado. Total de líneas procesadas: {count}")



#Prueba para int a="hola";
def check_type_compatibility(datatype, value):
    if datatype == "int" and not value.isdigit():
        return False  # Si es int, pero el valor no es un número
    if datatype == "char" and not (len(value) == 3 and value.startswith("'") and value.endswith("'")):
        return False  # Validación simple para char (por ejemplo: 'a')
    return True

# Dentro de la validación de declaraciones
def validate_declaration(datatype, identifier, value):
    if not check_type_compatibility(datatype, value):
        print(f"Error semántico: Incompatibilidad de tipos en la asignación a '{identifier}'.")
    else:
        print(f"'{identifier}' asignado correctamente.")        
