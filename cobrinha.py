import pygame
import random

largura_tela = 800
altura_tela = 600
rodando = True
game_over = False  # Estado de game over
fps = 8
LADO_QUADRADO = 20

# cobra começa no meio
xq = largura_tela // 2
yq = altura_tela // 2

# corpo da cobra (lista de quadrados)
corpo_cobra = [[xq, yq]]

# direção (0, -20 = cima)
dx = 0
dy = -20

# comida
comida_x = 200
comida_y = 200

def reiniciar_jogo():
    """Reinicia todas as variáveis do jogo"""
    global game_over, xq, yq, corpo_cobra, dx, dy, comida_x, comida_y
    game_over = False
    xq = largura_tela // 2
    yq = altura_tela // 2
    corpo_cobra = [[xq, yq]]
    dx = 0
    dy = -20
    comida_x = 200
    comida_y = 200
    print("Jogo Reiniciado!")

def proc_eventos():
    global rodando, dx, dy
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False
        if evento.type == pygame.KEYDOWN:
            if not game_over:  # Só aceita comandos se não estiver em game over
                if evento.key == pygame.K_UP and dy != 20:
                    dx = 0
                    dy = -20
                    print("Cima")
                if evento.key == pygame.K_DOWN and dy != -20:
                    dx = 0
                    dy = 20
                    print("Baixo")
                if evento.key == pygame.K_LEFT and dx != 20:
                    dx = -20
                    dy = 0
                    print("Esquerda")
                if evento.key == pygame.K_RIGHT and dx != -20:
                    dx = 20
                    dy = 0
                    print("Direita")
            # Tecla R para reiniciar manualmente (funciona sempre)
            if evento.key == pygame.K_r:
                reiniciar_jogo()

def proc_colisoes():
    global xq, yq, corpo_cobra, dx, dy, comida_x, comida_y, game_over
    
    if game_over:
        return  # Não processa colisões em game over
    
    # nova posição da cabeça
    nova_cabeca_x = corpo_cobra[0][0] + dx
    nova_cabeca_y = corpo_cobra[0][1] + dy
    
    # bateu na borda? -> REINICIA AUTOMATICAMENTE!
    if nova_cabeca_x < 0 or nova_cabeca_x > largura_tela - LADO_QUADRADO:
        print("Bateu na borda! Reiniciando...")
        reiniciar_jogo()
        return
    if nova_cabeca_y < 0 or nova_cabeca_y > altura_tela - LADO_QUADRADO:
        print("Bateu na borda! Reiniciando...")
        reiniciar_jogo()
        return
    
    # bateu no corpo? -> REINICIA AUTOMATICAMENTE!
    nova_cabeca = [nova_cabeca_x, nova_cabeca_y]
    for parte in corpo_cobra:
        if parte[0] == nova_cabeca[0] and parte[1] == nova_cabeca[1]:
            print("Comeu o rabo! Reiniciando...")
            reiniciar_jogo()
            return
    
    # comeu comida?
    if nova_cabeca_x == comida_x and nova_cabeca_y == comida_y:
        print("Comeu!")
        # nova comida
        comida_x = random.randint(0, 39) * 20
        comida_y = random.randint(0, 29) * 20
    else:
        # tira o ultimo pedaço do corpo
        corpo_cobra.pop()
    
    # adiciona nova cabeça
    corpo_cobra.insert(0, nova_cabeca)

def desenhar_cobra(tela):
    for i in range(len(corpo_cobra)):
        x = corpo_cobra[i][0]
        y = corpo_cobra[i][1]
        if i == 0:
            cor = "#00FF00"  # cabeça verde claro
        else:
            cor = "#008000"  # corpo verde escuro
        pygame.draw.rect(tela, cor, (x, y, LADO_QUADRADO, LADO_QUADRADO))

if __name__ == "__main__":
    pygame.init()
    tela = pygame.display.set_mode((largura_tela, altura_tela))
    pygame.display.set_caption("Cobrinha Infinita")
    relogio = pygame.time.Clock()
    
    while rodando:
        proc_eventos()
        proc_colisoes()
        
        tela.fill("#1a3c1a")  # fundo verde bem escuro
        
        if game_over:
            # Tela de game over breve (reinicia automaticamente)
            fonte = pygame.font.Font(None, 74)
            texto = fonte.render("GAME OVER!", True, "#FF0000")
            texto_rect = texto.get_rect(center=(largura_tela//2, altura_tela//2))
            tela.blit(texto, texto_rect)
            
            fonte_pequena = pygame.font.Font(None, 36)
            texto_reiniciar = fonte_pequena.render("Reiniciando em 1s... (R para manual)", True, "#FFFFFF")
            texto_rect2 = texto_reiniciar.get_rect(center=(largura_tela//2, altura_tela//2 + 60))
            tela.blit(texto_reiniciar, texto_rect2)
        else:
            desenhar_cobra(tela)
            # comida vermelha REDONDA
            pygame.draw.circle(tela, "#FF0000", (comida_x + 10, comida_y + 10), 10)
        
        pygame.display.flip()
        relogio.tick(fps)
    
    print("Janela fechada pelo usuário!")
    pygame.quit()