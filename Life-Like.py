import pygame
import easygui
import random
import pickle

#Configuración de usuario
def pedir_configuracion():
    """Descripción: Función que solicita al usuario la cantidad de filas,
columnas y el tamaño de las celdas mediante una ventana gráfica.
Entradas: No recibe parámetros.
Salidas: filas (int), columnas (int), tam_celda (int).
Restricciones: Valores numéricos enteros positivos"""

    while True:

        datos = easygui.multenterbox(
            "Configuración inicial",
            "Autómata celular",
            ["Filas", "Columnas", "Tamaño de celda"]
        )

        try:

            filas = int(datos[0])
            columnas = int(datos[1])
            tam_celda = int(datos[2])

            if filas > 0 and columnas > 0 and tam_celda > 0:
                return filas, columnas, tam_celda

        except:
            pass

        easygui.msgbox("Ingrese únicamente números enteros positivos.")

# Configuración de reglas
def pedir_reglas():
    """Descripción: Solicita al usuario las reglas de nacimiento y
supervivencia del autómata Life-Like.
Entradas: No recibe parámetros.
Salidas: nacimiento (str), supervivencia (str).
Restricciones: Deben ingresarse dígitos entre 0 y 8."""

    while True:

        datos = easygui.multenterbox(
            "Reglas Life-Like",
            "Configuración",
            ["Nacimiento (B)", "Supervivencia (S)"]
        )

        nacimiento = datos[0]
        supervivencia = datos[1]

        valido = True

        for caracter in nacimiento + supervivencia:
            if caracter not in "012345678":
                valido = False

        if valido:
            return nacimiento, supervivencia

        easygui.msgbox("Solo se permiten dígitos entre 0 y 8.")

#Creación de matriz
def crear_matriz(filas, columnas):
    """Descripción: Función que crea una matriz bidimensional inicializada
con ceros para representar el estado inicial del autómata celular.
Entradas: filas (int), columnas(int).
Salidas: matriz (list)
Restricciones: filas y columnas deben ser números enteros positivos
mayores que 0"""
    matriz = []
    for i in range(filas):
        fila = []
        for j in range(columnas):
            fila.append(0)
        matriz.append(fila)
    return matriz

#Ventana
def crear_ventana(filas, columnas, tam_celda):
    """Descripción: Función que crea la ventana principal de pygame con
las dimensiones necesarias para mostrar la cuadrícula del autómata celular.
Entradas: filas (int), columnas(int), tam_celda (int).
Salidas: pantalla (pygame.Surface).
Restricciones: filas > 0, columnas > 0, tam_celda > 0, pygame inicializado."""
    ancho = columnas * tam_celda
    alto = filas * tam_celda
    pantalla = pygame.display.set_mode((ancho, alto))
    pygame.display.set_caption("Autómata Celular")
    return pantalla

#Dibujar Matriz
def dibujar_matriz(pantalla, matriz, filas, columnas, tam_celda):
    """Descripción: Función que dibuja en la ventana el estado actual de la
matriz del autómata celular.
Entradas: pantalla (pygame.Surface), matriz (list), filas (int), columnas (int),
tam_celda (int).
Salidas: no retorna ningún valor.
Restricciones: pantalla inicializada, matriz con dimensiones filas x columnas,
tam_celda > 0, estados de las células deben corresponder a valores válidos para
el autómata."""
    pantalla.fill((255, 255, 255))
    for fila in range(filas):
        for columna in range(columnas):
            if matriz[fila][columna] == 1:
                color = (0, 100, 255)
            else:
                color = (255, 255, 255)
            rect = pygame.Rect(
                columna * tam_celda,
                fila * tam_celda,
                tam_celda,
                tam_celda
            )
            pygame.draw.rect(pantalla, color, rect)
            pygame.draw.rect(pantalla, (200, 200, 200), rect, 1)
    pygame.display.flip()

#Cambiar estado de celda
def cambiar_estado_celda(matriz, fila, columna):
    """Descripción: Función que cambia el estado de una célula entre viva y muerta.
Entradas: matriz (list), fila (int), columna (int).
Salidas: No retorna ningún valor.
Restricciones: fila y columna deben existir dentro de la matriz."""
    if matriz[fila][columna] == 0:
        matriz[fila][columna] = 1
    else:
        matriz[fila][columna] = 0

# Reiniciar matriz vacía
def reiniciar_vacio(matriz, filas, columnas):
    """Descripción: Función que reinicia todas las células de la matriz al estado 0.
Entradas: matriz (list), filas (int), columnas (int).
Salidas: no retorna ningún valor.
Restricciones: La matriz debe tener dimensiones filas x columnas."""

    for fila in range(filas):
        for columna in range(columnas):
            matriz[fila][columna] = 0

# Reiniciar matriz aleatoria
def reiniciar_aleatorio(matriz, filas, columnas):
    """Descripción: Función que asigna aleatoriamente el estado 0 o 1 a cada célula de la matriz.
Entradas: matriz (list), filas (int), columnas (int).
Salidas: no retorna ningún valor.
Restricciones: La matriz debe tener dimensiones filas x columnas."""

    for fila in range(filas):
        for columna in range(columnas):
            matriz[fila][columna] = random.randint(0, 1)

# Guardar estado
def guardar_estado(
    matriz,
    filas,
    columnas,
    tam_celda,
    nacimiento,
    supervivencia
):
    """Descripción: Función que guarda la configuración y el estado actual del autómata en un archivo.
Entradas: matriz (list), filas (int), columnas (int), tam_celda (int)
Salidas: No retorna ningún valor.
Restricciones: Los datos deben ser serializables mediante pickle."""

    datos = {
        "filas": filas,
        "columnas": columnas,
        "tam_celda": tam_celda,
        "matriz": matriz,
        "nacimiento": nacimiento,
        "supervivencia": supervivencia
    }

    with open("estado.pkl", "wb") as archivo:
        pickle.dump(datos, archivo)

# Cargar estado
def cargar_estado():
    """Descripción: Función que carga desde un archivo la configuración y el estado del autómata.
Entradas: No recibe parámetros.
Salidas: filas (int), columnas (int), tam_celda (int), matriz (list)
Restricciones: El archivo estado.pkl debe existir y contener datos válidos."""

    try:

        with open("estado.pkl", "rb") as archivo:
            datos = pickle.load(archivo)

        return (
            datos["filas"],
            datos["columnas"],
            datos["tam_celda"],
            datos["matriz"],
            datos["nacimiento"],
            datos["supervivencia"]
        )

    except FileNotFoundError:

        easygui.msgbox("No existe ningún archivo guardado.")

        return None

# Obtener vecinos
def obtener_vecinos(matriz, fila, columna):
    """Descripción: Obtiene los vecinos de una célula utilizando
el vecindario de Moore.
Entradas: matriz (list), fila (int), columna (int)
Salidas: vecinos (list)
Restricciones: fila y columna deben existir dentro de la matriz."""

    vecinos = []
    filas = len(matriz)
    columnas = len(matriz[0])
    for df in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            if df == 0 and dc == 0:
                continue
            nueva_fila = fila + df
            nueva_columna = columna + dc
            if (0 <= nueva_fila < filas and
                0 <= nueva_columna < columnas):
                vecinos.append(
                    matriz[nueva_fila][nueva_columna]
                )
    return vecinos

# Transición de célula
def transicion_celula(estado, vecinos, nacimiento, supervivencia):
    """Descripción: Calcula el nuevo estado de una célula según
las reglas Life-Like.
Entradas: estado (int), vecinos (list), nacimiento (str), supervivencia (str)
Salidas: nuevo_estado (int)
Restricciones:
estado debe ser 0 o 1.
vecinos debe contener estados válidos.
nacimiento y supervivencia deben contener dígitos entre 0 y 8.
"""

    vecinos_vivos = sum(vecinos)
    if estado == 0:
        if str(vecinos_vivos) in nacimiento:
            return 1
        return 0
    else:
        if str(vecinos_vivos) in supervivencia:
            return 1
        return 0

# Transición de matriz
def transicion(matriz, nacimiento, supervivencia):
    """Descripción: Genera una nueva matriz aplicando las reglas
Life-Like a todas las células.
Entradas: matriz (list), nacimiento (str), supervivencia (str)
Salidas: nueva_matriz (list)
Restricciones: La matriz debe contener únicamente estados válidos.
nacimiento y supervivencia deben contener dígitos entre 0 y 8.
"""

    filas = len(matriz)
    columnas = len(matriz[0])

    nueva_matriz = crear_matriz(filas, columnas)

    for fila in range(filas):
        for columna in range(columnas):

            estado = matriz[fila][columna]

            vecinos = obtener_vecinos(matriz,fila,columna)

            nueva_matriz[fila][columna] = transicion_celula(
                estado,
                vecinos,
                nacimiento,
                supervivencia
            )

    return nueva_matriz

#Principal
def main():
    """Descripción: Función que controla la ejecución principal del programa. Inicializa
Pygame, solicita la configuración al usuario, crea la matriz y la ventana, y mantiene el
ciclo principal de ejecución hasta que el usuario cierre la aplicación.
Entradas: no recibe parámetros.
Salidas: no retorna ningún valor.
Restricciones: bibliotecas necesarias instaladas, valores válidos en la configuración,
Pygame inicializado en el sistema."""

    pygame.init()
    reloj = pygame.time.Clock()
    filas, columnas, tam_celda = pedir_configuracion()
    nacimiento, supervivencia = pedir_reglas()
    
    matriz = crear_matriz(filas, columnas)
    
    pantalla = crear_ventana(filas,columnas,tam_celda)
    ejecutando = True
    pausado = True
    while ejecutando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                ejecutando = False
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                columna = x // tam_celda
                fila = y // tam_celda
                cambiar_estado_celda(matriz,fila,columna)
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_b:
                    reiniciar_vacio(matriz, filas,columnas)
                elif evento.key == pygame.K_r:
                    reiniciar_aleatorio(matriz,filas,columnas)
                elif evento.key == pygame.K_g:
                    guardar_estado(
                        matriz,
                        filas,
                        columnas,
                        tam_celda,
                        nacimiento,
                        supervivencia
                    )
                elif evento.key == pygame.K_c:
                    resultado = cargar_estado()
                    if resultado is not None:
                        (filas, columnas, tam_celda,
                            matriz,
                            nacimiento,
                            supervivencia
                        ) = resultado

                        pantalla = crear_ventana(filas, columnas, tam_celda)
                elif evento.key == pygame.K_SPACE:
                    pausado = not pausado

        if not pausado:
            matriz = transicion(matriz, nacimiento, supervivencia)
                    
        dibujar_matriz(pantalla, matriz, filas, columnas, tam_celda)
        reloj.tick(10)
        
    pygame.quit()
if __name__ == "__main__":
    main()
    
