import pygame
import random
pygame.init()

screen = pygame.display.set_mode([500, 500])
clock = pygame.time.Clock()
pressstart = pygame.font.Font("Press_Start_2P/PressStart2P-Regular.ttf", 28)
enemy_img = pygame.image.load("enemy.png")
player_img = pygame.image.load("player.png")
colorImage = pygame.Surface(enemy_img.get_size()).convert_alpha()
colorImage.fill((255, 0, 0))
enemy_img.blit(colorImage, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
stage = "start"
stages = ["start", "intro", "game"]
level = 1
pos_enemy = []
player_pos = [250, 500 - 32]
load_width = 0
move_left = False
move_right = False
projs = []
enemy_proj = []

ticks= 0 

def start():
    space = pressstart.render("PRESS SPACE", True, (255, 255, 255))
    screen.blit(space, (125, 250))
    for event in pygame.event.get():
        try:
            if event.key == pygame.K_SPACE:
                return True
            if event.type == pygame.QUIT:
                exit()
        except:
            pass  # mousemove
    return False


def intro():
    global load_width, pos_enemy
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
    enemies = [0, 4, 8, 12, 16, 40]
    try:
        enemies = enemies[level]
    except:
        end = pressstart.render("YOU WIN", True, (255, 255, 255))
        screen.blit(end, (125, 250))
        return False
    spacing = 500 / 4
    if enemies % 4 != 0:
        spacing = 500 / 3
    spacing += 16  # sprite offset
    for i in range(0, enemies):
        cnt = i
        if cnt % 4 == 0:
            cnt += 1
        row_offset = ((cnt - 1) // 4) * 30
        screen.blit(enemy_img, (spacing * (i % 4) * load_width, 100 + row_offset))
        load_width += 0.001
    if load_width > 1:
        for i in range(enemies):
            cnt = i
            if cnt % 4 == 0:
                cnt += 1
            row_offset = ((cnt - 1) // 4) * 30
            for _ in range(level):  # multilives
                pos_enemy.append(
                    (int(spacing * (i % 4) * load_width), int(100 + row_offset))
                )
        return True
    return False


def game():
    global move_left, move_right, level, stage, load_width
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                fire(player_pos[0])
            if event.key == pygame.K_LEFT:
                move_left = True
            elif event.key == pygame.K_RIGHT:
                move_right = True
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                move_left = False
            elif event.key == pygame.K_RIGHT:
                move_right = False
    for i, v in enumerate(projs):
        if not chech_hit(pygame.Rect(v[0], v[1], 10, 10)):
            pygame.draw.rect(screen, (0, 255, 0), (v[0], v[1], 10, 10))
            projs[i][1] -= 10

    if move_left:
        player_pos[0] -= 5
    elif move_right:
        player_pos[0] += 5
    if player_pos[0] > 500:
        player_pos[0] = 464
    if player_pos[0] < 0:
        player_pos[0] = 0
    screen.blit(player_img, player_pos)
    for x, y in pos_enemy:
        screen.blit(enemy_img, (x, y))
    if len(pos_enemy) != 0:
        firing = random.choices(pos_enemy,k=level)
        for firing in firing:
            enemyfire(firing[0],firing[1])
    for  index, i in enumerate(enemy_proj):
        if not is_lost(pygame.Rect(i[0], i[1], 10, 10)):
            pygame.draw.rect(screen, (255, 0, 0), (i[0], i[1], 10, 10))
            enemy_proj[index][1] += 3 * level


    if len(pos_enemy) == 0:
        level += 1
        load_width = 0
        stage = "intro"


def fire(x):
    projs.append([x + 16, 464])
def enemyfire(x,y):
    if ticks % 120 == 0:
        enemy_proj.append([x + 16,y])

def chech_hit(obj):
    global pos_enemy
    enemy = []
    for i in pos_enemy:
        col = obj.colliderect(pygame.Rect(i[0], i[1], 32, 32))
        if col:
            col = pygame.Rect(i[0], i[1], 32, 32)
            coord = (col.left, col.top)

            pos_enemy.pop(pos_enemy.index(coord))
            projs.pop(projs.index([obj.left, obj.top]))
            return True
    return False
def is_lost(proj):
    global player_pos, stage
    if proj.colliderect(pygame.Rect(player_pos[0], player_pos[1], 32, 32)):
        stage = "lose"
        return True
    return False

while True:
    screen.fill((0, 0, 0))
    if stage == "start":
        if start():
            stage = "intro"
    elif stage == "intro":
        if intro():
            stage = "game"
    elif stage == "game":
        game()
    elif stage == "lose":
        end = pressstart.render("YOU LOSE", True, (255, 255, 255))
        screen.blit(end, (125, 250))
    pygame.display.update()
    pygame.display.flip()
    clock.tick(120)
    ticks += 1
