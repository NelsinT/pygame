import pygame
import sys

# Inicializa o Pygame
pygame.init()

# Configurações iniciais da tela
screen_width, screen_height = 800, 600  # Dimensões padrão da janela
screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)  # Janela redimensionável
pygame.display.set_caption("Stellar Conquest")

# Configuração dos botões
font = pygame.font.SysFont("Arial", 40)
button_width, button_height = 200, 60
button_spacing = 20
button_base_color = (232, 60, 126)  # Cor do botão
button_hover_color = (255, 80, 150)  # Cor ao passar o mouse
button_border_color = (232, 60, 126)  # Cor das bordas

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


def draw_button(screen, text, rect, font, base_color, hover_color, border_color):
    mouse_pos = pygame.mouse.get_pos()
    is_hovered = rect.collidepoint(mouse_pos)
    color = hover_color if is_hovered else base_color

    # Desenha o botão
    pygame.draw.rect(screen, color, rect)
    pygame.draw.rect(screen, border_color, rect, 2)  # Borda personalizada

    # Desenha o texto
    text_surface = font.render(text, True, (255, 255, 255))
    text_rect = text_surface.get_rect(center=rect.center)
    screen.blit(text_surface, text_rect)

    # Retorna True se o botão foi clicado
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

    # Recalcula as posições dos botões para manter a centralização
    play_button = pygame.Rect((screen_width // 2 - button_width // 2, screen_height // 2 - button_height - button_spacing), (button_width, button_height))
    options_button = pygame.Rect((screen_width // 2 - button_width // 2, screen_height // 2), (button_width, button_height))
    exit_button = pygame.Rect((screen_width // 2 - button_width // 2, screen_height // 2 + button_height + button_spacing), (button_width, button_height))

    # Desenha os botões e detecta cliques
    if draw_button(screen, "Play", play_button, font, button_base_color, button_hover_color, button_border_color):
        print("Play button clicked!")  # Ação do botão Play
    if draw_button(screen, "Options", options_button, font, button_base_color, button_hover_color, button_border_color):
        print("Options button clicked!")  # Ação do botão Options
    if draw_button(screen, "Exit", exit_button, font, button_base_color, button_hover_color, button_border_color):
        running = False  # Fecha o programa

    # Atualiza o display
    pygame.display.flip()

# Finaliza o Pygame
pygame.quit()
sys.exit()
