import pygame, random
from algorithm import checkForWinner
pygame.init()

SCREEN = pygame.display.set_mode((WIDTH:=625, HEIGHT:=725))
CLOCK = pygame.Clock()
FPS = 30
GAMING = 1
CLEAR = 0
RED = 1
BLUE = 2
COLS,ROWS = 6,7

def createTable(): return [[CLEAR]*COLS for i in range(ROWS)]
def createGrid(zoom):
    x = 35//2
    y = 35//2
    positions = []
    for i in range(ROWS):
        positions.append([])
        for j in range(COLS):
            positions[i].append((x*zoom,y*zoom))
            x += 35
        y += 35
        x = 35//2
    return positions

def createGameMap(table, positions):
    game_map = {}
    for i in range(ROWS):
        for j in range(COLS):
            game_map[positions[i][j]] = table[i][j]
    return game_map

def mouseCollision(pos, mouse_pos,clicked):
    if not clicked:return False
    circle_rect = pygame.Rect(*pos,25,25)
    mouse_rect = pygame.Rect(*mouse_pos, 25,25)
    return circle_rect.colliderect(mouse_rect)

def updateMap(game_map, clicked, mouse_pos, turn):
    for pos in game_map:
        state = game_map[pos]
        if state != CLEAR:
            color = (255,0,0) if state == RED else (0,0,255)
            pygame.draw.circle(SCREEN, color, (pos[0], pos[1]), 35)
        elif mouseCollision(pos, mouse_pos,clicked) and state == CLEAR and canPlace(game_map, pos):
            game_map[pos] = turn
            turn = BLUE if turn == RED else RED
        else:
            pygame.draw.circle(SCREEN, (255,255,255), (pos[0], pos[1]), 35)
    return turn

def convertToGrid(game_map):
    grid = createTable()
    i,j = 0,0
    for pos in game_map:
        if j >= COLS:
            j = 0
            i += 1
        grid[i][j] = game_map[pos]
        j += 1
    return grid

def canPlace(game_map, pos):
    x = pos[0]
    y = pos[1]
    comparison = (x,y+(35*3))
    if comparison in game_map and game_map[comparison] != CLEAR:
        return True
    else:
        print(False)
    if comparison not in game_map and game_map[pos] == CLEAR:
        return True
    return False

game_map = createGameMap(createTable(),createGrid(3))
turn = random.choice([BLUE, RED])

while GAMING:
    mouse_pos = pygame.mouse.get_pos()
    clicked = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            GAMING = 0
        if event.type == pygame.MOUSEBUTTONDOWN:
            clicked = True
    
    SCREEN.fill((0,0,200))
    prev = turn
    turn = updateMap(game_map, clicked, mouse_pos, turn)
    pygame.display.flip()
    if prev != turn and checkForWinner(convertToGrid(game_map)):
        game_map = createGameMap(createTable(), createGrid(3))
    CLOCK.tick(FPS)
pygame.quit()