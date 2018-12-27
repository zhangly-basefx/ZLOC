##
## Script:       export_ZLOC_for_pftrack.py v1.0
##
## Author:       Hyuk Ko
##               kohyuk91@gmail.com
##
## Date:         2018/12/27
##
## Description:  Exports '2D Tracks' to ZLOC file. Saves data to Temp.
##
## Usage:        1.Add this node to 'User Track' node
##               2.Input Offset Value and press Enter

import pfpy
from pfpy import Tracker, Clip
import tempfile

def pfNodeName():
    return 'Export_ZLOC'

def pfNodeTopLevelButton():
    return 1

def pfAutoRun():
    return False      
      
def main():
    
    TEMP = tempfile.gettempdir()
    path = TEMP + '/zloc_temp.txt'
    
    clipStr = ''
    
    ############################ Fix Offset Value according to 'In Point'.
    offset = int(raw_input())  # Sequence Start with 0001 => offset = 0
    ############################ Sequence Start with 1001 => offset = 1000

    c = pfpy.getClipRef(0)
    width =  c.getFrameWidth()
    height =  c.getFrameHeight()
    inPoint = c.getInPoint()
    outPoint = c.getOutPoint()
    clipLen = outPoint - inPoint + 1

    num = pfpy.getNumTrackers()
    trackerList = list()    

    halfWidth = width / 2
    halfHeight = height / 2
    
    for i in range(num):
        t = pfpy.getTrackerRef(i)
        trackerList.append(t.getName())
        
        for j in range(clipLen):
            if not t.getHidden(j+offset+1):
                clipStr += "%s %d %.15f %.15f\n"%("zloc_"+t.getName(),j + offset + 1,(t.getTrackPosition(j+offset+1)[0] +0.5 - halfWidth)/halfWidth,((t.getTrackPosition(j+offset+1)[1] +0.5 - halfHeight)/halfHeight)*-1)
    
    with open(path,"w") as f:
        f.write(clipStr)
        
    print "OFFSET:" + str(offset) + ", Successfully Exported ZLOC"
    
