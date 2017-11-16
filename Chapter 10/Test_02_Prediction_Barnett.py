from Utilities import *
from scipy.misc import imread
import matplotlib.cbook as cbook
import os

T = np.linspace( 1993, 2016, 24)
dQ = np.array([30,38,54,
                 70,  78,  94, 112, 216,
                369, 605, 834,1041,1384,
               1973,3045,4441,4921,5159,
               5683,5742,5355,4943,4390,
               3890])

Tp = np.linspace( 1997, 2015, 19)
Price = np.array([2.49,2.09,2.27,
                  4.31,3.96,3.38,5.47,5.89,
                  8.69,6.73,6.97,8.86,3.94,
                  4.37,4.00,2.75,3.73,4.37,
                  2.62])
print( len(Price))

Ta = np.linspace( 1981.5,2029.5,49)
Wa = [1,4,10,21,27,32,40,51,73,98,115,151,191,272,328,402,482,567,757,1275,2072,3008,3891,4971,6538,9074,12158,13785,14886,17886,20886,23886] 
dWa = np.array( Wa)
for i in range( len(dWa)-1,0,-1): dWa[i] -= dWa[i-1]
dWb = np.zeros( len( Ta))
for i in range( len( dWa)-1): dWb[i] = dWa[i]
N = [650,650,650,650,650,650,650,650,650,650,640,620,560,510,470,440,390,340,310,280,260]
for i in range( len( dWa)-1, len(dWb)): dWb[i] = N[i-len( dWa)+1]

T0 = np.linspace( 1996, 2020, 15)
dQ0 = np.ones( 15) * 0.5
for i in range( 1, len(dQ0)): dQ0[i] = dQ0[i-1] * 0.75
dQ1 = np.zeros( len(Ta))
for i in range( len(dQ0)): dQ1[i] = dQ0[i]

Production = np.convolve( dWb, dQ1)

Prepare_Russian_Font()
fig = plt.figure( figsize=(15,10))
img = imread( cbook.get_sample_data( os.getcwd() + '\\Barnett_Forecast.jpg'))
plt.imshow(img, zorder=0, extent=[1986.5, 2037.2, -950, 6750],  interpolation='nearest', aspect='auto')

plt.errorbar( T, dQ, yerr=dQ*0.03, fmt='o', color="r", label="Реальная добыча")
plt.plot( Tp, Price*100, "-", lw=3, color="b", label="Центов за млн BTU")
plt.plot( [1995,2030], [3890,3890], "--", lw=2, color="r", label="Уровень добычи 2022 г")
plt.plot( [1995,2030], [400,400], "--", lw=2, color="b", label="400 центов за млн BTU")
#plt.plot( Ta, dWb*2, "-", lw=2, color="r")
#plt.plot( T0, dQ0*10000, "-", lw=2, color="g")
#plt.plot( Ta[1:], Production[0:48], "-", lw=3, color="b")

##plt.plot( T, dQ, "-", lw=2, color="k", label="Данные Железнодорожной Комиссии Техаса")
##plt.plot( Ta, dWb*2, "-", lw=2, color="r", label="Ввод новых скважин N={:5.0f}".format( np.sum(dWb)))
##plt.plot( T0, dQ0*10000, "-", lw=2, color="g", label="Спад добычи из одной скважины, {:2.0f}% добычи за 5 лет".format( 100*np.sum(dQ0[0:5])/np.sum(dQ0)))
##plt.plot( Ta[1:], Production[0:48], "-", lw=3, color="b", label="Предсказание (UT+Rice)")
#plt.plot( [2013.1, 2013.1], [0,6000], "-", lw=4, color="r")

plt.xlabel("Годы")
plt.xlim( 1987, 2038)
#plt.ylabel("миллионов единиц")
plt.ylim( -1000, 6800)
plt.title( 'Реальная добыча по данным Железнодорожной комиссии Техаса, 2016 г')
plt.grid(True)
plt.legend(loc=1)
plt.savefig( ".\\Graphs\\figure_10_02.png")
fig.show()
