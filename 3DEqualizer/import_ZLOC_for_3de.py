#
#
# 3DE4.script.name:	Import ZLOC...
#
# 3DE4.script.version:	v1.1
#
# 3DE4.script.gui:	Main Window::3DE4::File::Import
# 3DE4.script.gui:	Object Browser::Context Menu Point
# 3DE4.script.gui:	Object Browser::Context Menu Points
# 3DE4.script.gui:	Object Browser::Context Menu PGroup
#
# 3DE4.script.comment:    Imports 2D tracking curves from a ZLOC file.
# 3DE4.script.comment:    Author: Hyuk Ko
# 3DE4.script.comment:    v1.1 @ 2018/12/27
# 3DE4.script.comment:    v1.0 @ 2018/10/19
# 3DE4.script.comment:    kohyuk91@gmail.com
#
# Original Script:    export_tracks.py(by 3DE) - modified by Hyuk Ko
#

#
# main script...

import tempfile

TEMP = tempfile.gettempdir()

c	= tde4.getCurrentCamera()
pg	= tde4.getCurrentPGroup()
if c!=None and pg!=None:
	
	req	= tde4.createCustomRequester()
	tde4.addTextFieldWidget(req,"frame_offset_field","Frame Offset","0")
	tde4.addFileWidget(req,"file_browser","Filename...","*.txt")
	
	ret	= tde4.postCustomRequester(req,"Import ZLOC from Clipboard...",500,0,"From TXT","From TEMP","Cancel")
	if ret==1:
		path = tde4.getWidgetValue(req,"file_browser")
		offset = int(tde4.getWidgetValue(req,"frame_offset_field"))
		
		if path!=None:
			#
			# main block...
			
			rawList = []
			with open(path,'r') as f:
				rawList = [word for line in f for word in line.split()]
				
			zlocNameList = sorted(set(rawList[0::4]), key=rawList.index)
			groupByFourList = [rawList[i:i+4] for i in range(0, len(rawList), 4)]
			
			for zlocName in zlocNameList:
				p = tde4.createPoint(pg)
				tde4.setPointName(pg,p,zlocName)
			
				for i in range(len(groupByFourList)):
					if groupByFourList[i][0] == zlocName:
						tde4.setPointPosition2D(pg,p,c,int(groupByFourList[i][1])+offset,[(float(groupByFourList[i][2])+1)/2,(float(groupByFourList[i][3])-1)/-2])
		else:
			tde4.postQuestionRequester("Import ZLOC...","Error, couldn't open file.","Ok")
	
	if ret==2:
		path = TEMP + '/zloc_temp.txt'
		offset = int(tde4.getWidgetValue(req,"frame_offset_field"))
		
		if path!=None:
			#
			# main block...
			
			rawList = []
			with open(path,'r') as f:
				rawList = [word for line in f for word in line.split()]
				
			zlocNameList = sorted(set(rawList[0::4]), key=rawList.index)
			groupByFourList = [rawList[i:i+4] for i in range(0, len(rawList), 4)]
			
			for zlocName in zlocNameList:
				p = tde4.createPoint(pg)
				tde4.setPointName(pg,p,zlocName)
			
				for i in range(len(groupByFourList)):
					if groupByFourList[i][0] == zlocName:
						tde4.setPointPosition2D(pg,p,c,int(groupByFourList[i][1])+offset,[(float(groupByFourList[i][2])+1)/2,(float(groupByFourList[i][3])-1)/-2])
		else:
			tde4.postQuestionRequester("Import ZLOC...","Error, couldn't open file.","Ok")
else:
	tde4.postQuestionRequester("Import ZLOC...","There is no current Point Group or Camera.","Ok")

