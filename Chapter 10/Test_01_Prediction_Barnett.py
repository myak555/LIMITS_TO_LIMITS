from Utilities import *
from scipy.misc import imread
import matplotlib.cbook as cbook
import os

Ta = np.linspace( 1981.5,2029.5,49)
Wa = [1,4,10,21,27,32,40,51,73,98,115,151,191,272,328,402,482,567,757,1275,2072,3008,3891,4971,6538,9074,12158,13785,15144] 
dWa = np.array( Wa)
for i in range( len(dWa)-1,0,-1): dWa[i] -= dWa[i-1]
dWb = np.zeros( len( Ta))
for i in range( len( dWa)-1): dWb[i] = dWa[i]
N = [1840,1480,1270,1190,1090,990,840,780,722,683,640,620,560,510,470,440,390,340,310,280,260]
for i in range( len( dWa)-1, len(dWb)): dWb[i] = N[i-len( dWa)+1]-13

T0 = np.linspace( 1996, 2020, 25)
dQ0 = np.ones( 25) * 0.52
for i in range( 1, len(dQ0)): dQ0[i] = dQ0[i-1] * 0.88
dQ1 = np.zeros( len(Ta))
for i in range( len(dQ0)): dQ1[i] = dQ0[i]

Production = np.convolve( dWb, dQ1)

fig = plt.figure( figsize=(15,10))
img = imread( cbook.get_sample_data( os.getcwd() + '/Barnett_Forecast.jpg'))
plt.imshow(img, zorder=0, extent=[1986.5, 2037.2, -950, 6750],  interpolation='nearest', aspect='auto')

plt.plot( Ta, dWb*2, "-", lw=2, color="r", label="Ввод новых скважин N={:5.0f}".format( np.sum(dWb)))
plt.plot( T0, dQ0*10000, "-", lw=2, color="g", label="Спад добычи из одной скважины, {:2.0f}% добычи за 5 лет".format( 100*np.sum(dQ0[0:5])/np.sum(dQ0)))
plt.plot( Ta[1:], Production[0:48], "-", lw=3, color="b", label="Модель добычи (UT+Rice)")

plt.xlabel("Годы")
plt.xlim( 1987, 2038)
plt.ylim( -1000, 6800)
plt.title( 'Предсказание Университета Техаса и Университета Райса 2013 г')
plt.grid(True)
plt.legend(loc=1)
plt.savefig( "./Graphs/figure_10_01.png")
if InteractiveModeOn: plt.show(True)
