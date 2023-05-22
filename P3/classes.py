import math
import typing

from pythontuio import TuioServer
from pythontuio import Cursor

def distance(p1:tuple, p2:tuple):
    return math.sqrt((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2)

class Blob:
    def __init__(self, pos: tuple, id: int) -> None:
        self.x = round(pos[0])
        self.y = round(pos[1])
        self.used = False
        self.id = id
    
    def getTuple(self):
        return (self.x, self.y)
    
    def setUsed(self):
        self.used = True

class Touch:
    def __init__(self, id:int, blob:Blob = None) -> None:
        self.id = id
        self.pos:tuple = blob.getTuple()
        self.ageFrames = 0
        self.ageFramesUntracked = 0

    def getTuple(self) -> tuple: # returns this touches blobs coords as tuple 
        return self.pos


class MyServer:
    def __init__(self) -> None:
        self.server = TuioServer()
        self.trackedIds = list();
    
    def updateTouches(self, tlist:list(), screenw:int, screenh:int):
        
        thist:Touch
        checked = list();
        checked.clear()
        # list 1 aus Touches
        # list 2 aus Cursors
        # wenn in list 2 aber nicht in 1 remove
        for thist in tlist:
            if thist.id not in self.trackedIds: # not tracked yet
                curs = Cursor(thist.id)

                tpos = thist.getTuple();
                normal = (tpos[0]/screenw, tpos[1]/screenh);
                curs.position = normal;

                self.server.cursors.append(curs)
                self.trackedIds.append(thist.id)
            else: # is schon drinne
                curs:Cursor
                for curs in self.server.cursors:
                    if curs.session_id == thist.id:
                        tpos = thist.getTuple();
                        normal = (tpos[0]/screenw, tpos[1]/screenh);
                        curs.position = normal;
        
        # alte raus
        disappearedTouchesTotallyNotSusList = [obj for obj in self.server.cursors if obj.session_id not in [item.id for item in tlist]]
        
        self.server.cursors = [obj for obj in self.server.cursors if obj not in disappearedTouchesTotallyNotSusList]

        self.server.send_bundle()

class Tracker:
    def __init__(self, threshold:int=50) -> None:
        self.currentFrameBlobs = list()  # all blobs from this frame
        self.touches = list()          # contains all touches registered rn
        self.moveThreshold = threshold       # in pixels
        self.nextTouchID = 0                 # next tracked touch gets this ID
        self.nextBlobID = 0
        self.framesUntrackedDelete = 1
        self.mytuio = MyServer()
        self.screenw = 1920;
        self.screenh = 1080;
        
    #returns the blob that was used as the new blob for a touch
    def doNearestNeighbor(self,currentTouch:Touch, allBlobs:list[Blob]) -> Blob:
        min_dist = float('inf')
        nearest = None

        for blob in allBlobs:
            dist = distance(blob.getTuple(), currentTouch.getTuple())
            #print("Distance is {0} for blob {1}".format(dist, blob.id))
            if dist <= self.moveThreshold:
                if dist < min_dist:
                    min_dist = dist
                    nearest = blob
            
        if(nearest is not None):
            currentTouch.pos = nearest.getTuple()
        return nearest
    
    def findNearestTouchFromBlob(self, blob:Blob):
        min_dist = float('inf')
        nearest = None

        if(len(self.touches) == 0):
            return None, -1

        for tou in self.touches:
            dist = distance(blob.getTuple(), tou.getTuple())
            #print("Distance is {0} for blob {1}".format(dist, blob.id))
            if dist < min_dist:
                min_dist = dist
                nearest = tou
        return nearest, dist

    def addTouchToList(self, blob:Blob):
        self.touches.append(Touch(self.nextTouchID, blob))
        self.nextTouchID += 1

    #add to cache
    def addBlobToFrame(self, blobcoords:tuple)->None:
        self.currentFrameBlobs.append(Blob(blobcoords, self.nextBlobID));
        self.nextBlobID += 1

    #clear cache
    def clearCurrentFrame(self)->None:
        self.currentFrameBlobs.clear()
        

    def getTouchBlobs(self)->list:
        l = list()
        t:Touch
        for t in self.touches:
            l.append(t.blob)
        return l
    
    def printBlobs(self)->None:
        b:Blob
        for b in self.currentFrameBlobs:
            print("bID: {} ({},{})".format(b.id,b.x,b.y))
    
    def printTouches(self)->None:
        b:Touch
        for b in self.touches:
            print("tID: {} ({},{})".format(b.id,b.pos[0],b.pos[1]))
    
    def updateTouches(self):
        # Loop all blobs
        print("---")
        self.printBlobs()
        print("-")
        cBlob:Blob
        cTouch:Touch

        if(self.nextTouchID >= 11):
            print("its sus")

        toremove:list = list()
        for cTouch in self.touches:
            if(cTouch.id == 9 and cTouch.pos[0] == 663):
                print("susu")
            cBlob = self.doNearestNeighbor(cTouch, self.currentFrameBlobs)
            if(cBlob is None):
                toremove.append(cTouch)
                #self.touches.remove(cTouch) # no suitable new pos found remove ist sus hier
            else:
                self.currentFrameBlobs.remove(cBlob) # 
            
        
        self.touches=[item for item in self.touches if item not in toremove]
        #create new touch
        if(len(self.currentFrameBlobs) > 0):
            #print("adding new:")
            for cBlob in self.currentFrameBlobs:
                near, d = self.findNearestTouchFromBlob(cBlob)
                if(near is not None and d < self.moveThreshold):
                    print("-> ({}:{}) with new tID {} / Nearest: {}, dist: {}".format(cBlob.x, cBlob.y, self.nextTouchID, near.id, d))
                    near.pos = cBlob.getTuple()
                else: # Register new touch
                    self.addTouchToList(cBlob)
                    

        #self.printTouches()
        #print("---")

        #tuio
        self.mytuio.updateTouches(self.touches, self.screenw, self.screenh);






        