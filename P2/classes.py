import math
import typing
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
        self.framesUntrackedDelete = 1
        self.rejectBlobRange = 5 # 2 blobs can't be too close to each other
    #returns the blob that was used as the new blob for a touch
    def doNearestNeighbor(self,currentTouch:Touch, allBlobs:list[Blob]) -> Blob:
        min_dist = float('inf')
        nearest = None

        for blob in allBlobs:
            dist = distance(blob.getTuple(), currentTouch.getTuple())
            #print("Distance is {0} for blob {1}".format(dist, blob.id))
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
        itr_b:Blob
    
        for itr_b in self.currentFrameBlobs:
            if(distance(itr_b.getTuple(), blobcoords) < self.rejectBlobRange):
                return
            
        self.currentFrameBlobs.append(Blob(blobcoords, self.nextBlobID));
        self.nextBlobID += 1

    #clear cache
    def clearCurrentFrame(self)->None:
        self.currentFrameBlobs.clear()
        self.nextBlobID = 0

    def getTouchBlobs(self)->list:
        l = list()
        t:Touch
        for t in self.touches:
            l.append(t.blob)
        return l
    
    def removeTouchesWithSameBlob(self)->None:
        touch: Touch 
        checkt: Touch
        for touch in self.touches:
            for checkt in self.touches:
                if(touch.blob == checkt.blob and touch.id != checkt.id):
                    print("Touches {0} and {1} have the same blob!".format(touch.id, checkt.id))
                    if(checkt.ageFrames < touch.ageFrames):
                        print("-> Deleted {0}".format(checkt.id))
                        self.touches.remove(checkt)
                    else:
                        print("-> Deleted {0}".format(touch.id))
                        self.touches.remove(touch)

    def removeTouchesTooClose(self)->None:
        touch: Touch 
        checkt: Touch
        for touch in self.touches:
            for checkt in self.touches:
                if(distance(touch.getTuple(), checkt.getTuple()) < self.rejectBlobRange and touch.id != checkt.id):
                    print("Touches {0} and {1} have the same blob!".format(touch.id, checkt.id))
                    if(checkt.ageFrames < touch.ageFrames):
                        print("-> Deleted {0}".format(checkt.id))
                        self.touches.remove(checkt)
                    else:
                        print("-> Deleted {0}".format(touch.id))
                        self.touches.remove(touch)

        
    #Alle blobs killen die zu nah an touches sind??
    # dont forget to update age on touches and destroy touches that are too old
    # or create new touches 
    # do nearest neighbor for all touches and the currentframeblobs
    def updateTouches(self):
        touch: Touch
        usedBlobsForTouch = list() # list of all blobs that were used to update an existing touch
        print("-----------------")
        ## debug
        """
        print("Current frame has {0} blobs".format(len(self.currentFrameBlobs)))
        b:Blob;
        for b in self.currentFrameBlobs:
            print("blob id:{0} at ({1},{2})".format(b.id, b.x, b.y))
        """

        #Problem: 2 touches können sich den gleichen blob als neue Position raussuchen...
        #Das führt dazu dass zwei Touches an der gleichen Position sind
        for touch in self.touches:
            touch.ageFrames += 1
            nearestBlob = self.doNearestNeighbor(touch, self.currentFrameBlobs)
            
            if(nearestBlob is None):
                print("Blob is none for touch: " + str(touch.id))
                ##dead
                touch.ageFramesUntracked += 1
                if(touch.ageFramesUntracked >= self.framesUntrackedDelete):
                    print("Touch {0} has been untracked since {1} frames".format(touch.id, touch.ageFramesUntracked))
                    print("Deleting touch {0} after age of {1}".format(touch.id, touch.ageFrames))
                    self.touches.remove(touch)
            else:
                touch.blob = nearestBlob # update blob
                usedBlobsForTouch.append(nearestBlob)

        # An der stelle hier vllt überprüfen ob es solche Kandidaten gibt?
        #self.removeTouchesWithSameBlob()

        # loop over all current frame touches and see if there are 
        # touches that didnt get used for an existing touch
        cBlob: Blob
        for cBlob in self.currentFrameBlobs:  # loop all blobs
            if cBlob not in usedBlobsForTouch and cBlob not in self.getTouchBlobs(): #didnt get used
                #create a new touch 
                print("Adding touch {} from blob at {}:{}".format(self.nextTouchID, cBlob.x, cBlob.y))
                self.addTouchToList(cBlob)
        
        # Remove touches that somehow are attached to the same blob or 
        self.removeTouchesWithSameBlob()

        