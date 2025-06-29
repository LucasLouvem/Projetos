import pygame
import random
import sys
import math

pygame.init()

# ───────────────────────── CONFIGURAÇÃO ──────────────────────────
CARD_W, CARD_H   = 100, 130
GAP_X,  GAP_Y    = 20, 20        # espaço entre cartas
MARGIN_X, MARGIN_Y = 60, 60      # margens internas
COLS             = 5             # 5 colunas → 5 × 3 = 15 posições (uma sobra)
PAIRS            = 7             # 7 pares  → 14 cartas

ROWS = math.ceil((PAIRS * 2) / COLS)
WIDTH  = MARGIN_X * 2 + COLS * CARD_W + (COLS - 1) * GAP_X
HEIGHT = MARGIN_Y * 2 + ROWS * CARD_H + (ROWS - 1) * GAP_Y

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Memory Game")

clock = pygame.time.Clock()

# ───────────────────────── CARREGAR IMAGENS ──────────────────────
fundo  = pygame.image.load("imagens/background.png").convert()
fundo  = pygame.transform.scale(fundo, (WIDTH, HEIGHT))

costas = pygame.image.load("imagens/cartafundo.png").convert_alpha()
costas = pygame.transform.scale(costas, (CARD_W, CARD_H))

frentes = [
    pygame.image.load(f"imagens/carta{i}.png").convert_alpha()
    for i in range(1, PAIRS + 1)
]

# ───────────────────────── CRIAR CARTAS ──────────────────────────
# duplica, embaralha e associa um pair_id a cada superfície
baralho = []
for pair_id, img in enumerate(frentes):
    surf = pygame.transform.scale(img, (CARD_W, CARD_H))
    baralho.extend([
        {"front": surf, "pair_id": pair_id},
        {"front": surf, "pair_id": pair_id},
    ])

random.shuffle(baralho)

cards = []
for i, card_info in enumerate(baralho):
    row, col = divmod(i, COLS)
    x = MARGIN_X + col * (CARD_W + GAP_X)
    y = MARGIN_Y + row * (CARD_H + GAP_Y)
    cards.append({
        "rect"     : pygame.Rect(x, y, CARD_W, CARD_H),
        "front"    : card_info["front"],
        "pair_id"  : card_info["pair_id"],
        "shown"    : False,
        "matched"  : False,
    })

# ───────────────────────── LÓGICA DE JOGO ────────────────────────
first, second   = None, None     # índices das duas cartas viradas
flip_start_time = 0              # milissegundos do segundo clique

running = True
while running:
    # 1) ── eventos ───────────────────────────────────────────────
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN and second is None:
            pos = pygame.mouse.get_pos()
            for idx, card in enumerate(cards):
                if card["rect"].collidepoint(pos) and not card["shown"]:
                    card["shown"] = True
                    if first is None:
                        first = idx
                    elif idx != first:
                        second = idx
                        flip_start_time = pygame.time.get_ticks()
                    break

    # 2) ── verificação de par ────────────────────────────────────
    if first is not None and second is not None:
        if pygame.time.get_ticks() - flip_start_time > 800:  # 0,8 s
            if cards[first]["pair_id"] == cards[second]["pair_id"]:
                cards[first]["matched"]  = True
                cards[second]["matched"] = True
            else:
                cards[first]["shown"]  = False
                cards[second]["shown"] = False
            first, second = None, None

    # 3) ── desenhar ──────────────────────────────────────────────
    screen.blit(fundo, (0, 0))
    for card in cards:
        if card["shown"] or card["matched"]:
            screen.blit(card["front"], card["rect"])
        else:
            screen.blit(costas, card["rect"])

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
