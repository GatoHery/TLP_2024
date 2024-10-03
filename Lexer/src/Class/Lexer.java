package Class;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import Type.TokenType;

public class Lexer {
	private String input;
    private int position;

    // Tabla de símbolos usando un HashMap
    private Map<String, SymbolInfo> symbolTable;

    public Lexer(String input) {
        this.input = input;
        this.position = 0;
        this.symbolTable = new HashMap<>();
    }

    // Función principal que tokeniza la entrada y llena la tabla de símbolos
    public List<Token> tokenize() {
        List<Token> tokens = new ArrayList<>();

        while (position < input.length()) {
            char currentChar = input.charAt(position);

            if (Character.isWhitespace(currentChar)) {
                position++;  // Ignorar espacios en blanco
            } else if (Character.isLetter(currentChar)) {
                tokens.add(lexIdentifierOrKeyword());
            } else if (Character.isDigit(currentChar)) {
                tokens.add(lexNumber());
            } else if (currentChar == '\'' || currentChar == '"') {
                tokens.add(lexString());
            } else if (isOperatorStart(currentChar)) {
                tokens.add(lexOperator());
            } else if (isDelimiter(currentChar)) {
                tokens.add(new Token(TokenType.DELIMITER, Character.toString(currentChar)));
                position++;
            } else {
                System.out.println("Unexpected character: " + currentChar);
                position++;
            }
        }
        tokens.add(new Token(TokenType.END_OF_FILE, ""));
        return tokens;
    }

    // Analizar identificadores y palabras clave, incluyendo secuencias con ::
    private Token lexIdentifierOrKeyword() {
        int start = position;
        StringBuilder fullIdentifier = new StringBuilder();

        while (position < input.length() && (Character.isLetterOrDigit(input.charAt(position)) || input.charAt(position) == ':')) {
            fullIdentifier.append(input.charAt(position));
            position++;
        }

        String value = fullIdentifier.toString();

        // Identificar palabras clave, librerías y funciones predefinidas
        switch (value) {
            case "include":
            case "using":
            case "namespace":
            case "if":
            case "while":
            case "else":
                symbolTable.put(value, new SymbolInfo("KEYWORD", "Palabra reservada del lenguaje"));
                return new Token(TokenType.KEYWORD, value);

            case "std":
                symbolTable.put(value, new SymbolInfo("KEYWORD", "Palabra reservada del lenguaje"));
                return new Token(TokenType.KEYWORD, value);

            case "int":
                symbolTable.put(value, new SymbolInfo("INT", "Identificador de tipo de dato"));
                return new Token(TokenType.KEYWORD, value);

            case "cout":
                symbolTable.put(value, new SymbolInfo("BUILTIN_FUNCTIONS", "Operador de salida de datos estándar"));
                return new Token(TokenType.IDENTIFIER, value);

            case "main":
                symbolTable.put(value, new SymbolInfo("ID", "Identificador de función principal"));
                return new Token(TokenType.IDENTIFIER, value);

            default:
                // Si es un identificador normal, registrarlo en la tabla de símbolos
                symbolTable.put(value, new SymbolInfo("ID", "Identificador"));
                return new Token(TokenType.IDENTIFIER, value);
        }
    }

    // Analizar números
    private Token lexNumber() {
        int start = position;
        while (position < input.length() && Character.isDigit(input.charAt(position))) {
            position++;
        }
        String value = input.substring(start, position);
        return new Token(TokenType.NUMBER, value);
    }

    // Analizar cadenas de texto
    private Token lexString() {
        char quoteType = input.charAt(position);
        position++;
        int start = position;

        while (position < input.length() && input.charAt(position) != quoteType) {
            position++;
        }

        String value = input.substring(start, position);
        position++; // Saltar la comilla de cierre

        // Guardar la cadena en la tabla de símbolos con descripción
        symbolTable.put(value, new SymbolInfo("STRING", "Cadena de caracteres"));
        return new Token(TokenType.STRING, value);
    }

    // Analizar operadores
    private Token lexOperator() {
        int start = position;
        position++;
        if (position < input.length() && isOperatorContinuation(input.charAt(position))) {
            position++;
        }
        String value = input.substring(start, position);

        // Asignar tipo y descripción según el operador encontrado
        switch (value) {
            case "<<":
                symbolTable.put(value, new SymbolInfo("LGREATER", "Operador de salida"));
                break;
            default:
                symbolTable.put(value, new SymbolInfo("OPERATOR", "Operador matemático o lógico"));
                break;
        }
        return new Token(TokenType.OPERATOR, value);
    }

    private boolean isOperatorStart(char c) {
        return c == '+' || c == '-' || c == '*' || c == '/' || c == '=' || c == '<' || c == '>' || c == '!' || c == ':';
    }

    private boolean isOperatorContinuation(char c) {
        return c == '=' || c == ':';
    }

    private boolean isDelimiter(char c) {
        return c == ';' || c == '{' || c == '}' || c == '(' || c == ')';
    }

    // Método para mostrar la tabla de símbolos con el formato especificado
    public void printSymbolTable() {
        System.out.println("Tabla de Símbolos:");
        for (Map.Entry<String, SymbolInfo> entry : symbolTable.entrySet()) {
            System.out.println("Símbolo: " + entry.getKey() + ", Tipo: " + entry.getValue().type +
                               ", Descripción: " + entry.getValue().description);
        }
    }
}
