#==============================================================================
# class for MaxPlanet GUI
#------------------------------------------------------------------------------
import os                 as os
import tkinter            as tk
import planet_lib         as lib

from   tkinter            import (ttk, font, messagebox, filedialog)
from   tkinter.messagebox import askyesno

#==============================================================================
# package's constants
#------------------------------------------------------------------------------
_WIN            = '1680x1050'
_DPI            = 100
_WIDTH_MAX      = 60

#==============================================================================
# class TPlanetGui
#------------------------------------------------------------------------------
class TPlanetGui(tk.Tk):
    
    #==========================================================================
    # Static variables & methods
    #--------------------------------------------------------------------------

    #==========================================================================
    # Constructor & utilities
    #--------------------------------------------------------------------------
    def __init__(self, journal, planet):
        "Creates and shows GUI for MaxPlanet"

        journal.I( 'TPlanetGui constructor...')
        
        #----------------------------------------------------------------------
        #iniciatizazia tk.Tk
        #----------------------------------------------------------------------
        super().__init__()
        self.user    = 'max'
        self.version = '0.01'

        #----------------------------------------------------------------------
        # Internal data
        #----------------------------------------------------------------------
        self.journal  = journal
        self.planet   = planet
        
        self.lblTiles = {}       # Zoznam  {lblTile: tile}
        
        #----------------------------------------------------------------------
        # Initialisation
        #----------------------------------------------------------------------
        self.show()   # Initial drawing

        self.journal.O( 'TPlanetGui created for Object {}'.format(self.title))

    #==========================================================================
    # GUI methods
    #--------------------------------------------------------------------------
    def show(self):
        "Shows Max Planet GUI"
        
        self.journal.I( f'TPlanetGui{self.title}.show' )
        
        #----------------------------------------------------------------------
        # Nastavenia root window
        #----------------------------------------------------------------------

        self.geometry('1435x740')
        self.minsize(1050,400)
        self.title(self.planet.name)
#        self.icon_path = resource_path('ikona.ico')
#        self.iconbitmap(self.icon_path)

        #----------------------------------------------------------------------
        # Nastavenia style
        #----------------------------------------------------------------------
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.layout('Custom.TNotebook', []) # copy of TNotebook
        self.style.configure('Treeview', bakcground='silver', foreground='black', rowheight=15, fieldbackground='grey' )
        self.style.map('Treeview', background=[('selected','green')] )

        #----------------------------------------------------------------------
        # Panel pre Status bar
        #----------------------------------------------------------------------
        self.statusBarShow()

        #----------------------------------------------------------------------
        # Pravy panel pre nastroje
        #----------------------------------------------------------------------
        self.toolsShow()
        
        #----------------------------------------------------------------------
        # Lavy panel pre mapu
        #----------------------------------------------------------------------
        self.frame_map = ttk.Frame(self, relief=tk.RAISED, borderwidth=1)
        self.frame_map.pack(side='left', fill='both')

#        self.mapShow()

        #----------------------------------------------------------------------
        # Vytvorim Menu pre click on Tile / nastavenie height
        #----------------------------------------------------------------------
        self.tileMenu = tk.Menu(self, tearoff = 0)
        
        for h in range(0, 3100, 200):
            self.tileMenu.add_command(label =f"Height :   {str(h).ljust(5)}", command=lambda t=str(h): self.tileHeight(t))
            
        
        self.journal.O( f'TPlanetGui{self.title}.show: End' )

    #==========================================================================
    # Status bar
    #--------------------------------------------------------------------------
    def statusBarShow(self):
       
        frame_status_bar = ttk.Frame(self, relief=tk.RAISED, borderwidth=1)
        frame_status_bar.pack(side='bottom', anchor='s', fill='x')
       
        frame_status_bar.columnconfigure(0, weight=5)
        frame_status_bar.columnconfigure(1, weight=1)
        frame_status_bar.columnconfigure(2, weight=1)
       
        self.str_status_bar = tk.StringVar(value = 'str_status_bar')
       
        status_bar_txt = ttk.Label(frame_status_bar, relief=tk.RAISED, textvariable=self.str_status_bar)
        status_bar_txt.grid(row = 0, column = 0, sticky = 'we' )
       
        status_bar_ver = ttk.Label(frame_status_bar, relief=tk.RAISED, text=f'(c) SIQO v. {self.version}')
        status_bar_ver.grid(row = 0, column = 2, padx = 3 ,sticky = 'we')

        #----------------------------------------------------------------------
        # URL Menu
        #----------------------------------------------------------------------
#        self.rcm_url = tk.Menu(self, tearoff = 0)

#        self.rcm_url.add_command(label=_URLS[0], command=lambda: self.changeUrl(_URLS[0]) )
#        self.rcm_url.add_command(label=_URLS[1], command=lambda: self.changeUrl(_URLS[1]) )
      
    #--------------------------------------------------------------------------
    def setStatus(self, mess):
       
        self.str_status_bar.set(mess)
 
    #==========================================================================
    # Pravy panel pre nastroje
    #--------------------------------------------------------------------------
    def toolsShow(self):
       
        frame_tool = ttk.Frame(self, relief=tk.RAISED, borderwidth=1)
        frame_tool.pack(side='right', anchor='e', expand=True, fill='both')
       
        #----------------------------------------------------------------------
        # TABS as ttk.Notebook
        #----------------------------------------------------------------------
        self.tab_selected = 0
       
        self.tabs = ttk.Notebook(frame_tool, style='TNotebook')
        self.tabs.pack(expand=True, fill='both')
        self.tabs.enable_traversal()
       
        # Vytkreslenie jednotlivych tabs
        self.tabEditShow()
        self.tabSimulShow()
   
        self.tabs.bind('<<NotebookTabChanged>>', self.tabChanged)
        self.tabs.select(self.tab_selected)
       
    #--------------------------------------------------------------------------
    def tabChanged(self, event):
       
        self.tabSelected = self.tabs.index("current")
#        self.refresh()

    #--------------------------------------------------------------------------
    def tabEditShow(self):
       
        #----------------------------------------------------------------------
        # Vytvorim frame a skonfigurujem grid
        #----------------------------------------------------------------------
        frm = ttk.Frame(self.tabs)

        frm.columnconfigure( 0, weight=1)
        frm.columnconfigure( 1, weight=1)
        frm.columnconfigure( 2, weight=1)
        frm.columnconfigure( 3, weight=1)
        frm.columnconfigure( 4, weight=1)
        frm.columnconfigure( 5, weight=1)
        frm.columnconfigure( 6, weight=1)
        frm.columnconfigure( 7, weight=1)
        frm.columnconfigure( 8, weight=1)
        frm.columnconfigure( 9, weight=1)
       
        frm.rowconfigure   (0, weight=1)
        frm.rowconfigure   (1, weight=1)
        frm.rowconfigure   (2, weight=1)
        frm.rowconfigure   (3, weight=1)
        frm.rowconfigure   (4, weight=1)
        frm.rowconfigure   (5, weight=1)
        frm.rowconfigure   (6, weight=1)
        frm.rowconfigure   (7, weight=1)
        frm.rowconfigure   (8, weight=1)
 
        # Vlozim frame do Tabs       
        self.tabs.add(frm, text='Edit Planet')
 
        #----------------------------------------------------------------------
        # Generate new geography
        #----------------------------------------------------------------------

        lbl_gen1 = ttk.Label(frm, relief=tk.FLAT, text='New Planet for')
        lbl_gen1.grid(row=0, column=1, sticky='e')
       
        self.str_rows = tk.StringVar(value=self.planet.rows)
        spin_rows = ttk.Spinbox(frm, from_=5, to=90, textvariable=self.str_rows, wrap=True, width=3)
        spin_rows.grid(row=0, column=2)
       
        lbl_gen2 = ttk.Label(frm, relief=tk.FLAT, text='rows  and' )
        lbl_gen2.grid(row=0, column=3)

        self.str_cols = tk.StringVar(value=self.planet.cols)
        spin_cols = ttk.Spinbox(frm, from_=5, to=90, textvariable=self.str_cols, wrap=True, width=3)
        spin_cols.grid(row=0, column=4)
       
        lbl_gen3 = ttk.Label(frm, relief=tk.FLAT, text='columns' )
        lbl_gen3.grid(row=0, column=5)

        btn_gen = ttk.Button(frm, text='Generate now', command=self.generate)
        btn_gen.grid(row=0, column=8, sticky='we')
        
        separator1 = ttk.Separator(frm, orient='horizontal')
        separator1.grid(row=1, column=1, columnspan=8, sticky='we')       
        
        #----------------------------------------------------------------------
        # Load & Save Buttons
        #----------------------------------------------------------------------
        btn_load = ttk.Button(frm, text='Load Planet', command=self.load)
        btn_load.grid(row=2, column=8, sticky='we')
        
        btn_save = ttk.Button(frm, text='Save Planet', command=self.save)
        btn_save.grid(row=3, column=8, sticky='we')
        
        separator2 = ttk.Separator(frm, orient='horizontal')
        separator2.grid(row=4, column=1, columnspan=8, sticky='we')       
        
        #----------------------------------------------------------------------
        # Edit Tile
        #----------------------------------------------------------------------
        self.lbl_tile = ttk.Label(frm, relief=tk.FLAT, text='I will work with Tile' )
        self.lbl_tile.grid(row=5, column=1, columnspan=8)
        
    #--------------------------------------------------------------------------
    def generate(self):

        self.planet.generate( int(self.str_rows.get()), int(self.str_cols.get()) )
        self.mapShow()
        
    #--------------------------------------------------------------------------
    def load(self):
        
        #----------------------------------------------------------------------
        # Zistim, kam mam zapisat
        #----------------------------------------------------------------------
        fileName = filedialog.askopenfilename(
            title      = 'Metadata file',
            initialdir = self.planet.fName,
            filetypes  = (('json files', '*.json'), ('All files', '*.*'))
            )
 
        if fileName == '': return
        
        #----------------------------------------------------------------------
        # Nacitanie metadat
        #----------------------------------------------------------------------
        self.setStatus(f'Loading planet from {fileName}')
        self.planet.fName = fileName
        self.planet.load()

        self.mapShow()
         
    #--------------------------------------------------------------------------
    def save(self):
        
        #----------------------------------------------------------------------
        # Zistim, kam mam zapisat
        #----------------------------------------------------------------------
        fileName = filedialog.asksaveasfile( mode='w', defaultextension=".json", initialfile = self.planet.fName)

        if fileName is None: return
        
        #----------------------------------------------------------------------
        # Nacitanie metadat
        #----------------------------------------------------------------------
        self.setStatus(f'Saving planet into {fileName.name}')
        self.planet.fName = fileName.name
        self.planet.save()
         
    #--------------------------------------------------------------------------
    def tabSimulShow(self):
       
        #----------------------------------------------------------------------
        # Vytvorim frame a skonfigurujem grid
        #----------------------------------------------------------------------
        frm = ttk.Frame(self.tabs)

        frm.columnconfigure( 0, weight=1)
        frm.columnconfigure( 1, weight=1)
        frm.columnconfigure( 2, weight=1)
        frm.columnconfigure( 3, weight=1)
        frm.columnconfigure( 4, weight=1)
       
        frm.rowconfigure   (0, weight=1)
        frm.rowconfigure   (1, weight=1)
        frm.rowconfigure   (2, weight=1)
        frm.rowconfigure   (3, weight=1)
        frm.rowconfigure   (4, weight=1)
        frm.rowconfigure   (5, weight=1)
        frm.rowconfigure   (6, weight=1)
        frm.rowconfigure   (7, weight=1)
        frm.rowconfigure   (8, weight=1)
 
        # Vlozim frame do Tabs       
        self.tabs.add(frm, text='Simulation')
 
        #----------------------------------------------------------------------
        # Obsah tab
        #----------------------------------------------------------------------
        
    #==========================================================================
    # Lavy panel pre mapu
    #--------------------------------------------------------------------------
    def mapShow(self):
       
        #----------------------------------------------------------------------
        # Odstranim existujuce lblTiles
        #----------------------------------------------------------------------
        for lblTile in self.lblTiles:
            lblTile.destroy()

        self.lblTiles.clear()
        
        #----------------------------------------------------------------------
        # Re-Konfiguracia gridu podla rows * cols
        #----------------------------------------------------------------------
        self.frame_map.grid_forget()
        
        for row in range(self.planet.rows):
            self.frame_map.rowconfigure(row, weight=1)
      
        for col in range(self.planet.cols):
            self.frame_map.columnconfigure(col, weight=1)
            
        #----------------------------------------------------------------------
        # Vytvorenie rows * cols tiles
        #----------------------------------------------------------------------
        for row in range(self.planet.rows):
            for col in range(self.planet.cols):
                
                # Zistim vlastnosti Tile na pozicii row, col
                tile    = self.planet.getTile(row, col)
                height  = tile.height
                bcColor = lib.getHeightColor(height)
            
                # Vytvorim label na zobrazenie Tile
                lblTile = ttk.Label(self.frame_map, relief=tk.RAISED, text=self.tileText(row, col, height), cursor='hand2')
                lblTile.configure(background=bcColor)
                lblTile.bind( '<Button-1>', self.tileLeftClick)
                lblTile.bind( '<Button-3>', self.tileRightClick)
                lblTile.grid(row=row, column=col, sticky='nwse')
                
                # Ulozim si vazbu {lblTile: Tile}
                self.lblTiles[lblTile] = tile
            
    #--------------------------------------------------------------------------
    def tileLeftClick(self, event):
        
        #----------------------------------------------------------------------
        # Zistim podla eventu, na ktoru lblTile som vlastne clickol
        #----------------------------------------------------------------------
        self.lblTileSelected = event.widget
        
        # Pre istotu si vypisem nazov tile, ktora je spojena s lblTile
        tile = self.lblTiles[self.lblTileSelected]
        self.setStatus(f'tileLeftClick: {self.lblTileSelected} => {tile.tileId} with height {tile.height}')
    
        # Zobraz vlastnosti Tile
        self.lbl_tile['text'] = f'I will work with {tile.tileId} with height {tile.height} m'
        
        

    #--------------------------------------------------------------------------
    def tileRightClick(self, event):
        
        #----------------------------------------------------------------------
        # Zistim podla eventu, na ktoru lblTile som vlastne clickol
        #----------------------------------------------------------------------
        self.lblTileSelected = event.widget
        
        # Pre istotu si vypisem nazov tile, ktora je spojena s lblTile
        tile = self.lblTiles[self.lblTileSelected]
        self.setStatus(f'tileRightClick: {self.lblTileSelected} => {tile.tileId} with height {tile.height}')
    
        #nakoniec otvor popup menu
        try    : self.tileMenu.tk_popup(event.x_root, event.y_root)
        finally: self.tileMenu.grab_release()

    #--------------------------------------------------------------------------
    def tileHeight(self, heightStr):
        
        height = int(heightStr)
        
        # Ziskam tile, ktora je spojena s touto lblTile
        tile   = self.lblTiles[self.lblTileSelected]
        row    = tile.row
        col    = tile.col
        
        self.setStatus(f'tileHeight: {height} for tileId = {tile.tileId}')
        
        # Nastavim vysku tile
        tile.height = height
        
       # Updatnem na obrazovke lblTile
        self.lblTileSelected.configure( background = lib.getHeightColor(height)      )
        self.lblTileSelected.configure( text       = self.tileText(row, col, height) )
        
    #--------------------------------------------------------------------------
    def tileTribes(self):
        
        pass
        
    #--------------------------------------------------------------------------
    def tileText(self, row, col, height):
        
        return f'{str(row).rjust(2)}x{str(col).rjust(2)}'
#        return f' {str(row).rjust(3)}x{str(col).rjust(3)}x{str(height).rjust(4)} '
        
    #==========================================================================
    # Utility
    #--------------------------------------------------------------------------
    def treeWhere(self, tree, event):
       
        row   = ''
        val   = ''
        col   = ''
        colid = ''
       
        iid = tree.identify_row(event.y)
      
        # presun focus a selection sem ak nie je vybraný iaden riadok
        if iid and len(tree.selection()) == 0:
            tree.focus(iid)
            tree.selection_set(iid)
         
        if tree.identify_region(event.x,event.y) == 'heading':
            hd    = tree.identify_column(event.x)
            colid = int(tree.identify_column(event.x)[1:]) - 1
            val   = tree.heading(hd, 'text')
           
        elif tree.identify_region(event.x,event.y) == 'cell':
            curItem = tree.focus()
            val   = tree.item(curItem, 'values')
            colid = int(tree.identify_column(event.x)[1:]) - 1
           
            row   = val
            val   = val[colid]
            hd    = tree.identify_column(event.x)
            col   = tree.heading(hd, 'text')
           
        return {'row':row, 'col':col, 'val':val, 'colNum':colid}
       
    #--------------------------------------------------------------------------
    def datToTab(self, dat, tree):
       
        #----------------------------------------------------------------------
        # Zadefinujem stlpce podla nazvov atributov v dat[0]
        #----------------------------------------------------------------------
        tree["columns"] = dat[0]
        
        #----------------------------------------------------------------------
        # Ziskam maximalne sirky stlpcov
        #----------------------------------------------------------------------
        maxW = [0 for col in dat[0]]
       
        for row in dat:
            
            i = 0
            for col in row:
                
                if (col is not None): w = len(str(col))
                else                : w = 0
               
                if w>maxW[i] and w<_WIDTH_MAX: maxW[i] = w
                i += 1
       
        #----------------------------------------------------------------------
        # Zadefinujem vlastnosti stlpcov
        #----------------------------------------------------------------------
        i = 0
        for col in tree["columns"]:
            
            tree.column(col, width=(8*maxW[i])+10, minwidth=30)
            i += 1
       
        #----------------------------------------------------------------------
        # Zadefinujem nazvy stlpcov
        #----------------------------------------------------------------------
        for h in dat[0]:
            tree.heading(h, text=h, anchor='w')
       
        #----------------------------------------------------------------------
        # Vlozim udaje do riadkov
        #----------------------------------------------------------------------
        for row in dat[1:]:
            tree.insert('', tk.END, values=row, tags=['TableCell'])
           
        tree['show'] = 'headings'
        tree.tag_configure('TableCell', font=font.nametofont('TkFixedFont'))
       
    #--------------------------------------------------------------------------
    def treeClear(self, tree):
       
        for i in tree.get_children():
            tree.delete(i)
           
    #--------------------------------------------------------------------------
    def treeExpand(self, tree, parent=''):
       
        tree.item(parent, open=True)
        for child in tree.get_children(parent):
            self.treeExpand(tree, child)
           
    #--------------------------------------------------------------------------
    def datToTree(self, dat, tree, rootId=None, maxId=0):
       
        if rootId is None: tree.tag_configure('TreeCell', font=font.nametofont('TkFixedFont'))
        localPos = 0
       
        #----------------------------------------------------------------------
        # Prejdem vsetky polozky dictionary
        #----------------------------------------------------------------------
        for key, val in dat.items():
           
            maxId += 1
 
            #------------------------------------------------------------------
            # Ak je item dictionary, potom rekurzia
            if type(val)==dict:
                
                tree.insert('', tk.END, text=f'[{key}]', iid=maxId, open=True, tags=['TreeCell'])
                if rootId is not None: tree.move(maxId, rootId, localPos)
               
                maxId  = self.datToTree(val, tree, maxId, maxId)
           
            #------------------------------------------------------------------
            # Ak je item list
            elif type(val)==list:
                
                tree.insert('', tk.END, text=f'[{key}]', iid=maxId, open=True, tags=['TreeCell'])
                listRoot = maxId
                if rootId is not None: tree.move(listRoot, rootId, localPos)
 
                # Vlozim list po riadkoch
                listPos = 0
                for row in val:
                   
                    maxId   += 1
                    tree.insert('', tk.END, text=f'{str(row)}', iid=maxId, open=True, tags=['TreeCell'])
                    tree.move(maxId, listRoot, listPos)
                    listPos += 1
           
            #------------------------------------------------------------------
            # Trivialna polozka
            else:
                key = str(key).ljust(12)
               
                # Vlozim do stromu
                tree.insert('', tk.END, text=f'{key}: {str(val)}', iid=maxId, open=True, tags=['TreeCell'])
               
                # Ak som v podstrome, presuniem pod rootId
                if rootId is not None: tree.move(maxId, rootId, localPos)
               
            #------------------------------------------------------------------
            # Zvysenie lokalnej pozicie
            localPos += 1
               
        return maxId
       
    #--------------------------------------------------------------------------

#------------------------------------------------------------------------------
print('Max Planet GUI ver 0.30')

#==============================================================================
#                              END OF FILE
#------------------------------------------------------------------------------
