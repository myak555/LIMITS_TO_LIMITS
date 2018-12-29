from Predictions import *

Z = np.linspace( 0, 75, 76)
T = np.zeros( len(Z))
for i in range( len(T)):
    if Z[i] < 13: T[i] = 288 - 6 * Z[i] 
    if 13 <= Z[i] and Z[i] < 22: T[i] = 210
    if 22 <= Z[i] and Z[i] < 43: T[i] = 210 + 3*(Z[i]-22)
    if 43 <= Z[i] and Z[i] < 54: T[i] = 273
    if 54 <= Z[i] : T[i] = 273 - 3*(Z[i]-54)
    
fig = plt.figure( figsize=(15,10))
plt.plot( T-273.15, Z, "-", lw=2, color='m')
plt.xlabel("Temperature [C]")
#plt.xlim( 1830, 2030)
plt.ylabel("Height [km]")
#plt.ylim( 300, 410)
plt.title( "Temperature in Atmosphere")
plt.grid(True)
#plt.legend(loc=0)
plt.savefig( ".\\Graphs\\figure_17_01_Platt.png")
fig.show()
