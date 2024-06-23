import pygame, sys
import entities, input_manager, sprite_manager

pygame.init()

screen = pygame.display.set_mode([640, 480])
clock = pygame.time.Clock()
input = input_manager.InputManager([pygame.K_a, pygame.K_s, pygame.K_d, pygame.K_w])
sprite  = sprite_manager.SpriteManager()

player = entities.Player(0, 0, 32, 32, 5)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        input.poll(event)
    
    player.update([], input)
    
    screen.fill([255,255,255])
    
    player.draw(screen, [0, 0], sprite)
    pygame.display.update()
    clock.tick(60)