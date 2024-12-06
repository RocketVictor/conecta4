import numpy as np
import random

# Códigos de color ANSI para resaltar fichas
RESET = "\033[0m"
RED = "\033[31m"  # Rojo
YELLOW = "\033[33m"  # Amarillo
BRIGHT = "\033[1m"  # Negrita

def crear_tablero():
    """Crea un tablero vacío para Conecta 4."""
    return np.zeros((6, 7), dtype=int)

def imprimir_tablero(tablero, ultima_jugada=None):
    """
    Imprime el tablero en un formato visual amigable.
    Destaca la última ficha jugada.
    """
    print("\n  0   1   2   3   4   5   6")
    print(" +---+---+---+---+---+---+---+")
    for fila in range(5, -1, -1):
        fila_str = []
        for col in range(7):
            celda = tablero[fila][col]
            if ultima_jugada and (fila, col) == ultima_jugada:
                # Última ficha jugada resaltada
                ficha = (f"{BRIGHT + RED}X{RESET}" if celda == 1 else 
                         f"{BRIGHT + YELLOW}O{RESET}")
            else:
                ficha = " " if celda == 0 else ("X" if celda == 1 else "O")
            fila_str.append(ficha)
        print(" | " + " | ".join(fila_str) + " |")
        print(" +---+---+---+---+---+---+---+")

def es_valido(tablero, columna):
    """Verifica si se puede jugar en la columna indicada."""
    return columna >= 0 and columna < 7 and tablero[5][columna] == 0

def encontrar_fila(tablero, columna):
    """Encuentra la fila más baja disponible en una columna."""
    for fila in range(6):
        if tablero[fila][columna] == 0:
            return fila

def soltar_ficha(tablero, fila, columna, ficha):
    """Coloca una ficha en el tablero."""
    tablero[fila][columna] = ficha

def verificar_ganador(tablero, ficha):
    """Comprueba si hay un ganador."""
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
    """Verifica si el tablero está lleno."""
    return all(tablero[5][col] != 0 for col in range(7))

def mover_ia(tablero, ficha):
    """Movimiento básico de la IA basado en selección válida."""
    for columna in range(7):
        if es_valido(tablero, columna):
            return columna
    return -1

def juego():
    """Función principal para jugar Conecta 4."""
    tablero = crear_tablero()
    juego_terminado = False
    ultima_jugada = None

    print("\n¡Bienvenidos a Conecta 4!\n")
    imprimir_tablero(tablero)

    modo = input("Selecciona el modo de juego:\n1. Jugador vs Jugador\n2. Jugador vs IA\nTu elección: ")
    vs_ia = modo == "2"

    # Selección aleatoria de quién empieza
    turno = random.choice([0, 1])
    print(f"\nEl jugador que comienza es {'Jugador 1 (X)' if turno == 0 else ('IA (O)' if vs_ia else 'Jugador 2 (O)')}")

    while not juego_terminado:
        if turno == 0:
            print("\nTurno del Jugador 1 (X)")
        else:
            if vs_ia:
                print("\nTurno de la IA (O)")
            else:
                print("\nTurno del Jugador 2 (O)")

        if vs_ia and turno == 1:
            columna = mover_ia(tablero, 2)
        else:
            try:
                columna = int(input("Selecciona una columna (0-6): "))
            except ValueError:
                print("Entrada inválida. Por favor ingresa un número entre 0 y 6.")
                continue

        if not es_valido(tablero, columna):
            print("Movimiento inválido. Intenta de nuevo.")
            continue

        fila = encontrar_fila(tablero, columna)
        ficha = 1 if turno == 0 else 2
        soltar_ficha(tablero, fila, columna, ficha)
        ultima_jugada = (fila, columna)

        imprimir_tablero(tablero, ultima_jugada)

        if verificar_ganador(tablero, ficha):
            if vs_ia and turno == 1:
                print("\n¡La IA gana! ¡Mejor suerte la próxima vez!")
            else:
                print(f"\n¡El Jugador {turno + 1} gana! ¡Felicidades!")
            juego_terminado = True
        elif tablero_lleno(tablero):
            print("\n¡El juego termina en empate! ¡No hay más movimientos!")
            juego_terminado = True
        else:
            turno = (turno + 1) % 2

if __name__ == "__main__":
    juego()
