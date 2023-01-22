import pygame
from random import randint, shuffle










pygame.init()
W, H = 640, 480
SW, SH = 30, 30
display = pygame.display.set_mode((W, H))
screen = display.copy()

squares = []

for x in range(randint(0, 20)):
    squares.append([pygame.Rect(x * 40, 10, SW, SH), False, "green", False])

while True:
    e = pygame.event.wait()
    if e.type == pygame.QUIT or e.type == pygame.KEYUP and e.key == 27:
        break
    elif e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
        for x in squares:
            x[3] = False
        for square in squares:
            if square[0].collidepoint(e.pos):
                square[1] = True
                square[3] = True
    elif e.type == pygame.MOUSEBUTTONUP and e.button == 1:
        for square in squares:
            if square[1] == True:
                square[1] = False
                square[0].center = e.pos
    elif e.type == pygame.MOUSEMOTION and e.buttons[0]:
        for square in squares:
            if square[1] == True:
                square[0].center = e.pos
    elif e.type == pygame.KEYDOWN and e.key == pygame.K_l:
        for i, square in enumerate(squares):
            if square[3] == True:
                if i > 0:
                    squares[i], squares[i - 1] = squares[i - 1], squares[i]
    elif e.type == pygame.KEYDOWN and e.key == pygame.K_e:
        for i, square in enumerate(squares):
            if square[3] == True:
                if i < len(squares) - 1:
                    squares[i], squares[i + 1] = squares[i + 1], squares[i]
    else:
        print(e)
    screen.fill((255, 255, 255))
    for square in squares:
        pygame.draw.rect(screen, square[2], square[0])
    display.blit(screen, (0, 0))
    pygame.display.flip()

pygame.quit()