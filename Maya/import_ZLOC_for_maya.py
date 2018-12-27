##
## Script:      import_ZLOC_for_MAYA.py v1.0
##
## Author:      Hyuk Ko
##              kohyuk91@gmail.com
##
## Date:        2018/12/27 #v1.1
##              2018/08/07 #v1.0
##
## Description: Creates locators that are constrained to TrackerU/V coordinates
##
## Usage:       1.Select camera and run script
##              2.Click 'TXT' or 'TEMP'
##

   
import maya.cmds as mc
import tempfile

class ImportZLOC():
    
    def __init__(self):
        
        self.win = 'Import_ZLOC'
        self.TEMP = tempfile.gettempdir()
        
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
            mc.button(label='TEMP', command=self.import_from_temp)
            mc.setParent('..')
            
            mc.separator(height=15, style='out') #############################
            
            mc.button(label='CREATE EMPTY ZLOC', command=self.create_empty_zloc)
            
            mc.separator(height=15, style='out') #############################
                       
            mc.showWindow(self.win)
        else:
            mc.confirmDialog( title='WARNING', message='Select a Camera!')
    
    def import_from_txt(self, a):
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
        
        
    def import_from_temp(self, a):
        grpExist = False
        
        if len(mc.ls(selection=True, long=True))==1 and mc.objectType(mc.listRelatives(mc.ls(selection=True, long=True), shapes=True, fullPath=True)[0]) == 'camera':
            selCam_Name = mc.ls(selection=True, long=True)[0] # Get Camera
            selCam_Shape = mc.listRelatives(selCam_Name, shapes=True, fullPath=True)[0] # Get 'Shape' of Camera
            
            path = self.TEMP + '/zloc_temp.txt' # Get Txt file Path
                    
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
            
    def create_empty_zloc(self, a):
        grpExist = False
        
        if len(mc.ls(selection=True, long=True))==1 and mc.objectType(mc.listRelatives(mc.ls(selection=True, long=True), shapes=True, fullPath=True)[0]) == 'camera':
            selCam_Name = mc.ls(selection=True, long=True)[0] # Get Camera
            selCam_Shape = mc.listRelatives(selCam_Name, shapes=True, fullPath=True)[0] # Get 'Shape' of Camera
            
            #path = mc.fileDialog2(fileFilter='*.txt', dialogStyle=2, fileMode=1)[0] # Get Txt file Path
                    
            if True:
                #word_list = []
                
                locName_list = ['null_zloc'] #sorted(set(word_list[0::4]),key=word_list.index) # Get Locator Names from List ex) ['zloc01','zloc02', ......]
                word_four_list = [['null_zloc','1','0','0']]#[word_list[i:i+4] for i in range(0, len(word_list), 4)] # Group Elements By 4 ex) [['zloc01','1','0.198568','0.754568'],['zloc01','2','0.188568','0.784568'], ......]
                
                if mc.objExists('zloc_grp'):
                    grpExist = True
                else:
                    mc.group(n='zloc_grp',empty=True) # Create zloc Group
                    mc.createDisplayLayer(name="ZLocLayer", empty=True)
                    mc.setAttr('ZLocLayer.color', 17)
                    mc.editDisplayLayerMembers('ZLocLayer', 'zloc_grp', noRecurse=True)
                    
                null_zloc = mc.spaceLocator(n='null_zloc_#')[0]
                mc.addAttr(null_zloc, longName='TrackerU', attributeType='double', defaultValue=0)
                mc.addAttr(null_zloc, longName='TrackerV', attributeType='double', defaultValue=0)
                mc.addAttr(null_zloc, longName='OffsetU', attributeType='double', defaultValue=0)
                mc.addAttr(null_zloc, longName='OffsetV', attributeType='double', defaultValue=0)
                mc.setAttr(null_zloc + '.TrackerU', keyable=True)
                mc.setAttr(null_zloc + '.TrackerV', keyable=True)
                mc.setAttr(null_zloc + '.OffsetU', keyable=True)
                mc.setAttr(null_zloc + '.OffsetV', keyable=True)
                mc.setAttr(null_zloc + '.sx', 0.1)
                mc.setAttr(null_zloc + '.sy', 0.1)
                mc.setAttr(null_zloc + '.sz', 0.01)
                    
                mc.expression(s=null_zloc + '.translateX=((((-10 *' + null_zloc + '.translateZ) / ' + selCam_Name + '.focalLength) * (' + selCam_Name + '.horizontalFilmAperture * 2.54) ) / 2 ) * (' + null_zloc + '.TrackerU +' + null_zloc + '.OffsetU)', object=null_zloc, alwaysEvaluate=True, unitConversion='all')
                mc.expression(s=null_zloc + '.translateY=((((-10 *' + null_zloc + '.translateZ) / ' + selCam_Name + '.focalLength) * (' + selCam_Name + '.verticalFilmAperture * 2.54) ) / -2 ) * (' + null_zloc + '.TrackerV +' + null_zloc + '.OffsetV)', object=null_zloc, alwaysEvaluate=True, unitConversion='all')
                newZLocName = mc.ls(mc.parent(null_zloc, 'zloc_grp'),long=True)[0]
                mc.xform(newZLocName, a=True, rotation=(0,0,0))
                mc.setAttr(newZLocName + '.tz', -10)
                
                
                if grpExist == False:
                    mc.parentConstraint(selCam_Name, 'zloc_grp', maintainOffset=False) # Parent Constraint zloc Group to Camera
                    mc.scaleConstraint(selCam_Name, 'zloc_grp', maintainOffset=True) # Scale Constraint zloc Group to Camera
                else:
                    pass
    
            else:
                mc.confirmDialog( title='WARNING', message='Something is Wrong!')
                mc.deleteUI(self.win)
        else:
            mc.confirmDialog( title='WARNING', message='Select a Camera!')
            mc.deleteUI(self.win)

ImportZLOC().display()
