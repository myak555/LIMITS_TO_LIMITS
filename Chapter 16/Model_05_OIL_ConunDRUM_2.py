from Oil_Shock_Model import *

Discovery_Projected = np.array( Discovery)
for i in range(215,len(Years)):
    Discovery_Projected[i] = Discovery_Projected[i-1] * 0.965

Developed_Resource = np.convolve( mc.Filter, Discovery_Projected)[0:len(Years)]
Reserves = np.zeros( len(Years))
Production = np.zeros( len(Years))
Reserves[0] = Developed_Resource[0]

for i in range(1,len(Years)):
    Production[i] = Reserves[i-1] * sm.GetRate( Years[i])
    Reserves[i] = Reserves[i-1] + Developed_Resource[i] - Production[i]

Production = Filter( Production, matrix = [1,1,2,1,1])

Cumulative_Discovery = Cumulative( Discovery_Projected)
Cumulative_Developed = Cumulative( Developed_Resource)
Cumulative_Produced = Cumulative( Production)

fig = plt.figure( figsize=(15,15))
fig.suptitle( 'Предсказание алгоритмом "Нефтяной шок" (П.Пукайт)', fontsize=22)
gs = plt.GridSpec(2, 1, height_ratios=[1.5, 1]) 
ax1 = plt.subplot(gs[0])
ax2 = plt.subplot(gs[1])

ax1.set_title("Открытия, освоение и добыча")
ax1.plot( Years, Discovery_Projected, "-", lw=2, color="b", label="Открытия, URR={:.0f} млрд т".format( np.sum(Discovery_Projected)/1000))
ax1.plot( Years, Developed_Resource, "-", lw=2, color="g", label="Освоенные ресурсы, URR={:.0f} млрд т".format( np.sum(Developed_Resource)/1000))
ax1.plot( Years, Production, "-", lw=2, color="r", label="Добыча (модель), URR={:.0f} млрд т".format( np.sum(Production)/1000))
ax1.errorbar( pYear, pOil, yerr=pOil*0.05, fmt=".", color="#FF5050", label="Добыча нефти и газового конденсата" )
ax1.set_xlim( 1850, 2150)
ax1.set_ylim( 0, 6000)
ax1.set_ylabel("млн тонн")
ax1.grid(True)
ax1.legend(loc=0)

ax2.set_title("Запасы")
ax2.plot( Years, Cumulative_Discovery/1000, "-", lw=2, color="b", label="Всего открыто (Лагеррер, 2014)")
ax2.plot( Years, Cumulative_Developed/1000, "-", lw=2, color="g", label="Всего освоено (модель)")
ax2.plot( Years, Cumulative_Produced/1000, "-", lw=2, color="r", label="Всего добыто (модель)")
ax2.plot( Years, Reserves/1000, "--", lw=2, color="k", label="Подтверждённые запасы (модель)")
ax2.set_xlim( 1850, 2150)
ax2.set_ylim( 0, 320)
ax2.set_xlabel("Год")
ax2.set_ylabel("млрд тонн")
ax2.grid(True)
ax2.legend(loc=2)

plt.savefig( "./Graphs/figure_16_05.png")
if InteractiveModeOn: plt.show(True)
