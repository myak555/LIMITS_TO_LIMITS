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

Q = np.linspace( 0, 4000, 100)
M1 = ERoEI( "Модель 1, URR=1.0·10¹⁵ toe", 0.01, Eroei0=20)
M2 = ERoEI( "Модель 2, URR=1.4·10¹⁵ toe", 0.006, Eroei0=30)
M3 = ERoEI( "Модель 3, URR=3.3·10¹⁵ toe", 0.003, Eroei0=40)

Res = Resources()
Pop = Population()

Year = np.linspace( 1800, 2300, 501)
population_low = Pop.UN_Low.GetVector(Year)
population_medium = Pop.UN_Medium.GetVector(Year)
population_high = Pop.UN_High.GetVector(Year)

All_1P = Bathtub( 1965, s0=0.2, x1 = 2060, s1=0.20, middle=12513).GetVector(Year)
All_1P += Hubbert( 2018, 0.5, 0.1, -1600).GetVector(Year)

All_2P = Bathtub( 1965, s0=0.2, x1 = 2085, s1=0.15, middle=12852).GetVector(Year)
All_2P += Hubbert( 2018, 0.5, 0.1, -1600).GetVector(Year)
All_2P += Hubbert( 2050, 0.3, 0.14, 3070).GetVector(Year)

All_3P = Bathtub( 1965, s0=0.2, x1 = 2220, s1=0.15, middle=13244).GetVector(Year)
All_3P += Hubbert( 2018, 0.5, 0.1, -1600).GetVector(Year)
All_3P += Hubbert( 2052, 0.2, 0.1, 5000).GetVector(Year)

for i in range(len(Year)):
    j = int(Year[i] - Res.Year[0])
    if j < 0: continue
    if j >= len( Res.Year): break
    All_1P[i] = Res.Total[j]
    All_2P[i] = Res.Total[j]
    All_3P[i] = Res.Total[j]

PP_1P = 1000.0 * All_1P / population_low  
PP_2P = 1000.0 * All_2P / population_medium  
PP_3P = 1000.0 * All_3P / population_high

Cum_1P = np.array( All_1P) 
Cum_2P = np.array( All_2P) 
Cum_3P = np.array( All_3P) 

for i in range(1,len(Year)):
    Cum_1P[i] += Cum_1P[i-1]
    Cum_2P[i] += Cum_2P[i-1]
    Cum_3P[i] += Cum_3P[i-1]

M1_Cons_1P = All_1P * M1.GetVectorInverse(Cum_1P/1000)
M2_Cons_1P = All_1P * M2.GetVectorInverse(Cum_1P/1000)
M3_Cons_1P = All_1P * M3.GetVectorInverse(Cum_1P/1000)
M1_Cons_2P = All_2P * M1.GetVectorInverse(Cum_2P/1000)
M2_Cons_2P = All_2P * M2.GetVectorInverse(Cum_2P/1000)
M3_Cons_2P = All_2P * M3.GetVectorInverse(Cum_2P/1000)
M1_Cons_3P = All_3P * M1.GetVectorInverse(Cum_3P/1000)
M2_Cons_3P = All_3P * M2.GetVectorInverse(Cum_3P/1000)
M3_Cons_3P = All_3P * M3.GetVectorInverse(Cum_3P/1000)

ERoEI_renewable = 15
ERoEI_nuclear = 10
Prd = Interpolation_Realistic_2012()
Prd.Solve( Year)
Prd.Correct_To_Actual( 1890, 2017)
Renewable = Prd.Renewable * (1-1/ERoEI_renewable)
Nuclear = Prd.Nuclear * (1-1/ERoEI_nuclear)

M1_Cons_1P_r = M1_Cons_1P + Renewable 
M2_Cons_1P_r = M2_Cons_1P + Renewable 
M3_Cons_1P_r = M3_Cons_1P + Renewable 
M1_Cons_2P_r = M1_Cons_2P + Renewable 
M2_Cons_2P_r = M2_Cons_2P + Renewable 
M3_Cons_2P_r = M3_Cons_2P + Renewable 
M1_Cons_3P_r = M1_Cons_3P + Renewable 
M2_Cons_3P_r = M2_Cons_3P + Renewable 
M3_Cons_3P_r = M3_Cons_3P + Renewable 

M1_Cons_1P_rn = M1_Cons_1P + Renewable + Nuclear 
M2_Cons_1P_rn = M2_Cons_1P + Renewable + Nuclear 
M3_Cons_1P_rn = M3_Cons_1P + Renewable + Nuclear
M1_Cons_2P_rn = M1_Cons_2P + Renewable + Nuclear
M2_Cons_2P_rn = M2_Cons_2P + Renewable + Nuclear
M3_Cons_2P_rn = M3_Cons_2P + Renewable + Nuclear
M1_Cons_3P_rn = M1_Cons_3P + Renewable + Nuclear
M2_Cons_3P_rn = M2_Cons_3P + Renewable + Nuclear
M3_Cons_3P_rn = M3_Cons_3P + Renewable + Nuclear

PP_1P = 1000.0 * All_1P / population_low  
M1_CPP_1P = 1000.0 * M1_Cons_1P_rn / population_low  
PP_2P = 1000.0 * All_2P / population_medium  
M2_CPP_2P = 1000.0 * M2_Cons_2P_rn / population_medium  
PP_3P = 1000.0 * All_3P / population_high
M3_CPP_3P = 1000.0 * M3_Cons_3P_rn / population_high

fig = plt.figure( figsize=(15,15))
fig.suptitle( 'Модель с учётом ERoEI, ВИЭ и ядерной энергии', fontsize=22)
gs = plt.GridSpec(2, 1, height_ratios=[1, 1]) 
ax1 = plt.subplot(gs[0])
ax2 = plt.subplot(gs[1])

ax1.set_title("Нетто годовое извлечение энергии")
#ax1.plot( Year, All_1P, "--", lw=1, color='#A0A0A0')
ax1.plot( Year, M1_Cons_1P, "--", lw=1, color='r', label="Ископаемое топливо")
ax1.plot( Year, M1_Cons_1P_r, "-.", lw=1, color='r', label="+ВИЭ при ERoEI={:.0f}".format(ERoEI_renewable))
ax1.plot( Year, M1_Cons_1P_rn, "-", lw=2, color='r', label="+Ядерная при ERoEI={:.0f}".format(ERoEI_nuclear))
#ax1.plot( Year, All_2P, "-", lw=1, color='#A0A0A0')
ax1.plot( Year, M2_Cons_2P, "--", lw=1, color='g')
ax1.plot( Year, M2_Cons_2P_r, "-.", lw=1, color='g')
ax1.plot( Year, M2_Cons_2P_rn, "-", lw=2, color='g')
#ax1.plot( Year, All_3P, "-.", lw=1, color='#A0A0A0')
ax1.plot( Year, M3_Cons_3P, "--", lw=1, color='b')
ax1.plot( Year, M3_Cons_3P_r, "-.", lw=1, color='b')
ax1.plot( Year, M3_Cons_3P_rn, "-", lw=2, color='b')
ax1.plot( [2050, 2050], [0, 20000], "--", lw=3, color='#505050')
ax1.set_xlim( 1850, 2150)
ax1.set_ylim( 0, 22000)
ax1.set_ylabel("Млн toe")
ax1.text(1960, 20500, "Максимум полезной энергии - 2050 год")
ax1.grid(True)
ax1.legend(loc=2)

ax2.set_title("Нетто энергия на душу населения")
#ax2.plot( Year, PP_1P, "--", lw=1, color='#A0A0A0')
ax2.plot( Year, M1_CPP_1P, "-", lw=2, color='r', label="M1_1P (пик={:.0f} кг)".format(np.max(M1_CPP_1P)))
#ax2.plot( Year, PP_2P, "--", lw=1, color='#A0A0A0')
ax2.plot( Year, M2_CPP_2P, "-", lw=2, color='g', label="M2_2P (пик={:.0f} кг)".format(np.max(M2_CPP_2P)))
#ax2.plot( Year, PP_3P, "--", lw=1, color='#A0A0A0')
ax2.plot( Year, M3_CPP_3P, "-", lw=2, color='b', label="M3_3P (пик={:.0f} кг)".format(np.max(M3_CPP_3P)))
ax2.plot( [1960,2150], [1031,1031], "-.", lw=2, color='#505050')
ax2.plot( [1913,2150], [522,522], "--", lw=2, color='#505050')
ax2.plot( [1890,2150], [282,282], "-.", lw=2, color='#505050')
ax2.text( 1970, 1106, "Уровень 1960 года")
ax2.text( 1970, 595, "Уровень 1913 года")
ax2.text( 1970, 355, "Уровень 1890 года")
ax2.set_xlim( 1850, 2150)
ax2.set_ylim( 0, 2000)
ax2.set_xlabel("Годы")
ax2.set_ylabel("кг нефтяного эквив. в год")
ax2.grid(True)
ax2.legend(loc=2)

plt.savefig( ".\\Graphs\\figure_15_06.png")
fig.show()
