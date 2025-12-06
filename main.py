import pygame
import random
import json

def dibujar(posUsuario, manzanas, ventana, rojo, negro, verde, violeta, tamMapa, obstaculos, muros):
    x, y = 0, 0
    rojo_oscuro = (150, 0, 0)
    violeta_oscuro = (80, 0, 150)
    grisOscuro = (40, 40, 40)
    colores = []
    color = 155 // max(1, len(posUsuario))
    for c in range(len(posUsuario)):
        colores.append((0,(c)*color+100,50))

    tamPixel = 600 / tamMapa
    for i in range(tamMapa):
        for e in range(tamMapa):
            if[e, i] in posUsuario:
                pygame.draw.rect(ventana, colores[posUsuario.index([e,i])], (x, y, tamPixel, tamPixel))
            elif [e, i] in manzanas:
                pygame.draw.rect(ventana, rojo, (x, y, tamPixel, tamPixel))
                pygame.draw.rect(ventana, rojo_oscuro, (x, y, tamPixel, tamPixel), 6)
            elif (obstaculos == "<Con Obstáculos>") and ([e, i] in muros):
                pygame.draw.rect(ventana, violeta, (x, y, tamPixel, tamPixel))
                pygame.draw.rect(ventana, violeta_oscuro, (x, y, tamPixel, tamPixel), 6)
            else:
                if (i + e) % 2 == 0:
                    pygame.draw.rect(ventana, negro, (x, y, tamPixel, tamPixel))
                else:
                    pygame.draw.rect(ventana, grisOscuro, (x, y, tamPixel, tamPixel))

            x += tamPixel

        y += tamPixel
        x = 0

def comer_manzana(cabeza,posUsuario,manzanas,manzanasEnvenenadas,tamMapa):
    cabeza += 1
    posUsuario.append(posUsuario[0].copy())
    for posicion in posUsuario:
        if posicion in manzanas:
            manzanas.remove(posicion)
    posicionesPosibles_manzanas = []
    for pos_x in range(tamMapa):
        for pos_y in range(tamMapa):
            posicionesPosibles_manzanas.append([pos_x, pos_y])

    for pos in posUsuario:
        if pos in posicionesPosibles_manzanas:
            posicionesPosibles_manzanas.remove(pos)
    for pos2 in manzanas:
        if pos2 in posicionesPosibles_manzanas:
            posicionesPosibles_manzanas.remove(pos2)
    for pos3 in manzanasEnvenenadas:
        if pos3 in posicionesPosibles_manzanas:
            posicionesPosibles_manzanas.remove(pos3)
    if len(posicionesPosibles_manzanas) > 0:
        manzanaNueva = random.choice(posicionesPosibles_manzanas)
        manzanas.append(manzanaNueva)

    return manzanas, posUsuario, cabeza

def generar_manzanaEnvenenada(tamMapa,posUsuario, manzanas, manzanasEnvenenadas):
    posicionesPosibles_manzanasEnvenenadas = []
    for pos_x in range(tamMapa):
        for pos_y in range(tamMapa):
            posicionesPosibles_manzanasEnvenenadas.append([pos_x, pos_y])
    for pos in posUsuario:
        if pos in posicionesPosibles_manzanasEnvenenadas:
            posicionesPosibles_manzanasEnvenenadas.remove(pos)
    for pos2 in manzanas:
        if pos2 in posicionesPosibles_manzanasEnvenenadas:
            posicionesPosibles_manzanasEnvenenadas.remove(pos2)
    for pos3 in manzanasEnvenenadas:
        if pos3 in posicionesPosibles_manzanasEnvenenadas:
            posicionesPosibles_manzanasEnvenenadas.remove(pos3)
    posNoValidas = []
    for y in range(-2, 3):
        for x in range(-2, 3):
            posNoValidas.append([posUsuario[0][0] + x, posUsuario[0][1] + y])
    for pos4 in posNoValidas:
        if pos4 in posicionesPosibles_manzanasEnvenenadas:
            posicionesPosibles_manzanasEnvenenadas.remove(pos4)

    envenenada = random.choice(posicionesPosibles_manzanasEnvenenadas)
    manzanasEnvenenadas.append(envenenada)

    return manzanasEnvenenadas

def mover(posUsuario, manzanas, cabeza, direccion, tamMapa, obstaculos, manzanasEnvenenadas):

    if cabeza > 0:
        j = cabeza
        while j > 0:
            posUsuario[j] = posUsuario[j - 1].copy()
            j -= 1

    if posUsuario[0] in manzanas:
        manzana, posUsuario, cabeza = comer_manzana(cabeza,posUsuario,manzanas,manzanasEnvenenadas,tamMapa)

        if (obstaculos == "<Con Obstáculos>") and (cabeza % 2 == 0):
            manzanasEnvenenadas = generar_manzanaEnvenenada(tamMapa,posUsuario, manzanas, manzanasEnvenenadas)

    if direccion == "norte":
        posUsuario[0][1] -= 1
    elif direccion == "sur":
        posUsuario[0][1] += 1
    elif direccion == "este":
        posUsuario[0][0] += 1
    elif direccion == "oeste":
        posUsuario[0][0] -= 1

    return posUsuario, cabeza, manzanas, manzanasEnvenenadas


def chocarBorde(posUsuario, corriendo, direccion, tamMapa, obstaculos, muros):
    if posUsuario[0][1] == 0 and direccion == "norte":
        corriendo = False
    elif posUsuario[0][1] == tamMapa - 1 and direccion == "sur":
        corriendo = False
    elif posUsuario[0][0] == tamMapa - 1 and direccion == "este":
        corriendo = False
    elif posUsuario[0][0] == 0 and direccion == "oeste":
        corriendo = False
    elif len(posUsuario) > 1:
        if posUsuario[0] in posUsuario[1:]:
            corriendo = False
    if (obstaculos == "<Con Obstáculos>") and (posUsuario[0] in muros):
        corriendo = False
    if len(posUsuario) == tamMapa ** 2:
        corriendo = False
    return corriendo


def juego(ventana, tamMapa, obstaculos, numManzanas, velocidad):
    font = pygame.font.Font(None, 40)

    rojo = (255, 0, 0)
    negro = (0, 0, 0)
    verde = (0, 255, 0)
    morado = (80, 40, 130)
    violeta = (127, 0, 255)

    reloj = pygame.time.Clock()

    corriendo = True

    posUsuario = []
    posUsuario.append([tamMapa // 2, tamMapa // 2])
    cabeza = len(posUsuario) - 1
    manzanas = [[random.randint(0, tamMapa - 1), random.randint(0, tamMapa - 1)] for z in range(numManzanas)]
    manzanasEnvenenadas = []
    while posUsuario[0] in manzanas:
        manzanas = [[random.randint(0, tamMapa - 1), random.randint(0, tamMapa - 1)] for z in range(numManzanas)]
    direccion = ""

    event_list = []
    while corriendo:

        ventana.fill((100, 100, 100))

        for evento in pygame.event.get():
            if evento.type == pygame.KEYDOWN:
                if len(event_list) < 3:
                    if len(event_list) > 0:
                        if (evento.key == pygame.K_w or evento.key == pygame.K_UP) and event_list[len(event_list)-1] != "sur":
                            event_list.append("norte")

                        if (evento.key == pygame.K_s or evento.key == pygame.K_DOWN) and event_list[len(event_list)-1] != "norte":
                            event_list.append("sur")

                        if (evento.key == pygame.K_d or evento.key == pygame.K_RIGHT) and event_list[len(event_list)-1] != "oeste":
                            event_list.append("este")

                        if (evento.key == pygame.K_a or evento.key == pygame.K_LEFT) and event_list[len(event_list)-1] != "este":
                            event_list.append("oeste")
                    else:
                        if (evento.key == pygame.K_w or evento.key == pygame.K_UP) and direccion != "sur":
                            event_list.append("norte")

                        if (evento.key == pygame.K_s or evento.key == pygame.K_DOWN) and direccion != "norte":
                            event_list.append("sur")

                        if (evento.key == pygame.K_d or evento.key == pygame.K_RIGHT) and direccion != "oeste":
                            event_list.append("este")

                        if (evento.key == pygame.K_a or evento.key == pygame.K_LEFT) and direccion != "este":
                            event_list.append("oeste")

            if evento.type == pygame.QUIT:
                corriendo = False
                return 0

        if len(event_list) > 0:
            direccion = event_list.pop(0)


        dibujar(posUsuario, manzanas, ventana, rojo, negro, verde, violeta, tamMapa, obstaculos, manzanasEnvenenadas)
        corriendo = chocarBorde(posUsuario, corriendo, direccion, tamMapa, obstaculos, manzanasEnvenenadas)
        posUsuario, cabeza, manzanas, manzanasEnvenenadas = mover(posUsuario, manzanas, cabeza, direccion, tamMapa, obstaculos,
                                   manzanasEnvenenadas)

        puntuacion = font.render(f"Manzanas: {len(posUsuario)-1}", True, morado)
        ventana.blit(puntuacion, (400, 40))

        pygame.display.flip()

        reloj.tick(velocidad)
    guardarPartida(tamMapa, obstaculos, numManzanas, velocidad, cabeza)
    return 1


def menu(ventana):
    font = pygame.font.Font(None, 40)
    gris = (100, 100, 100)
    rojo = (255, 0, 0)
    negro = (0, 0, 0)
    verde = (0, 255, 0)
    morado = (80, 40, 130)
    morado_claro = (105, 60, 160)

    reloj = pygame.time.Clock()
    corriendo = True
    elegir_tam = {"<Pequeño>":10, "<Mediano>":15, "<Grande>":20}
    elegir = "<Pequeño>"
    obstaculos = "<Sin Obstaculos>"
    seleccionado = 1
    elegirManzanas = 1
    velocidades = {"Lento":5, "Medio":7, "Rapido":9}
    velocidad = "Medio"
    while corriendo:

        ventana.fill(negro)

        for evento in pygame.event.get():
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RETURN and seleccionado == 1:
                    corriendo = False
                    return 1, elegir_tam[elegir], obstaculos, elegirManzanas, velocidades[velocidad]

                if evento.key == pygame.K_RETURN and seleccionado == 6:
                    corriendo = False
                    return 2, elegir_tam[elegir], obstaculos, elegirManzanas, velocidades[velocidad]
                if (evento.key == pygame.K_d or evento.key == pygame.K_RIGHT) and seleccionado == 2:
                    if elegir == "<Pequeño>":
                        elegir = "<Mediano>"
                    elif elegir == "<Mediano>":
                        elegir = "<Grande>"
                    else:
                        elegir = "<Pequeño>"

                if (evento.key == pygame.K_a or evento.key == pygame.K_LEFT) and seleccionado == 2:
                    if elegir == "<Pequeño>":
                        elegir = "<Grande>"
                    elif elegir == "<Mediano>":
                        elegir = "<Pequeño>"
                    else:
                        elegir = "<Mediano>"

                if evento.key in (pygame.K_LEFT, pygame.K_RIGHT, pygame.K_a, pygame.K_d) and seleccionado == 3:
                    if obstaculos == "<Con Obstaculos>":
                        obstaculos = "<Sin Obstaculos>"
                    else:
                        obstaculos = "<Con Obstaculos>"

                if (evento.key == pygame.K_a or evento.key == pygame.K_LEFT) and seleccionado == 4:
                    if elegirManzanas == 1:
                        elegirManzanas = 5
                    elif elegirManzanas == 5:
                        elegirManzanas = 3
                    else:
                        elegirManzanas = 1
                if (evento.key == pygame.K_d or evento.key == pygame.K_RIGHT) and seleccionado == 4:
                    if elegirManzanas == 1:
                        elegirManzanas = 3
                    elif elegirManzanas == 3:
                        elegirManzanas = 5
                    else:
                        elegirManzanas = 1

                if (evento.key == pygame.K_d or evento.key == pygame.K_RIGHT) and seleccionado == 5:
                    if velocidad == "Medio":
                        velocidad = "Rapido"
                    elif velocidad == "Rapido":
                        velocidad = "Lento"
                    else:
                        velocidad = "Medio"
                if (evento.key == pygame.K_a or evento.key == pygame.K_LEFT) and seleccionado == 5:
                    if velocidad == "Medio":
                        velocidad = "Lento"
                    elif velocidad == "Lento":
                        velocidad = "Rapido"
                    else:
                        velocidad = "Medio"

                if evento.key in (pygame.K_UP, pygame.K_w):
                    if seleccionado > 1:
                        seleccionado -= 1
                    else:
                        seleccionado = 6
                if evento.key in (pygame.K_DOWN, pygame.K_s):
                    if seleccionado < 6:
                        seleccionado += 1
                    else:
                        seleccionado = 1

            if evento.type == pygame.QUIT:
                corriendo = False

        jugar = "JUGAR"
        salir = "SALIR"

        if seleccionado == 1:
            texto_jugar = font.render(jugar, True, morado_claro)
        else:
            texto_jugar = font.render(jugar, True, morado)

        if seleccionado == 2:
            texto_elegir_tam = font.render(elegir, True, morado_claro)
        else:
            texto_elegir_tam = font.render(elegir, True, morado)

        if seleccionado == 3:
            texto_elegir_obst = font.render(obstaculos, True, morado_claro)
        else:
            texto_elegir_obst = font.render(obstaculos, True, morado)


        if seleccionado == 4:
            texto_Manzanas = font.render(f"Manzanas: {elegirManzanas}", True, morado_claro)
        else:
            texto_Manzanas = font.render(f"Manzanas: {elegirManzanas}", True, morado)

        if seleccionado == 5:
            texto_Velocidad = font.render(f"Velocidad: {velocidad}", True, morado_claro)
        else:
            texto_Velocidad = font.render(f"Velocidad: {velocidad}", True, morado)

        if seleccionado == 6:
            texto_salir = font.render(salir, True, morado_claro)
        else:
            texto_salir = font.render(salir, True, morado)

        snake = font.render("Snake", True, verde)
        ventana.blit(snake, (260, 20))
        ventana.blit(texto_jugar, (250, 200))
        ventana.blit(texto_Velocidad, (180, 400))
        ventana.blit(texto_salir, (250, 450))
        ventana.blit(texto_Manzanas, (220, 350))
        ventana.blit(texto_elegir_tam, (230, 250))
        ventana.blit(texto_elegir_obst, (180, 300))

        pygame.display.flip()
        reloj.tick(60)


def perder(ventana,tamMapa, obstaculos, numManzanas, velocidad):
    font = pygame.font.Font(None, 40)

    clave = f"{tamMapa}:{obstaculos}:{numManzanas}:{velocidad}"

    negro = (0, 0, 0)
    verde = (0, 255, 0)
    morado = (80, 40, 130)

    reloj = pygame.time.Clock()

    corriendo = True

    while corriendo:

        ventana.fill(negro)

        for evento in pygame.event.get():
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RETURN:
                    corriendo = False
                    return 1
            if evento.type == pygame.QUIT:
                corriendo = False
                return 0
        partidas, record, manzana = leer_cositas(clave)
        if manzana == (tamMapa ** 2):
            perder = "Has ganado!!!"
        else:
            perder = "Has perdido"
        jugar = "Dale a enter para volver al menu"
        par = "Partidas jugadas: " + str(partidas)
        rec = "Record personal: " + str(record)
        manza = "Manzanas comidas: " + str(manzana)
        mapas = {10:"Pequeño",15:"Mediano",20:"grande"}
        veloz = {5:"Lento", 7:"Medio",9:"Rapido"}

        modo1 = f"Mapa:{mapas[tamMapa]} {obstaculos}"
        modo2 = f"Manzanas:{numManzanas} Velocidad:{veloz[velocidad]}"
        modo_juego1 = font.render(modo1, True, verde)
        modo_juego2 = font.render(modo2, True, verde)
        texto = font.render(perder, True, morado)
        texto2 = font.render(jugar, True, morado)
        texto3 = font.render(par, True, verde)
        texto4 = font.render(manza, True, verde)
        texto5 = font.render(rec, True, verde)
        ventana.blit(modo_juego1, (80, 210))
        ventana.blit(modo_juego2, (80, 240))
        ventana.blit(texto, (210, 20))
        ventana.blit(texto2, (90, 150))
        ventana.blit(texto3, (160, 280))
        ventana.blit(texto4, (160, 310))
        ventana.blit(texto5, (160, 340))

        pygame.display.flip()
        reloj.tick(60)

def guardarPartida(tamMapa, obstaculos, numManzanas, velocidad, manzanas_comidas):
    clave = f"{tamMapa}:{obstaculos}:{numManzanas}:{velocidad}"
    try:
        with open("estadisticas.json", "r") as f:
            estadisticas = json.load(f)

            if clave in estadisticas:
                record = estadisticas[clave][2]
                if manzanas_comidas > record:
                    record = manzanas_comidas
                estadisticas[clave] = [estadisticas[clave][0]+1, manzanas_comidas, record]
            else:
                estadisticas.update({clave:[1,manzanas_comidas,manzanas_comidas]})

            with open("estadisticas.json", "w") as f:
                json.dump(estadisticas, f, indent=4)

    except FileNotFoundError:
        with open("estadisticas.json", "w") as f:
            estadisticas = {clave:[1,manzanas_comidas,manzanas_comidas]}
            json.dump(estadisticas, f, indent=4)


def leer_cositas(clave):
    with open("estadisticas.json", "r") as f:
        estadisticas = json.load(f)
        partidas = estadisticas[clave][0]
        record = estadisticas[clave][2]
        manza = estadisticas[clave][1]
        return partidas, record, manza


def main():
    pygame.init()
    ANCHO, ALTO = 600, 600
    ventana = pygame.display.set_mode((ANCHO, ALTO))
    pygame.display.set_caption("Pygame Snake")

    opcion = 1
    while opcion == 1:
        opcion, elegir, obstaculos, elegirManzanas, velocidad = menu(ventana)
        if opcion == 1:
            opcion = juego(ventana, elegir, obstaculos, elegirManzanas, velocidad)
            if opcion == 1:
                opcion = perder(ventana,elegir,obstaculos, elegirManzanas, velocidad)

    pygame.quit()
main()