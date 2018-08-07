##
## Script:		export_ZLOC_to_clipboard_for_PFTrack.py v1.0
##
## Author:		Hyuk Ko
##				kohyuk91@gmail.com
##
## Date:		2018/05/01
##
## Description:	Exports 'User Tracks' to ZLOC file. Saves file to desktop.
##
## Usage:		1.Add this node to 'User Track' node
##	


import pfpy
from pfpy import Tracker, Clip
import os
import subprocess
import platform

def pfNodeName():
	return 'Export_ZLOC_0_Offset'

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
	
	#userhome = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
	#path = userhome + '/zloc.txt'
	#output = open(path, 'w')
	
	############### Fix Offset Value according to 'In Point'.
	offset = 0    # Sequence Start with 0001 => offset = 0
	############### Sequence Start with 1001 => offset = 1000

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
			nl = [t.getName(),str(j + offset + 1),str((t.getTrackPosition(j+offset+1)[0] - halfWidth)/halfWidth),str(((t.getTrackPosition(j+offset+1)[1] - halfHeight)/halfHeight)*-1)]
			nl = ' '.join(nl)
			nl = nl + '\n'
			output.write(nl)

	output.close()
	print "Successfully Exported ZLOC"