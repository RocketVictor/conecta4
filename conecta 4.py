import numpy as np
import random
import time

# Códigos de color para resaltar fichas
REINICIO = "\033[0m"
ROJO = "\033[31m"  # Rojo
AMARILLO = "\033[33m"  # Amarillo
BRILLO = "\033[1m"  # Para el brillo
# Imprimir la matriz 6 columnas x 7 filas llena de ceros:
def crear_tablero():
    return np.zeros((6, 7), dtype=int) 
# Imprime el tablero que se ve durante el juego y cambia los colores del último movimiento:
def imprimir_tablero(tablero, ultima_jugada=None):
    print("\n   0   1   2   3   4   5   6")
    print(" +---+---+---+---+---+---+---+")
    for fila in range(5, -1, -1):
        fila_str = []
        for col in range(7):
            celda = tablero[fila][col]
            if ultima_jugada and (fila, col) == ultima_jugada:
                if celda == 1:
                    ficha = f"{BRILLO + ROJO}X{REINICIO}"
                else:
                    ficha = f"{BRILLO + AMARILLO}O{REINICIO}"
            else:
                if celda == 0:
                    ficha = " "
                elif celda == 1:
                    ficha = "X"
                else:
                    ficha = "O"
            fila_str.append(ficha)
        print(" | " + " | ".join(fila_str) + " |")
        print(" +---+---+---+---+---+---+---+")
# Comprueba si el valor está dentro de los parametros de la tabla: 
def es_valido(tablero, columna):
    return columna >= 0 and columna < 7 and tablero[5][columna] == 0
# Selecciona la fila más baja:
def encontrar_fila(tablero, columna):
    for fila in range(6):
        if tablero[fila][columna] == 0:
            return fila
# Suelta la ficha en la fila más baja:
def soltar_ficha(tablero, fila, columna, ficha):
    tablero[fila][columna] = ficha

def verificar_ganador(tablero, ficha):
    # Comprueba en horizontal:
    for fila in range(6):
        for col in range(4):
            if np.all(tablero[fila, col:col+4] == ficha):
                return True

    # Comprueba en vertical:
    for col in range(7):
        for fila in range(3):
            if np.all(tablero[fila:fila+4, col] == ficha):
                return True

    # Comprueba las diagonales positivas:
    for fila in range(3):
        for col in range(4):
            if all([tablero[fila+i][col+i] == ficha for i in range(4)]):
                return True

    # Comprueba las diagonales negativas:
    for fila in range(3):
        for col in range(3, 7):
            if all([tablero[fila+i][col-i] == ficha for i in range(4)]):
                return True

    return False
# Devuelve el tablero tras el último movimiento:
def tablero_lleno(tablero):
    return all(tablero[5][col] != 0 for col in range(7))
# Movimientos de la ia:
def mover_ia(tablero, ficha):
    print("Fatimer está pensando...")
    tiempo_pensamiento = random.uniform(1, 5)  # Tiempo de espera aleatorio entre 1 y 5 segundos:
    time.sleep(tiempo_pensamiento)

    # Estrategia 1: Intentar ganar si es posible:
    for columna in range(7):
        if es_valido(tablero, columna):
            fila = encontrar_fila(tablero, columna)
            tablero[fila][columna] = ficha
            if verificar_ganador(tablero, ficha):
                tablero[fila][columna] = 0  
                return columna
            tablero[fila][columna] = 0  

    # Estrategia 2: Bloquear al jugador si está por ganar:
    ficha_oponente = 1 if ficha == 2 else 2
    for columna in range(7):
        if es_valido(tablero, columna):
            fila = encontrar_fila(tablero, columna)
            tablero[fila][columna] = ficha_oponente
            if verificar_ganador(tablero, ficha_oponente):
                tablero[fila][columna] = 0  
                return columna
            tablero[fila][columna] = 0  

    # Estrategia 3: Elegir una columna válida aleatoriamente:
    columnas_validas = [col for col in range(7) if es_valido(tablero, col)]
    return random.choice(columnas_validas)

def juego():
    while True:  # Bucle principal para jugar múltiples rondas:
        tablero = crear_tablero()
        juego_terminado = False
        ultima_jugada = None

        print("\n¡Bienvenidos a Conecta 4!\n")
        imprimir_tablero(tablero)

        modo = input("Selecciona el modo de juego:\n1. Jugador vs Jugador\n2. Jugador vs Fatimer\nTu elección: ")
        while modo < "1" or modo > "2":
            modo = input("Modo de juego incorrecto, vuelve a elegir el modo: ")
        if modo == "1":
            contra_bot = False
        else:
            contra_bot = True

        turno = random.choice([0, 1])
        print(f"\nEl jugador que comienza es {'Jugador 1 (X)' if turno == 0 else ('Fatimer (X)' if contra_bot else 'Jugador 2 (O)')}")

        tiempo_restante = [45, 45]  # 45 segundos para ambos jugadores:
        while not juego_terminado:
            inicio_turno = time.time()
            
            if turno == 0:
                print(f"\nTurno del Jugador 1 (X) - Tiempo restante: {int(tiempo_restante[0])} segundos")
            else:
                if contra_bot:
                    print(f"\nTurno de Fatimer (O) - Tiempo restante: {int(tiempo_restante[1])} segundos")
                else:
                    print(f"\nTurno del Jugador 2 (O) - Tiempo restante: {int(tiempo_restante[1])} segundos")
            
            if tiempo_restante[turno] <= 0:
                if turno == 1 and contra_bot:
                    print("\nDerrotaste a Fatimer, ¡felicidades!")
                elif turno == 0 and contra_bot:
                    print("\n¡Has perdido! ¡No puedes contra Fatimer!")
                else:
                    print(f"\nEl Jugador {turno + 1} se quedó sin tiempo. ¡El otro jugador gana!")
                juego_terminado = True
                break

            if contra_bot and turno == 1:
                columna = mover_ia(tablero, 2)
            else:
                columna = -1
                while columna < 0 or columna > 6:
                    entrada = input("Selecciona una columna (0-6): ")
                    try:
                        columna = int(entrada)  # Intentar convertir a entero:
                    except ValueError:
                        continue

            tiempo_transcurrido = time.time() - inicio_turno
            tiempo_restante[turno] -= tiempo_transcurrido

            if not es_valido(tablero, columna):
                print("Movimiento inválido. Intenta de nuevo.")
                continue

            fila = encontrar_fila(tablero, columna)
            ficha = 1 if turno == 0 else 2
            soltar_ficha(tablero, fila, columna, ficha)
            ultima_jugada = (fila, columna)

            imprimir_tablero(tablero, ultima_jugada)

            if verificar_ganador(tablero, ficha):
                if contra_bot and turno == 1:
                    print("\n¡Has perdido! ¡No puedes contra Fatimer!")
                elif contra_bot and turno == 0:
                    print("\nDerrotaste a Fatimer, ¡felicidades!")
                else:
                    print(f"\n¡El Jugador {turno + 1} gana! ¡Felicidades!")
                juego_terminado = True
            elif tablero_lleno(tablero):
                print("\n¡El juego termina en empate! ¡No hay más movimientos!")
                juego_terminado = True
            else:
                turno = (turno + 1) % 2

        # Preguntar al usuario si desea jugar otra partida:
        jugar_de_nuevo = input("\n¿Quieres jugar otra ronda? (s/n): ")
        if jugar_de_nuevo != 's':
            print("¡Gracias por jugar! ¡Hasta la próxima!")
            break
juego()