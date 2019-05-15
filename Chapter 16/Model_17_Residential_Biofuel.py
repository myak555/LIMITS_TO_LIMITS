from Predictions import *

#
# Energy Model with dynamic ERoEI (after C.Hall and K.Kleatgaard)
# Using investment and return functions defined as Markov chains
# Models changes in staple consumption, resulting in "Undulating Plateau"
# Resource - actual energy production (mln toe)
# Population - population function (mln)
# q0>0 - assumed energy production at T0 (mln toe)
# URR - total recoverable resources (mln toe)
# Dynamic ERoEI
# Added residential biofuels and animal power estimates 
#
class Energy_Model_6:
    def __init__( self, Resource, Population, ERoEI, q0, URR=1400e3, staple_level = 1.4):
        self.Resource = Resource
        self.Population = Population
        self.URR = URR
        self.q0 = q0
        self.ERoEI = ERoEI
        self.Staple_Level = staple_level
        self.Staple_Step = 0.15
        self.Staple_Crisis_Intensity = 0.95 # 2-8% production decline in crisis      
        self.Deprivation = 1.0
        yr = np.linspace(0,99,100)
        mc = Markov_Chain([3, 8, 10], yr, 0)
        mc.Filter[0] = 0
        self.Return_Function = mc.Filter / np.sum( mc.Filter)
        mc = Markov_Chain([10], yr, 0)
        self.Invest_Function = -mc.Filter
        #print( np.sum( self.Return_Function), np.sum(self.Invest_Function))
        self.Biomass = Linear_Combo()
        self.Biomass.Wavelets += [Hubbert( x0=2000.000, s0=0.06567, s1=0.04720, peak=460.000, shift=585.000)]
        self.Biomass.Wavelets += [Hubbert( x0=1847.435, s0=0.22145, s1=0.37971, peak=88.089, shift=0.000)]
        self.Animal_Power = Sigmoid( 1915, 0.1, 400, 50)
        self.ERoEI_Biomass = 2.5
        return
    def Solve( self, t0):
        self.Solution_Time = np.array( t0)
        self.Solution_ERoEI = np.zeros( len(t0))
        self.Production = np.zeros( len(t0))
        self.ProductionCalibrated = np.zeros( len(t0))
        self.UsefulProduction = np.zeros( len(t0))
        self.Production_PH = np.zeros( len(t0))
        self.Consumption_PH = np.zeros( len(t0))
        self.Solution_Q = np.zeros( len(t0))
        self.Pop = self.Population.GetVector( t0)

        # Expand fossil fuel data to the start of time
        if self.Solution_Time[0] < self.Resource.Calibration_Year[0]:
            b = self.Resource.Calibration_Carbon[0] / self.q0
            b **= 1/(self.Resource.Calibration_Year[0]-self.Solution_Time[0])
        deltaT = int(self.Resource.Calibration_Year[0] - t0[0])
        print (deltaT)
        perCapita = 0
        for i in range( len( t0)):
            t = t0[i]
            if t < self.Resource.Calibration_Year[0]:
                self.ProductionCalibrated[i] = self.q0 * b ** (t-t0[0])
                continue
            if t > self.Resource.Calibration_Year[-1]:
                self.ProductionCalibrated[i] = self.Pop[i] * perCapita
                continue
            self.ProductionCalibrated[i] = self.Resource.Calibration_Carbon[i-deltaT]
            perCapita = self.ProductionCalibrated[i] / self.Pop[i]

        # Initial values
        self.Solution_ERoEI[0] = 10**self.ERoEI.Compute(0)
        return_function = self.Return_Function * self.Solution_ERoEI[0]
        norm_return = self.ProductionCalibrated[0] / return_function[1]
        for j in range( len( return_function)-1):
            self.Production[j] = norm_return * return_function[j+1]
            self.UsefulProduction[j] = self.Production[j] + norm_return * self.Invest_Function[j] 
        self.Production_PH[0] = self.Production[0] / self.Pop[0]
        self.Consumption_PH[0] = self.UsefulProduction[0] / self.Pop[0]
        self.Solution_Q[0] = self.Production[0]

        # Propagate
        for i in range( 1,len(t0)-len(self.Return_Function)):
            self.Solution_ERoEI[i] = 10**self.ERoEI.Compute( self.Solution_Q[i-1]/1000)
            if t0[i] > 2017:
                #break #Uncomment to kill investments in 2018
                deltaQ = self.Production[i-1] * self.Pop[i] / self.Pop[i-1] * self.Deprivation
                deltaQ -= self.Production[i]
            else:
                deltaQ = self.ProductionCalibrated[i] - self.Production[i]
            if deltaQ < 0:
                #print( "Degrowth: {:g} {:.1f}".format( t0[i], deltaQ) )
                deltaQ = 0
                if t0[i] <= 2017: # stick to actual
                    self.Production[i] = self.ProductionCalibrated[i]
                    self.UsefulProduction[i-1] = self.ProductionCalibrated[i-1] * (1-1/self.Solution_ERoEI[i-1])
            sump = np.sum( self.Production)
            if sump + self.Solution_ERoEI[i]*deltaQ >= self.URR:
                deltaQ = 0
            p_crisis = 1
            if t0[i] > 2017:
                cl = (self.Consumption_PH[i-2] + self.Consumption_PH[i-3] + self.Consumption_PH[i-4]) / 3
                if cl < self.Staple_Level:
                    deltaQ = 0
                    p_crisis = self.Staple_Crisis_Intensity
                    self.Staple_Level -= self.Staple_Step
                    if self.Staple_Level < self.Staple_Step: self.Staple_Level = self.Staple_Step
            return_function = self.Return_Function * self.Solution_ERoEI[i]
            norm_return = deltaQ / return_function[1]
            useful_function = return_function + self.Invest_Function
            for j in range( len( return_function)):
                self.Production[i+j-1] += return_function[j] * norm_return
                self.UsefulProduction[i+j-1] += useful_function[j] * norm_return
            self.Production[i] *= p_crisis
            self.Production[i+1] *= p_crisis**0.5
            self.Production_PH[i] = self.Production[i] / self.Pop[i]
            self.Consumption_PH[i-1] = self.UsefulProduction[i-1] / self.Pop[i-1]
            self.Solution_Q[i] = self.Solution_Q[i-1] + self.Production[i]
        self.Solution_Q = np.clip( self.Solution_Q, 0, self.URR)
        self.Production_PH_Carbon = np.array( self.Production_PH)
        self.Consumption_PH_Carbon = np.array( self.Consumption_PH)
        self.Production_Bio = self.Biomass.GetVector(t0)
        self.Production_Animal = self.Animal_Power.GetVector(t0)
        eBio = self.Production_Bio/self.Pop + self.Production_Animal/self.Pop
        self.Production_PH += eBio
        self.Consumption_PH += eBio * (1-1/self.ERoEI_Biomass)
        return
    def GetConsumptionYear( self, y):
        returnY = 0
        consumptionY = 0
        for i in range( len( self.Solution_Time)):
            if self.Solution_Time[i] == y :
                consumptionY = self.Consumption_PH[i]
                print( "In {:g} per head production  {:.0f} кг and consumption {:.0f} кг".format(
                    self.Solution_Time[i], self.Production_PH[i]*1000, consumptionY*1000))
            if returnY == 0 and consumptionY>0 and self.Consumption_PH[i] < consumptionY:
                returnY = self.Solution_Time[i]
                print( "In {:g} per head production  {:.0f} кг and consumption {:.0f} кг".format(
                    returnY, self.Production_PH[i]*1000, self.Consumption_PH[i]*1000))
                break
        return returnY, consumptionY

#
# Solve numerically
#
Year = np.linspace( 1800, 2300, 501)
P = Population()
R = Resources()
eroei = Sigmoid( 501, 0.005, 2, 0)
E = Energy_Model_6( R, P.UN_Medium, eroei, 40)
E.Solve( Year)
maxYear = np.argmax( E.Production)
print( "In {:g} production peak at {:.0f} mln toe".format( Year[maxYear], E.Production[maxYear]))
maxProd = np.argmax( E.Production_PH)
print( "In {:g} production per person is {:.1f} kg".format( Year[maxProd], 1000*E.Production_PH[maxProd]))
maxCons = np.argmax( E.Consumption_PH)
print( "In {:g} consumption per person is {:.1f} kg".format( Year[maxCons], 1000*E.Consumption_PH[maxCons]))
endProd = np.argmax( E.Solution_Q)
for i in range( endProd, 0, -1):
    if E.Solution_Q[i] > 0.999*E.URR: continue
    endProd = i
    break
print( "In {:g} cumulative production is {:.1f} mlrd toe".format( Year[endProd], E.Solution_Q[endProd]/1000))
return1930,consumption1930 = E.GetConsumptionYear( 1930)

x_start, x_end = 1800, 2150

fig = plt.figure( figsize=(15,10))
fig.suptitle( 'Базовая модель энергетики с добавкой бытовой энергии', fontsize=22)
gs = plt.GridSpec(2, 1, height_ratios=[1, 1]) 
ax1 = plt.subplot(gs[0])
#ax2 = plt.subplot(gs[1])
ax3 = plt.subplot(gs[1])

ax1.set_title("Население и годовая добыча")
#ax1.errorbar( R.Calibration_Year, R.Calibration_Carbon, yerr=R.Calibration_Carbon*0.05, fmt=".", color="k", label="Реальная добыча")
ax1.plot( Year, E.Pop, "-", lw=2, color="b", label="Население (модель ООН)")
ax1.plot( Year, E.Production, "-", lw=2, color="k", label="Годовая добыча")
ax1.plot( Year, E.UsefulProduction, "--", lw=2, color="k", label="За вычетом ERoEI")
ax1.plot( Year, E.Production_Bio, "-", lw=2, color="g", label="Бытовое биотопливо")
ax1.plot( Year, E.Production_Animal, "-", lw=2, color="y", label="Мускульная сила животных")
ax1.plot( [Year[maxYear],Year[maxYear]], [0,E.Production[maxYear]*1.1], "--", lw=1, color="k")
ax1.text( Year[maxYear]-75, E.Production[maxYear]*0.1, "Максимум энергии: {:.1f} млрд toe в {:g} году".format( E.Production[maxYear]/1000,Year[maxYear]))
ax1.set_xlim( x_start, x_end)
ax1.set_ylim( 0,15000)
ax1.set_ylabel("миллионов")
ax1.grid(True)
ax1.legend(loc=0)

##ax2.set_title("Извлекаемые запасы и накопленная добыча")
##ax2.plot( [Year[0],Year[-1]], [E.URR/1000,E.URR/1000], "-.", lw=1, color="k", label="URR={:.0f} млрд тонн".format(E.URR/1000))
##ax2.plot( Year, E.Solution_Q/1000, "-", lw=2, color="k", label="Накопленная добыча")
##ax2.plot( Year, E.Solution_ERoEI*10, "-", lw=2, color="r", label="ERoEIext x 10")
##ax2.plot( [Year[endProd],Year[endProd]], [0,E.Solution_Q[endProd]*1.1/1000], "--", lw=1, color="k")
##ax2.text( Year[endProd] - 150, E.URR/2000, "Окончание добычи: {:.0f} млрд toe в {:g} году".format( E.Solution_Q[endProd]/1000,Year[endProd]))
##ax2.text( x_start + 10, 850, "Переменный ERoEI")
##ax2.set_xlim(x_start, x_end)
##ax2.set_ylim( 0, 1500)
##ax2.set_ylabel("млрд тонн")
##ax2.grid(True)
##ax2.legend(loc=0)

ax3.set_title("Потребление и затраты")
ax3.plot( Year,  E.Production_PH_Carbon*1000, "-", lw=2, color="#404040", label="Уголь, нефть, газ")
ax3.plot( Year,  E.Consumption_PH_Carbon*1000, "--", lw=2, color="#404040", label="Потребление (за вычетом ERoEI)")
ax3.plot( Year,  E.Production_PH*1000, "-", lw=2, color="g", label="Энергии на душу")
ax3.plot( Year,  E.Consumption_PH*1000, "--", lw=2, color="g", label="Потребление (за вычетом ERoEI)")
ax3.plot( [Year[maxProd],Year[maxProd]], [0, E.Production_PH[maxProd]*1500], "--", lw=1, color="k")
ax3.plot( [1930, return1930], [ consumption1930*1000, consumption1930*1000], "-.", lw=1, color="k")
ax3.text( Year[maxProd] - 25,  E.Production_PH[maxProd]*1030, "Максимум энергии: {:.0f} кг на душу в {:g} году".format(1000* E.Production_PH[maxProd],Year[maxProd]))
ax3.text( 1945, consumption1930*700, "Потребление 1930 и {:g} гг: {:.0f} кг".format(return1930,consumption1930*1000))
ax3.set_xlim( x_start, x_end)
ax3.set_ylim( 0, 2000)
ax3.set_xlabel("Год")
ax3.set_ylabel("кг нефт. экв.")
ax3.grid(True)
ax3.legend(loc=2)

plt.savefig( "./Graphs/figure_16_17.png")
fig.show()

