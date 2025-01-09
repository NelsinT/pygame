import pygame
import sys

# Inicializa o Pygame
pygame.init()

# Configurações iniciais da tela
screen_width, screen_height = 800, 600  # Dimensões padrão da janela
screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)  # Janela redimensionável
pygame.display.set_caption("Stellar Conquest")

# Configuração dos botões
font = pygame.font.SysFont("Arial", 50, bold=True)  # Fonte maior e em negrito
button_spacing = 40
button_text_color = (232, 60, 126)  # Cor do texto base
button_hover_color = (255, 105, 180)  # Cor ao passar o mouse (vibrante)
shadow_color = (150, 30, 90)  # Cor para a sombra do texto

# Caminho completo para a imagem
image_path = r"C:\Users\NelsinT\Desktop\pygame\pygame\imagens\homescreen.png"
icon_path = r"C:\Users\NelsinT\Desktop\pygame\pygame\imagens\icon.png"

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
    pygame.display.set_icon(icon_image)  # Define o ícone personalizado
except pygame.error as e:
    print(f"Erro ao carregar a imagem do ícone: {e}")
    pygame.quit()
    sys.exit()


def draw_text_button(screen, text, position, font, base_color, hover_color, shadow_color):
    mouse_pos = pygame.mouse.get_pos()

    # Verifica se o mouse está sobre o texto
    text_surface = font.render(text, True, base_color)
    text_rect = text_surface.get_rect(center=position)
    is_hovered = text_rect.collidepoint(mouse_pos)

    # Altera a cor do texto ao passar o mouse
    color = hover_color if is_hovered else base_color
    text_surface = font.render(text, True, color)

    # Adiciona sombra ao texto
    shadow_surface = font.render(text, True, shadow_color)
    shadow_rect = shadow_surface.get_rect(center=(position[0] + 2, position[1] + 2))  # Leve deslocamento para sombra
    screen.blit(shadow_surface, shadow_rect)

    # Desenha o texto principal
    screen.blit(text_surface, text_rect)

    # Retorna True se o texto foi clicado
    return is_hovered and pygame.mouse.get_pressed()[0]


# Loop principal
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:  # Sai com a tecla ESC
                running = False
        elif event.type == pygame.VIDEORESIZE:
            # Atualiza o tamanho da janela e redimensiona a imagem
            screen_width, screen_height = event.w, event.h
            screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)
            homescreen_image = pygame.transform.scale(homescreen_image, (screen_width, screen_height))

    # Exibe a imagem na tela redimensionada
    screen.blit(homescreen_image, (0, 0))

    # Calcula as posições dos textos (botões) para manter a centralização
    play_position = (screen_width // 2, screen_height // 2 - 50 - button_spacing)
    options_position = (screen_width // 2, screen_height // 2)
    exit_position = (screen_width // 2, screen_height // 2 + 50 + button_spacing)

    # Desenha os textos (botões) e detecta cliques
    if draw_text_button(screen, "Play", play_position, font, button_text_color, button_hover_color, shadow_color):
        print("Play button clicked!")  # Ação do botão Play
    if draw_text_button(screen, "Options", options_position, font, button_text_color, button_hover_color, shadow_color):
        print("Options button clicked!")  # Ação do botão Options
    if draw_text_button(screen, "Exit", exit_position, font, button_text_color, button_hover_color, shadow_color):
        running = False  # Fecha o programa

    # Atualiza o display
    pygame.display.flip()

# Finaliza o Pygame
pygame.quit()
sys.exit()
