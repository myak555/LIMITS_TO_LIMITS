from Resources import *
import matplotlib

matplotlib.rcParams['xtick.direction'] = 'out'
matplotlib.rcParams['ytick.direction'] = 'out'

Reserves = np.linspace( 0, 800, 801)

Res_1 = Gauss( 250, 1, .00006, 1).GetVector(Reserves)
Res_2 = Gauss( 215, 1, .000022, 1).GetVector(Reserves)
D_1 = np.array(Res_1)
D_2 = np.array(Res_2)
for i in range( len(D_1)-1): D_1[i+1] += D_1[i]
for i in range( len(D_2)-1): D_2[i+1] += D_2[i]
D_1 /= D_1[len(D_1)-1] / 100
D_2 /= D_2[len(D_2)-1] / 100

X, Y = np.meshgrid(Reserves, Reserves)
Z = np.array(X)
Bins = np.linspace( 0, 1600, 1601)
Counts = np.zeros( len(Bins))
for i in range( len(Res_1)):
    for j in range( len(Res_2)):
        Z[j,i] = Res_1[i] * Res_2[j]
        k = int( (Reserves[i]+Reserves[j]))
        Counts[k] += Z[j,i] 

Counts /= max( Counts)
D_12 = np.array(Counts)
for i in range( len(D_12)-1): D_12[i+1] += D_12[i]
D_12 /= D_12[len(D_12)-1] / 100

fig = plt.figure( figsize=(15,15))
plt.suptitle( "Распределение вероятностей жидких и газообразных, 2017 год")

gs = plt.GridSpec(2, 2, height_ratios=[1, 1], width_ratios=[1, 1]) 
ax1 = plt.subplot(gs[0])
ax2 = plt.subplot(gs[1])
ax3 = plt.subplot(gs[2])
ax4 = plt.subplot(gs[3])

ax1.plot([260, 300, 400], [10, 50, 90], "o", color="g")
ax1.plot(Reserves-169, D_1, "-.", color="g")
ax1.plot(Reserves, D_1, "-", lw = 2, color="g")
ax1.set_xlim( 0, 800)
ax1.set_ylim( 0, 100)
ax1.set_xlabel( "Сырая нефть, млрд тонн")
ax1.set_ylabel( "Вероятность (что менее)")
ax1.grid(True)
ax1.text(450, 85, "3P URR = 400 млрд т")
ax1.text(400, 45, "2P URR = 300 млрд т")
ax1.text(300, 5, "1P URR = 260 млрд т")

ax2.plot([ 230, 315, 460], [10, 50, 90], "o", color="r")
ax2.plot(Reserves-127, D_2, "-.", color="r")
ax2.plot(Reserves, D_2, "-", lw = 2, color="r")
ax2.set_xlim( 0, 800)
ax2.set_ylim( 0, 100)
ax2.set_xlabel( "Газ, конденсат, ШФЛУ, млрд toe")
ax2.set_ylabel( "Вероятность (что менее)")
ax2.grid(True)
ax2.text(420, 85, "3P URR = 460 млрд toe")
ax2.text(330, 45, "2P URR = 315 млрд toe")
ax2.text(250, 5, "1P URR = 230 млрд toe")

CS = ax3.contour(Y, X, Z*100, levels = [10, 50, 90])
CS.levels = ["10%","50%","90%"]
ax3.clabel(CS, inline=1, fontsize=10)
ax3.set_xlim( 100, 600)
ax3.set_ylim( 100, 600)
ax3.set_xlabel( "Газ, конденсат, ШФЛУ, млрд toe")
ax3.set_ylabel( "Сырая нефть, млрд тонн")
ax3.text(105, 150, "Остаточные извлекаемые (1P) = 230 млрд toe", color='g')
ax3.grid(True)

ax4.plot([ 530-127-169], [10], "o", color="g")
ax4.plot([ 530, 640, 800], [10, 50, 90], "o", color="k")
#ax4.plot(Bins, Counts*100, "--", color="k")
ax4.plot(Bins, D_12, "-", lw = 2, color="k")
ax4.plot(Bins-169-127, D_12, "-.", lw = 2, color="g")
ax4.set_xlim( 0, 1200)
ax4.set_ylim( 0, 100)
ax4.set_xlabel( "Все жидкие и газообразные, млрд toe")
ax4.set_ylabel( "Вероятность (что менее)")
ax4.grid(True)
ax4.text(20, 85, "3P URR = 800 млрд toe")
ax4.text(20, 45, "2P URR = 640 млрд toe")
ax4.text(550, 5, "1P URR = 530 млрд toe")

plt.savefig( "./Graphs/figure_14_11.png")
if InteractiveModeOn: plt.show(True)
