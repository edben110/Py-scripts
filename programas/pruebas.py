import pygame
import random

pygame.init()

# Configuración de pantalla
ANCHO, ALTO = 800, 600
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Mini Beat 'em Up")
clock = pygame.time.Clock()
FPS = 60

# Colores
BLANCO = (255, 255, 255)
ROJO = (255, 0, 0)
AZUL = (0, 128, 255)

# Clase Jugador
class Jugador(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((40, 70))
        self.image.fill(AZUL)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.vel = 5
        self.vida = 100
        self.atacando = False

    def update(self, teclas):
        dx, dy = 0, 0

        if teclas[pygame.K_LEFT]:
            dx = -self.vel
        if teclas[pygame.K_RIGHT]:
            dx = self.vel
        if teclas[pygame.K_UP]:
            dy = -self.vel
        if teclas[pygame.K_DOWN]:
            dy = self.vel

        if teclas[pygame.K_SPACE]:
            self.atacando = True
        else:
            self.atacando = False

        # Movimiento
        self.rect.x += dx
        self.rect.y += dy

        # Limitar al "suelo"
        if self.rect.top < 300:
            self.rect.top = 300
        if self.rect.bottom > ALTO - 50:
            self.rect.bottom = ALTO - 50

# Clase Enemigo
class Enemigo(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((40, 70))
        self.image.fill(ROJO)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.vel = 2
        self.vida = 50

    def update(self, jugador):
        if abs(jugador.rect.centerx - self.rect.centerx) < 300:
            if jugador.rect.centerx > self.rect.centerx:
                self.rect.x += self.vel
            else:
                self.rect.x -= self.vel

            if jugador.rect.centery > self.rect.centery:
                self.rect.y += self.vel
            else:
                self.rect.y -= self.vel

        # Combate simple
        if self.rect.colliderect(jugador.rect):
            if jugador.atacando:
                self.vida -= 1
            else:
                jugador.vida -= 0.5

        if self.vida <= 0:
            self.kill()

# Fondo (más ancho que la pantalla para desplazamiento)
fondo = pygame.Surface((1600, ALTO))
fondo.fill((50, 200, 50))
pygame.draw.rect(fondo, (100, 100, 255), (0, 250, 1600, 200))  # Suelo

# Inicializar jugador y enemigos
jugador = Jugador(100, 400)
enemigos = pygame.sprite.Group()
for i in range(5):
    enemigos.add(Enemigo(random.randint(500, 1500), random.randint(320, 500)))

todos = pygame.sprite.Group(jugador, *enemigos)

# Cámara
desplazamiento = 0

# Bucle principal
corriendo = True
while corriendo:
    clock.tick(FPS)
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            corriendo = False

    teclas = pygame.key.get_pressed()
    jugador.update(teclas)

    # Cámara (scrolling lateral)
    if jugador.rect.centerx - desplazamiento > ANCHO // 2:
        desplazamiento = jugador.rect.centerx - ANCHO // 2

    # Limitar desplazamiento de cámara
    if desplazamiento < 0:
        desplazamiento = 0
    elif desplazamiento > 1600 - ANCHO:
        desplazamiento = 1600 - ANCHO

    for enemigo in enemigos:
        enemigo.update(jugador)

    # Dibujar fondo
    pantalla.blit(fondo, (-desplazamiento, 0))

    # Dibujar sprites
    for sprite in todos:
        pantalla.blit(sprite.image, (sprite.rect.x - desplazamiento, sprite.rect.y))

    # Dibujar vida
    pygame.draw.rect(pantalla, ROJO, (10, 10, jugador.vida * 2, 20))
    pygame.draw.rect(pantalla, (0, 0, 0), (10, 10, 200, 20), 2)

    pygame.display.flip()

pygame.quit()
