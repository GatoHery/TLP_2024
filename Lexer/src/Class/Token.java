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
    String type;     // Tipo de dato (e.g., int, float, etc.)
    String scope;    // Ámbito (e.g., global, local)
    String value;    // Valor si es una constante

    public SymbolInfo(String type, String scope, String value) {
        this.type = type;
        this.scope = scope;
        this.value = value;
    }

    @Override
    public String toString() {
        return "SymbolInfo{" +
                "type='" + type + '\'' +
                ", scope='" + scope + '\'' +
                ", value='" + value + '\'' +
                '}';
    }
}
