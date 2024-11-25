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
    elif coincidencias_variable_linea:
        tipo_variable = coincidencias_variable_linea.group(1)
        nombre_variable = coincidencias_variable_linea.group(2)
        valor_asignado = coincidencias_variable_linea.group(3)

        # Guardar la variable en el diccionario de variables
        if valor_asignado is not None:
            variables[nombre_variable] = {
                'valor': valor_asignado,
                'tipo': tipo_variable
            }
        else:
            variables[nombre_variable] = {'valor': None, 'tipo': tipo_variable}  # Solo declaración sin asignación

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
    try:
        file1 = open('ptest.c', 'r')
        while True:
            global count
            count += 1

            # Obtener la siguiente línea del archivo
            line = file1.readline()

            # Si la línea está vacía,
