// Clase principal para probar el Lexer

import java.io.File;
import java.io.FileNotFoundException;
import java.util.List;
import java.util.Scanner;
import java.util.InputMismatchException;

import Class.Lexer;
import Class.Token;

public class Main {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        String code = "";

        try {
            // Menú para seleccionar la opción
            System.out.println("Seleccione una opción para ingresar el código:");
            System.out.println("1. Ingresar ruta del archivo de código");
            System.out.println("2. Ingresar el código manualmente por consola");
            System.out.println("3. Usar el código de ejemplo");

            int option = scanner.nextInt();
            scanner.nextLine();  // Consumir la nueva línea

            switch (option) {
                case 1:
                    System.out.print("Ingrese la ruta completa del archivo: ");
                    String filePath = scanner.nextLine();
                    code = readCodeFromFile(filePath);
                    break;

                case 2:
                    System.out.println("Ingrese el código:");
                    code = scanner.nextLine();
                    break;

                case 3:
                    // Código de ejemplo
                    code = "int #x# == $10.1; if(x + 3){ while(x){ x = x + 1;} }else{std::out<<'Nada'}";
                    System.out.println("Usando el código de ejemplo...");
                    break;

                default:
                    System.out.println("Opción no válida. Saliendo del programa.");
                    return; // Finaliza la ejecución si la opción no es válida
            }

            // Procesar el código con el lexer
            Lexer lexer = new Lexer(code);
            List<Token> tokens = lexer.tokenize();
            System.out.println("===================================");
            System.out.println("Mostrando lista de caracteres:");
            System.out.println("===================================");

            for (Token token : tokens) {
                System.out.printf("Token: %s | Valor: %s\n", token.getType(), token.getValue());
            }
            System.out.println("===================================");

            lexer.printSymbolTable();

        } catch (InputMismatchException e) {
            System.out.println("Error: Ingrese un número válido para seleccionar una opción.");
        } catch (FileNotFoundException e) {
            System.out.println("Error: No se pudo encontrar el archivo. Verifique la ruta e intente nuevamente.");
        } catch (Exception e) {
            System.out.println("Error inesperado: " + e.getMessage());
            e.printStackTrace();  // Esto es opcional, para obtener más detalles en caso de errores.
        } finally {
            scanner.close();  // Asegurarse de cerrar el Scanner
        }
    }

    // Método para leer el código desde un archivo
    private static String readCodeFromFile(String filePath) throws FileNotFoundException {
        StringBuilder code = new StringBuilder();
        try (Scanner fileScanner = new Scanner(new File(filePath))) {
            while (fileScanner.hasNextLine()) {
                code.append(fileScanner.nextLine()).append("\n");
            }
        }
        return code.toString();
    }
}
