import pygame
from random import randint

pygame.init()

pygame.mixer.music.set_volume(0.5)
musica_fundo = pygame.mixer.music.load("BoxCat Games - Mission.mp3")
pygame.mixer.music.play(-1)
som_colisao = pygame.mixer.Sound("smw_kick.wav")
som_colisao.set_volume(0.7)

LARGURA = 680
ALTURA = 680

tela = pygame.display.set_mode((LARGURA, ALTURA))
fonte = pygame.font.SysFont("arial", 20, True, True)
pygame.display.set_caption('Jogo da Cobrinha')
relogio = pygame.time.Clock()

cobra_corpo = []
comprimento_inicial = 10
x_cobra = ALTURA//2
y_cobra = LARGURA//2
x_maca = randint(60, 640)
y_maca = randint(60, 640)

deslocar = 5
x_controle = deslocar
y_controle = 0

rodar = True
pontuacao = 0
maior_pontuacao = 0
aumetar_velocidade = 0


def criar_linha(cor, pos_inicial, pos_final, espessura):
    return pygame.draw.line(tela, cor, pos_inicial, pos_final, espessura)


def criar_retangulo(cor, coordenada):
    return pygame.draw.rect(tela, cor, coordenada)


def mover_cobra(x_controle, y_controle, event):
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_a and x_controle == 0:
            x_controle = -deslocar
            y_controle = 0
        if event.key == pygame.K_d and x_controle == 0:
            x_controle = deslocar
            y_controle = 0
        if event.key == pygame.K_w and y_controle == 0:
            x_controle = 0
            y_controle = -deslocar
        if event.key == pygame.K_s and y_controle == 0:
            x_controle = 0
            y_controle = deslocar

    return x_controle, y_controle


def aumentar_cobra(lista_cobra):
    for posicao in lista_cobra:
        criar_retangulo(("green"), (posicao[0], posicao[1], 20, 20))


def reiniciar_jogo():
    global pontuacao, comprimento_inicial, x_cobra, y_cobra, cobra_cabeca, cobra_corpo, x_maca, y_maca, morreu, deslocar
    pontuacao = 0
    comprimento_inicial = 10
    x_cobra = ALTURA//2
    y_cobra = LARGURA//2
    cobra_corpo = []
    cobra_cabeca = []
    x_maca = randint(60, 640)
    y_maca = randint(60, 640)
    morreu = False
    deslocar = 5


while rodar:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            rodar = False
        x_controle, y_controle = mover_cobra(x_controle, y_controle, event)

    tela.fill('white')
    mensagem = f"Pontos: {pontuacao}"
    mensagem2 = f"Recorde: {maior_pontuacao}"
    texto_formatado = fonte.render(mensagem, True, ("black"))
    texto_formatado2 = fonte.render(mensagem2, True, ("black"))

    x_cobra += x_controle
    y_cobra += y_controle

    linha_superior = criar_linha(("black"), (0, 30), (680, 30), 4)
    cobra = criar_retangulo(("green4"), (x_cobra, y_cobra, 20, 20))
    maca = criar_retangulo(("red2"), (x_maca, y_maca, 20, 20))

    if aumetar_velocidade == 5 and deslocar < 15:
        deslocar += 0.3
        aumetar_velocidade = 0

    if cobra.colliderect(maca):
        x_maca = randint(60, 640)
        y_maca = randint(60, 640)
        aumetar_velocidade += 1
        pontuacao += 1

        if pontuacao > maior_pontuacao:
            maior_pontuacao = pontuacao

        som_colisao.play()
        comprimento_inicial += 1

    cobra_cabeca = (x_cobra, y_cobra)
    cobra_corpo.append(cobra_cabeca)

    if len(cobra_corpo) > comprimento_inicial:
        del cobra_corpo[0]

    if cobra_corpo.count(cobra_cabeca) > 1:
        fonte2 = pygame.font.SysFont("arial", 20, True, True)
        mensagem = f"Game Over!!! Presione R para recomeçar o jogo."
        texto_formatado = fonte2.render(mensagem, True, "white")
        ret_texto = texto_formatado.get_rect()

        morreu = True
        while morreu:
            tela.fill("black")
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        reiniciar_jogo()

            ret_texto.center = (LARGURA//2, ALTURA//2)
            tela.blit(texto_formatado, ret_texto)
            pygame.display.update()

    if x_cobra > LARGURA:
        x_cobra = 0 - 20
    if x_cobra < 0 - 20:
        x_cobra = LARGURA
    if y_cobra > ALTURA:
        y_cobra = 29
    if cobra.colliderect(linha_superior):
        y_cobra = ALTURA

    aumentar_cobra(cobra_corpo)
    tela.blit(texto_formatado, (0, 3))
    tela.blit(texto_formatado2, (540, 3))
    pygame.display.flip()
    relogio.tick(30)

pygame.quit()
