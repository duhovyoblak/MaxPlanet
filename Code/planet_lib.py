#==============================================================================
# Planet Max: Utility library file
#------------------------------------------------------------------------------

#==============================================================================
# Constans
#------------------------------------------------------------------------------
heights = { 
       0: {'color':'#4faed0', 'agrWork':  0, 'agrSource':    0, 'indWork':  0, 'indSource':    0},
       
     100: {'color':'#66ff33', 'agrWork':180, 'agrSource': 1800, 'indWork':200, 'indSource':  400},
     200: {'color':'#5ceb2e', 'agrWork':200, 'agrSource': 2000, 'indWork':230, 'indSource':  450},
     300: {'color':'#52d629', 'agrWork':190, 'agrSource': 1700, 'indWork':270, 'indSource':  500},
     400: {'color':'#47c224', 'agrWork':180, 'agrSource': 1400, 'indWork':300, 'indSource':  600},
     500: {'color':'#38a31c', 'agrWork':170, 'agrSource': 1200, 'indWork':350, 'indSource':  800},
     600: {'color':'#298514', 'agrWork':160, 'agrSource': 1000, 'indWork':400, 'indSource': 1200},
     700: {'color':'#1a660d', 'agrWork':150, 'agrSource':  900, 'indWork':450, 'indSource': 1600},
     800: {'color':'#0a4705', 'agrWork':150, 'agrSource':  800, 'indWork':500, 'indSource': 2000},
     900: {'color':'#003300', 'agrWork':150, 'agrSource':  750, 'indWork':600, 'indSource': 2100},
     
    1000: {'color':'#333300', 'agrWork':150, 'agrSource':  700, 'indWork':600, 'indSource': 1900},
    1100: {'color':'#423300', 'agrWork':160, 'agrSource':  650, 'indWork':570, 'indSource': 1800},
    1200: {'color':'#523300', 'agrWork':160, 'agrSource':  600, 'indWork':530, 'indSource': 1700},
    1300: {'color':'#613300', 'agrWork':160, 'agrSource':  550, 'indWork':500, 'indSource': 1600},
    1400: {'color':'#803300', 'agrWork':160, 'agrSource':  500, 'indWork':470, 'indSource': 1400},
    1500: {'color':'#8f3300', 'agrWork':170, 'agrSource':  450, 'indWork':430, 'indSource': 1100},
    1600: {'color':'#9e3300', 'agrWork':170, 'agrSource':  400, 'indWork':400, 'indSource':  900},
    1700: {'color':'#ad3300', 'agrWork':170, 'agrSource':  370, 'indWork':380, 'indSource':  800},
    1800: {'color':'#bd3300', 'agrWork':150, 'agrSource':  330, 'indWork':360, 'indSource':  700},
    1900: {'color':'#cc3300', 'agrWork':140, 'agrSource':  300, 'indWork':330, 'indSource':  600},
    
    2000: {'color':'#d1470f', 'agrWork':130, 'agrSource':  250, 'indWork':300, 'indSource':  500},
    2100: {'color':'#d6591d', 'agrWork':100, 'agrSource':  200, 'indWork':280, 'indSource':  450},
    2200: {'color':'#da6c2b', 'agrWork': 50, 'agrSource':  150, 'indWork':260, 'indSource':  400},
    2300: {'color':'#df7e38', 'agrWork': 20, 'agrSource':  100, 'indWork':240, 'indSource':  370},
    2400: {'color':'#e8a354', 'agrWork': 20, 'agrSource':   50, 'indWork':220, 'indSource':  330},
    2500: {'color':'#edb562', 'agrWork':  0, 'agrSource':    0, 'indWork':200, 'indSource':  300},
    2600: {'color':'#f1c870', 'agrWork':  0, 'agrSource':    0, 'indWork':170, 'indSource':  250},
    2700: {'color':'#f6da7d', 'agrWork':  0, 'agrSource':    0, 'indWork':140, 'indSource':  200},
    2800: {'color':'#faed8b', 'agrWork':  0, 'agrSource':    0, 'indWork':120, 'indSource':  150},
    2900: {'color':'#ffff99', 'agrWork':  0, 'agrSource':    0, 'indWork':100, 'indSource':  100},
    
    3000: {'color':'#ffffff', 'agrWork':  0, 'agrSource':    0, 'indWork':  0, 'indSource':    0}
}

#------------------------------------------------------------------------------
tribes = { 
       'Green Men'  : {'density'   : 0,
                       'color'     : {'red':0,   'green':1,   'blue':0   }, 
                       'preference': {'agr':1.0, 'ind'  :0.0, 'war' :0.0 },
                       'knowledge' : {'agr':0.1, 'ind'  :0.1, 'war' :0.1 },
                       'resrs'     : {},
                       'denses'    : {}
                      },
       
       'Blue Indy'  : {'density'   : 0,
                       'color'     : {'red':0,   'green':0,   'blue':1   }, 
                       'preference': {'agr':0.0, 'ind'  :1.0, 'war' :0.0 },
                       'knowledge' : {'agr':0.1, 'ind'  :0.1, 'war' :0.1 },
                       'resrs'     : {},
                       'denses'    : {}
                      },
       
       'Red Wariors': {'density'   : 0,
                       'color'     : {'red':1,   'green':0,   'blue':0   }, 
                       'preference': {'agr':0.0, 'ind'  :0.0, 'war' :1.0 },
                       'knowledge' : {'agr':0.1, 'ind'  :0.1, 'war' :0.1 },
                       'resrs'     : {},
                       'denses'    : {}
                      }
}

#==============================================================================
# Resource harvesting Functions
#------------------------------------------------------------------------------
def getAgrRes(height, dens, knowledge):
    "Returns agr resource for respective height and workforce density and knowledge"
    
    # Je mozne vyuzit maximalne stanovenu pracovnu silu, zvysna sa uz neda pouzit
    if dens > heights[height]['agrWork']: dens = heights[height]['agrWork']
    
    return heights[height]['agrSource'] * (dens / heights[height]['agrWork']) * knowledge

#------------------------------------------------------------------------------
def getIndRes(height, dens, knowledge):
    "Returns ind resource for respective height and workforce density and knowledge"
    
    # Je mozne vyuzit maximalne stanovenu pracovnu silu, zvysna sa uz neda pouzit
    if dens > heights[height]['indWork']: dens = heights[height]['indWork']
    
    return heights[height]['indSource'] * (dens / heights[height]['indWork']) * knowledge

#==============================================================================
# Color Functions
#------------------------------------------------------------------------------
def getHeightColor(height):
    
    for h, rec in heights.items():
        if h >= height: return rec['color']
        
    # Ak nemam definovanu vysku
    return '#000000'

#------------------------------------------------------------------------------
def getPopulColor(tribes, denMax):
    
    # Ziskam mix color z populacii vsetkych Tribes
    mix = [0, 0, 0]
    
    for tribe in tribes.values():
        
        tribePopul = tribe['density']
    
        mix[0] += (tribe['color']['red'  ] * tribePopul)
        mix[1] += (tribe['color']['green'] * tribePopul)
        mix[2] += (tribe['color']['blue' ] * tribePopul)
        
    # Normalizujem mix na globalny strop=5000 density
    mix = normMax(mix, maxVal=denMax)
    
    return rgbToHex(mix[0], mix[1], mix[2])

#------------------------------------------------------------------------------
def getKnowlColor(tribes):
    
    return 'blue'

#------------------------------------------------------------------------------
def getPrefsColor(tribes):
    
    return 'green'
    
#------------------------------------------------------------------------------
def rgbToHex(r, g, b):
    
    return '#{:02X}{:02X}{:02X}'.format( round(r),round(g), round(b) )
   
#==============================================================================
# Math utilities
#------------------------------------------------------------------------------
def normMax(mix, maxVal, norma=255):
    
    # Nomralizujem na normu
    if maxVal>0:
        for i in range(len(mix)): mix[i] = mix[i] / maxVal * norma
    
    return mix
    
#------------------------------------------------------------------------------
def normSum(mix, norma=1):
    
    # Ziskam celkovu sumu mixu
    suma = 0
    for val in mix: suma += val
    
    if suma==0: return mix
    
    # Normalizacia na normu
    for i in range(len(mix)): mix[i] /= suma
    
    return mix

#==============================================================================
#                              END OF FILE
#------------------------------------------------------------------------------