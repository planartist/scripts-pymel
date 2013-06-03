"""
	script: 	ekn_search.py
	author: 	Francesco Surace
	date:		  05/2013
	version:	0.1

	Description
		Search by name an object into the Maya scene
"""

# Import Modules
import pymel.core
from functools import partial 


class ekn_search_window(object):

    def __init__(self):
        '''
          Init Function
        '''
        self._ver = "0.1"
        self._base_name = "Ekn-Search"
        self._title = "Ekn-Search v{0}".format(self._ver)
        # Check if window exists
        if pymel.core.window(self._base_name, exists=True):
            pymel.core.deleteUI(self._base_name, window=True)
            
        self.main_window = pymel.core.window( self._base_name, 
                                              title=self._title,
                                              widthHeight=(350, 400), 
                                              resizeToFitChildren=True, 
                                              sizeable=True )
        self._layout = dict()
        self.build()
        
    
    def frame_layout(self):
        '''
          Create windows layout
        '''
        self._layout["main"] = pymel.core.columnLayout( adjustableColumn=True,
                                                        columnOffset=('both', 10),
                                                        parent=self.main_window )

        # Area search text field
        pymel.core.separator( height=20, style='in', parent=self._layout["main"] )
        self._layout["area_search_rowLayout"] = pymel.core.rowLayout( adjustableColumn=True, 
                                                                      numberOfColumns=2, 
                                                                      parent=self._layout["main"] )
        ekn_input_text_field = pymel.core.textField( parent=self._layout["area_search_rowLayout"] )
        ekn_input_button = pymel.core.button( label='Search', 
                                              width=60,
                                              parent=self._layout["area_search_rowLayout"] )
        pymel.core.separator( height=20, style='in', parent=self._layout["main"] )

        # Area results list
        content_form_layout = pymel.core.formLayout(  enableBackground=True,
                                                      backgroundColor=(0.4,0.4,0.4), 
                                                      height=300,
                                                      parent=self._layout["main"] )
        result_list = pymel.core.treeView(  allowReparenting=False, 
                                            numberOfButtons=0, 
                                            attachButtonRight=False, 
                                            enableKeys=True,
                                            parent=content_form_layout )

        # Set treeView layout inside formLayout
        pymel.core.formLayout( content_form_layout, e=True, attachForm=(result_list,'top', 2) )
        pymel.core.formLayout( content_form_layout, e=True, attachForm=(result_list,'left', 2) )
        pymel.core.formLayout( content_form_layout, e=True, attachForm=(result_list,'bottom', 2) )
        pymel.core.formLayout( content_form_layout, e=True, attachForm=(result_list,'right', 2) )
        
        # Print number of results founded
        number_items = pymel.core.text( label=('About (  ) results'), height=30, parent=self._layout["main"] )

        # How to launch the search command
        pymel.core.button( ekn_input_button, edit=True, command=partial( self.search_engine, ekn_input_text_field, result_list, number_items ) )
        pymel.core.textField( ekn_input_text_field, e=True, aie=True, enterCommand=partial( self.search_engine, ekn_input_text_field, result_list, number_items ) )

        # Add callback to item
        pymel.core.treeView( result_list, edit=True, selectionChangedCommand=partial(self.selectTreeCallBack, result_list) ) # selection command
        pymel.core.treeView( result_list, edit=True, editLabelCommand=self.editLabelCallback ) # lock rename

        pymel.core.setParent(self._layout["main"])


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


    def selectTreeCallBack(self, tree_list, *args):
        '''
          Select objects inside the Maya scene
        '''
        pymel.core.select(clear=True)

        all_items = pymel.core.treeView( tree_list, query=True, children='' )
        for itm in all_items:
          # Check if the item is selected and exists inside Maya
          if ( pymel.core.treeView( tree_list, query=True, itemSelected=itm ) & (pymel.core.objExists(itm)) ): 
            pymel.core.select(str(itm), add=True)    
          # if the object was deleted, it's selected inside the list with a red colour
          elif not(pymel.core.objExists(itm)): 
            pymel.core.treeView( tree_list, edit=True, selectItem=(itm,True), selectionColor=(itm, 1,0,0) )


    def editLabelCallback(self, *args):
        '''
          Lock the rename command
        '''
        pymel.core.warning("you can\'t rename the object from here!")
        return ''


    def search_engine( self, input_text, tree_view, items_founded, *args ):
        '''
          Search Algorithm
        '''
        # Clean list and treeView UI
        item_list = []
        pymel.core.treeView( tree_view, e=True, removeAll=True  )
        
        name = pymel.core.textField( input_text, query=True, text=True )
        if (name != ''):
          filter_transform = pymel.core.itemFilter( byType=('transform') )
          filter_name = pymel.core.itemFilter( byName=('*'+name+'*') )
          filter_result = pymel.core.itemFilter( intersect=(filter_transform, filter_name) )

          # Put items into list
          for item in pymel.core.lsThroughFilter( filter_result, sort='byName' ):
            item_list.append(item)
          
          # Delete all filters
          pymel.core.delete( filter_transform, filter_name, filter_result )

          # Update treeView UI
          for obj in item_list:
            pymel.core.treeView( tree_view, edit=True, addItem=(str(obj), "")  )

          # Update text results UI
          pymel.core.text( items_founded, edit=True, label=('About ( '+ str( len(item_list) ) +' ) results') )


    @classmethod
    def UI(ekn_search_window):
        win_ui = ekn_search_window()
        win_ui.show_window()
    
    
def UI():
    output_ui = OutputManager_UI()
    output_ui.show_window()


# Launch the window
win = ekn_search_window.UI()

