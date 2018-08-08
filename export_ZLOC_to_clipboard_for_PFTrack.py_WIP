##
## Script:       export_ZLOC_to_clipboard_for_PFTrack.py v1.0
##
## Author:       Hyuk Ko
##               kohyuk91@gmail.com
##
## Date:         2018/08/08
##
## Description:  Exports 'User Tracks' to ZLOC file. Saves data to Clipboard.
##
## Usage:        1.Add this node to 'User Track' node
##               2.Input Offset Value and'Run' Script

import pfpy
from pfpy import Tracker, Clip
import subprocess
import platform

def pfNodeName():
    return 'Export_ZLOC_to_CLIPBOARD'

def pfNodeTopLevelButton():
    return 1

def pfAutoRun():
    return False      
      
def copy_to_clipboard(os, text):
    if os == 'Windows':
        p = subprocess.Popen(['clip'], stdin=subprocess.PIPE)        
    elif os == 'Darwin':
        p = subprocess.Popen(['pbcopy'], stdin=subprocess.PIPE)
    elif os == 'Linux':
        p = subprocess.Popen(['xclip', '-selection', 'c'], stdin=subprocess.PIPE)
        #p = subprocess.Popen(['xsel'], stdin=subprocess.PIPE) # If xclip dosnt work
    p.stdin.write(text)
    p.stdin.close()
      
def main():
    
    currentOS = platform.system() # 'Windows' or 'Darwin'(MACOS) or 'Linux'

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
            clipStr += "%s %d %.15f %.15f\n"%("zloc_"+t.getName(),j + offset + 1,(t.getTrackPosition(j+offset+1)[0] - halfWidth)/halfWidth,((t.getTrackPosition(j+offset+1)[1] - halfHeight)/halfHeight)*-1)
    
    copy_to_clipboard(currentOS, clipStr)

    print "OFFSET:" + str(offset) + ", Successfully Exported ZLOC"
    
