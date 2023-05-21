from pythontuio import TuioServer
from pythontuio import Cursor
from classes import Touch, Blob

class MyServer:
    def __init__(self) -> None:
        self.server = TuioServer()
        self.trackedIds = list();
    
    def updateTouches(self, tlist:list(), screenw:int, screenh:int):
        
        thist:Touch
        for thist in tlist:
            if thist.id not in self.trackedIds: # not tracked yet
                curs = Cursor(thist.id)

                tpos = thist.getTuple();
                normal = (screenw/tpos[0], screenh/tpos[1]);
                curs.position = normal;

                self.server.cursors.append(curs)
                self.trackedIds.append(thist.id)
        
        self.server.send_bundle()