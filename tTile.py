#==============================================================================
# Siqo class TTile
#------------------------------------------------------------------------------
# from   dwm_calendar         import DWM_Calendar

#==============================================================================
# package's constants
#------------------------------------------------------------------------------
_SEP   = 50*''

#==============================================================================
# package's variables
#------------------------------------------------------------------------------

#==============================================================================
# TTile
#------------------------------------------------------------------------------
class TTile:

    #==========================================================================
    # Static variables & methods
    #--------------------------------------------------------------------------
    journal = None   # Globalny journal
    tiles   = {}     # Zoznam vsetkych tiles  {tileId: tileObj}

    #==========================================================================
    # Constructor & utilities
    #--------------------------------------------------------------------------
    def __init__(self, tileId, height=0):
        "Calls constructor of TTile and initialise it with empty data"

        self.journal.I('TTile.constructor')
        
        self.tileId     = tileId      # ID tile
        self.height     = height      # Priemerna vyska tile nad morom
        self.row        = 0           # Pozicia tile - riadok
        self.col        = 0           # Pozicia tile - stlpec
        self.neighs     = []          # Zoznam geografickych susedov tile [tileObj]
        self.history    = []          # Historia tile [{'agrState':agrState, 'tribes':tribes}]
        
        # Zaradim novu tile do zoznamu tiles
        self.tiles[self.tileId] = self

        self.journal.O(f'{self.tileId}.constructor: done')
        
    #--------------------------------------------------------------------------
    def __str__(self):
        "Prints info about this Tile"

        toRet = ''
        for line in self.info()['out']: toRet += line +'\n'

        return toRet

    #==========================================================================
    # Reports for users
    #--------------------------------------------------------------------------
    def info(self):
        "Returns info about the Tile"

        msg = []
        msg.append(f'Tile ID   :{self.tileId}'   )
        msg.append(f'height    :{self.height}'   )
        msg.append(f'row       :{self.row}'   )
        msg.append(f'col       :{self.col}'   )
        msg.append(_SEP)
        msg.append('Neighbours:')

        for neighObj in self.neighs:
            msg.append(f'{neighObj.tileId}    :{neighObj.height}'   )
            
        return {'res':'OK', 'msg':msg}

    #==========================================================================
    # API for GUI
    #--------------------------------------------------------------------------
    def reset(self):
        "Resets state of Tile into begining state"
    
        self.journal.I(f'{self.tileId}.reset:')
        
        # Ak existuje nejaka historia, zrusim ju do zakladneho stavu
        if len(self.history) > 0:
            begState = self.history[0]
            self.history.clear()
            self.history.append(begState)
        
        self.journal.O(f'{self.tileId}.reset: done')
        
    #--------------------------------------------------------------------------
    
    #==========================================================================
    # Internal methods
    #--------------------------------------------------------------------------
        
    #==========================================================================
    # Persistency methods
    #--------------------------------------------------------------------------
    def toJson(self):
        "Creates json representation of this tile"

        self.journal.I(f'{self.tileId}.toJson:')
        
        data = {}
        
        data['tileId' ] = self.tileId   # ID tile
        data['height' ] = self.height   # Priemerna vyska tile nad morom
        data['row'    ] = self.row      # Pozicia tile - riadok
        data['col'    ] = self.col      # Pozicia tile - stlpec
        data['history'] = self.history  # Historia tile [{'agrState':agrState, 'tribes':tribes}]
        
        self.journal.O(f'{self.tileId}.toJson: done')
        
        return data
        
    #--------------------------------------------------------------------------
    def fromJson(self, data):
        "Updates tile from json structure"

        self.journal.I(f'{self.tileId}.fromJson:')
        
        self.height  = data['height' ]
        self.history = data['history']
        
        self.journal.O(f'{self.tileId}.fromJson: done')
        
#------------------------------------------------------------------------------
print('TTile ver 0.01')

#==============================================================================
#                              END OF FILE
#------------------------------------------------------------------------------