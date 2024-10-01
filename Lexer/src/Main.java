public class Main {
    public static void main(String[] args) {
        //textp a tokenizar
        String texto = "int a ;";

        //lista de tipos de tokens
        String[] operadores = {"operador_suma","+","operador_resta","-","operador_multiplicar","*",
                "operador_dividir","-", "operador_modulo","%","operador_asignar","-","operador_incrementar","++",
                "operador_decremento","--","operador_menor_que","<","operador_mayor_que",">",
                "operador_salida_estandar","<<","operador_entrada_estandar",">>"};
        String[] operadores_logicos = {"operador_logico_AND","&&","operador_logico_OR","||"};
        String[] comentarios = {"comentario_de_linea","//","comentario_inicio","/*","comentario_fin","*/",
                "comentario_vacio","/**/"};
        String[] tipos_de_datos = {"caracter","char","entero","int","booleano","bool","flotante","float",
                "flotante_doble_presision","double", "enumerados","enum", "estructura","struct", "sin_retorno","void",
                "retorno_funcion","return"};
        String[] palabras_reservadas = {"salida_de_texto","cout","salida_de_texto","cin",
                "salida_de_texto_formateada","printf","retorno_funcion","return","condicional_if","if",
                "condicional_else","else","salto_de_linea","endl","bucle_while","while"};
        char[] no_identificadores = {'_','`','~','!','@','#','$','^','&','*','(',')','=',
                '|','"',':',';','{','}','[',']','<','>','?','/'};
        char[] numeros = {'0','1','2','3','4','5','6','7','8','9'};

        //extrar texto
        String[] arreglo = texto.split(" ");
        for (String frase : arreglo) {
            
        }

    }
}