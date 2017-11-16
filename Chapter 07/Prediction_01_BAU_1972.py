from Population import *
from scipy.misc import imread
import matplotlib.cbook as cbook
import os

#
# Феноменологическая интерполяция кривых модели BAU 1972
# "Limits to Growth", 1972, график 35 на странице 124
#
class Interpolation_BAU_1972:
    def __init__( self):
        self.Population_Function_1 = Sigmoid( 1970, 0.055, 1600, 5100)
        self.Population_Function_2 = Hubbert( 2050, 0.065, 0.078, 5200)
        self.Resources_Function_1 = Sigmoid( 2013, 0.052, 1200e3, 180e3)
        self.Resources_Function_2 = Hubbert( 2025, 0.150, 0.060, -180e3)
        self.Food_Function_1 = Bathtub( 1975, 0.08, 2027, 0.12, 540, 1230, 270)
        self.Food_Function_2 = Hubbert( 1932, 0.1, 0.1, 50)
        self.Food_Function_3 = Hubbert( 2012, 0.2, 0.2, 150)
        self.Food_Function_4 = Hubbert( 2065, 0.1, 0.1, -65)
        self.Industrial_Function_1 = Bathtub( 1970, 0.04, 2027, 0.09, 50, 1150, 30)
        self.Industrial_Function_2 = Hubbert( 2015, 0.12, 0.25, 430)
        self.Services_Function_1 = Bathtub( 1995, 0.035, 2035, 0.07, 120, 2600, 120)
        self.Services_Function_2 = Hubbert( 2016, 0.16, 0.2, 500)
        self.Services_Function_3 = Hubbert( 2080, 0.3, 0.3, 100)
        self.Pollution_Function_1 = Bathtub( 2012, 0.06, 2050, 0.15, 5e3, 310e3, 20e3)
        self.Pollution_Function_2 = Hubbert( 2033, 0.2, 0.2, 170e3)
        return
    def Solve( self, t):
        self.Time = t
        self.Population = self.Population_Function_1.GetVector( t)
        self.Population += self.Population_Function_2.GetVector( t)
        self.Resources = self.Resources_Function_1.GetVector( t)
        self.Resources += self.Resources_Function_2.GetVector( t)
        self.Food_PP = self.Food_Function_1.GetVector( t)
        self.Food_PP += self.Food_Function_2.GetVector( t)
        self.Food_PP += self.Food_Function_3.GetVector( t)
        self.Food_PP += self.Food_Function_4.GetVector( t)
        self.Industrial_PP = self.Industrial_Function_1.GetVector( t)
        self.Industrial_PP += self.Industrial_Function_2.GetVector( t)
        self.Services_PP = self.Services_Function_1.GetVector( t)
        self.Services_PP += self.Services_Function_2.GetVector( t)
        self.Services_PP += self.Services_Function_3.GetVector( t)
        self.Pollution = self.Pollution_Function_1.GetVector( t)
        self.Pollution += self.Pollution_Function_2.GetVector( t)
        return

T = np.linspace( 1900, 2100, 201)
BAU_1972 = Interpolation_BAU_1972()
BAU_1972.Solve(T)

Prepare_Russian_Font()
fig = plt.figure( figsize=(15,10))
img = imread( cbook.get_sample_data( os.getcwd() + '\\BAO_World3_1972_cropped_light.png'))
plt.imshow(img, zorder=0, extent=[1900, 2100, 0, 15100],  interpolation='nearest', aspect='auto')

plt.plot( BAU_1972.Time, BAU_1972.Population, "-", lw=3, color="b", label="Население (BAU-1972) [млн]")
plt.plot( BAU_1972.Time, BAU_1972.Resources/100*1.25, "-", lw=3, color="r", label="Ресурсы (BAU-1972) х0.01 [тут]")
plt.plot( BAU_1972.Time, BAU_1972.Pollution/100*1.25, "-", lw=3, color="y", label="Загрязнение (BAU-1972) х0.01 [тут]")
plt.plot( BAU_1972.Time, BAU_1972.Food_PP*5.7, "--", lw=2, color="g", label="Продовольствие (BAU-1972) х5 [1/душу/год]")
plt.plot( BAU_1972.Time, BAU_1972.Industrial_PP*5.7, "--", lw=2, color="k", label="Промтовары (BAU-1972) х5 [1/душу/год]")
plt.plot( BAU_1972.Time, BAU_1972.Services_PP*5.7, "--", lw=2, color="m", label="Услуги (BAU-1972) х5 [1/душу/год]")

plt.xlabel("Годы")
plt.xlim( 1900, 2100)
plt.ylabel("миллионов единиц")
plt.ylim( 0, 15000)
plt.title( 'Аппроксимация "Стандартного Сценария" World3 1972 г')
plt.grid(True)
plt.legend(loc=0)
plt.savefig( ".\\Graphs\\figure_07_01.png")
fig.show()
