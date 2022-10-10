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

    #--------------------------------------------------------------------------
    @staticmethod
    def getDenMax(period):
        
        denMax = 0
        
        # Prejdem vsetky tiles
        for tile in TTile.tiles.values():
        
            tileSum = 0
            
            # Prejdem vsetky tribe na tile pre konkretnu periodu
            for tribe in tile.history[period]['tribes'].values():
                tileSum += tribe['density']
                
            if tileSum > denMax: denMax = tileSum

        return denMax
    
    #==========================================================================
    # Constructor & utilities
    #--------------------------------------------------------------------------
    def __init__(self, tileId, height=0):
        "Calls constructor of TTile and initialise it with empty data"

        self.journal.I('TTile.constructor')
        
        self.tileId     = tileId          # ID tile
        self.row        = 0               # Pozicia tile - riadok
        self.col        = 0               # Pozicia tile - stlpec
        self.neighs     = []              # Zoznam geografickych susedov tile [tileObj]

        self.height     = height          # Priemerna vyska tile nad morom
        self.history    = [{'tribes':{}, 'agrState':{}}] # Historia tile
        
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
    def clear(self):
        "Clear state of Tile"
    
        self.journal.I(f'{self.tileId}.clear:')
        
        self.history.clear()
        self.history.append( {'tribes':{}, 'agrState':{}} )
        
        self.journal.O(f'{self.tileId}.clear: done')
        
    #--------------------------------------------------------------------------
    def reset(self):
        "Resets state of Tile into begining state"
    
        self.journal.I(f'{self.tileId}.reset:')
        
        # Vratim historiu ju do zakladneho stavu
        begState = self.history[0]
        self.history.clear()
        self.history.append(begState)
        
        self.journal.O(f'{self.tileId}.reset: done')
        
    #--------------------------------------------------------------------------
    def getDenStr(self, period):
        
        tribes = self.history[period]['tribes']
        
        toRet = 'Density:'
        for tribeId, tribeObj in tribes.items():
            
            toRet += f" {tribeId}:{tribeObj['density']}"
        
        if toRet=='Density: ': toRet = 'No tribe here'
        return toRet
    
    #--------------------------------------------------------------------------
    def setTribe(self, period, tribeId, tribeObj):
        
        self.journal.I(f'{self.tileId}.setTribe: period {period} tribe {tribeId} ')
        
        print(tribeObj)
        
        # Ziskam data z historie
        dat = self.history[period]
        
        # Upravim data podla poziadavky
        dat['tribes'  ][tribeId] = tribeObj
        dat['agrState']          = self.aggregate(period)
        
        # Zapisem data do historie
        self.history[period] = dat
        
        self.journal.O()
        
    #==========================================================================
    # Internal methods
    #--------------------------------------------------------------------------
    def aggregate(self, period):
        "Returns tile aggregates for respective period"
        
        return {}
        
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
        
        if 'history' in data.keys() and len(data['history'])>0: 
            self.history = data['history']
        
        self.journal.O(f'{self.tileId}.fromJson: done')
        
#------------------------------------------------------------------------------
print('TTile ver 0.01')

#==============================================================================
#                              END OF FILE
#------------------------------------------------------------------------------