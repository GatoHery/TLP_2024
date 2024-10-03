package Class;

import Type.TokenType;

public class Token {
	TokenType type;
    String value;

    public Token(TokenType type, String value) {
        this.type = type;
        this.value = value;
    }

    @Override
    public String toString() {
        return "Token{" +
                "type=" + type +
                ", value='" + value + '\'' +
                '}';
    }
}

// Clase para representar la información almacenada en la tabla de símbolos
class SymbolInfo {
    String type;
    String description;

    public SymbolInfo(String type, String description) {
        this.type = type;
        this.description = description;
    }

    @Override
    public String toString() {
        return "SymbolInfo{" +
                "type='" + type + '\'' +
                ", description='" + description + '\'' +
                '}';
    }
}
