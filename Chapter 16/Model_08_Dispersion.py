from Predictions import *

class Markov_Chain:
    def __init__( self, taus, Years, Year0, time_shift=0):
        self.Years = Years
        self.Year0 = Year0
        self.Filter = self.GetRho(taus[0])
        offset = int( self.Year0 - self.Years[0]) 
        for i in range( 1, len(taus)):
            self.Filter = np.convolve( self.Filter, self.GetRho(taus[i]))[offset:offset+len(self.Years)]
        self.Filter = np.roll( self.Filter, time_shift)
        return        
    def GetRho(self, tau):
        Time = self.Years - self.Year0
        tmp = np.exp( -Time/tau)
        for i in range( len(self.Years)):
            if self.Years[i]>=self.Year0: break
            tmp[i] = 0.0
        norm = np.sum( tmp)
        #print( tau, norm, 1/norm)
        return tmp/norm

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

Years = np.linspace( 1800,2200,401)
k = 130
X1 = (Years - 1799)/k
Y1 = X1**6 * (1-np.exp(-1/X1**6)) 
dY1 = 6 * X1**5 - 6 * np.exp(-1/X1**6) * (X1**5 + 1/X1)
norm = 310e3 / Y1[-1] 
Y1 *= norm
Y1 = np.roll( Y1, 48)
Y1[:48] = 0
norm = 310e3 / np.sum( dY1) 
dY1 *= norm
dY1 = np.roll( dY1, 48)
dY1[:48] = 0
dY2 = Gompertz(2035,0.05,0.039,310000).GetVector(Years)
Y2 = GompertzIntegral(2035,0.05,0.039,310000).GetVector(Years)
dY3 = GenHubbert(1914,0.28,0.15,21700).GetVector(Years)

Discovery = np.zeros( len(Years))
dYear, Discovery_Actual = Load_Calibration( "./Data/Backdated_Discovery_Laherrere_2014.csv", "Year", "Discovery")
for i in range(len(Years)):
    if Years[i] < dYear[0]: continue
    if dYear[-1] < Years[i]: break
    Discovery[i] = Discovery_Actual[ int(Years[i]-dYear[0])]
for i in range(99,-1,-1):
    Discovery[i] = Discovery[i+1] * 0.92

Discovery_Projected = np.array( Discovery)
for i in range(215,len(Years)):
    Discovery_Projected[i] = Discovery_Projected[i-1] * 0.965

Cumulative_Discovery = np.array( Discovery_Projected)
Cumulative_Y3 = np.array( dY3)
for i in range( 1, len(Years)):
    Cumulative_Discovery[i] += Cumulative_Discovery[i-1]
    Cumulative_Y3[i] += Cumulative_Y3[i-1]

fig = plt.figure( figsize=(15,10))
fig.suptitle( 'Описание открытий кривой Хабберта и дисперсионной кривой Пукайта', fontsize=22)
gs = plt.GridSpec( 2, 1) 
ax1 = plt.subplot(gs[0])
ax2 = plt.subplot(gs[1])

ax1.set_title("Открытия в год")
ax1.plot( Years, Discovery_Projected, "-", lw=2, color="b", label="Открытия, URR={:.0f} млрд т".format( np.sum(Discovery_Projected)/1000))
ax1.plot( Years, dY1, "-", lw=2, color="g", label="Дисперсионная модель Пукайта, URR={:.0f} млрд т".format( np.sum(dY1)/1000))
ax1.plot( Years, dY2, "-", lw=2, color="m", label="Кривая Гомперца, URR={:.0f} млрд т".format(np.sum(dY2)/1000))
ax1.plot( Years, dY3, "-", lw=2, color="r", label="Хаббертиана, URR={:.0f} млрд т".format(np.sum(dY3)/1000))
ax1.set_xlim( 1850, 2200)
ax1.set_ylim( 0, 6000)
ax1.set_ylabel("млн тонн")
ax1.grid(True)
ax1.legend(loc=0)

ax2.set_title("Накопленные")
ax2.plot( Years, Cumulative_Discovery/1000, "-", lw=2, color="b", label="URR={:.0f} млрд т".format( Cumulative_Discovery[-1]/1000))
ax2.plot( Years, Y1/1000, "-", lw=2, color="g", label="URR={:.0f} млрд т".format( Y1[-1]/1000))
ax2.plot( Years, Y2/1000, "-", lw=2, color="m", label="URR={:.0f} млрд т".format( Y2[-1]/1000))
ax2.plot( Years, Cumulative_Y3/1000, "-", lw=2, color="r", label="URR={:.0f} млрд т".format( Cumulative_Y3[-1]/1000))
ax2.set_xlim( 1850, 2200)
ax2.set_ylim( -50, 350)
ax2.set_ylabel("млрд тонн")
ax2.grid(True)
ax2.legend(loc=0)
ax2.set_xlabel("Год")

plt.savefig( ".\\Graphs\\figure_16_08.png")
fig.show()
