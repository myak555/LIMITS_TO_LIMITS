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
        self.URR = np.sum( self.Production)*365.25/12/1000
        return

T  = np.linspace( 1950, 2050, 1201)

wells =  [Well( T, 1000, 0.70, 200, 0.40, [2010,2010,2012,2012,2020])]
Total_Production = np.zeros( len(T))
Total_URR = 0
for w in wells:
    Total_Production += w.Production 
    Total_URR += w.URR

fig = plt.figure( figsize=(15,10))
for i in range( len(wells)):
    w = wells[i]
    plt.plot( T, w.Production, "-", color="b", lw=1, label="Скважина {:g}, URR={:5.1f} тыс баррелей".format( i+1, w.URR))
plt.plot( T, Total_Production, "-", color="g", lw=3, label="Всего с месторождения, URR={:5.1f} тыс баррелей".format( Total_URR))
plt.xlabel("Годы")
plt.xlim( 1950, 2050)
plt.ylabel("Суточный дебит [баррелей]")
plt.ylim( 0, 1200)
plt.title( "Месторождение дяди Джо - одна суперскважина")
plt.grid(True)
plt.legend(loc=0)
plt.savefig( "./Graphs/figure_08_04.png")
fig.show()
