from Oil_Shock_Model import *

k = 130
X1 = (Years - 1799)/k
Y1 = X1**6 * (1-np.exp(-1/X1**6)) 
dY1 = 6 * X1**5 - 6 * np.exp(-1/X1**6) * (X1**5 + 1/X1)
norm = 310e3 / Y1[-1] 
Y1 *= norm
Y1 = np.roll( Y1, 48)
Y1[:48] = 0
norm = 310e3 / np.sum( dY1) 
dY1 *= norm
dY1 = np.roll( dY1, 48)
dY1[:48] = 0
dY2 = Gompertz(2035,0.05,0.039,310000).GetVector(Years)
Y2 = GompertzIntegral(2035,0.05,0.039,310000).GetVector(Years)
dY3 = GenHubbert(1914,0.28,0.15,21700).GetVector(Years)

Discovery_Projected = np.array( Discovery)
for i in range(215,len(Years)):
    Discovery_Projected[i] = Discovery_Projected[i-1] * 0.965

Cumulative_Discovery = Cumulative( Discovery_Projected)
Cumulative_Y3 = Cumulative( dY3)

fig = plt.figure( figsize=(15,10))
fig.suptitle( 'Описание открытий кривой Хабберта и дисперсионной кривой Пукайта', fontsize=22)
gs = plt.GridSpec( 2, 1) 
ax1 = plt.subplot(gs[0])
ax2 = plt.subplot(gs[1])

ax1.set_title("Открытия в год")
ax1.plot( Years, Discovery_Projected, "-", lw=2, color="b", label="Открытия, URR={:.0f} млрд т".format( np.sum(Discovery_Projected)/1000))
ax1.plot( Years, dY1, "-", lw=2, color="g", label="Дисперсионная модель Пукайта, URR={:.0f} млрд т".format( np.sum(dY1)/1000))
ax1.plot( Years, dY2, "-", lw=2, color="m", label="Кривая Гомперца, URR={:.0f} млрд т".format(np.sum(dY2)/1000))
ax1.plot( Years, dY3, "-", lw=2, color="r", label="Хаббертиана, URR={:.0f} млрд т".format(np.sum(dY3)/1000))
ax1.set_xlim( 1850, 2200)
ax1.set_ylim( 0, 6000)
ax1.set_ylabel("млн тонн")
ax1.grid(True)
ax1.legend(loc=0)

ax2.set_title("Накопленные")
ax2.plot( Years, Cumulative_Discovery/1000, "-", lw=2, color="b", label="URR={:.0f} млрд т".format( Cumulative_Discovery[-1]/1000))
ax2.plot( Years, Y1/1000, "-", lw=2, color="g", label="URR={:.0f} млрд т".format( Y1[-1]/1000))
ax2.plot( Years, Y2/1000, "-", lw=2, color="m", label="URR={:.0f} млрд т".format( Y2[-1]/1000))
ax2.plot( Years, Cumulative_Y3/1000, "-", lw=2, color="r", label="URR={:.0f} млрд т".format( Cumulative_Y3[-1]/1000))
ax2.set_xlim( 1850, 2200)
ax2.set_ylim( -50, 350)
ax2.set_ylabel("млрд тонн")
ax2.grid(True)
ax2.legend(loc=0)
ax2.set_xlabel("Год")

plt.savefig( "./Graphs/figure_16_08.png")
fig.show()
