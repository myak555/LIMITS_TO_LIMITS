from Predictions import *

#
# Energy Model with dynamic ERoEI (after C.Hall and K.Kleatgaard)
# Using investment and return functions defined as Markov chains
# Models changes in staple consumption, resulting in "Undulating Plateau"
# Resource - actual energy production (mln toe)
# Population - population function (mln)
# q0>0 - assumed energy production at T0 (mln toe)
# URR - total recoverable resources (mln toe)
# Renewable energy extraction 
# Nuclear energy estimates 
# Residential biofuels and animal power estimates 
#
class Energy_Model_7:
    def __init__( self, Resource, Population, ERoEI, q0, URR=1000e3, staple_level = 1.6):
        # Resource initialization
        self.Resource = Resource
        self.Population = Population
        self.URR = URR
        self.q0 = q0
        self.Actual_Year = 2017

        # ERoEI (extended)
        self.ERoEI = ERoEI
        self.ERoEI_Renewable = 15
        self.ERoEI_Nuclear = 10
        self.ERoEI_Biomass = 2.5

        # Staple consumption modeling
        self.Staple_Level = staple_level
        self.Staple_Step = 0.15
        self.Staple_Crisis_Intensity = 0.95 # 2-8% production decline in crisis      
        self.Investment_Factor_Carbon = 1.005
        self.Investment_Factor_Renewable = 1.020
        #self.Renewable_Physical_Limit = 4600*31.6/42 # 4.6 TW (heat)
        self.Renewable_Physical_Limit = 9000 # 4.6 GW(e)
        
        # Investment filters
        yr = np.linspace(0,99,100)
        mc = Markov_Chain([3, 8, 10], yr, 0)
        mc.Filter[0] = 0
        self.Return_Function = mc.Filter / np.sum( mc.Filter)
        mc = Markov_Chain([10], yr, 0)
        self.Invest_Function = -mc.Filter
        #print( np.sum( self.Return_Function), np.sum(self.Invest_Function))

        # Biomass consumption modeling
        self.Biomass = Linear_Combo()
        self.Biomass.Wavelets += [Hubbert( x0=2000.000, s0=0.06567, s1=0.04720, peak=460.000, shift=585.000)]
        self.Biomass.Wavelets += [Hubbert( x0=1847.435, s0=0.22145, s1=0.37971, peak=88.089, shift=0.000)]
        self.Animal_Power = Sigmoid( 1915, 0.1, 400, 50)

        # Nuclear consumption modeling
        self.Nuclear = Linear_Combo()
        self.Nuclear.Wavelets = [Weibull( 1968, .018, 2.2, 40000)]
        self.Nuclear.Wavelets += [Hubbert( 2013, 0.3, 0.3, -100)]
        self.Nuclear.Wavelets += [Hubbert( 2028, 0.4, 0.29, 70)]
        self.Nuclear.Wavelets += [Hubbert( 2038, 0.4, 0.4, -70)]
        self.Nuclear.Wavelets += [Hubbert( 2052, 0.4, 0.4, 40)]
        #self.Nuclear.Wavelets += [Sigmoid( 2063, .08, 0, 0)] # Pessimistic case
        #self.Nuclear.Wavelets += [Sigmoid( 2063, .08, 0, 1550)]  # Medium case
        self.Nuclear.Wavelets += [Sigmoid( 2063, .08, 0, 3100)]  # Optimistic case
        return
    def Solve( self, t0):
        self.Solution_Time = np.array( t0)
        self.Solution_ERoEI_Carbon = np.zeros( len(t0))
        self.Production_Carbon = np.zeros( len(t0))
        self.Production_Calibrated_Carbon = np.zeros( len(t0))
        self.Production_Renewable = np.zeros( len(t0))
        self.Production_Calibrated_Renewable = np.zeros( len(t0))
        self.Production_Useful = np.zeros( len(t0))
        self.Production_PH = np.zeros( len(t0))
        self.Consumption_PH = np.zeros( len(t0))
        self.Solution_Q = np.zeros( len(t0))
        self.Pop = self.Population.GetVector( t0)
        self._Expand_Energy( t0)

        # Carbon and renewable run
        for i in range( 1,len(t0)-len(self.Return_Function)):
            self.Solution_ERoEI_Carbon[i] = 10**self.ERoEI.Compute( self.Solution_Q[i-1]/1000)
            if t0[i] > self.Actual_Year:
                deltaQ_carbon = self.Production_Carbon[i-1] * self.Pop[i] / self.Pop[i-1] * self.Investment_Factor_Carbon
                deltaQ_carbon -= self.Production_Carbon[i]
                #deltaQ_carbon = 0 #Uncomment to kill investments past the actual year
                deltaQ_renewable = self.Production_Renewable[i-1] * self.Pop[i] / self.Pop[i-1] * self.Investment_Factor_Renewable
                deltaQ_renewable -= self.Production_Renewable[i]
                #deltaQ_renewable = 0 #Uncomment to kill investments past the actual year
            else:
                deltaQ_carbon = self.Production_Calibrated_Carbon[i] - self.Production_Carbon[i]
                deltaQ_renewable = self.Production_Calibrated_Renewable[i] - self.Production_Renewable[i]
            if deltaQ_carbon < 0:
                #print( "Degrowth carbon: {:g} {:.1f}".format( t0[i], deltaQ_carbon) )
                deltaQ_carbon = 0
                if t0[i] <= self.Actual_Year: # stick to actual
                    self.Production_Carbon[i] = self.Production_Calibrated_Carbon[i]
                    self.Production_Useful[i-1] = self.Production_Calibrated_Carbon[i-1] * (1-1/self.Solution_ERoEI_Carbon[i-1])
            if deltaQ_renewable < 0:
                #print( "Degrowth renewable: {:g} {:.1f}".format( t0[i], deltaQ_renewable) )
                deltaQ_renewable = 0
                if t0[i] <= self.Actual_Year: # stick to actual
                    self.Production_Renewable[i] = self.Production_Calibrated_Renewable[i]
                    self.Production_Useful[i-1] = self.Production_Calibrated_Carbon[i-1] * (1-1/self.Solution_ERoEI_Carbon[i-1])
                    self.Production_Useful[i-1] += self.Production_Calibrated_Renewable[i-1] * (1-1/self.ERoEI_Renewable)
            sump_carbon = np.sum( self.Production_Carbon)
            if sump_carbon + self.Solution_ERoEI_Carbon[i]*deltaQ_carbon >= self.URR:
                deltaQ_carbon = 0
            if self.Production_Renewable[i] + deltaQ_renewable >= self.Renewable_Physical_Limit:
                deltaQ_renewable = 0
            p_crisis = 1
            if t0[i] > self.Actual_Year:
                cl = (self.Consumption_PH[i-2] + self.Consumption_PH[i-3] + self.Consumption_PH[i-4]) / 3
                if cl < self.Staple_Level:
                    deltaQ_carbon = 0
                    deltaQ_renewable = 0
                    p_crisis = self.Staple_Crisis_Intensity
                    self.Staple_Level -= self.Staple_Step
                    if self.Staple_Level < self.Staple_Step: self.Staple_Level = self.Staple_Step
            return_function_carbon = self.Return_Function * self.Solution_ERoEI_Carbon[i]
            norm_return_carbon = deltaQ_carbon / return_function_carbon[1]
            return_function_renewable = self.Return_Function * self.ERoEI_Renewable
            norm_return_renewable = deltaQ_renewable / return_function_renewable[1]
            useful_function = return_function_carbon + self.Invest_Function
            for j in range( len( return_function_carbon)):
                self.Production_Carbon[i+j-1] += return_function_carbon[j] * norm_return_carbon
                self.Production_Renewable[i+j-1] += return_function_renewable[j] * norm_return_renewable
                self.Production_Useful[i+j-1] += (return_function_carbon[j] + self.Invest_Function[j]) * norm_return_carbon
                self.Production_Useful[i+j-1] += (return_function_renewable[j] + self.Invest_Function[j]) * norm_return_renewable
            for j in range(3):
                crisis_norm = p_crisis**(1/(j+1))
                self.Production_Carbon[i+j] *= crisis_norm
                self.Production_Renewable[i+j] *= crisis_norm
            self.Production_PH[i] = (self.Production_Carbon[i]+self.Production_Renewable[i]) / self.Pop[i]
            self.Consumption_PH[i-1] = self.Production_Useful[i-1] / self.Pop[i-1]
            self.Solution_Q[i] = self.Solution_Q[i-1] + self.Production_Carbon[i]
        self.Solution_Q = np.clip( self.Solution_Q, 0, self.URR)
        self.Production = self.Production_Carbon + self.Production_Renewable
        self.Production_PH_Carbon = self.Production_Carbon / self.Pop
        self.Production_PH_Renewable = self.Production_Renewable / self.Pop
        self._Add_Nuclear(t0)
        self._Add_ResidentialBio_and_Animal(t0)
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
    # Expands energy data to the Big Bang and sets the initial values
    #
    def _Expand_Energy(self, t0):
        if self.Solution_Time[0] < self.Resource.Calibration_Year[0]:
            b = self.Resource.Calibration_Carbon[0] / self.q0
            qRN = self.Resource.Calibration_Renewable[0] / b 
            b **= 1/(self.Resource.Calibration_Year[0]-self.Solution_Time[0])
        self.offsetT = int(self.Resource.Calibration_Year[0] - t0[0])
        print ("Model time offset from stats: ", self.offsetT)
        print ("Model actual year: ", self.Actual_Year)
        perCapita = 0
        perCapitaRN = 0
        for i in range( len( t0)):
            t = t0[i]
            if t < self.Resource.Calibration_Year[0]:
                self.Production_Calibrated_Carbon[i] = self.q0 * b ** (t-t0[0])
                self.Production_Calibrated_Renewable[i] = qRN * b ** (t-t0[0])
                continue
            if t > self.Resource.Calibration_Year[-1]:
                self.Production_Calibrated_Carbon[i] = self.Pop[i] * perCapita
                self.Production_Calibrated_Renewable[i] = self.Pop[i] * perCapitaRN
                continue
            self.Production_Calibrated_Carbon[i] = self.Resource.Calibration_Carbon[i-self.offsetT]
            self.Production_Calibrated_Renewable[i] = self.Resource.Calibration_Renewable[i-self.offsetT]
            perCapita = self.Production_Calibrated_Carbon[i] / self.Pop[i]
            perCapitaRN = self.Production_Calibrated_Renewable[i] / self.Pop[i]

        # Initial values
        self.Solution_ERoEI_Carbon[0] = 10**self.ERoEI.Compute(0)
        return_function_carbon = self.Return_Function * self.Solution_ERoEI_Carbon[0]
        return_function_renewable = self.Return_Function * self.ERoEI_Renewable
        norm_return_carbon = self.Production_Calibrated_Carbon[0] / return_function_carbon[1]
        norm_return_renewable = self.Production_Calibrated_Renewable[0] / return_function_renewable[1]
        for j in range( len( return_function_carbon)-1):
            self.Production_Carbon[j] = norm_return_carbon * return_function_carbon[j+1]
            self.Production_Renewable[j] = norm_return_renewable * return_function_renewable[j+1]
            self.Production_Useful[j] = self.Production_Carbon[j] + norm_return_carbon * self.Invest_Function[j] 
            self.Production_Useful[j] += self.Production_Renewable[j] + norm_return_renewable * self.Invest_Function[j] 
        self.Production_PH[0] = (self.Production_Carbon[0] + self.Production_Renewable[0]) / self.Pop[0]
        self.Consumption_PH[0] = self.Production_Useful[0] / self.Pop[0]
        self.Solution_Q[0] = self.Production_Carbon[0]
        return
    #
    # Adds nuclear power production and investment
    # Note BP conversion from thermal toe to electric energy is used: 0.39
    #
    def _Add_Nuclear(self, t0):
        self.Production_Nuclear = self.Nuclear.GetVector(t0)
        self.Investment_Nuclear = self.Nuclear.GetVector(t0+50) / self.ERoEI_Nuclear 
        for i in range( len( t0)):
            t = t0[i]
            if t < 1930:
                self.Investment_Nuclear[i] = 0
            if t < 1954:
                self.Production_Nuclear[i] = 0
                continue
            if t > self.Resource.Calibration_Year[-1]: break
            self.Production_Nuclear[i] = self.Resource.Calibration_Nuclear[i-self.offsetT]
        self.Production += self.Production_Nuclear
        self.Production_Useful += self.Production_Nuclear
        self.Production_Useful -= self.Investment_Nuclear 
        self.Production_PH_Nuclear = self.Production_Nuclear/self.Pop
        self.Production_PH += self.Production_PH_Nuclear
        self.Consumption_PH += self.Production_PH_Nuclear - self.Investment_Nuclear/self.Pop
##        for i in range( len(self.Solution_Time)):
##            if self.Solution_Time[i] < 1900: continue
##            if self.Solution_Time[i] > self.Actual_Year + 50: break
##            print( "{:.0f}: {:.1f} {:.1f}".format( self.Solution_Time[i], self.Production_PH_Nuclear[i]*1000,
##                (self.Production_PH_Nuclear[i] - self.Investment_Nuclear[i]/self.Pop[i])*1000))
        return
    #
    # Adds residential biofuels and animal power (rough estimate based on IPCC data)
    #
    def _Add_ResidentialBio_and_Animal(self, t0):
        self.Production_Bio = self.Biomass.GetVector(t0)
        self.Production_Animal = self.Animal_Power.GetVector(t0)
        self.Production += self.Production_Bio + self.Production_Animal 
        self.Production_PH_Bio_Animal = (self.Production_Bio + self.Production_Animal)/self.Pop
        self.Production_PH += self.Production_PH_Bio_Animal
        self.Consumption_PH += self.Production_PH_Bio_Animal * (1-1/self.ERoEI_Biomass)
        return
    
#
# Solve numerically
#
Year = np.linspace( 1800, 2300, 501)
P = Population()
R = Resources()
eroei = Sigmoid( 501, 0.005, 2, 0)
E = Energy_Model_7( R, P.UN_Low, eroei, 40)
E.Solve( Year)
maxYear = np.argmax( E.Production)
print( "In {:g} production peak at {:.0f} mln toe".format( Year[maxYear], E.Production[maxYear]))
maxProd = np.argmax( E.Production_PH[:300])
print( "In {:g} production per person is {:.1f} kg".format( Year[maxProd], 1000*E.Production_PH[maxProd]))
maxCons = np.argmax( E.Consumption_PH[:300])
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
fig.suptitle( 'Модель энергетики Халла-Клитгаарда - Сценарии 1 и 3', fontsize=22)
gs = plt.GridSpec(2, 1, height_ratios=[1, 1]) 
ax1 = plt.subplot(gs[0])
#ax2 = plt.subplot(gs[1])
ax3 = plt.subplot(gs[1])

ax1.set_title("Население и производство")
Energy_Calibration = R.Calibration_Total+E.Production_Bio[90:218]+E.Production_Animal[90:218]
Energy_Calibration_Error = R.Calibration_Total*0.1 + (E.Production_Bio[90:218]+E.Production_Animal[90:218])*0.25
ax1.errorbar( R.Calibration_Year, Energy_Calibration, yerr=Energy_Calibration_Error, fmt=".", color="m")
ax1.plot( Year, E.Pop, "-.", lw=2, color="b", label="Население (модель ООН)")
ax1.plot( Year, E.Production_Animal, "-", lw=1, color="y", label="Мускульная сила животных")
ax1.plot( Year, E.Production_Animal + E.Production_Bio, "-", lw=1, color="g", label="+ Бытовое биотопливо")
ax1.plot( Year, E.Production_Carbon + E.Production_Animal + E.Production_Bio, "-", lw=1, color="k", label="+ Уголь, нефть, газ")
ax1.plot( Year, E.Production_Renewable + E.Production_Carbon + E.Production_Animal + E.Production_Bio, "-", lw=1, color="b", label="+ Возобновляемая")
ax1.plot( Year, E.Production, "-", lw=2, color="m", label="+ Ядерная")
ax1.plot( Year, E.Production_Useful, "--", lw=2, color="m", label="За вычетом ERoEI")
ax1.plot( [Year[maxYear],Year[maxYear]], [0,E.Production[maxYear]*1.1], "--", lw=1, color="k")
ax1.text( Year[maxYear]-75, E.Production[maxYear]*0.1, "Максимум энергии: {:.1f} млрд toe в {:g} году".format( E.Production[maxYear]/1000,Year[maxYear]))
ax1.set_xlim( x_start, x_end)
ax1.set_ylim( 0,20000)
ax1.set_ylabel("миллионов")
ax1.grid(True)
ax1.legend(loc=0)

ax3.set_title("Потребление и затраты")
ax3.plot( Year,  E.Production_PH_Bio_Animal*1000, "-", lw=1, color="g", label="Бытовое биотопливо")
ax3.plot( Year,  E.Production_PH_Renewable*1000, "-", lw=1, color="b", label="Возобновляемая энергия")
ax3.plot( Year,  E.Production_PH_Carbon*1000, "-", lw=1, color="k", label="Уголь, нефть, газ")
ax3.plot( Year,  E.Production_PH_Nuclear*1000, "-", lw=1, color="m", label="Ядерная энергия")
ax3.plot( Year,  E.Production_PH*1000, "-", lw=2, color="m", label="Энергии на душу")
ax3.plot( Year,  E.Consumption_PH*1000, "--", lw=2, color="m", label="Потребление (за вычетом ERoEI)")
ax3.plot( [Year[maxProd],Year[maxProd]], [0, E.Production_PH[maxProd]*1500], "--", lw=1, color="k")
ax3.plot( [1930, return1930], [ consumption1930*1000, consumption1930*1000], "-.", lw=1, color="k")
ax3.text( Year[maxProd] - 25,  E.Production_PH[maxProd]*1030, "Максимум энергии: {:.0f} кг на душу в {:g} году".format(1000* E.Production_PH[maxProd],Year[maxProd]))
ax3.text( 1945, consumption1930*700, "Потребление 1930 и {:g} гг: {:.0f} кг".format(return1930,consumption1930*1000))
ax3.set_xlim( x_start, x_end)
ax3.set_ylim( 0, 2300)
ax3.set_xlabel("Год")
ax3.set_ylabel("кг нефт. экв.")
ax3.grid(True)
ax3.legend(loc=2)

plt.savefig( "./Graphs/figure_16_20.png")
if InteractiveModeOn: plt.show(True)

