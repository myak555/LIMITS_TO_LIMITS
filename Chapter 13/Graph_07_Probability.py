from Resources import *
import matplotlib

matplotlib.rcParams['xtick.direction'] = 'out'
matplotlib.rcParams['ytick.direction'] = 'out'

Reserves = np.linspace( 0, 500, 501)

Deposit_1 = Gauss( 48, .5, .002, 1).GetVector(Reserves)
Deposit_2 = Gauss( 92, .1, .001, 1).GetVector(Reserves)
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
plt.suptitle( "Распределение вероятностей двух месторождений, 2060 год")

gs = plt.GridSpec(2, 2, height_ratios=[1, 1], width_ratios=[1, 1]) 
ax1 = plt.subplot(gs[0])
ax2 = plt.subplot(gs[1])
ax3 = plt.subplot(gs[2])
ax4 = plt.subplot(gs[3])

ax1.plot([9.5, 47, 100], [10, 50, 90], "o", color="k")
ax1.plot([31, 54, 88], [10, 50, 90], "o", color="k")
ax1.plot([48, 57, 73], [10, 50, 90], "o", color="r")
ax1.plot(Reserves, Deposit_1*100, "--", color="r")
ax1.plot(Reserves, D_1, "-", lw = 2, color="r")
ax1.set_xlim( 0, 250)
ax1.set_ylim( 0, 100)
ax1.set_xlabel( "Большая Пупыра, млн т")
ax1.set_ylabel( "Вероятность (что менее)")
ax1.grid(True)
ax1.text(110, 85, "3P UR = 73 млн т")
ax1.text(60, 45, "2P UR = 57 млн т")
ax1.text(55, 5, "1P UR = 48 млн т")
ax1.arrow(9.5, 10, 36, 0, color="r", width=0.4)
ax1.arrow(47, 50, 5, 0, color="r", width=0.4)
ax1.arrow(100, 90, -23, 0, color="r", width=0.4)

ax2.plot([ 62, 117, 200], [10, 50, 90], "o", color="k")
ax2.plot([ 77, 105, 147], [10, 50, 90], "o", color="k")
ax2.plot([ 92, 105, 127], [10, 50, 90], "o", color="b")
ax2.plot(Reserves, Deposit_2*100, "--", color="b")
ax2.plot(Reserves, D_2, "-", lw = 2, color="b")
ax2.set_xlim( 0, 250)
ax2.set_ylim( 0, 100)
ax2.set_xlabel( "Данахервам, млн т")
ax2.set_ylabel( "Вероятность (что менее)")
ax2.grid(True)
ax2.text(10, 90, "3P UR = 127 млн т")
ax2.text(130, 45, "2P UR = 105 млн т")
ax2.text(110, 5, "1P UR = 92 млн т")
ax2.arrow(62, 10, 27, 0, color="b", width=0.4)
ax2.arrow(117, 50, -10, 0, color="b", width=0.4)
ax2.arrow(200, 90, -70, 0, color="b", width=0.4)

CS = ax3.contour(Y, X, Z*100, levels = [10, 50, 90])
CS.levels = ["10%","50%","90%"]
ax3.clabel(CS, inline=1, fontsize=10)
ax3.set_xlim( 0, 250)
ax3.set_ylim( 0, 250)
ax3.set_xlabel( "Данахервам, млн т")
ax3.set_ylabel( "Большая Пупыра, млн т")
ax3.text(5, 205, "Остаточные геологические (3P) = 32 млн т", color='g')
ax3.text(5, 185, "Остаточные извлекаемые (3P) = 1 млн т", color='g')
ax3.grid(True)

ax4.plot([ 32], [90], "o", color="g")
ax4.plot([ 147, 165, 191], [10, 50, 90], "o", color="k")
ax4.plot(Bins, Counts*100, "--", color="k")
ax4.plot(Bins, D_12, "-", lw = 2, color="k")
ax4.plot(Bins-60/0.57-45/0.83, D_12, "-.", lw = 2, color="g")
ax4.set_xlim( 0, 500)
ax4.set_ylim( 0, 100)
ax4.set_xlabel( "Оба месторождения, млн т")
ax4.set_ylabel( "Вероятность (что менее)")
ax4.grid(True)
ax4.text(230, 85, "3P UR = 191 млн т")
ax4.text(200, 45, "2P UR = 165 млн т")
ax4.text(160, 5, "1P UR = 147 млн т")

plt.savefig( "./Graphs/figure_13_07.png")
if InteractiveModeOn: plt.show(True)
