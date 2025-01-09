import pygame
import sys
import pandas as pd
import os

# Inicializa o Pygame
pygame.init()
pygame.mixer.init()  # Inicializa o mixer para música

# Configurações iniciais da tela
screen_width, screen_height = 800, 600  # Dimensões padrão da janela
fullscreen = False  # Começa com fullscreen desativado
screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)  # Janela redimensionável
pygame.display.set_caption("Stellar Conquest")

# Configuração dos botões
font = pygame.font.SysFont("Arial", 50, bold=True)
small_font = pygame.font.SysFont("Arial", 30)
button_spacing = 40
button_text_color = (232, 60, 126)
button_hover_color = (255, 105, 180)
shadow_color = (150, 30, 90)

# Caminho completo para a imagem
image_path = r"C:\Users\NelsinT\Desktop\pygame\pygame\imagens\homescreen.png"
icon_path = r"C:\Users\NelsinT\Desktop\pygame\pygame\imagens\icon.png"
music_path = r"C:\Users\NelsinT\Desktop\pygame\pygame\soundtrack\background_music.mp3"
config_path = "config.csv"

# Função para carregar ou criar configurações
def load_config():
    if os.path.exists(config_path):
        df = pd.read_csv(config_path)
        config = df.iloc[0].to_dict()
        # Garante que as chaves necessárias existam
        if "fullscreen" not in config:
            config["fullscreen"] = False
        if "volume" not in config:
            config["volume"] = 0.5
        return config
    else:
        # Configuração padrão inicial
        default_config = {"volume": 0.5, "fullscreen": False}
        save_config(default_config)
        return default_config

def save_config(config):
    df = pd.DataFrame([config])  # Cria um DataFrame com os dados
    df.to_csv(config_path, index=False)

# Carrega as configurações do arquivo
config = load_config()
volume = config["volume"]
fullscreen = config["fullscreen"]

# Configura o modo da janela baseado no estado de fullscreen
if fullscreen:
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
else:
    screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)

# Carrega a imagem da homescreen
try:
    homescreen_image = pygame.image.load(image_path)
except pygame.error as e:
    print(f"Erro ao carregar a imagem: {e}")
    pygame.quit()
    sys.exit()

# Carrega e define o ícone
try:
    icon_image = pygame.image.load(icon_path)
    pygame.display.set_icon(icon_image)
except pygame.error as e:
    print(f"Erro ao carregar a imagem do ícone: {e}")
    pygame.quit()
    sys.exit()

# Carrega e reproduz a música de fundo
try:
    pygame.mixer.music.load(music_path)
    pygame.mixer.music.set_volume(volume)  # Define o volume inicial
    pygame.mixer.music.play(-1)
except pygame.error as e:
    print(f"Erro ao carregar a música: {e}")
    pygame.quit()
    sys.exit()


def draw_text_button(screen, text, position, font, base_color, hover_color, shadow_color):
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


def options_menu(screen):
    global fullscreen  # Para modificar o estado globalmente
    global volume  # Para modificar o volume globalmente
    running = True
    slider_width = 200
    slider_x = 400 + int(volume * slider_width)  # Calcula posição inicial do slider com base no volume

    while running:
        screen.fill((30, 30, 30))  # Cor de fundo para a tela de opções

        # Eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if toggle_rect.collidepoint(pygame.mouse.get_pos()):
                    fullscreen = not fullscreen
                    if fullscreen:
                        screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
                    else:
                        screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)

                # Controle de volume pelo slider
                if slider_rect.collidepoint(pygame.mouse.get_pos()):
                    slider_x = pygame.mouse.get_pos()[0]
                    slider_x = max(slider_rect.x, min(slider_x, slider_rect.x + slider_width))
                    volume = (slider_x - slider_rect.x) / slider_width
                    pygame.mixer.music.set_volume(volume)

        # Renderiza o botão de tela cheia (toggle)
        toggle_text = "Fullscreen: ON" if fullscreen else "Fullscreen: OFF"
        toggle_rect = pygame.Rect(300, 200, 200, 50)
        pygame.draw.rect(screen, (80, 80, 80), toggle_rect)
        draw_text_button(screen, toggle_text, toggle_rect.center, small_font, (255, 255, 255), (180, 180, 180), shadow_color)

        # Renderiza o slider de volume
        volume_text = small_font.render("Volume:", True, (255, 255, 255))
        screen.blit(volume_text, (250, 300))
        slider_rect = pygame.Rect(400, 310, slider_width, 10)
        pygame.draw.rect(screen, (100, 100, 100), slider_rect)
        pygame.draw.circle(screen, (255, 0, 0), (slider_x, slider_rect.y + 5), 10)

        # Atualiza a tela
        pygame.display.flip()

    # Salva o estado de fullscreen e volume
    config["fullscreen"] = fullscreen
    config["volume"] = volume
    save_config(config)


# Loop principal
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
        elif event.type == pygame.VIDEORESIZE and not fullscreen:
            screen_width, screen_height = event.w, event.h
            screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)
            homescreen_image = pygame.transform.scale(homescreen_image, (screen_width, screen_height))

    scaled_background = pygame.transform.scale(homescreen_image, (screen_width, screen_height))
    screen.blit(scaled_background, (0, 0))

    play_position = (screen_width // 2, screen_height // 2 - 50 - button_spacing)
    options_position = (screen_width // 2, screen_height // 2)
    exit_position = (screen_width // 2, screen_height // 2 + 50 + button_spacing)

    if draw_text_button(screen, "Play", play_position, font, button_text_color, button_hover_color, shadow_color):
        print("Play button clicked!")
    if draw_text_button(screen, "Options", options_position, font, button_text_color, button_hover_color, shadow_color):
        options_menu(screen)  # Passa o screen para a função
    if draw_text_button(screen, "Exit", exit_position, font, button_text_color, button_hover_color, shadow_color):
        running = False

    pygame.display.flip()

pygame.quit()
sys.exit()
