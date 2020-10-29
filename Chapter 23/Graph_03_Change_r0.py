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

P = 7.8e9
r1 = 1.1
r2 = 0.242
Rho_function = Bathtub( x0=5.0, s0=2.0, x1 = 15.0, s1=0.8, left=0.0, middle=0.95, right=0.0)

VS1 = VirusSpread1(0.05, 8000, Rho_function, r1, P)
VS2 = VirusSpread1(0.05, 8000, Rho_function, r2, P)
VS1.Integrate()
VS2.Integrate()

##print("Time\tI\tC\tdI")
##for i in range(0,len(day),10):
##    print("{:.0f}\t{:.0f}\t{:.0f}\t{:.0f}".format(day[i], I[i], C[i], dI[i]))

xlimits =(0,500)

fig = plt.figure( figsize=(15,10))
fig.suptitle( 'Распространение скрытного вируса с при r0={:.2f} и {:.2f}'.format(VS1.r0, VS2.r0), fontsize=22)
gs = plt.GridSpec(2, 1, height_ratios=[2, 1.2]) 
ax1 = plt.subplot(gs[0])
ax2 = plt.subplot(gs[1])

ax1.plot( VS1.time, VS1.Infected*1e-9, "--", lw=3, color='g', label="Инфицированные r0={:.2f}".format(VS1.r0))
ax1.plot( VS1.time, VS1.Shedding*1e-9, "--", lw=3, color='r', label="Заразные r0={:.2f}".format(VS1.r0))
ax1.plot( VS2.time, VS2.Infected*1e-9, "-", lw=3, color='g', label="Инфицированные r0={:.2f}".format(VS2.r0))
ax1.plot( VS2.time, VS2.Shedding*1e-9, "-", lw=3, color='r', label="Заразные r0={:.2f}".format(VS2.r0))
ax1.set_xlim( xlimits)
ax1.set_ylim( 0, 8)
ax1.set_ylabel("Миллиардов инфицированных")
ax1.grid(True)
ax1.legend(loc=4)

ax2.plot( VS1.time, VS1.dI*1e-6/VS1.dt, "--", lw=3, color='g')
ax2.plot( VS2.time, VS2.dI*1e-6/VS2.dt, "-", lw=3, color='g')
ax2.set_xlim( xlimits)
ax2.set_ylim( 0, 800)
ax2.set_xlabel("День после первого случая")
ax2.set_ylabel("Млн случаев")
ax2.grid(True)

plt.savefig( "./Graphs/figure_23_04.png")
if InteractiveModeOn: plt.show(True)
