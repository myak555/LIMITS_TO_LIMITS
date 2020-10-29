from Population import *

class VirusSpread1:
    def __init__(self, dt, nsamples, Rho_function, r, P):
        self.dt = dt
        self.r = r
        self.Population = P
        self.t0 = np.log(P)/r
        self.Susceptible_Fraction = 0.5
        self.time = np.linspace(0,nsamples*dt,nsamples+1)
        self.Rho = Rho_function.GetVector(self.time)
        self.r0 = np.sum(self.Rho) * self.r * self.dt
        return
    def Integrate(self):
        L = len(self.time)
        self.Susceptible = np.zeros(L)
        self.Susceptible[0] = (P-1) * self.Susceptible_Fraction 
        self.Infected = np.zeros(L)
        self.Infected[0] = 1
        self.dI = np.zeros(L)
        self.dI[0] = 1
        self.Shedding = np.zeros(L)
        for i in range(1,L):
            # compute infected
            self.dI[i] = self.Shedding[i] * self.r * self.dt * \
                (self.Susceptible[i-1]/self.Population)
            self.Infected[i] = self.Infected[i-1] + self.dI[i]
            self.Susceptible[i] = self.Susceptible[i-1] - self.dI[i]
            # update contageous
            for j in range( i,L):
                self.Shedding[j] += self.Rho[j-i] * self.dI[i-1]
        self.dI /= self.dt
        return

P = 7.8e9
#r = 2.0/9.0
r = 0.255*2
#r = 2.5/9.0
Rho_function = Bathtub( x0=5.5, s0=1.6, x1 = 15.0, s1=0.8, left=0.0, middle=0.95, right=0.0)
VS = VirusSpread1(0.25, 1000*4, Rho_function, r, P)
VS.Integrate()
print( np.sum(VS.Rho))

day = np.linspace(0,1000,1001)
rs = 0.255
t0 = np.log(P)/rs
I = Sigmoid(t0, rs, 0, P).GetVector(day)
dI = Hubbert(t0, rs, rs, peak=P*rs/4).GetVector(day)

print("Time\tI\t\tdI\t\tS\t\tShedding")
for i in range(0,len(VS.time),40):
    print("{:.0f}\t{:>.0f}\t\t{:>.0f}\t\t{:>.0f}\t\t{:>.0f}".format(VS.time[i], VS.Infected[i], VS.dI[i], VS.Susceptible[i], VS.Shedding[i]))

xlimits =(0,600)
norm = 1e-9

fig = plt.figure( figsize=(15,10))
fig.suptitle( 'Распространение скрытного вируса с при r0={:.2f}'.format(VS.r0), fontsize=22)
gs = plt.GridSpec(2, 1, height_ratios=[2, 1.2]) 
ax1 = plt.subplot(gs[0])
ax2 = plt.subplot(gs[1])

ax1.plot( [VS.time[0],VS.time[-1]], [P*norm,P*norm], "-.", lw=2, color='k', label="Население Земли")
ax1.plot( VS.time, VS.Infected*norm, "-", lw=3, color='g', label="Инфицированные")
ax1.plot( VS.time, VS.Shedding*norm, "-", lw=3, color='r', label="Заразные")
ax1.plot( day, I*1e-9, "--", lw=2, color='k', label="Сигмоида при r={:.3f}".format(rs))
ax1.set_xlim( xlimits)
ax1.set_ylim( 0, 8)
#ax1.set_ylim( 0, 600)
ax1.set_ylabel("Миллиардов")
ax1.grid(True)
ax1.legend(loc=0)

ax2.plot( day, dI*1e-6, "--", lw=2, color='k')
ax2.plot( VS.time, VS.dI*1e-6, "-", lw=3, color='g', label="Заразившиеся/сутки")
ax2.set_xlim( xlimits)
ax2.set_ylim( 0, 500)
ax2.set_xlabel("День после первого случая")
ax2.set_ylabel("Млн случаев")
ax2.grid(True)
ax2.legend(loc=0)
plt.savefig( "./Graphs/figure_23_02bis.png")

if True:
    fig = plt.figure( figsize=(15,5))
    fig.suptitle( 'Заразность', fontsize=22)
    gs = plt.GridSpec(2, 1, height_ratios=[1,0.05]) 
    ax1 = plt.subplot(gs[0])
    ax1.plot( VS.time, VS.Rho, "-", lw=2, color='g', label="Заразность")
    ax1.set_xlim( 0, 40)
    ax1.set_ylim( 0, 1)
    ax1.set_xlabel("День после заражения")
    ax1.set_ylabel("Часть заражённых")
    ax1.grid(True)
    ax1.legend(loc=0)
    plt.savefig( "./Graphs/figure_23_02bisa.png")

if InteractiveModeOn: plt.show(True)
