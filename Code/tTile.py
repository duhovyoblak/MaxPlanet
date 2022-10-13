#==============================================================================
# Siqo class TTile
#------------------------------------------------------------------------------
import planet_lib    as lib

#==============================================================================
# package's constants
#------------------------------------------------------------------------------
_SEP   = 50*''

#==============================================================================
# package's variables
#------------------------------------------------------------------------------
_C_DENS_GROWTH   = 0.5  # Koeficient prirastku populacie pri nadbytku resources
_STRES_MIN       = 0.1  # Zakladna miera stresu populacie

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
        self.history    = [{'period':0, 'densTot':0, 'tribes':{}}] # Historia tile
        
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
        self.history.append( {'period':0, 'densTot':0, 'tribes':{}} )
        
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
        for tribeId, tribeObj in tribes.items(): toRet += f" {tribeId}:{tribeObj['density']}"
        if toRet=='Density: ': toRet = 'No tribe here'
        
        return toRet
    
    #--------------------------------------------------------------------------
    def setTribe(self, period, tribeId, tribeObj):
        
        self.journal.I(f'{self.tileId}.setTribe: period {period} tribe {tribeId} ')
        
        print(tribeObj)
        
        #----------------------------------------------------------------------
        # Ziskam data z historie
        actPeriod = self.history[period]
        
        #----------------------------------------------------------------------
        # Upravim data podla poziadavky
        actPeriod['tribes'][tribeId] = tribeObj
        
        #----------------------------------------------------------------------
        # Updatnem densTot
        densTot = 0
        for tribeObj in tribes.values(): densTot += tribeObj['density']
        actPeriod['densTot'] = densTot
        
        #----------------------------------------------------------------------
        # Zapisem data do historie
        self.history[period] = actPeriod
        
        self.journal.O()
        
    #--------------------------------------------------------------------------
    def simPeriod(self, period):
        
        self.journal.I(f'{self.tileId}.simPeriod: period {period}')
        
        #----------------------------------------------------------------------
        # Vyberiem z historie predchadzajucu periodu a inicializujem simulovanu periodu
        #----------------------------------------------------------------------
        lastPeriod = self.history[period-1]
        simPeriod  = {'period':period}
        
        #----------------------------------------------------------------------
        # Vyriesim zber resurces vratane trades podla stavu v lastPeriod
        #----------------------------------------------------------------------
        resrs = self.getResource(lastPeriod)
 
        #----------------------------------------------------------------------
        # Vyriesim ubytok/prirastok populacie na zaklade ziskanych resources a emigracie
        #----------------------------------------------------------------------
        denses = self.evaluateDensity(lastPeriod, resrs)
 
        #----------------------------------------------------------------------
        # Vyriesim zmenu preferenci Tribe podla dovodu ubytku/prirastku populacie
        # Vyriesim zmenu zabudanie/zvysovanie Tribe knowledge
        #----------------------------------------------------------------------
        tribes = lastPeriod['tribes']

        #----------------------------------------------------------------------
        # Vyriesim vznik noveho tribe zo vsetkych tribe na Tile
        #----------------------------------------------------------------------

        #----------------------------------------------------------------------
        # Zapisem tribes ktore prezili do simulovanej Tile
        #----------------------------------------------------------------------
        for tribeId, dens in denses.items():
            
            if dens > 0:
                simPeriod['tribes'][tribeId]            = tribes[tribeId]
                simPeriod['tribes'][tribeId]['density'] = dens
                simPeriod['resrs' ][tribeId]            = resrs [tribeId]
                
        #----------------------------------------------------------------------
        # Zapisem vysledky simulacie do historie
        #----------------------------------------------------------------------
        if period < len(self.history): self.history[period] = simPeriod
        else                         : self.history.append(simPeriod)

        self.journal.O(f'{self.tileId}.simPeriod: done')

    #==========================================================================
    # Internal methods
    #--------------------------------------------------------------------------
    def getResource(self, lastPeriod):
        "Returns resources per Tribe based on preferences including trades and wars"

        self.journal.I(f'{self.tileId}.getResource:')
        
        # Vlastnosti Tile
        agrSource = lib.getHeightAgrSource(self.height)  # Vlastnosti biomu - urodnost AGR
        indSource = lib.getHeightIndSource(self.height)  # Vlastnosti biomu - nerasty pre IND
        densTot   = lastPeriod['densTot']                # Celkova densita vsetkych Tribes na Tile
        resrs = {}
        
        #----------------------------------------------------------------------
        # Zber AGR urody a IND vyrobkov jednotlivymi tribe
        #----------------------------------------------------------------------
        for tribeId, tribeObj in lastPeriod['tribes'].items():
            
            # Vlastnosti tribe
            dens = tribeObj['density'   ]
            pref = tribeObj['preference']
            know = tribeObj['knowledge' ]
            
            resrs[tribeId] = {}
            
            #------------------------------------------------------------------
            # Zber AGR resources - zlomok podla pomeru density Tribe voci celkovej densite na Tile
            resrs[tribeId]['agr'] = dens * pref['agr'] * know['agr'] * agrSource *(dens/densTot)

            #------------------------------------------------------------------
            # Zber IND resources - zlomok podla pomeru density Tribe voci celkovej densite na Tile
            resrs[tribeId]['ind'] = dens * pref['ind'] * know['ind'] * indSource *(dens/densTot)

        #----------------------------------------------------------------------
        # Nakupovanie zvysnych AGR za zvysne IND vyrobky a 
        # Lupenie WAR zdrojov od inych tribes
        #----------------------------------------------------------------------



        self.journal.O()
        return resrs

    #--------------------------------------------------------------------------
    #--------------------------------------------------------------------------
    def evaluateDensity(self, lastPeriod, resrs):
        "Returns changes in populations density per Tribe based on earned resources and emigration"

        self.journal.I(f'{self.tileId}.evaluateDensity:')
        
        denses = {}
        
        for tribeId, tribeObj in lastPeriod['tribes'].items():

            # Vstupne hodnoty
            res   = resrs[tribeId]['agr'] + resrs[tribeId]['ind'] + resrs[tribeId]['war']
            dens  = tribeObj['density']

            #------------------------------------------------------------------
            # Ubytok populacie nasledkom nedostatku zdrojov 1 res per 1 clovek/km2
            #------------------------------------------------------------------
            if dens > res: 
                
                # Velkost populacie ktorej chybaju zdroje a zomrie
                death = dens-res
                
                # Miera stresu je pomer zomretej populacie voci povodnej populacii
                stres = death/dens
                
                # Zostane zit len tolko ludi kolko ma zdroje
                dens = res
                
            #------------------------------------------------------------------
            # Prirastok populacie nasledkom nadbytkku zdrojov
            #------------------------------------------------------------------
            else: 
                
                dens  = dens + _C_DENS_GROWTH * (res-dens)   # Blahobyt
                stres = _STRES_MIN  # Zakladna miera stresu
            
            #------------------------------------------------------------------
            # Emigracia do susednych Tiles
            #------------------------------------------------------------------
            
            # Urcim, aka cast populacie sa rozhodla odist podla miery stresu
            
            for neigh in self.neighs:
                
                #Hustota Tribeu u susedov
                neighDens = neigh.history[lastPeriod['period']]['tribes'][tribeId]['density']
                
                # Ak je u nas vacsia densita naseho Tribe ako u susedov
                if dens > neighDens:
                    
                    #


            #------------------------------------------------------------------
            # Zapis vysledku pre tribe
            #------------------------------------------------------------------
            denses[tribeId] = dens
        
        self.journal.O()
        return denses

    #--------------------------------------------------------------------------
    #--------------------------------------------------------------------------
    #--------------------------------------------------------------------------
    #--------------------------------------------------------------------------
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
        
        if 'history' in data.keys() and len(data['history'])>0: 
            self.history = data['history']
        
        self.journal.O(f'{self.tileId}.fromJson: done')
        
#------------------------------------------------------------------------------
print('TTile ver 0.01')

#==============================================================================
#                              END OF FILE
#------------------------------------------------------------------------------