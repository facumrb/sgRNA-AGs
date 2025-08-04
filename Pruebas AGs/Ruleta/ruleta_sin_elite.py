import random

# Constantes globales
TAMANO_POBLACION = 10
LONGITUD_CROMOSOMA = 30
PROBABILIDAD_CROSSOVER = 75  # 75%
PROBABILIDAD_MUTACION = 5    # 5%
NUMERO_CICLOS = 20


def mostrar_pantalla(poblacion, decimales, objetivo, fitness, num_poblacion, total, min_val, max_val, prom):
    """Muestra en pantalla el estado actual de la población y sus estadísticas.
    
    Args:
        poblacion: Matriz de cromosomas binarios
        decimales: Lista de valores decimales de cada cromosoma
        objetivo: Lista de valores de la función objetivo
        fitness: Lista de valores de fitness
        num_poblacion: Número de generación actual
        total: Lista con totales [objetivo, fitness]
        min_val: Lista con valores mínimos [objetivo, fitness]
        max_val: Lista con valores máximos [objetivo, fitness]
        prom: Lista con promedios [objetivo, fitness]
    """
    # Mostrar encabezado
    if num_poblacion != 0:
        print(f"Población {num_poblacion}")
    else:
        print("Población Inicial\n")

    print(" =============================================================================")
    
    # Mostrar individuos
    for individuo in range(TAMANO_POBLACION):
        # Identificador del individuo
        print(f"{individuo:2d}: ", end="")

        # Representación binaria del cromosoma
        for gen in range(LONGITUD_CROMOSOMA):
            print(f"{poblacion[gen][individuo]}", end="")
        print(" ", end="")

        # Valores decimales, objetivo y fitness
        print(f"{decimales[individuo]:10.4f} {objetivo[individuo]:10.4f} {fitness[individuo]:10.4f}")

    # Mostrar estadísticas
    print("\nResumen:")
    _mostrar_estadisticas(total, min_val, max_val, prom)


def generar_poblacion_inicial(poblacion):
    """Genera una población inicial aleatoria de cromosomas binarios."""
    for individuo in range(TAMANO_POBLACION):
        for gen in range(LONGITUD_CROMOSOMA):
            poblacion[gen][individuo] = random.randint(0, 1)


def convertir_binario_a_decimal(poblacion, decimales):
    """Convierte cada cromosoma binario a su valor decimal equivalente."""
    for individuo in range(TAMANO_POBLACION):
        valor_decimal = 0
        exponente = LONGITUD_CROMOSOMA - 1
        
        for gen in range(LONGITUD_CROMOSOMA):
            if poblacion[gen][individuo] == 1:
                valor_decimal += 2 ** exponente
            exponente -= 1
            
        decimales[individuo] = valor_decimal


def calcular_funcion_objetivo(decimales, objetivo, total, min_val, max_val, prom):
    """Calcula el valor de la función objetivo para cada individuo y estadísticas globales.
    
    La función objetivo es f(x) = (x/coef)^2, donde coef es el valor máximo posible
    del cromosoma binario.
    
    Args:
        decimales: Lista de valores decimales de cada cromosoma
        objetivo: Lista donde se almacenarán los valores de la función objetivo
        total: Lista donde se almacenará el total [0] de valores objetivo
        min_val: Lista donde se almacenará el valor mínimo [0] de la función objetivo
        max_val: Lista donde se almacenará el valor máximo [0] de la función objetivo
        prom: Lista donde se almacenará el promedio [0] de valores objetivo
        
    Returns:
        Representación binaria del cromosoma con mayor valor decimal
    """
    coeficiente = (2 ** LONGITUD_CROMOSOMA) - 1
    maximo_decimal = 0
    
    # Calcular valor objetivo para cada individuo
    for individuo in range(TAMANO_POBLACION):
        valor_objetivo = _calcular_valor_objetivo(decimales[individuo], coeficiente)
        objetivo[individuo] = valor_objetivo
        
        # Actualizar el máximo valor decimal encontrado
        if decimales[individuo] > maximo_decimal:
            maximo_decimal = int(decimales[individuo])

    # Convertir el máximo valor a binario (sin el prefijo '0b')
    binario = bin(maximo_decimal)[2:]

    # Calcular estadísticas de la población
    _calcular_estadisticas_objetivo(objetivo, total, min_val, max_val, prom)

    return binario


def _calcular_valor_objetivo(valor_decimal, coeficiente):
    """Calcula el valor de la función objetivo para un valor decimal dado.
    
    Args:
        valor_decimal: Valor decimal del cromosoma
        coeficiente: Valor máximo posible del cromosoma
        
    Returns:
        Valor de la función objetivo
    """
    return float(round((valor_decimal / coeficiente) ** 2, 4))


def _calcular_estadisticas_objetivo(objetivo, total, min_val, max_val, prom):
    """Calcula estadísticas para los valores de la función objetivo.
    
    Args:
        objetivo: Lista de valores de la función objetivo
        total: Lista donde se almacenará el total [0] de valores objetivo
        min_val: Lista donde se almacenará el valor mínimo [0] de la función objetivo
        max_val: Lista donde se almacenará el valor máximo [0] de la función objetivo
        prom: Lista donde se almacenará el promedio [0] de valores objetivo
    """
    # Inicializar estadísticas con el primer individuo
    total[0] = min_val[0] = max_val[0] = prom[0] = objetivo[0]
    
    # Calcular estadísticas para el resto de individuos
    for individuo in range(1, TAMANO_POBLACION):
        total[0] += objetivo[individuo]
        
        if objetivo[individuo] < min_val[0]:
            min_val[0] = objetivo[individuo]
            
        if objetivo[individuo] > max_val[0]:
            max_val[0] = objetivo[individuo]
            
    prom[0] = total[0] / TAMANO_POBLACION


def calcular_fitness(objetivo, fitness, total, min_val, max_val, prom):
    """Calcula el valor de fitness para cada individuo y actualiza estadísticas.
    
    El fitness se calcula como la proporción del valor objetivo de cada individuo
    respecto al total de la población.
    
    Args:
        objetivo: Lista de valores de la función objetivo
        fitness: Lista donde se almacenarán los valores de fitness
        total: Lista donde se almacenará el total [1] de valores fitness
        min_val: Lista donde se almacenará el valor mínimo [1] de fitness
        max_val: Lista donde se almacenará el valor máximo [1] de fitness
        prom: Lista donde se almacenará el promedio [1] de valores fitness
    """
    total[1] = 0
    
    # Calcular fitness para cada individuo
    for individuo in range(TAMANO_POBLACION):
        fitness[individuo] = objetivo[individuo] / total[0]
        total[1] += fitness[individuo]
    
    # Actualizar estadísticas de fitness
    _actualizar_estadisticas_fitness(total, min_val, max_val, prom)


def _actualizar_estadisticas_fitness(total, min_val, max_val, prom):
    """Actualiza las estadísticas de fitness basadas en los valores objetivo.
    
    Args:
        total: Lista con totales [objetivo, fitness]
        min_val: Lista con valores mínimos [objetivo, fitness]
        max_val: Lista con valores máximos [objetivo, fitness]
        prom: Lista con promedios [objetivo, fitness]
    """
    # Normalizar estadísticas de objetivo para obtener estadísticas de fitness
    min_val[1] = min_val[0] / total[0]
    max_val[1] = max_val[0] / total[0]
    prom[1] = prom[0] / total[0]


def seleccion_por_ruleta(seleccion, fitness):
    """Implementa el método de selección por ruleta para elegir individuos para reproducción.
    
    La selección por ruleta asigna a cada individuo una probabilidad de ser seleccionado
    proporcional a su valor de fitness.
    
    Args:
        seleccion: Lista donde se almacenarán los índices de los individuos seleccionados
        fitness: Lista de valores de fitness de cada individuo
    """
    # Escalar fitness a porcentajes (0-100)
    fit_escalado = _escalar_fitness_a_porcentajes(fitness)
    
    # Construir la ruleta
    ruleta = _construir_ruleta(fit_escalado)
    
    # Seleccionar individuos
    _seleccionar_individuos(ruleta, seleccion)


def _escalar_fitness_a_porcentajes(fitness):
    """Escala los valores de fitness a porcentajes enteros (0-100).
    
    Args:
        fitness: Lista de valores de fitness
        
    Returns:
        Lista de valores de fitness escalados a porcentajes
    """
    fit_escalado = [0] * TAMANO_POBLACION
    indice_maximo = 0
    total_fitness = 0
    
    # Convertir fitness a porcentajes
    for individuo in range(TAMANO_POBLACION):
        fit_escalado[individuo] = int(fitness[individuo] * 100)
        
        # Asegurar un mínimo de representación
        if fit_escalado[individuo] == 0:
            fit_escalado[individuo] = 1
            
        # Encontrar el individuo con mayor fitness
        if fit_escalado[individuo] > fit_escalado[indice_maximo]:
            indice_maximo = individuo
            
        total_fitness += fit_escalado[individuo]
    
    # Ajustar para que la suma sea exactamente 100%
    _ajustar_total_porcentaje(fit_escalado, total_fitness, indice_maximo)
    
    return fit_escalado


def _ajustar_total_porcentaje(fit_escalado, total_fitness, indice_maximo):
    """Ajusta los valores de fitness para que sumen exactamente 100%.
    
    Args:
        fit_escalado: Lista de valores de fitness escalados
        total_fitness: Suma total de los valores de fitness escalados
        indice_maximo: Índice del individuo con mayor fitness
    """
    if total_fitness < 100:
        diferencia = 100 - total_fitness
        fit_escalado[indice_maximo] += diferencia
    elif total_fitness > 100:
        diferencia = total_fitness - 100
        fit_escalado[indice_maximo] -= diferencia


def _construir_ruleta(fit_escalado):
    """Construye una ruleta basada en los valores de fitness escalados.
    
    Args:
        fit_escalado: Lista de valores de fitness escalados a porcentajes
        
    Returns:
        Lista que representa la ruleta, donde cada posición contiene el índice
        de un individuo, repetido según su porcentaje de fitness
    """
    ruleta = [0] * 100  # Ruleta de 100 posiciones (porcentajes) 
    # ruleta = [0] * 120
    posicion_ruleta = 0
    
    for individuo in range(TAMANO_POBLACION):
        for _ in range(fit_escalado[individuo]):
            ruleta[posicion_ruleta] = individuo
            posicion_ruleta += 1
            
    return ruleta


def _seleccionar_individuos(ruleta, seleccion):
    """Selecciona individuos girando la ruleta.
    
    Args:
        ruleta: Lista que representa la ruleta
        seleccion: Lista donde se almacenarán los índices de los individuos seleccionados
    """
    for individuo in range(TAMANO_POBLACION):
        posicion = random.randint(0, 99)
        seleccion[individuo] = ruleta[posicion]


def aplicar_crossover(poblacion, pob_siguiente, seleccion):
    """Aplica el operador de cruce (crossover) entre pares de individuos seleccionados.
    
    El crossover se realiza con una probabilidad definida por PROBABILIDAD_CROSSOVER.
    Si se aplica, se selecciona un punto de cruce aleatorio y se intercambian los genes
    a partir de ese punto entre los dos padres.
    
    Args:
        poblacion: Matriz de cromosomas binarios actual
        pob_siguiente: Matriz para almacenar la nueva generación
        seleccion: Lista de índices de los individuos seleccionados
    """
    for i in range(0, TAMANO_POBLACION, 2):  # Procesar parejas de individuos
        padre1 = seleccion[i]
        padre2 = seleccion[i + 1]
        
        if _aplicar_crossover_segun_probabilidad():
            _realizar_crossover_en_punto(poblacion, pob_siguiente, padre1, padre2, i)
        else:
            _copiar_padres_sin_crossover(poblacion, pob_siguiente, padre1, padre2, i)


def _aplicar_crossover_segun_probabilidad():
    """Determina si se debe aplicar crossover según la probabilidad configurada.
    
    Returns:
        True si se debe aplicar crossover, False en caso contrario
    """
    return random.randint(0, 100) < PROBABILIDAD_CROSSOVER


def _realizar_crossover_en_punto(poblacion, pob_siguiente, padre1, padre2, posicion_hijo):
    """Realiza el crossover en un punto aleatorio entre dos padres.
    
    Args:
        poblacion: Matriz de cromosomas binarios actual
        pob_siguiente: Matriz para almacenar la nueva generación
        padre1: Índice del primer padre
        padre2: Índice del segundo padre
        posicion_hijo: Posición donde se almacenarán los hijos en pob_siguiente
    """
    punto_cruce = random.randint(1, LONGITUD_CROMOSOMA - 1)
    
    # Primera parte del cromosoma
    for gen in range(punto_cruce):
        pob_siguiente[gen][posicion_hijo] = poblacion[gen][padre1]
        pob_siguiente[gen][posicion_hijo + 1] = poblacion[gen][padre2]
        
    # Segunda parte del cromosoma (intercambiada)
    for gen in range(punto_cruce, LONGITUD_CROMOSOMA):
        pob_siguiente[gen][posicion_hijo] = poblacion[gen][padre2]
        pob_siguiente[gen][posicion_hijo + 1] = poblacion[gen][padre1]


def _copiar_padres_sin_crossover(poblacion, pob_siguiente, padre1, padre2, posicion_hijo):
    """Copia los padres directamente sin aplicar crossover.
    
    Args:
        poblacion: Matriz de cromosomas binarios actual
        pob_siguiente: Matriz para almacenar la nueva generación
        padre1: Índice del primer padre
        padre2: Índice del segundo padre
        posicion_hijo: Posición donde se almacenarán los hijos en pob_siguiente
    """
    for gen in range(LONGITUD_CROMOSOMA):
        pob_siguiente[gen][posicion_hijo] = poblacion[gen][padre1]
        pob_siguiente[gen][posicion_hijo + 1] = poblacion[gen][padre2]


def aplicar_mutacion(pob_siguiente):
    """Aplica el operador de mutación a los individuos según una probabilidad.
    
    La mutación se aplica con una probabilidad definida por PROBABILIDAD_MUTACION.
    Si se aplica, se selecciona un gen aleatorio y se invierte su valor (0->1 o 1->0).
    
    Args:
        pob_siguiente: Matriz de cromosomas binarios de la nueva generación
    """
    for individuo in range(TAMANO_POBLACION):
        if _aplicar_mutacion_segun_probabilidad():
            _mutar_gen_aleatorio(pob_siguiente, individuo)


def _aplicar_mutacion_segun_probabilidad():
    """Determina si se debe aplicar mutación según la probabilidad configurada.
    
    Returns:
        True si se debe aplicar mutación, False en caso contrario
    """
    return random.randint(0, 100) < PROBABILIDAD_MUTACION


def _mutar_gen_aleatorio(pob_siguiente, individuo):
    """Muta un gen aleatorio de un individuo.
    
    Args:
        pob_siguiente: Matriz de cromosomas binarios
        individuo: Índice del individuo a mutar
    """
    gen_a_mutar = random.randint(0, LONGITUD_CROMOSOMA - 1)
    pob_siguiente[gen_a_mutar][individuo] = 1 - pob_siguiente[gen_a_mutar][individuo]


def actualizar_poblacion(poblacion, pob_siguiente):
    """Actualiza la población actual con la nueva generación."""
    for individuo in range(TAMANO_POBLACION):
        for gen in range(LONGITUD_CROMOSOMA):
            poblacion[gen][individuo] = pob_siguiente[gen][individuo]


def guardar_datos(cromosoma, max_val, min_val, prom, num_poblacion):
    """Guarda los datos de la generación actual en un archivo CSV."""
    with open("Algoritmos.csv", "a", encoding="utf-8") as archivo:
        if num_poblacion != 0:
            archivo.write(f'"{cromosoma}";{max_val[0]};{min_val[0]};{prom[0]}\n')
        else:
            # Escribir encabezado si es la población inicial
            archivo.write("Cromosoma;Maximo;Minimo;Promedio\n")


def _mostrar_estadisticas(total, min_val, max_val, prom):
    """Función auxiliar para mostrar estadísticas de la población.
    
    Args:
        total: Lista con totales [objetivo, fitness]
        min_val: Lista con valores mínimos [objetivo, fitness]
        max_val: Lista con valores máximos [objetivo, fitness]
        prom: Lista con promedios [objetivo, fitness]
    """
    print(f"{'Total:':<10} {total[0]:10.4f} {total[1]:10.4f}")
    print(f"{'Minimo:':<10} {min_val[0]:10.4f} {min_val[1]:10.4f}")
    print(f"{'Maximo:':<10} {max_val[0]:10.4f} {max_val[1]:10.4f}")
    print(f"{'Promedio:':<10} {prom[0]:10.4f} {prom[1]:10.4f}")


def inicializar_estructuras():
    """Inicializa todas las estructuras de datos necesarias para el algoritmo genético.
    
    Returns:
        Tupla con todas las estructuras inicializadas:
        (poblacion, pob_siguiente, decimales, objetivo, fitness, total, min_val, max_val, prom, seleccion)
    """
    poblacion = [[0 for _ in range(TAMANO_POBLACION)] for _ in range(LONGITUD_CROMOSOMA)]
    pob_siguiente = [[0 for _ in range(TAMANO_POBLACION)] for _ in range(LONGITUD_CROMOSOMA)]
    decimales = [0.0] * TAMANO_POBLACION
    objetivo = [0.0] * TAMANO_POBLACION
    fitness = [0.0] * TAMANO_POBLACION
    total = [0.0] * 2       # [0]: valores objetivo, [1]: valores fitness
    min_val = [0.0] * 2     # [0]: mínimo objetivo, [1]: mínimo fitness
    max_val = [0.0] * 2     # [0]: máximo objetivo, [1]: máximo fitness
    prom = [0.0] * 2        # [0]: promedio objetivo, [1]: promedio fitness
    seleccion = [0] * TAMANO_POBLACION
    
    return (poblacion, pob_siguiente, decimales, objetivo, fitness, 
            total, min_val, max_val, prom, seleccion)


def main():
    """Función principal que ejecuta el algoritmo genético."""
    # Inicialización de estructuras de datos
    (poblacion, pob_siguiente, decimales, objetivo, fitness,
     total, min_val, max_val, prom, seleccion) = inicializar_estructuras()
    
    num_poblacion = 0  # Contador de generaciones

    # Ejecutar el algoritmo genético
    ejecutar_algoritmo_genetico(poblacion, pob_siguiente, decimales, objetivo, fitness,
                               total, min_val, max_val, prom, seleccion)


def ejecutar_algoritmo_genetico(poblacion, pob_siguiente, decimales, objetivo, fitness,
                               total, min_val, max_val, prom, seleccion):
    """Ejecuta el algoritmo genético completo.
    
    Args:
        poblacion: Matriz de cromosomas binarios
        pob_siguiente: Matriz para almacenar la siguiente generación
        decimales: Lista de valores decimales de cada cromosoma
        objetivo: Lista de valores de la función objetivo
        fitness: Lista de valores de fitness
        total: Lista con totales [objetivo, fitness]
        min_val: Lista con valores mínimos [objetivo, fitness]
        max_val: Lista con valores máximos [objetivo, fitness]
        prom: Lista con promedios [objetivo, fitness]
        seleccion: Lista para almacenar los individuos seleccionados
    """
    num_poblacion = 0  # Contador de generaciones
    
    # Generar y evaluar la población inicial
    generar_poblacion_inicial(poblacion)
    evaluar_poblacion(poblacion, decimales, objetivo, fitness, total, min_val, max_val, prom)
    
    # Mostrar y guardar datos de la población inicial
    cromosoma = bin(int(max(decimales)))[2:]  # Obtener el cromosoma con mayor valor
    mostrar_pantalla(poblacion, decimales, objetivo, fitness, num_poblacion, total, min_val, max_val, prom)
    guardar_datos(cromosoma, max_val, min_val, prom, num_poblacion)
    input("Presione una tecla para continuar...")

    # Ciclo principal del algoritmo genético
    for generacion in range(1, NUMERO_CICLOS + 1):
        num_poblacion = generacion
        
        # Aplicar operadores genéticos
        aplicar_operadores_geneticos(poblacion, pob_siguiente, seleccion, fitness)
        
        # Evaluar la nueva generación
        evaluar_poblacion(poblacion, decimales, objetivo, fitness, total, min_val, max_val, prom)

        # Mostrar y guardar datos de la generación actual
        cromosoma = bin(int(max(decimales)))[2:]  # Obtener el cromosoma con mayor valor
        mostrar_pantalla(poblacion, decimales, objetivo, fitness, num_poblacion, total, min_val, max_val, prom)
        guardar_datos(cromosoma, max_val, min_val, prom, num_poblacion)
        input("Presione una tecla para continuar...")


def evaluar_poblacion(poblacion, decimales, objetivo, fitness, total, min_val, max_val, prom):
    """Evalúa la población actual calculando valores decimales, objetivo y fitness.
    
    Args:
        poblacion: Matriz de cromosomas binarios
        decimales: Lista para almacenar valores decimales
        objetivo: Lista para almacenar valores de la función objetivo
        fitness: Lista para almacenar valores de fitness
        total: Lista para almacenar totales
        min_val: Lista para almacenar valores mínimos
        max_val: Lista para almacenar valores máximos
        prom: Lista para almacenar promedios
    """
    convertir_binario_a_decimal(poblacion, decimales)
    calcular_funcion_objetivo(decimales, objetivo, total, min_val, max_val, prom)
    calcular_fitness(objetivo, fitness, total, min_val, max_val, prom)


def aplicar_operadores_geneticos(poblacion, pob_siguiente, seleccion, fitness):
    """Aplica los operadores genéticos para crear una nueva generación.
    
    Args:
        poblacion: Matriz de cromosomas binarios actual
        pob_siguiente: Matriz para almacenar la nueva generación
        seleccion: Lista para almacenar los individuos seleccionados
        fitness: Lista de valores de fitness
    """
    seleccion_por_ruleta(seleccion, fitness)
    aplicar_crossover(poblacion, pob_siguiente, seleccion)
    aplicar_mutacion(pob_siguiente)
    actualizar_poblacion(poblacion, pob_siguiente)

if __name__ == "__main__":
    main()