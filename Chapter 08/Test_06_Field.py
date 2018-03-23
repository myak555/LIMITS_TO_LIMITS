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
        return

T = np.linspace( 1900, 2100, 2401)
t = np.array( [0,13,18,36,80])
wt = np.ones( 50) * 1970
for i in range( len( wt)): wt[i] += i * 0.1
f = Field( wt, T, 800, 0.10, 800, 0.08, t)

WB = Weibull( x0=1970, b=0.033, k=1.7, peak=680/12)
WB_Data = WB.GetVector( T)
WB_URR = np.sum( WB_Data)
WB_Data *= 12e6/365.25

fig = plt.figure( figsize=(15,10))
plt.plot( T, f.Production, "-", color="g", lw=3, label="Всего с месторождения, URR={:7.1f} млн баррелей".format( f.URR))
plt.plot( T, WB_Data, "--", color="g", lw=2, label="Аппроксимация Вейбулла, URR={:7.1f} млн баррелей".format( WB_URR))
plt.xlabel("Годы")
plt.xlim( 1960, 2060)
plt.ylabel("Суточный дебит [баррелей]")
plt.ylim( 0, 50000)
plt.title( "Месторождение Весёлое - классическая разработка, 50 скважин")
plt.grid(True)
plt.legend(loc=0)
plt.savefig( ".\\Graphs\\figure_08_06.png")
fig.show()
