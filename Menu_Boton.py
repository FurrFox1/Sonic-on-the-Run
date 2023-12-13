import pygame
from pygame.locals import *
import sys

class MainMenu:
    def __init__(self, screen):
        from Main import WIDTH, HEIGHT
        self.screen = screen
        self.background = pygame.transform.scale(pygame.image.load("./Background/fondo_menu.png"), (WIDTH, HEIGHT))

        self.play_button = Boton(150, 50, "./GUI/Boton.png", "Jugar", 40, WIDTH // 1.5 - 75, HEIGHT // 2 + 50, action="play")
        self.options_button = Boton(160, 50, "./GUI/Boton.png", "Opciones", 40, WIDTH // 1.5 - 75, HEIGHT // 2 + 120, action="options")
        self.quit_button = Boton(150, 50, "./GUI/Boton.png", "Salir", 40, WIDTH // 1.5 - 75 , HEIGHT // 2 + 200, action="quit")
        self.click_sound = pygame.mixer.Sound("./Sounds/Game Menu Select Sound Effect (mp3cut.net).mp3")
        pygame.mixer.music.load("./Sounds/Sonic 3 Music_ Angel Island Zone Act 1.mp3")

        self.buttons_group = pygame.sprite.Group(self.play_button, self.options_button, self.quit_button)

    def run(self, game_instance):
        pygame.mixer.music.play(loops=-1)  # El argumento loops=-1 indica reproducción en bucle
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()

                action = None
                for button in self.buttons_group:
                    action = button.handle_event(event)
                    if action:
                        self.click_sound.play()
                        break

                if action == "play":
                    pygame.mixer.music.stop()
                    game_instance.reset_game()  
                    return

                elif action == "options":
                    opciones_menu = Opciones(self.screen, self)
                    opciones_menu.run()
                    pygame.mixer.music.play(loops=-1)

                elif action == "quit":
                    pygame.quit()
                    sys.exit()

            self.screen.blit(self.background, (0, 0))
            self.buttons_group.draw(self.screen)
            pygame.display.flip()

class Opciones:
    def __init__(self, screen, main_menu):
        from Main import WIDTH, HEIGHT
        self.screen = screen
        self.background = pygame.transform.scale(pygame.image.load("./Background/fondo_menu.png"), (WIDTH, HEIGHT))

        self.musica_button = Boton(150, 50, "./GUI/Boton.png", "Musica", 40, WIDTH // 2 - 75, HEIGHT // 2 + 50, action="toggle_music")
        self.atras_button = Boton(150, 50, "./GUI/Boton.png", "Atras", 40, WIDTH // 2 - 75, HEIGHT // 2 + 120, action="back")

        self.buttons_group = pygame.sprite.Group(self.musica_button, self.atras_button)
        self.main_menu = main_menu

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()

                action = None
                for button in self.buttons_group:
                    action = button.handle_event(event)
                    if action:
                        self.main_menu.click_sound.play()  # Usa el sonido del menú principal
                        break

                if action == "toggle_music":
                    # Lógica para habilitar/deshabilitar la música
                    pygame.mixer.music.set_volume(1 - pygame.mixer.music.get_volume())  # Cambia el volumen
                elif action == "back":
                    return  # Vuelve al menú principal

            self.screen.blit(self.background, (0, 0))
            self.buttons_group.draw(self.screen)
            pygame.display.flip()

class Boton(pygame.sprite.Sprite):
    def __init__(self, width, height, image_path, text, font_size, pos_x, pos_y, action=None):
        super().__init__()

        self.width = width
        self.height = height
        self.image = pygame.transform.scale(pygame.image.load(image_path), (width, height))
        self.rect = self.image.get_rect(topleft=(pos_x, pos_y))
        self.text = text
        self.font_size = font_size
        self.color_text = (0, 0, 0)  # Color blanco por defecto
        self.action = action

        self.font = pygame.font.Font(None, font_size)
        self.render_text()

    def render_text(self):
        # Renderizar el texto en la imagen del botón
        text_surface = self.font.render(self.text, True, self.color_text)
        text_rect = text_surface.get_rect(center=(self.width / 2, self.height / 2))
        self.image.blit(text_surface, text_rect)

    def handle_event(self, event):
        if event.type == MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                if self.action:
                    return self.action
        return None