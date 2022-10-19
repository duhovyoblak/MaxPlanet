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
_DENS_GROWTH     = 0.2   # Koeficient prirodzeneho prirastku populacie

_STRES_MIN       = 0.1   # Zakladna miera stresu populacie
_STRES_MAX       = 0.8   # Maximalna miera stresu populacie
_STRES_EMIG      = 0.2   # Koeficient emigracie kvoli stresu

_KNOW_GROWTH     = 1.10  # Koeficient zvysenia knowledge ak jej tribe venuje pozornost
_KNOW_LIMIT      = 0.33  # Hranica pozornosti, pri ktorej sa knowledge zvysuje
_KNOW_DECAY      = 0.95  # Koeficient zabudania knowledge ak jej tribe nevenuje pozornost

#==============================================================================
# TTile
#------------------------------------------------------------------------------
class TTile:

    #==========================================================================
    # Static variables & methods
    #--------------------------------------------------------------------------
    journal    = None        # Globalny journal
    tiles      = {}          # Zoznam vsetkych tiles  {tileId: tileObj}

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

        return round(denMax, 2)
    
    #--------------------------------------------------------------------------
    @staticmethod
    def getKnowMax(period):
        
        knowMax = 0
        
        # Prejdem vsetky tiles
        for tile in TTile.tiles.values():
        
            agrSum = 0
            indSum = 0
            warSum = 0
            
            # Prejdem vsetky tribe na tile pre konkretnu periodu
            for tribe in tile.history[period]['tribes'].values():
                agrSum += tribe['knowledge']['agr']
                indSum += tribe['knowledge']['ind']
                warSum += tribe['knowledge']['war']
                
            if agrSum > knowMax: knowMax = agrSum
            if indSum > knowMax: knowMax = indSum
            if warSum > knowMax: knowMax = warSum

        return round(knowMax, 3)
    
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
            
        for actPer in self.history:
            
            msg.append(f"Period = {actPer['period']}")
            
            for tribeId, tribeObj in actPer['tribes'].items():
                msg.append(f"{tribeId}: density={tribeObj['density']} resr={tribeObj['resrs']} denses={tribeObj['denses']}")
            
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
    def getPeriodDenStr(self, period):
        
        tribes = self.getPeriod(period)['tribes']
        
        toRet = 'Density:'
        for tribeId, tribeObj in tribes.items(): 
            if tribeObj['density']>0:
                toRet += f" {tribeId}:{round(tribeObj['density'], 2)}"
    
        if toRet=='Density:': toRet = 'No tribe here'
        
        return toRet
    
    #--------------------------------------------------------------------------
    def getPeriodKnwStr(self, period):
        
        tribes = self.getPeriod(period)['tribes']
        
        toRet = 'Knowledge:'
        for tribeId, tribeObj in tribes.items():
            if tribeObj['density']>0:
                toRet += f" {tribeId}: agr={round(tribeObj['knowledge']['agr'], 2)}, ind={round(tribeObj['knowledge']['ind'], 2)}, war={round(tribeObj['knowledge']['war'], 2)}"
 
        if toRet=='Knowledge:': toRet = 'No tribe here'
        
        return toRet
    
    #--------------------------------------------------------------------------
    def getPeriodPrfStr(self, period):
        
        tribes = self.getPeriod(period)['tribes']
        
        toRet = 'Preferences:'
        for tribeId, tribeObj in tribes.items(): 
            if tribeObj['density']>0:
                toRet += f" {tribeId}: agr={round(tribeObj['preference']['agr'], 2)}, ind={round(tribeObj['preference']['ind'], 2)}, war={round(tribeObj['preference']['war'], 2)}"
 
        if toRet=='Preferences:': toRet = 'No tribe here'
        
        return toRet
    
    #--------------------------------------------------------------------------
    def simPeriod(self, period):
        "Simulates respective period for this Tile based on previous period values"
        
        self.journal.I(f'{self.tileId}.simPeriod: period {period}')
        
        #----------------------------------------------------------------------
        # Vyberiem z historie predchadzajucu periodu a inicializujem simulovanu periodu
        #----------------------------------------------------------------------
        lastPeriod = self.getPeriod(period-1)
        simPeriod  = self.getPeriod(period  )
        
        #----------------------------------------------------------------------
        # Vyriesim zber resurces vratane trades podla stavu v lastPeriod
        #----------------------------------------------------------------------
        self.getResource(lastPeriod)
        
        #----------------------------------------------------------------------
        # Vyriesim ubytok/prirastok populacie na zaklade ziskanych resources a emigracie
        #----------------------------------------------------------------------
        self.evaluateDensity(lastPeriod, simPeriod)
 
        #----------------------------------------------------------------------
        # Vyriesim zmenu preferenci Tribe podla dovodu ubytku/prirastku populacie
        # Vyriesim zmenu zabudanie/zvysovanie Tribe knowledge
        #----------------------------------------------------------------------
        self.prefsAndKnowledge(lastPeriod, simPeriod)

        self.journal.O(f'{self.tileId}.simPeriod: done')

    #==========================================================================
    # Internal methods
    #--------------------------------------------------------------------------
    def getResource(self, lastPeriod):
        "Returns resources per Tribe based on preferences including trades and wars"

        self.journal.I(f'{self.tileId}.getResource:')
        
        # Vlastnosti Tile
        resrs = {}
        
        #----------------------------------------------------------------------
        # Zber AGR urody a IND vyrobkov jednotlivymi tribe
        #----------------------------------------------------------------------
        for tribeId, tribeObj in lastPeriod['tribes'].items():
            
            # Vlastnosti tribe
            dens = tribeObj['density'   ]
            pref = tribeObj['preference']
            know = tribeObj['knowledge' ]
            
            resrs[tribeId] = {'agr':0, 'ind':0, 'war':0}
            
            #------------------------------------------------------------------
            # Zber AGR resources - zlomok podla pomeru density Tribe voci celkovej densite na Tile
            resrs[tribeId]['agr'] = lib.getAgrRes( self.height, dens*pref['agr'], know['agr'] )
            resrs[tribeId]['agr'] = round( resrs[tribeId]['agr'], 3)

            #------------------------------------------------------------------
            # Zber IND resources - zlomok podla pomeru density Tribe voci celkovej densite na Tile
            resrs[tribeId]['ind'] = lib.getIndRes( self.height, dens*pref['ind'], know['ind'] )
            resrs[tribeId]['ind'] = round( resrs[tribeId]['ind'], 3)

        #----------------------------------------------------------------------
        # Nakupovanie zvysnych AGR za zvysne IND vyrobky a 
        # Lupenie WAR zdrojov od inych tribes
        #----------------------------------------------------------------------



        #----------------------------------------------------------------------
        # Zapisem priebezne vypocty o ziskanych resources do lastPeriod Tile
        #----------------------------------------------------------------------
        for tribeId, tribeObj in lastPeriod['tribes'].items():
            
                lastPeriod['tribes'][tribeId]['resrs'] = resrs [tribeId]
            
        #----------------------------------------------------------------------
        self.journal.O()

    #--------------------------------------------------------------------------
    def evaluateDensity(self, lastPeriod, simPeriod):
        "Evaluates population density per Tribe based on earned resources and emigration"

        self.journal.I(f'{self.tileId}.evaluateDensity:')
        period = lastPeriod['period']+1
        
        #----------------------------------------------------------------------
        # Vyhodnotim zmeny populacie pre vsetky Tribes na Tile
        #----------------------------------------------------------------------
        for tribeId, tribeObj in lastPeriod['tribes'].items():

            # Vstupne hodnoty
            resrTot = tribeObj['resrs']['agr'] + tribeObj['resrs']['ind'] + tribeObj['resrs']['war']
            
            # Zacinam simulaciu s povodnym obyvatelstvom z predchadzajucej periody
            densSim = tribeObj['density']

            #------------------------------------------------------------------
            # Opravim populaciu o prirodzeny prirastok
            #------------------------------------------------------------------
            densGrowth = _DENS_GROWTH * densSim
            densSim   += densGrowth

            #------------------------------------------------------------------
            # Ubytok populacie nasledkom nedostatku zdrojov 1 res per 1 clovek/km2
            #------------------------------------------------------------------
            if densSim > resrTot: 
                
                # Zistim, kolko populcie zomrie lebo nema zdroje
                densDeath = densSim - resrTot
                
                # Miera stresu je pomer zomretej populacie voci povodnej populacii
                strsTot = _STRES_MIN + (densDeath / densSim)
                if strsTot > _STRES_MAX: strsTot = _STRES_MAX
                
                # Zostane zit len tolko ludi kolko ma zdroje
                densSim   = resrTot
                
            else:
                strsTot   = _STRES_MIN
                densDeath = 0
                
            #------------------------------------------------------------------
            # Emigracia do vsetkych susednych Tiles
            #------------------------------------------------------------------
            densEmig = 0
            for neighTile in self.neighs:
                
                #--------------------------------------------------------------
                # Ak susedna Tile nie je more
                #--------------------------------------------------------------
                if neighTile.height > 0:
                
                    #----------------------------------------------------------
                    #Hustota tohto Tribeu u susedov v last period
                    #----------------------------------------------------------
                    densNeigh = neighTile.getPeriodDens(period-1, tribeId)
                
                    #----------------------------------------------------------
                    # Ak je u nas vacsia densita naseho Tribe ako u susedov
                    #----------------------------------------------------------
                    if densSim > densNeigh: 
                    
                        #------------------------------------------------------
                        # Emigracia do susedneho tribe
                        #------------------------------------------------------
                        emig      = _STRES_EMIG * strsTot * (densSim-densNeigh)
                        densEmig += emig
                    
                        #------------------------------------------------------
                        # Pridam emigrovanych do susednej Tile v sim period
                        #------------------------------------------------------
                        neighTile.addPeriodDens(period, tribeId, emig)
                    
            #------------------------------------------------------------------
            # Ubytok populacie nasledkom celkove emigracie
            #------------------------------------------------------------------
            densSim -= densEmig

            #------------------------------------------------------------------
            # Zapisem priebezne vypocty do lastPeriod
            #------------------------------------------------------------------
            tribeObj['denses'] = {'densSim'   :round(densSim   , 2),
                                  'densGrowth':round(densGrowth, 2),
                                  'densDeath' :round(densDeath , 2),
                                  'stres'     :round(strsTot   , 2),
                                  'densEmig'  :round(densEmig  , 2) }
        
            #------------------------------------------------------------------
            # Ak tribe prezil, zapisem ho do simulovanej periody s densSim
            #------------------------------------------------------------------
            if densSim > 0:
                self.addPeriodDens(period, tribeId, round(densSim, 2))
                
            #------------------------------------------------------------------
        self.journal.O()

    #--------------------------------------------------------------------------
    def prefsAndKnowledge(self, lastPeriod, simPeriod):
        "Evaluates changes in preferences and knowledge"

        self.journal.I(f'{self.tileId}.prefsAndKnowledge:')
        period = lastPeriod['period']+1
        
        #----------------------------------------------------------------------
        # Vyhodnotim zmeny pre vsetky Tribes na Tile
        #----------------------------------------------------------------------
        for tribeId, tribeObj in lastPeriod['tribes'].items():

            #------------------------------------------------------------------
            # Zmena knowledge podla miery preferencii = pozornosti, ktory tribe venoval oblasti
            #------------------------------------------------------------------
            know = self.knowledgeChange(tribeObj, 'agr')
            self.setPeriodKnowledge(period, tribeId, 'agr', know)
            
            know = self.knowledgeChange(tribeObj, 'ind')
            self.setPeriodKnowledge(period, tribeId, 'ind', know)
            
            know = self.knowledgeChange(tribeObj, 'war')
            self.setPeriodKnowledge(period, tribeId, 'war', know)

            #------------------------------------------------------------------
            # Zmena preferences podla miery 
            #------------------------------------------------------------------

            
        self.journal.O()

    #--------------------------------------------------------------------------
    #--------------------------------------------------------------------------
    #==========================================================================
    # Tile tools
    #--------------------------------------------------------------------------
    def getPeriod(self, period):
        "Returns period if exists, creates empty id does not exists"
        
        # Ak je to prave nasledujuca perioda v historii, vytvorim ju
        if period == len(self.history): 
            self.history.append({ 'period':period, 'tribes':{} })

        return self.history[period]
        
    #--------------------------------------------------------------------------
    def getPeriodTribe(self, period, tribeId):
        "Returns tribe for respective period"
        
        actPeriod = self.getPeriod(period)
        
        #----------------------------------------------------------------------
        # Ak tribe neexistuje, doplnim ho podla KOPIE predchadzajucej periody alebo z library
        #----------------------------------------------------------------------
        if tribeId not in actPeriod['tribes'].keys(): 
            
            lastPeriod = self.getPeriod(period)
            
            #------------------------------------------------------------------
            # Ak v predchadzajucej periode zelany tribe Id nebol, vlozim ho z library
            #------------------------------------------------------------------
            if tribeId not in lastPeriod['tribes']:
                actPeriod['tribes'][tribeId] = dict(lib.tribes[tribeId])
            else:
                actPeriod['tribes'][tribeId] = dict(lastPeriod['tribes'][tribeId])

            #------------------------------------------------------------------
            # Vynulujem simulovanu periodu
            #------------------------------------------------------------------
            actPeriod['tribes'][tribeId]['density'] = 0
            actPeriod['tribes'][tribeId]['resrs'  ] = {}
            actPeriod['tribes'][tribeId]['denses' ] = {}

        #----------------------------------------------------------------------
        return actPeriod['tribes'][tribeId]
        
    #--------------------------------------------------------------------------
    def getPeriodDensTot(self, period):
        "Returns total density for respective period"
        
        toRet = 0
        
        actPeriod = self.getPeriod(period)
        
        for tribeObj in actPeriod['tribes'].values():
            toRet += tribeObj['density']
        
        return toRet
        
    #--------------------------------------------------------------------------
    def getPeriodDens(self, period, tribeId):
        "Returns density of tribeId for respective period"
        
        periodTribe = self.getPeriodTribe(period, tribeId)
        return periodTribe['density']
        
    #--------------------------------------------------------------------------
    def setPeriodDens(self, period, tribeId, dens):
        
        periodTribe = self.getPeriodTribe(period, tribeId)
        periodTribe['density'] = dens
        
    #--------------------------------------------------------------------------
    def addPeriodDens(self, period, tribeId, dens):
        
        periodTribe = self.getPeriodTribe(period, tribeId)
        periodTribe['density'] += round(dens, 3)
        
    #--------------------------------------------------------------------------
    def setPeriodKnowledge(self, period, tribeId, resType, know):
        
        actPeriod = self.getPeriod(period)

        if tribeId in actPeriod['tribes'].keys():
            actPeriod['tribes'][tribeId]['knowledge'][resType] = know

    #--------------------------------------------------------------------------
    def knowledgeChange(self, tribeObj, resType):
        
        toRet = 0
        attention = tribeObj['preference'][resType]
            
        if attention > _KNOW_LIMIT: toRet = tribeObj['knowledge'][resType] * _KNOW_GROWTH
        else                      : toRet = tribeObj['knowledge'][resType] * _KNOW_DECAY
            
        # Znalosti nemouzu byt vyssie ako 1 (=100%)
        if toRet > 1: toRet = 1
        
        return round(toRet,3)

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