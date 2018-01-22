from Utilities import *

Ta,Pa = Load_Calibration( "Population_calibration.csv", "Year", "Population")
Ta,Da = Load_Calibration( "Population_calibration.csv", "Year", "Delta")

T  = np.linspace(1890, 2200, 311)
P = []

P0 = 1530.88
b = 22/1000
a = 9.5/1000

for t in T:
    p = P0 * np.exp( (b-a)*(t-1890))
    P += [p]
    print( "{0:4.0f} {1:7.1f}".format( t, p))

Prepare_Russian_Font()
fig = plt.figure( figsize=(15,10))
plt.plot( T, P, "-", lw=1, label="Население (экспонента)")
plt.errorbar( Ta, Pa, yerr=Da, fmt='o', label="Население (реальное)")
plt.xlabel("Годы")
plt.xlim( 1900, 2100)
plt.ylabel("миллионов человек")
plt.ylim( 0, 25000)
plt.title( "Население Земли (аналитическое решение)")
plt.grid(True)
plt.legend(loc=0)
plt.savefig( ".\\Graphs\\figure_03_01.png")
fig.show()
    
