import pygame
import random
import os

pygame.init()

BLACK = (0, 0, 0)
size = [600, 800]
screen = pygame.display.set_mode(size)

done = False
clock = pygame.time.Clock()

def runGame():
    # Game variables
    score = 0
    game_over = False

    # Load images
    bomb_image = pygame.image.load('bomb.png')
    bomb_image = pygame.transform.scale(bomb_image, (50, 50))
    person_image = pygame.image.load('person4.png')
    person_image = pygame.transform.scale(person_image, (100, 100))

    bombs = []
    for i in range(5):
        rect = pygame.Rect(bomb_image.get_rect())
        rect.left = random.randint(0, size[0])
        rect.top = -100
        dy = random.randint(3, 9)
        bombs.append({'rect': rect, 'dy': dy})

    person = pygame.Rect(person_image.get_rect())
    person.left = size[0] // 2 - person.width // 2
    person.top = size[1] - person.height
    person_dx = 0

    global done
    while not done:
        clock.tick(30)
        screen.fill(BLACK)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
                break
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    person_dx = -5
                elif event.key == pygame.K_RIGHT:
                    person_dx = 5
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    person_dx = 0
                elif event.key == pygame.K_RIGHT:
                    person_dx = 0

        if not game_over:
            for bomb in bombs:
                bomb['rect'].top += bomb['dy']
                if bomb['rect'].top > size[1]:
                    bombs.remove(bomb)
                    rect = pygame.Rect(bomb_image.get_rect())
                    rect.left = random.randint(0, size[0])
                    rect.top = -100
                    dy = random.randint(3, 9)
                    bombs.append({'rect': rect, 'dy': dy})

                if bomb['rect'].colliderect(person):
                    game_over = True
                    break

            person.left = person.left + person_dx

            if person.left < 0:
                person.left = 0
            elif person.left > size[0] - person.width:
                person.left = size[0] - person.width

            screen.blit(person_image, person)

            for bomb in bombs:
                screen.blit(bomb_image, bomb['rect'])

            score += 1

        if game_over:
            font = pygame.font.Font(None, 36)
            text = font.render("Game Over", True, (255, 255, 255))
            text_rect = text.get_rect(center=(size[0] // 2, size[1] // 2))
            screen.blit(text, text_rect)

        pygame.display.update()

runGame()
pygame.quit()
