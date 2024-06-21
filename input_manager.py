import pygame
import math_functions

class InputManager:
    def __init__(self, keyList:list[int]=[]):
        self.key_info_list = []
        self.key_state_list = []
        
        if keyList != []:
            self.add_key_list(keyList)

    def debug(self, keyNumber:int):
        for i in range(len(self.key_info_list)):
            key = self.key_info_list[i]
            
            if key == keyNumber:
                state = self.key_state_list[i]
                print(f"Key: {key} is {state}")
                return
        print(f"Error: No such key with the value of {keyNumber} is being monitored.")

    def add_key_list(self, keyList:list[int]):
        for num in keyList:
            self.add_key(num)
    
    def add_key(self, keyNumber:int):
        self.key_info_list.append(keyNumber)
        self.key_state_list.append(False)
    
    def get_key_state(self, keyNumber:int):
        for i, keyN in enumerate(self.key_info_list):
            if keyN == keyNumber:
                return self.key_state_list[i]
            
        print(f"Error: No such key with the value of {keyNumber} is being monitored.")

    def get_vector(self, left:int, right:int, up:int, down:int):
        x = 0
        y = 0
        
        if self.get_key_state(left): x -= 1
        if self.get_key_state(right): x += 1
        if self.get_key_state(up):y -= 1
        if self.get_key_state(down):y += 1
        
        return math_functions.normalize([x, y])

    def poll(self, event:pygame.event):
        if event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
            for i, num in enumerate(self.key_info_list):
                if num == event.key:
                    self.key_state_list[i] = (event.type == pygame.KEYDOWN)