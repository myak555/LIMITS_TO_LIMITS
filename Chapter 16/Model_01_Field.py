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
f.Production *= 0.159 * 0.85 * 365.25 / 1000
f.URR *= 0.159 * 0.85
x = 600
Capex = Bathtub( 1959.8, 5, 1960.2, 5, 0, x*0.05, 0).GetVector(T)
Capex += Bathtub( 1962.8, 5, 1965.2, 5, 0, x*0.10, 0).GetVector(T)
Capex += Bathtub( 1968, 5, 1974, 5, 0, x, 0).GetVector(T)
Capex += Bathtub( 1988, 5, 1993, 5, 0, x*0.3, 0).GetVector(T)
Spenditure = Bathtub( 1965, 1, 2055, 1, 0, 15, 0).GetVector(T)

fig = plt.figure( figsize=(15,10))
plt.plot( T, f.Production, "-", color="g", lw=3, label="Добыча, URR={:.1f} млн тонн".format( f.URR))
plt.plot( T, -Capex, "--", color="r", lw=2, label="Капитальные затраты, Всего={:.1f} млн тонн".format( np.sum(Capex)/1000/12))
plt.plot( T, -Capex-Spenditure, "-", color="r", lw=3, label="+ Текущие затраты, Всего={:.1f} млн тонн".format( np.sum(Spenditure)/1000/12))
plt.annotate("Сейсморазведка", xy=(1960,5), xytext=(1952,750), arrowprops=dict(facecolor='black', shrink=0.05))
plt.annotate("Разведочные скважины", xy=(1964,5), xytext=(1968.5,600), arrowprops=dict(facecolor='black', shrink=0.05))
plt.annotate("Освоение", xy=(1971,5), xytext=(1975.5,450), arrowprops=dict(facecolor='black', shrink=0.05))
plt.annotate("Гидроразрывы", xy=(1990,5), xytext=(1981.5,300), arrowprops=dict(facecolor='black', shrink=0.05))
plt.annotate("Окончание эксплуатации", xy=(2056,-15), xytext=(2010,-300), arrowprops=dict(facecolor='black', shrink=0.05))
plt.xlabel("Годы")
plt.xlim( 1950, 2070)
plt.ylabel("Годовая добыча / затраты [тыс тонн]")
plt.ylim( -700, 2300)
plt.title( "Месторождение Весёлое - добыча и затраты")
plt.grid(True)
plt.legend(loc=1)
plt.savefig( ".\\Graphs\\figure_16_01.png")
fig.show()
