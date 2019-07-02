from Population import *

def GetTarProduction( BP_Year):
    Tar_Year = np.linspace(1967,2018,52)
    Tar_Production = np.array([1,15,29,34,42,52,51,47,46,56,
                               54,64,101,138,121,125,174,167,217,278,
                               296,330,334,343,349,364,377,397,428,443,
                               527,590,569,608,658,744,803,1020,965,1116,
                               1186,1199,1353,1468,1617,1779,1939,2159,2367,2417,
                               2669,3055])
    P2 = Hubbert( 2025, .15, .1, 4000.0).GetVector( BP_Year)
    for i,y in enumerate(BP_Year):
        if y < Tar_Year[0]:
            P2[i] = 0.0
            continue
        if y > Tar_Year[-1]: break
        P2[i] = Tar_Production[int(y-Tar_Year[0])]
    return P2
    
T = np.linspace(1850,2150,301)
H1 = Hubbert( 2000, .04145, .039, 1700).GetVector( T)
print( "{:g}\t{:.1f}\t{:.1f}".format(T[100], H1[100], np.sum(H1)))
H2 = Hubbert( 2015, .04812, .067, 4200).GetVector( T)
print( "{:g}\t{:.1f}\t{:.1f}".format( T[100], H2[100], np.sum(H2)))

rho_crude = 0.852
rho_gc = 0.720
rho_tar = 0.950

BP_Year, M = Load_Calibration( "./Data/01_BP_Oil_Liquids.csv", ["Year", "2019"])
BP_Year, rho = Load_Calibration( "./Data/03_BP_Oil_Density.csv", ["Year", "2019"])
V_tar = GetTarProduction( BP_Year) * 0.365 * 0.159
print(V_tar)

Y_NGPL = np.linspace(2000, 2018, 19)
NGPL_Percent_By_Volume = [9.2,9.4,9.7,9.2,9.2,9.3,9.3,9.4,9.5,10.2,10.7,11.3,11.5,11.6,12.1,12.3,12.9,13.3,13.9]
NGPL_Tonn = [236.39,241.70,247.66,244.12,256.76,262.13,265.91,268.28,272.80,
             284.47,302.88,321.06,336.36,339.49,361.54,377.92,396.08,409.76,435.97]
NGPL = [363.67,371.85,381.01,375.57,395.02,403.28,409.09,412.74,419.70,437.65,
        465.97,493.93,517.47,522.29,556.21,581.42,609.35,630.40,670.73]
V_less_NGPL = 1-np.array(NGPL_Percent_By_Volume)/100

M_tar = rho_tar * V_tar 
M_crude = ((1-rho_gc/rho) * M - (rho_tar-rho_gc) * V_tar) / (1-rho_gc/rho_crude) 
M_gc = M - M_crude - M_tar
for i in range( len( M_crude)):
    if M_crude[i] < M[i] - M_tar[i]: continue
    M_crude[i] = M[i] - M_tar[i]
    M_gc[i] = 0.0

j = np.argmax( M_crude)
print( "{:s}\t{:s}\t{:s}\t{:s}\t{:s}".format( "Year", "Tar", "Crude", "Con+NGPL", "NGPL(BP)"))
print( "mln tonn\tmln tonn\tmln tonn\tmln tonn\tmln tonn")
for i,y in enumerate(BP_Year):
    if y < 2000:
        print( "{:g}\t{:>8.1f}\t{:>8.1f}\t{:>8.1f}".format( y, M_tar[i],M_crude[i],M_gc[i]))
    else:
        if i==j:
            print( "{:g}\t{:>8.1f}\t{:>8.1f}\t{:>8.1f}\t{:>8.1f}\t{:>8.1f} <-- Peak Oil".format(
                y, M_tar[i],M_crude[i],M_gc[i],NGPL_Tonn[int(y)-2000],M_crude[i]+M_gc[i]-NGPL_Tonn[int(y)-2000]))
        else:
            print( "{:g}\t{:>8.1f}\t{:>8.1f}\t{:>8.1f}\t{:>8.1f}\t{:>8.1f}".format(
                y, M_tar[i],M_crude[i],M_gc[i],NGPL_Tonn[int(y)-2000],M_crude[i]+M_gc[i]-NGPL_Tonn[int(y)-2000]))
        
fig = plt.figure( figsize=(15,10))
fig.suptitle( 'Оценка добычи сырой нефти по отчётам "ВР" 2008-2019 гг', fontsize=22)
gs = plt.GridSpec(2, 1, height_ratios=[3, 1]) 
ax1 = plt.subplot(gs[0])
ax2 = plt.subplot(gs[1])

ax1.bar( BP_Year, M_crude, width=0.35, color='#B1FFBE', yerr=M_crude*0.05,
         label='Классическая сырая нефть (вычислено по данным "BP", 2019 г)')
ax1.bar( BP_Year, M_tar, bottom=M_crude, width=0.35, color='#6D6D6D',
         label="Битум (по данным Министерства Природных Ресурсов Канады, 2018 г)")
ax1.bar( BP_Year, M_gc, width=0.35, bottom=M_crude+M_tar, yerr=M*0.05, color='#FFD1D2',
         label="Конденсат и NGPL")
ax1.plot( Y_NGPL, NGPL_Tonn, "-", lw=5, color='r', alpha=0.5, label='Доля NGPL в добыче ("BP", 2019 г)')
ax1.plot( T, H1, "--", lw=2, color='k', label="Классическая сырая нефть (Хабберт, 1956, URR=1250 млрд баррелей)")
ax1.plot( T, H2, "-", lw=2, color='k', label="Нефть и жидкости (Лагеррер, 2013, URR=2200 млрд баррелей)")

ax1.set_xlim( 1965, 2020)
ax1.set_ylabel("Млн тонн в год")
ax1.set_ylim( 0, 8000)
ax1.grid(True)
ax1.set_title( "Абсолютные значения")
ax1.legend(loc=0)

ax2.plot( BP_Year, rho, "-", lw=2, color='g', label='Средняя плотность всех "жидкостей", г/см³')
ax2.plot( Y_NGPL, V_less_NGPL, "-", lw=2, color='r', label='Объёмная доля нефти, конденсата и битума (без NGPL)')
ax2.set_xlim( 1965, 2020)
ax2.set_xlabel("Годы")
ax2.grid(True)
ax2.legend(loc=0)
ax2.set_title( "Средняя плотность нефти и жидкостей")

plt.savefig( "./Graphs/figure_09_04.png")
if InteractiveModeOn: plt.show(True)
