from Population import *

class VirusSpread1:
    def __init__(self, dt, nsamples, Rho_function, r, P):
        self.dt = dt
        self.r = r
        self.InitiallyInfected = 1
        self.Population = P
        self.t0 = np.log(P)/r
        self.time = np.linspace(0,nsamples*dt,nsamples+1)
        self.Rho = Rho_function.GetVector(self.time)
        self.r0 = np.sum(self.Rho) * self.r * self.dt
        return
    def Integrate(self):
        L = len(self.time)
        self.Susceptible = np.zeros(L)
        self.Susceptible[0] = P-self.InitiallyInfected
        self.Infected = np.zeros(L)
        self.Infected[0] = 1
        self.dI = np.zeros(L)
        self.dI[0] = self.InitiallyInfected
        self.Shedding = np.zeros(L)
        for i in range(1,L):
            # compute infected
            self.dI[i] = self.Shedding[i] * self.r * self.dt * \
                self.Susceptible[i-1]/self.Population
            self.Infected[i] = self.Infected[i-1] + self.dI[i]
            self.Susceptible[i] = self.Susceptible[i-1] - self.dI[i]
            # update contageous
            for j in range( i,L):
                self.Shedding[j] += self.Rho[j-i] * self.dI[i-1]
        self.dI /= self.dt
        return

class VirusSpread2:
    def __init__(self, dt, nsamples, Rho_function, Phi_function, rN, rS, P):
        self.dt = dt
        self.rN = rN
        self.rS = rS
        self.Population = P
        self.InitiallyInfected = 1
        self.time = np.linspace(0,nsamples*dt,nsamples+1)
        self.Phi = Phi_function.GetVector(self.time)
        self.dPhiS = np.clip( Rate(self.Phi, dt), 0, 1)
        self.dPhiR = np.clip( -Rate(self.Phi, dt), 0, 1)
        self.Rho = Rho_function.GetVector(self.time)
        self.RhoN = np.clip(self.Rho-self.Phi, 0, 1)
        self.RhoS = self.Rho - self.RhoN
        self.r0 = np.sum(self.Rho) * self.rN * self.dt
        self.t0 = np.log(P)/self.rN
        return
    def Integrate(self):
        L = len(self.time)
        self.Susceptible = np.zeros(L)
        self.Susceptible[0] = P-self.InitiallyInfected
        self.Infected = np.zeros(L)
        self.Infected[0] = self.InitiallyInfected
        self.dI = np.zeros(L)
        self.dI[0] = self.InitiallyInfected
        self.SheddingN = np.zeros(L)
        self.SheddingS = np.zeros(L)
        self.Symptomatic = np.zeros(L)
        self.dSymptoms = np.zeros(L)
        self.Recovered = np.zeros(L)
        for i in range(1,L):
            # compute infected
            self.dI[i] = (self.SheddingN[i] * self.rN + \
                self.SheddingS[i] * self.rS) * self.dt * \
                self.Susceptible[i-1]/self.Population
            self.Infected[i] = self.Infected[i-1] + self.dI[i]
            self.Susceptible[i] = self.Susceptible[i-1] - self.dI[i]
            # update contageous and symptomatic
            for j in range( i,L):
                self.SheddingN[j] += self.RhoN[j-i] * self.dI[i-1]
                self.SheddingS[j] += self.RhoS[j-i] * self.dI[i-1]
                self.Symptomatic[j] += self.Phi[j-i] * self.dI[i-1]
                self.dSymptoms[j] += self.dPhiS[j-i] * self.dI[i-1]
                self.Recovered[j] += self.dPhiR[j-i] * self.dI[i-1]
        self.dI /= self.dt
        self.Recovered = Cumulative(self.Recovered) * self.dt
        #self.dSymptoms /= self.dt        
        #self.Recovered = self.Infected - self.Symptomatic
        return


P = 7.8e9
r = 0.255
rN = r
rS = r*0.50
Rho_function = Bathtub( x0=5.5, s0=1.6, x1 = 15.0, s1=0.8, left=0.0, middle=0.95, right=0.0)
Phi_function = Bathtub( x0=6.0, s0=3.0, x1 = 23.0, s1=0.6, left=0.0, middle=0.90, right=0.0)

VS1 = VirusSpread1(0.25, 6000, Rho_function, r, P)
VS2 = VirusSpread2(0.25, 6000, Rho_function, Phi_function, rN, rS, P)
VS1.Integrate()
VS2.Integrate()

print("Time\tI\t\tdI\t\tS\t\tShedding")
for i in range(0,len(VS2.time),40):
    print("{:.0f}\t{:>.0f}\t\t{:>.0f}".format(
        VS2.time[i], VS2.Symptomatic[i], VS2.Infected[i]))

xlimits =(200,1400)
norm = 1e-9

fig = plt.figure( figsize=(15,10))
fig.suptitle( 'Нелетальный вирус, социальное дистанцирование', fontsize=22)
gs = plt.GridSpec(2, 1, height_ratios=[2, 1.2]) 
ax1 = plt.subplot(gs[0])
ax2 = plt.subplot(gs[1])

ax1.plot( [xlimits[0], xlimits[1]], [P*norm, P*norm], "-.", lw=2, color='k', label="Популяция")
ax1.plot( VS2.time, VS2.Infected*norm, "-", lw=3, color='g', label="Инфицированные")
ax1.plot( VS2.time, VS2.Recovered*norm, "-", lw=3, color='y', label="Переболевшие")
ax1.plot( VS2.time, VS2.SheddingN*norm, "-", lw=3, color='r', label="Заразные (без симптомов)")
ax1.plot( VS2.time, VS2.SheddingS*norm, "-", lw=3, color='k', label="Заразные (с симптомами)")
ax1.plot( VS2.time, VS2.Symptomatic*norm, "-", lw=3, color='m', label="Больные с симптомами")
ax1.plot( VS1.time, VS1.Infected*norm, "--", lw=2, color='k', label="Инфицированные, R=Const")
ax1.plot( VS1.time, VS1.Shedding*norm, "-.", lw=2, color='k', label="Заразные, R=Const")
ax1.set_xlim( xlimits)
ax1.set_ylim( 0, 8)
ax1.set_ylabel("Миллиардов")
ax1.grid(True)
ax1.legend(loc=0)

ax2.plot( VS2.time, VS2.dI*1e-6, "-", lw=3, color='g',label="Заразились")
ax2.plot( VS2.time, VS2.dSymptoms*1e-6, "-", lw=3, color='m', label="Заболели")
ax2.plot( VS1.time, VS1.dI*1e-6, "--", lw=2, color='g',label="Без дистанционирования")
ax2.set_xlim( xlimits)
ax2.set_ylim( 0, 175)
ax2.set_xlabel("День после первого случая")
ax2.set_ylabel("миллионов в сутки")
ax2.grid(True)
ax2.legend(loc=0)

plt.savefig( "./Graphs/figure_23_03.png")


if False:
    fig = plt.figure( figsize=(15,5))
    fig.suptitle( 'Заразность и симптоматика', fontsize=22)
    gs = plt.GridSpec(2, 1, height_ratios=[1,0.05]) 
    ax1 = plt.subplot(gs[0])
    ax1.plot( VS2.time, VS2.Phi, "-", lw=2, color='m', label="Симптоматика")
    ax1.plot( VS2.time, VS2.Rho, "-", lw=2 , color='g', label="Заразность")
    ax1.plot( VS2.time, VS2.RhoN, "-.", lw=3, color='k', label="Заразность без симптомов")
    ax1.plot( VS2.time, VS2.RhoS, "--", lw=3, color='k', label="Заразность с симптомами")
    ax1.fill_between(VS2.time, VS2.RhoS, color="m", alpha=0.1)
    ax1.fill_between(VS2.time, VS2.RhoN, color="k", alpha=0.3)
    ax1.set_xlim( 0, 40)
    ax1.set_ylim( 0, 1)
    ax1.set_xlabel("День после заражения")
    ax1.set_ylabel("Вероятность")
    ax1.grid(True)
    ax1.legend(loc=0)
    plt.savefig( "./Graphs/figure_23_03a.png")


if InteractiveModeOn: plt.show(True)
