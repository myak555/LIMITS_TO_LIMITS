from Population import *

#
# Описывает дебит из условной скважины:
# после бурения: начальный дебит Q0 со спадом dQ0
# после интенсификации: начальный дебит Q1 со спадом dQ1
# ввод в эксплуатацию t[0], плато до t[1],
# интенсификация t[2], плато до t[3]
# тампонаж t[4]
#
class Well:
    def __init__( self, T0, Q0, dQ0, Q1, dQ1, t):
        self.Initial = Q0
        self.Decline0 = dQ0
        self.Enhanced = Q1
        self.Decline1 = dQ1
        self.Production = np.zeros( len(T0))
        for i in range( len( T0)):
            dt = T0[i]
            if dt < t[0]: continue
            if dt >= t[4]: continue
            if t[0] <= dt and dt < t[2]:
                self.Production[i] = self.Initial * (1-self.Decline0) ** max( 0, dt-t[1]) 
            if t[2] <= dt and dt < t[4]:
                self.Production[i] = self.Enhanced * (1-self.Decline1) ** max( 0, dt-t[3]) 
        self.URR = np.sum( self.Production)*365.25/12/1000000
        return

#
# Описывает дебит из условного месторождения:
# WТ - расписание ввода скважин по годам
#
class Field:
    def __init__( self, WT, T0, Q0, dQ0, Q1, dQ1, t):
        self.Wells = []
        self.Production = np.zeros( len(T0))
        self.URR = 0
        for i in range( len(WT)):
            rnd = 0.9 + np.random.random() * 0.2
            tmp = Well( T0, Q0*rnd, dQ0, Q1*rnd, dQ1, t+WT[i])
            self.Wells += [tmp]
            self.Production += tmp.Production
            self.URR += tmp.URR
        self.Cumulative = np.array( self.Production)
        for i in range( 1, len( self.Cumulative)): self.Cumulative[i] += self.Cumulative[i-1] 
        return

T = np.linspace( 1900, 2100, 2401)
t = np.array( [0,13,18,36,80])
wt = np.ones( 85) * 1970
for i in range( len( wt)):
    wt[i] += i * 0.1
    if i > 45: wt[i] += 9
    if i > 47: wt[i] += 3
    if i > 49: wt[i] += 22
    if i > 55: wt[i] += 2
    if i > 60: wt[i] += 5
    if i > 70: wt[i] += 5
f = Field( wt, T, 865, 0.10, 800, 0.08, t)

WB = Weibull( x0=1970, peak=1200/12, b=0.022, k=1.5)
WB_Data = WB.GetVector( T)
WB_URR = np.sum( WB_Data)
WB_Cumulative = np.array( WB_Data)
for i in range( 1, len(WB_Data)): WB_Cumulative[i] += WB_Cumulative[i-1]  
WB_Data *= 12e6/365.25

T_Report =   [1965, 1970, 1980, 1990, 2000, 2010, 2020, 2030, 2040]
URR_Proven = [   5,  550, 1120, 1120, 1120, 1190, 1200, 1250, 1250]
NWells =     [   1,    6,   51,   53,   60,   70,   80,   85,   85]

Creaming = Sigmoid( 1965, 0.1, -1250, 1250).GetVector( T)
Remaining = Creaming - f.Cumulative/12e6*365.25
NWells1 = np.linspace( 1,300,301)
Creaming_Approx = 5 + 280*np.log(NWells1)

fig = plt.figure( figsize=(15,10))
plt.plot( NWells1, Creaming_Approx, "--", color="b", lw=2, label="Аппроксимация -- запасы растут бесконечно")
plt.errorbar( NWells, URR_Proven, fmt='o', color="b", label="SEC начальные извлекаемые [млн баррелей]")
plt.xlabel("Количество пробуренных скважин (включая разведочные)")
plt.xlim( 0, 300)
plt.ylabel("миллионов баррелей")
plt.ylim( 0, 2000)
plt.title( "Месторождение Весёлое - кривая снятия сливок")
plt.grid(True)
plt.legend(loc=0)
plt.annotate("Здесь две точки - из отчётов 2030 и 2040 годов!", xy=(85,1250), xytext=(115,885), arrowprops=dict(facecolor='black', shrink=0.05))
plt.savefig( "./Graphs/figure_08_08.png")
if InteractiveModeOn: plt.show(True)
