from Population import *

T = np.linspace(1850,2150,301)
H1 = Hubbert( 2000, .04145, .039, 1700).GetVector( T)
print( T[100], H1[100], np.sum(H1))
H2 = Hubbert( 2015, .04812, .067, 4200).GetVector( T)
print( T[100], H2[100], np.sum(H2))

rho_crude = 0.852
rho_gc = 0.720
rho_tar = 0.950

BP_Year, M = Load_Calibration( "./Data/01_BP_Oil_Liquids.csv", ["Year", "2018"])
BP_Year, rho = Load_Calibration( "./Data/03_BP_Oil_Density.csv", ["Year", "2018"])

P2 = Hubbert( 2022, .15, .1, 3.0).GetVector( BP_Year)
P2 += Hubbert( 1980, 1.2, 1.2, 0.1).GetVector( BP_Year)
P2 += Hubbert( 1984.5, 1, 1, 0.15).GetVector( BP_Year)
P2 += Hubbert( 1988, 1, .5, 0.20).GetVector( BP_Year)
P2 += Hubbert( 1998, .3, .8, 0.25).GetVector( BP_Year)
P2 += Hubbert( 2004, 1, 1, 0.25).GetVector( BP_Year)
P2 += Hubbert( 2007, 1, 1, 0.10).GetVector( BP_Year)
V_tar = P2 * 365 * 0.159

M_tar = rho_tar * V_tar 
M_crude = ((1-rho_gc/rho) * M - (rho_tar-rho_gc) * V_tar) / (1-rho_gc/rho_crude) 
M_gc = M - M_crude - M_tar
for i in range( len( M_crude)):
    if M_crude[i] < M[i] - M_tar[i]: continue
    M_crude[i] = M[i] - M_tar[i]
    M_gc[i] = 0.0

for i in range( len(BP_Year)):
    print( "{:g}\t{:>8.1f}\t{:>8.1f}\t{:>8.1f}".format( BP_Year[i], M_tar[i],M_crude[i],M_gc[i]))

fig = plt.figure( figsize=(15,10))
fig.suptitle( 'Оценка добычи сырой нефти по отчётам "ВР" 2008-2018 гг', fontsize=22)
gs = plt.GridSpec(2, 1, height_ratios=[3, 1]) 
ax1 = plt.subplot(gs[0])
ax2 = plt.subplot(gs[1])

ax1.bar( BP_Year, M_crude, width=0.35, color='#B1FFBE', yerr=M_crude*0.05, label='Классическая сырая нефть (вычислено по данным "BP", 2018 г)')
ax1.bar( BP_Year, M_tar, bottom=M_crude, width=0.35, color='#6D6D6D', label="Битум (по данным Министерства Природных Ресурсов Канады, 2017 г)")
ax1.bar( BP_Year, M_gc, width=0.35, bottom=M_crude+M_tar, yerr=M*0.05, color='#FFD1D2', label="Конденсат и NGPL")
ax1.plot( T, H1, "--", lw=2, color='k', label="Классическая сырая нефть (Хабберт, 1956, URR=1250 млрд баррелей)")
ax1.plot( T, H2, "-", lw=2, color='k', label="Нефть и жидкости (Лагеррер, 2013, URR=2200 млрд баррелей)")

ax1.set_xlim( 1965, 2020)
ax1.set_ylabel("Млн тонн в год")
ax1.set_ylim( 0, 8000)
ax1.grid(True)
ax1.set_title( "Абсолютные значения")
ax1.legend(loc=0)

ax2.plot( BP_Year, rho, "-", lw=2, color='g')
ax2.set_xlim( 1965, 2020)
ax2.set_xlabel("Годы")
ax2.set_ylabel("г/см³")
ax2.grid(True)
ax2.set_title( "Средняя плотность нефти и жидкостей")

plt.savefig( "./Graphs/figure_09_04.png")
if InteractiveModeOn: plt.show(True)
