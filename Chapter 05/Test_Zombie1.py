from Population import *

#
# Описывает модель для задачи "зомби-апокалипсиса"
# "When zombies attack!:  Mathematical modelling of an outbreak of zombie infection"
# by Philip Munz, Ioan Hudea, Joe Imad, and Robert J. Smith
# S0 - начальная популяция людей
# I0 - начальная популяция инфицированных
# Z0 - начальная популяция зомби
#
class Zombie_Apocalypse_1:
    def __init__( self, S0=7630, I0=2.8, Z0=0.0006):
        self.StablePopulation = 10000 # стабильная популяция (людей)
        self.S_Initial = S0
        self.S = S0
        self.I_Initial = I0
        self.I = I0
        self.Z_Initial = Z0
        self.Z = Z0
        self.natural_birth_rate = 0.0495/365 # естественная рождаемость (людей)
        self.transmission = 0.00002 # заражение людей от зомби и инфицированных
        self.conversion = 1/28 # превращение заражённых в зомби (инкубационный период 28 дней)
        self.human_kill = 0.000001 # уничтожение человека (зомби съели мозг) 
        self.zombie_kill = 0.000001 # уничтожение зомби (разрывная пуля в голову) 
        self.zombie_rot = 0.001 # естественное гниение зомби
        return
    def dS_dt( self, t):
        tmp = 1 - (self.S+self.I)/self.StablePopulation
        tmp *= self.natural_birth_rate*self.S
        tmp -= self.transmission*self.S*(self.Z+self.I)
        tmp -= self.human_kill*self.S*self.Z
        return tmp
    def dI_dt( self, t):
        tmp = -(self.S+self.I)/self.StablePopulation
        tmp *= self.natural_birth_rate*self.I
        tmp += self.transmission*self.S*self.Z
        tmp -= self.conversion*self.I
        tmp -= self.human_kill*self.I*self.Z
        return tmp
    def dZ_dt( self, t):
        tmp = self.conversion*self.I
        tmp -= self.zombie_kill*(self.S+self.I)*self.Z
        tmp -= self.zombie_rot*self.Z
        return tmp
    def _func( self, y, t):
        self.S = max( [y[0], 0])
        self.I = max( [y[1], 0])
        self.Z = max( [y[2], 0])
        if self.last_billion_day<0 and self.S+self.I < 1000:
            self.last_billion_day = int(t)
            print( "Last billion on day:", self.last_billion_day)
        if self.last_million_day<0 and self.S+self.I < 1:
            self.last_million_day = int(t)
            print( "Last million on day:", self.last_million_day)
        if self.last_thousand_day<0 and self.S+self.I < 1e-3:
            self.last_thousand_day = int(t)
            print( "Last thousand on day:", self.last_thousand_day)
        if self.last_human_day<0 and self.S+self.I < 1e-6:
            self.S = 0
            self.I = 0
            self.last_human_day = int(t)
            print( "Last human on day:", self.last_human_day)
        f0 = self.dS_dt( t)
        f1 = self.dI_dt( t)
        f2 = self.dZ_dt( t)
        return [f0, f1, f2]
    def Solve( self, t0):
        self.last_billion_day = -1
        self.last_million_day = -1
        self.last_thousand_day = -1
        self.last_human_day = -1
        y0 = [self.S, self.I, self.Z]
        soln = odeint(self._func, y0, t0, h0=0.01, hmax = 0.25)
        self.Solution_Time = t0
        self.Solution_Population = soln[:, 0].clip(0) + soln[:, 1].clip(0)
        self.Solution_Infected = soln[:, 1].clip(0)
        self.Solution_Zombies = soln[:, 2].clip(0)
        self.S = self.S_Initial
        self.I = self.I_Initial
        self.Z = self.Z_Initial
        return

#
# Solve numerically
#
T = np.linspace(0, 365*5, 365*5+1)
Z1 = Zombie_Apocalypse_1()
Z1.Solve( T)

fig = plt.figure( figsize=(15,10))
#plt.errorbar( [0,3650], [7633,8410], fmt="o")
plt.plot( Z1.Solution_Time, Z1.Solution_Population, "-", color="b", lw=3, label="Популяция людей")
plt.plot( Z1.Solution_Time, Z1.Solution_Infected, "--", color="b", lw=3, label="В том числе инфицированных")
plt.plot( Z1.Solution_Time, Z1.Solution_Zombies, "-", color="g", lw=3, label="Популяция зомби")
plt.plot( [Z1.last_billion_day, Z1.last_million_day, Z1.last_thousand_day, Z1.last_human_day], [1000, 1,1e-3,1e-6], "o", color="k")
plt.text( Z1.last_billion_day, 1050, "Миллиард выживших: день {:g}".format(Z1.last_billion_day))
plt.text( Z1.last_million_day, 450, "Последний миллион выживших: день {:g}".format(Z1.last_million_day))
plt.text( Z1.last_thousand_day-100, 250, "Последняя тысяча выживших: день {:g}".format(Z1.last_thousand_day))
plt.text( Z1.last_human_day-200, 50, "Последний выживший: день {:g}".format(Z1.last_human_day))
plt.xlabel("дни")
plt.xlim( 0, 1000)
plt.ylabel("миллионов")
plt.ylim( 0, 8000)
plt.title( "Эпидемия зомбивируса")
plt.grid(True)
plt.legend(loc=0)
plt.savefig( ".\\Graphs\\figure_05_14.png")
fig.show()
