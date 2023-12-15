import pygame
import sqlite3
import json

from pygame.locals import *
from Menu_Boton import *
from Player import  *
from Enemy import *
from Objetos import *

# Clase Game
class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Sonic on the Run")
        icono = pygame.image.load("./GUI/LogoSonic vector.png")
        pygame.display.set_icon(icono)
        
        # Conectar a la base de datos SQLite
        self.conn = sqlite3.connect('scores.db')
        self.create_scores_table()

        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.musica_nivel = pygame.mixer.Sound("./Sounds/nivel1.mp3")
        self.running = True
        self.game_won = False
        self.score = 0
        self.current_level = 0
        self.pausa = False
        self.spawn()
        self.run_main_menu()


    def create_scores_table(self):
    # Crear una tabla si no existe
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS scores (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                score INTEGER NOT NULL
            )
        ''')
        self.conn.commit()
    
    def save_score_to_db(self, name):
        # Guardar el nombre y la puntuación en la base de datos SQLite
        cursor = self.conn.cursor()
        cursor.execute('INSERT INTO scores (name, score) VALUES (?, ?)', (name, self.player.score))
        self.conn.commit()


    def spawn(self):
        self.fondo = pygame.transform.scale(pygame.image.load("./Background/paper_texture_green_hill.png"), (WIDTH, HEIGHT))
        self.player_images_run = ["./Run/Run_1.png", "./Run/Run_2.png", "./Run/Run_3.png", "./Run/Run_4.png"]
        self.player_images_jump = ["./Jump/Jump_1.png", "./Jump/Jump_2.png", "./Jump/Jump_3.png"]
        self.player_image_wait = "./Wait/wait_1.png"

        self.ring_images = ["./Ring/Ring1.png", "./Ring/Ring2.png", "./Ring/Ring3.png", "./Ring/Ring4.png"]

        self.enemy_images_run = ["./Enemies/badnick1.png", "./Enemies/badnick2.png", "./Enemies/badnick3.png"]
        self.enemy_width = 100  # Anchura del enemigo
        self.enemy_height = 100  # Altura del enemigo

        # Nivel 1
        self.enemies = [
            Enemy(self.enemy_images_run, (self.enemy_width, self.enemy_height), 400, 100),
            Enemy(self.enemy_images_run, (self.enemy_width, self.enemy_height), 400, 500),
            Enemy(self.enemy_images_run, (self.enemy_width, self.enemy_height), 400, 300)

            
        ]

        self.player = Player(self.player_images_run, self.player_images_jump, self.player_image_wait,"./GUI/Salud.png", 3, (125, 125), 0, 400)

        self.platforms = [
            Plataforma("./Plataforms/Green_hill_plataform.png", 200, 100, 400, 500),
            Plataforma("./Plataforms/Green_hill_plataform.png", 200, 100, 400, 300),
            Plataforma("./Plataforms/Green_hill_plataform.png", 200, 100, 400, 100)
        
        ]

        self.rings = [
            Ring(self.ring_images, (50, 50), 200, 300, self.player),
            Ring(self.ring_images, (50, 50), 550, 300, self.player)
        ]

        self.meta = Meta(["./Goal/goal_ring1.png", "./Goal/goal_ring2.png","./Goal/goal_ring3.png",
                    "./Goal/goal_ring4.png","./Goal/goal_ring5.png", "./Goal/goal_ring6.png",
                    "./Goal/goal_ring7.png"], (100, 100), 700, 300)

        self.players_group = pygame.sprite.Group(self.player)
        self.platforms_group = pygame.sprite.Group(*self.platforms)
        self.enemies_group = pygame.sprite.Group(*self.enemies)
        self.rings_group = pygame.sprite.Group(*self.rings)  # Crear el grupo para los anillos
        self.botones_group = pygame.sprite.Group()
        self.all_sprites = pygame.sprite.Group(self.meta, *self.rings)  # Agregar las instancias de Ring a all_sprites

        self.players_group.add(self.player)  
        self.platforms_group.add(*self.platforms)  # Agregar cada plataforma individualmente
        self.enemies_group.add(*self.enemies)  # Agregar cada enemigo individualmente
        self.rings_group.add(*self.rings)  # Agregar cada anillo individualmente
        self.all_sprites.add(self.meta)

    def spawn2(self):
        self.musica_nivel = pygame.mixer.Sound("./Sounds/Chemical Plant (Classic) - Sonic Generations [OST].mp3")
        self.musica_nivel.play(loops=-1)
        self.fondo = pygame.transform.scale(pygame.image.load("./Background/Chemical_plant_bg.png"), (WIDTH, HEIGHT))
        self.player_images_run = ["./Run/Run_1.png", "./Run/Run_2.png", "./Run/Run_3.png", "./Run/Run_4.png"]
        self.player_images_jump = ["./Jump/Jump_1.png", "./Jump/Jump_2.png", "./Jump/Jump_3.png"]
        self.player_image_wait = "./Wait/wait_1.png"

        self.ring_images = ["./Ring/Ring1.png", "./Ring/Ring2.png", "./Ring/Ring3.png", "./Ring/Ring4.png"]

        self.enemy_images_run = ["./Enemies/badnick1.png", "./Enemies/badnick2.png", "./Enemies/badnick3.png"]
        self.enemy_width = 100  # Anchura del enemigo
        self.enemy_height = 100  # Altura del enemigo
        # Configuración para el siguiente nivel
        
        if self.current_level == 1:
            # Nivel 2
            self.enemies = [
                Enemy(self.enemy_images_run, (self.enemy_width, self.enemy_height), 700, 100),
                Enemy(self.enemy_images_run, (self.enemy_width, self.enemy_height), 700, 400),
                Enemy(self.enemy_images_run, (self.enemy_width, self.enemy_height), 100, 400),
                Enemy(self.enemy_images_run, (self.enemy_width, self.enemy_height), 100, 100)

                
            ]

            self.player.rect.topleft = (500, 500)

            self.platforms = [
                Plataforma("./Plataforms/Plataforma_chemical_plant.png", 300, 100, 600, 400),
                Plataforma("./Plataforms/Plataforma_chemical_plant.png", 300, 100, 600, 100),
                Plataforma("./Plataforms/Plataforma_chemical_plant.png", 200, 100, 100, 400),
                Plataforma("./Plataforms/Plataforma_chemical_plant.png", 200, 100, 100, 100)
            
            ]

            self.rings = [
                Ring(self.ring_images, (50, 50), 100, 550, self.player),
                Ring(self.ring_images, (50, 50), 400, 300, self.player),
                Ring(self.ring_images, (50, 50), 100, 50, self.player)
            ]

            self.meta = Meta(["./Goal/goal_ring1.png", "./Goal/goal_ring2.png","./Goal/goal_ring3.png",
                        "./Goal/goal_ring4.png","./Goal/goal_ring5.png", "./Goal/goal_ring6.png",
                        "./Goal/goal_ring7.png"], (100, 100), 400, 400)

            self.players_group = pygame.sprite.Group(self.player)
            self.platforms_group = pygame.sprite.Group(*self.platforms)
            self.enemies_group = pygame.sprite.Group(*self.enemies)
            self.rings_group = pygame.sprite.Group(*self.rings)  # Crear el grupo para los anillos
            self.botones_group = pygame.sprite.Group()
            self.all_sprites = pygame.sprite.Group(self.meta, *self.rings)  # Agregar las instancias de Ring a all_sprites

            self.players_group.add(self.player)  
            self.platforms_group.add(*self.platforms)  # Agregar cada plataforma individualmente
            self.enemies_group.add(*self.enemies)  # Agregar cada enemigo individualmente
            self.rings_group.add(*self.rings)  # Agregar cada anillo individualmente
            self.all_sprites.add(self.meta)

    def spawn3(self):
        self.musica_nivel = pygame.mixer.Sound("./Sounds/Death Egg Classic - Sonic Generations Remix.mp3")
        self.musica_nivel.play(loops=-1)
        self.fondo = pygame.transform.scale(pygame.image.load("./Background/paper_texture_boss.png"), (WIDTH, HEIGHT))
        self.player_images_run = ["./Run/Run_1.png", "./Run/Run_2.png", "./Run/Run_3.png", "./Run/Run_4.png"]
        self.player_images_jump = ["./Jump/Jump_1.png", "./Jump/Jump_2.png", "./Jump/Jump_3.png"]
        self.player_image_wait = "./Wait/wait_1.png"

        self.ring_images = ["./Ring/Ring1.png", "./Ring/Ring2.png", "./Ring/Ring3.png", "./Ring/Ring4.png"]

        self.enemy_images_run = ["./Enemies/badnick1.png", "./Enemies/badnick2.png", "./Enemies/badnick3.png"]
        self.enemy_width = 100  # Anchura del enemigo
        self.enemy_height = 100  # Altura del enemigo
        
        if self.current_level == 2:
            #Nivel 3
            self.enemies = [
                Enemy(self.enemy_images_run, (self.enemy_width, self.enemy_height), 600, 100),
                Enemy(self.enemy_images_run, (self.enemy_width, self.enemy_height), 600, 400),
                Enemy(self.enemy_images_run, (self.enemy_width, self.enemy_height), 150, 400),
                Enemy(self.enemy_images_run, (self.enemy_width, self.enemy_height), 150, 100)

                
            ]

            self.player.rect.topleft = (500, 500)

            self.platforms = [
                Plataforma("./Plataforms/boss_plataform.png", 500, 100, 400, 400),
                Plataforma("./Plataforms/boss_plataform.png", 500, 100, 400, 100)
        
            ]

            self.rings = [
                Ring(self.ring_images, (50, 50), 400, 550, self.player),
                Ring(self.ring_images, (50, 50), 400, 50, self.player),
                Ring(self.ring_images, (50, 50), 100, 50, self.player),
                Ring(self.ring_images, (50, 50), 700, 50, self.player)
            ]

            self.meta = Meta(["./Goal/goal_ring1.png", "./Goal/goal_ring2.png","./Goal/goal_ring3.png",
                        "./Goal/goal_ring4.png","./Goal/goal_ring5.png", "./Goal/goal_ring6.png",
                        "./Goal/goal_ring7.png"], (100, 100), 400, 300)

            #Creamos los grupos
            self.players_group = pygame.sprite.Group(self.player)
            self.platforms_group = pygame.sprite.Group(*self.platforms)
            self.enemies_group = pygame.sprite.Group(*self.enemies)
            self.rings_group = pygame.sprite.Group(*self.rings)  
            self.botones_group = pygame.sprite.Group()

            #Agregamos a cada objeto al grupo
            self.players_group.add(self.player)  
            self.platforms_group.add(*self.platforms)  
            self.enemies_group.add(*self.enemies)  
            self.rings_group.add(*self.rings) 
            self.all_sprites.add(self.meta)

    
    def run_main_menu(self):
        self.botones_group.empty()
        main_menu = MainMenu(self.screen) 
        main_menu.run(self)
        

    def run_game(self):
        while self.running:
            self.clock.tick(FPS)
            self.handle_events()

            if not self.pausa:
                self.update()
                self.draw()

            keys = pygame.key.get_pressed()
            if keys[K_RETURN]:
                self.toggle_pause()

        self.close()

    #----------------------------PAUSADO------------------------------------
    def toggle_pause(self):
        # Cambia el estado de pausa al contrario
        self.pausa = not self.pausa

        if self.pausa:
            # Muestra la pantalla de pausa
            self.show_pause_screen()
        else:
            # Oculta la pantalla de pausa
            self.hide_pause_screen()

    def show_pause_screen(self):
        # Pantalla de pausa
        pause_font = pygame.font.Font(None, 70)
        pause_text = pause_font.render("Pausa", True, (0, 0, 0))
        pause_rect = pause_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))

        while self.pausa:
            self.handle_events()

            keys = pygame.key.get_pressed()
            if keys[K_r]:
                # Si se presiona la tecla 'r', se reanuda el juego
                self.toggle_pause()

            self.screen.blit(pause_text, pause_rect)
            pygame.display.flip()
            self.clock.tick(FPS)

    def hide_pause_screen(self):
        self.pausa = False


    #----------------------------Ventana de cargar de victoria o siguiente nivel------------------------------------


    def level_completed_screen(self):
        self.level_completed = pygame.mixer.Sound("./Sounds/Sonic 3 Music_ Level Complete.mp3")
        self.level_completed.play()

        # Pantalla de victoria
        
        if self.current_level == 2:
            victory_font = pygame.font.Font(None, 70)
            victory_text = victory_font.render("¡Ganaste!", True, (0, 0, 0))
            victory_rect = victory_text.get_rect(center=(WIDTH // 2, HEIGHT // 4))

            score_font = pygame.font.Font(None, 36)
            score_text = score_font.render(f"Score: {self.player.score}", True, (0, 0, 0))
            score_rect = score_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))

            menu_button = Boton(150, 50, "./GUI/Boton.png", "Menú Principal", 30, WIDTH // 2 - 75, HEIGHT // 2 + 110)

            buttons_group = pygame.sprite.Group(menu_button)

            show_victory_screen = True

            while show_victory_screen:
                self.musica_nivel.stop()
                for event in pygame.event.get():
                    if event.type == QUIT:
                        self.running = False
                        show_victory_screen = False
                    elif event.type == MOUSEBUTTONDOWN:
                        if menu_button.rect.collidepoint(event.pos):
                            # Solicitar al usuario que ingrese su nombre por consola
                            name = input("Ingresa tu nombre de usuario: ")
                            show_victory_screen = False
                            self.save_score_to_db(name)
                            self.save_score(name)
                            self.run_main_menu()
                            return

                self.screen.blit(pygame.image.load("./Background/paper_texture.jpg"), (0, 0))
                self.screen.blit(victory_text, victory_rect)
                self.screen.blit(score_text, score_rect)
                buttons_group.draw(self.screen)  # Dibujar botón
                pygame.display.flip()
                self.clock.tick(FPS)
                
            # Limpiar el grupo de botones después de salir del bucle
            buttons_group.empty()


        # Pantalla de nivel completado
        level_completed_font = pygame.font.Font(None, 70)
        level_completed_text = level_completed_font.render("Nivel Completado", True, (0, 0, 0))
        level_completed_rect = level_completed_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))

        next_level_button = Boton(200, 50, "./GUI/Boton.png", "Siguiente Nivel", 30, WIDTH // 2 - 100, HEIGHT // 2 + 50)

        # Crear un nuevo grupo de botones con el botón de siguiente nivel
        buttons_group = pygame.sprite.Group(next_level_button)

        level_completed = False

        while not level_completed:
            self.players_group.empty()
            self.platforms_group.empty()
            self.enemies_group.empty()
            self.botones_group.empty()
            self.all_sprites.empty()
            self.rings_group.empty()
            self.musica_nivel.stop()
            self.music_nivel1.stop()
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.running = False
                    level_completed = True
                elif event.type == MOUSEBUTTONDOWN:
                    if next_level_button.rect.collidepoint(event.pos):
                        self.level_completed.stop()
                        self.current_level += 1
                        if self.current_level == 1:
                            self.spawn2()  
                        if self.current_level == 2:
                            self.spawn3() 
                        level_completed = True
        
    
            # Dibujar la pantalla de nivel completado
            self.screen.blit(pygame.image.load("./Background/paper_texture.jpg"), (0, 0))
            self.screen.blit(level_completed_text, level_completed_rect)
            buttons_group.draw(self.screen)  # Dibujar botón
            pygame.display.flip()
            self.clock.tick(FPS)

        # Limpiar el grupo de botones después de salir del bucle
        buttons_group.empty()


    #----------------------------Guardado de Score--------------------------------


    def save_score(self, name):
        # Guardar el puntaje en un archivo JSON
        # Cargar el archivo JSON existente
        try:
            with open("scores.json", "r") as file:
                scores = json.load(file)
        except FileNotFoundError:
            scores = []

        # Agregar el puntaje actual al archivo
        scores.append({"name": name, "score": self.player.score})

        # Guardar los puntajes actualizados en el archivo
        with open("scores.json", "w") as file:
            json.dump(scores, file)

    #----------------------------Actualizacion de eventos y mecanica del juego-------------------------------

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                self.running = False
            elif event.type == KEYDOWN:
                if event.key == K_SPACE and self.player.on_ground:
                    self.player.jump()
                elif event.key == K_ESCAPE:
                    self.running = False

        keys = pygame.key.get_pressed()
        self.player.vel_x = (keys[K_RIGHT] - keys[K_LEFT]) * 8

        # Reiniciar invulnerabilidad después de perder una vida
        if not self.player.invulnerable:
            self.player.invulnerable = False

    def update_enemies(self):
        # Eliminar enemigos marcados para eliminación
        self.enemies_group.remove(*[enemy for enemy in self.enemies_group if enemy.should_remove])

        # Actualizar a los enemigos restantes
        for enemy in self.enemies_group.sprites():
            enemy.update(self.platforms_group)
        
        for enemy in self.enemies_group.sprites():
            if enemy.should_remove:
                # Explosion
                explosion = Explosion(["./Enemies/explotion1.png", "./Enemies/explotion2.png", "./Enemies/explotion3.png", "./Enemies/explotion4.png"], (50, 50), enemy.rect.centerx, enemy.rect.centery)
                self.all_sprites.add(explosion)
                enemy.kill()  #Elimina el enemigo

    def update(self):
        on_ground_before = self.player.on_ground
        self.player.on_ground = False

        # Verificar colisiones con plataformas en el eje y
        for platform in pygame.sprite.spritecollide(self.player, self.platforms_group, False):
            if self.player.vel_y >= 0 and 0 < self.player.rect.bottom - platform.rect.top < 10:
                self.player.rect.bottom = platform.rect.top
                self.player.on_ground = True
                self.player.vel_y = 0

        # Verificar colisiones con plataformas en el eje x (nueva lógica)
        self.player.rect.x += self.player.vel_x
        for platform in pygame.sprite.spritecollide(self.player, self.platforms_group, False):
            if self.player.vel_y > 0 and platform.rect.top < self.player.rect.bottom < platform.rect.bottom:
                self.player.rect.bottom = platform.rect.top
                self.player.vel_y = 0
                self.player.on_ground = True

        # Restaurar la posición del jugador si no está en el suelo y no está colisionando con ninguna plataforma
        if not self.player.on_ground:
            self.player.rect.y += 1
            on_ground = False
            for platform in pygame.sprite.spritecollide(self.player, self.platforms_group, False):
                if self.player.vel_y >= 0 and 0 < self.player.rect.bottom - platform.rect.top < 10:
                    on_ground = True
                    self.player.on_ground = True
                    self.player.vel_y = 0
                    break
            if not on_ground:
                self.player.on_ground = False

        # Verificar colisión con el enemigo solo si no está en el período de invulnerabilidad
        if not self.player.is_invulnerable():
            for enemy in pygame.sprite.spritecollide(self.player, self.enemies_group, False):
                if isinstance(enemy, Enemy):
                    if self.player.jump_collision and self.player.rect.bottom < enemy.rect.centery:
                        # Enemigo a ser removido
                        enemy.mark_for_removal()

                        # Crear una explosión en la posición del enemigo eliminado
                        explosion = Explosion(
                            ["./Enemies/explotion1.png", "./Enemies/explotion2.png", "./Enemies/explotion3.png",
                            "./Enemies/explotion4.png"], (50, 50), enemy.rect.centerx, enemy.rect.centery)
                        self.all_sprites.add(explosion)

                    elif not self.player.jump_collision:
                        # Colisión regular en el suelo, aplicar daño
                        self.player.perder_vida()
                        self.player.invulnerable = True
                        self.player.reset_invulnerability()

        
        if not on_ground_before and self.player.on_ground:
            self.player.image_index = 0
            self.player.image = self.player.image_wait
            self.player.jump_collision = False  # Reiniciar la bandera al tocar el suelo

        for ring in pygame.sprite.spritecollide(self.player, self.rings_group, True):
                ring.collect()
        
        if self.player.vidas <= 0:
            self.game_over()

        # Verificar colisión con la meta
        for meta in pygame.sprite.spritecollide(self.player, self.all_sprites, False):
            if isinstance(meta, Meta) and len(self.enemies_group) == 0:
                self.level_completed_screen()

        self.update_enemies()
    
    #--------------------------------Dibujado por pantalla------------------------------

    def draw(self):
        self.screen.blit(self.fondo, (0, 0))
        self.platforms_group.draw(self.screen)
        self.enemies_group.draw(self.screen)
        self.all_sprites.draw(self.screen)
        self.rings_group.draw(self.screen)
        self.players_group.draw(self.screen)
        self.player.draw_lives(self.screen)
        
        # Mostrar el puntaje del jugador en la esquina superior derecha
        score_font = pygame.font.Font(None, 36)
        score_text = score_font.render(f"Score: {self.player.score}", True, (0, 0, 0))
        score_rect = score_text.get_rect(topright=(WIDTH - 10, 10))
        self.screen.blit(score_text, score_rect)

        if self.player.vidas > 0:
            self.botones_group.draw(self.screen)


        self.players_group.update()
        self.rings_group.update()
        self.all_sprites.update()  # Actualizar todas las sprites
        pygame.display.flip()

    #--------------------------------Game Over y Reinicio de partida------------------------

    def game_over(self):
        self.game_over_sound = pygame.mixer.Sound("./Sounds/Sonic 1 Music_ Game Over.mp3")
        game_over_font = pygame.font.Font(None, 70)
        game_over_text = game_over_font.render("GAME OVER", True, (0, 0, 0))
        game_over_rect = game_over_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))

        retry_button = Boton(150, 50, "./GUI/Boton.png", "Reintentar", 30, WIDTH // 2 - 75, HEIGHT // 2 + 50)
        menu_button = Boton(150, 50, "./GUI/Boton.png", "Menú Principal", 30, WIDTH // 2 - 75, HEIGHT // 2 + 110)

        # Crear un nuevo grupo de botones con los botones de reintentar y menú principal
        self.botones_group = pygame.sprite.Group(retry_button, menu_button)
        self.musica_nivel.stop()
        self.music_nivel1.stop()
        self.game_over_sound.play()
        restart_game = False

        while not restart_game:
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.running = False
                    restart_game = True
                elif event.type == MOUSEBUTTONDOWN:
                    if retry_button.rect.collidepoint(event.pos):
                        restart_game = True
                        self.game_over_sound.stop()
                        self.reset_game()

                    elif menu_button.rect.collidepoint(event.pos):
                        # Lógica para volver al menú principal
                        self.game_over_sound.stop()
                        self.musica_nivel.stop()
                        self.run_main_menu()
                        return

            self.screen.blit(pygame.image.load("./Background/paper_texture.jpg"), (0, 0))
            self.screen.blit(game_over_text, game_over_rect)
            self.botones_group.draw(self.screen) 
            pygame.display.flip()
            self.clock.tick(FPS)

        # Eliminar los botones del grupo después de salir del bucle
        self.botones_group.empty()

    def reset_game(self):
        self.music_nivel1 = pygame.mixer.Sound("./Sounds/nivel1.mp3")
        self.music_nivel1.play(loops=-1)
        self.player.vidas = 3
        self.player.lives = 3  # Actualizar correctamente las vidas del jugador
        self.player.rect.topleft = (0, 600)
        self.players_group.empty()
        self.platforms_group.empty()
        self.enemies_group.empty()
        self.botones_group.empty()
        self.all_sprites.empty()
        self.current_level = 0
        self.spawn()

        

    def close(self):
        pygame.quit()



# Configuración de pantalla y otros valores
WIDTH = 800
HEIGHT = 600
FPS = 30

# Crear y ejecutar el juego
game = Game()
game.run_game()
game.close()