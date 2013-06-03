"""
    script:     ekn_light_editor.py
    author:     Francesco Surace
    date:       05/2013
    version:    0.1

    Description
        Maya and Arnold Light Manager
"""

# Import Modules
import pymel.core
from functools import partial 


# Global Variables
const_prefix_sets = 'eknLightSet_'


class ekn_light_manager_window(object):

    def __init__(self):
        '''
          Init Function
        '''
        self._ver = "0.1"
        self._base_name = "Ekn-Light Manager"
        self._title = "Ekn-Light Manager v{0}".format(self._ver)
        # Check if window exists
        if pymel.core.window(self._base_name, exists=True):
            pymel.core.deleteUI(self._base_name, window=True)
            
        self.main_window = pymel.core.window( self._base_name, 
                                              title=self._title,
                                              widthHeight=(350, 700), 
                                              resizeToFitChildren=True, 
                                              sizeable=False )
        self._layout = dict()
        self.build()
        
    
    def frame_layout(self):
        '''
          Create windows layout
        '''
        self._layout["main"] = pymel.core.columnLayout( adjustableColumn=True,
                                                        columnOffset=('both', 10),
                                                        parent=self.main_window )

        # Main tree lister
        group_treeView_list = pymel.core.treeView()
        lights_treeView_list = pymel.core.treeView()

        # Area toolbar text field
        pymel.core.separator( height=20, style='in', parent=self._layout["main"] )

        # Toolbar buttons lights
        self._layout["area_toolbar_rowLayout"] = pymel.core.rowLayout( adjustableColumn=True, 
                                                                      numberOfColumns=8,
                                                                      parent=self._layout["main"] )
                                                        
        self._layout["shelf_content"] = pymel.core.columnLayout( parent=self._layout["area_toolbar_rowLayout"] )        

        # Shelf light buttons
        self._layout["shelf"] = pymel.core.rowLayout(   numberOfColumns=11, 
                                                        parent=self._layout["shelf_content"], 
                                                        columnAttach=[  (1, 'left', 5), (2, 'left', 5), (3, 'left', 5), (4, 'left', 5), 
                                                                        (5, 'both', 15), (6, 'left', 0), (7, 'left', 5), (8, 'both', 5),
                                                                        (9, 'left', 15), (10, 'left', 15), (11, 'both', 5)] )
        # Spot Light
        self._layout["btn_spot_light"] = pymel.core.nodeIconButton( style='iconOnly',
                                                                    image='spotlight.png',
                                                                    parent=self._layout["shelf"], 
                                                                    width=44, 
                                                                    height=44,
                                                                    command=partial(self.create_light, 'spotLight', group_treeView_list, lights_treeView_list) )
        # Directional Light
        self._layout["btn_directional_light"] = pymel.core.nodeIconButton(  style='iconOnly',
                                                                            image='directionallight.png',
                                                                            parent=self._layout["shelf"], 
                                                                            width=44, 
                                                                            height=44,
                                                                            command=partial(self.create_light, 'directionalLight', group_treeView_list, lights_treeView_list) )

        # Area Light
        self._layout["btn_area_light"] = pymel.core.nodeIconButton( style='iconOnly',
                                                                    image='arealight.png',
                                                                    parent=self._layout["shelf"], 
                                                                    width=44, 
                                                                    height=44,
                                                                    command=partial(self.create_light, 'areaLight', group_treeView_list, lights_treeView_list) )

        # Point Light
        self._layout["btn_point_light"] = pymel.core.nodeIconButton(    style='iconOnly',
                                                                        image='pointlight.png',
                                                                        parent=self._layout["shelf"], 
                                                                        width=44, 
                                                                        height=44,
                                                                        command=partial(self.create_light, 'pointLight', group_treeView_list, lights_treeView_list) )

        # Separator Center
        pymel.core.separator( height=50, horizontal=False, style='in', parent=self._layout["shelf"] )

  
        # Area Light
        self._layout["btn_area_light"] = pymel.core.nodeIconButton( style='iconOnly',
                                                                    image='aiAreaLight.png',
                                                                    parent=self._layout["shelf"], 
                                                                    width=44, 
                                                                    height=44,
                                                                    command=partial(self.create_light, 'aiAreaLight', group_treeView_list, lights_treeView_list) )
        # Dome Light
        self._layout["btn_dome_light"] = pymel.core.nodeIconButton( style='iconOnly',
                                                                    image='aiSkyDomeLight.png',
                                                                    parent=self._layout["shelf"], 
                                                                    width=44, 
                                                                    height=44,
                                                                    command=partial(self.create_light, 'aiSkyDomeLight', group_treeView_list, lights_treeView_list) )

        # Mesh Light
        self._layout["btn_mesh_light"] = pymel.core.nodeIconButton( style='iconOnly',
                                                                    image='aiMeshLight.png',
                                                                    parent=self._layout["shelf"], 
                                                                    width=44, 
                                                                    height=44,
                                                                    command=partial(self.create_light, 'aiAreaLight', group_treeView_list, lights_treeView_list) )

        # Line Separator
        pymel.core.separator( height=20, style='in', parent=self._layout["main"] )


         # Content - treeLister, attribute editor
        self._layout["content"] = pymel.core.rowLayout( numberOfColumns=3, rowAttach=[(1,'top',0), (2,'bottom',10), (3, 'bottom',10)], 
                                                        columnAttach=[(1,'left',-2), (2,'left',0), (3,'left',5)],
                                                        parent=self._layout["main"] )

        # Edit Buttons
        self._layout["edit_content"] = pymel.core.columnLayout( rowSpacing=5, parent=self._layout["content"])

        # Refresh button
        ekn_button_refresh = pymel.core.nodeIconButton(     style='iconOnly',
                                                            image='btn_refresh.png',
                                                            parent=self._layout["edit_content"], 
                                                            width=30, 
                                                            height=30,
                                                            command=partial( self.refresh_lists, group_treeView_list, lights_treeView_list ) )

        # Add button
        self._layout["btn_add_group"] = pymel.core.nodeIconButton(  style='iconOnly',
                                                                    image='btn_add.png',
                                                                    parent=self._layout["edit_content"], 
                                                                    width=30, 
                                                                    height=30,
                                                                    command=partial(self.add_group, group_treeView_list) )
        # Delete button
        self._layout["btn_delete_group"] = pymel.core.nodeIconButton(   style='iconOnly',
                                                                        image='btn_delete.png',
                                                                        parent=self._layout["edit_content"], 
                                                                        width=30, 
                                                                        height=30,
                                                                        command=partial(self.delete_group, group_treeView_list, lights_treeView_list) )

        content_form_group_layout = pymel.core.formLayout(  enableBackground=True,
                                                            backgroundColor=(0.4,0.4,0.4), 
                                                            height=300,
                                                            parent=self._layout["content"] )
        
        
        pymel.core.treeView(    group_treeView_list, edit=True, 
                                allowReparenting=False, 
                                numberOfButtons=0, 
                                attachButtonRight=False, 
                                enableKeys=True,
                                width=147,
                                parent=content_form_group_layout )

        content_form_lights_layout = pymel.core.formLayout( enableBackground=True,
                                                            backgroundColor=(0.4,0.4,0.4), 
                                                            height=300,
                                                            parent=self._layout["content"] )
        pymel.core.treeView(    lights_treeView_list, edit=True,
                                allowReparenting=False, 
                                numberOfButtons=0, 
                                attachButtonRight=False, 
                                enableKeys=True,
                                width=200,
                                parent=content_form_lights_layout )

        # Set treeView layout inside formLayout
        pymel.core.formLayout( content_form_group_layout, e=True, attachForm=(group_treeView_list,'top', 2) )
        pymel.core.formLayout( content_form_group_layout, e=True, attachForm=(group_treeView_list,'left', 2) )
        pymel.core.formLayout( content_form_group_layout, e=True, attachForm=(group_treeView_list,'bottom', 2) )
        pymel.core.formLayout( content_form_group_layout, e=True, attachForm=(group_treeView_list,'right', 2) )

        pymel.core.formLayout( content_form_lights_layout, e=True, attachForm=(lights_treeView_list,'top', 2) )
        pymel.core.formLayout( content_form_lights_layout, e=True, attachForm=(lights_treeView_list,'left', 2) )
        pymel.core.formLayout( content_form_lights_layout, e=True, attachForm=(lights_treeView_list,'bottom', 2) )
        pymel.core.formLayout( content_form_lights_layout, e=True, attachForm=(lights_treeView_list,'right', 2) )
        
        pymel.core.setParent(self._layout["main"])

        # Run Filter Lights
        self.create_default_light_group(group_treeView_list)
        pymel.core.treeView( group_treeView_list, edit=True, selectionChangedCommand=partial(self.update_lights_tree_view, group_treeView_list, lights_treeView_list) )
        pymel.core.treeView( lights_treeView_list, edit=True, selectionChangedCommand=partial(self.select_light, lights_treeView_list) )
        pymel.core.treeView( group_treeView_list, edit=True, editLabelCommand=self.editLabelCallback ) # lock rename
        pymel.core.treeView( lights_treeView_list, edit=True, editLabelCommand=self.editLabelCallback ) # lock rename


    def build(self):
        '''
          Build windows
        '''
        self.frame_layout()
        

    def show_window(self):
        '''
          Show Window
        '''
        pymel.core.showWindow( self.main_window )


    def create_default_light_group(self, tree_group_list, *args):
        '''
          Create default lights group
        '''
        pymel.core.treeView(    tree_group_list, edit=True,
                                addItem=[   ("DEFAULT", ""), ("Ambient", "DEFAULT"), ("Area", "DEFAULT"), ("Directional","DEFAULT"), 
                                            ("Point","DEFAULT"), ("Spot", "DEFAULT"), ("Volume", "DEFAULT"), ("Arnold", "DEFAULT") ] )


    def search_light_in_scene( self, *args ):
        '''
          Search lights in Maya scene and return the dictionary of lights grouped
        '''
        default_lights_grouped = {'spotLight':[], 'directionalLight':[], 'pointLight':[], 'areaLight':[], 'arnoldLight':[], 'ambientLight':[], 'volumeLight':[]}
        
        filter_current_maya_lights = pymel.core.itemFilter( byType=('light') )
        filter_shape_node = pymel.core.itemFilter( byType=('shape') )
        filter_name_arnold_node = pymel.core.itemFilter( byName=('ai*') ) # Name convention for Arnold's lights
        filter_current_arnold_lights = pymel.core.itemFilter( intersect=(filter_shape_node, filter_name_arnold_node) )
        filter_result = pymel.core.itemFilter( union=(filter_current_maya_lights, filter_current_arnold_lights) )

        # Put the lights into the right group inside the dictionary
        for item in pymel.core.lsThroughFilter( filter_result, sort='byType' ):
            if item[:2] == 'ai': # If it's Arnold's light
                # Add to dictionary the light
                default_lights_grouped['arnoldLight'].append(str(item))                
            else: # If not Arnold's light
                # Add to dictionary the light
                default_lights_grouped[str(item.type())].append(str(item))

        # Delete all filters
        pymel.core.delete( filter_current_maya_lights,filter_shape_node, filter_name_arnold_node, filter_current_arnold_lights, filter_result )

        #return a dictionary with all lights grouped
        return default_lights_grouped


    def search_new_group_added(self, *args):
        '''
          Search new sets to add in group list tree view
        '''
        all_scene_sets = pymel.core.listSets(allSets=True)
        ekn_light_set = []

        for c_set in all_scene_sets:
            if (str(c_set) != 'initialShadingGroup') & (str(c_set) != 'initialParticleSE') & (str(c_set) != 'defaultCreaseDataSet'):
                ekn_light_set.append(str(c_set))

        return ekn_light_set


    def update_group_added(self, tree_group_list, *args):
        '''
          Update list of group added
        '''
        ekn_light_set = self.search_new_group_added()

        if len(ekn_light_set)>0:
            for group in ekn_light_set:
                if not(pymel.core.treeView( tree_group_list, query=True, itemExists=str(group)[12:]) ):
                    pymel.core.treeView( tree_group_list, edit=True, addItem=(str(group)[12:], ''))


    def update_lights_tree_view( self, tree_group_list, tree_lights_list, *args ):
        '''
          Update tree view with all lights grouped
        '''
        pymel.core.treeView( tree_lights_list, edit=True, removeAll=True )

        lights_grouped = self.search_light_in_scene()

        all_items = pymel.core.treeView( tree_group_list, query=True, children='' )
        
        for itm in all_items:
            # Check if the item is selected
            if ( pymel.core.treeView( tree_group_list, query=True, itemSelected=itm ) ): 
                if  ((itm == 'Ambient') | (itm == 'Area') | 
                    (itm == 'Directional') | (itm == 'Point') | (itm == 'Spot') | 
                    (itm == 'Volume') | (itm == 'Arnold')):
                    # Add the lights in the right list
                        for lgt in lights_grouped[str(itm).lower()+"Light"]: 
                            if not(pymel.core.treeView( tree_lights_list, query=True, itemExists=str(lgt)) ):                      
                                pymel.core.treeView( tree_lights_list, edit=True, addItem=(str(lgt), ''))
                # Show all lights in default grops
                elif (itm == "DEFAULT"):
                    for grp in lights_grouped:
                        for lgt in lights_grouped[grp]:
                            if not(pymel.core.treeView( tree_lights_list, query=True, itemExists=str(lgt)) ): 
                                pymel.core.treeView( tree_lights_list, edit=True, addItem=(str(lgt), ''))
                # Group added by user
                else:
                    for lgt in pymel.core.listRelatives(const_prefix_sets+itm):
                        if not(pymel.core.treeView( tree_lights_list, query=True, itemExists=str(lgt)) ): 
                            pymel.core.treeView( tree_lights_list, edit=True, addItem=(str(lgt), ''))



    def create_light(self, name_node, tree_group_list, tree_lights_list, *args):
        '''
          Create lights
          For Area and Arnold light: set the connection with defaultLightSet
        '''
        if (name_node == 'areaLight') | (name_node == 'aiAreaLight') | (name_node == 'aiSkyDomeLight'):
            # Create Node
            item = pymel.core.createNode(name_node)
            # Connect light with the Maya's defaultLightSet
            item_transform = pymel.core.pickWalk(direction='up')
            pymel.core.connectAttr( str(item_transform)[3:-2]+'.instObjGroups', 'defaultLightSet.dagSetMembers', na=True )

        elif (name_node == 'spotLight'):
            pymel.core.spotLight()

        elif (name_node == 'directionalLight'):
            pymel.core.directionalLight()

        elif (name_node == 'pointLight'):
            pymel.core.pointLight()

        # Update Tree View
        self.update_lights_tree_view( tree_group_list, tree_lights_list )


    def select_light( self, tree_lights_list, *args ):
        '''
          Select the light only if it exists
        '''
        pymel.core.select(clear=True)

        all_items = pymel.core.treeView( tree_lights_list, query=True, children='' )
        for itm in all_items:
            # Check if the item is selected and exists inside Maya
            if ( pymel.core.treeView( tree_lights_list, query=True, itemSelected=itm ) & (pymel.core.objExists(itm)) ): 
                pymel.core.select(str(itm), add=True)    
                pymel.core.pickWalk(direction='up') # select also transform (just in case to delete the light)
            # if the object was deleted, it red selected inside the list
            elif not(pymel.core.objExists(itm)): 
                pymel.core.treeView( tree_lights_list, edit=True, selectItem=(itm,True), selectionColor=(itm, 1,0,0) )


    def editLabelCallback(self, *args):
        '''
          Lock the rename
        '''
        pymel.core.warning("you can\'t rename the object from here!")
        return ''


    def refresh_lists(self, tree_group_list, tree_lights_list, *args):
        '''
          Refresh tree view lists
        '''
        self.update_group_added(tree_group_list)
        self.update_lights_tree_view(tree_group_list, tree_lights_list)


    def dialog_set_name_group(self, *args):
        '''
          Dialog window to create new group
        '''
        result = pymel.core.promptDialog(   title='Group',
                                            message='Enter Name:',
                                            button=['OK', 'Cancel'],
                                            defaultButton='OK',
                                            cancelButton='Cancel',
                                            dismissString='Cancel' )
        if result == 'OK':
            return pymel.core.promptDialog(query=True, text=True)
        elif result == 'Cancel':
            return 'Cancel'


    def add_group(self, tree_group_list, *args):
        '''
          Add a new group of light
        '''
        name_group = self.dialog_set_name_group()
        if name_group == '':
            name_group = 'Light Group'
        
        # Check if user pressed the dismiss button
        if name_group != 'Cancel':
            new_set = pymel.core.sets(name=str((const_prefix_sets+name_group.upper())))
            pymel.core.lockNode(new_set) # Lock Node - Can't delete node from Maya
            pymel.core.sets( new_set, edit=True, addElement=pymel.core.ls(selection=True) )
            self.update_group_added(tree_group_list)
            

    def delete_group(self, tree_group_list, tree_lights_list, *args):
        '''
          Remove a group of light selected
        '''
        all_items = pymel.core.treeView( tree_group_list, query=True, children='' )
        for itm in all_items:
            # Check if the item is selected
            if ( pymel.core.treeView( tree_group_list, query=True, itemSelected=itm ) ): 
                # Check if the item is not a Default group and eliminate the group selected
                if ((itm != 'DEFAULT') & (itm != 'Ambient') & (itm != 'Area') & 
                    (itm != 'Directional') & (itm != 'Point') & (itm != 'Spot') & 
                    (itm != 'Volume') & (itm != 'Arnold') ):
                    pymel.core.lockNode(const_prefix_sets+str(itm), lock=False) # Unlock Node - Can delete node from Maya
                    pymel.core.delete(const_prefix_sets+str(itm))
        
        # Update and Refresh the treeView lists
        pymel.core.treeView(tree_group_list, edit=True, removeAll=True)
        self.create_default_light_group(tree_group_list)
        self.refresh_lists(tree_group_list, tree_lights_list)


    @classmethod
    def UI(ekn_light_manager_window):
        win_ui = ekn_light_manager_window()
        win_ui.show_window()
    
    
def UI():
    output_ui = OutputManager_UI()
    output_ui.show_window()


# Launch the window
win = ekn_light_manager_window.UI()

