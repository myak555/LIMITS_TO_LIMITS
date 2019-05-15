from Resources import *
import matplotlib

matplotlib.rcParams['xtick.direction'] = 'out'
matplotlib.rcParams['ytick.direction'] = 'out'

Reserves = np.linspace( 0, 500, 501)

Deposit_1 = Gauss( 40, .0048, .00048, 1).GetVector(Reserves)
Deposit_2 = Gauss( 88, .0032, .00032, 1).GetVector(Reserves)
D_1 = np.array(Deposit_1)
D_2 = np.array(Deposit_2)
for i in range( len(D_1)-1): D_1[i+1] += D_1[i]
for i in range( len(D_2)-1): D_2[i+1] += D_2[i]
D_1 /= D_1[len(D_1)-1] / 100
D_2 /= D_2[len(D_2)-1] / 100

X, Y = np.meshgrid(Reserves, Reserves)
Z = np.array(X)
Bins = np.linspace( 0, 1000, 1001)
Counts = np.zeros( len(Bins))
for i in range( len(Deposit_1)):
    for j in range( len(Deposit_2)):
        Z[j,i] = Deposit_1[i] * Deposit_2[j]
        k = int( (Reserves[i]+Reserves[j]))
        Counts[k] += Z[j,i] 

Counts /= max( Counts)
D_12 = np.array(Counts)
for i in range( len(D_12)-1): D_12[i+1] += D_12[i]
D_12 /= D_12[len(D_12)-1] / 100

fig = plt.figure( figsize=(15,15))
plt.suptitle( "Распределение вероятностей двух месторождений, 2040 год")

gs = plt.GridSpec(2, 2, height_ratios=[1, 1], width_ratios=[1, 1]) 
ax1 = plt.subplot(gs[0])
ax2 = plt.subplot(gs[1])
ax3 = plt.subplot(gs[2])
ax4 = plt.subplot(gs[3])

ax1.plot([9.5, 47, 100], [10, 50, 90], "o", color="k")
ax1.plot([31, 54, 88], [10, 50, 90], "o", color="r")
ax1.plot(Reserves, Deposit_1*100, "--", color="r")
ax1.plot(Reserves, D_1, "-", lw = 2, color="r")
ax1.set_xlim( 0, 250)
ax1.set_ylim( 0, 100)
ax1.set_xlabel( "Большая Пупыра, млн т")
ax1.set_ylabel( "Вероятность (что менее)")
ax1.grid(True)
ax1.text(110, 85, "3P UR = 88 млн т")
ax1.text(60, 45, "2P UR = 54 млн т")
ax1.text(45, 5, "1P UR = 31 млн т")
ax1.arrow(9.5, 10, 21, 0, color="r", width=0.4)
ax1.arrow(47, 50, 5, 0, color="r", width=0.4)
ax1.arrow(100, 90, -10, 0, color="r", width=0.4)

ax2.plot([ 62, 117, 200], [10, 50, 90], "o", color="k")
ax2.plot([ 77, 105, 147], [10, 50, 90], "o", color="b")
ax2.plot(Reserves, Deposit_2*100, "--", color="b")
ax2.plot(Reserves, D_2, "-", lw = 2, color="b")
ax2.set_xlim( 0, 250)
ax2.set_ylim( 0, 100)
ax2.set_xlabel( "Данахервам, млн т")
ax2.set_ylabel( "Вероятность (что менее)")
ax2.grid(True)
ax2.text(40, 90, "3P UR = 147 млн т")
ax2.text(120, 45, "2P UR = 105 млн т")
ax2.text(80, 5, "1P UR = 77 млн т")
ax2.arrow(62, 10, 13, 0, color="b", width=0.4)
ax2.arrow(117, 50, -10, 0, color="b", width=0.4)
ax2.arrow(200, 90, -50, 0, color="b", width=0.4)

CS = ax3.contour(Y, X, Z*100, levels = [10, 50, 90])
CS.levels = ["10%","50%","90%"]
ax3.clabel(CS, inline=1, fontsize=10)
ax3.set_xlim( 0, 250)
ax3.set_ylim( 0, 250)
ax3.set_xlabel( "Данахервам, млн т")
ax3.set_ylabel( "Большая Пупыра, млн т")
ax3.text(5, 205, "Остаточные геологические (3P) = 113 млн т", color='g')
ax3.grid(True)

ax4.plot([ 113], [90], "o", color="g")
ax4.plot([ 123, 163, 214], [10, 50, 90], "o", color="k")
ax4.plot(Bins, Counts*100, "--", color="k")
ax4.plot(Bins, D_12, "-", lw = 2, color="k")
ax4.plot(Bins-40/0.5-16/0.75, D_12, "-.", lw = 2, color="g")
ax4.set_xlim( 0, 500)
ax4.set_ylim( 0, 100)
ax4.set_xlabel( "Оба месторождения, млн т")
ax4.set_ylabel( "Вероятность (что менее)")
ax4.grid(True)
ax4.text(230, 85, "3P UR = 214 млн т")
ax4.text(180, 45, "2P UR = 163 млн т")
ax4.text(130, 5, "1P UR = 123 млн т")

plt.savefig( "./Graphs/figure_13_06.png")
fig.show()
