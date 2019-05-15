from Predictions import *

def Rho(tau, Years, Year0):
    Time = Years - Year0
    tmp = np.exp( -Time/tau)
    for i in range( len(Years)):
        if Years[i]>=Year0: break
        tmp[i] = 0.0
    norm = np.sum( tmp)
    #print( tau, norm, 1/norm)
    return tmp/norm

Years = np.linspace( 1850,2150,301)
Fallow = Rho(3, Years, 1950)
Construction = Rho(8, Years, 1950)
Maturation = Rho(5, Years, 1950)
Depletion = Rho(10, Years, 1950)
Construction = np.convolve( Fallow, Construction)[100:100+len(Years)]
Maturation = np.convolve( Construction, Maturation)[100:100+len(Years)]
Depletion = np.convolve( Maturation, Depletion)[100:100+len(Years)]

print( "Fallow norm = {:.3f}".format( np.sum(Fallow))) 
print( "Construction norm = {:.3f}".format( np.sum(Depletion))) 
print( "Maturation norm = {:.3f}".format( np.sum(Maturation))) 
print( "Depletion norm = {:.3f}".format( np.sum(Depletion))) 

for i in range( 100,130):
    print("{:g}, {:.2f}, {:.2f}, {:.2f}, {:.2f}".format( Years[i], Fallow[i], Construction[i], Maturation[i], Depletion[i]))

fig = plt.figure( figsize=(15,10))
plt.plot( Years, Fallow, "-", lw=2, color="r", label="Принятие решения (характерное время ~ 3 года)")
plt.plot( Years, Construction, "-", lw=2, color="g", label="Строительство (характерное время ~ 8 лет)")
plt.plot( Years, Maturation, "-", lw=2, color="b", label="Разработка / бурение  (характерное время ~ 5 лет)")
plt.plot( Years, Depletion, "-", lw=2, color="k", label="Выработка ресурса (характерное время ~10 лет)")

plt.xlabel("Год (условный)")
plt.ylabel("Доля запасов [единиц]")
plt.xlim( 1930, 2100)
plt.title( 'Предсказание добычи цепочкой Маркова (П.Пукайт)')
plt.grid(True)
plt.legend(loc=0)
plt.savefig( "./Graphs/figure_16_03.png")
fig.show()
