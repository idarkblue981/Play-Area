from pygame import mixer
import pygame
from random import choice, randint
from time import sleep

pygame.init()


# Screen, window icon and caption
screen = pygame.display.set_mode((1200, 600))
pygame.display.set_caption("Play Area")
window_icon = pygame.image.load("./Assets/Art/window-icon.png")
pygame.display.set_icon(window_icon)


# Background, music and font
background = pygame.image.load("./Assets/Art/background.png")
mixer.music.load("./Assets/Music/music.wav")
mixer.music.play(-1)
font = pygame.font.Font(None, 74)


# Player settings
player_speed = 2
player = pygame.image.load("./Assets/Art/player.png")
playerX = 1200 / 2 - 32
playerY = 600 / 2 - 32
playerX_change, playerY_change = 0, 0


# Enemy settings
enemy_image = pygame.image.load("./Assets/Art/enemy.png")
enemies = []
enemy_speed = 1
enemy_spawn_rate = 30  # Lower is faster (frames)
last_spawn_time = pygame.time.get_ticks()


def reset_game():
    global playerX, playerY, playerX_change, playerY_change, enemies, start_time, last_spawn_time
    playerX = 1200 / 2 - 32
    playerY = 600 / 2 - 32
    playerX_change, playerY_change = 0, 0
    enemies = []
    start_time = pygame.time.get_ticks()
    last_spawn_time = pygame.time.get_ticks()


def spawn_enemy():
    if len(enemies) < 20:
        side = choice(["top", "bottom", "left", "right"])
        diagonal = choice([True, False])
        direction = choice([-1, 1])
        
        if side == "top":
            x = randint(0, 1200 - enemy_image.get_width())
            y = -enemy_image.get_height()
            dx = direction * enemy_speed
            dy = direction * enemy_speed if diagonal else enemy_speed
        elif side == "bottom":
            x = randint(0, 1200 - enemy_image.get_width())
            y = 600
            dx = direction * enemy_speed
            dy = direction * -enemy_speed if diagonal else -enemy_speed
        elif side == "left":
            x = -enemy_image.get_width()
            y = randint(0, 600 - enemy_image.get_height())
            dx = direction * enemy_speed if diagonal else enemy_speed
            dy = direction * enemy_speed
        elif side == "right":
            x = 1200
            y = randint(0, 600 - enemy_image.get_height())
            dx = direction * -enemy_speed if diagonal else -enemy_speed
            dy = direction * enemy_speed
        
        enemies.append([x, y, dx, dy])


def check_collision(ex, ey, px, py, pw, ph):
    if ex < px + pw and ex + enemy_image.get_width() > px and ey < py + ph and ey + enemy_image.get_height() > py:
        return True
    return False


def game_over_screen(score):
    screen.blit(background, (0, 0))
    game_over_text = font.render(f"Game Over! Your Score: {int(score)}", True, (255, 0, 0))
    screen.blit(game_over_text, (300, 250))
    pygame.display.update()
    sleep(5)


reset_game()


# Main loop
running = True
while running:
    screen.blit(background, (0, 0))

    current_time = pygame.time.get_ticks()
    elapsed_time = (current_time - start_time) / 1000

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_UP:
                playerY_change = -player_speed
            elif event.key == pygame.K_LEFT:
                playerX_change = -player_speed
            elif event.key == pygame.K_RIGHT:
                playerX_change = player_speed
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0
            if event.key == pygame.K_UP:
                playerY_change = player_speed


    # Update player position
    playerX += playerX_change
    playerY += playerY_change


    # Boundary checks
    if playerX < 10:
        playerX = 10
    elif playerX > 1200 - player.get_width() - 10:
        playerX = 1200 - player.get_width() - 10
    if playerY < 10:
        playerY = 10
    elif playerY > 600 - player.get_height() - 10:
        playerY = 600 - player.get_height() - 10


    # Enemy spawning
    if current_time - last_spawn_time > enemy_spawn_rate:
        spawn_enemy()
        last_spawn_time = current_time


    # Update enemies and check for collisions
    for enemy in enemies[:]:
        enemy[0] += enemy[2]
        enemy[1] += enemy[3]
        
        if enemy[0] < -enemy_image.get_width() or enemy[0] > 1200 or enemy[1] < -enemy_image.get_height() or enemy[1] > 600:
            enemies.remove(enemy)
        else:
            if check_collision(enemy[0], enemy[1], playerX, playerY, player.get_width(), player.get_height()):
                game_over_screen(elapsed_time)
                reset_game()
                break


    # Player and enemies
    screen.blit(player, (playerX, playerY))
    for enemy in enemies:
        screen.blit(enemy_image, (enemy[0], enemy[1]))


    # Score
    score_text = font.render(f"Score: {int(elapsed_time)}", True, (255, 255, 255))
    screen.blit(score_text, (10, 10))


    pygame.display.update()