import pygame
from pygame.locals import *
import pygame.color
import MovingBlock
import random


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

    def add_tuio_cursor(self, cursor: Cursor):
        print("Added {}".format(cursor.session_id))
        self.cursor_paths[cursor.session_id] = []  # Initialize an empty path for the cursor

    def update_tuio_cursor(self, cursor: Cursor) -> None:
        last_position = self.cursor_paths[cursor.session_id][-1] if self.cursor_paths[cursor.session_id] else None
        if cursor.position != last_position:
            self.cursor_paths[cursor.session_id].append(Point2D(cursor.position[0], cursor.position[1]))  # Append the cursor position to its path

    def remove_tuio_cursor(self, cursor: Cursor) -> None:
        path = self.cursor_paths[cursor.session_id]  # Get the path for the cursor
        #print("Removed cursor")
        if len(path) > 1:
            result = self.recognizer.recognize(path)  # Recognize gesture for the cursor
            print("Recognized gesture: " + result.Name + " with a score of " + str(result.Score))

        newlist = []
        for block in self.blockList:
            #print("comparing " + str(block.type.value) + " to " + result.Name + "")
            if block.type.value != result.Name:
                newlist.append(block)
            else:
                print("Removed block")
        self.blockList = newlist
        


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
#blockList.append(MovingBlock.MovingBlock(0,0,50,50,(255,0,0,255),1,MovingBlock.ShapeType.CHECKMARK, screen))



def main():
    dorun = True

    SPAWNCOOLDOWN = 60
    spawncooldown = SPAWNCOOLDOWN

    while dorun:
        for event in pygame.event.get():
            if event.type ==QUIT:
                dorun = False
        
        #spawn blocks
        spawncooldown -= 1
        
        if(spawncooldown <= 0):
            rands = random.randint(1,3)
            shape = MovingBlock.ShapeType.CHECKMARK
            if(rands == 1):
                shape = MovingBlock.ShapeType.CHECKMARK
            elif(rands == 2):
                shape = MovingBlock.ShapeType.CIRCLE
            elif(rands == 3):
                shape = MovingBlock.ShapeType.DELETE

            randx = random.randint(0,WINDOW_SIZE[0]-50)
            

            listener.blockList.append(MovingBlock.MovingBlock(randx,0,50,50,(255,0,0,255),1,shape, screen))
            spawncooldown = SPAWNCOOLDOWN


        #update game objects
        for block in listener.blockList:
            block.update()

        #draw the screen
        screen.fill((0,0,0,255))

        #draw the game objects
        for block in listener.blockList:
            block.draw()
            if(block.rect.y > WINDOW_SIZE[1]):
                dorun = False
                print("Game Over")

        #draw the cursors
        mycurs = client.cursors
        draw_cursors(mycurs)


        pygame.display.flip()
        pygame.event.pump()

        clock.tick(60)
    pygame.quit()

if __name__ == '__main__':
    main()
