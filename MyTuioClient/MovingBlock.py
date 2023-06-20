import GameObject
import pygame
from enum import Enum
from pathlib import Path
import os

class ShapeType(Enum):
    DELETE = "Delete"
    CIRCLE = "Circle"
    CHECKMARK = "Check"



class MovingBlock(GameObject.GameObject):
    def __init__(self, x:int, y:int, width:int, height:int, color:tuple, speed:int, type:ShapeType, screen) -> None:
        self.color = color
        self.rect = pygame.Rect(x, y, width, height)
        self.speed = speed
        self.type = type # pattern type
        self.surf = pygame.Surface((width, height))
        self.screen = screen

        #resolve image name
        self.imgname = ""
        if self.type == ShapeType.CIRCLE:
            self.imgname = "circle.png"
        elif self.type == ShapeType.CHECKMARK:
            self.imgname = "checkmark.png"
        elif self.type == ShapeType.DELETE:
            self.imgname = "delete.png"

        self.sprite = pygame.transform.scale(pygame.image.load(os.getcwd() + os.sep+"sprites"+os.sep+self.imgname), (self.rect.width, self.rect.height))


        
    def update(self) -> None:
        self.rect.y += self.speed
        

    def draw(self) -> None:
        self.surf.fill(self.color)
        self.surf.blit(self.sprite, (0,0))
        self.screen.blit(self.surf, (self.rect.x, self.rect.y))

       