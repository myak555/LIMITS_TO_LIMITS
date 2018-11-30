from Population import *
import scipy.special as spec

Size = np.linspace( -3, 5, 101)
Size = 10**Size
Average = 20
Sigma = 1.7
P1 = 1/(1+Size/Average)
P2 = (1-spec.erf((np.log(Size)-np.log(Average))/2**0.5/Sigma))/2

fig = plt.figure( figsize=(15,10))
plt.errorbar( Size, P1, fmt="o", color="k", label="1/(1+S/Sa)")
plt.plot( Size, P2, "-", lw=3, color="r", label="Логнормальное распределение")
plt.plot( [Average, Average], [0,1], "--", lw=2, color="r")

plt.xlabel("Запасы [млн баррелей]")
plt.xscale("log", nonposx='clip')
plt.ylabel("Вероятность существования")
plt.xlim( 1e-3, 1e5)
plt.title( 'Распределение месторождений нефти (П.Пукайт)')
plt.grid(True)
plt.legend(loc=3)
plt.savefig( ".\\Graphs\\figure_16_02.png")
fig.show()
