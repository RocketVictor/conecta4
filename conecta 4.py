import numpy as np
import random
import time
import threading

# Códigos de color ANSI para resaltar fichas
REINICIO = "\033[0m"
ROJO = "\033[31m"  # Rojo
AMARILLO = "\033[33m"  # Amarillo
NEGRO = "\033[1m"  # Negro

def crear_tablero():
    return np.zeros((6, 7), dtype=int)

def imprimir_tablero(tablero, ultima_jugada=None):
    print("\n   0   1   2   3   4   5   6")
    print(" +---+---+---+---+---+---+---+")
    for fila in range(5, -1, -1):
        fila_str = []
        for col in range(7):
            celda = tablero[fila][col]
            if ultima_jugada and (fila, col) == ultima_jugada:
                ficha = (f"{NEGRO + ROJO}X{REINICIO}" if celda == 1 else 
                         f"{NEGRO + AMARILLO}O{REINICIO}")
            else:
                ficha = " " if celda == 0 else ("X" if celda == 1 else "O")
            fila_str.append(ficha)
        print(" | " + " | ".join(fila_str) + " |")
        print(" +---+---+---+---+---+---+---+")

def es_valido(tablero, columna):
    return columna >= 0 and columna < 7 and tablero[5][columna] == 0

def encontrar_fila(tablero, columna):
    for fila in range(6):
        if tablero[fila][columna] == 0:
            return fila

def soltar_ficha(tablero, fila, columna, ficha):
    tablero[fila][columna] = ficha

def verificar_ganador(tablero, ficha):
    # Comprobar horizontal
    for fila in range(6):
        for col in range(4):
            if np.all(tablero[fila, col:col+4] == ficha):
                return True

    # Comprobar vertical
    for col in range(7):
        for fila in range(3):
            if np.all(tablero[fila:fila+4, col] == ficha):
                return True

    # Comprobar diagonales positivas
    for fila in range(3):
        for col in range(4):
            if all([tablero[fila+i][col+i] == ficha for i in range(4)]):
                return True

    # Comprobar diagonales negativas
    for fila in range(3):
        for col in range(3, 7):
            if all([tablero[fila+i][col-i] == ficha for i in range(4)]):
                return True

    return False

def tablero_lleno(tablero):
    return all(tablero[5][col] != 0 for col in range(7))

def mover_ia(tablero, ficha):
    print("Fatimer está pensando...")
    tiempo_pensamiento = random.uniform(1, 5)  # Tiempo de espera aleatorio entre 1 y 5 segundos
    time.sleep(tiempo_pensamiento)

    # Estrategia 1: Intentar ganar si es posible
    for columna in range(7):
        if es_valido(tablero, columna):
            fila = encontrar_fila(tablero, columna)
            tablero[fila][columna] = ficha
            if verificar_ganador(tablero, ficha):
                tablero[fila][columna] = 0  # Deshacer movimiento
                return columna
            tablero[fila][columna] = 0  # Deshacer movimiento

    # Estrategia 2: Bloquear al jugador si está por ganar
    ficha_oponente = 1 if ficha == 2 else 2
    for columna in range(7):
        if es_valido(tablero, columna):
            fila = encontrar_fila(tablero, columna)
            tablero[fila][columna] = ficha_oponente
            if verificar_ganador(tablero, ficha_oponente):
                tablero[fila][columna] = 0  # Deshacer movimiento
                return columna
            tablero[fila][columna] = 0  # Deshacer movimiento

    # Estrategia 3: Elegir una columna válida aleatoriamente
    columnas_validas = [col for col in range(7) if es_valido(tablero, col)]
    return random.choice(columnas_validas)

# Función para actualizar el tiempo y mostrarlo correctamente
def actualizar_tiempo(tiempo_restante, turno, stop_event):
    while tiempo_restante[turno] > 0:
        if stop_event.is_set():
            break
        print(f"Tiempo restante: {tiempo_restante[turno]} segundos", end="\r", flush=True)
        time.sleep(1)
        tiempo_restante[turno] -= 1

    if tiempo_restante[turno] <= 0:
        print(f"Tiempo restante: {0} segundos")

# Función principal del juego
def juego():
    tablero = crear_tablero()
    juego_terminado = False
    ultima_jugada = None

    print("\n¡Bienvenidos a Conecta 4!\n")
    imprimir_tablero(tablero)

    modo = input("Selecciona el modo de juego:\n1. Jugador vs Jugador\n2. Jugador vs Fatimer\nTu elección: ")
    contra_bot = modo == "2"

    turno = random.choice([0, 1])
    print(f"\nEl jugador que comienza es {'Jugador 1 (X)' if turno == 0 else ('Fatimer (X)' if contra_bot else 'Jugador 2 (O)')}")

    tiempo_restante = [45, 45]  # 45 segundos para ambos jugadores
    stop_event = threading.Event()  # Evento de paro del temporizador

    while not juego_terminado:
        if turno == 0:
            print(f"\nTurno del Jugador 1 (X) ")
        else:
            if contra_bot:
                print(f"\nTurno de Fatimer (O) ")
            else:
                print(f"\nTurno del Jugador 2 (O) ")

        # Iniciar el hilo para el contador de tiempo
        stop_event.clear()  # Reiniciar el evento de paro para el nuevo turno
        timer_thread = threading.Thread(target=actualizar_tiempo, args=(tiempo_restante, turno, stop_event))
        timer_thread.start()

        entrada_valida = False
        while tiempo_restante[turno] > 0 and not entrada_valida:
            try:
                columna = int(input("\nSelecciona una columna (0-6): "))
                if columna < 0 or columna > 6:
                    raise ValueError
                if not es_valido(tablero, columna):
                    print("Movimiento inválido. Intenta de nuevo.")
                    continue
                entrada_valida = True
            except ValueError:
                print("Entrada inválida. Por favor ingresa un número entre 0 y 6.")
            
            # Verificar si el tiempo se ha agotado
            if tiempo_restante[turno] <= 0:
                print(f"\nEl tiempo del Jugador {turno + 1} se agotó. ¡Pierde el turno!")
                juego_terminado = True
                stop_event.set()  # Detener el temporizador si el jugador se queda sin tiempo
                break

        timer_thread.join()

        if juego_terminado:
            break

        fila = encontrar_fila(tablero, columna)
        ficha = 1 if turno == 0 else 2
        soltar_ficha(tablero, fila, columna, ficha)
        ultima_jugada = (fila, columna)

        imprimir_tablero(tablero, ultima_jugada)

        if verificar_ganador(tablero, ficha):
            print(f"\n¡El Jugador {turno + 1} gana! ¡Felicidades!")
            juego_terminado = True
        elif tablero_lleno(tablero):
            print("\n¡El juego termina en empate!")
            juego_terminado = True
        else:
            turno = (turno + 1) % 2  # Cambiar turno

if __name__ == "__main__":
    juego()