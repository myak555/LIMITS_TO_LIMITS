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
Randers_2012 = Interpolation_BAU_2012()
Randers_2012.Solve( Year)
Randers_2012.Correct_To_Actual( 1830, 2012)

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
Prd._Nuclear_Functions[-1].Right = 0 # Simulates negative nuclear scenario
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

delay = 5
Population_Z1 = Sigmoid( 2054 + delay, 0.15, 0, -8300).GetVector(Year)
Population_Z2 = Sigmoid( 2050 + delay, 0.2, 0, -6200).GetVector(Year)
Population_Z3 = Sigmoid( 2046 + delay, 0.25, 0, -4200).GetVector(Year)
population_low_Z = population_medium + Population_Z1
population_medium_Z = population_medium + Population_Z2
population_high_Z = population_medium + Population_Z3

M1_CPP_2P_Z = 1000.0 * M2_Cons_2P_rn / population_low_Z  
M2_CPP_2P_Z = 1000.0 * M2_Cons_2P_rn / population_medium_Z  
M3_CPP_2P_Z = 1000.0 * M2_Cons_2P_rn / population_high_Z

fig = plt.figure( figsize=(15,15))
fig.suptitle( 'Модель с сокращением рождаемости "Население Z"', fontsize=22)
gs = plt.GridSpec(2, 1, height_ratios=[1, 1]) 
ax1 = plt.subplot(gs[0])
ax2 = plt.subplot(gs[1])

ax1.set_title("Население")
ax1.plot( Year, Prd.Nuclear, "-", lw=2, color='m', label="Пессимистический прогноз по АЭС")
ax1.plot( Year, population_low, "--", lw=1, color='g')
ax1.plot( Year, population_medium, "--", lw=1, color='b', label="Прогноз ООН")
ax1.plot( Year, population_high, "--", lw=1, color='r')
ax1.plot( Year, Randers_2012.Population, "--", lw=2, color='m', label="Модель NewWorld-2012")
ax1.plot( Year, population_low_Z, "-", lw=3, color='g', label="Стабилизация на 3.2 млрд")
ax1.plot( Year, population_medium_Z, "-", lw=3, color='b', label="Стабилизация на 5.2 млрд")
ax1.plot( Year, population_high_Z, "-", lw=3, color='r', label="Стабилизация на 7.6 млрд")
ax1.plot( [2040, 2040], [0, 9000], "-.", lw=2, color='#505050')
ax1.set_xlim( 1850, 2150)
ax1.set_ylim( 0, 12500)
ax1.set_ylabel("миллионов")
ax1.text(1960, 9300, "Максимум населения: 8.9 млрд в 2040 году")
ax1.grid(True)
ax1.legend(loc=2)

ax2.set_title("Нетто энергия на душу населения")
ax2.plot( Year, M1_CPP_1P, "--", lw=1, color='r')
ax2.plot( Year, M2_CPP_2P, "--", lw=1, color='g')
ax2.plot( Year, M3_CPP_3P, "--", lw=1, color='b')
ax2.plot( Year, M1_CPP_2P_Z, "-", lw=3, color='g')
ax2.plot( Year, M2_CPP_2P_Z, "-", lw=3, color='b')
ax2.plot( Year, M3_CPP_2P_Z, "-", lw=3, color='r')
ax2.plot( [1960,2150], [1020,1020], "-.", lw=2, color='#505050')
ax2.plot( [1937,2150], [620,620], "-.", lw=2, color='#505050')
ax2.plot( [1906,2150], [450,450], "-.", lw=2, color='#505050')
ax2.text( 1970, 1106, "Уровень 1960 года")
ax2.text( 1970, 726, "Уровень 1938 года")
ax2.text( 1970, 336, "Уровень 1906 года")
ax2.set_xlim( 1850, 2150)
ax2.set_ylim( 0, 2000)
ax2.set_xlabel("Годы")
ax2.set_ylabel("кг нефтяного эквив. в год")
ax2.grid(True)
#ax2.legend(loc=2)

plt.savefig( ".\\Graphs\\figure_15_09.png")
fig.show()
