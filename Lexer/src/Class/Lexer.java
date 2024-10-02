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
            } else if (isOperator(currentChar)) {
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

    // Analizar identificadores y palabras clave
    private Token lexIdentifierOrKeyword() {
        int start = position;
        while (position < input.length() && Character.isLetterOrDigit(input.charAt(position))) {
            position++;
        }
        String value = input.substring(start, position);

        // Si es una palabra clave (aquí puedes añadir más)
        if (value.equals("if") || value.equals("while")) {
            return new Token(TokenType.KEYWORD, value);
        } else {
            // Si es un identificador, registrarlo en la tabla de símbolos
            SymbolInfo info = new SymbolInfo("unknown", "global", "null"); // Datos predeterminados
            symbolTable.put(value, info);
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

    // Analizar operadores
    private Token lexOperator() {
        char op = input.charAt(position);
        position++;
        return new Token(TokenType.OPERATOR, Character.toString(op));
    }

    private boolean isOperator(char c) {
        return c == '+' || c == '-' || c == '*' || c == '/';
    }

    private boolean isDelimiter(char c) {
        return c == ';' || c == '{' || c == '}';
    }

    // Método para mostrar la tabla de símbolos
    public void printSymbolTable() {
        System.out.println("Tabla de Símbolos:");
        for (Map.Entry<String, SymbolInfo> entry : symbolTable.entrySet()) {
            System.out.println("Símbolo: " + entry.getKey() + " -> " + entry.getValue());
        }
    }
}
