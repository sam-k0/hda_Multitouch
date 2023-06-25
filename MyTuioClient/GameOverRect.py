import GameObject
import pygame
from pathlib import Path
import os



class GameOverRect(GameObject.GameObject):
    def __init__(self, x:int, y:int, width:int, height:int, screen) -> None:
        self.rect = pygame.Rect(x, y, width, height)
        self.surf = pygame.Surface((width, height))
        self.screen = screen
        self.drawn_rect_width = 0

        
    def update(self) -> None:
        pass
        

    def draw(self, scale:float) -> None:
        # Calculate the dimensions of the centered rectangle
        rect_width = 200 * scale
        rect_height = 150 * scale

        self.drawn_rect_width = rect_width
        
        # Calculate the position of the centered rectangle
        surface_width, surface_height = self.surf.get_size()
        rect_x = (surface_width - rect_width) // 2
        rect_y = (surface_height - rect_height) // 2

        # Draw the centered rectangle
        rect_color = (255, 0, 0)  # RGB color value (red in this example)

        pygame.draw.rect(self.surf, rect_color, (rect_x, rect_y, rect_width, rect_height))
        
        
        # Draw the text
        self.screen.blit(self.surf, (self.rect.x, self.rect.y))


       