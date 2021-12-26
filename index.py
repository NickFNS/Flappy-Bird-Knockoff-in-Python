import pygame, sys, random

from pygame import surface
from pygame.constants import KEYDOWN

def dibujar_piso():
    pantalla.blit(superficie_piso, (posicion_x_piso, 900))
    pantalla.blit(superficie_piso, (posicion_x_piso + 576, 900))

def crear_tubo():
    pos_aleatoria_tubo = random.choice(altura_tubos)
    tubo_arriba = superficie_tubo.get_rect(midtop = (625, pos_aleatoria_tubo))
    tubo_abajo = superficie_tubo.get_rect(midbottom = (625, pos_aleatoria_tubo - 300))
    return tubo_abajo, tubo_arriba

def mover_tubo(tubos):
    for tubo in tubos:
        tubo.centerx -= 5

    return tubos

def dibujar_tubo(tubos):
    for tubo in tubos:
        if tubo.bottom >= 1024:
            pantalla.blit(superficie_tubo, tubo)
        else:
            girar_tubo = pygame.transform.flip(superficie_tubo, False, True)
            pantalla.blit(girar_tubo, tubo)

def revisar_colision(tubos):
    for tubo in tubos:
        if recta_pajaro.colliderect(tubo):
            sonido_muerte.play()
            return False
        
        if recta_pajaro.top <= -100 or recta_pajaro.bottom >= 900:
            sonido_muerte.play()
            return False

    return True

def rotar_pajaro(pajaro):
    nuevo_pajaro = pygame.transform.rotozoom(pajaro, -movimiento_pajaro * 2, 1)
    return nuevo_pajaro

def animacion_pajaro():
    nuevo_pajaro = cuadros_pajaro[index_pajaro]
    recta_nuevo_pajaro = nuevo_pajaro.get_rect(center = (100, recta_pajaro.centery))
    return nuevo_pajaro, recta_nuevo_pajaro

def mostrar_puntaje(estado_juego):
    if estado_juego == "Jugando":
        superficie_puntaje = fuente_juego.render(str(int(puntaje)), True, (255, 255, 255))
        recta_puntaje = superficie_puntaje.get_rect(center = (288, 100))
        pantalla.blit(superficie_puntaje, recta_puntaje)
    if estado_juego == "Game Over":
        superficie_puntaje = fuente_juego.render(f'Puntaje: {(int(puntaje))}', True, (255, 255, 255))
        recta_puntaje = superficie_puntaje.get_rect(center = (288, 100))
        pantalla.blit(superficie_puntaje, recta_puntaje)

        superficie_puntaje_mas_alto = fuente_juego.render(f'Mayor puntaje: {(int(puntaje))}', True, (255, 255, 255))
        recta_puntaje_mas_alto = superficie_puntaje.get_rect(center = (235, 850))
        pantalla.blit(superficie_puntaje_mas_alto, recta_puntaje_mas_alto)

def actualizar_puntaje(puntaje, puntaje_mas_alto):
    if puntaje > puntaje_mas_alto:
        puntaje_mas_alto = puntaje
    return puntaje_mas_alto

pygame.init()
pantalla = pygame.display.set_mode((576, 1024))
clock = pygame.time.Clock()
fuente_juego = pygame.font.Font('04B_19.ttf', 40)

# Variables del juego
gravedad = 0.25
movimiento_pajaro = 0
juego_activo = True
puntaje = 0
puntaje_mas_alto = 0

superficie_fondo = pygame.image.load('sprites/fondo.png').convert()
superficie_fondo = pygame.transform.scale2x(superficie_fondo)

superficie_piso = pygame.image.load('sprites/base.png').convert()
superficie_piso = pygame.transform.scale2x(superficie_piso)
posicion_x_piso = 0

pajaro_alas_bajas = pygame.transform.scale2x(pygame.image.load('sprites/pajaro_alas_abajo.png').convert_alpha())
pajaro_alas_medias = pygame.transform.scale2x(pygame.image.load('sprites/pajaro_alas_medias.png').convert_alpha())
pajaro_alas_altas = pygame.transform.scale2x(pygame.image.load('sprites/pajaro_alas_altas.png').convert_alpha())
cuadros_pajaro = [pajaro_alas_bajas, pajaro_alas_medias, pajaro_alas_altas]
index_pajaro = 0
superficie_pajaro = cuadros_pajaro[index_pajaro]
recta_pajaro = superficie_pajaro.get_rect(center = (100, 512))

ALETEOPAJARO = pygame.USEREVENT + 1
pygame.time.set_timer(ALETEOPAJARO, 200)

superficie_tubo = pygame.image.load('sprites/tubo.png').convert()
superficie_tubo = pygame.transform.scale2x(superficie_tubo)
lista_tubos = []
SPAWNTUBO = pygame.USEREVENT
pygame.time.set_timer(SPAWNTUBO, 1200)
altura_tubos = [400, 600, 800]

superficie_game_over = pygame.transform.scale2x(pygame.image.load('sprites/mensaje.png').convert_alpha())
recta_game_over = superficie_game_over.get_rect(center = (288, 512))

# Efectos de sonido
sonido_aleteo = pygame.mixer.Sound('sonidos/swoosh.wav')
sonido_muerte = pygame.mixer.Sound('sonidos/muerte.wav')
sonido_puntaje = pygame.mixer.Sound('sonidos/punto.wav')
contador_sonido_puntaje = 100

# Bucle principal
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and juego_activo:
                sonido_aleteo.play()
                movimiento_pajaro = 0
                movimiento_pajaro -= 7
            if event.key == pygame.K_SPACE and juego_activo == False:
                juego_activo = True
                recta_pajaro.center = (100, 512)
                lista_tubos.clear()
                movimiento_pajaro = 0
                puntaje = 0
        
        if event.type == SPAWNTUBO:
            lista_tubos.extend(crear_tubo())
        
        if event.type == ALETEOPAJARO:
            if index_pajaro < 2:
                index_pajaro += 1
            else:
                index_pajaro = 0

        superficie_pajaro, recta_pajaro = animacion_pajaro()

    pantalla.blit(superficie_fondo, (0, 0))

    if juego_activo == True:
        # Movimiento del pajaro
        movimiento_pajaro += gravedad
        pajaro_rotacion = rotar_pajaro(superficie_pajaro)
        recta_pajaro.centery += movimiento_pajaro
        pantalla.blit(pajaro_rotacion, recta_pajaro)
        juego_activo = revisar_colision(lista_tubos)

        # Movimiento de los tubos
        lista_tubos = mover_tubo(lista_tubos)
        dibujar_tubo(lista_tubos)
        puntaje += 0.01
        mostrar_puntaje("Jugando")
        contador_sonido_puntaje -= 1
        if contador_sonido_puntaje <= 0:
            sonido_puntaje.play()
            contador_sonido_puntaje = 100
    else:
        pantalla.blit(superficie_game_over, recta_game_over)
        puntaje_mas_alto = actualizar_puntaje(puntaje, puntaje_mas_alto)
        mostrar_puntaje("Game Over")

    # Piso
    posicion_x_piso -= 1
    dibujar_piso()
    if posicion_x_piso <= -576:
        posicion_x_piso = 0

    pygame.display.update()
    clock.tick(60)