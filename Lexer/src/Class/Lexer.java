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
				position++; // Ignorar espacios en blanco
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
				tokens.add(lexInvalid()); // Manejar caracteres inválidos como un bloque
			}
		}
		tokens.add(new Token(TokenType.END_OF_FILE, ""));
		return tokens;
	}

	// Analizar identificadores y palabras clave
	private Token lexIdentifierOrKeyword() {
		int start = position;
		StringBuilder identifier = new StringBuilder();

		boolean invalidIdentifier = false;

		while (position < input.length() && isValidIdentifierChar(input.charAt(position))) {
			identifier.append(input.charAt(position));
			position++;
		}

		// Verificar si hay un carácter inválido en medio del identificador
		if (position < input.length() && !Character.isWhitespace(input.charAt(position))
				&& !isDelimiter(input.charAt(position)) && !isOperatorStart(input.charAt(position))) {
			invalidIdentifier = true;
			identifier.append(input.charAt(position));
			position++;

			while (position < input.length() && !Character.isWhitespace(input.charAt(position))
					&& !isDelimiter(input.charAt(position))) {
				identifier.append(input.charAt(position));
				position++;
			}
		}

		String value = identifier.toString();

		if (invalidIdentifier) {
			return new Token(TokenType.ERROR, "Invalid identifier: " + value);
		}

		// Verificar si es una palabra clave
		switch (value) {
		case "include":
		case "using":
		case "namespace":
		case "if":
		case "while":
		case "else":
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

	// Función para caracteres inválidos
	private Token lexInvalid() {
		int start = position;
		StringBuilder invalidToken = new StringBuilder();

		while (position < input.length() && !Character.isWhitespace(input.charAt(position))
				&& !isDelimiter(input.charAt(position))) {
			invalidToken.append(input.charAt(position));
			position++;
		}

		return new Token(TokenType.ERROR, "Invalid identifier: " + invalidToken.toString());
	}

	// Verifica si el carácter es válido en un identificador
	private boolean isValidIdentifierChar(char c) {
		return Character.isLetterOrDigit(c) || c == '_';
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

		// Si el siguiente carácter también es un operador, lo manejamos por separado
		if (position < input.length() && isOperatorContinuation(input.charAt(position))) {
			// En lugar de combinar los operadores, tratamos cada uno por separado
			String firstOperator = input.substring(start, position); // Primer operador
			symbolTable.put(firstOperator, new SymbolInfo("OPERATOR", "Operador matemático o lógico"));
			return new Token(TokenType.OPERATOR, firstOperator); // Retorna solo el primer operador
		}

		// Caso estándar de un solo operador
		String value = input.substring(start, position);
		symbolTable.put(value, new SymbolInfo("OPERATOR", "Operador matemático o lógico"));
		return new Token(TokenType.OPERATOR, value);
	}

	private boolean isOperatorStart(char c) {
		return c == '+' || c == '-' || c == '*' || c == '/' || c == '=' || c == '<' || c == '>' || c == '!' || c == ':';
	}

	private boolean isOperatorContinuation(char c) {
		return c == '=';
	}

	private boolean isDelimiter(char c) {
		return c == ';' || c == '{' || c == '}' || c == '(' || c == ')';
	}

	public void printSymbolTable() {
		System.out.println("===================================");
		System.out.println("Tabla de Símbolos:");
		System.out.println("===================================");

		for (Map.Entry<String, SymbolInfo> entry : symbolTable.entrySet()) {
			System.out.printf("Símbolo     : %s\n", entry.getKey());
			System.out.printf("Tipo        : %s\n", entry.getValue().type);
			System.out.printf("Descripción : %s\n", entry.getValue().description);
			System.out.println("-----------------------------------");
		}
		System.out.println("===================================");
	}
}
