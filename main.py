import pygame
import sys
import random


pygame.init()


LARGURA, ALTURA = 800, 600
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Cosmos: O Pálido Ponto Azul")


# Cores 
PRETO = (3, 3, 5)             # Espaço profundo (quase preto)
BRANCO = (240, 240, 245)       # Estrelas brilhantes
AZUL_PALIDO = (150, 200, 255)   # O Pálido Ponto Azul (Planeta Terra)
CINZA_TEXTO = (180, 180, 190)   # Legendas legíveis
VERMELHO_NEON = (255, 80, 80)   # Alerta / Inimigos / Vida
VERDE_CYAN = (0, 230, 160)     # Sucesso / Transições / Metas


fonte_titulo = pygame.font.SysFont("consolas", 52, bold=True)
fonte_subtitulo = pygame.font.SysFont("consolas", 22)
fonte_texto = pygame.font.SysFont("consolas", 18)
fonte_hud = pygame.font.SysFont("consolas", 16, bold=True)
fonte_lore = pygame.font.SysFont("georgia", 20, italic=True)

# Estados do Jogo
MENU, JOGO, TRANSIÇÃO, VITORIA, DERROTA = 0, 1, 2, 3, 4
estado_atual = MENU

#  FRASES DA LORE 
LORE_NIVEIS = {
    1: '"Olhe novamente para esse ponto. Isso é o aqui. Isso é a nossa casa. Isso somos nós."',
    2: '"A Terra é um cenário muito pequeno numa vasta arena cósmica de perigos."',
    3: '"Nossas posturas, nossa suposta autoimportância... são desafiadas por este ponto de luz pálida."',
    4: '"Na nossa obscuridade, não há indícios de que a ajuda virá de outro lugar para nos salvar."'
}
frase_transicao = ""
carta_aberta = False 

#  CONFIGURAÇÕES 
# Jogador 
nave_largura = 36
nave_altura = 32
nave_x = LARGURA // 2 - nave_largura // 2
nave_y = ALTURA - 90
nave_velocidade = 8  
vidas = 3
pontos = 0
nivel = 1

# Tiros
tiros = []
tiro_velocidade = -11 
tiro_largura, tiro_altura = 3, 14
ultimo_tiro = 0
cooldown_tiro = 150  

# Asteroides 
asteroides = []
asteroide_velocidade_base = 5   
tempo_ultimo_asteroide = 0
frequencia_asteroide = 500      

# Inimigos 
bichos = []
bicho_largura, bicho_altura = 34, 24
tempo_ultimo_bicho = 0
frequencia_bicho = 1500         

# Pedrinhas 
pedrinhas = []
pedrinha_velocidade = 8         
pedrinha_largura, pedrinha_altura = 6, 6


PONTOS_POR_NIVEL = 200

# Estrelas de Fundo 
estrelas = [{"x": random.randint(0, LARGURA), "y": random.randint(0, ALTURA), "vel": random.uniform(0.5, 2)} for _ in range(40)]

# Área de clique da nave da Engenheira Jai 
rect_nave_jai = pygame.Rect(LARGURA // 2 - 25, 170, 50, 50)


def resetar_jogo():
    global nave_x, nave_y, vidas, pontos, nivel, tiros, asteroides, bichos, pedrinhas, carta_aberta
    nave_x = LARGURA // 2 - nave_largura // 2
    nave_y = ALTURA - 90
    vidas = 3
    pontos = 0
    nivel = 1
    tiros = []
    asteroides = []
    bichos = []
    pedrinhas = []
    carta_aberta = False


def quebrar_texto(texto, largura_maxima, fonte):
    palavras = texto.split(' ')
    linhas = []
    linha_atual = ""
    for palavra in palavras:
        testar_linha = linha_atual + " " + palavra if linha_atual else palavra
        if fonte.size(testar_linha)[0] <= largura_maxima:
            linha_atual = testar_linha
        else:
            linhas.append(linha_atual)
            linha_atual = palavra
    if linha_atual:
        linhas.append(linha_atual)
    return linhas



def desenhar_estrelas():
    for estrela in estrelas:
        if estado_atual == JOGO:
            estrela["y"] += estrela["vel"]
            if estrela["y"] > ALTURA:
                estrela["y"] = 0
                estrela["x"] = random.randint(0, LARGURA)
        pygame.draw.circle(tela, (100, 100, 120), (int(estrela["x"]), int(estrela["y"])), 1)

def desenhar_menu():
    tela.fill(PRETO)
    desenhar_estrelas()
    
    titulo = fonte_titulo.render("C O S M O S", True, BRANCO)
    subtitulo = fonte_subtitulo.render("A Jornada pelo Pálido Ponto Azul", True, AZUL_PALIDO)
    tela.blit(titulo, (LARGURA // 2 - titulo.get_width() // 2, 110))
    tela.blit(subtitulo, (LARGURA // 2 - subtitulo.get_width() // 2, 165))
    
    
    painel_com = pygame.Rect(LARGURA // 2 - 260, 240, 520, 140)
    pygame.draw.rect(tela, (15, 15, 25), painel_com)
    pygame.draw.rect(tela, AZUL_PALIDO, painel_com, 1) 
    
    txt_com = fonte_texto.render("> COMANDOS DE BORDO:", True, BRANCO)
    txt_setas = fonte_texto.render("  Direcionais [<- / ->] : Mover Nave exploradora", True, CINZA_TEXTO)
    txt_espaco = fonte_texto.render("  Barra de Espaço       : Disparar Módulos Laser", True, CINZA_TEXTO)
    txt_objetivo = fonte_texto.render(f"  Objetivo: Proteger o ponto azul por 4 setores", True, VERDE_CYAN)
    
    tela.blit(txt_com, (painel_com.x + 20, painel_com.y + 15))
    tela.blit(txt_setas, (painel_com.x + 20, painel_com.y + 45))
    tela.blit(txt_espaco, (painel_com.x + 20, painel_com.y + 75))
    tela.blit(txt_objetivo, (painel_com.x + 20, painel_com.y + 105))
    
    txt_iniciar = fonte_subtitulo.render("[ Pressione ENTER para Iniciar ]", True, BRANCO)
    tela.blit(txt_iniciar, (LARGURA // 2 - txt_iniciar.get_width() // 2, 440))

def desenhar_transicao():
    tela.fill(PRETO)
    desenhar_estrelas()
    
    txt_nv = fonte_titulo.render(f"SETOR {nivel - 1} CONCLUÍDO", True, VERDE_CYAN)
    tela.blit(txt_nv, (LARGURA // 2 - txt_nv.get_width() // 2, ALTURA // 2 - 120))
    
    texto_para_exibir = frase_transicao if frase_transicao != "" else LORE_NIVEIS[1]
    
    # Divisão lore
    linhas_texto = quebrar_texto(texto_para_exibir, 700, fonte_lore)
    
    y_offset = ALTURA // 2 - 30
    for linha in linhas_texto:
        txt_renderizado = fonte_lore.render(linha, True, AZUL_PALIDO)
        tela.blit(txt_renderizado, (LARGURA // 2 - txt_renderizado.get_width() // 2, y_offset))
        y_offset += 32
    
    txt_cont = fonte_texto.render("Pressione ENTER para continuar viagem...", True, CINZA_TEXTO)
    tela.blit(txt_cont, (LARGURA // 2 - txt_cont.get_width() // 2, ALTURA // 2 + 140))

def rodar_jogo():
    global nave_x, vidas, pontos, nivel, ultimo_tiro, tempo_ultimo_asteroide, tempo_ultimo_bicho, estado_atual, frase_transicao
    tela.fill(PRETO)
    desenhar_estrelas()
    
    agora = pygame.time.get_ticks()
    velocidade_atual_asteroide = asteroide_velocidade_base + (nivel * 0.8)
    
    #  CONTROLES DO JOGADOR
    teclas = pygame.key.get_pressed()
    if teclas[pygame.K_LEFT] and nave_x > 0:
        nave_x -= nave_velocidade
    if teclas[pygame.K_RIGHT] and nave_x < LARGURA - nave_largura:
        nave_x += nave_velocidade
    if teclas[pygame.K_SPACE] and agora - ultimo_tiro > cooldown_tiro:
        tiros.append(pygame.Rect(nave_x + nave_largura // 2 - tiro_largura // 2, nave_y, tiro_largura, tiro_altura))
        ultimo_tiro = agora

    #  GERAR ASTEROIDES
    if agora - tempo_ultimo_asteroide > max(250, (frequencia_asteroide - (nivel * 60))):
        tamanho = random.randint(18, 44)
        ast_x = random.randint(0, LARGURA - tamanho)
        asteroides.append(pygame.Rect(ast_x, -tamanho, tamanho, tamanho))
        tempo_ultimo_asteroide = agora

    #  GERAR BICHOS
    if nivel >= 2 and agora - tempo_ultimo_bicho > frequencia_bicho:
        bicho_x = random.randint(50, LARGURA - 50)
        bichos.append({"rect": pygame.Rect(bicho_x, 65, bicho_largura, bicho_altura), "dir": random.choice([-1, 1]), "ultimo_tiro": agora})
        tempo_ultimo_bicho = agora

    #  ATUALIZAR TIROS DO JOGADOR
    for tiro in tiros[:]:
        tiro.y += tiro_velocidade
        if tiro.y < 0:
            tiros.remove(tiro)

    #  ATUALIZAR ASTEROIDES
    for asteroide in asteroides[:]:
        asteroide.y += velocidade_atual_asteroide
        
        if asteroide.colliderect(pygame.Rect(nave_x, nave_y, nave_largura, nave_altura)):
            vidas -= 1
            asteroides.remove(asteroide)
            if vidas <= 0: estado_atual = DERROTA
            continue
            
        if asteroide.y > ALTURA:
            asteroides.remove(asteroide)
            continue
            
        for tiro in tiros[:]:
            if tiro.colliderect(asteroide):
                if tiro in tiros: tiros.remove(tiro)
                if asteroide in asteroides: asteroides.remove(asteroide)
                pontos += 50

    #  ATUALIZAR BICHOS 
    for bicho in bichos[:]:
        rect = bicho["rect"]
        rect.x += bicho["dir"] * 3  
        
        if rect.left <= 0 or rect.right >= LARGURA:
            bicho["dir"] *= -1
            
        if agora - bicho["ultimo_tiro"] > 800: 
            pedrinhas.append(pygame.Rect(rect.centerx - 3, rect.bottom, pedrinha_largura, pedrinha_altura))
            bicho["ultimo_tiro"] = agora
            
        for tiro in tiros[:]:
            if tiro.colliderect(rect):
                if tiro in tiros: tiros.remove(tiro)
                if bicho in bichos: bichos.remove(bicho)
                pontos += 100

    for pedrinha in pedrinhas[:]:
        pedrinha.y += pedrinha_velocidade
        
        if pedrinha.colliderect(pygame.Rect(nave_x, nave_y, nave_largura, nave_altura)):
            vidas -= 1
            pedrinhas.remove(pedrinha)
            if vidas <= 0: estado_atual = DERROTA
            continue
            
        if pedrinha.y > ALTURA:
            pedrinhas.remove(pedrinha)

    meta_atual = nivel * PONTOS_POR_NIVEL
    if pontos >= meta_atual:
        if nivel in LORE_NIVEIS:
            frase_transicao = LORE_NIVEIS[nivel]
        else:
            frase_transicao = '"Preservar e valorizar o pálido ponto azul, o único lar que conhecemos."'
            
        nivel += 1
        tiros.clear()
        asteroides.clear()
        bichos.clear()
        pedrinhas.clear()
        
        if nivel > 4:
            estado_atual = VITORIA
        else:
            estado_atual = TRANSIÇÃO

    #  DESIGN 
    pygame.draw.circle(tela, AZUL_PALIDO, (LARGURA - 60, 70), 5)
    
    ponto_topo = (nave_x + nave_largura // 2, nave_y)
    ponto_esq = (nave_x, nave_y + nave_altura)
    ponto_dir = (nave_x + nave_largura, nave_y + nave_altura)
    ponto_centro = (nave_x + nave_largura // 2, nave_y + nave_altura - 6)
    pygame.draw.polygon(tela, BRANCO, [ponto_topo, ponto_dir, ponto_centro, ponto_esq])
    
    for tiro in tiros:
        pygame.draw.rect(tela, (0, 255, 255), tiro)
    for asteroide in asteroides:
        pygame.draw.rect(tela, (70, 75, 90), asteroide, border_radius=3)
        pygame.draw.rect(tela, (100, 105, 120), asteroide, 1, border_radius=3) 
    for bicho in bichos:
        r = bicho["rect"]
        pts = [(r.centerx, r.top), (r.right, r.centery), (r.centerx, r.bottom), (r.left, r.centery)]
        pygame.draw.polygon(tela, VERMELHO_NEON, pts)
    for pedrinha in pedrinhas:
        pygame.draw.circle(tela, VERMELHO_NEON, (pedrinha.x, pedrinha.y), 3)

    txt_pontos = fonte_hud.render(f"SCORE_SYS: {pontos:04d} / {meta_atual:04d}", True, BRANCO)
    txt_vidas  = fonte_hud.render(f"HULL_INT: {'I' * vidas}", True, VERMELHO_NEON)
    txt_nivel  = fonte_hud.render(f"SECTOR:   {nivel}/4", True, AZUL_PALIDO)
    
    tela.blit(txt_pontos, (20, 20))
    tela.blit(txt_vidas, (20, 40))
    tela.blit(txt_nivel, (20, 60))

def desenhar_fim_jogo(resultado):
    tela.fill(PRETO)
    desenhar_estrelas()
    
    if resultado == "vitoria":
        
        titulo = fonte_titulo.render("JORNADA CONCLUÍDA", True, AZUL_PALIDO)
        frase_antiga = fonte_lore.render('"Ela nos lembra da nossa responsabilidade de tratar melhor uns outros."', True, CINZA_TEXTO)
        
        tela.blit(titulo, (LARGURA // 2 - titulo.get_width() // 2, 40))
        tela.blit(frase_antiga, (LARGURA // 2 - frase_antiga.get_width() // 2, 100))
        
        
        nave_jai_x = rect_nave_jai.centerx
        nave_jai_y = rect_nave_jai.centery
        pygame.draw.polygon(tela, BRANCO, [(nave_jai_x, nave_jai_y - 20), (nave_jai_x - 25, nave_jai_y + 20), (nave_jai_x + 25, nave_jai_y + 20)])
        pygame.draw.polygon(tela, VERDE_CYAN, [(nave_jai_x, nave_jai_y - 10), (nave_jai_x - 12, nave_jai_y + 15), (nave_jai_x + 12, nave_jai_y + 15)])
        pygame.draw.circle(tela, AZUL_PALIDO, (nave_jai_x, nave_jai_y + 5), 4) 
        
        if not carta_aberta:
            txt_clique = fonte_hud.render("[ CLIQUE NA NAVE PARA TRANSMISSÃO GALÁTICA ]", True, VERDE_CYAN)
            tela.blit(txt_clique, (LARGURA // 2 - txt_clique.get_width() // 2, 250))
        else:
            
            txt_nome = fonte_hud.render("[ Engenheira dos Cosmos Jai ]", True, VERDE_CYAN)
            tela.blit(txt_nome, (LARGURA // 2 - txt_nome.get_width() // 2, 245))

            balao = pygame.Rect(50, 275, 700, 245) # Alinhado com 700px de largura
            pygame.draw.rect(tela, (12, 12, 22), balao)       
            pygame.draw.rect(tela, AZUL_PALIDO, balao, 1)    
            
            carta_completa = (
                "O universo é vasto, mas encontre algo que te faça sorrir, encontre uma ambição "
                "que consuma seu tempo, uma paixão que queime seu peito como asteróides "
                "colidindo com um simples ponto azul. E mesmo que você colida todos os dias, "
                "o espaço continuará afundado em silêncio. E mesmo que o espaço seja silencioso, "
                "A colisão dentro de nossas mentes é barulhenta demais. Eu ouço. Seja gentil "
                "consigo mesmo, temos cosmos para desvendar e talvez no final do dia um café quente "
                "depois de derrotar os desafios. Boa sorte!"
            )
            
            
            linhas_carta = quebrar_texto(carta_completa, 650, fonte_lore)
            
            y_offset = balao.y + 20
            for linha in linhas_carta:
                txt_linha = fonte_lore.render(linha, True, BRANCO)
                tela.blit(txt_linha, (balao.x + 25, y_offset))
                y_offset += 26
            
        txt_voltar = fonte_subtitulo.render("[ Pressione M para reiniciar o sistema ]", True, CINZA_TEXTO)
        tela.blit(txt_voltar, (LARGURA // 2 - txt_voltar.get_width() // 2, ALTURA - 40))
        
    else:
        titulo = fonte_titulo.render("CONEXÃO PERDIDA", True, VERMELHO_NEON)
        frase = fonte_lore.render('"Na vastidão do espaço, não há indícios de que a ajuda virá de fora."', True, CINZA_TEXTO)
        tela.blit(titulo, (LARGURA // 2 - titulo.get_width() // 2, ALTURA // 2 - 60))
        tela.blit(frase, (LARGURA // 2 - frase.get_width() // 2, ALTURA // 2))
        
        txt_voltar = fonte_subtitulo.render("[ Pressione M para reiniciar o sistema ]", True, BRANCO)
        tela.blit(txt_voltar, (LARGURA // 2 - txt_voltar.get_width() // 2, ALTURA // 2 + 120))

#  LOOP PRINCIPAL 
relogio = pygame.time.Clock()

while True:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            
        if evento.type == pygame.MOUSEBUTTONDOWN:
            if evento.button == 1:  
                if estado_atual == VITORIA:
                    pos_mouse = pygame.mouse.get_pos()
                    if rect_nave_jai.collidepoint(pos_mouse):
                        carta_aberta = True  

        if evento.type == pygame.KEYDOWN:
            if estado_atual == MENU:
                if evento.key == pygame.K_RETURN:
                    resetar_jogo()
                    estado_atual = JOGO
            elif estado_atual == TRANSIÇÃO:
                if evento.key == pygame.K_RETURN:
                    estado_atual = JOGO
            elif estado_atual in [VITORIA, DERROTA]:
                if evento.key == pygame.K_m:
                    resetar_jogo()  
                    estado_atual = MENU

    if estado_atual == MENU:
        desenhar_menu()
    elif estado_atual == JOGO:
        rodar_jogo()
    elif estado_atual == TRANSIÇÃO:
        desenhar_transicao()
    elif estado_atual == VITORIA:
        desenhar_fim_jogo("vitoria")
    elif estado_atual == DERROTA:
        desenhar_fim_jogo("derrota")

    pygame.display.flip()
    relogio.tick(60)