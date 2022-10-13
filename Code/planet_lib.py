#==============================================================================
# Planet Max: library file
#------------------------------------------------------------------------------

#==============================================================================
# Constans
#------------------------------------------------------------------------------
heights = { 
       0: {'color':'#4faed0', 'agrSource':  0, 'indSource':  0},
       
     100: {'color':'#66ff33', 'agrSource': 18, 'indSource':  4},
     200: {'color':'#5ceb2e', 'agrSource': 20, 'indSource':  4},
     300: {'color':'#52d629', 'agrSource': 17, 'indSource':  4},
     400: {'color':'#47c224', 'agrSource': 14, 'indSource':  6},
     500: {'color':'#38a31c', 'agrSource': 12, 'indSource':  8},
     600: {'color':'#298514', 'agrSource': 10, 'indSource': 12},
     700: {'color':'#1a660d', 'agrSource':  9, 'indSource': 16},
     800: {'color':'#0a4705', 'agrSource':  8, 'indSource': 20},
     900: {'color':'#003300', 'agrSource':  7, 'indSource': 20},
     
    1000: {'color':'#333300', 'agrSource':  7, 'indSource': 19},
    1100: {'color':'#423300', 'agrSource':  6, 'indSource': 18},
    1200: {'color':'#523300', 'agrSource':  6, 'indSource': 17},
    1300: {'color':'#613300', 'agrSource':  5, 'indSource': 16},
    1400: {'color':'#803300', 'agrSource':  5, 'indSource': 14},
    1500: {'color':'#8f3300', 'agrSource':  4, 'indSource': 11},
    1600: {'color':'#9e3300', 'agrSource':  4, 'indSource':  9},
    1700: {'color':'#ad3300', 'agrSource':  3, 'indSource':  8},
    1800: {'color':'#bd3300', 'agrSource':  3, 'indSource':  7},
    1900: {'color':'#cc3300', 'agrSource':  3, 'indSource':  6},
    
    2000: {'color':'#d1470f', 'agrSource':  2, 'indSource':  5},
    2100: {'color':'#d6591d', 'agrSource':  1, 'indSource':  4},
    2200: {'color':'#da6c2b', 'agrSource':  0, 'indSource':  4},
    2300: {'color':'#df7e38', 'agrSource':  0, 'indSource':  3},
    2400: {'color':'#e8a354', 'agrSource':  0, 'indSource':  3},
    2500: {'color':'#edb562', 'agrSource':  0, 'indSource':  3},
    2600: {'color':'#f1c870', 'agrSource':  0, 'indSource':  2},
    2700: {'color':'#f6da7d', 'agrSource':  0, 'indSource':  2},
    2800: {'color':'#faed8b', 'agrSource':  0, 'indSource':  1},
    2900: {'color':'#ffff99', 'agrSource':  0, 'indSource':  1},
    
    3000: {'color':'#ffffff', 'agrSource':  0, 'indSource':  0}
}

#------------------------------------------------------------------------------
tribes = { 
       'Green Men'  : {'color'     : {'red':0,   'green':1,   'blue':0   }, 
                       'preference': {'agr':1.0, 'ind'  :0.0, 'war' :0.0 },
                       'knowledge' : {'agr':0.1, 'ind'  :0.1, 'war' :0.1 },
                      },
       'Blue Indy'  : {'color'     : {'red':0,   'green':0,   'blue':1   }, 
                       'preference': {'agr':0.0, 'ind'  :1.0, 'war' :0.0 },
                       'knowledge' : {'agr':0.1, 'ind'  :0.1, 'war' :0.1 },
                      },
       'Red Wariors': {'color'     : {'red':1,   'green':0,   'blue':0   }, 
                       'preference': {'agr':0.0, 'ind'  :0.0, 'war' :1.0 },
                       'knowledge' : {'agr':0.1, 'ind'  :0.1, 'war' :0.1 },
                      }
}

#==============================================================================
# Functions
#------------------------------------------------------------------------------
def getHeightAgrSource(height):
    
    return heights['agrSource']

#------------------------------------------------------------------------------
def getHeightIndSource(height):
    
    return heights['indSource']

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