from Population import *

step = 0.1
P = 7.8e9
r = 1.1
day = np.linspace(0,200,2001)
Rho = Bathtub( x0=5.0, s0=2.0, x1 = 15.0, s1=0.8, left=0.0, middle=0.95, right=0.0).GetVector(day)
r0 = np.sum(Rho) * r * step
I = np.zeros(len(day))
I[0] = 1
dI = np.zeros(len(day))
dI[0] = 1
C = np.zeros(len(day))
for i in range(1,len(day)):
    # compute infected
    dI[i] = C[i]*r*step*(1-I[i-1]/P)
    I[i] = I[i-1] + dI[i]
    # update contageous
    for j in range( i, len(day)):
        C[j] += Rho[j-i] * dI[i-1]

t0 = np.log(P)/r
S = Sigmoid(t0, r, 0, P).GetVector(day)
dS = Hubbert(t0, r, r, peak=P*r/4).GetVector(day)

print("Time\tI\tC\tdI")
for i in range(0,len(day),10):
    print("{:.0f}\t{:.0f}\t{:.0f}\t{:.0f}".format(day[i], I[i], C[i], dI[i]))

xlimits =(0,200)

fig = plt.figure( figsize=(15,10))
fig.suptitle( 'Распространение скрытного вируса с при r0={:.2f}'.format(r0), fontsize=22)
gs = plt.GridSpec(2, 1, height_ratios=[2, 1.2]) 
ax1 = plt.subplot(gs[0])
ax2 = plt.subplot(gs[1])

ax1.plot( day, I*1e-9, "-", lw=3, color='g', label="Инфицированные")
ax1.plot( day, C*1e-9, "-", lw=3, color='r', label="Заразные")
ax1.plot( day, S*1e-9, "--", lw=3, color='g', label="Сигмоида из Примера 1, r0=14'000")
ax1.set_xlim( xlimits)
ax1.set_ylim( 0, 8)
ax1.set_ylabel("Миллиардов инфицированных")
ax1.grid(True)
ax1.legend(loc=4)

ax2.plot( day, dI*1e-6/step, "-", lw=3, color='g')
ax2.plot( day, dS*1e-6, "--", lw=3, color='g')
ax2.set_xlim( xlimits)
ax2.set_ylim( 0, 2100)
ax2.set_xlabel("День после первого случая")
ax2.set_ylabel("Млн случаев")
ax2.grid(True)

plt.savefig( "./Graphs/figure_23_03.png")
if InteractiveModeOn: plt.show(True)
