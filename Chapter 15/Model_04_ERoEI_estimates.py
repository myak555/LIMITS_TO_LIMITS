from Predictions import *

class ERoEI:
    #
    # Performs ERoEI modeling
    #
    def __init__( self, name, sigma, Q0=501, Eroei0=30):
        self.Name = name
        if Eroei0 >= 100: Eroei0 = 99 
        if Eroei0 < 2: Eroei0 = 2 
        self.Calibration_ERoEI = Eroei0
        self.Calibration_Q = Q0 
        self.Sigma = sigma 
        tmp = 2 / (2 - np.log10(Eroei0)) - 1
        tmp = np.log( tmp) / sigma + Q0
        self.Sigmoid = Sigmoid( tmp, sigma, 2, 0)
        print( "Q = {:.1f}, ERoEI={:.1f}".format( 0, self.Compute( 0)))
        print( "Q = {:.1f}, ERoEI={:.1f}".format( 501, self.Compute( 501)))
        print( "Q = {:.1f}, ERoEI={:.1f}".format( 1000, self.Compute( 1000)))
        print( "Q = {:.1f}, ERoEI={:.1f}".format( 1400, self.Compute( 1400)))
        print( "Q = {:.1f}, ERoEI={:.1f}".format( 3300, self.Compute( 3300)))
        return
    def Compute( self, x):
        tmp = self.Sigmoid.Compute( x)
        return 10**tmp
    def GetVector( self, x):
        tmp = self.Sigmoid.GetVector( x)
        return 10**tmp

Q = np.linspace( 0, 4000, 100)
M1 = ERoEI( "Модель 1, URR=1.0·10¹⁵ toe", 0.01, Eroei0=20)
M2 = ERoEI( "Модель 2, URR=1.4·10¹⁵ toe", 0.006, Eroei0=30)
M3 = ERoEI( "Модель 3, URR=3.3·10¹⁵ toe", 0.003, Eroei0=40)
M1_v = M1.GetVector(Q) 
M2_v = M2.GetVector(Q) 
M3_v = M3.GetVector(Q) 

fig = plt.figure( figsize=(15,10))
fig.suptitle( 'Иллюстрация ERoEI(Q)', fontsize=22)
gs = plt.GridSpec(2, 1, height_ratios=[2, 1]) 
ax1 = plt.subplot(gs[0])
ax2 = plt.subplot(gs[1])

ax1.set_title("ERoEI")
ax1.plot( Q, M1_v, "--", lw=2, color='r', label=M1.Name)
ax1.plot( Q, M2_v, "-", lw=2, color='g', label=M2.Name)
ax1.plot( Q, M3_v, "-.", lw=2, color='b', label=M3.Name)
ax1.plot( [501,501], [-10,150], "--", lw=2, color='k')
ax1.plot( [1000,1000], [-10,20], "--", lw=2, color='k')
ax1.plot( [1400,1400], [-10,20], "--", lw=2, color='k')
ax1.set_xlim( 0, 3300)
ax1.set_ylim( -10, 100)
ax1.text(600, 50, "Накопленная добыча 2017 года")
ax1.grid(True)
ax1.legend(loc=0)

ax2.set_title("1-1/ERoEI")
ax2.plot( Q, 1-1/M1_v, "--", lw=2, color='r')
ax2.plot( Q, 1-1/M2_v, "-", lw=2, color='g')
ax2.plot( Q, 1-1/M3_v, "-.", lw=2, color='b')
ax2.plot( [501,501], [0,1.2], "--", lw=2, color='k')
ax2.plot( [1000,1000], [0,1.2], "--", lw=2, color='k')
ax2.plot( [1400,1400], [0,1.2], "--", lw=2, color='k')
ax2.set_xlim( 0, 3300)
ax2.set_ylim( 0, 1.2)
ax2.grid(True)
ax2.set_xlabel("Накопленная добыча Q, млрд toe")
ax2.grid(True)

plt.savefig( "./Graphs/figure_15_04.png")
fig.show()
