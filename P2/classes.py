import math
import typing
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
    def __init__(self, threshold:int=50) -> None:
        self.currentFrameBlobs = list()  # all blobs from this frame
        self.touches = list()          # contains all touches registered rn
        self.moveThreshold = threshold       # in pixels
        self.nextTouchID = 0                 # next tracked touch gets this ID
        self.nextBlobID = 0

    #returns the blob that was used as the new blob for a touch
    def doNearestNeighbor(self,currentTouch:Touch, allBlobs:list[Blob]) -> Blob:
        min_dist = float('inf')
        nearest = None

        for blob in allBlobs:
            dist = distance(blob.getTuple(), currentTouch.getTuple())
            if dist > self.moveThreshold: # if distance is too far, skip
                continue
            if dist < min_dist:
                min_dist = dist
                nearest = blob
            
        return nearest # returns none when touch has no next blob

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
        self.nextBlobID = 0

    # dont forget to update age on touches and destroy touches that are too old
    # or create new touches 
    # do nearest neighbor for all touches and the currentframeblobs
    def updateTouches(self):
        touch: Touch
        usedBlobsForTouch = list() # list of all blobs that were used to update an existing touch

        for touch in self.touches:
            touch.ageFrames += 1
            nearestBlob = self.doNearestNeighbor(touch, self.currentFrameBlobs)
            if(nearestBlob is None):
                print("Blob is none for touch: " + str(touch.id))
                touch.ageFramesUntracked += 1
            else:
                touch.blob = nearestBlob # update blob


        # loop over all current frame touches and see if there are 
        # touches that didnt get used for an existing touch

        cBlob: Blob
        for cBlob in self.currentFrameBlobs:  # loop all blobs
            if cBlob not in usedBlobsForTouch: #didnt get used
                #create a new touch
                self.addTouchToList(cBlob)
                print("Adding blob to list of touches!")
