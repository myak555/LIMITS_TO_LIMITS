from Resources import *
from scipy.misc import imread
import matplotlib.cbook as cbook
import os

Year_Energy, Coal_Energy = Load_Calibration(
            "./Data/06_BP_Coal.csv",["Year", "2019"])
Year_Energy = Year_Energy[16:] 
Coal_Energy = Coal_Energy[16:]
dumm, Oil_Energy = Load_Calibration(
            "./Data/01_BP_Oil_Liquids.csv",["Year","2019"])
Oil_Energy = Oil_Energy[16:]
dumm, Gas_Energy = Load_Calibration(
            "./Data/04_BP_Gas.csv",["Year","2019"])
Gas_Energy = Gas_Energy[16:]
dumm, Hydro_Energy = Load_Calibration(
            "./Data/09_BP_Hydro.csv",["Year","2019"])
Hydro_Energy = Hydro_Energy[16:]
dumm, Nuclear_Energy = Load_Calibration(
            "./Data/08_BP_Nuclear.csv",["Year","2019"])
Nuclear_Energy = Nuclear_Energy[16:]
dumm, Renewable_Energy = Load_Calibration(
            "./Data/10_BP_Renewable.csv",["Year","2019"])
Renewable_Energy = Renewable_Energy[16:]

RAS_Biomass_Functions = Linear_Combo()
RAS_Biomass_Functions.Wavelets += [Sigmoid( x0=2003, s0=0.04344, left=235.000, right=2200)]
RAS_Biomass_Functions.Wavelets += [Hubbert( x0=2003, s0=0.09652, s1=0.10832, peak=-217)]
RAS_Biomass_Functions.Wavelets += [Hubbert( x0=1910, s0=0.13509, s1=0.08774, peak=50)]
RAS_Biomass_Functions.Wavelets += [Hubbert( x0=1992, s0=0.10000, s1=0.10000, peak=20)]
RAS_Biomass_Functions.Wavelets += [Hubbert( x0=2015, s0=0.07107, s1=0.38742, peak=50)]
RAS_Biomass_Functions.Wavelets += [Hubbert( x0=2040, s0=0.25419, s1=0.18530, peak=50, shift=-50)]

T = np.linspace( 1860, 2040, 181)
Biomass = RAS_Biomass_Functions.GetVector(T)
Coal_and_Biomass = Coal_Energy + Biomass[122:-21]  
Oil_and_Coal = Oil_Energy + Coal_and_Biomass  
Gas_and_Oil = Gas_Energy + Oil_and_Coal  
Total1 = Gas_and_Oil + (Nuclear_Energy + Hydro_Energy + Renewable_Energy)*0.38  
Total2 = Gas_and_Oil + (Nuclear_Energy + Hydro_Energy + Renewable_Energy)  

fig = plt.figure( figsize=(15,10))
img = imread( cbook.get_sample_data( os.getcwd() + '/RAS_Energy_Projection.jpg'))
plt.imshow(img, zorder=0, extent=[1849.7, 2051.85, -5.80, 23.3 ],  interpolation='nearest', aspect='auto')
plt.plot( [1860, 1860], [-1, 19], "--", lw=1, color="m")
plt.plot( [2040, 2040], [-1, 19], "--", lw=1, color="m")
plt.plot( [1800, 2100], [0, 0], "--", lw=1, color="m")
plt.plot( [1800, 2100], [18, 18], "--", lw=1, color="m")

plt.plot( T, Biomass/1000, "--", lw=1, color="k", label="Биомасса и мусор (РАН, с графика)")
plt.errorbar( Year_Energy, Coal_and_Biomass/1000, yerr=Coal_and_Biomass/20000, fmt=".", color="k",
              label="Биомасса (РАН) + Уголь (ВР, 2019)")
plt.errorbar( Year_Energy, Oil_and_Coal/1000, yerr=Oil_and_Coal/20000, fmt=".", color="g",
              label=' + Нефть, битум, конденсат и ШФЛУ (ВР, 2019)')
plt.errorbar( Year_Energy, Gas_and_Oil/1000, yerr=Gas_and_Oil/20000, fmt=".", color="b",
              label=' + Природный газ (ВР, 2019)')
plt.errorbar( Year_Energy, Total2/1000, yerr=Total2/20000, fmt=".", color="m",
              label='Всего энергии (ВР, 2019 и Биомасса РАН, 2014)')
plt.plot( Year_Energy, Total1/1000, "--", lw=3, color="y", label="Общая энергия без учёта КПД")
plt.plot( [2018,2018], [0,20], "-.", lw=1, color="k")

plt.xlabel("Годы")
plt.xlim( 1850, 2050)
plt.ylabel("миллиарды тонн")
plt.ylim( -5, 22)
plt.title( 'Энергетическое предсказание РАН против статистики "ВР"')
plt.grid(True)
plt.legend(loc=2)
plt.savefig( "./Graphs/figure_09_20.png")
if InteractiveModeOn: plt.show(True)
