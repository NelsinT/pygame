import pygame
import sys
import pandas as pd
import os
import time
import random

pygame.init()
pygame.mixer.init()  # musica fundo


screen_width, screen_height = 800, 600
fullscreen = False
screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)
pygame.display.set_caption("Stellar Conquest")
game_state = "menu"


font = pygame.font.SysFont("Arial", 50, bold=True)
small_font = pygame.font.SysFont("Arial", 30)
button_spacing = 40
button_text_color = (232, 60, 126)
button_hover_color = (255, 105, 180)
shadow_color = (150, 30, 90)

# path das imagens
image_path = r"imagens\homescreen.png"
icon_path = r"imagens\icon.png"
music_path = r"soundtrack\background_music.mp3"
single_player_image_path = r"imagens\single_player.png"
player_image_path = r"imagens\player.png"
enemy_image_path = r"imagens\enemy.png"
config_path = "config.csv"

#variaveis (:
rocket_position = [screen_width // 10, screen_height // 10]
rocket_speed = 5
bullets = []
bullet_width, bullet_height = 5, 10
bullet_speed = 10
bullet_color = (255, 255, 0)
shoot_cooldown = 0.5
last_shot_time = 0
enemy_kills = 0
credits = 0
last_spawn_time = 0
enemies = []
enemy_speed = 3


def load_config():
    if os.path.exists(config_path):
        df = pd.read_csv(config_path)
        config = df.iloc[0].to_dict()
        if "fullscreen" not in config:
            config["fullscreen"] = False
        if "volume" not in config:
            config["volume"] = 0.1
        return config
    else:
        default_config = {"volume": 0.1, "fullscreen": False}
        save_config(default_config)
        return default_config


def shoot_bullet():
    global last_shot_time
    current_time = time.time()
    if current_time - last_shot_time >= shoot_cooldown:
        bullet_x = rocket_position[0] + player_width // 2 - bullet_width // 2
        bullet_y = rocket_position[1]
        bullets.append({"x": bullet_x, "y": bullet_y})
        last_shot_time = current_time


def pause_menu():
    global game_state, scaled_background, screen_width, screen_height, screen

    background_snapshot = screen.copy()

    while game_state == "pause_menu":
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                game_state = "single_player"
                return

            elif event.type == pygame.VIDEORESIZE:
                screen
                screen_width, screen_height = event.w, event.h
                screen = pygame.display.set_mode(
                    (screen_width, screen_height), pygame.RESIZABLE
                )
                scaled_background = scale_background()
                background_snapshot = pygame.transform.scale(
                    background_snapshot, (screen_width, screen_height)
                )

        screen.blit(scaled_background, (0, 0))

        for enemy in enemies:
            screen.blit(enemy_image, (enemy["x"], enemy["y"]))
            if enemy["show_health_bar"]:
                draw_health_bar(enemy)

        for bullet in bullets:
            pygame.draw.rect(
                screen,
                bullet_color,
                (bullet["x"], bullet["y"], bullet_width, bullet_height),
            )

        draw_enemy_kills()
        draw_credits()
        overlay = pygame.Surface((screen_width, screen_height))
        overlay.set_alpha(128)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))

        draw_text_button(
            screen,
            "PAUSA",
            (screen_width // 2, screen_height // 2 - 150),
            font,
            (255, 255, 255),
            button_hover_color,
            shadow_color,
        )


        resume_pos = (screen_width // 2, screen_height // 2 - 50)
        restart_pos = (screen_width // 2, screen_height // 2)
        menu_pos = (screen_width // 2, screen_height // 2 + 50)

        screen.blit(player_image, rocket_position)

        if draw_text_button(
            screen,
            "Retomar",
            resume_pos,
            small_font,
            button_text_color,
            button_hover_color,
            shadow_color,
        ):
            game_state = "single_player"
            return

        if draw_text_button(
            screen,
            "Reiniciar",
            restart_pos,
            small_font,
            button_text_color,
            button_hover_color,
            shadow_color,
        ):
            restart_game()
            game_state = "single_player"
            return

        if draw_text_button(
            screen,
            "Menu Principal",
            menu_pos,
            small_font,
            button_text_color,
            button_hover_color,
            shadow_color,
        ):
            restart_game()
            game_state = "menu"
            return

        pygame.display.flip()

def play_options_screen():
    global running, screen, fullscreen, screen_width, screen_height, scaled_background, game_state
    single_player_scaled = pygame.transform.scale(single_player_image, (300, 300))  # Tamanho inicial da imagem do botão

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:  
                    return
                elif event.key == pygame.K_F11:  
                    fullscreen = not fullscreen
                    if fullscreen:
                        screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
                        screen_width, screen_height = screen.get_size()
                    else:
                        screen_width, screen_height = 800, 600
                        screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)
                    scaled_background = scale_background()

            elif event.type == pygame.VIDEORESIZE and not fullscreen:
                screen_width, screen_height = event.w, event.h
                screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)
                scaled_background = scale_background()
                single_player_scaled = pygame.transform.scale(single_player_image, (screen_width // 4, screen_width // 4))

        screen.blit(scaled_background, (0, 0))

        button_spacing = screen_width / 2  
        single_pos = (screen_width // 2 - button_spacing // 1.8, screen_height // 2)
        multi_pos_left = (screen_width // 2 + button_spacing // 2 - 50, screen_height // 2) 
        multi_pos_right = (screen_width // 2 + button_spacing // 2 + 150, screen_height // 2)  

      
        single_rect = single_player_scaled.get_rect(center=single_pos)

       
        multi_rect_left = single_player_scaled.get_rect(center=multi_pos_left)
        multi_rect_right = single_player_scaled.get_rect(center=multi_pos_right)

        screen.blit(single_player_scaled, single_rect.topleft)  
        screen.blit(single_player_scaled, multi_rect_left.topleft)  
        screen.blit(single_player_scaled, multi_rect_right.topleft)  

        single_text_pos = (single_rect.centerx, single_rect.bottom + 30)
        multi_text_pos = (multi_rect_left.centerx + 150, multi_rect_left.bottom + 30)  

        draw_text_button(screen, "Single Player", single_text_pos, small_font, (255, 255, 255), (180, 180, 180), shadow_color)
        draw_text_button(screen, "Multiplayer", multi_text_pos, small_font, (255, 255, 255), (180, 180, 180), shadow_color)

        # Verifica clique nos botões
        mouse_pos = pygame.mouse.get_pos()
        if single_rect.collidepoint(mouse_pos) and pygame.mouse.get_pressed()[0]:
            print("Single Player selecionado!")
            game_state = "single_player" 
            return
        if (multi_rect_left.collidepoint(mouse_pos) or multi_rect_right.collidepoint(mouse_pos)) and pygame.mouse.get_pressed()[0]:
            print("Multiplayer selecionado!")
            game_state = "menu"
        pygame.display.flip()

def draw_health_bar(enemy):
    max_health = 3
    bar_width = 50
    bar_height = 5
    health_percentage = enemy["health"] / max_health
    current_bar_width = int(bar_width * health_percentage)
    bar_x = enemy["x"] + (enemy_width // 2) - (bar_width // 2)
    bar_y = enemy["y"] - 10

    pygame.draw.rect(screen, (255, 0, 0), (bar_x, bar_y, bar_width, bar_height))
    pygame.draw.rect(screen, (0, 255, 0), (bar_x, bar_y, current_bar_width, bar_height))


def restart_game():
    global rocket_position, bullets, enemies, last_shot_time, last_spawn_time, enemy_kills, credits
    rocket_position = [screen_width // 10, screen_height // 10]
    bullets = []
    enemies = []
    last_shot_time = 0
    last_spawn_time = 0
    enemy_kills = 0
    credits = 0


def save_config(config):
    df = pd.DataFrame([config])
    df.to_csv(config_path, index=False)


config = load_config()
volume = config["volume"]
fullscreen = config["fullscreen"]


def spawn_enemy():
    enemy_x = random.randint(0, screen_width - enemy_width)
    enemy_y = -enemy_height
    enemies.append({"x": enemy_x, "y": enemy_y, "health": 3, "show_health_bar": False})


try:
    single_player_image = pygame.image.load(single_player_image_path)
except pygame.error as e:
    print(f"Erro ao carregar imagens dos botões: {e}")
    pygame.quit()
    sys.exit()

try:

    enemy_image_path = pygame.image.load(enemy_image_path)
    enemy_size = (80, 80)
    enemy_image = pygame.transform.scale(enemy_image_path, enemy_size)
    enemy_width, enemy_height = enemy_image.get_size()
except pygame.error as e:
    print(f"Erro ao carregar a imagem do inimigo: {e}")
    pygame.quit()
    sys.exit()

try:

    player_image = pygame.image.load(player_image_path)
    new_player_size = (100, 100)
    player_image = pygame.transform.scale(player_image, new_player_size)
    player_width, player_height = player_image.get_size()
except pygame.error as e:
    print(f"Erro ao carregar a imagem do player: {e}")
    pygame.quit()
    sys.exit()
    sys.exit()

try:
    homescreen_image = pygame.image.load(image_path)
except pygame.error as e:
    print(f"Erro ao carregar a imagem: {e}")
    pygame.quit()
    sys.exit()

if fullscreen:
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    screen_width, screen_height = screen.get_size()
else:
    screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)


def scale_background():
    return pygame.transform.scale(homescreen_image, (screen_width, screen_height))


scaled_background = scale_background()

try:
    icon_image = pygame.image.load(icon_path)
    pygame.display.set_icon(icon_image)
except pygame.error as e:
    print(f"Erro ao carregar a imagem do ícone: {e}")
    pygame.quit()
    sys.exit()

try:
    single_player_image = pygame.image.load(single_player_image_path)
    rocket_width, rocket_height = single_player_image.get_size()
except pygame.error as e:
    print(f"Erro ao carregar a imagem do foguete: {e}")
    pygame.quit()
    sys.exit()

try:
    pygame.mixer.music.load(music_path)
    pygame.mixer.music.set_volume(volume)
    pygame.mixer.music.play(-1)
except pygame.error as e:
    print(f"Erro ao carregar a música: {e}")
    pygame.quit()
    sys.exit()


def draw_text_button(
    screen, text, position, font, base_color, hover_color, shadow_color
):
    mouse_pos = pygame.mouse.get_pos()
    text_surface = font.render(text, True, base_color)
    text_rect = text_surface.get_rect(center=position)
    is_hovered = text_rect.collidepoint(mouse_pos)
    color = hover_color if is_hovered else base_color
    text_surface = font.render(text, True, color)
    shadow_surface = font.render(text, True, shadow_color)
    shadow_rect = shadow_surface.get_rect(center=(position[0] + 2, position[1] + 2))
    screen.blit(shadow_surface, shadow_rect)
    screen.blit(text_surface, text_rect)
    return is_hovered and pygame.mouse.get_pressed()[0]


def play_options_screen():
    global running, screen, fullscreen, screen_width, screen_height, scaled_background, game_state
    single_player_scaled = pygame.transform.scale(single_player_image, (300, 300))

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return
                elif event.key == pygame.K_F11:
                    fullscreen = not fullscreen
                    if fullscreen:
                        screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
                        screen_width, screen_height = screen.get_size()
                    else:
                        screen_width, screen_height = 800, 600
                        screen = pygame.display.set_mode(
                            (screen_width, screen_height), pygame.RESIZABLE
                        )
                    scaled_background = scale_background()
            elif event.type == pygame.VIDEORESIZE and not fullscreen:
                screen_width, screen_height = event.w, event.h
                screen = pygame.display.set_mode(
                    (screen_width, screen_height), pygame.RESIZABLE
                )
                scaled_background = scale_background()

                new_player_size = (screen_width // 12, screen_height // 12)
                player_image = pygame.transform.scale(
                    pygame.image.load(player_image_path), new_player_size
                )
                player_width, player_height = player_image.get_size()

        screen.blit(scaled_background, (0, 0))

        button_spacing = screen_width / 2
        single_pos = (screen_width // 2 - button_spacing // 1.8, screen_height // 2)
        multi_pos_left = (
            screen_width // 2 + button_spacing // 2 - 50,
            screen_height // 2,
        )
        multi_pos_right = (
            screen_width // 2 + button_spacing // 2 + 150,
            screen_height // 2,
        )

        single_rect = single_player_scaled.get_rect(center=single_pos)

        multi_rect_left = single_player_scaled.get_rect(center=multi_pos_left)
        multi_rect_right = single_player_scaled.get_rect(center=multi_pos_right)

        screen.blit(single_player_scaled, single_rect.topleft)
        screen.blit(single_player_scaled, multi_rect_left.topleft)
        screen.blit(single_player_scaled, multi_rect_right.topleft)

        single_text_pos = (single_rect.centerx, single_rect.bottom + 30)
        multi_text_pos = (multi_rect_left.centerx + 150, multi_rect_left.bottom + 30)

        draw_text_button(
            screen,
            "Single Player",
            single_text_pos,
            small_font,
            (255, 255, 255),
            (180, 180, 180),
            shadow_color,
        )
        draw_text_button(
            screen,
            "Multiplayer",
            multi_text_pos,
            small_font,
            (255, 255, 255),
            (180, 180, 180),
            shadow_color,
        )

        mouse_pos = pygame.mouse.get_pos()
        if single_rect.collidepoint(mouse_pos) and pygame.mouse.get_pressed()[0]:
            print("Single Player selecionado!")
            game_state = "single_player"
            return
        if (
            multi_rect_left.collidepoint(mouse_pos)
            or multi_rect_right.collidepoint(mouse_pos)
        ) and pygame.mouse.get_pressed()[0]:
            print("Multiplayer selecionado!")
            game_state = "menu"
        pygame.display.flip()


def options_menu():
    global fullscreen, volume, screen_width, screen_height, screen, scaled_background
    running = True
    slider_width = 200

    slider_x = (screen_width // 2 - slider_width // 2) + int(volume * slider_width)
    dragging = False

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
            elif event.type == pygame.VIDEORESIZE and not fullscreen:
                screen_width, screen_height = event.w, event.h
                screen = pygame.display.set_mode(
                    (screen_width, screen_height), pygame.RESIZABLE
                )

                scaled_background = scale_background()

                slider_x = (screen_width // 2 - slider_width // 2) + int(
                    volume * slider_width
                )
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if slider_rect.collidepoint(pygame.mouse.get_pos()):
                    dragging = True
                elif toggle_rect.collidepoint(pygame.mouse.get_pos()):
                    fullscreen = not fullscreen
                    if fullscreen:
                        screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
                        screen_width, screen_height = screen.get_size()
                    else:
                        screen_width, screen_height = 800, 600
                        screen = pygame.display.set_mode(
                            (screen_width, screen_height), pygame.RESIZABLE
                        )

                    scaled_background = scale_background()
                    slider_x = (screen_width // 2 - slider_width // 2) + int(
                        volume * slider_width
                    )
            elif event.type == pygame.MOUSEBUTTONUP:
                dragging = False
            elif event.type == pygame.MOUSEMOTION and dragging:
                slider_x = pygame.mouse.get_pos()[0]
                slider_x = max(
                    slider_rect.x, min(slider_x, slider_rect.x + slider_width)
                )
                volume = (slider_x - slider_rect.x) / slider_width
                pygame.mixer.music.set_volume(volume)

        screen.blit(scaled_background, (0, 0))

        center_x = screen_width // 2
        center_y = screen_height // 2

        toggle_text = "Fullscreen: ON" if fullscreen else "Fullscreen: OFF"
        toggle_rect = pygame.Rect(center_x - 100, center_y - 120, 200, 50)
        draw_text_button(
            screen,
            toggle_text,
            toggle_rect.center,
            small_font,
            (255, 255, 255),
            (180, 180, 180),
            shadow_color,
        )

        draw_text_button(
            screen,
            "Volume:",
            (center_x, center_y - 30),
            small_font,
            (255, 255, 255),
            (180, 180, 180),
            shadow_color,
        )

        slider_rect = pygame.Rect(
            center_x - slider_width // 2, center_y + 10, slider_width, 10
        )
        pygame.draw.rect(screen, (100, 100, 100), slider_rect)
        pygame.draw.circle(screen, (255, 0, 0), (int(slider_x), slider_rect.y + 5), 10)

        volume_percent = f"{int(volume * 100)}%"
        draw_text_button(
            screen,
            volume_percent,
            (center_x, slider_rect.y + 30),
            small_font,
            (255, 255, 255),
            (180, 180, 180),
            shadow_color,
        )

        pygame.display.flip()

    config["fullscreen"] = fullscreen
    config["volume"] = volume
    save_config(config)

    def draw_enemy_kills():
        kill_text = small_font.render(f"Kills: {enemy_kills}", True, (255, 255, 255))
        screen.blit(kill_text, (screen_width - 150, 40))

    def draw_credits():
        kill_text = small_font.render(f"Creditos: {credits}", True, (255, 255, 255))
        screen.blit(kill_text, (screen_width - 150, 65))


running = True


def draw_enemy_kills():
    position = (screen_width - 150, 40)
    draw_text_button(
        screen,
        f"Kills: {enemy_kills}",
        position,
        small_font,
        (255, 255, 255),
        (180, 180, 180),
        shadow_color,
    )


def draw_credits():
    position = (screen_width - 150, 65)
    draw_text_button(
        screen,
        f"Créditos: {credits}",
        position,
        small_font,
        (255, 255, 255),
        (180, 180, 180),
        shadow_color,
    )


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_F11:
                fullscreen = not fullscreen
                if fullscreen:
                    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
                    screen_width, screen_height = screen.get_size()
                else:
                    screen_width, screen_height = 800, 600
                    screen = pygame.display.set_mode(
                        (screen_width, screen_height), pygame.RESIZABLE
                    )
                scaled_background = scale_background()
            elif event.key == pygame.K_ESCAPE:
                if game_state == "single_player":
                    game_state = "pause_menu"

        elif event.type == pygame.VIDEORESIZE and not fullscreen:
            screen_width, screen_height = event.w, event.h
            screen = pygame.display.set_mode(
                (screen_width, screen_height), pygame.RESIZABLE
            )
            scaled_background = scale_background()


    if game_state == "menu":
        screen.blit(scaled_background, (0, 0))

        play_position = (screen_width // 2, screen_height // 2 - 50 - button_spacing)
        options_position = (screen_width // 2, screen_height // 2)
        exit_position = (screen_width // 2, screen_height // 2 + 50 + button_spacing)

        if draw_text_button(
            screen,
            "Play",
            play_position,
            font,
            button_text_color,
            button_hover_color,
            shadow_color,
        ):
            game_state = "play_options"
        if draw_text_button(
            screen,
            "Options",
            options_position,
            font,
            button_text_color,
            button_hover_color,
            shadow_color,
        ):
            options_menu()
        if draw_text_button(
            screen,
            "Exit",
            exit_position,
            font,
            button_text_color,
            button_hover_color,
            shadow_color,
        ):
            running = False

    elif game_state == "play_options":
        play_options_screen()

    elif game_state == "single_player":

        screen.blit(scaled_background, (0, 0))
        screen.blit(player_image, rocket_position)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            rocket_position[1] -= rocket_speed
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            rocket_position[1] += rocket_speed
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            rocket_position[0] -= rocket_speed
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            rocket_position[0] += rocket_speed
        if keys[pygame.K_SPACE]:
            shoot_bullet()

        rocket_position[0] = max(
            0, min(rocket_position[0], screen_width - player_width)
        )
        rocket_position[1] = max(
            0, min(rocket_position[1], screen_height - player_height)
        )

        current_time = time.time()
        if current_time - last_spawn_time >= 1:
            spawn_enemy()
            last_spawn_time = current_time

        for enemy in enemies[:]:
            enemy["y"] += enemy_speed
            if enemy["y"] > screen_height:
                enemies.remove(enemy)
            else:
                screen.blit(enemy_image, (enemy["x"], enemy["y"]))
                if enemy["show_health_bar"]:
                    draw_health_bar(enemy)

        for bullet in bullets[:]:
            bullet["y"] -= bullet_speed
            pygame.draw.rect(
                screen,
                bullet_color,
                (bullet["x"], bullet["y"], bullet_width, bullet_height),
            )
            if bullet["y"] < 0:
                bullets.remove(bullet)

        for bullet in bullets[:]:
            bullet_rect = pygame.Rect(
                bullet["x"], bullet["y"], bullet_width, bullet_height
            )
            for enemy in enemies[:]:
                enemy_rect = pygame.Rect(
                    enemy["x"], enemy["y"], enemy_width, enemy_height
                )
                if bullet_rect.colliderect(enemy_rect):
                    bullets.remove(bullet)
                    enemy["health"] -= 1
                    enemy["show_health_bar"] = True
                    if enemy["health"] <= 0:
                        enemies.remove(enemy)
                        enemy_kills += 1
                        credits += 1
                    break
        draw_enemy_kills()
        draw_credits()
    elif game_state == "pause_menu":
        pause_menu()

    pygame.display.flip()

pygame.quit()
