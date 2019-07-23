from Predictions import *
from scipy.misc import imread
import matplotlib.cbook as cbook
import os

T = np.linspace( 1900, 2100, 201)
BAU_1972 = Interpolation_BAU_1972()
BAU_1972.Solve(T)

fig = plt.figure( figsize=(15,10))
img = imread( cbook.get_sample_data( os.getcwd() + '/BAU_World3_1972_light_cropped.png'))
plt.imshow(img, zorder=0, extent=[1900, 2100, 0, 1.000],  interpolation='nearest', aspect='auto')

plt.plot( BAU_1972.Time, BAU_1972.Population_U, "-", lw=3, color="b", label="Население")
plt.plot( BAU_1972.Time, BAU_1972.Resources_U, "-", lw=3, color="k", label="Ресурсы")
plt.plot( BAU_1972.Time, BAU_1972.Pollution_U, "-", lw=3, color="y", label="Загрязнение")
plt.plot( BAU_1972.Time, BAU_1972.Food_PC_U, "--", lw=2, color="g", label="Продовольствие (на душу)")
plt.plot( BAU_1972.Time, BAU_1972.Industrial_PC_U, "--", lw=2, color="r", label="Промтовары (на душу)")
plt.plot( BAU_1972.Time, BAU_1972.Services_PC_U, "--", lw=2, color="m", label="Услуги (на душу)")
plt.plot( BAU_1972.Time, BAU_1972.Birth_Rate_U, "--", lw=1, color="g", label="Рождаемость")
plt.plot( BAU_1972.Time, BAU_1972.Death_Rate_U, "--", lw=1, color="r", label="Смертность")
plt.plot( [2000,2000], [0,1], "--", lw=2, color="k", label="2000 год")

plt.xlabel("Годы")
plt.xlim( 1900, 2100)
plt.ylabel("условных единиц")
plt.ylim( 0, 1)
plt.title( 'Аппроксимация "Стандартного Сценария" World3 1972 г')
plt.grid(True)
plt.legend(loc=0)
plt.savefig( "./Graphs/figure_07_01.png")
if InteractiveModeOn: plt.show(True)
