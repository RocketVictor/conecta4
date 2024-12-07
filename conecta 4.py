import numpy as np
import random

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
                # Última ficha jugada resaltada
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
    
    for columna in range(7):
        if es_valido(tablero, columna):
            return columna
    return -1

def juego():
    
    tablero = crear_tablero()
    juego_terminado = False
    ultima_jugada = None

    print("\n¡Bienvenidos a Conecta 4!\n")
    imprimir_tablero(tablero)

    modo = input("Selecciona el modo de juego:\n1. Jugador vs Jugador\n2. Jugador vs IA\nTu elección: ")
    contra_bot = modo == "2"

    # Selección aleatoria de quién empieza
    turno = random.choice([0, 1])
    print(f"\nEl jugador que comienza es {'Jugador 1 (X)' if turno == 0 else ('IA (O)' if contra_bot else 'Jugador 2 (O)')}")

    while not juego_terminado:
        if turno == 0:
            print("\nTurno del Jugador 1 (X)")
        else:
            if contra_bot:
                print("\nTurno de la IA (O)")
            else:
                print("\nTurno del Jugador 2 (O)")

        if contra_bot and turno == 1:
            columna = mover_ia(tablero, 2)
        else:
            columna = int(input("Selecciona una columna (0-6): "))
            if columna <0 or columna > 6:
                print("Entrada inválida. Por favor ingresa un número entre 0 y 6.")
        
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
