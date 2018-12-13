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
dYear, Discovery_Actual = Load_Calibration( "./Data/Backdated_Discovery_Laherrere_2014.csv", "Year", "Discovery")
for i in range(len(Years)):
    if Years[i] < dYear[0]: continue
    if dYear[-1] < Years[i]: break
    Discovery[i] = Discovery_Actual[ int(Years[i]-dYear[0])]
for i in range(99,-1,-1):
    Discovery[i] = Discovery[i+1] * 0.92

Discovery_Projected = np.array( Discovery)
Discovery_Projected_2 = np.array( Discovery)
Discovery_Projected_3 = np.array( Discovery)
for i in range(215,len(Years)):
    Discovery_Projected[i] = Discovery_Projected[i-1] * 0.965
    Discovery_Projected_2[i] = Discovery_Projected_2[i-1] * 0.90
    Discovery_Projected_3[i] = Discovery_Projected_3[i-1] * 0.99

Developed_Resource = np.convolve( mc.Filter, Discovery_Projected)[0:len(Years)]
Developed_Resource_2 = np.convolve( mc.Filter, Discovery_Projected_2)[0:len(Years)]
Developed_Resource_3 = np.convolve( mc.Filter, Discovery_Projected_3)[0:len(Years)]
Reserves = np.zeros( len(Years))
Reserves_2 = np.zeros( len(Years))
Reserves_3 = np.zeros( len(Years))
Production = np.zeros( len(Years))
Production_2 = np.zeros( len(Years))
Production_3 = np.zeros( len(Years))
Reserves[0] = Developed_Resource[0]
Reserves_2[0] = Developed_Resource_2[0]
Reserves_3[0] = Developed_Resource_3[0]

for i in range(1,len(Years)):
    Production[i] = Reserves[i-1] * sm.GetRate( Years[i])
    Reserves[i] = Reserves[i-1] + Developed_Resource[i] - Production[i]
    Production_2[i] = Reserves_2[i-1] * sm.GetRate( Years[i])
    Reserves_2[i] = Reserves_2[i-1] + Developed_Resource_2[i] - Production_2[i]
    Production_3[i] = Reserves_3[i-1] * sm.GetRate( Years[i])
    Reserves_3[i] = Reserves_3[i-1] + Developed_Resource_3[i] - Production_3[i]

Production = Filter( Production, matrix = [1,1,2,1,1])
Production_2 = Filter( Production_2, matrix = [1,1,2,1,1])
Production_3 = Filter( Production_3, matrix = [1,1,2,1,1])

Cumulative_Discovery = np.array( Discovery_Projected)
Cumulative_Developed = np.array( Developed_Resource)
Cumulative_Produced = np.array( Production)
for i in range( 1, len(Years)):
    Cumulative_Discovery[i] += Cumulative_Discovery[i-1]
    Cumulative_Developed[i] += Cumulative_Developed[i-1]
    Cumulative_Produced[i] += Cumulative_Produced[i-1]

pYear, pOil = Load_Calibration( "Resources_Calibration.csv", "Year", "Oil")
pCondensate, pNGPL = Load_Calibration( "Resources_Calibration.csv", "Condensate", "NGPL")
pOil += pCondensate

fig = plt.figure( figsize=(15,15))
fig.suptitle( 'Изменение URR в модели "Нефтяной шок" (П.Пукайт)', fontsize=22)
gs = plt.GridSpec(2, 1, height_ratios=[1.5, 1]) 
ax1 = plt.subplot(gs[0])
ax2 = plt.subplot(gs[1])

ax1.set_title("Открытия, освоение и добыча")
ax1.plot( Years, Discovery_Projected_3, "-.", lw=2, color="b", label="Открытия (оптимистично), URR={:.0f} млрд т".format( np.sum(Discovery_Projected_3)/1000))
ax1.plot( Years, Discovery_Projected, "-", lw=2, color="b", label="Открытия, URR={:.0f} млрд т".format( np.sum(Discovery_Projected)/1000))
ax1.plot( Years, Discovery_Projected_2, "--", lw=2, color="b", label="Открытия (пессимистично), URR={:.0f} млрд т".format( np.sum(Discovery_Projected_2)/1000))
#ax1.plot( Years, Developed_Resource, "-", lw=2, color="g", label="Освоенные ресурсы, URR={:.0f} млрд т".format( np.sum(Developed_Resource)/1000))
ax1.plot( Years, Production_3, "-.", lw=2, color="r", label="Добыча (оптимистично), URR={:.0f} млрд т".format( np.sum(Production_3)/1000))
ax1.plot( Years, Production, "-", lw=2, color="r", label="Добыча, URR={:.0f} млрд т".format( np.sum(Production)/1000))
ax1.plot( Years, Production_2, "--", lw=2, color="r", label="Добыча (пессимистично), URR={:.0f} млрд т".format( np.sum(Production_2)/1000))
ax1.errorbar( pYear, pOil, yerr=pOil*0.05, fmt=".", color="#FF5050")
ax1.set_xlim( 1900, 2200)
ax1.set_ylim( 0, 6000)
ax1.set_ylabel("млн тонн")
ax1.grid(True)
ax1.legend(loc=0)

ax2.set_title("Запасы")
#ax2.plot( Years, Cumulative_Discovery/1000, "-", lw=2, color="b", label="Всего открыто (Лагеррер, 2014)")
#ax2.plot( Years, Cumulative_Developed/1000, "-", lw=2, color="g", label="Всего освоено (модель)")
#ax2.plot( Years, Cumulative_Produced/1000, "-", lw=2, color="r", label="Всего добыто (модель)")
ax2.plot( Years, Reserves_3/1000, "-.", lw=2, color="k", label="Освоенные запасы (оптимистично)")
ax2.plot( Years, Reserves/1000, "-", lw=2, color="k", label="Освоенные запасы")
ax2.plot( Years, Reserves_2/1000, "--", lw=2, color="k", label="Освоенные запасы (пессимистично)")
ax2.set_xlim( 1900, 2200)
ax2.set_ylim( 0, 80)
ax2.set_xlabel("Год")
ax2.set_ylabel("млрд тонн")
ax2.grid(True)
ax2.legend(loc=0)

plt.savefig( ".\\Graphs\\figure_16_06.png")
fig.show()
