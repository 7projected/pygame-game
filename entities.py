import pygame, input_manager, sprite_manager, math_functions, math

class Entity(pygame.Rect):
    def __init__(self, pos_x, pos_y, width, height):
        super().__init__(pos_x, pos_y, width, height)
        self.velocity = [0, 0]
        self.move_steps = 20
        self.on_left_wall = False
        self.on_right_wall = False
        self.on_bottom_wall = False
        self.on_top_wall = False
    
    def debug(self, velo:bool, on_walls:bool, pos:bool):
        if velo:
            print(f'v_x:{int(self.velocity[0])} v_y:{int(self.velocity[1])}')
        if on_walls:
            print(f'left_wall:{self.on_left_wall}   right_wall:{self.on_right_wall}   top_wall:{self.on_top_wall}   bottom_wall:{self.on_bottom_wall}')
        if pos:
            print(f'x:{int(self.left)} y:{int(self.top)}')
    
    def move_and_slide(self, rect_list:list[pygame.Rect]):
        last_x = self.left
        last_y = self.top
    
        check_rect = pygame.Rect(self.left, self.top, self.width, self.height)

        x_step_size = self.velocity[0] / self.move_steps
        y_step_size = self.velocity[1] / self.move_steps
        
        if self.velocity[0] != 0:
            for x in range(self.move_steps):
                check_rect.topleft = [self.left + (x_step_size*x), self.top]
                if check_rect.collidelist(rect_list) >= 0:
                    if self.velocity[0] > 0:
                        self.on_right_wall = True
                    if self.velocity[0] < 0:
                        self.on_left_wall = True
                    break
                else:
                    last_x = check_rect.left
                    if x == self.move_steps-1:
                        self.on_right_wall = False
                        self.on_left_wall = False
                    
        
        if self.velocity[1] != 0:
            for y in range(self.move_steps):
                check_rect.topleft = [last_x, self.top + (y_step_size*y)]
                if check_rect.collidelist(rect_list) >= 0:
                    if self.velocity[1] > 0:
                        self.on_bottom_wall = True
                    if self.velocity[1] < 0:
                        self.on_top_wall = True
                    break
                else:
                    last_y = check_rect.top
                    if y == self.move_steps-1:
                        self.on_top_wall = False
                        self.on_bottom_wall = False
        
        self.topleft = [last_x, last_y]

class Bullet(Entity):
    def __init__(self, pos_x:float, pos_y:float, dir:list[float]):
        super().__init__(pos_x, pos_y, 8, 8)
        self.dir = dir
        self.speed = 5
        self.velocity = [self.dir[0] * self.speed, self.dir[1] * self.speed]
        self.surf = pygame.Surface([8, 8])
        self.frame = 0
        self.max_frame = 10
    
    def draw(self, surf:pygame.Surface, parent:Entity, i):
        surf.blit(self.surf, [self.left - 4, self.top - 4])
        self.frame += 1
        
        if self.frame == self.max_frame:
            parent.draw_list.pop(i)

class Player(Entity):
    def __init__(self, pos_x:float, pos_y:float, width:int, height:int, speed:float):
        super().__init__(pos_x, pos_y, width, height)
        self.speed = speed
        self.dash_speed = speed * 5
        self.size = [width, height]
        self.rotation = 0
        self.draw_list :list[Bullet]= []
    
    def update(self, rect_list:list[pygame.Rect], input:input_manager.InputManager):
        input_dir = input.get_vector(pygame.K_a, pygame.K_d, pygame.K_w, pygame.K_s)
        self.velocity = [input_dir[0] * self.speed, input_dir[1] * self.speed]
        self.move_and_slide(rect_list)
        
        mouse_dir = math_functions.normalize([input.mouse_pos[0] - self.centerx, input.mouse_pos[1] - self.centery])
        # makes the rotation face the mouse dir
        self.rotation = (180 / math.pi) * -math.atan2(mouse_dir[0], mouse_dir[1])
        
        for item in self.draw_list:
            item.move_and_slide(rect_list)
        
        if input.mouse_buttons[0]:
            mouse_spawn_mult = 20
            self.draw_list.append(Bullet(self.centerx + mouse_dir[0] * mouse_spawn_mult, self.centery + mouse_dir[1] * mouse_spawn_mult, mouse_dir))

    def draw(self, surf:pygame.Surface, offset:list, sprite_m:sprite_manager.SpriteManager):
        sprite = pygame.Surface(self.size).convert_alpha()
        sprite.fill([0, 0, 0, 0])
        pygame.draw.rect(sprite, [0, 0, 0], [0, 0, self.size[0], self.size[1]])
        
        rotated_sprite = pygame.transform.rotate(sprite, int(-self.rotation))
        draw_position = rotated_sprite.get_rect(center = sprite.get_rect(topleft = self.topleft).center)
        surf.blit(rotated_sprite, [draw_position[0] + offset[0], draw_position[1] + offset[1]])
        
        for i, item in enumerate(self.draw_list):
            item.draw(surf, self, i)