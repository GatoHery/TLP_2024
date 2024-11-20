import re

count = 0
debug = False

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

    if coincidencias_funcion:
        tipo_retorno = coincidencias_funcion.group(1)
        nombre_funcion = coincidencias_funcion.group(2)
        parametros = coincidencias_funcion.group(3)

        lista_parametros = [param.strip() for param in parametros.split(',')]

        return {
            'tipo_retorno': tipo_retorno,
            'nombre_funcion': nombre_funcion,
            'cantidad_parametros': len(lista_parametros),
            'lista_parametros': lista_parametros
        }
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
    elif coincidencias_variable_linea:
        tipo_variable = coincidencias_variable_linea.group(1)
        nombre_variable = coincidencias_variable_linea.group(2)
        valor_asignado = coincidencias_variable_linea.group(3)

        if valor_asignado is not None:
            return {
                'tipo_variable': tipo_variable,
                'nombre_variable': nombre_variable,
                'valor_asignado': valor_asignado
            }
        else:
            return {
                'tipo_variable': tipo_variable,
                'nombre_variable': nombre_variable,
                'declaracion': True
            }
    elif coincidencias_variable_multilinea:
        tipo_variable = coincidencias_variable_multilinea.group(1)
        nombre_variable = coincidencias_variable_multilinea.group(2)

        return {
            'tipo_variable': tipo_variable,
            'nombre_variable': nombre_variable,
            'valor_asignado': None,
            'declaracion': True
        }
    elif coincidencias_if:
        condicion = coincidencias_if.group(1)

        return {
            'tipo_estructura': 'if',
            'condicion': condicion,
        }
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
    elif coincidencias_while:
        condicion = coincidencias_while.group(1)
        return {
            'tipo_estructura': 'while',
            'condicion': condicion
        }
    elif coincidencias_fin:
        return 'FIN'
    elif coincidencias_include:
        archivo_incluido = coincidencias_include.group(1)

        return {
            'tipo_inclusion': 'header',
            'archivo_incluido': archivo_incluido
        }
    else:
        return None

def analizar_codigo_desde_archivo():
    try:
        file1 = open('test.c', 'r')
        while True:
            global count
            count += 1
        
            # Get next line from file
            line = file1.readline()
        
            # if line is empty
            # end of file is reached
            if not line:
                break
            res = analizar_codigo(line.strip())
            if res == None and not debug:
                continue
            print(res)
        
        file1.close()
    except FileNotFoundError:
        print("El archivo 'test.c' no se encontró.")

analizar_codigo_desde_archivo()
