from Population import *
from Predictions import *
from scipy.misc import imread
import matplotlib.cbook as cbook
import os

T = np.linspace( 1650, 2050, 401)
P0 = Population()
P1 = Linear_Combo()
P1.Wavelets += [Sigmoid( x0=1980.000, s0=0.01236, left=0.486, right=4.900)]
P1.Wavelets += [Hubbert( x0=2030.000, s0=0.05641, s1=0.05000, peak=5.100)]
P1.Wavelets += [Hubbert( x0=2000.000, s0=1.00000, s1=0.05000, peak=0.337)]
P1.Wavelets += [Hubbert( x0=1850.000, s0=0.50000, s1=0.50000, peak=-0.100)]
Pop1 = P1.GetVector(T)

fig = plt.figure( figsize=(15,10))
img = imread( cbook.get_sample_data( os.getcwd() + '/Carr-Sounders_Wilcox_UN_1968.png'))
plt.imshow(img, zorder=0, extent=[1630.8, 2015.1, -2.950, 7.450],  interpolation='nearest', aspect='auto')

plt.errorbar( P0.Calibration_Year, P0.Calibration_Total/1000, yerr=P0.Calibration_Yerr/1000, fmt=".", color="b", label="Реальная популяция (ООН, 2015)")
plt.plot( T, Pop1, "--", lw=2, color="r", label="Аппроксимация 1972 г")
plt.xlabel("Год")
plt.xlim( 1640, 2050)
plt.ylabel("млрд")
plt.ylim( -3, 10)
plt.title( 'Данные о популяции Земли в "Пределах роста" 1972 г')
plt.grid(True)
plt.legend(loc=0)
plt.savefig( "./Graphs/figure_19_09.png")
if InteractiveModeOn: plt.show(True)
