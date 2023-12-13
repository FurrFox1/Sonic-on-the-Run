import pygame
from pygame.locals import *

class Meta(pygame.sprite.Sprite):
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
            self.image_index = (self.image_index + 1) % len(self.images)
            self.image = self.images[self.image_index]

class Plataforma(pygame.sprite.Sprite):
    def __init__(self, image, width, height, pos_x, pos_y):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load(image), (width, height))
        self.rect = self.image.get_rect(midtop=(pos_x, pos_y))


class Ring(pygame.sprite.Sprite):
    def __init__(self, images, size, pos_x, pos_y, player):
        super().__init__()
        self.images = [pygame.transform.scale(pygame.image.load(img), size) for img in images]
        self.image_index = 0
        self.image = self.images[self.image_index]
        self.rect = self.image.get_rect(center=(pos_x, pos_y))
        self.animation_speed = 100  # Milisegundos por fotograma
        self.last_update = pygame.time.get_ticks()
        self.player = player
        self.ring_sound = pygame.mixer.Sound("./Sounds/Sonic Ring - Sound Effect (HD).mp3")

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.animation_speed:
            self.last_update = now
            self.image_index = (self.image_index + 1) % len(self.images)
            self.image = self.images[self.image_index]

        # Verificar colisión con el jugador
        if pygame.sprite.collide_rect(self, self.player):
            self.collect()  # Llama a la función de recoger cuando hay una colisión

    def collect(self):
        self.ring_sound.play()
        self.player.score += 100
        self.kill()  # Elimina el anillo después de ser recogido