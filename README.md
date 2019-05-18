Al iniciar la ejecución de la instruccion "start" del programa se le presentarán una serie de pasos:


**paso 1:** "-Insert the command you use to run your algorithm (no params and full paths required) in a shell as this were it-"

    Este paso refiere a la especificación de un comando que pueda ser directamente ejecutado en algún shell que permita la ejecución del programa.
    No se le exige al usuario una ubicación exacta del fichero que contenga el código del algoritmo a ejecutar, se le exige solamente el path completo del mismo 
    y no se espera que se introduzca ningún tipo de parámetro.

_ejemplo:_ 
    python D:\Proyectos\Escuela\OptimizationModels\algorithms\gradient_descent.py

    si el algoritmo exigiera algún parámetro se comprobará en pasos posteriores, es decir, si el comando:
    python D:\Proyectos\Escuela\OptimizationModels\algorithms\gradient_descent.py 1 1 1 fuera válido dado que el algoritmo requiere 3 parámetros,
    se exige que se obvie estos y nos quedamos con el comando sin parámetros como presentado en el ejemplo.


**paso 2:** "Insert for each parameter needed it's type (z means integer, r means real)"

    En este paso se exigirá que se introduzca un identificador por cada parámetro en forma de cadena separada por espacios.
    la z representaría un parámetro entero mientras que la r representaría uno real.

_ejemplo:_
    r z r

    siendo válida dicha entrada y definiendo 3 parámetros de entrada, el 1ro real al igual que el 3ro mientras que el 2do entero.


**paso 3:** "-Insert Lower and Upper search boundries for integer param #%d [example: 0 100]" ó "-Insert Lower and Upper search boundries for real param #%d [example: 1,5 99,9]" 

    Por cada uno de los parámetros declarados por el usuario se le pedirá una definición de los "boundries", superior e inferior. Deben ser enteros 
    separados por espacios o, si el parámetro es real, floats separados por espacios 

_ejemplo:_
    1 20 (caso entero o real)

    1,5 99 (caso real)


**paso 4:** "Insert optimal value (if none then you should expect minimization)" 

    Se requiere una declaración del óptimo esperado (en cuyo caso se minimiza el módulo de la resta del óptimo con el valor devuelto por el algoritmo del usuario).
    Si no se ofrece una definición entonces se minimizará el valor devuelto por el algoritmo del usuario.

_ejemplo:_
    100 (caso de que se este optimizando un porcentaje)
    en este caso se minimizará |100 - alg(params)|


Luego comenzara la ejecución del algoritmo Harmony Search! A esperar resultados! (estaran claros a la hora de imprimirlos)


**EJEMPLO DE EJECUCION OFRECIDO:** Se le ofrece un ejemplo de prueba ya listo:

    ---paso 1---
        python D:\ .... \algorithms\gradient_descent.py (full path required)

    ---paso 2---
        r z r

    ---paso 3---
        0.01 0.9         (eta)
        2 20             (iterations amount)
        0.0000001 0.9    (epsilon)

    ---paso 4---
        no se especifica y se elije minimizar


NOTA:
    se recomienda firmemente que el usuario modifique su programa que contiene el algoritmo para que evalúe un conjunto de entrenamiento aceptable que cubra
    mayormente el caso general de entrada para su problema, y devuelva, en vez de un solo valor, una lista de valores (separados por espacios) que representen:
    
    caso de algoritmo determinista: costo de ejecución por cada entrenamiento.
    caso de algoritmo no determinista: probabilidad de que el resultado sea el óptimo por cada entrenamiento, requiere varias corridas por entrenamiento.

    En ambos casos básicamente se pide una evaluación de su resultado. Asi se podrá utilizar un comparador basado en un concepto de dominancia explicado en el informe 
    de esta implementación. Gracias!
    