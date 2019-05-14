from Utilities import *
from scipy.misc import imread
import matplotlib.cbook as cbook
import os

T = np.linspace( 1995, 2016, 22)
dQ = np.array([86.2,86.6,88.8,91.7,92.2])

dQ = np.array( [67983,69836,72085,73405,72221,
                74934,75174,74962,77676,81012,
                81908,82519,82334,82894,81222,
                83251,84026,86183,86606,88826,
                91704,92150])
dC = np.array( [70332,71792,73856,74484,76264,
                76946,77864,78777,80549,83350,
                84678,85777,87161,86578,85691,
                88722,89729,90675,92114,93025,
                95003,96558])
EIA_All = np.array( [70306.4,71987.5,74222.8,75682.0,74839.3,
                 77729.1,77673.2,77103.7,79623.4,83450.1,
                 85114.6,85198.4,85248.2,86637.5,85847.3,
                 88280.0,88799.3,90780.9,91293.7,93812.5,
                 96744.1,97175.3])
EIA_OnC = np.array( [62430.3,63818.3,65802.4,67032.8,65967.0,
                     68526.7,68131.9,67290.2,69460.2,72595.2,
                     73865.6,73476.2,73175.2,74048.0,72869.2,
                     74573.5,74647.2,76060.1,76190.0,78070.0,
                     80454.7,80578.1])

fig = plt.figure( figsize=(15,10))
img = imread( cbook.get_sample_data( os.getcwd() + '/EIA_Prognosis.png'))
plt.imshow(img, zorder=0, extent=[1991.2, 2036, 51.9, 125],  interpolation='nearest', aspect='auto')

plt.errorbar( T, EIA_All/1000, yerr=EIA_All*0.00003, fmt='o', color="b", label="Все жидкости (EIA-2017)")
plt.errorbar( T, EIA_OnC/1000, yerr=EIA_All*0.00003, fmt='o', color="k", label="Нефть и лицензионный конденсат (EIA-2017)")

plt.xlim( 1985, 2040)
plt.ylim( 45, 130)
plt.title( 'Прогнозы EIA, 2000-2011 гг')
#plt.grid(True)
plt.legend(loc=4)
plt.savefig( "./Graphs/figure_09_19.png")
fig.show()
