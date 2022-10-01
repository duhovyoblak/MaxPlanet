#==============================================================================
# Siqo class TPlanet
#------------------------------------------------------------------------------
import siqo_general  as     gen
from   tTile         import TTile

#==============================================================================
# package's constants
#------------------------------------------------------------------------------

#==============================================================================
# package's variables
#------------------------------------------------------------------------------

#==============================================================================
# TPlanet
#------------------------------------------------------------------------------
class TPlanet:

    #==========================================================================
    # Static variables & methods
    #--------------------------------------------------------------------------

    #==========================================================================
    # Constructor & utilities
    #--------------------------------------------------------------------------
    def __init__(self, journal, name):
        "Calls constructor of TPlanet and initialise it with empty data"

        journal.I('TPlanet.constructor')
        
        # Nastavenie journal-u projektu
        self.journal    = journal     # Odkaz na globalny journal
        TTile.journal   = journal
        
        
        # Nastavenie vlastnosti planety
        self.name       = name               # Nazov planety
        self.fName      = 'TestPlanet.json'  # Nazov suboru pre perzistenciu planetu
        self.rows       = 0                  # Pocet riadkov rastra planety
        self.cols       = 0                  # Pocet stlpcov rastra planety
        self.period     = 0                  # Maximalna perioda dosiahnuta v simulacii

        # Prepojim evidenciu Tiles
        self.tiles      = TTile.tiles # Geografia planety  {tileId: tileObj}

        self.journal.O(f'{self.name}.constructor: done')
        
    #--------------------------------------------------------------------------
    def __str__(self):
        "Prints info about this Planet"

        toRet = ''
        for line in self.info()['msg']: toRet += line +'\n'

        return toRet

    #==========================================================================
    # Reports for users
    #--------------------------------------------------------------------------
    def info(self):
        "Returns info about the Planet"

        msg = []
        msg.append(f'Planet name :{self.name}'       )
        msg.append(f'File name   :{self.fName}'      )
        msg.append(f'rows        :{self.rows}'       )
        msg.append(f'cols        :{self.cols}'       )
        msg.append(f'tiles       :{len(self.tiles)}' )
        msg.append(f'period      :{self.period}'     )

        return {'res':'OK', 'msg':msg}

    #==========================================================================
    # API for GUI
    #--------------------------------------------------------------------------
    def clear(self):
        "Clears all Planet's data"
    
        self.journal.I(f'{self.name}.clear:')
        
        self.period = 0
        self.rows   = 0
        self.cols   = 0
        
        self.tiles.clear()
        
        self.journal.O(f'{self.name}.clear: done')
        
    #--------------------------------------------------------------------------
    def reset(self):
        "Resets state of Planet into begining state"
    
        self.journal.I(f'{self.name}.reset:')
        
        self.period = 0
        for tile in self.tiles.values(): tile.reset()
        
        self.journal.O(f'{self.name}.reset: done')
        
    #--------------------------------------------------------------------------
    def generate(self, rows, cols):
        "Creates new void Planet"
    
        self.journal.I(f'{self.name}.generate: New planet {rows} * {cols}')
        
        #----------------------------------------------------------------------
        # Zrusim existujucu planetu
        #----------------------------------------------------------------------
        self.clear()
        
        #----------------------------------------------------------------------
        # Najprv vytvorim vsetky tiles        
        #----------------------------------------------------------------------
        self.rows = rows
        self.cols = cols
        
        for r in range(self.rows):
            for c in range(self.cols):
                tileObj     = TTile( self.getTileId(r, c) )
                tileObj.row = r
                tileObj.col = c

        #----------------------------------------------------------------------
        # Potom nastavim vsetkym tiles ich susedov
        #----------------------------------------------------------------------
        for tileId, tileObj in self.tiles.items():
                
                neighs = self.getNeighbours(tileId)
                tileObj.neighs = neighs
        
        self.journal.O(f'{self.name}.generate: done')
    
    #==========================================================================
    # Internal methods
    #--------------------------------------------------------------------------
    def getTile(self, row, col):
        "Returns Tile for respective row, col"
        
        tileId = self.getTileId(row, col)
        
        if tileId in self.tiles.keys(): return self.tiles[tileId]
        else:
            self.journal.M(f'{self.name}.getTile: Tile ID {tileId} does not exists')
            return None
        
    #--------------------------------------------------------------------------
    def getTileId(self, row, col):
        "Returns tileID for respective row, col"
        
        return f'Tile {row}, {col}'
        
    #--------------------------------------------------------------------------
    def getNeighbours(self, tileId):
        "Returns neighbours [tileObj] for tile with respective ID"
        
        toRet = []
        
        #----------------------------------------------------------------------
        # Ziskam poziciu row, col pre tileID
        #----------------------------------------------------------------------
        tile = self.tiles[tileId]
        row = tile.row
        col = tile.col
        
        #----------------------------------------------------------------------
        # Urcim susedov
        #----------------------------------------------------------------------
        for dr in range(-1,2):
            for dc in range(-1,2):
                
                neighId = self.getTileId( (row+dr)%self.rows, (col+dc)%self.cols )  
                
                # Ak to nie je ID mna, potom je to sused a vlozim ho do zoznamu susedov
                if neighId != tileId: toRet.append(self.tiles[neighId])
                
        return toRet
        
    #==========================================================================
    # Persistency methods
    #--------------------------------------------------------------------------
    def save(self):
        "Saves planet into disk file"

        self.journal.I(f'{self.name}.save:')
        
        #----------------------------------------------------------------------
        # Vyrobim json na ulozenie
        #----------------------------------------------------------------------
        data = {}
        
        data['rows'  ]  = self.rows
        data['cols'  ]  = self.cols
        data['period']  = self.period
        
        data['tiles']   = {}
        
        for tileId, tileObj in self.tiles.items():
            data[tileId] = tileObj.toJson()
        
        #----------------------------------------------------------------------
        # Zapisem json na disk
        #----------------------------------------------------------------------
        gen.dumpJson(self.journal, self.fName, data)
        
        self.journal.O(f'{self.name}.save: done')
        
    #--------------------------------------------------------------------------
    def load(self):
        "Loads planet from disk file"

        self.journal.I(f'{self.name}.load:')
        
        #----------------------------------------------------------------------
        # Nacitam json z disku
        #----------------------------------------------------------------------
        data = gen.loadJson(self.journal, self.fName)
        
        #----------------------------------------------------------------------
        # Vygenerujem cistu planetu rows*cols
        #----------------------------------------------------------------------
        self.generate(data['rows'], data['cols'])
        
        #----------------------------------------------------------------------
        # Updatnem parametre tiles podla data
        #----------------------------------------------------------------------
        self.period = data['period']
        
        for tileId, tileObj in self.tiles.items():
            tileObj.fromJson( data[tileId] )
        
        self.journal.O(f'{self.name}.load: done')
        
        
#------------------------------------------------------------------------------
print('TPlanet ver 0.01')

#==============================================================================
#                              END OF FILE
#------------------------------------------------------------------------------