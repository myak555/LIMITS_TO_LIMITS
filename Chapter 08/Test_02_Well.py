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

w1 = Well( T, 24, 0.24, 18, 0.10, [1960,1963,1965,1974,2010])
w2 = Well( T, 22, 0.24, 17, 0.10, [1961,1963,1966,1975,2010])
w3 = Well( T, 20, 0.24, 16, 0.10, [1962,1963,1967,1976,2010])
Total_Production = w1.Production + w2.Production + w3.Production 
Total_URR = w1.URR + w2.URR + w3.URR

fig = plt.figure( figsize=(15,10))
plt.plot( T, w1.Production, "-", color="b", lw=1, label="Скважина 01, URR={:5.1f} тыс баррелей".format( w1.URR))
plt.plot( T, w2.Production, "--", color="b", lw=1, label="Скважина 02, URR={:5.1f} тыс баррелей".format( w2.URR))
plt.plot( T, w3.Production, "-.", color="b", lw=1, label="Скважина 03, URR={:5.1f} тыс баррелей".format( w3.URR))
plt.plot( T, Total_Production, "-", color="g", lw=3, label="Всего с месторождения, URR={:5.1f} тыс баррелей".format( Total_URR))
plt.xlabel("Годы")
plt.xlim( 1950, 2050)
plt.ylabel("Суточный дебит [баррелей]")
plt.ylim( 0, 80)
plt.title( "Месторождение дяди Джо - три скважины")
plt.grid(True)
plt.legend(loc=0)
plt.savefig( "./Graphs/figure_08_02.png")
fig.show()
