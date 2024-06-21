import pygame

def get_sprite_from_sheet(sheet:pygame.Surface, tileSize:int, x:int, y:int):
    surf = pygame.Surface([tileSize, tileSize]).convert_alpha()
    surf.fill([0, 0, 0, 0])
    surf.blit(sheet, [0, 0], [x * tileSize, y * tileSize, tileSize, tileSize])
    return surf

class SpriteManager:
    def __init__(self, list:list= None) -> None:
        self.sprite_name_list = []
        self.sprite_list = []
        if list != None:
            for item in list:
                self.add_sprite_with_path(item[0], item[1])
    
    def load_atlas(self, atlasPath:str, tileSize:int, upscaleSize:int, nameList:list, withShadow:bool= False):
        sprite_sheet = pygame.image.load(atlasPath)
        i = 0
        for y in range(int(sprite_sheet.get_width() // tileSize)):
            for x in range(int(sprite_sheet.get_width() // tileSize)):
                if i <= len(nameList) - 1:
                    surf = get_sprite_from_sheet(sprite_sheet, tileSize, x, y)
                    
                    surf = pygame.transform.scale(surf, [upscaleSize, upscaleSize])
                    
                    if withShadow:
                        overlay = pygame.Surface([upscaleSize, upscaleSize/2]).convert_alpha()
                        overlay.fill([0, 0, 0, 127])
                        s = surf.copy()
                        s.blit(overlay, [0, upscaleSize/2])
                        self.sprite_name_list.append(nameList[i] + "_shadow")
                        self.sprite_list.append(s)
                    
                    self.sprite_name_list.append(nameList[i])
                    self.sprite_list.append(surf)
                i += 1
        
    
    def add_sprite_with_path(self, name:str, path:str):
        sprite = pygame.image.load(path)
        self.sprite_name_list.append(name)
        self.sprite_list.append(sprite)
        
    def add_sprite(self, name:str, surf:pygame.Surface):
        self.sprite_name_list.append(name)
        self.sprite_list.append(surf)
    
    def get_sprite(self, name:str):
        for i, i_name in enumerate(self.sprite_name_list):
            if i_name == name:
                return self.sprite_list[i]
        print(f'Error: No sprite found with the name {name}.')