from Population import *

class VirusSpread1:
    def __init__(self, dt, nsamples, Rho_function, r, P):
        self.dt = dt
        self.r = r
        self.Population = P
        self.t0 = np.log(P)/r
        self.time = np.linspace(0,nsamples*dt,nsamples+1)
        self.Rho = Rho_function.GetVector(self.time)
        self.r0 = np.sum(self.Rho) * self.r * self.dt
        return
    def Integrate(self):
        L = len(self.time)
        self.Infected = np.zeros(L)
        self.Infected[0] = 1
        self.dI = np.zeros(L)
        self.dI[0] = 1
        self.Shedding = np.zeros(L)
        for i in range(1,L):
            # compute infected
            self.dI[i] = self.Shedding[i] * self.r * self.dt * \
                (1-self.Infected[i-1]/self.Population)
            self.Infected[i] = self.Infected[i-1] + self.dI[i]
            # update contageous
            for j in range( i,L):
                self.Shedding[j] += self.Rho[j-i] * self.dI[i-1]
        return

class VirusSpread2:
    def __init__(self, dt, nsamples, Rho_function, Phi_function, r, P):
        self.dt = dt
        self.r = r
        self.Population = P
        self.t0 = np.log(P)/r
        self.time = np.linspace(0,nsamples*dt,nsamples+1)
        self.Rho = Rho_function.GetVector(self.time)
        self.Phi = Phi_function.GetVector(self.time)
        self.PhiIndex = np.argmax( self.Phi)
        self.PhiMax = self.Phi[self.PhiIndex]
        #print(self.PhiIndex, self.PhiMax)
        self.r0 = np.sum(self.Rho) * self.r * self.dt
        return
    def Integrate(self):
        L = len(self.time)
        self.Infected = np.zeros(L)
        self.Infected[0] = 1
        self.dI = np.zeros(L)
        self.dI[0] = 1
        self.Shedding = np.zeros(L)
        self.Symptomatic = np.zeros(L)
        self.dS = np.zeros(L)
        self.Recovered = np.zeros(L)
        for i in range(1,L):
            # compute infected
            self.dI[i] = self.Shedding[i] * self.r * self.dt * \
                (1-self.Infected[i-1]/self.Population)
            self.Infected[i] = self.Infected[i-1] + self.dI[i]
            # update contageous and symptomatic
            for j in range( i,L):
                self.Shedding[j] += self.Rho[j-i] * self.dI[i-1]
                self.Symptomatic[j] += self.Phi[j-i] * self.dI[i-1]
        for i in range(self.PhiIndex, L):
            self.Recovered[i] = self.Infected[i-self.PhiIndex] * self.PhiMax
        self.dI /= self.dt
        for i in range(1,L):
            self.dS[i] = self.Recovered[i] - self.Recovered[i-1] 
        self.dS /= self.dt
        self.Recovered = np.clip( self.Recovered-self.Symptomatic, 0, self.Population)        
        print(min(self.Recovered),max(self.Recovered))
        return


P = 7.8e9
r = 0.242
Rho_function = Bathtub( x0=5.0, s0=2.0, x1 = 15.0, s1=0.8, left=0.0, middle=0.95, right=0.0)
Phi_function = Bathtub( x0=6.0, s0=3.0, x1 = 23.0, s1=0.6, left=0.0, middle=0.90, right=0.0)

VS1 = VirusSpread2(0.05, 12000, Rho_function, Phi_function, r, P)
#VS2 = VirusSpread1(0.05, 8000, Rho_function, r2, P)
VS1.Integrate()
#VS2.Integrate()

##print("Time\tI\tC\tdI")
##for i in range(0,len(day),10):
##    print("{:.0f}\t{:.0f}\t{:.0f}\t{:.0f}".format(day[i], I[i], C[i], dI[i]))

xlimits =(100,600)

fig = plt.figure( figsize=(15,10))
fig.suptitle( 'Эпидемия вируса "фиолетовой лихорадки"', fontsize=22)
gs = plt.GridSpec(2, 1, height_ratios=[2, 1.2]) 
ax1 = plt.subplot(gs[0])
ax2 = plt.subplot(gs[1])

ax1.plot( [xlimits[0], xlimits[1]], [P*1e-9, P*1e-9], "--", lw=2, color='k', label="Популяция")
ax1.plot( VS1.time, VS1.Infected*1e-9, "-", lw=3, color='g', label="Инфицированные")
ax1.plot( VS1.time, VS1.Recovered*1e-9, "-", lw=3, color='y', label="Переболевшие")
ax1.plot( VS1.time, VS1.Shedding*1e-9, "-", lw=3, color='r', label="Заразные (в т.ч. без симптомов)")
ax1.plot( VS1.time, VS1.Symptomatic*1e-9, "-", lw=3, color='m', label="Больные с симптомами")
##ax1.plot( VS2.time, VS2.Infected*1e-9, "-", lw=3, color='g', label="Инфицированные r0={:.2f}".format(VS2.r0))
##ax1.plot( VS2.time, VS2.Shedding*1e-9, "-", lw=3, color='r', label="Заразные r0={:.2f}".format(VS2.r0))
ax1.set_xlim( xlimits)
ax1.set_ylim( 0, 8)
ax1.set_ylabel("Миллиардов")
ax1.grid(True)
ax1.legend(loc=0)

ax2.plot( VS1.time, VS1.dI*1e-6, "-", lw=3, color='g',label="Заразились")
ax2.plot( VS1.time, VS1.dS*1e-6, "-", lw=3, color='m', label="Заболели")
#ax2.plot( VS2.time, VS2.dI*1e-6/VS2.dt, "-", lw=3, color='g')
ax2.set_xlim( xlimits)
ax2.set_ylim( 0, 200)
ax2.set_xlabel("День после первого случая")
ax2.set_ylabel("Млн в сутки")
ax2.grid(True)
ax2.legend(loc=0)

plt.savefig( "./Graphs/figure_23_05.png")

##fig = plt.figure( figsize=(15,5))
##fig.suptitle( 'Заразность и симптоматика', fontsize=22)
##gs = plt.GridSpec(2, 1, height_ratios=[1,0.1]) 
##ax1 = plt.subplot(gs[0])
##
##tau = np.linspace(0, 40, 401)
##ax1.plot( tau, Rho_function.GetVector(tau), "--", lw=2, color='g', label="Заразность")
##ax1.plot( tau, Phi_function.GetVector(tau), "-", lw=3, color='m', label="Симптоматика")
##ax1.set_xlim( tau[0], tau[-1])
##ax1.set_ylim( 0, 1)
##ax1.set_xlabel("День после заражения")
##ax1.set_ylabel("Вероятность")
##ax1.grid(True)
##ax1.legend(loc=0)
##plt.savefig( "./Graphs/figure_23_05a.png")

if InteractiveModeOn: plt.show(True)
