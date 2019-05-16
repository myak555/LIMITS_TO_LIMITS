from Predictions import *

Res = Resources()
Pop = Population()
Randers_2012 = Interpolation_BAU_2012()

Year = np.linspace( 1800, 2300, 501)
All_1P = Bathtub( 1965, s0=0.2, x1 = 2057, s1=0.10, middle=12638).GetVector(Year)
All_2P = Bathtub( 1965, s0=0.2, x1 = 2080, s1=0.07, middle=14785).GetVector(Year)
All_3P = Bathtub( 1965, s0=0.2, x1 = 2148, s1=0.06, middle=25720).GetVector(Year)

for i in range(len(Year)):
    j = int(Year[i] - Res.Year[0])
    if j < 0: continue
    if j >= len( Res.Year): break
    All_1P[i] = Res.Total[j]
    All_2P[i] = Res.Total[j]
    All_3P[i] = Res.Total[j]

population_low = Pop.UN_Low.GetVector(Year)
population_medium = Pop.UN_Medium.GetVector(Year)
population_high = Pop.UN_High.GetVector(Year)

for i in range( 2018, 2025):
    j = int(i - Year[0])
    All_1P[j] = population_low[j] * 1.556

for i in range( 2018, 2037):
    j = int(i - Year[0])
    All_2P[j] = population_medium[j] * 1.556

for i in range( 2018, 2095):
    j = int(i - Year[0])
    All_3P[j] = population_high[j] * 1.556

PP_1P = 1000.0 * All_1P / population_low  
PP_2P = 1000.0 * All_2P / population_medium  
PP_3P = 1000.0 * All_3P / population_high

Randers_2012.Solve( Year)
Randers_2012.Correct_To_Actual( 1830, 2012)
Randers_2012.TotalC = Randers_2012.Coal + Randers_2012.Oil + Randers_2012.Gas 
 
fig = plt.figure( figsize=(15,15))
fig.suptitle( 'Модель "Поддержание добычи на душу населения"', fontsize=22)
gs = plt.GridSpec(2, 1) 
ax1 = plt.subplot(gs[0])
ax2 = plt.subplot(gs[1])

ax1.set_title("Годовая добыча")
ax1.plot( Year, All_1P, "--", lw=2, color='k', label="Всё ископаемое топливо (1P), URR={:.1f} млрд т".format(np.sum(All_1P)/1000))
ax1.plot( Year, All_2P, "-", lw=2, color='k', label="Всё ископаемое топливо (2P), URR={:.1f} млрд т".format(np.sum(All_2P)/1000))
ax1.plot( Year, All_3P, "-.", lw=2, color='k', label="Всё ископаемое топливо (3P), URR={:.1f} млрд т".format(np.sum(All_3P)/1000))
ax1.plot( Year, Randers_2012.TotalC, "-", lw=2, color='r', label="Модель NewWorld-2012, URR={:.1f} млрд т".format(np.sum(Randers_2012.TotalC)/1000))
ax1.plot( [2036, 2036], [0, 15000], "--", lw=1, color='b')
ax1.set_xlim( 1850, 2150)
ax1.set_ylim( 0, 25000)
ax1.set_ylabel("Млн toe")
ax1.text(2005, 2500, "2036 год")
ax1.grid(True)
ax1.legend(loc=2)

ax2.set_title("Добыча на душу населения")
ax2.plot( Year, PP_1P, "--", lw=2, color='k', label="1P/UN_Low (пик={:.0f} кг)".format(np.max(PP_1P)))
ax2.plot( Year, PP_2P, "-", lw=2, color='k', label="2P/UN_Medium (пик={:.0f} кг)".format(np.max(PP_2P)))
ax2.plot( Year, PP_3P, "-.", lw=2, color='k', label="3P/UN_High (пик={:.0f} кг)".format(np.max(PP_3P)))
ax2.plot( [1973, 1973], [0, 1500], "--", lw=1, color='b')
ax2.plot( [1979, 1979], [0, 1500], "--", lw=1, color='b')
ax2.text(1870, 1250, "Нефтяной кризис 1973-1979 гг")
ax2.set_xlim( 1850, 2150)
ax2.set_ylim( 0, 2000)
ax2.set_xlabel("Годы")
ax2.set_ylabel("кг нефтяного эквивалента в год")
#ax1.text(2060, 16000, "2048 год")
ax2 .grid(True)
ax2.legend(loc=2)

plt.savefig( "./Graphs/figure_15_02.png")
if InteractiveModeOn: plt.show(True)
