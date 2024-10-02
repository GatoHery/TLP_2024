// Clase principal para probar el Lexer

import java.util.List;

import Class.Lexer;
import Class.Token;

public class Main {
        public static void main(String[] args) {
            String code = "int x = 10; if(x + 3){ while(x){ x = x + 1;} }else{std::out<<'Nada'}";
    
            Lexer lexer = new Lexer(code);
            List<Token> tokens = lexer.tokenize();
    
            // Mostrar los tokens
            for (Token token : tokens) {
                System.out.println(token);
            }
    
            // Mostrar la tabla de símbolos
            lexer.printSymbolTable();
        }
    }