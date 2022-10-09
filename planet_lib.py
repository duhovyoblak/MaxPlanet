#==============================================================================
# Planet Max: library file
#------------------------------------------------------------------------------

#==============================================================================
# Constans
#------------------------------------------------------------------------------
heights = { 
       0: {'color':'#4faed0', 'agrSource': 0, 'indSource': 0.01},
       
     100: {'color':'#66ff33', 'agrSource': 0, 'indSource': 0.01},
     200: {'color':'#5ceb2e', 'agrSource': 0, 'indSource': 0.01},
     300: {'color':'#52d629', 'agrSource': 0, 'indSource': 0.01},
     400: {'color':'#47c224', 'agrSource': 0, 'indSource': 0.01},
     500: {'color':'#38a31c', 'agrSource': 0, 'indSource': 0.01},
     600: {'color':'#298514', 'agrSource': 0, 'indSource': 0.01},
     700: {'color':'#1a660d', 'agrSource': 0, 'indSource': 0.01},
     800: {'color':'#0a4705', 'agrSource': 0, 'indSource': 0.01},
     900: {'color':'#003300', 'agrSource': 0, 'indSource': 0.01},
     
    1000: {'color':'#333300', 'agrSource': 0, 'indSource': 0.01},
    1100: {'color':'#423300', 'agrSource': 0, 'indSource': 0.01},
    1200: {'color':'#523300', 'agrSource': 0, 'indSource': 0.01},
    1300: {'color':'#613300', 'agrSource': 0, 'indSource': 0.01},
    1400: {'color':'#803300', 'agrSource': 0, 'indSource': 0.01},
    1500: {'color':'#8f3300', 'agrSource': 0, 'indSource': 0.01},
    1600: {'color':'#9e3300', 'agrSource': 0, 'indSource': 0.01},
    1700: {'color':'#ad3300', 'agrSource': 0, 'indSource': 0.01},
    1800: {'color':'#bd3300', 'agrSource': 0, 'indSource': 0.01},
    1900: {'color':'#cc3300', 'agrSource': 0, 'indSource': 0.01},
    
    2000: {'color':'#d1470f', 'agrSource': 0, 'indSource': 0.01},
    2100: {'color':'#d6591d', 'agrSource': 0, 'indSource': 0.01},
    2200: {'color':'#da6c2b', 'agrSource': 0, 'indSource': 0.01},
    2300: {'color':'#df7e38', 'agrSource': 0, 'indSource': 0.01},
    2400: {'color':'#e8a354', 'agrSource': 0, 'indSource': 0.01},
    2500: {'color':'#edb562', 'agrSource': 0, 'indSource': 0.01},
    2600: {'color':'#f1c870', 'agrSource': 0, 'indSource': 0.01},
    2700: {'color':'#f6da7d', 'agrSource': 0, 'indSource': 0.01},
    2800: {'color':'#faed8b', 'agrSource': 0, 'indSource': 0.01},
    2900: {'color':'#ffff99', 'agrSource': 0, 'indSource': 0.01},
    
    3000: {'color':'#ffffff', 'agrSource': 0, 'indSource': 0.01}
}

#------------------------------------------------------------------------------
tribes = { 
       'Green Men'  : {'color'     : {'red':0,   'green':1,   'blue':0   }, 
                       'preference': {'agr':0.7, 'ind'  :0.2, 'war' :0.1 },
                       'knowledge' : {'agr':0.1, 'ind'  :0.1, 'war' :0.1 },
                      },
       'Blue Indy'  : {'color'     : {'red':0,   'green':0,   'blue':1   }, 
                       'preference': {'agr':0.2, 'ind'  :0.6, 'war' :0.2 },
                       'knowledge' : {'agr':0.1, 'ind'  :0.1, 'war' :0.1 },
                      },
       'Red Wariors': {'color'     : {'red':1,   'green':0,   'blue':0   }, 
                       'preference': {'agr':0.2, 'ind'  :0.3, 'war' :0.5 },
                       'knowledge' : {'agr':0.1, 'ind'  :0.1, 'war' :0.1 },
                      }
}

#==============================================================================
# Functions
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

#------------------------------------------------------------------------------
def rgbToHex(r, g, b):
    
    return '#{:02X}{:02X}{:02X}'.format( round(r),round(g), round(b) )
   
#==============================================================================
#                              END OF FILE
#------------------------------------------------------------------------------