from Population import *

T_adult =        [1, 104, 315, 560, 736,1444,1471,1588]
P_adult =        [8,   8, 620,2200,2056, 122, 100,  27]
P_adult_error =  [0,   0,  30, 100, 100,   0,   0,   0]
T_litter =       [1, 104, 300, 600, 736,1444,1471,1588]
P_litter =       [0,  12, 800,   8,   0,   0,   0,   0]
P_litter_error = [0,   2, 200,   8,   0,   0,   0,   0]

fig = plt.figure( figsize=(15,10))
plt.errorbar( T_adult, P_adult, fmt='o', yerr=P_adult_error, color="r", label="Популяция взрослых")
plt.errorbar( T_litter, P_litter, fmt='o', yerr=P_litter_error, color="g", label="Популяция мышат")
plt.plot( T_adult, P_adult, "--", lw=1, color="r", label="Взрослые мыши (линейная интерполяция)")
plt.plot( T_litter, P_litter, "--", lw=1, color="g", label="Мышата (линейная интерполяция)")
#plt.plot( P.Solution_Time, P.Solution_L, "-", lw=1, color="b", label="Приплод")
#plt.plot( P.Solution_Time, P.Solution_P, "-", lw=1, color="r", label="Общее количество мышей")
plt.xlabel("Дни")
plt.xlim( 0, 1600)
plt.ylabel("Число мышей")
plt.ylim( -50, 2950)
plt.title( 'Популяция Вселенной-25 (по статье Кэлхуна)')
plt.grid(True)
plt.legend(loc=0)
plt.savefig( "./Graphs/figure_06_01.png")
fig.show()
