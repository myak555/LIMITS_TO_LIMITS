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
    def GetVectorInverse( self, x):
        tmp = self.GetVector( x)
        return 1-1/tmp

T = np.linspace( 1950, 2050, 401)
A = Hubbert( 2000, 0.03, 0.113, 50).GetVector(T)
A_decline = Sigmoid( 2009, 10, 1, 0).GetVector(T)
A *= A_decline
B = Hubbert( 2025, 0.02928, 0.0825, 57).GetVector(T)
C = Hubbert( 2000, 0.04, 0.0825, 50).GetVector(T)
C_decline = Sigmoid( 2040, 2, 1, 0).GetVector(T)
C *= C_decline
World = A + B + C

A_prd = np.ones(len(T)) * 0.5
A_prd *= A_decline
B_prd = Sigmoid(2016,0.161,1,15).GetVector(T)
C_prd = np.ones(len(T)) * 7
C_prd *= C_decline
World_prd = A_prd + B_prd + C_prd

A_cns = np.ones(len(T)) * 0.5
A_cns *= A_decline
B_cns = np.ones(len(T)) * 1.5
C_cns = Sigmoid(2016,0.161,3,1).GetVector(T)
C_cns *= C_decline
World_cns = A_cns + B_cns + C_cns
D_cns = World - World_prd - World_cns
World_cns = World - World_prd

ERoEI_A = A/(A_prd+0.001)
ERoEI_B = B/(B_prd+0.001)
ERoEI_C = C/(C_prd+0.001)
ERoEI_World = World/(A_prd+B_prd+C_prd)

for i in range( len(T)):
    if T[i] == 2000:
        print( "In year {:g} ({:g}):".format(T[i],i))
        print( "Production A = {:.1f}, spent = {:.1f}, ERoEIst = {:.1f}, consumption = {:.2f}".format(A[i],A_prd[i],ERoEI_A[i],A_cns[i]/10))
        print( "Production B = {:.1f}, spent = {:.1f}, ERoEIst = {:.1f}, consumption = {:.2f}".format(B[i],B_prd[i],ERoEI_B[i],B_cns[i]/1))
        print( "Production C = {:.1f}, spent = {:.1f}, ERoEIst = {:.1f}, consumption = {:.2f}".format(C[i],C_prd[i],ERoEI_C[i],C_cns[i]/0.1))
        print( "Production D = {:.1f}, spent = {:.1f}, consumption = {:.2f}".format(0,D_cns[i],D_cns[i]/88.9))
        print( "Production Total = {:.1f}, spent = {:.1f}, ERoEIst = {:.1f}, consumption = {:.2f}".format(World[i],World_prd[i],ERoEI_World[i],World_cns[i]/100))
    if T[i] == 2008:
        print( "In year {:g} ({:g}):".format(T[i],i))
        print( "Production A = {:.1f}, spent = {:.1f}, ERoEIst = {:.1f}, consumption = {:.2f}".format(A[i],A_prd[i],ERoEI_A[i],A_cns[i]/10))
        print( "Production B = {:.1f}, spent = {:.1f}, ERoEIst = {:.1f}, consumption = {:.2f}".format(B[i],B_prd[i],ERoEI_B[i],B_cns[i]/1))
        print( "Production C = {:.1f}, spent = {:.1f}, ERoEIst = {:.1f}, consumption = {:.2f}".format(C[i],C_prd[i],ERoEI_C[i],C_cns[i]/0.1))
        print( "Production D = {:.1f}, spent = {:.1f}, consumption = {:.2f}".format(0,D_cns[i],D_cns[i]/88.9))
        print( "Production Total = {:.1f}, spent = {:.1f}, ERoEIst = {:.1f}, consumption = {:.2f}".format(World[i],World_prd[i],ERoEI_World[i],World_cns[i]/100))
    if T[i] == 2010:
        print( "In year {:g} ({:g}):".format(T[i],i))
        print( "Production A = {:.1f}, spent = {:.1f}, ERoEIst = {:.1f}, consumption = {:.2f}".format(A[i],A_prd[i],ERoEI_A[i],A_cns[i]/6.5))
        print( "Production B = {:.1f}, spent = {:.1f}, ERoEIst = {:.1f}, consumption = {:.2f}".format(B[i],B_prd[i],ERoEI_B[i],B_cns[i]/1))
        print( "Production C = {:.1f}, spent = {:.1f}, ERoEIst = {:.1f}, consumption = {:.2f}".format(C[i],C_prd[i],ERoEI_C[i],C_cns[i]/0.1))
        print( "Production D = {:.1f}, spent = {:.1f}, consumption = {:.2f}".format(0,D_cns[i],D_cns[i]/91.9))
        print( "Production Total = {:.1f}, spent = {:.1f}, ERoEIst = {:.1f}, consumption = {:.2f}".format(World[i],World_prd[i],ERoEI_World[i],World_cns[i]/99.5))
    if T[i] == 2025:
        print( "In year {:g} ({:g}):".format(T[i],i))
        print( "Production A = {:.1f}, spent = {:.1f}, ERoEIst = {:.1f}, consumption = {:.2f}".format(A[i],A_prd[i],ERoEI_A[i],A_cns[i]/3.5))
        print( "Production B = {:.1f}, spent = {:.1f}, ERoEIst = {:.1f}, consumption = {:.2f}".format(B[i],B_prd[i],ERoEI_B[i],B_cns[i]/1))
        print( "Production C = {:.1f}, spent = {:.1f}, ERoEIst = {:.1f}, consumption = {:.2f}".format(C[i],C_prd[i],ERoEI_C[i],C_cns[i]/0.1))
        print( "Production D = {:.1f}, spent = {:.1f}, consumption = {:.2f}".format(0,D_cns[i],D_cns[i]/91.9))
        print( "Production Total = {:.1f}, spent = {:.1f}, ERoEIst = {:.1f}, consumption = {:.2f}".format(World[i],World_prd[i],ERoEI_World[i],World_cns[i]/96.5))
    if T[i] == 2039:
        print( "In year {:g} ({:g}):".format(T[i],i))
        print( "Production A = {:.1f}, spent = {:.1f}, ERoEIst = {:.1f}, consumption = {:.2f}".format(A[i],A_prd[i],ERoEI_A[i],A_cns[i]/1.5))
        print( "Production B = {:.1f}, spent = {:.1f}, ERoEIst = {:.1f}, consumption = {:.2f}".format(B[i],B_prd[i],ERoEI_B[i],B_cns[i]/1))
        print( "Production C = {:.1f}, spent = {:.1f}, ERoEIst = {:.1f}, consumption = {:.2f}".format(C[i],C_prd[i],ERoEI_C[i],C_cns[i]/0.1))
        print( "Production D = {:.1f}, spent = {:.1f}, consumption = {:.2f}".format(0,D_cns[i],D_cns[i]/91.9))
        print( "Production Total = {:.1f}, spent = {:.1f}, ERoEIst = {:.1f}, consumption = {:.2f}".format(World[i],World_prd[i],ERoEI_World[i],World_cns[i]/94.5))
    if T[i] == 2042:
        print( "In year {:g} ({:g}):".format(T[i],i))
        print( "Production A = {:.1f}, spent = {:.1f}, ERoEIst = {:.1f}, consumption = {:.2f}".format(A[i],A_prd[i],ERoEI_A[i],A_cns[i]/1.5))
        print( "Production B = {:.1f}, spent = {:.1f}, ERoEIst = {:.1f}, consumption = {:.2f}".format(B[i],B_prd[i],ERoEI_B[i],B_cns[i]/1))
        print( "Production C = {:.1f}, spent = {:.1f}, ERoEIst = {:.1f}, consumption = {:.2f}".format(C[i],C_prd[i],ERoEI_C[i],C_cns[i]/0.1))
        print( "Production D = {:.1f}, spent = {:.1f}, consumption = {:.2f}".format(0,D_cns[i],D_cns[i]/91.9))
        print( "Production Total = {:.1f}, spent = {:.1f}, ERoEIst = {:.1f}, consumption = {:.2f}".format(World[i],World_prd[i],ERoEI_World[i],World_cns[i]/94.5))

fig = plt.figure( figsize=(15,15))
fig.suptitle( 'Гипотетические страны А,В,С', fontsize=22)
gs = plt.GridSpec(3, 1, height_ratios=[2, 1, 1]) 
ax1 = plt.subplot(gs[0])
ax2 = plt.subplot(gs[1])
ax3 = plt.subplot(gs[2])

ax1.set_title("Добыча угля / затраты на добычу")
ax1.plot( T, A, "-", lw=2, color='r', label="Страна А")
ax1.plot( T, A_prd, "--", lw=2, color='r')
ax1.plot( T, B, "-", lw=2, color='g', label="Страна B")
ax1.plot( T, B_prd, "--", lw=2, color='g')
ax1.plot( T, C, "-", lw=2, color='b', label="Страна C")
ax1.plot( T, C_prd, "--", lw=2, color='b')
ax1.plot( T, World, "-", lw=3, color='k', label="Всего")
ax1.plot( [2009,2009], [0,80], "--", lw=1, color='m')
ax1.plot( [2041,2041], [0,80], "--", lw=1, color='m')
ax1.set_xlim( 1980, 2050)
ax1.set_ylim( 0, 160)
ax1.set_ylabel("Млн тонн")
ax1.text(1992, 70, "Гражданская война в А", color='m')
ax1.text(2030, 83, "Закрыт разрез в C", color='m')
ax1.grid(True)
ax1.legend(loc=0)

ax2.plot( T[:-162], ERoEI_A[:-162], "-", lw=2, color='r')
ax2.plot( T, ERoEI_B, "-", lw=2, color='g')
ax2.plot( T[:-36], ERoEI_C[:-36], "-", lw=2, color='b')
ax2.set_ylabel("ERoEIst")
ax2.set_xlim( 1980, 2050)
ax2.set_ylim( 0, 110)
ax2.grid(True)

ax3.plot( T, ERoEI_World, "-", lw=3, color='k')
ax3.set_ylabel("ERoEIst")
ax3.set_xlim( 1980, 2050)
ax3.set_ylim( 0, 18)
ax3.set_xlabel("Годы")
ax3.grid(True)

plt.savefig( "./Graphs/figure_15_07.png")
if InteractiveModeOn: plt.show(True)
