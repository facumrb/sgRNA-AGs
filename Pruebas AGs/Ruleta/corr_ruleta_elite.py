import random


def mostrar_pantalla(poblacion, decimales, objetivo, fitness, pob, total, min_val, max_val, prom):
    if pob != 0:
        print(f"Poblacion {pob}")
    else:
        print("Poblacion Inicial\n")

    print(" =============================================================================")

    for c in range(10):
        print(f"{c:2d}: ", end="")

        # Muestra la fila de población (binarios)
        for i in range(30):
            print(f"{poblacion[i][c]}", end="")
        print(" ", end="")

        # Muestra los valores decimales, objetivo y fitness
        print(f"{decimales[c]:10.4f} {objetivo[c]:10.4f} {fitness[c]:10.4f}")

    # Muestra totales, mínimos, máximos y promedios
    print("\nResumen:")
    print(f"{'Total:':<10} {total[0]:10.4f} {total[1]:10.4f}")
    print(f"{'Minimo:':<10} {min_val[0]:10.4f} {min_val[1]:10.4f}")
    print(f"{'Maximo:':<10} {max_val[0]:10.4f} {max_val[1]:10.4f}")
    print(f"{'Promedio:':<10} {prom[0]:10.4f} {prom[1]:10.4f}")


def PoblacionInicial(poblacion):
    for c in range(10):
        for i in range(30):
            poblacion[i][c] = random.randint(0, 1)


def BinDec(poblacion, decimales):
    for i in range(10):
        dec = 0
        exp = 29
        for c in range(30):
            if poblacion[c][i] == 1:
                dec += 2 ** exp
            exp -= 1
        decimales[i] = dec


def FunObj(decimales, objetivo, total, min_val, max_val, prom):
    coef = (2 ** 30) - 1
    m = 0
    for c in range(10):
        aux = round((decimales[c] / coef) ** 2, 4)
        objetivo[c] = float(aux)
        if decimales[c] > m:
            m = int(decimales[c])

    binario = bin(m)[2:]  # binario sin el prefijo '0b'

    total[0] = min_val[0] = max_val[0] = prom[0] = objetivo[0]
    for c in range(1, 10):
        total[0] += objetivo[c]
        if objetivo[c] < min_val[0]:
            min_val[0] = objetivo[c]
        if objetivo[c] > max_val[0]:
            max_val[0] = objetivo[c]
    prom[0] = total[0] / 10

    return binario


def FunFit(objetivo, fitness, total, min_val, max_val, prom):
    total[1] = 0
    for c in range(10):
        fitness[c] = objetivo[c] / total[0]
        total[1] += fitness[c]

    min_val[1] = min_val[0] / total[0]
    max_val[1] = max_val[0] / total[0]
    prom[1] = prom[0] / total[0]


def Ruleta(seleccion, fitness, poblacion, pob_siguiente):
    max1 = max2 = m1 = m2 = 0
    ruleta = [0] * 120
    rul = 0
    fit = [0] * 10
    i = 0
    max_idx = 0

    r = random.Random()

    # Ajuste de valores de fitness
    for c in range(10):
        fit[c] = int(fitness[c] * 100)
        if fit[c] == 0:
            fit[c] = 1
        if fit[c] > fit[max_idx]:
            max_idx = c
        i += fit[c]

    if i < 100:
        dif = 100 - i
        fit[max_idx] += dif
    elif i > 100:
        dif = i - 100
        fit[max_idx] -= dif

    # Elitismo: seleccionar los dos mejores
    for c in range(10):
        if fit[c] >= max1:
            max2 = max1
            m2 = m1
            max1 = fit[c]
            m1 = c
        elif fit[c] > max2:
            max2 = fit[c]
            m2 = c

    for i in range(30):
        pob_siguiente[i][0] = poblacion[i][m1]
        pob_siguiente[i][1] = poblacion[i][m2]

    # Construir ruleta
    for c in range(10):
        for _ in range(fit[c]):
            ruleta[rul] = c
            rul += 1

    # Selección por ruleta (a partir de la posición 2)
    for c in range(2, 10):
        i = r.randint(0, 99)
        seleccion[c] = ruleta[i]


def CrossOver(poblacion, pob_siguiente, seleccion):
    PC = 75  # Probabilidad de crossover = 0.75

    for c in range(0, 10, 2):  # avanzar de a 2
        pad1 = seleccion[c]
        pad2 = seleccion[c + 1]
        prob = random.randint(0, 100)

        if prob < PC:
            pto = random.randint(1, 29)  # punto de cruce
            for i in range(pto):
                pob_siguiente[i][c] = poblacion[i][pad1]
                pob_siguiente[i][c + 1] = poblacion[i][pad2]
            for i in range(pto, 30):
                pob_siguiente[i][c] = poblacion[i][pad2]
                pob_siguiente[i][c + 1] = poblacion[i][pad1]
        else:
            for i in range(30):
                pob_siguiente[i][c] = poblacion[i][pad1]
                pob_siguiente[i][c + 1] = poblacion[i][pad2]


def Mutacion(pob_siguiente):
    PM = 5  # Probabilidad de mutación = 5%

    for c in range(10):
        prob = random.randint(0, 100)
        if prob < PM:
            pto = random.randint(1, 29)
            pob_siguiente[pto][c] = 1 - pob_siguiente[pto][c]  # invierte el bit


def ActualizarPob(poblacion, pob_siguiente):
    for c in range(10):
        for i in range(30):
            poblacion[i][c] = pob_siguiente[i][c]


def GuardarDatos(cromosoma, max_val, min_val, prom, pob):
    with open("Algoritmos.csv", "a", encoding="utf-8") as file:
        if pob != 0:
            file.write(f'"{cromosoma}";{max_val[0]};{min_val[0]};{prom[0]}\n')
        else:
            file.write("Cromosoma;Maximo;Minimo;Promedio\n")


def main():
    poblacion = [[0 for _ in range(10)] for _ in range(30)]
    pob_siguiente = [[0 for _ in range(10)] for _ in range(30)]
    decimales = [0.0] * 10
    objetivo = [0.0] * 10
    fitness = [0.0] * 10
    total = [0.0] * 2
    min_val = [0.0] * 2
    max_val = [0.0] * 2
    prom = [0.0] * 2
    seleccion = [0] * 10
    ciclos = 100

    pob = 0

    PoblacionInicial(poblacion)
    BinDec(poblacion, decimales)
    cromosoma = FunObj(decimales, objetivo, total, min_val, max_val, prom)
    FunFit(objetivo, fitness, total, min_val, max_val, prom)
    mostrar_pantalla(poblacion, decimales, objetivo, fitness, pob, total, min_val, max_val, prom)
    GuardarDatos(cromosoma, max_val, min_val, prom, pob)
    input("Presione una tecla para continuar...")

    for c in range(1, ciclos + 1):
        pob = c
        Ruleta(seleccion, fitness, poblacion, pob_siguiente)
        CrossOver(poblacion, pob_siguiente, seleccion)
        Mutacion(pob_siguiente)
        ActualizarPob(poblacion, pob_siguiente)
        BinDec(poblacion, decimales)
        cromosoma = FunObj(decimales, objetivo, total, min_val, max_val, prom)
        FunFit(objetivo, fitness, total, min_val, max_val, prom)

        mostrar_pantalla(poblacion, decimales, objetivo, fitness, pob, total, min_val, max_val, prom)
        GuardarDatos(cromosoma, max_val, min_val, prom, pob)
        input("Presione una tecla para continuar...")

if __name__ == "__main__":
    main()