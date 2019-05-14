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

w1 = Well( T, 24, 0.08, 18, 0.06, [1960,1970,1980,1990,2030])

fig = plt.figure( figsize=(15,10))
plt.plot( T, w1.Production, "-", lw=1, label="Скважина 01, URR={:5.1f} тыс баррелей".format( w1.URR))
plt.xlabel("Годы")
plt.xlim( 1950, 2050)
plt.ylabel("Суточный дебит [баррелей]")
plt.ylim( 0, 30)
plt.title( "Типичный профиль добычи нефтяной скважины")
plt.grid(True)
plt.legend(loc=0)
plt.annotate("Разведка и принятие решения", xy=(1954,0), xytext=(1964,8), arrowprops=dict(facecolor='black', shrink=0.05))
plt.annotate("Бурение", xy=(1958,0), xytext=(1965,6), arrowprops=dict(facecolor='black', shrink=0.05))
plt.annotate("Ввод в эксплуатацию", xy=(1960,0), xytext=(1966,5), arrowprops=dict(facecolor='black', shrink=0.05))
plt.annotate('Фонтанная добыча. "Полочка" определяется конструкцией скважины и параметрами залежи', xy=(1962,24), xytext=(1965,27), arrowprops=dict(facecolor='black', shrink=0.05))
plt.annotate("Фонтанная добыча. Снижение пластового давления", xy=(1973,19), xytext=(1978,22), arrowprops=dict(facecolor='black', shrink=0.05))
plt.annotate("Капремонт и интенсификация добычи (например, гидроразрыв)", xy=(1980,18), xytext=(1983,20), arrowprops=dict(facecolor='black', shrink=0.05))
plt.annotate("Механизированная добыча. Рост обводнённости", xy=(2001,9), xytext=(2007,13), arrowprops=dict(facecolor='black', shrink=0.05))
plt.annotate("Скважина тампонирована", xy=(2030,2), xytext=(2024,6), arrowprops=dict(facecolor='black', shrink=0.05))
plt.savefig( "./Graphs/figure_08_01.png")
fig.show()
