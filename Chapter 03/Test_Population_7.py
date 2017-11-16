from Population import *

#
# Solve numerically
#
T  = np.linspace(1890, 2200, 311)
P = Population( 1530.88, 35/1000, 1345, 10400, 1997)
P.Solve( T)

Prepare_Russian_Font()
fig = plt.figure( figsize=(10,18))
plt.plot( T, P.UN_High.GetVector(T), "-", lw=2, color="r", label=P.UN_High.Name)
plt.plot( T, P.UN_Medium.GetVector(T), "-", lw=2, color="y", label=P.UN_Medium.Name)
plt.plot( T, P.UN_Low.GetVector(T), "-", lw=2, color="g", label=P.UN_Low.Name)
plt.plot( P.Solution_Year, P.Solution_Total, ".", lw=1, color="y", label="Уравнение Ферхюльста (численное)")
plt.errorbar( P.Calibration_Year, P.Calibration_Total, yerr=P.Calibration_Total*0.02, fmt='o', color="b", label="Население (реальное)")
plt.xlabel("Годы")
plt.xlim( 1900, 2100)
plt.ylabel("миллионов человек")
plt.ylim( 0, 17000)
plt.title( "Население Земли (оценки ООН)")
plt.grid(True)
plt.legend(loc=0)
plt.savefig( ".\\Graphs\\figure_03_07.png")
fig.show()
