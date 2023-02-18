import pygame
from random import randrange

screen_width = 1200
screen_height = 800

tile_width = 50
tile_height = 50

border = 1
length = 1
direction = [0, 0]

time = 0
dt = 100
keydelay = False # 키 연속 입력 방지, 디버깅해서 추가했음

def random_position():
    return [randrange(0.5 * tile_width, screen_width - 0.5 * tile_width, tile_width), 
            randrange(0.5 * tile_height, screen_height - 0.5 * tile_height, tile_height)]
    
snake = pygame.rect.Rect([0, 0, tile_width - 2 * border, tile_height - 2 * border])
snake.center = random_position()
pieces = [snake.copy()]

food = snake.copy()
food.center = random_position()
screen = pygame.display.set_mode([screen_width, screen_height])
clock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        if event.type == pygame.KEYDOWN and keydelay == False:
            if event.key == pygame.K_LEFT and direction != [tile_width, 0]:
                direction = [-tile_width, 0]
            elif event.key == pygame.K_RIGHT and direction != [-tile_width, 0]:
                direction = [tile_width, 0]
            elif event.key == pygame.K_UP and direction != [0, tile_height]:
                direction = [0, -tile_height]
            elif event.key == pygame.K_DOWN and direction != [0, -tile_height]:
                direction = [0, tile_height]
            keydelay = True
    
    # 배경(검은색)
    screen.fill('black')
    
    # 자기 자신과 부딪히지 않기
    crush = pygame.Rect.collidelist(snake, pieces[:-1]) != -1
    
    # 창 끝으로 나가거나 부딪히면
    if snake.left < 0 or snake.right > screen_width or snake.top < 0 or snake.bottom > screen_height or crush:
        direction = [0, 0]
        print("Game Over")
        
        # 초기화
        length = 1
        snake.center = random_position()
        food.center = random_position()
        pieces = [snake.copy()]
        
    # 뱀모양 그리기
    [pygame.draw.rect(screen, 'blue', piece) for piece in pieces]
    
    # 음식 그리기
    [pygame.draw.rect(screen, 'red', food)]
    
    # 음식 먹으면 길이 증가 및 음식 위치 재선정
    if snake.center == food.center:
        length += 1
        #디버깅해서 음식 위치가 뱀 몸에 닿으면 위치 재선정
        while True:
            food.center = random_position()
            if food not in pieces:
                break
            
    # 방향을 반영하여 뱀 이동
    time_now = pygame.time.get_ticks()
    if time_now - time > dt:
        time = time_now
        snake.move_ip(direction)
        pieces.append(snake.copy())
        pieces = pieces[-length:]
        keydelay = False
    pygame.display.update()
    clock.tick(60)
    
pygame.quit()