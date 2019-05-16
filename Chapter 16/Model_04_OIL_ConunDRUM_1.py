from Oil_Shock_Model import *

Discovery_Projected = np.array( Discovery)
for i in range(215,len(Years)):
    Discovery_Projected[i] = Discovery_Projected[i-1] * 0.965

Developed_Resource = np.convolve( mc.Filter, Discovery_Projected)[0:len(Years)]

Cumulative_Discovery = Cumulative( Discovery_Projected)
Cumulative_Developed = Cumulative( Developed_Resource)

fig = plt.figure( figsize=(15,15))
fig.suptitle( 'Aлгоритм "Нефтяной шок" (П.Пукайт)', fontsize=22)
gs = plt.GridSpec(2, 1, height_ratios=[1.5, 1]) 
ax1 = plt.subplot(gs[0])
ax2 = plt.subplot(gs[1])

ax1.set_title("Обнаружение и подготовка месторождений нефти")
ax1.plot( Years[50:], mc.Filter[0:-50]*10000, "-.", lw=2, color="k", label="Фильтр х 10'000")
ax1.plot( Years, Discovery, "-", lw=2, color="b", label="Открытия (Лагеррер, 2014), URR={:.0f} млрд т".format( np.sum(Discovery)/1000))
ax1.plot( Years, Discovery_Projected, "--", lw=2, color="b", label="Будущие открытия, URR={:.0f} млрд т".format( np.sum(Discovery_Projected)/1000))
ax1.plot( Years, Developed_Resource, "-", lw=2, color="g", label="Освоенные ресурсы, URR={:.0f} млрд т".format( np.sum(Developed_Resource)/1000))
ax1.set_xlim( 1850, 2150)
ax1.set_ylim( 0, 6000)
ax1.set_ylabel("млн тонн")
ax1.grid(True)
ax1.legend(loc=0)

ax2.set_title("Запасы")
ax2.plot( Years, Cumulative_Discovery/1000, "-", lw=2, color="b", label="Всего открыто (Лагеррер, 2014)")
ax2.plot( Years, Cumulative_Developed/1000, "-", lw=2, color="g", label="Всего освоено (модель)")
ax2.set_xlim( 1850, 2150)
ax2.set_ylim( 0, 320)
ax2.set_xlabel("Год")
ax2.set_ylabel("млрд тонн")
ax2.grid(True)
ax2.legend(loc=0)

plt.savefig( "./Graphs/figure_16_04.png")
if InteractiveModeOn: plt.show(True)
