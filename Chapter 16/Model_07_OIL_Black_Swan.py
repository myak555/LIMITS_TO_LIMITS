from Oil_Shock_Model import *

Discovery_Projected = np.array( Discovery)
Discovery_Projected_2 = np.array( Discovery)
for i in range(215,len(Years)):
    Discovery_Projected[i] = Discovery_Projected[i-1] * 0.965
    Discovery_Projected_2[i] = Discovery_Projected_2[i-1] * 0.965
for i in range(215,len(Years)):
    if 2019 <= Years[i] and Years[i] <= 2023: Discovery_Projected_2[i] = 5000 

Developed_Resource = np.convolve( mc.Filter, Discovery_Projected)[0:len(Years)]
Developed_Resource_2 = np.convolve( mc.Filter, Discovery_Projected_2)[0:len(Years)]
Reserves = np.zeros( len(Years))
Reserves_2 = np.zeros( len(Years))
Production = np.zeros( len(Years))
Production_2 = np.zeros( len(Years))
Reserves[0] = Developed_Resource[0]
Reserves_2[0] = Developed_Resource_2[0]

for i in range(1,len(Years)):
    Production[i] = Reserves[i-1] * sm.GetRate( Years[i])
    Reserves[i] = Reserves[i-1] + Developed_Resource[i] - Production[i]
    Production_2[i] = Reserves_2[i-1] * sm.GetRate( Years[i])
    Reserves_2[i] = Reserves_2[i-1] + Developed_Resource_2[i] - Production_2[i]

Production = Filter( Production, matrix = [1,1,2,1,1])
Production_2 = Filter( Production_2, matrix = [1,1,2,1,1])

Cumulative_Discovery = Cumulative( Discovery_Projected)
Cumulative_Developed = Cumulative( Developed_Resource)
Cumulative_Produced = Cumulative( Production)

fig = plt.figure( figsize=(15,10))
fig.suptitle( 'Прилёт "Чёрного лебедя" в модели "Нефтяной шок" (П.Пукайт)', fontsize=22)
gs = plt.GridSpec(1, 1) 
ax1 = plt.subplot(gs[0])

ax1.set_title("Открытия, освоение и добыча")
ax1.plot( Years, Discovery_Projected, "-", lw=2, color="b", label="Открытия, URR={:.0f} млрд т".format( np.sum(Discovery_Projected)/1000))
ax1.plot( Years, Discovery_Projected_2, "--", lw=2, color="b", label="Открытия (Чёрный лебедь), URR={:.0f} млрд т".format( np.sum(Discovery_Projected_2)/1000))
ax1.plot( Years, Production, "-", lw=2, color="r", label="Добыча, URR={:.0f} млрд т".format( np.sum(Production)/1000))
ax1.plot( Years, Production_2, "--", lw=2, color="r", label="Добыча (Чёрный лебедь), URR={:.0f} млрд т".format( np.sum(Production_2)/1000))
ax1.errorbar( pYear, pOil, yerr=pOil*0.05, fmt=".", color="#FF5050")
ax1.set_xlim( 1900, 2200)
ax1.set_ylim( 0, 6000)
ax1.set_ylabel("млн тонн")
ax1.grid(True)
ax1.legend(loc=0)
ax1.set_xlabel("Год")

plt.savefig( "./Graphs/figure_16_07.png")
fig.show()
