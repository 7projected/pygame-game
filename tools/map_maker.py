import pygame, sys, random, math_functions, os
tile_size = 32
world_size_x = 100
world_size_y = 100
world = []
offset = [0, 0]
default_state = 0

state = 0
states = [
    [255, 255, 255], # empty
    [150, 150, 150], # draw but no collision
    [100, 100, 150], # empty with collision
    [0, 0, 255]      # draw with collsion
]

for y in range(world_size_y):
    app = []
    for x in range(world_size_x):
        app.append(default_state)
    world.append(app)

pygame.init()

display_size = [1280, 720]
screen = pygame.display.set_mode(display_size)
clock = pygame.time.Clock()
dt = 0
cam_move_threshold = 50
cam_move_stages = 5
cam_speed = 100
lmb_pressed = False
font = pygame.font.Font(None, 32)

def save_file():
    file_i = 0
    file_str = f'./tools/saves/{file_i}.map'
    
    while os.path.exists(file_str):
        file_i += 1
        file_str = f'./tools/saves/{file_i}.map'
    
    with open(file_str, "w") as file:
        for y in world:
            st = ''
            for x in y:
                st += f'{x} '
            st += '\n'
            file.write(st)

while True:
    mouse_pos = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                lmb_pressed = True
            if event.button == 4:
                state += 1
            if event.button == 5:
                state -= 1
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                lmb_pressed = False
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_F3:
                save_file()
    
    state = math_functions.clamp(state, 0, len(states)-1)
    
    for i in range(cam_move_stages): 
        if mouse_pos[0] < cam_move_threshold * i:
            offset[0] -= cam_speed * dt
        if mouse_pos[0] > display_size[0] - cam_move_threshold * i:
            offset[0] += cam_speed * dt
        if mouse_pos[1] < cam_move_threshold * i:
            offset[1] -= cam_speed * dt
        if mouse_pos[1] > display_size[1] - cam_move_threshold * i:
            offset[1] += cam_speed * dt
    
    offset = [math_functions.clamp(offset[0], 0, world_size_x * tile_size - display_size[0]), math_functions.clamp(offset[1], 0, world_size_y * tile_size - display_size[1])]
    
    grid_mouse_pos = math_functions.gridify(mouse_pos[0] + offset[0], mouse_pos[1] + offset[1], tile_size)
    if lmb_pressed:
        world[grid_mouse_pos[1]][grid_mouse_pos[0]] = state
    
    screen.fill([255,255,255])
    
    for y_i, y in enumerate(world):
        for x_i, x in enumerate(y):
            color = states[x]
            pygame.draw.rect(screen, color, [x_i * tile_size - offset[0], y_i * tile_size - offset[1], tile_size, tile_size])
    
    
    t = font.render(f'{state}                                                                Press the F3 key to create a file for this map.', True, [0, 0, 0])
    screen.blit(t, [0, 0])    
    
    pygame.display.update()
    dt = clock.tick(60) / 1000