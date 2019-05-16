from Utilities import *

Periods = ["Мейендорф"]
Periods += ["Древнейший дриас"]
Periods += ["Бёллинг"]
Periods += ["Древний дриас"]
Periods += ["Аллерёд"]
Periods += ["Поздний дриас"]
Periods += ["Пребореальный"]

Period_Times = [-12500]
Period_Times += [-11850]
Period_Times += [-11720]
Period_Times += [-11590]
Period_Times += [-11400]
Period_Times += [-10730]
Period_Times += [-9640]

Y_Vostok, D_Vostok, Y2_Vostok, T_Vostok = Load_Calibration(
    "./Climate_Proxy/050_Vostok, Antarctica.txt",
    ["Age_Pub", "Proxy", "Age_Marine09", "Temp_Pub"],
    separator="\t")
Y_Vostok = 1950 - Y_Vostok
#T_Vostok += 55

Y_DomeC, D_DomeC, Y2_DomeC, T_DomeC = Load_Calibration(
    "./Climate_Proxy/025_Dome C, Antarctica.txt",
    ["Age_Pub", "Proxy", "Age_Marine09", "Temp_Pub"], separator="\t")
Y_DomeC = 1950 - Y_DomeC
T_DomeC += 25

Y_LD, D_LD = Load_Calibration(
    "./Climate_Proxy/Deuterium_Law_Dome.txt",
    ["Year", "Deuterium_excess"], separator=" ")

Y_LD2, Delta18O_LD = Load_Calibration(
    "./Climate_Proxy/D18O_Law_Dome.txt",
    ["age_CE", "d18O"], separator="\t")

Y_Greenland, d18O_Greenland, Y2_Greenland, T_Greenland = Load_Calibration(
    "./Climate_Proxy/067b_Agassiz & Renland.txt",
    ["Age_Pub", "Proxy", "Age_Marine09", "Temp_Pub"], separator="\t")
Y_Greenland = 1950 - Y_Greenland
T_Greenland -= 12

Y_GISP2, T_GISP2 = Load_Calibration(
    "./Climate_Proxy/GISP_2_Temperature.txt",
    ["Age", "Temperature"], separator=" ")
Y_GISP2 = 1950 - Y_GISP2*1000
#T_GISP2 += 32

Y_GISP2_A, d18O_GISP2 = Load_Calibration(
    "./Climate_Proxy/GISP_2.txt",
    ["Age", "d18O"], separator="\t")
Y_GISP2_A = 1950 - Y_GISP2_A

YearCorr, Law_Dome_d18O, Central_England_Tmean, Casey_Tmean = Load_Calibration(
    "./Climate_Proxy/LD_CA_Correlation.txt",
    ["Year", "LD_d18O", "CE_Year_Average", "Casey_Year_Average"],
    separator="\t")

Matrix = np.ones(11)
Central_England_T10 = Filter( Central_England_Tmean[:360], matrix=Matrix)
Casey_T10 = Filter( Casey_Tmean[6:61], matrix=Matrix)
Law_Dome_d18O_10 = Filter( Law_Dome_d18O[23:], matrix=Matrix)
Law_Dome_T10 = Law_Dome_d18O_10*2+35.5
limits = -20000, 2100

fig = plt.figure( figsize=(15,15))
gs = plt.GridSpec(3, 1, height_ratios=[1,1,1]) 
ax1 = plt.subplot(gs[0])
ax2 = plt.subplot(gs[1])
ax3 = plt.subplot(gs[2])

ax1.set_title('Ледовый керн скважин в Антарктике и Гренландии', fontsize=22)
ax1.errorbar( YearCorr[23:], Law_Dome_T10, xerr=3, yerr=2, alpha=0.2, fmt=".", color="m")
ax1.plot( YearCorr[23:], Law_Dome_T10, "-", lw=2, color="m", alpha=0.2, label='Law Dome')
ax1.errorbar( Y_Greenland, T_Greenland, xerr=20, yerr=3, alpha=0.2, fmt=".", color="g")
ax1.plot( Y_Greenland, T_Greenland, "-", lw=2, color="g", alpha=0.5, label='Agassiz/Renland')
ax1.errorbar( Y_DomeC, T_DomeC, xerr=10, yerr=2, alpha=0.2, fmt=".", color="b")
ax1.plot( Y_DomeC, T_DomeC, "-", lw=2, color="b", alpha=0.5, label='EPICA Dome C')
ax1.errorbar( Y_GISP2, T_GISP2, xerr=20, yerr=2, alpha=0.2, fmt=".", color="y")
ax1.plot( Y_GISP2, T_GISP2, "-", lw=2, color="y", alpha=0.5, label='GISP2')
ax1.errorbar( Y_Vostok, T_Vostok, xerr=20, yerr=2, alpha=0.2, fmt=".", color="r")
ax1.plot( Y_Vostok, T_Vostok, "-", lw=2, color="r", alpha=0.5, label='Восток')
#ax1.plot( YearCorr[6:61], Casey_T10, "-", lw=2, color="r", alpha=0.5, label='Casey')
ax1.set_xlim( limits)
ax1.set_ylim( -65, -5)
ax1.set_yticks( [-60,-50,-40,-30,-20,-10])
ax1.set_ylabel("[ºЦ]")
ax1.legend(loc=0)
ax1.grid(True)

ax2.errorbar( Y_DomeC, D_DomeC, xerr=10, yerr=5, alpha=0.2, fmt=".", color="b")
ax2.plot( Y_DomeC, D_DomeC, "-", lw=2, color="b", alpha=0.5, label='δD "EPICA Dome C"')
ax2.errorbar( Y_Vostok, D_Vostok, xerr=10, yerr=5, alpha=0.2, fmt=".", color="r")
ax2.plot( Y_Vostok, D_Vostok, "-", lw=2, color="r", alpha=0.5, label='δD "Восток"')
ax2.errorbar( Y_LD, D_LD-480, xerr=1, yerr=1, alpha=0.2, fmt="o", color="m", label='δD "Law Dome"-480ppm')
for i in range(len(Periods)):
    ax2.plot( [Period_Times[i],Period_Times[i]], [-480+10*i,-370], "--", lw=1, color="k")
    ax2.text( Period_Times[i]+10, -480+10*i, Periods[i], color="k", fontsize=12)
ax2.set_xlim( limits)
ax2.set_ylim( -490,-370)
ax2.set_ylabel("[ppmv]")
ax2.legend(loc=2)
ax2.grid(True)

ax3.errorbar( Y_LD2, Delta18O_LD, xerr=2, yerr=0.1, alpha=0.2, fmt="o", color="m")
ax3.plot( Y_LD2, Delta18O_LD, "-", lw=2, color="m", alpha=0.2, label='δ¹⁸О "Law Dome"')
#ax3.plot( YearCorr[23:], Law_Dome_d18O[23:], "--", lw=3, color="b", alpha=0.5, label='Law Dome 2')
ax3.errorbar( Y_Greenland, d18O_Greenland, xerr=2, yerr=0.1, alpha=0.2, fmt=".", color="g")
ax3.plot( Y_Greenland, d18O_Greenland, "-", lw=2, color="g", alpha=0.5, label='δ¹⁸О "Agassiz/Renland"')
ax3.errorbar( Y_GISP2_A, d18O_GISP2, xerr=10, yerr=0.1, alpha=0.2, fmt=".", color="y")
ax3.plot( Y_GISP2_A, d18O_GISP2, "-", lw=2, color="y", alpha=0.5, label='δ¹⁸О "GISP2"')
ax3.arrow( -8600, -18, -400, 0, width=0.5, color="k")
ax3.text( -9500, -17.5, "Климатический оптимум голоцена", color="k", fontsize=10)
ax3.arrow( -5400, -18, 400, 0, width=0.5, color="k")
ax3.arrow( -2750, -18, -400, 0, width=0.5, color="k")
ax3.text( -2700, -17.5, "Древний Египет", color="k", fontsize=10)
ax3.arrow( -400, -18, 400, 0, width=0.5, color="k")
ax3.arrow( -1495, -22, -400, 0, width=0.5, color="k")
ax3.text( -1720, -21.5, "Вавилон", color="k", fontsize=10)
ax3.arrow( -939, -22, 400, 0, width=0.5, color="k")
ax3.arrow( -400, -26, -400, 0, width=0.5, color="k")
ax3.text( -1120, -25.5, "Древняя Греция", color="k", fontsize=10)
ax3.arrow( 200, -26, 400, 0, width=0.5, color="k")
ax3.arrow( -353, -30, -400, 0, width=0.5, color="k")
ax3.text( -920, -29.5, "Древний Рим", color="k", fontsize=10)
ax3.arrow( 76, -30, 400, 0, width=0.5, color="k")
ax3.arrow( 1362, -34, -400, 0, width=0.5, color="k")
ax3.text( -2000, -33.5, "Священная Римская империя", color="k", fontsize=10)
ax3.arrow( 1406, -34, 400, 0, width=0.5, color="k")
ax3.arrow( -2452, -38, -400, 0, width=0.5, color="k")
ax3.text( -4000, -37.5, "Ранние империи Китая (?)", color="k", fontsize=10)
ax3.arrow( -1446, -38, 400, 0, width=0.5, color="k")
ax3.arrow( -646, -42, -400, 0, width=0.5, color="k")
ax3.text( -500, -41.5, "Империи Китая", color="k", fontsize=10)
ax3.arrow( 1546, -42, 400, 0, width=0.5, color="k")
ax3.set_ylabel("[ppmv]")
ax3.set_xlim( limits)
ax3.set_ylim( -45,-15)
ax3.legend(loc=0)
ax3.grid(True)
ax3.set_xlabel("год")

plt.savefig( "./Graphs/figure_17_07.png")
if InteractiveModeOn: plt.show(True)
