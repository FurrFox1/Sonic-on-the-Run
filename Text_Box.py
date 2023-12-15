import pygame

class TextBox:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = ""
        self.font = pygame.font.Font(None, 36)
        self.input_rect = pygame.Rect(200, 200, 140, 32)
        self.color = pygame.Color('lightskyblue3')

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            else:
                self.text += event.unicode

    def draw(self, screen):  
        pygame.draw.rect(screen, self.color, self.input_rect, 2)
        self.text_surface = self.font.render(self.text, True, (255, 255, 255))  # Texto blanco
        screen.blit(self.text_surface, (self.input_rect.x + 5, self.rect.y + 5))  # Ajuste de la posición del texto
        self.input_rect.w = self.text_surface.get_width() + 10
