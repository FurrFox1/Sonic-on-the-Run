import pygame
from pygame.locals import *

class Enemy(pygame.sprite.Sprite):
    def __init__(self, images_run, size, pos_x, pos_y):
        super().__init__()
        self.images_run = [pygame.transform.scale(pygame.image.load(img), size) for img in images_run]
        self.image_index = 0
        self.image = self.images_run[self.image_index]
        self.rect = self.image.get_rect(midbottom=(pos_x, pos_y))
        self.vel_x = 2  # Velocidad horizontal del enemigo
        self.vel_y = 0  # Velocidad vertical del enemigo
        self.gravity = 1  # Gravedad del enemigo
        self.facing_right = True
        self.on_platform = False  # Nuevo atributo para rastrear si el enemigo está sobre una plataforma
        self.should_remove = False
        self.explotion_sound = pygame.mixer.Sound("./Sounds/Badnik Defeated (mp3cut.net).mp3")
        self.current_platform = None
        
        

    def mark_for_removal(self):
        self.should_remove = True
        self.explotion_sound.play()

    def handle_horizontal_movement(self, platforms):
        # Mover enemigo horizontalmente solo si está sobre una plataforma
        if self.on_platform:
            self.rect.x += self.vel_x

            # Ajustar posición si el enemigo está fuera de los límites de la plataforma
            current_platform_rect = None
            for platform in pygame.sprite.spritecollide(self, platforms, False):
                if pygame.sprite.collide_rect(self, platform):
                    current_platform_rect = platform.rect
                    break

            if current_platform_rect:
                if self.vel_x > 0:
                    # Movimiento hacia la derecha
                    if self.rect.right > current_platform_rect.right:
                        self.rect.right = current_platform_rect.right
                        self.vel_x = -self.vel_x  # cambiar dirección al llegar al borde derecho
                elif self.vel_x < 0:
                    # Movimiento hacia la izquierda
                    if self.rect.left < current_platform_rect.left:
                        self.rect.left = current_platform_rect.left
                        self.vel_x = -self.vel_x  # cambiar dirección al llegar al borde izquierdo
            


        


    def update(self, platforms):
        from Main import WIDTH, HEIGHT
        self.handle_horizontal_movement(platforms)
        # Verificar colisiones con plataformas en el eje y
        self.rect.y += self.vel_y
        self.handle_platform_collision(platforms, "y")

        # Aplicar gravedad solo si no está sobre una plataforma
        if not self.on_platform:
            self.vel_y += self.gravity

        # Cambiar de dirección y voltear la imagen al llegar al borde
        if self.rect.left < 0 or self.rect.right > WIDTH:
            self.vel_x = -self.vel_x
            self.facing_right = not self.facing_right

        # Actualizar la imagen de la animación
        self.image_index = (self.image_index + 1) % len(self.images_run)
        self.image = pygame.transform.flip(self.images_run[self.image_index], not self.facing_right, False)

        # Mover enemigo horizontalmente solo si está sobre la plataforma
        if self.on_platform:
            self.rect.x += self.vel_x

            # Ajustar posición si el enemigo está fuera de los límites de la plataforma
            platform_rect = platforms.sprites()[0].rect  # asumimos que hay solo una plataforma en el grupo
            if self.rect.left < platform_rect.left:
                self.rect.left = platform_rect.left
                self.vel_x = -self.vel_x  # cambiar dirección al llegar al borde izquierdo
            elif self.rect.right > platform_rect.right:
                self.rect.right = platform_rect.right
                self.vel_x = -self.vel_x  # cambiar dirección al llegar al borde derecho

        # Verificar colisiones con plataformas en el eje x
        self.handle_platform_collision(platforms, "x")

    def handle_platform_collision(self, platforms, axis):
        from Player import Player
        for platform in pygame.sprite.spritecollide(self, platforms, False):
            if axis == "x":
                if self.vel_x > 0:
                    self.rect.right = platform.rect.left
                    self.vel_x = -self.vel_x
                elif self.vel_x < 0:
                    self.rect.left = platform.rect.right
                    self.vel_x = -self.vel_x
            elif axis == "y":
                if self.vel_y > 0:
                    self.rect.bottom = platform.rect.top
                    self.vel_y = 0
                    self.on_platform = True  # El enemigo está sobre la plataforma
                elif self.vel_y < 0:
                    self.rect.top = platform.rect.bottom
                    self.vel_y = 0
                    self.on_platform = False  # El enemigo ya no está sobre la plataforma

        # Marcar para eliminación si colisiona con el jugador
        for player in pygame.sprite.spritecollide(self, platforms, False):
            if isinstance(player, Player) and player.vel_y < 0:
                self.mark_for_removal()
                break

class Explosion(pygame.sprite.Sprite):
    def __init__(self, images, size, pos_x, pos_y):
        super().__init__()
        self.images = [pygame.transform.scale(pygame.image.load(img), size) for img in images]
        self.image_index = 0
        self.image = self.images[self.image_index]
        self.rect = self.image.get_rect(center=(pos_x, pos_y))
        self.animation_speed = 100  # Milisegundos por fotograma
        self.last_update = pygame.time.get_ticks()
        

    def update(self):
        
        now = pygame.time.get_ticks()
        if now - self.last_update > self.animation_speed:
            self.last_update = now
            self.image_index += 1
            if self.image_index >= len(self.images):
                self.kill()  # Elimina el sprite de explosión cuando la animación está completa
            else:
                self.image = self.images[self.image_index]
