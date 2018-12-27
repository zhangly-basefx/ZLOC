##
## Script:       import_ZLOC_for_pftrack.py v1.0
##
## Author:       Hyuk Ko
##               kohyuk91@gmail.com
##
## Date:         2018/12/28
##
## Description:  Import ZLOC file from Temp.
##
## Usage:        1.Input Offset Value and press Enter
##               

import pfpy
from pfpy import Tracker, Clip
import tempfile

def pfNodeName():
    return 'Import_ZLOC_from_TEMP'

def pfNodeTopLevelButton():
    return 1

def pfAutoRun():
    return False
      
def main():
    
    ############################ Fix Offset Value according to 'In Point'.
    offset = int(raw_input())  # Sequence Start with 0001 => offset = 0
    ############################ Sequence Start with 1001 => offset = 1000
    
    ############################
    TEMP = tempfile.gettempdir()
    path = TEMP + '/zloc_temp.txt'
    ############################
    
    c = pfpy.getClipRef(0)
    width =  c.getFrameWidth()
    height =  c.getFrameHeight()
    inPoint = c.getInPoint()
    outPoint = c.getOutPoint()
    clipLen = outPoint - inPoint + 1
    
    word_list = []
    with open(path,'r') as f:
        word_list = [word for line in f for word in line.split()] # Open txt & Append All Words as Single Elements to List ex) ['zloc01','1','0.198568','0.754568','zloc01','2','0.188568','0.784568', ......]
    zlocNameList = sorted(set(word_list[0::4]), key=word_list.index)
    groupByFourList = [word_list[i:i+4] for i in range(0, len(word_list), 4)]
    
    for zlocName in zlocNameList:
        t = Tracker.new(zlocName)
        
        for i in range(len(groupByFourList)):
            if groupByFourList[i][0] == zlocName:
                t.setTrackPosition(int(groupByFourList[i][1])+offset, (float(groupByFourList[i][2])+1)/2 * width-0.5, (float(groupByFourList[i][3])-1)/-2 * height-0.5)
                
        for j in range(inPoint+offset,outPoint+offset,1):
            if t.getKeyed(j) == False:
                t.setHidden(j, 1)
            else:
                pass
 
