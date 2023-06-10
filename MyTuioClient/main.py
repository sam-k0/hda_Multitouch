import pygame
from pygame.locals import *
import pygame.color

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

    def add_tuio_cursor(self, cursor: Cursor):
        print("Added {}".format(cursor.session_id))

    def update_tuio_cursor(self, cursor: Cursor) -> None:
        last_position = self.cursor_paths[cursor.session_id][-1] if self.cursor_paths[cursor.session_id] else None
        if cursor.position != last_position:
            self.cursor_paths[cursor.session_id].append(Point2D(cursor.position[0], cursor.position[1]))  # Append the cursor position to its path

    def remove_tuio_cursor(self, cursor: Cursor) -> None:
        path = self.cursor_paths[cursor.session_id]  # Get the path for the cursor
        
        if len(path) > 1:
            result = self.recognizer.recognize(path)  # Recognize gesture for the cursor
            print("Recognized gesture: " + result.Name + " with a score of " + str(result.Score))
        

client = TuioClient(("localhost",3333))
t = Thread(target=client.start)
listener = MyListener()
client.add_listener(listener)

t.start()

pygame.init()
WINDOW_SIZE = (800,600)
screen = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("sam-k0's TUIO Client")

def draw_number(number, x, y):
    font = pygame.font.Font(None, 36)  # Choose the desired font and size
    text_surface = font.render(str(number), True, (255, 255, 255))  # Render the text
    text_rect = text_surface.get_rect()
    text_rect.center = (x, y)  # Set the position of the text
    screen.blit(text_surface, text_rect)  # Draw the text onto the screen

def draw_cursors(cursors:list()):
    screen.fill((0,0,0,255))
    curs:Cursor
    for curs in cursors:
        x,y = curs.position[0]*WINDOW_SIZE[0], curs.position[1]*WINDOW_SIZE[1]
        pygame.draw.circle(screen, (255,0,255,255), (int(x),int(y)), 10)
        draw_number(curs.session_id, x,y)



def main():

    dorun = True
    while dorun:
        for event in pygame.event.get():
            if event.type ==QUIT:
                dorun = False
        mycurs = client.cursors
        draw_cursors(mycurs)

        pygame.display.flip()
        pygame.event.pump()
    pygame.quit()

if __name__ == '__main__':
    main()
