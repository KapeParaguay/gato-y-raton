import pygame
import numpy as np
import random

# Dimensiones del tablero
tableroTamanio = 8
tamanioCelda = 100
anchoVentana = tableroTamanio * tamanioCelda
altoVentana = tableroTamanio * tamanioCelda

# Colores
colorFondo = 'yellow'
colorLinea = 'royalblue'

# Inicializamos el tablero
tablero = np.zeros((tableroTamanio, tableroTamanio))

# Posiciones iniciales
gatoPos = (0, tableroTamanio - 1)
ratonPos = (tableroTamanio - 1, 0)

# Definir las posiciones iniciales en el tablero
tablero[gatoPos] = 1  # 1 representa al Gato
tablero[ratonPos] = 2  # 2 representa al Ratón

# Para evitar movimientos repetidos
movimientosPrevios = set()

# Generar destino para el ratón
def generarDestino(ratonPos, minDistancia):
    while True:
        destino = (random.randint(0, tableroTamanio - 1), random.randint(0, tableroTamanio - 1))
        distancia = np.sum(np.abs(np.array(destino) - np.array(ratonPos)))
        if distancia >= minDistancia:
            return destino

destino = generarDestino(ratonPos, 4)

def moverJugador(tablero, posicionActual, nuevaPosicion):
    if (0 <= nuevaPosicion[0] < tableroTamanio) and (0 <= nuevaPosicion[1] < tableroTamanio):
        jugador = tablero[posicionActual]
        tablero[posicionActual] = 0
        tablero[nuevaPosicion] = jugador
        return nuevaPosicion
    else:
        return posicionActual

def evaluar(tablero):
    gatoPos = np.argwhere(tablero == 1)
    ratonPos = np.argwhere(tablero == 2)
    
    if gatoPos.size == 0 or ratonPos.size == 0:
        return 0

    gatoPos = gatoPos[0]
    ratonPos = ratonPos[0]
    distancia = np.sum(np.abs(gatoPos - ratonPos))
    return -distancia  # Queremos minimizar la distancia para el Gato

def minimax(tablero, profundidad, maximizando, movimientosPrevios):
    if profundidad == 0 or juegoTerminado(tablero):
        return evaluar(tablero)
    
    if maximizando:
        mejorValor = -np.inf
        movimientos = generarMovimientos(tablero, 1, movimientosPrevios)
        for movimiento in movimientos:
            valor = minimax(movimiento, profundidad - 1, False, movimientosPrevios)
            mejorValor = max(mejorValor, valor)
        return mejorValor
    else:
        mejorValor = np.inf
        movimientos = generarMovimientos(tablero, 2, movimientosPrevios)
        for movimiento in movimientos:
            valor = minimax(movimiento, profundidad - 1, True, movimientosPrevios)
            mejorValor = min(mejorValor, valor)
        return mejorValor

def generarMovimientos(tablero, jugador, movimientosPrevios):
    movimientos = []
    posicionActual = np.argwhere(tablero == jugador)
    
    if posicionActual.size == 0:
        return movimientos

    posicionActual = posicionActual[0]
    posiblesMovimientos = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (-1, -1)]
    for movimiento in posiblesMovimientos:
        nuevaPosicion = (posicionActual[0] + movimiento[0], posicionActual[1] + movimiento[1])
        if (0 <= nuevaPosicion[0] < tableroTamanio) and (0 <= nuevaPosicion[1] < tableroTamanio):
            nuevoTablero = tablero.copy()
            nuevoTablero[posicionActual[0], posicionActual[1]] = 0
            nuevoTablero[nuevaPosicion[0], nuevaPosicion[1]] = jugador
            # Verificar si el movimiento ya se ha realizado anteriormente
            if tuple(map(tuple, nuevoTablero)) not in movimientosPrevios:
                movimientos.append(nuevoTablero)
    return movimientos

def generarMovimientosRaton(tablero, ratonPos, movimientosPrevios):
    movimientos = []
    posiblesMovimientos = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (-1, -1), (-1, 1), (1, -1)]
    for movimiento in posiblesMovimientos:
        nuevaPosicion = (ratonPos[0] + movimiento[0], ratonPos[1] + movimiento[1])
        if (0 <= nuevaPosicion[0] < tableroTamanio) and (0 <= nuevaPosicion[1] < tableroTamanio):
            nuevoTablero = tablero.copy()
            nuevoTablero[ratonPos[0], ratonPos[1]] = 0
            nuevoTablero[nuevaPosicion[0], nuevaPosicion[1]] = 2
            if tuple(map(tuple, nuevoTablero)) not in movimientosPrevios:
                movimientos.append((nuevoTablero, nuevaPosicion))
    # Ordenar movimientos por la distancia al destino
    movimientos.sort(key=lambda x: np.sum(np.abs(np.array(x[1]) - np.array(destino))))
    return movimientos

def juegoTerminado(tablero):
    gatoPos = np.argwhere(tablero == 1)
    ratonPos = np.argwhere(tablero == 2)
    if gatoPos.size == 0 or ratonPos.size == 0:
        return True
    gatoPos = gatoPos[0]
    ratonPos = ratonPos[0]
    if np.array_equal(gatoPos, ratonPos):
        return True
    if np.array_equal(ratonPos, destino):
        return True
    return False

def dibujarDestino(pantalla, imagenDestino, destino):
    destinoRect = pygame.Rect(destino[1] * tamanioCelda, destino[0] * tamanioCelda, tamanioCelda, tamanioCelda)
    pantalla.blit(imagenDestino, destinoRect.topleft)

def jugar():
    global gatoPos, ratonPos
    turnoGato = True
    profundidad = 3

    # Inicializar pygame
    pygame.init()
    pantalla = pygame.display.set_mode((anchoVentana, altoVentana))
    pygame.display.set_caption("Juego del Gato y el Ratón")
    reloj = pygame.time.Clock()

    # Cargar imágenes GIF y redimensionarlas
    imagenGato = pygame.image.load('static/gato.gif')
    imagenRaton = pygame.image.load('static/raton.gif')
    imagenDestino = pygame.image.load('static/destino.png')
    imagenGato = pygame.transform.scale(imagenGato, (tamanioCelda, tamanioCelda))
    imagenRaton = pygame.transform.scale(imagenRaton, (tamanioCelda, tamanioCelda))
    imagenDestino = pygame.transform.scale(imagenDestino, (tamanioCelda, tamanioCelda))

    corriendo = True
    while corriendo and not juegoTerminado(tablero):
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                corriendo = False

        pantalla.fill(colorFondo)

        # Dibujar el tablero
        for x in range(tableroTamanio):
            for y in range(tableroTamanio):
                rect = pygame.Rect(y * tamanioCelda, x * tamanioCelda, tamanioCelda, tamanioCelda)
                pygame.draw.rect(pantalla, colorLinea, rect, 1)
                if tablero[x, y] == 1:
                    pantalla.blit(imagenGato, rect.topleft)
                elif tablero[x, y] == 2:
                    pantalla.blit(imagenRaton, rect.topleft)
        
        # Dibujar el destino
        dibujarDestino(pantalla, imagenDestino, destino)

        pygame.display.flip()

        if turnoGato:
            mejorValor = -np.inf
            mejorMovimiento = None
            movimientos = generarMovimientos(tablero, 1, movimientosPrevios)
            for movimiento in movimientos:
                valor = minimax(movimiento, profundidad, False, movimientosPrevios)
                if valor > mejorValor:
                    mejorValor = valor
                    mejorMovimiento = movimiento
            if mejorMovimiento is not None:
                movimientosPrevios.add(tuple(map(tuple, mejorMovimiento)))
                tablero[:] = mejorMovimiento
                gatoPos = np.argwhere(tablero == 1)[0]
        else:
            mejorValor = np.inf
            mejorMovimiento = None
            movimientos = generarMovimientosRaton(tablero, ratonPos, movimientosPrevios)
            for movimiento, nuevaPosicion in movimientos:
                valor = minimax(movimiento, profundidad, True, movimientosPrevios)
                if valor < mejorValor:
                    mejorValor = valor
                    mejorMovimiento = movimiento
            if mejorMovimiento is not None:
                movimientosPrevios.add(tuple(map(tuple, mejorMovimiento)))
                tablero[:] = mejorMovimiento
                ratonPos = np.argwhere(tablero == 2)[0]

        turnoGato = not turnoGato
        reloj.tick(2)  # Controla la velocidad del juego

    # Mostrar el resultado final
    pantalla.fill(colorFondo)
    if gatoPos.size == 0 or ratonPos.size == 0:
        mensaje = "Error en la posición de los jugadores."
    else:
        if np.array_equal(ratonPos, destino):
            mensaje = "El Ratón ha alcanzado su destino y ha escapado!"
        else:
            mensaje = "El Gato ha atrapado al Ratón!"
    
    fuente = pygame.font.Font(None, 40)
    texto = fuente.render(mensaje, True, 'royalblue')
    pantalla.blit(texto, (20, altoVentana // 2 - 37))
    pygame.display.flip()

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                return

if __name__ == "__main__":
    jugar()
