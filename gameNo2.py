import pygame
import sys
import random
pygame.init()

width = 1000
height = 600
speed = 10

score = 0

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BG_COLOR = (255, 51, 255)

enemy_size = 40
enemy_pos = [random.randint(0, width-enemy_size), 0]

player_size = 40
player_pos = [width/2, height-2*player_size]
enemy_list = [enemy_pos]

screen = pygame.display.set_mode((width, height))

game_over = False

myfont = pygame.font.SysFont("monospace", 35)
clock = pygame.time.Clock()

def set_level(score, speed):
    if score < 100:
        speed = 10
    elif score < 150:
        speed = 12
    elif score <200:
        speed = 15
    else:
        speed = 20
    #speed = (score/5) + 1
    return speed

def drop_enemies( enemy_list ):
    delay = random.random()
    if len(enemy_list) < 30 and delay < 0.2:
        x_pos = random.randint(0, width-enemy_size)
        y_pos = 0
        enemy_list.append([x_pos, y_pos])

def draw_enemies(enemy_list):
    for enemy_pos in enemy_list:
        pygame.draw.rect(screen, BLUE, (enemy_pos[0], enemy_pos[1], enemy_size, enemy_size))

def update_position(enemy_list, score):
    for idx,enemy_pos in enumerate(enemy_list):
        if 0 <= enemy_pos[1] < height:
            enemy_pos[1] += speed
        else:
            enemy_list.pop(idx)
            score += 1
    return score

def collision_check(enemy_list, player_pos):
    for enemy_pos in enemy_list:
        if detect_collision(enemy_pos, player_pos):
            return True
    return False

def detect_collision(player_pos, enemy_pos):
    p_x = player_pos[0]
    p_y = player_pos[1]

    e_x = enemy_pos[0]
    e_y = enemy_pos[1]

    if(e_x >= p_x and e_x <(p_x + player_size)) or (e_x <= p_x < (e_x + enemy_size)):
        if(e_y >= p_y and e_y < (p_y + player_size)) or (p_y >= e_y and p_y < (e_y + enemy_size)):
            return True
    return False

while not game_over:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.KEYDOWN:
            x = player_pos[0]
            y = player_pos[1]
            if event.key == pygame.K_LEFT:
                x -= player_size
            elif event.key == pygame.K_RIGHT:
                x += player_size
            player_pos = [x, y]
    screen.fill(BG_COLOR)

    drop_enemies(enemy_list)
    score = update_position(enemy_list, score)
    speed = set_level(score, speed)
    text = "Score:" + str(score)
    label = myfont.render(text, 1, (255, 255, 0))
    screen.blit(label, (width-200, height-40))
    if collision_check(enemy_list, player_pos):
        game_over = True
        break
    draw_enemies(enemy_list)

    pygame.draw.rect(screen, (229, 255, 204), (player_pos[0], player_pos[1], player_size, player_size))
    clock.tick(30)
    pygame.display.update()
