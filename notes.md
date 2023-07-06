# Interfaces

- CLI (Command Line): Textual, Abstract, Keyboard input
- GUI (Graphical User Interface): Indirect, Mouse / Pointer
- NUI (Natural User Interface): Physical, Direct, Gestual
<br>
--> Multitouch Interfaces such as Touch Screens on iPad

- Touch creates contact between resistive circuit layers and therefore closing a switch
<br>


# Tracking
## What is  tracking?

- Following an object
- spatial and time tracking (pos_t(i) -> pos_t(i+1)+...pos_t(i+n))
- Every object has an UID
- Needs sensors

## Techniques: Marker-based and Markerless

- Marker based: Placed markers onto objects, tracker only tracks the markers
- Point based: Only a single point gets tracked
- Line based: the Objects' outlines get tracked, therefore rotation is known at all times

## Optical Flow (Markerless)

Tracking of pixel-regional features frame by frame using nearest neighbor / local search

## VR Tracking (head mounted device)

- VR headsets use cameras / laser distance measuring to track environment

## MoCap
- Body motion tracking 
- facial tracking

### Passive tracking (Using markers)

- Placing markers (usually reflecting balls) on the subjects body that reflect the tracking camera's infrared beams

- Marker occlusion occurs when a marker is hidden, which results in that point being unable to be tracked

### Active  tracking
- Using Depth sensors or infrared cameras that directly track the subjects body and movements without using markers.<br>
Examples include gyroscopes, motion and acceleration sensors being attached to the subjects body

- No occlusion issues as there are no markers to be hidden
- Limited range: Depth cameras are only accurate on small distances

# use cases for tracking
- Market analysis
- Analyzing points of attention
    - Eye tracking
- Medicine
- computer interaction for the disabled

# blob tracking
- Tracking of blobs
- No feature extraction necessary
- States of blob interpretation:
    - new finger recognized
    - already known finger  changed position
    - already known finger changed position
- Using nearest neighbor algorithm
- set a maxium possible distance a finger can logically move frame to frame
- Tracking of metadata:
    - tracked finger age
    - path
    - size

# Continuos gestures
- Do not have a fixed end but more of an indefinite length
- Examples: Moving, rotating, scaling objects

# Discrete gestures
- Have a fixed length and thus an expected end
- In tracking, the path needs to be normalized before evaluation
- Region based evaluation
    - Dividing the screen into zones
- Direction based evaluation
    - todo
- $1 Gesture recognizer
    - 

- Examples: Circles, Squares, Checkmarks etc