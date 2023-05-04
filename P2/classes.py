import math
def distance(p1:tuple, p2:tuple):
    return math.sqrt((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2)

class Blob:
    def __init__(self, pos: tuple, id: int) -> None:
        self.x = round(pos[0])
        self.y = round(pos[1])
        self.id = id
    
    def getTuple(self):
        return (self.x, self.y)

class Touch:
    def __init__(self, id:int, blob:Blob = None) -> None:
        self.id = id
        self.blob = blob # the blob saves the coords from this
        self.ageFrames = 0
        self.ageFramesUntracked = 0

    def getTuple(self) -> tuple: # returns this touches blobs coords as tuple 
        return (self.blob.x, self.blob.y)


class Tracker:
    def __init__(self) -> None:
        self.currentFrameBlobs = list() # all blobs from this frame
        self.touches = list()   # contains all touches registered rn
        self.moveThreshold = 50 # in pixels
        self.nextTouchID = 0    # next tracked touch gets this ID

    #returns the blob that was used as the new blob for a touch
    def doNearestNeighbor(self,currentTouch:Touch, newBlobs:list[Blob], threshold:int) -> Blob:
        min_dist = float('inf')
        nearest = None
        for blob in newBlobs:
            dist = distance(blob.getTuple(), currentTouch.getTuple())
            if dist > threshold: # if distance is too far, skip
                # TODO: We probably also want to mark it as expired...
                continue
            if dist < min_dist:
                min_dist = dist
                nearest = blob
        
        currentTouch.blob = nearest
        return nearest

    #add to cache
    def addBlobToFrame(self, blob:Blob)->None:
        self.currentFrameBlobs.append(blob);

    #clear cache
    def clearCurrentFrame(self)->None:
        self.currentFrameBlobs.clear()

    # dont forget to update age on touches and destroy touches that are too old
    # or create new touches 
    # do nearest neighbor for all touches and the currentframeblobs
    def updateTouches(self):
        pass