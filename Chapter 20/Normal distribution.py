from Predictions import *

def findMinMax( data):
    found = False
    for i, y in enumerate(data):
        if not found and y >= 1.e-6:
            found = True
            first = i
            continue
        if found and y < 1.e-6:
            last = i
            break
    return first, last

income = np.linspace( 0, 150000, 150001)
soc1 = Gauss( 2456.159, 0.00001, 0.00001, 100/560.5).GetVector(income)
soc2 = Gauss( 1500, 0.0000001, 0.0000001, 100/4188.8).GetVector(income)
for i, y in enumerate(income):
    if y > 10: break
    soc1[i] = 0
    soc2[i] = 0
gdp1 = np.sum(soc1*income*12) / 1e6
gdp2 = np.sum(soc2*income*12) / 1e6
first1, last1 = findMinMax( soc1)
first2, last2 = findMinMax( soc2)
ss1 = 0
for i, y in enumerate(income):
    if y > 30: break
    ss1 += soc2[i]
ss3 = 0
for i, y in enumerate(income):
    if y > 90: break
    ss3 += soc2[i]

print("Страна 1:")
print("   Население: {:.1f}".format(np.sum(soc1)))
print("   ВВП: {:.1f}".format(gdp1))
print("   ВВП/душу: {:.0f}".format(gdp1*1e6/np.sum(soc1)))
print("   Беднейший в популяции: {:.0f}".format(income[first1]))
print("   Богатейший в популяции: {:.0f}".format(income[last1]))
print("Страна 2:")
print("   Население: {:.1f}".format(np.sum(soc2)))
print("   ВВП: {:.1f}".format(gdp2))
print("   ВВП/душу: {:.0f}".format(gdp2*1e6/np.sum(soc2)))
print("   Беднейший в популяции: {:.0f}".format(income[first2]))
print("   Богатейший в популяции: {:.0f}".format(income[last2]))
print("   На потреблении 1У.Е. в день: {:.2f}".format(ss1))
print("   На потреблении 3У.Е. в день: {:.2f}".format(ss3))

fig = plt.figure( figsize=(15,8))
fig.suptitle('Две страны с нормальным распределением ресурсов', fontsize=25)
gs = plt.GridSpec(1, 1) 
ax1 = plt.subplot(gs[0])
ax1.plot( income[first1:last1+1], soc1[first1:last1+1], "-", lw=2, color= "r")
ax1.plot( income[first2:last2+1], soc2[first2:last2+1], "-", lw=2, color= "g")
ax1.set_xlim( 0, 12000)
#ax1.set_ylim( 0, 0.25)
ax1.grid(True)
ax1.set_ylabel("Часть популяции [млн]")
ax1.set_xlabel("Месячное потребление, [У.Е.]")
plt.savefig( "./Graphs/ND.png")
plt.show()
