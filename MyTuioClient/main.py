import pygame
from pygame.locals import *
import pygame.color
import MovingBlock
import GameOverRect
import random
from math import hypot

from pythontuio import TuioClient
from pythontuio import Cursor
from pythontuio import TuioListener
from threading import Thread


from Recognizer import GeometricRecognizer # Custom recognizer
from TuioPatterns import Point2D



class MyListener(TuioListener):

    def __init__(self):
        self.cursor_paths = {}
        self.recognizer = GeometricRecognizer()
        self.recognizer.load_templates()
        self.blockList = list()
        self.score = 0
        self.gameOver = False
        self.spawnTimer = 60
        self.spawnTimerMax = 60
        self.lastZoomDistance = 0
        self.zoomFactor = 1.0
        self.gameOverRect = None
        self.blockSpeed = 1.0

    def add_tuio_cursor(self, cursor: Cursor):
        print("Added {}".format(cursor.session_id))
        self.cursor_paths[cursor.session_id] = []  # Initialize an empty path for the cursor

    def update_tuio_cursor(self, cursor: Cursor) -> None:
        last_position = self.cursor_paths[cursor.session_id][-1] if self.cursor_paths[cursor.session_id] else None
        if cursor.position != last_position:
            self.cursor_paths[cursor.session_id].append(Point2D(cursor.position[0], cursor.position[1]))  # Append the cursor position to its path

        if self.gameOver:
            cursor_path = self.cursor_paths[cursor.session_id]
            next_cursor_path = self.cursor_paths.get(cursor.session_id + 1)
            if cursor_path is not None and next_cursor_path is not None and len(next_cursor_path) > 0:
                print("Cursor path length: " + str(len(cursor_path)) + " Next cursor path length: " + str(len(next_cursor_path)))
                current_distance = hypot(cursor_path[0].x - next_cursor_path[-1].x, cursor_path[0].y - next_cursor_path[-1].y)

                if self.lastZoomDistance != 0:
                    if current_distance < self.lastZoomDistance:
                        print("Zoom-in gesture")
                        self.zoomFactor *= 1.1  # Increase the zoom factor for zooming in
                    else:
                        print("Zoom-out gesture")
                        self.zoomFactor *= 0.9  # Decrease the zoom factor for zooming out
                self.lastZoomDistance = current_distance

    def remove_tuio_cursor(self, cursor: Cursor) -> None:
        path = self.cursor_paths[cursor.session_id]  # Get the path for the cursor
        #print("Removed cursor")
        if len(path) > 1:
            result = self.recognizer.recognize(path)  # Recognize gesture for the cursor
            print("Recognized gesture: " + result.Name + " with a score of " + str(result.Score))

        if self.gameOver is False: # As long as not game over
            newlist = []
            for block in self.blockList:
                #print("comparing " + str(block.type.value) + " to " + result.Name + "")
                if block.type.value != result.Name:
                    newlist.append(block)
                else:
                    print("Removed block")
                    self.score += 100
                    self.blockSpeed *= 1.055

            if(newlist != self.blockList):
                print("increasing speed")
                self.spawnTimerMax = int(self.spawnTimerMax *0.9)
            
            self.blockList = newlist
        else:
            self.zoomFactor = 1.0
    
    def update_game(self) -> None:
        #spawn blocks
        if self.gameOver is False:
            self.spawnTimer -= 1
            if(self.spawnTimer <= 0):
                rands = random.randint(1,3)
                shape = MovingBlock.ShapeType.CHECKMARK
                if(rands == 1):
                    shape = MovingBlock.ShapeType.CHECKMARK
                elif(rands == 2):
                    shape = MovingBlock.ShapeType.CIRCLE
                elif(rands == 3):
                    shape = MovingBlock.ShapeType.DELETE

                randx = random.randint(0,WINDOW_SIZE[0]-50)
            
                self.blockList.append(MovingBlock.MovingBlock(randx,0,50,50,(255,0,0,255),self.blockSpeed,shape, screen))
                self.spawnTimer = self.spawnTimerMax

            #update game objects
            for block in self.blockList:
                block.update()

            #draw the game objects
            for block in self.blockList:
                block.draw()
                if(block.rect.y > WINDOW_SIZE[1]):
                    # Game over 
                    print("Game over")
                    self.gameOver = True
                    self.blockList = list()
        else: # game over

            # Draw game over stuff
            self.gameOverRect = GameOverRect.GameOverRect(0,0,WINDOW_SIZE[0], WINDOW_SIZE[1],screen)
            self.gameOverRect.draw(self.zoomFactor)

            font = pygame.font.Font(None, 36)  # Choose the desired font and size
            text_surface = font.render("Zoom The Rectangle To Screen Size To Start", True, (255, 255, 255))  # Render the text
            text_rect = text_surface.get_rect()
            text_rect.center = (WINDOW_SIZE[0]/2, WINDOW_SIZE[1]/2)  # Set the position of the text
            screen.blit(text_surface, text_rect)  # Draw the text onto the screen

            if(self.gameOverRect.drawn_rect_width > WINDOW_SIZE[0] or self.gameOverRect.drawn_rect_width <= 20): # zoomed and start new game
                print("New game")
                self.score = 0
                self.gameOver = False
                self.spawnTimer = 60
                self.spawnTimerMax = 60
                self.lastZoomDistance = 0
                self.zoomFactor = 1.0
                self.gameOverRect = None
                for l in self.cursor_paths:
                    l = {}


# TUIO CLient
client = TuioClient(("localhost",3333))
t = Thread(target=client.start)
listener = MyListener()
client.add_listener(listener)

t.start()

# PYGAME setup
pygame.init()
WINDOW_SIZE = (800,600)
screen = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("sam-k0's TUIO Client")
clock = pygame.time.Clock()

# Pygame helper functions

def draw_number(number, x, y):
    font = pygame.font.Font(None, 36)  # Choose the desired font and size
    text_surface = font.render(str(number), True, (255, 255, 255))  # Render the text
    text_rect = text_surface.get_rect()
    text_rect.center = (x, y)  # Set the position of the text
    screen.blit(text_surface, text_rect)  # Draw the text onto the screen

def draw_cursors(cursors:list()):
    #screen.fill((0,0,0,255))
    curs:Cursor
    for curs in cursors:
        x,y = curs.position[0]*WINDOW_SIZE[0], curs.position[1]*WINDOW_SIZE[1]
        pygame.draw.circle(screen, (255,0,255,255), (int(x),int(y)), 10)
        draw_number(curs.session_id, x,y)

        path:list() = listener.cursor_paths[curs.session_id]  # Get the path for the cursor
        if len(path) > 1:
            scaled_path = [(p.x * WINDOW_SIZE[0], p.y * WINDOW_SIZE[1]) for p in path]
            pygame.draw.lines(screen, (255, 255, 255), False, scaled_path, 2)

# Game

def main():
    dorun = True

    while dorun:
        for event in pygame.event.get():
            if event.type ==QUIT:
                dorun = False
        
        #draw the screen
        screen.fill((0,0,0,255))

        #update the game
        #listener.update_game()

        #draw the cursors
        mycurs = client.cursors
        draw_cursors(mycurs)

        #draw the score
        draw_number("Score: "+str(listener.score), WINDOW_SIZE[0]/2, 50)

        pygame.display.flip()
        pygame.event.pump()

        clock.tick(60)
    pygame.quit()

if __name__ == '__main__':
    main()
