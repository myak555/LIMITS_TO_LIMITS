from Resources import *
import matplotlib

matplotlib.rcParams['xtick.direction'] = 'out'
matplotlib.rcParams['ytick.direction'] = 'out'

Reserves = np.linspace( 0, 600, 601)

Res_1 = np.zeros(len(Reserves))
Res_2 = Gauss( 60, 0.013, .0025, 1).GetVector(Reserves)
D_1 = np.zeros(len(Reserves))
s = 35
for i in range( len(D_1)):
    d = Reserves[i] / s
    if d<=0: continue
    d = 1 - (1 / d) ** 0.85
    if d<=0: continue
    D_1[i] = d
D_1 /= D_1[len(D_1)-1] / 100
for i in range( 1, len(D_1)-1): Res_1[i] = (D_1[i+1]-D_1[i-1])/2.0
Res_1 /= np.max( Res_1)
    
D_2 = np.array(Res_2)
for i in range( len(D_2)-1): D_2[i+1] += D_2[i]
D_2 /= D_2[len(D_2)-1] / 100

X, Y = np.meshgrid(Reserves, Reserves)
Z = np.array(X)
Bins = np.linspace( 0, 1200, 1201)
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
plt.suptitle( "Распределение вероятностей твёрдых, жидких и газообразных, 2017 год")

gs = plt.GridSpec(2, 2, height_ratios=[1, 1], width_ratios=[1, 1]) 
ax1 = plt.subplot(gs[0])
ax2 = plt.subplot(gs[1])
ax3 = plt.subplot(gs[2])
ax4 = plt.subplot(gs[3])

ax1.plot([400, 900, 2600], [10, 50, 90], "o", color="k")
ax1.plot(Reserves*10-205, D_1, "-.", color="k")
ax1.plot(Reserves*10, D_1, "-", lw = 2, color="k")
#ax1.plot(Reserves*10, Res_1*100, "--", lw = 2, color="k")
ax1.set_xlim( 0, 3000)
ax1.set_ylim( 0, 100)
ax1.set_xlabel( "Уголь и твёрдые, млрд toe")
ax1.set_ylabel( "Вероятность (что менее)")
ax1.grid(True)
ax1.text(300, 85, "3P URR = 2600 млрд т")
ax1.text(1000, 45, "2P URR = 900 млрд т")
ax1.text(500, 5, "1P URR = 400 млрд т")

ax2.plot([ 530, 640, 800], [10, 50, 90], "o", color="r")
ax2.plot(Reserves*10-296, D_2, "-.", color="r")
ax2.plot(Reserves*10, D_2, "-", lw = 2, color="r")
ax2.set_xlim( 0, 1500)
ax2.set_ylim( 0, 100)
ax2.set_xlabel( "Жидкости и природный газ, млрд toe")
ax2.set_ylabel( "Вероятность (что менее)")
ax2.grid(True)
ax2.text(50, 85, "3P URR = 800 млрд toe")
ax2.text(700, 45, "2P URR = 640 млрд toe")
ax2.text(600, 5, "1P URR = 530 млрд toe")

CS = ax3.contour(Y*10, X*10, Z*100, levels = [10, 50, 90])
CS.levels = ["10%","50%","90%"]
ax3.clabel(CS, inline=1, fontsize=10)
ax3.set_xlim( 0, 1400)
ax3.set_ylim( 0, 1400)
ax3.set_xlabel( "Жидкости и природный газ, млрд toe")
ax3.set_ylabel( "Уголь и твёрдые, млрд toe")
ax3.text(50, 150, "Остаточные извлекаемые (1P) = 500 млрд toe", color='g')
ax3.grid(True)

ax4.plot([ 500], [10], "o", color="g")
ax4.plot([ 1000, 1400, 3300], [10, 50, 90], "o", color="m")
#ax4.plot(Bins, Counts*100, "--", color="m")
ax4.plot(Bins*10, D_12, "-", lw = 2, color="m")
ax4.plot(Bins*10-501, D_12, "-.", lw = 2, color="g")
ax4.set_xlim( 0, 4000)
ax4.set_ylim( 0, 100)
ax4.set_xlabel( "Энергоресурсы, млрд toe")
ax4.set_ylabel( "Вероятность (что менее)")
ax4.grid(True)
ax4.text(200, 85, "3P URR = 3300 млрд toe")
ax4.text(1500, 45, "2P URR = 1400 млрд toe")
ax4.text(1100, 5, "1P URR = 1000 млрд toe")

plt.savefig( ".\\Graphs\\figure_14_12.png")
fig.show()
