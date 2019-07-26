from Predictions import *

class Shock_Model:
    def __init__( self):
        self.Pairs = []
        self.Pairs += [(1880,   0.035)] ## Start of data
        self.Pairs += [(1909,   0.031)] ## pre-WW1
        self.Pairs += [(1920,   0.038)] ## post-WW1
        self.Pairs += [(1929,   0.050)] ## Great Depression
        self.Pairs += [(1935,   0.047)] ## 
        self.Pairs += [(1940,   0.040)] ## WW2
        self.Pairs += [(1960,   0.040)] ## Space race
        self.Pairs += [(1968,   0.055)] ## 
        self.Pairs += [(1973,   0.068)] ## Start of oil embargo
        self.Pairs += [(1974,   0.066)] ##
        self.Pairs += [(1975,   0.060)] ## End of oil embargo
        self.Pairs += [(1979,   0.065)] ## Start of Iran hostage crisis
        self.Pairs += [(1981,   0.055)] ## Start of recession
        self.Pairs += [(1985,   0.048)] ## End of recession
        self.Pairs += [(1990,   0.048)] ## Start of Gulf War
        self.Pairs += [(1993,   0.046)] ## Fall of USSR/CIS
        self.Pairs += [(2000,   0.050)] ## Dot-Coms
        self.Pairs += [(2002,   0.050)] ##
        self.Pairs += [(2007,   0.057)] ## GFC
        self.Pairs += [(2009,   0.056)] ## Rush for "shale oil"
        self.Pairs += [(2015,   0.070)] ## Great Recession
        self.Pairs += [(2030,   0.100)]
        self.Pairs += [(2100,   0.100)]
        return
    def GetRate( self, y):
        y0, r0 = self.Pairs[0]
        if y < y0: return r0
        for i in range( 1, len(self.Pairs)):
            y0, r0 = self.Pairs[i-1]
            y1, r1 = self.Pairs[i]
            if y0 > y or y >= y1: continue
            tmp = r0 * (y1-y)
            tmp += r1 * (y-y0) 
            return tmp / (y1 - y0)
        y1, r1 = self.Pairs[-1]
        return r1
    def GetVector( self, years):
        tmp = np.zeros( len(years))
        for i in range( len(tmp)):
            tmp[i] = self.GetRate( years[i])
        return tmp

Years = np.linspace( 1800,2300,501)
mc = Markov_Chain([3, 8, 5, 10], Years, Years[0])
sm = Shock_Model()
Discovery = np.zeros( len(Years))
dYear, Discovery_Actual = Load_Calibration(
    "../Global Data/Laherrere_2014_Backdated_Discovery.csv",
    ["Year", "Discovery"])
for i in range(len(Years)):
    if Years[i] < dYear[0]: continue
    if dYear[-1] < Years[i]: break
    Discovery[i] = Discovery_Actual[ int(Years[i]-dYear[0])]
for i in range(99,-1,-1):
    Discovery[i] = Discovery[i+1] * 0.92

pYear, pOil, pCondensate, pNGPL = Load_Calibration(
    "../Global Data/Resources_Calibration.csv",
    ["Year", "Oil", "Condensate", "NGPL"])
pOil += pCondensate
