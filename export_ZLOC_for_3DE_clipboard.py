#
#
# 3DE4.script.name:	Export ZLOC to Clipboard...
#
# 3DE4.script.version:	v1.0
#
# 3DE4.script.gui:	Main Window::3DE4::File::Export
# 3DE4.script.gui:	Object Browser::Context Menu Point
# 3DE4.script.gui:	Object Browser::Context Menu Points
# 3DE4.script.gui:	Object Browser::Context Menu PGroup
#
# 3DE4.script.comment:	Exports selected trackers to ZLOC file.
# 3DE4.script.comment:	Author: Hyuk Ko
# 3DE4.script.comment:	v1.0 @ 2018/08/07
# 3DE4.script.comment:	kohyuk91@gmail.com
#
# Original Script:	export_tracks.py(by 3DE) - modified by Hyuk Ko
#

import subprocess
import platform

currentOS = platform.system() # 'Windows' or 'Darwin'(MACOS) or 'Linux'

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

c	= tde4.getCurrentCamera()
pg	= tde4.getCurrentPGroup()
if c!=None and pg!=None:
	n	= tde4.getCameraNoFrames(c)	
	p	= tde4.getContextMenuObject()			# check if context menu has been used, and retrieve point...
	if p!=None:
		pg	= tde4.getContextMenuParentObject()	# retrieve point's parent pgroup (not necessarily being the current one!)...
		l	= tde4.getPointList(pg,1)
	else:
		l	= tde4.getPointList(pg,1)		# otherwise use regular selection...
	if len(l)>0:
		clipStr = ''
		req	= tde4.createCustomRequester()
		tde4.addTextFieldWidget(req,"frame_offset_field","Frame Offset","0")
		tde4.addTextFieldWidget(req,"overscan_field","Overscan","1.00")
		ret	= tde4.postCustomRequester(req,"Export ZLOC...",500,0,"Ok","Cancel")
		if ret==1:
			offset	= int(tde4.getWidgetValue(req,"frame_offset_field"))
			overscan = float(tde4.getWidgetValue(req,"overscan_field"))
			
			if offset<0: offset = 0
				#
				# main block...
				
			for point in l:
				name	= tde4.getPointName(pg,point)
				c2d	= tde4.getPointPosition2DBlock(pg,point,c,1,n)
				n0	= 0
				for v in c2d:
					if v[0]!=-1.0 and v[1]!=-1.0: n0 += 1
				frame	= 1+offset
				for v in c2d:
					if v[0]!=-1.0 and v[1]!=-1.0: 
						dv = tde4.removeDistortion2D(c,frame,v)
						clipStr += "%s %d %.15f %.15f\n"%("zloc"+name,frame,(2*dv[0]-1)/overscan,(-2*dv[1]+1)/overscan)
					frame	+= 1
					
			copy_to_clipboard(currentOS,clipStr)	
	else:
		tde4.postQuestionRequester("Export ZLOC to Clipboard...","There are no selected points.","Ok")
else:
        tde4.postQuestionRequester("Export ZLOC to Clipboard...","There is no current Point Group or Camera.","Ok")