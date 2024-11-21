#lexer
import ply.lex as lex

# List of token names. Required
tokens = [
    "INCLUDE",
    "CONSTANT",
    "PLUS",
    "MINUS",
    "TIMES",
    "DIVIDE",
    "MOD",
    "AND",
    "OR",
    "NOT",
    "EQUALS",
    "NOTEQUALS",
    "LESS",
    "GREATER",
    "LPAREN",
    "RPAREN",
    "LBRACKET",
    "RBRACKET",
    "LBRACE",
    "RBRACE",
    "ID",
    "COMMA",
    "SEMICOLON",
    "APOSTROPHE",
    "QUOTE",
    "COMMENT",
    "COMMENTBLOCK",
    "ASSIGNMENT",
    #nuevos tokens
    "ASSIGN",
    #fin nuevos tokens
    "COLON",
    "QUESTION",
    "UNDERSCORE",
    "SQUOTE",
    "DATATYPE",
    "eof"
]

reserved_words = {
    "if": "IF",
    "else": "ELSE",
    "return": "RETURN",
    "void": "VOID",
    "do": "DO",
    "while": "WHILE",
    "break": "BREAK",
    "define": "DEFINE",
    "for": "FOR",
    "struct": "STRUCT",
    "switch": "SWITCH",
    "default": "DEFAULT",
    "case": "CASE",
    "true": "TRUE",
    "false": "FALSE"
}

dataTypes = {
    "int": "INT",
    "float": "FLOAT",
    "char": "CHAR",
    "bool": "BOOL",
    "double" : "DOUBLE",
    "string" : "STRING"    
}

# Add words reserved to tokens array
tokens += list(reserved_words.values())

# Regular expression rules
t_PLUS = r"\+"
t_MINUS = r"\-"
t_TIMES = r"\*"
t_DIVIDE = r"\/"
t_MOD = r"\%"
t_AND = r"\&\&"
t_OR = r"\|\|"
t_NOT = r"\!"
t_EQUALS = r"\=\="
t_NOTEQUALS = r"\!\="
t_LESS = r"\<"
t_GREATER = r"\>"
t_LPAREN = r"\("
t_RPAREN = r"\)"
t_LBRACE = r"\{"
t_RBRACE = r"\}"
t_LBRACKET = r"\["
t_RBRACKET = r"\]"
t_COMMA = r"\,"
t_SEMICOLON = r"\;"
t_APOSTROPHE = r"\'"
t_QUOTE = r"\""
#t_ASSIGNMENT = r"\="
t_SQUOTE = r"\'"
t_UNDERSCORE = r"\_"
t_QUESTION = r"\?"
t_COLON = r"\:"
t_eof= r'\$'
#nuevo
t_ASSIGN = r"\="


# A regular expression rule
def t_COMMENT(t):
    r"\/\/.*"
    pass

def t_COMMENTBLOCK(t):
    r"\/\*(.|\n)*\*\/"
    pass

def t_INCLUDE(t):
    r"\#(include)\s<([a-z]|[A-Z])*.h>"
    #r"\#(include)\shola.h"
    return t

#cambio
def t_RETURN(t):
    r'\breturn\b'  # Coincide con la palabra completa 'return'
    t.type = 'RETURN'  # Asegúrate de asignar un tipo específico, 'RETURN' para que no se confunda
    return t

def t_ID(t):
    r'([a-z]|[A-Z]|_)([a-z]|[A-Z]|\d|_)*'
    print(f"Reconocido: {t.value}")
    t.type = dataTypes.get(t.value, "ID")  # Prioridad para tipos de datos
    if t.type == "ID":
        t.type = reserved_words.get(t.value, "ID")  # Prioridad para palabras reservadas
    else:
        t.type = "DATATYPE"
    return t

def t_DATATYPE(t):
    r'(int|float|char|double|string)'
    return t

'''
def t_DECIMALNUMBER(t):
    r"\d+(\.\d+){1}"
    t.value = float(t.value)
    return t

def t_NUMBER(t):
    r"\d+"
    t.value = int(t.value)
    return t

def t_STRINGLIT(t):
    r'\".*\"'
    return t

def t_LETTER(t):
    r"\'.\'"
    t.value = t.value.replace("'", "")
    return t
'''

#cambios
def t_CONSTANT(t):
    r"(\d+(\.\d+)?) | (true|false) | (\"[^\"]*\") | \'.\'"
    return t




# Define a rule so we can track line numbers
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# Compute column.
#     input is the input text string
#     token is a token instance
def find_column(input, token):
    line_start = input.rfind('\n', 0, token.lexpos) + 1
    return (token.lexpos - line_start) + 1

# A string containing ignored characters (spaces and tabs)
t_ignore = " \t"

# Error handling rule
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)
    return t

class Identifier:
    name = ""
    dataType = ""
    value = ""
    scope = -1

    def __str__(self) :
        return f'{self.name}\t\t\t{self.dataType}\t\t{self.value}\t\t{self.scope}'

# Build the lexer
lexer = lex.lex()