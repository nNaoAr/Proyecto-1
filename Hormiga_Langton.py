import pygame
import easygui
import random

# Configuración de usuario
def pedir_configuracion():
    """Descripción: Solicita filas, columnas y tamaño de celda.
Entradas: Ninguna.
Salidas: filas (int), columnas (int), tam_celda (int).
Restricciones: Valores enteros positivos."""

    while True:
        datos = easygui.multenterbox(
            "Configuración inicial",
            "Hormiga de Langton",
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


# Solicitar reglas
def pedir_reglas():
    """Descripción: Solicita la cadena de reglas.
Entradas: Ninguna.
Salidas: reglas (str).
Restricciones: Solo se permiten caracteres R y L."""

    while True:
        reglas = easygui.enterbox("Ingrese la secuencia de reglas.\nEjemplo: RL o RLLR")

        if reglas is None:
            continue

        reglas = reglas.upper()
        valido = True
        for letra in reglas:

            if letra not in "RL":
                valido = False

        if valido and len(reglas) > 0:
            return reglas
        easygui.msgbox("Solo se permiten letras R y L.")


# Crear matriz
def crear_matriz(filas, columnas):
    """Descripción: Crea la matriz del autómata.
Entradas: filas (int), columnas (int).
Salidas: matriz (list).
Restricciones: filas y columnas mayores que 0."""

    matriz = []
    for fila in range(filas):
        nueva_fila = []
        for columna in range(columnas):
            nueva_fila.append(0)

        matriz.append(nueva_fila)
    return matriz


# Crear hormiga
def crear_hormiga(filas, columnas):
    """Descripción: Crea la hormiga en el centro.
Entradas: filas (int), columnas (int).
Salidas: hormiga (dict).
Restricciones: filas y columnas mayores que 0."""

    hormiga = {
        "fila": filas // 2,
        "columna": columnas // 2,
        "direccion": 0}
    return hormiga

#Generar colores
def generar_colores(n):
    """Descripción: Genera una lista de colores RGB.
Entradas: n (int).
Salidas: colores (list).
Restricciones: n mayor que 0."""

    colores = []
    colores.append((255, 255, 255))
    for i in range(n - 1):
        colores.append(
            (random.randint(0, 255), random.randint(0, 255),
                random.randint(0, 255)
            )
        )
    return colores

# Crear ventana
def crear_ventana(filas, columnas, tam_celda):
    """Descripción: Crea la ventana principal.
Entradas: filas (int), columnas (int), tam_celda (int).
Salidas: pantalla (pygame.Surface).
Restricciones: valores positivos."""

    ancho = columnas * tam_celda
    alto = filas * tam_celda
    pantalla = pygame.display.set_mode((ancho, alto))

    pygame.display.set_caption("Hormiga de Langton Generalizada")

    return pantalla


# Girar hormiga
def girar_hormiga(direccion, giro):
    """Descripción: Calcula la nueva dirección.
Entradas: direccion (int), giro (str).
Salidas: nueva_direccion (int).
Restricciones: giro debe ser R o L."""

    if giro == "R":
        return (direccion + 1) % 4
    return (direccion - 1) % 4


# Avanzar hormiga
def avanzar_hormiga(hormiga, filas, columnas):
    """Descripción: Avanza la hormiga una celda.
Entradas: hormiga (dict), filas (int), columnas (int).
Salidas: No retorna valor.
Restricciones: hormiga válida."""

    direccion = hormiga["direccion"]
    if direccion == 0:
        hormiga["fila"] -= 1
    elif direccion == 1:
        hormiga["columna"] += 1
    elif direccion == 2:
        hormiga["fila"] += 1
    else:
        hormiga["columna"] -= 1

    hormiga["fila"] %= filas
    hormiga["columna"] %= columnas


# Siguiente estado
def siguiente(matriz, hormiga, reglas):
    """Descripción: Calcula el siguiente estado del autómata.
Entradas: matriz (list), hormiga (dict), reglas (str).
Salidas: No retorna valor.
Restricciones: La cantidad de estados debe coincidir con la longitud de reglas."""

    fila = hormiga["fila"]
    columna = hormiga["columna"]

    estado = matriz[fila][columna]

    giro = reglas[estado]

    hormiga["direccion"] = girar_hormiga(hormiga["direccion"],giro)

    matriz[fila][columna] = (estado + 1) % len(reglas)

    avanzar_hormiga(hormiga,len(matriz),len(matriz[0]))


# Dibujar matriz
def dibujar_matriz(
    pantalla,
    matriz,
    hormiga,
    colores,
    filas,
    columnas,
    tam_celda
):
    """Descripción: Dibuja la matriz y la hormiga.
Entradas: pantalla, matriz, hormiga, colores.
Salidas: No retorna valor.
Restricciones: Datos válidos."""

    pantalla.fill((255, 255, 255))
    for fila in range(filas):
        for columna in range(columnas):
            estado = matriz[fila][columna]
            color = colores[estado]
            rect = pygame.Rect(
                columna * tam_celda,
                fila * tam_celda,
                tam_celda,
                tam_celda)

            pygame.draw.rect(pantalla,color,rect)
            pygame.draw.rect(pantalla,(200, 200, 200),rect,1)

    rect_hormiga = pygame.Rect(
        hormiga["columna"] * tam_celda,
        hormiga["fila"] * tam_celda,
        tam_celda,
        tam_celda
    )

    pygame.draw.rect(pantalla,(255, 0, 0),rect_hormiga)

    pygame.display.flip()


# Principal
def main():
    """Descripción: Controla la ejecución principal
Entradas: ninguna
Salidas: ninguna
Restricciones: pygame instalado"""

    pygame.init()

    reloj = pygame.time.Clock()
    filas, columnas, tam_celda = pedir_configuracion()
    reglas = pedir_reglas()
    matriz = crear_matriz(filas,columnas)

    hormiga = crear_hormiga(filas,columnas)
    colores = generar_colores(len(reglas))

    pantalla = crear_ventana(filas,columnas,tam_celda)

    ejecutando = True
    pausado = True

    while ejecutando:

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                ejecutando = False

            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE:
                    pausado = not pausado

        if not pausado:

                siguiente(matriz,hormiga,reglas)

        dibujar_matriz(
            pantalla,
            matriz,
            hormiga,
            colores,
            filas,
            columnas,
            tam_celda)

        reloj.tick(1000)

    pygame.quit()


if __name__ == "__main__":
    main()
