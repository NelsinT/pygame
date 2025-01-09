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
image_path = r"imagens\homescreen.png"
icon_path = r"imagens\icon.png"
music_path = r"soundtrack\background_music.mp3"
config_path = "config.csv"

# Função para carregar ou criar configurações
def load_config():
    if os.path.exists(config_path):
        df = pd.read_csv(config_path)
        config = df.iloc[0].to_dict()
        if "fullscreen" not in config:
            config["fullscreen"] = False
        if "volume" not in config:
            config["volume"] = 0.5
        return config
    else:
        default_config = {"volume": 0.5, "fullscreen": False}
        save_config(default_config)
        return default_config

def save_config(config):
    df = pd.DataFrame([config])
    df.to_csv(config_path, index=False)

# Carrega as configurações do arquivo
config = load_config()
volume = config["volume"]
fullscreen = config["fullscreen"]

# Carrega a imagem da homescreen
try:
    homescreen_image = pygame.image.load(image_path)
except pygame.error as e:
    print(f"Erro ao carregar a imagem: {e}")
    pygame.quit()
    sys.exit()

# Ajusta a tela inicial com base no fullscreen
if fullscreen:
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    screen_width, screen_height = screen.get_size()
else:
    screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)

# Função para redimensionar a imagem de fundo
def scale_background():
    return pygame.transform.scale(homescreen_image, (screen_width, screen_height))

scaled_background = scale_background()

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
    pygame.mixer.music.set_volume(volume)
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


def options_menu():
    global fullscreen, volume, screen_width, screen_height, screen, scaled_background
    running = True
    slider_width = 200

    # Calcula a posição inicial da bola com base no volume atual
    slider_x = (screen_width // 2 - slider_width // 2) + int(volume * slider_width)
    dragging = False  # Para controlar o arrasto do slider

    while running:
        screen.blit(scaled_background, (0, 0))  # Desenha o fundo redimensionado

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if slider_rect.collidepoint(pygame.mouse.get_pos()):
                    dragging = True  # Começa a arrastar
                elif toggle_rect.collidepoint(pygame.mouse.get_pos()):
                    fullscreen = not fullscreen
                    if fullscreen:
                        screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
                        screen_width, screen_height = screen.get_size()
                    else:
                        screen = pygame.display.set_mode((800, 600), pygame.RESIZABLE)
                        screen_width, screen_height = 800, 600
                    scaled_background = scale_background()
            elif event.type == pygame.MOUSEBUTTONUP:
                dragging = False  # Para o arrasto
            elif event.type == pygame.MOUSEMOTION and dragging:
                slider_x = pygame.mouse.get_pos()[0]
                slider_x = max(slider_rect.x, min(slider_x, slider_rect.x + slider_width))
                volume = (slider_x - slider_rect.x) / slider_width
                pygame.mixer.music.set_volume(volume)

        # Calcula posições centralizadas
        center_x = screen_width // 2
        center_y = screen_height // 2

        # Renderiza o botão de fullscreen centralizado
        toggle_text = "Fullscreen: ON" if fullscreen else "Fullscreen: OFF"
        toggle_rect = pygame.Rect(center_x - 100, center_y - 100, 200, 50)  # Acima do texto de volume
        draw_text_button(screen, toggle_text, toggle_rect.center, small_font, (255, 255, 255), (180, 180, 180), shadow_color)

        # Renderiza o texto de volume centralizado
        volume_text = small_font.render("Volume:", True, (255, 255, 255))
        screen.blit(volume_text, (center_x - volume_text.get_width() // 2, center_y - 20))

        # Renderiza o slider de volume centralizado abaixo do texto
        slider_rect = pygame.Rect(center_x - slider_width // 2, center_y + 10, slider_width, 10)
        pygame.draw.rect(screen, (100, 100, 100), slider_rect)
        pygame.draw.circle(screen, (255, 0, 0), (int(slider_x), slider_rect.y + 5), 10)

        # Exibe a porcentagem do volume imediatamente abaixo da barra
        volume_percent = f"{int(volume * 100)}%"  # Calcula a porcentagem
        volume_percent_text = small_font.render(volume_percent, True, (255, 255, 255))
        screen.blit(volume_percent_text, (center_x - volume_percent_text.get_width() // 2, slider_rect.y + 20))

        pygame.display.flip()

    # Salva o estado de fullscreen e volume
    config["fullscreen"] = fullscreen
    config["volume"] = volume
    save_config(config)






running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.type == pygame.VIDEORESIZE and not fullscreen:
                screen_width, screen_height = event.w, event.h
                screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)
                scaled_background = scale_background()

    screen.blit(scaled_background, (0, 0))

    play_position = (screen_width // 2, screen_height // 2 - 50 - button_spacing)
    options_position = (screen_width // 2, screen_height // 2)
    exit_position = (screen_width // 2, screen_height // 2 + 50 + button_spacing)

    if draw_text_button(screen, "Play", play_position, font, button_text_color, button_hover_color, shadow_color):
        print("Play button clicked!")
    if draw_text_button(screen, "Options", options_position, font, button_text_color, button_hover_color, shadow_color):
        options_menu()
    if draw_text_button(screen, "Exit", exit_position, font, button_text_color, button_hover_color, shadow_color):
        running = False

    pygame.display.flip()

pygame.quit()
sys.exit()
