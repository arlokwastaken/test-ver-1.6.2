#italian version of the game (test version 1.6.2)

# game designed and developed by Leonardo! (15 years old as of 3/8/25) with extensive help from ChatGPT3.5 and copilot
# most of the programming and debugging done by me, Leonardo, but explanation of various functions and correction of certain errors was done by ChatGPT3.5
# game not for mass publication, but to learn to program in python
# to play use the arrow keys or WASD to move, left mouse button to rotate the sword
# GAME IN DEVELOPMENT, NOT ALL FEATURES IMPLEMENTED!!
# version 1.6.2 (1 is the game, 6 is the version, 2 is the revision)
# game useful for building a programming portfolio, for learning to program in python and for fun (for me)
# all comments next to the code are indicative of the functionality of the code, to understand what each part does
# pixel art of the game created by me, ideas created by me, key design inspired by super mario world, colors and border are not identical but the shape is, walls are freely available on craftpix.net

#THE GAME IS DESIGNED FOR PYTHON 3.13 OR HIGHER, WITH PYGAME, RANDOM AND MATH LIBRARIES INSTALLED

#to use the game, recommended to have Python 3.13 or higher installed, open terminal or powershell (preferably cmd), indicate the folder-
#where the game is installed and type "python main.py" (without quotes) to start the game, if it doesn't work try "python3 main.py" or "py main.py"

#THE GAME CODE IS FREE TO ACCESS, THIS DOES NOT MEAN YOU CAN USE THE CODE FOR COMMERCIAL PURPOSES WITHOUT MY CONSENT.

import pygame   # library for the game
import random   # library for random numbers (object positions)
import math   # library for math functions (for circular movement)

pygame.init()
screen = pygame.display.set_mode((1920, 1080))
pygame.display.set_caption("game test ver:: 1.6.2")
clock = pygame.time.Clock()

# game initialization, with screen size and game window title

rows = 9
colons = 15
tile_map = [[0 for _ in range(colons)] for _ in range(rows)]

tile_size = 128
tile_images = []

for i in range(5):
    tile_img = pygame.image.load(f"assets/textures/tiles/tile_{i}.png").convert_alpha()
    tile_img = pygame.transform.scale(tile_img, (tile_size, tile_size))
    tile_images.append(tile_img)

tile_map = [
    [(4, 90), (1, 180), (4, 0), (4, 90), (1, 180), (1, 180), (1, 180), (1, 180), (1, 180), (4, 0), (0, 0), (4, 90), (1, 180), (1, 180), (4, 0)],
    [(1, -90), (3, 0), (1, 90), (1, -90), (3, 0), (3, 0), (3, 0), (3, 0), (3, 0), (1, 90), (0, 0), (1, -90), (3, 0), (3, 0), (1, 90)],
    [(1, -90), (3, 0), (1, 90), (1, -90), (3, 0), (3, 0), (3, 0), (3, 0), (3, 0), (1, 90), (0, 0), (1, -90), (3, 0), (3, 0), (1, 90)],
    [(1, -90), (3, 0), (1, 90), (4, 180), (1, 0), (1, 0), (1, 0), (2, 0), (3, 0), (1, 90), (0, 0), (1, -90), (3, 0), (3, 0), (1, 90)],
    [(1, -90), (3, 0), (1, 90), (0, 0), (0, 0), (0, 0), (0, 0), (1, -90), (3, 0), (1, 90), (0, 0), (1, -90), (3, 0), (3, 0), (1, 90)],
    [(1, -90), (3, 0), (1, 90), (0, 0), (0, 0), (0, 0), (0, 0), (1, -90), (3, 0), (1, 90), (0, 0), (1, -90), (3, 0), (3, 0), (1, 90)],
    [(1, -90), (3, 0), (2, 180), (1, 180), (1, 180), (1, 180), (1, 180), (2, -90), (3, 0), (2, 180), (1, 180), (2, -90), (3, 0), (3, 0), (1, 90)],
    [(1, -90), (3, 0), (3, 0), (3, 0), (3, 0), (3, 0), (3, 0), (3, 0), (3, 0), (3, 0), (3, 0), (3, 0), (3, 0), (3, 0), (1, 90)],
    [(4, 180), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (4, -90)],
]


player_img_orig = pygame.transform.scale(
    pygame.image.load("assets/textures/players/player.png").convert_alpha(),
    (60, 60) # loads the player image and resizes it to 60x60 pixels
) 

sword_img = pygame.transform.scale(
    pygame.image.load("assets/textures/items/sword.png").convert_alpha(),
    (50, 50)
)

key_img = pygame.transform.scale(
    pygame.image.load("assets/textures/items/key.png").convert_alpha(),
    (50, 50)
)

enemy_img_orig = pygame.transform.scale(
    pygame.image.load("assets/textures/players/enemy.png").convert_alpha(),
    (60, 60)
)

# loads the images for player, sword, key and enemy

x, y = 140, 140
width, height = 60, 60
speed = 6.5
angle = 0
radius = 60
player_dir = 0  # angle in radians, 0 = right

# player info: position, size, speed, angle (for sword), radius (for sword) and player_dir (player direction)

rotation_active = False
rotation_progress = 0

# sword info

key = pygame.Rect(random.randint(1450, 1800), random.randint(200, 500), 30, 30)

door = pygame.Rect(945, 600, 255, 40)

# key and door, with position and size

enemy = pygame.Rect(door.centerx - 30 - 100, door.centery - 30 - 400, 60, 60)
enemy_speed = 4
enemy_dir = 0  # enemy direction (in radians)

enemy_2 = pygame.Rect(door.centerx - 30 - 300, door.centery - 30 - 400, 60, 60)
enemy_2_speed = 4
enemy_2_dir = 0  # enemy 2 direction

# enemy, position, size and speed

items = [
    pygame.Rect(random.randint(1450, 1800), random.randint(200, 500), 40, 40),
]

# objects (sword and key), with position and size

held_item = None

# check sword and key, if the player has picked up an item

has_key = False
door_open = False
enemy_released = False

# key state, if the player has the key and if the door is open, and if the enemy is released

walls = [
    pygame.Rect(300, 0, 200, 720),
    pygame.Rect(485, 520, 460, 200),
    pygame.Rect(1200, 0, 200, 800)
]

# obstacles, with position and size

def collide_with_walls(rect):
    for wall in walls:
        if rect.colliderect(wall):
            return True
    return False

# check collision between player and obstacles

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            rotation_active = True
            rotation_progress = 0

# activates sword rotation when left mouse button is clicked

    keys = pygame.key.get_pressed()

    if rotation_active:
        angle += 0.3
        rotation_progress += 0.3
        if rotation_progress >= 2 * math.pi:
            rotation_active = False

# updates sword angle and rotation progress

    dir_x = 0
    dir_y = 0

    if keys[pygame.K_w] or keys[pygame.K_UP]:
        dir_y -= 1   # up
    if keys[pygame.K_s] or keys[pygame.K_DOWN]:
        dir_y += 1   # down
    if keys[pygame.K_a] or keys[pygame.K_LEFT]:
        dir_x += 1   # left
    if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
        dir_x -= 1   # right

    if dir_x != 0 or dir_y != 0:
        # calculates angle in radians, inverting y because y axis in pygame increases downward
        player_dir = math.atan2(-dir_y, dir_x)
    else:
        # keep last direction if nothing is pressed (optional)
        pass

    new_x, new_y = x, y
    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        new_x -= speed
    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        new_x += speed

    player_rect_x = pygame.Rect(new_x, y, width, height)
    if not collide_with_walls(player_rect_x):
        x = new_x

    if keys[pygame.K_UP] or keys[pygame.K_w]:
        new_y -= speed
    if keys[pygame.K_DOWN] or keys[pygame.K_s]:
        new_y += speed

    player_rect_y = pygame.Rect(x, new_y, width, height)
    if not collide_with_walls(player_rect_y):
        y = new_y

# updates player position based on pressed keys

    # Update enemy position and direction if released
    for i, (e, e_speed) in enumerate([(enemy, enemy_speed), (enemy_2, enemy_2_speed)]):
        if e and enemy_released:
            dx = x - e.x
            dy = y - e.y
            dist = math.hypot(dx, dy)

            if dist != 0:
                dx /= dist
                dy /= dist

            new_x = e.x + dx * e_speed
            new_y = e.y + dy * e_speed

            new_rect = pygame.Rect(new_x, new_y, e.width, e.height)

            if not collide_with_walls(new_rect):
                e.x = new_x
                e.y = new_y
            else:
                new_rect_x = pygame.Rect(e.x + dx * e_speed, e.y, e.width, e.height)
                if not collide_with_walls(new_rect_x):
                    e.x = new_rect_x.x
                else:
                    new_rect_y = pygame.Rect(e.x, e.y + dy * e_speed, e.width, e.height)
                    if not collide_with_walls(new_rect_y):
                        e.y = new_rect_y.y

            # Update enemy direction towards player
            if dist != 0:
                direction = math.atan2(dy, dx)  # angle in radians
            else:
                direction = 0

            if i == 0:
                enemy_dir = direction
            else:
                enemy_2_dir = direction

# limits player position within the screen

    new_x = max(0, min(x, 1920 - width))
    new_y = max(0, min(y, 1080 - height))

    x, y = new_x, new_y

    player_rect = pygame.Rect(x, y, width, height)

# updates player position and creates a rectangle for the player

    if held_item:
        corrected_angle = angle + math.pi / 2  # angle correction for sword rotation
        held_item.x = x + width // 2 + int(radius * math.cos(angle)) - held_item.width // 2
        held_item.y = y + height // 2 + int(radius * math.sin(angle)) - held_item.height // 2

# updates held item (sword or key) position based on player position and sword angle

    if enemy and held_item and enemy.colliderect(held_item):
        enemy = None

    if enemy_2 and held_item and enemy_2.colliderect(held_item):
        enemy_2 = None

    if enemy and enemy.colliderect(player_rect):
        running = False

    for item in items[:]:
        if player_rect.colliderect(item):
            held_item = item
            items.remove(item)
            break

    if player_rect.colliderect(key):
        has_key = True

    if has_key and player_rect.colliderect(door) and not door_open:
        door_open = True
        enemy_released = True

# checks if player picked up an item, if so removes it from items list and sets as held item, also checks if player has key and opened door

    goal = pygame.Rect(500, 0, 700, 100)

    game_over = False
    win = False

    if player_rect.colliderect(goal):
        game_over = True
        win = True

    if enemy and enemy.colliderect(player_rect):
        game_over = True
        win = False
    if enemy_2 and enemy_2.colliderect(player_rect):
        game_over = True
        win = False

    if game_over:
        in_game_over_screen = True
        while in_game_over_screen:
            screen.fill((0, 0, 0))
            font = pygame.font.Font(None, 100)
            small_font = pygame.font.Font(None, 40)

            if win:
                text = font.render("You won!", True, (0, 255, 0))
            else:
                text = font.render("You lost!", True, (255, 0, 0))

            retry_text = small_font.render("want to play again? r to play again, esc to exit", True, (255, 255, 255))
            text_rect = text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 - 50))
            retry_text_rect = retry_text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 + 50))

            screen.blit(text, text_rect)
            screen.blit(retry_text, retry_text_rect)
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        # Reset game state
                        x, y = 140, 140
                        angle = 0
                        rotation_active = False
                        rotation_progress = 0
                        key = pygame.Rect(random.randint(1450, 1800), random.randint(200, 500), 30, 30)
                        enemy = pygame.Rect(door.centerx - 30 - 100, door.centery - 30 - 400, 60, 60)
                        enemy_2 = pygame.Rect(door.centerx - 30 - 300, door.centery - 30 - 400, 60, 60)
                        held_item = None
                        has_key = False
                        door_open = False
                        enemy_released = False
                        items = [pygame.Rect(random.randint(1450, 1800), random.randint(200, 500), 40, 40)]
                        game_over = False
                        win = False
                        running = True
                        in_game_over_screen = False  # exits game over loop
                    elif event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        exit()
                if not game_over:
                    break

    for row_index, row in enumerate(tile_map):
        for col_index, cell in enumerate(row):
            if isinstance(cell, tuple):
                tile_id, rotation = cell
            else:
                tile_id = cell
                rotation = 0

            tile_img = tile_images[tile_id]
            rotated_tile = pygame.transform.rotate(tile_img, rotation)
            tile_x = col_index * tile_size
            tile_y = row_index * tile_size

            screen.blit(rotated_tile, (tile_x, tile_y))
        
    for wall in walls:
        pygame.draw.rect(screen, (139, 69, 19), wall, 15)  # Brown color

    if not door_open:
        pygame.draw.rect(screen, (139, 69, 19), door) # closed door (brown)
        pygame.draw.rect(screen, (0, 0, 0), door, 1) # Thin black border
    else:
        pygame.draw.rect(screen, (255, 204, 204), door)  # open door (light reddish)

    # Rotate and draw player based on player_dir
    player_dir_corrected = player_dir + math.pi / 2  # orientation correction
    player_img = pygame.transform.rotate(player_img_orig, -math.degrees(player_dir_corrected) + 180)
    player_rect_rotated = player_img.get_rect(center=(x + width // 2, y + height // 2))
    screen.blit(player_img, player_rect_rotated)

    # Rotate and draw enemy 1 if present
    if enemy:
        enemy_img = pygame.transform.rotate(enemy_img_orig, -math.degrees(enemy_dir) - 90)
        enemy_rect_rotated = enemy_img.get_rect(center=enemy.center)
        screen.blit(enemy_img, enemy_rect_rotated)

    # Rotate and draw enemy 2 if present
    if enemy_2:
        enemy_img_2 = pygame.transform.rotate(enemy_img_orig, -math.degrees(enemy_2_dir) - 90)
        enemy_2_rect_rotated = enemy_img_2.get_rect(center=enemy_2.center)
        screen.blit(enemy_img_2, enemy_2_rect_rotated)

    # Draw objects in items list (sword etc)
    for item in items:
        screen.blit(sword_img, item)

    # Draw rotated sword around player only if held
    if held_item and held_item.width == 40:
        rotated_sword = pygame.transform.rotate(sword_img, -math.degrees(angle))
        sword_rect = rotated_sword.get_rect(center=(held_item.centerx, held_item.centery))
        screen.blit(rotated_sword, sword_rect)

    # Draw key if player doesn't have it
    if not has_key:
        screen.blit(key_img, key)  # Key (sprite)

    pygame.draw.rect(screen, (255, 215, 0), goal, 10)  # Goal (gold yellow)

# draws player, enemy and objects on screen, general rendering

    pygame.display.flip()
    clock.tick(60)

# updates screen and limits frame rate to 60 FPS, possible to change value to increase or decrease frame rate, I plan to add an option to change frame rate (in game) in the future

pygame.quit()

# closes the game when the main loop ends