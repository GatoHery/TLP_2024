// TEST CASES

/*

// Success: return de variable
int main() {
    int a = 12;
    return a;
}

// Success: sum de 2 variables
int main() {
    int a = 12;
    int b = 13;
    return a + b;
}

// Success: return dentro de IF
int main() {
    int a = 12;
    int b = 13;
    if (a > b) {
        return a;
    } else {
        return b;
    }
}

// Success: uso de bool con libreria
#include <stdbool.h>
int main() {
    bool a = true;
    return a;
}

Error: Uso de bool sin libreria
int main() {
    bool a = true;
    return a;
}

Error: Variable 'a' redeclarada
int main() {
    int a = 12;
    int a = 13;
    return a;
}

Error: Division entre 0
int main() {
    int a = 12;
    int b = 0;
    return a / b;
}

////////////////////////// TEST CASES //////////////////////////

 /* 
Listado de funciones semánticas funcionales:
1- Ausencia de ; al final de la instrucción de código ✓
	Ejemplo
	int main() {
    	int a =2;
    	int b = 3
    	}

2- Variable repetida ✓ 
	Ejemplo
	int main() {
	int a = 10;
	int a = 35;
	return a;
	}

3- Variables incompatibles de tipo (int recibiendo cadena)✓
	Ejemplo
	int main (){
	int a ="como ta";
	}

4- Variables incompatibles de tipo (float recibiendo cadena)✓
	Ejemplo
	int main (){
	float b ="qiubo";
	}

5- División entre 0 ✓
	Ejemplo	
	int main() {
	int suma =10;
	int resta = 0;
	return suma/resta;
	}

6- Variable no declarada ✓
	Ejemplo
	int main() {
	int suma =10;
	return resta;
	}

7- Variables mal escritas previo a una declaración ✓
	Ejemplo
	int main() {
	1.5 int k =10;
	}

8- Else sin if ✓
	Ejemplo
	int main() {
	int a=2;

	else {return a;
	}
	return a;
	}

9- Resta con resultado negativo (nuestro parser no maneja int a= -5; da error) ✓
	Ejemplo 
	int main() {
	int a = 2;
	int b = 3;
    	return a-b;
    	}

10- Mal manejo sintaxis en return ✓
	Ejemplo
	int main() {
    	int a =2;
    	int b = 3;
    	return a+;
}

11- Uso de bool sin librería ✓
	int main() {
    	bool a = true;
    	return a;
	}

12- Mal uso de void ✓
	e	Ejemplo
	#include <stdio.h>

	void sumar() {
    int a = 5;   
    int b = 3;    
    return a + b;
	}


	int main() {
    sumar();        

    return 0;
	}
*/