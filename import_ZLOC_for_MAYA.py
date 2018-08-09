##
## Script:      import_ZLOC_for_MAYA.py v1.0
##
## Author:      Hyuk Ko
##              kohyuk91@gmail.com
##
## Date:        2018/08/07
##
## Description: Creates locators that are constrained to TrackerU/V coordinates
##
## Usage:       1.Select camera and run script
##              2.Click 'TXT' or 'CLIPBOARD'
##

try:
    from PySide2 import QtGui # MAYA2017+
except:
    from PySide import QtGui
    
import maya.cmds as mc

class ImportZLOC():
    
    def __init__(self):
        
        self.win = 'Import_ZLOC'
        
    def display(self):
        
        if len(mc.ls(selection=True, long=True))==1 and mc.objectType(mc.listRelatives(mc.ls(selection=True, long=True), shapes=True, fullPath=True)[0]) == 'camera':

            if mc.window(self.win, exists=True):
                mc.deleteUI(self.win)
            
            mc.window(self.win, sizeable=True, resizeToFitChildren=True)
            
            mc.rowColumnLayout(nc=1)
            
            mc.separator(height=15, style='out') #############################
            
            mc.text(label='Import from...', font='boldLabelFont')
            
            mc.separator(height=15, style='out') #############################
            
            mc.rowColumnLayout(nc=2, columnWidth=[(1,100),(2,100)])
            mc.button(label='TXT', command=self.import_from_txt)
            mc.button(label='CLIPBOARD', command=self.import_from_clipboard)
            mc.setParent('..')
            
            mc.separator(height=15, style='out') #############################
                       
            mc.showWindow(self.win)
        else:
            mc.confirmDialog( title='WARNING', message='Select a Camera!')
    
    def import_from_txt(self,a):
        grpExist = False
        
        if len(mc.ls(selection=True, long=True))==1 and mc.objectType(mc.listRelatives(mc.ls(selection=True, long=True), shapes=True, fullPath=True)[0]) == 'camera':
            selCam_Name = mc.ls(selection=True, long=True)[0] # Get Camera
            selCam_Shape = mc.listRelatives(selCam_Name, shapes=True, fullPath=True)[0] # Get 'Shape' of Camera
            
            path = mc.fileDialog2(fileFilter='*.txt', dialogStyle=2, fileMode=1)[0] # Get Txt file Path
                    
            if path[-3:] == 'txt':
                word_list = []
                with open(path,'r') as f:
                    word_list = [word for line in f for word in line.split()] # Open txt & Append All Words as Single Elements to List ex) ['zloc01','1','0.198568','0.754568','zloc01','2','0.188568','0.784568', ......]
                    
                locName_list = sorted(set(word_list[0::4]),key=word_list.index) # Get Locator Names from List ex) ['zloc01','zloc02', ......]
                word_four_list = [word_list[i:i+4] for i in range(0, len(word_list), 4)] # Group Elements By 4 ex) [['zloc01','1','0.198568','0.754568'],['zloc01','2','0.188568','0.784568'], ......]
                
                if mc.objExists('zloc_grp'):
                    grpExist = True
                else:
                    mc.group(n='zloc_grp',empty=True) # Create zloc Group
                    
                for i in locName_list: # Create Locators from 'locName_list' & Parent to zloc Group & Set Expression
                    loc = mc.spaceLocator(n=i)
                    locShape = mc.listRelatives(loc[0], shapes=True)[0]
                    mc.setAttr(locShape + '.overrideEnabled', 1)
                    mc.setAttr(locShape + '.overrideColor', 17)
                    mc.addAttr(i, longName='TrackerU', attributeType='double', defaultValue=0)
                    mc.addAttr(i, longName='TrackerV', attributeType='double', defaultValue=0)
                    mc.addAttr(i, longName='OffsetU', attributeType='double', defaultValue=0)
                    mc.addAttr(i, longName='OffsetV', attributeType='double', defaultValue=0)
                    mc.setAttr(i + '.TrackerU', keyable=True)
                    mc.setAttr(i + '.TrackerV', keyable=True)
                    mc.setAttr(i + '.OffsetU', keyable=True)
                    mc.setAttr(i + '.OffsetV', keyable=True)
                    mc.setAttr(i + '.sx', 0.1)
                    mc.setAttr(i + '.sy', 0.1)
                    mc.setAttr(i + '.sz', 0.001)
                    
                    mc.expression(s=i + '.translateX=((((-10 *' + i + '.translateZ) / ' + selCam_Name + '.focalLength) * (' + selCam_Name + '.horizontalFilmAperture * 2.54) ) / 2 ) * (' + i + '.TrackerU +' + i + '.OffsetU)', object=i, alwaysEvaluate=True, unitConversion='all')
                    mc.expression(s=i + '.translateY=((((-10 *' + i + '.translateZ) / ' + selCam_Name + '.focalLength) * (' + selCam_Name + '.verticalFilmAperture * 2.54) ) / -2 ) * (' + i + '.TrackerV +' + i + '.OffsetV)', object=i, alwaysEvaluate=True, unitConversion='all')
                    newZLocName = mc.ls(mc.parent(i, 'zloc_grp'),long=True)[0]
                    mc.xform(newZLocName, objectSpace=True, rotation=(0,0,0))
                    mc.setAttr(newZLocName + '.tz', -10)
                
                if grpExist == False:
                    mc.parentConstraint(selCam_Name, 'zloc_grp', maintainOffset=False) # Parent Constraint zloc Group to Camera
                    mc.scaleConstraint(selCam_Name, 'zloc_grp', maintainOffset=True) # Scale Constraint zloc Group to Camera
                else:
                    pass
                
                for i in range(len(word_four_list)):
                    mc.setKeyframe(word_four_list[i][0], t=int(word_four_list[i][1]), v=float(word_four_list[i][2]), at='TrackerU')
                    mc.setKeyframe(word_four_list[i][0], t=int(word_four_list[i][1]), v=float(word_four_list[i][3]), at='TrackerV')
                    
                mc.deleteUI(self.win)
                
            else:
                mc.confirmDialog( title='WARNING', message='No Path!')
                mc.deleteUI(self.win)
        else:
            mc.confirmDialog( title='WARNING', message='Select a Camera!')
            mc.deleteUI(self.win)
        
        
    def import_from_clipboard(self,a):
        grpExist = False
        
        if len(mc.ls(selection=True, long=True))==1 and mc.objectType(mc.listRelatives(mc.ls(selection=True, long=True), shapes=True, fullPath=True)[0]) == 'camera':
            selCam_Name = mc.ls(selection=True, long=True)[0] # Get Camera
            selCam_Shape = mc.listRelatives(selCam_Name, shapes=True, fullPath=True)[0] # Get 'Shape' of Camera
            cb = QtGui.QClipboard() # Get Clipboard
            cbText = str(cb.text()) # Make Clipboard into String
            
            if cbText[0:4] == 'zloc' or cbText[0:7] == 'Tracker':
                word_list = cbText.split() # Append All Words as Single Elements to List ex) ['zloc01','1','0.198568','0.754568','zloc01','2','0.188568','0.784568', ......]    
                locName_list = sorted(set(word_list[0::4]),key=word_list.index) # Get Locator Names from List ex) ['zloc01','zloc02', ......]
                word_four_list = [word_list[i:i+4] for i in range(0, len(word_list), 4)] # Group Elements By 4 ex) [['zloc01','1','0.198568','0.754568'],['zloc01','2','0.188568','0.784568'], ......]
                
                if mc.objExists('zloc_grp'):
                    grpExist = True
                else:
                    mc.group(n='zloc_grp',empty=True) # Create zloc Group
                for i in locName_list: # Create Locators from 'locName_list' & Parent to zloc Group & Set Expression
                    loc = mc.spaceLocator(n=i)
                    locShape = mc.listRelatives(loc[0], shapes=True)[0]
                    mc.setAttr(locShape + '.overrideEnabled', 1)
                    mc.setAttr(locShape + '.overrideColor', 17)
                    mc.addAttr(i, longName='TrackerU', attributeType='double', defaultValue=0)
                    mc.addAttr(i, longName='TrackerV', attributeType='double', defaultValue=0)
                    mc.addAttr(i, longName='OffsetU', attributeType='double', defaultValue=0)
                    mc.addAttr(i, longName='OffsetV', attributeType='double', defaultValue=0)
                    mc.setAttr(i + '.TrackerU', keyable=True)
                    mc.setAttr(i + '.TrackerV', keyable=True)
                    mc.setAttr(i + '.OffsetU', keyable=True)
                    mc.setAttr(i + '.OffsetV', keyable=True)
                    mc.setAttr(i + '.sx', 0.1)
                    mc.setAttr(i + '.sy', 0.1)
                    mc.setAttr(i + '.sz', 0.001)
                    
                    mc.expression(s=i + '.translateX=((((-10 *' + i + '.translateZ) / ' + selCam_Name + '.focalLength) * (' + selCam_Name + '.horizontalFilmAperture * 2.54) ) / 2 ) * (' + i + '.TrackerU +' + i + '.OffsetU)', object=i, alwaysEvaluate=True, unitConversion='all')
                    mc.expression(s=i + '.translateY=((((-10 *' + i + '.translateZ) / ' + selCam_Name + '.focalLength) * (' + selCam_Name + '.verticalFilmAperture * 2.54) ) / -2 ) * (' + i + '.TrackerV +' + i + '.OffsetV)', object=i, alwaysEvaluate=True, unitConversion='all')
                    newZLocName = mc.ls(mc.parent(i, 'zloc_grp'),long=True)[0]
                    mc.xform(newZLocName, objectSpace=True, rotation=(0,0,0))
                    mc.setAttr(newZLocName + '.tz', -10)
                
                if grpExist == False:
                    mc.parentConstraint(selCam_Name, 'zloc_grp', maintainOffset=False) # Parent Constraint zloc Group to Camera
                    mc.scaleConstraint(selCam_Name, 'zloc_grp', maintainOffset=True) # Scale Constraint zloc Group to Camera
                else:
                    pass
                for i in range(len(word_four_list)):
                    mc.setKeyframe(word_four_list[i][0], t=int(word_four_list[i][1]), v=float(word_four_list[i][2]), at='TrackerU')
                    mc.setKeyframe(word_four_list[i][0], t=int(word_four_list[i][1]), v=float(word_four_list[i][3]), at='TrackerV')
                
                mc.deleteUI(self.win)
                
            else:
                mc.confirmDialog( title='WARNING', message='Check Clipboard!')
                mc.deleteUI(self.win)
        else:
            mc.confirmDialog( title='WARNING', message='Select a Camera!')
            mc.deleteUI(self.win)

ImportZLOC().display()
