"""
	script: 	ekn_undo_history.py
	author: 	Francesco Surace
	date:		05/2013
	version:	0.1

	Description
		Navigate inside the undo history
"""

# Import Modules
import pymel.core
from functools import partial 


# Global Variables
file_path = ""
file_name = "ekn_undo_history.txt"



class ekn_undo_history_window(object):

    def __init__(self):
        '''
          Init Function
        '''
        self._ver = "0.1"
        self._base_name = "Ekn-Undo History"
        self._title = "Ekn-Undo History v{0}".format(self._ver)
        # Check if window exists
        if pymel.core.window(self._base_name, exists=True):
            pymel.core.deleteUI(self._base_name, window=True)
            
        self.main_window = pymel.core.window( self._base_name, 
                                              title=self._title,
                                              widthHeight=(350, 600), 
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

        # Area refresh button
        pymel.core.separator( height=20, style='in', parent=self._layout["main"] )
        self._layout["area_refresh_rowLayout"] = pymel.core.rowLayout( adjustableColumn=True, 
                                                                      numberOfColumns=1, 
                                                                      parent=self._layout["main"] )
        ekn_button_refresh = pymel.core.button( label='REFRESH', parent=self._layout["area_refresh_rowLayout"] )
        pymel.core.separator( height=20, style='in', parent=self._layout["main"] )

        # Area results list
        content_form_layout = pymel.core.formLayout(  enableBackground=True,
                                                      backgroundColor=(0.4,0.4,0.4), 
                                                      height=500,
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
        number_items = pymel.core.text( label=('Queue Size :  '), height=30, parent=self._layout["main"] )

        # Run command to write the file
        pymel.core.button( ekn_button_refresh, edit=True, command=partial( self.write_history_on_file, result_list, number_items ) )
        self.write_history_on_file( result_list, number_items )

        # Add callback to item
        pymel.core.treeView( result_list, edit=True, itemDblClickCommand=partial(self.selectTreeCallBack, result_list, number_items) ) # selection command
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


    def selectTreeCallBack(self, tree_list, undo_count, *args):
        '''
          Execute the undo command on the item selected
        '''
        index_item_selected = -100
        all_items = pymel.core.treeView( tree_list, query=True, children='' )
        for itm in all_items:
            # Check if the item is selected and stop after first selection
            if ( pymel.core.treeView( tree_list, query=True, itemSelected=itm ) ): 
                index_item_selected = pymel.core.treeView( tree_list, query=True, itemIndex=itm )
                break

        # Run Undo command until the item index selected
        if (index_item_selected > 0):
            i = index_item_selected
            while (i>0) & (i<=index_item_selected):
                pymel.core.undo()
                i=i-1

        self.write_history_on_file( tree_list, undo_count )


    def editLabelCallback(self, *args):
        '''
          Lock the rename command
        '''
        pymel.core.warning("you can\'t rename the object from here!")
        return ''


    def write_history_on_file( self, tree_view, items_founded, *args ):
        '''
          Write undo history file in the workspace directory
        '''
        # Recall global variables
        global file_name, file_path

        # Set undo commands to infitiny and clear treeView UI
        pymel.core.undoInfo( state=True, infinity=True )
        pymel.core.treeView( tree_view, e=True, removeAll=True  )

        # Set actual directory for save the file
        file_path = pymel.core.workspace( query=True, dir=True )

        # Setup maya script editor to write the correct command on file
        pymel.core.scriptEditorInfo(edit=True, historyFilename=file_path+file_name)
        pymel.core.scriptEditorInfo( edit=True, writeHistory=True )
        pymel.core.scriptEditorInfo( edit=True, clearHistoryFile=True)
        pymel.core.undoInfo( query=True, printQueue=True)
        pymel.core.scriptEditorInfo( edit=True, writeHistory=False )

        # Update TreeView list
        self.update_list( tree_view, items_founded )
        

    def update_list( self, tree_view_list, lenght_history, *args ):
        '''
          Load from file and update a treeview list
        '''
        # Recall global variables
        global file_name, file_path

        item_list = []

        # open file .txt in read mode
        file_read = open(file_path+file_name, 'r')
        # Put all lines inside the lists
        item_list = file_read.readlines() 
        # Close file
        file_read.close()
        # Reverse item_list
        item_list.reverse()

        # Put items into the list
        if len(item_list) > 0:
            for item in item_list:
                if item.find('<function') == -1: # Doesn't print the stack function
                    pymel.core.treeView( tree_view_list, edit=True, addItem=(item, "")  )
        
        # Update text results UI
        pymel.core.text( lenght_history, edit=True, label=('Queue Size : '+ str( len(item_list) ) ) )


    @classmethod
    def UI(ekn_undo_history_window):
        win_ui = ekn_undo_history_window()
        win_ui.show_window()
    
    
def UI():
    output_ui = OutputManager_UI()
    output_ui.show_window()


# Launch the window
win = ekn_undo_history_window.UI()

