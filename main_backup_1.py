#versione italiana del gioco (test versione 1.6.2))

# gioco progettato e sviluppato da Leonardo! (15 anni al momento del 3/8/25) ampio aiuto di ChatGPT3.5 e copilot
# il grosso della programmazione ed il debugging fatto da me, Leonardo, ma la spiegazione di funzioni varie e la correzione di certi errori è stata fatta da ChatGPT3.5
# gioco non per la pubblicazione di massa, ma per imparare a programmare in python
# per giocare usare le frecce direzionali o i tasti WASD per muoversi, tasto sinistro del mouse per ruotare la spada
# GIOCO IN SVILUPPO, NON TUTTE LE FUNZIONI SONO IMPLEMENTATE!!
# versione 1.6.2 (1 è il gioco, 6 è la versione, 2 è la revisione)
# gioco utile per costruire un portfolio di programmazione, per imparare a programmare in python e per divertirsi (per me)
# tutti i commenti accanto al codice sono indicativi della funzionalità del codice, per capire cosa fa ogni parte del codice
# pixel art del gioco create da me, idee create da me, il design della chiave sono ispirati da super mario world, i colori ed il bordo non sono identici ma la forma è quella, le pareti sono a libero accesso su craftpix.net

#IL GIOCO è PROGETTATO PER PYTHON 3.13 O SUPERIORE, CON LA LIBRERIA PYGAME, RANDOM E MATH INSTALLATE

#per usare il gioco, consigliato avere installato Python 3.13 o superiore, aprire il terminale oppure powershell (cmd preferibilmente), indicare la cartella-
#dove il gioco è installato e digitare "python main.py" (senza virgolette) per avviare il gioco, se non funziona provare a usare "python3 main.py" o "py main.py"

#IL CODICE GIOCO È A LIBERO ACCESSO, CIÒ NON VUOL DIRE CHE SI POSSA USUFRUIRE DEL CODICE PER SCOPI COMMERCIALI SENZA IL MIO CONSENSO.

import pygame   # libreria per il gioco
import random   # libreria per i numeri casuali (posizione degli oggetti)
import math   # libreria per le funzioni matematiche (per il movimento circolare)

pygame.init()
screen = pygame.display.set_mode((1920, 1080))
pygame.display.set_caption("gioco test ver:: 1.6.2")
clock = pygame.time.Clock()

# inizializazione gioco, con dimensione dello schermo e titolo della finestra di gioco

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
    (60, 60) # carica l'immagine del giocatore e la ridimensiona a 60x60 pixel
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

# carica le immagini del giocatore, della spada, della chiave e del nemico

x, y = 140, 140
width, height = 60, 60
speed = 6.5
angle = 0
radius = 60
player_dir = 0  # angolo in radianti, 0 = destra

# informazioni del giocatore, posizione, dimensioni, velocità, angolo (per la spada), raggio (per la spada) e player_dir (direzione del giocatore)

rotation_active = False
rotation_progress = 0

# informazioni spada

key = pygame.Rect(random.randint(1450, 1800), random.randint(200, 500), 30, 30)

door = pygame.Rect(945, 600, 255, 40)

# chiave e porta, con posizione e dimensioni

enemy = pygame.Rect(door.centerx - 30 - 100, door.centery - 30 - 400, 60, 60)
enemy_speed = 4
enemy_dir = 0  # direzione nemico (in radianti)

enemy_2 = pygame.Rect(door.centerx - 30 - 300, door.centery - 30 - 400, 60, 60)
enemy_2_speed = 4
enemy_2_dir = 0  # direzione nemico 2

# nemico, posizione, dimensioni e velocità

items = [
    pygame.Rect(random.randint(1450, 1800), random.randint(200, 500), 40, 40),
]

# oggetti (spada e chiave), con posizione, dimensioni

held_item = None

# check spada e chiave, se il giocatore ha preso un oggetto

has_key = False
door_open = False
enemy_released = False

# stato della chiave, se il giocatore ha la chiave e se la porta è aperta, e se il nemico è rilasciato

walls = [
    pygame.Rect(300, 0, 200, 720),
    pygame.Rect(485, 520, 460, 200),
    pygame.Rect(1200, 0, 200, 800)
]

# ostacoli, con posizione e dimensioni

def collide_with_walls(rect):
    for wall in walls:
        if rect.colliderect(wall):
            return True
    return False

# check collisione tra il giocatore e gli ostacoli

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

# attiva la rotazione della spada quando si clicca con il tasto sinistro del mouse

    keys = pygame.key.get_pressed()

    if rotation_active:
        angle += 0.3
        rotation_progress += 0.3
        if rotation_progress >= 2 * math.pi:
            rotation_active = False

# aggiorna l'angolo della spada e il progresso della rotazione

    dir_x = 0
    dir_y = 0

    if keys[pygame.K_w] or keys[pygame.K_UP]:
        dir_y -= 1   # su
    if keys[pygame.K_s] or keys[pygame.K_DOWN]:
        dir_y += 1   # giù
    if keys[pygame.K_a] or keys[pygame.K_LEFT]:
        dir_x += 1   # sinistra
    if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
        dir_x -= 1   # destra

    if dir_x != 0 or dir_y != 0:
        # calcola l'angolo in radianti, invertendo y perché l'asse y in pygame cresce verso il basso
        player_dir = math.atan2(-dir_y, dir_x)
    else:
        # mantieni l'ultima direzione se non premi nulla (opzionale)
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

# aggiorna la posizione del giocatore in base ai tasti premuti

    # Aggiorna posizione e direzione nemici se rilasciati
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

            # Aggiorna la direzione del nemico verso il giocatore
            if dist != 0:
                direction = math.atan2(dy, dx)  # angolo in radianti
            else:
                direction = 0

            if i == 0:
                enemy_dir = direction
            else:
                enemy_2_dir = direction

# limita la posizione del giocatore all'interno dello schermo

    new_x = max(0, min(x, 1920 - width))
    new_y = max(0, min(y, 1080 - height))

    x, y = new_x, new_y

    player_rect = pygame.Rect(x, y, width, height)

# aggiorna la posizione del giocatore e crea un rettangolo per il giocatore

    if held_item:
        corrected_angle = angle + math.pi / 2  # correzione dell'angolo per la rotazione della spada
        held_item.x = x + width // 2 + int(radius * math.cos(angle)) - held_item.width // 2
        held_item.y = y + height // 2 + int(radius * math.sin(angle)) - held_item.height // 2

# aggiorna la posizione dell'oggetto tenuto (spada o chiave) in base alla posizione del giocatore e all'angolo della spada

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

# controlla se il giocatore ha raccolto un oggetto, se sì lo rimuove dalla lista degli oggetti e lo imposta come oggetto tenuto, inoltre controlla se il giocatore ha la chiave e se ha aperto la porta

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
                text = font.render("Hai vinto!", True, (0, 255, 0))
            else:
                text = font.render("Hai perso!", True, (255, 0, 0))

            retry_text = small_font.render("gioca ancora? r per giocare ancora, esc per uscire", True, (255, 255, 255))
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
                        # Reset stato del gioco
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
                        in_game_over_screen = False  # esce dal ciclo di game over
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
        pygame.draw.rect(screen, (139, 69, 19), wall, 15)  # Colore marrone

    if not door_open:
        pygame.draw.rect(screen, (139, 69, 19), door) # porta chiusa (marrone)
        pygame.draw.rect(screen, (0, 0, 0), door, 1) # Bordo nero sottile
    else:
        pygame.draw.rect(screen, (255, 204, 204), door)  # porta aperta (rossastro chiaro)

    # Ruota e disegna il giocatore in base alla direzione player_dir
    player_dir_corrected = player_dir + math.pi / 2  # correzione orientamento
    player_img = pygame.transform.rotate(player_img_orig, -math.degrees(player_dir_corrected) + 180)
    player_rect_rotated = player_img.get_rect(center=(x + width // 2, y + height // 2))
    screen.blit(player_img, player_rect_rotated)

    # Ruota e disegna il nemico 1 se presente
    if enemy:
        enemy_img = pygame.transform.rotate(enemy_img_orig, -math.degrees(enemy_dir) - 90)
        enemy_rect_rotated = enemy_img.get_rect(center=enemy.center)
        screen.blit(enemy_img, enemy_rect_rotated)

    # Ruota e disegna il nemico 2 se presente
    if enemy_2:
        enemy_img_2 = pygame.transform.rotate(enemy_img_orig, -math.degrees(enemy_2_dir) - 90)
        enemy_2_rect_rotated = enemy_img_2.get_rect(center=enemy_2.center)
        screen.blit(enemy_img_2, enemy_2_rect_rotated)

    # Disegna gli oggetti nella lista items (spada ecc)
    for item in items:
        screen.blit(sword_img, item)

    # Disegna la spada ruotata attorno al giocatore solo se la tiene in mano
    if held_item and held_item.width == 40:
        rotated_sword = pygame.transform.rotate(sword_img, -math.degrees(angle))
        sword_rect = rotated_sword.get_rect(center=(held_item.centerx, held_item.centery))
        screen.blit(rotated_sword, sword_rect)

    # Disegna la chiave se il giocatore non la possiede
    if not has_key:
        screen.blit(key_img, key)  # Chiave (sprite)

    pygame.draw.rect(screen, (255, 215, 0), goal, 10)  # Obiettivo (giallo oro)

# disegna il giocatore, il nemico e gli oggetti sullo schermo, rendering generale

    pygame.display.flip()
    clock.tick(60)

# aggiorna lo schermo e limita il frame rate a 60 FPS, possibile modificare il valore per aumentare o diminuire il frame rate, ho in mente di aggiungere un'opzione per modificare il frame rate (in game) in futuro

pygame.quit()

# chiude il gioco quando il ciclo principale termina