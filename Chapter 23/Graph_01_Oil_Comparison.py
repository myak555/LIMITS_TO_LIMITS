from Population import *

day = np.linspace(0,40,401)
r = 2
P = 7.8e9
t0 = np.log(P)/r
print("{:.3f}".format(t0))
S = Sigmoid(t0, r, 0, P).GetVector(day)
E = (r+1)**day
dS = Hubbert(t0, r, r, peak=P*r/4).GetVector(day)
dE = np.log(r+1)*(r+1)**day

r_aS = (S[5]/S[0])**(1/5)
r_aE = (E[5]/E[0])**(1/5)
print( r_aS, r_aE)
print("Sig\tExp")
for i in range(10):
    print("{:.2f}\t{:.2f}\t{:.2f}\t{:.2f}\t{:.3f}\t{:.3f}".format(S[i], E[i], dS[i], dE[i], dS[i]/S[i], dE[i]/E[i]))

fig = plt.figure( figsize=(15,10))
fig.suptitle( 'Распространение очень скрытного вируса, r={:.2f}'.format(r), fontsize=22)
gs = plt.GridSpec(2, 1, height_ratios=[2, 1.2]) 
ax1 = plt.subplot(gs[0])
ax2 = plt.subplot(gs[1])

ax1.plot( day, S*1e-9, "-", lw=3, color='g', label="Сигмоида Мальтуса")
ax1.plot( day, E*1e-9, "-", lw=3, color='r', label='Экспонента "наивного эпидемиолога"')
ax1.set_xlim( 0, 40)
ax1.set_ylim( 0, 8)
ax1.set_ylabel("Миллиардов инфицированных")
ax1.grid(True)
ax1.legend(loc=4)

ax2.plot( day, dS*1e-9, "-", lw=3, color='g')
ax2.plot( day, dE*1e-9, "-", lw=3, color='r')
ax2.set_xlim( 0, 40)
ax2.set_ylim( 0, 5)
ax2.set_xlabel("День с первого заражения")
ax2.set_ylabel("Заражений в сутки")
ax2.grid(True)

plt.savefig( "./Graphs/figure_23_01.png")
if InteractiveModeOn: plt.show(True)
