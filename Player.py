import pygame
from pygame.locals import *

class Player(pygame.sprite.Sprite):
    def __init__(self, images_run, images_jump, image_wait, life_image, initial_lives, size, pos_x, pos_y):
        super().__init__()
        self.images_run = [pygame.transform.scale(pygame.image.load(img), size) for img in images_run]
        self.images_jump = [pygame.transform.scale(pygame.image.load(img), size) for img in images_jump]
        self.image_wait = pygame.transform.scale(pygame.image.load(image_wait), size)
        self.image_index = 0
        self.image = self.image_wait
        self.rect = self.image.get_rect(midbottom=(pos_x, pos_y))
        self.vidas = 3
        self.score = 0
        self.vel_y = 0
        self.vel_x = 0
        self.gravity = 1
        self.on_ground = False
        self.facing_right = True
        self.life_image = pygame.transform.scale(pygame.image.load(life_image), (30, 30))
        self.lives = initial_lives
        self.invulnerable = False
        self.invulnerable_duration = 1000  # Duración de la invulnerabilidad en milisegundos
        self.invulnerable_timer = 0  # Temporizador para gestionar el período de invulnerabilidad
        self.hurt = False
        self.jump_collision = False

        self.jump_sound = pygame.mixer.Sound("./Sounds/Sonic cd jump sound (mp3cut.net).mp3")
        self.damage_sound = pygame.mixer.Sound("./Sounds/Minecraft HitTake Damage Sound Effect (mp3cut.net).mp3")

    def jump(self):
        if self.on_ground:
            self.jump_sound.play()
            self.vel_y = -25
            self.on_ground = False
            self.jump_collision = True  # Marcar que el jugador está en el aire durante un salto

    def draw_lives(self, screen):
        for i in range(self.lives):
            screen.blit(self.life_image, (10 + i * 35, 10))

        # Eliminar la última imagen de corazón si el jugador está fuera de vidas
        if self.vidas <= 0 and self.lives > 0:
            self.lives = 0  # Asegurarse de que las vidas no sean negativas
            screen.fill((0, 0, 0), (10 + (self.lives) * 35, 10, 30, 30))

    def perder_vida(self):
        if not self.hurt:
            self.vidas -= 1
            if self.vidas <= 0:
                print("Game Over")
            else:
                self.hurt = True
                self.damage_sound.play()
                pygame.time.set_timer(pygame.USEREVENT, 2000)
                self.lives -= 1
                self.score -= 50

    def reset_invulnerability(self):
        self.invulnerable = False
        self.invulnerable_timer = pygame.time.get_ticks()  # Reiniciar el temporizador de invulnerabilidad

    def is_invulnerable(self):
        # Verificar si el jugador está en el período de invulnerabilidad
        return self.invulnerable and pygame.time.get_ticks() - self.invulnerable_timer < self.invulnerable_duration


    def update(self):
        from Main import WIDTH, HEIGHT
        self.vel_y += self.gravity
        self.rect.y += self.vel_y
        

        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT
            self.on_ground = True
            self.vel_y = 0

        self.rect.x += self.vel_x

        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > WIDTH:
            self.rect.right = WIDTH

        if self.vel_x != 0 and self.on_ground:
            if self.vel_x > 0:
                self.facing_right = True
            elif self.vel_x < 0:
                self.facing_right = False

            self.image_index = (self.image_index + 1) % len(self.images_run)
            self.image = self.images_run[self.image_index]
        elif not self.on_ground:
            self.image_index = (self.image_index + 1) % len(self.images_jump)
            self.image = self.images_jump[self.image_index]
        else:
            self.image = self.image_wait

        if not self.facing_right:
            self.image = pygame.transform.flip(self.image, True, False)

        if self.hurt:
            if pygame.time.get_ticks() - self.invulnerable_timer >= self.invulnerable_duration:
                self.hurt = False  # Restablecer el estado de golpeado
            else:
                self.image.set_alpha(128)  # Reducir la opacidad del jugador durante la invulnerabilidad
        else:
            self.image.set_alpha(255)  # Restaurar la opacidad del jugador si no está en el período de invulnerabilidad
        
        if not self.on_ground:
            self.jump_collision = True  # El jugador está en el aire
        else:
            self.jump_collision = False  # El jugador está en el suelo