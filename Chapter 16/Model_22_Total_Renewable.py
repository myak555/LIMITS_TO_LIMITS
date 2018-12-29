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
# Renewable energy extraction 
# Nuclear energy estimates 
# Residential biofuels and animal power estimates 
#
class Energy_Model_7:
    def __init__( self, Resource, Population, ERoEI, q0, URR=1400e3, staple_level = 1.5):
        self.Resource = Resource
        self.Population = Population
        self.URR = URR
        self.q0 = q0
        self.ERoEI = ERoEI
        self.ERoEI_Renewable = 10
        self.ERoEI_Nuclear = 10
        self.ERoEI_Biomass = 2.5
        self.Staple_Level = staple_level
        self.Staple_Step = 0.07
        self.Staple_Minimum = 0.5
        self.Staple_Crisis_Intensity = 0.01
        self.Deprivation = 1
        self.DeprivationRN = Sigmoid( 5000,0.05,1.012,1) 
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
        self.Nuclear = Linear_Combo()
        self.Nuclear.Wavelets += [Sigmoid( x0=2052.000, s0=0.20000, left=0.000, right=400.000, shift=0.000)]
        self.Nuclear.Wavelets += [Hubbert( x0=2029.000, s0=0.20950, s1=0.13679, peak=313.613, shift=0.000)]
        self.Nuclear.Wavelets += [Hubbert( x0=2009.000, s0=0.11160, s1=0.17825, peak=299.552, shift=0.000)]
        self.Nuclear.Wavelets += [Hubbert( x0=1992.000, s0=0.38355, s1=0.26714, peak=77.826, shift=0.000)]
        self.Nuclear.Wavelets += [Hubbert( x0=2020.000, s0=0.93207, s1=0.73828, peak=32.600, shift=0.000)]
        self.Nuclear.Wavelets += [Hubbert( x0=2047.000, s0=0.31440, s1=0.47830, peak=42.322, shift=0.000)]
        return
    
    #
    # Solves for the time array given
    #
    def Solve( self, t0):
        self.Solution_Time = np.array( t0)
        self.Solution_ERoEI = np.zeros( len(t0))
        self.Production = np.zeros( len(t0))
        self.ProductionCalibrated = np.zeros( len(t0))
        self.UsefulProduction = np.zeros( len(t0))
        self.ProductionRN = np.zeros( len(t0))
        self.ProductionCalibratedRN = np.zeros( len(t0))
        self.UsefulProductionRN = np.zeros( len(t0))
        self.Production_PH = np.zeros( len(t0))
        self.Consumption_PH = np.zeros( len(t0))
        self.Solution_Q = np.zeros( len(t0))
        self.Pop = self.Population.GetVector( t0)
        self._Expand_Energy( t0)

        # Carbon and renewable run
        for i in range( 1,len(t0)-len(self.Return_Function)):
            self.Solution_ERoEI[i] = 10**self.ERoEI.Compute( self.Solution_Q[i-1]/1000)
            if t0[i] > 2017:
                #break #Uncomment to kill investments in 2018
                deltaQ = self.Production[i-1] * self.Pop[i] / self.Pop[i-1] * self.Deprivation
                deltaQRN = self.ProductionRN[i-1] * self.Pop[i] / self.Pop[i-1] * self.DeprivationRN.Compute(self.ProductionRN[i-1])
                deltaQ -= self.Production[i]
                deltaQRN -= self.ProductionRN[i]
            else:
                deltaQ = self.ProductionCalibrated[i] - self.Production[i]
                deltaQRN = self.ProductionCalibratedRN[i] - self.ProductionRN[i]
            if deltaQ < 0:
                #print( "Degrowth Carbon: {:g} {:.1f}".format( t0[i], deltaQ) )
                deltaQ = 0
                if t0[i] <= 2017: # stick to actual
                    self.Production[i] = self.ProductionCalibrated[i]
                    self.UsefulProduction[i-1] = self.ProductionCalibrated[i-1] * (1-1/self.Solution_ERoEI[i-1])
            if deltaQRN < 0:
                #print( "Degrowth Renewable: {:g} {:.1f}".format( t0[i], deltaQRN) )
                deltaQRN = 0
                if t0[i] <= 2017: # stick to actual
                    self.ProductionRN[i] = self.ProductionCalibratedRN[i]
                    self.UsefulProductionRN[i-1] = self.ProductionCalibratedRN[i-1] * (1-1/self.ERoEI_Renewable)
            sump = np.sum( self.Production)
            if sump + self.Solution_ERoEI[i]*deltaQ >= self.URR:
                deltaQ = (self.URR - sump) * self.Staple_Crisis_Intensity / self.Solution_ERoEI[i]
                if deltaQ < 0: deltaQ = 0
            if t0[i] > 2017:
                cl = (self.Consumption_PH[i-2] + self.Consumption_PH[i-3] + self.Consumption_PH[i-4]) / 3
                if cl < self.Staple_Level:
                    print( "Crisis: {:g} {:.1f} < {:.1f}".format( t0[i], cl, self.Staple_Level) )
                    deltaQ *= self.Staple_Crisis_Intensity
                    deltaQRN *= self.Staple_Crisis_Intensity
                    self.Staple_Level -= self.Staple_Step
                    if self.Staple_Level < self.Staple_Minimum: self.Staple_Level = self.Staple_Minimum
            return_function = self.Return_Function * self.Solution_ERoEI[i]
            return_functionRN = self.Return_Function * self.ERoEI_Renewable
            norm_return = deltaQ / return_function[1]
            norm_returnRN = deltaQRN / return_functionRN[1]
            useful_function = return_function + self.Invest_Function
            useful_functionRN = return_functionRN + self.Invest_Function
            for j in range( len( return_function)):
                self.Production[i+j-1] += return_function[j] * norm_return
                self.ProductionRN[i+j-1] += return_functionRN[j] * norm_returnRN
                self.UsefulProduction[i+j-1] += useful_function[j] * norm_return
                self.UsefulProductionRN[i+j-1] += useful_functionRN[j] * norm_returnRN
            self.Production_PH[i] = (self.Production[i] + self.ProductionRN[i]) / self.Pop[i]
            self.Consumption_PH[i-1] = (self.UsefulProduction[i-1] + self.UsefulProductionRN[i-1]) / self.Pop[i-1]
            self.Solution_Q[i] = self.Solution_Q[i-1] + self.Production[i]
        self.Solution_Q = np.clip( self.Solution_Q, 0, self.URR)
        self.Production_Carbon = np.array( self.Production)
        self.UsefulProduction_Carbon = np.array( self.UsefulProduction)
        self.Production += self.ProductionRN
        self.UsefulProduction += self.UsefulProductionRN
        maxCons = 1-0.5/self.ERoEI_Renewable
        self.UsefulProduction = np.clip( self.UsefulProduction, 0, maxCons * self.Production)
        self.Production_PH = self.Production / self.Pop
        self.Consumption_PH = self.UsefulProduction / self.Pop

        self._Add_Nuclear(t0)
        self._Add_ResidentialBio_and_Animal(t0)
        return    

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
        perCapita = 0
        perCapitaRN = 0
        for i in range( len( t0)):
            t = t0[i]
            if t < self.Resource.Calibration_Year[0]:
                self.ProductionCalibrated[i] = self.q0 * b ** (t-t0[0])
                self.ProductionCalibratedRN[i] = qRN * b ** (t-t0[0])
                continue
            if t > self.Resource.Calibration_Year[-1]:
                self.ProductionCalibrated[i] = self.Pop[i] * perCapita
                self.ProductionCalibratedRN[i] = self.Pop[i] * perCapitaRN
                continue
            self.ProductionCalibrated[i] = self.Resource.Calibration_Carbon[i-self.offsetT]
            self.ProductionCalibratedRN[i] = self.Resource.Calibration_Renewable[i-self.offsetT]
            perCapita = self.ProductionCalibrated[i] / self.Pop[i]
            perCapitaRN = self.ProductionCalibratedRN[i] / self.Pop[i]

        # Initial values
        self.Solution_ERoEI[0] = 10**self.ERoEI.Compute(0)
        return_function = self.Return_Function * self.Solution_ERoEI[0]
        return_functionRN = self.Return_Function * self.ERoEI_Renewable
        norm_return = self.ProductionCalibrated[0] / return_function[1]
        norm_returnRN = self.ProductionCalibratedRN[0] / return_functionRN[1]
        for j in range( len( return_function)-1):
            self.Production[j] = norm_return * return_function[j+1]
            self.ProductionRN[j] = norm_returnRN * return_functionRN[j+1]
            self.UsefulProduction[j] = self.Production[j] + norm_return * self.Invest_Function[j] 
            self.UsefulProductionRN[j] = self.ProductionRN[j] + norm_returnRN * self.Invest_Function[j] 
        self.Production_PH[0] = (self.Production[0] + self.ProductionRN[0]) / self.Pop[0]
        self.Consumption_PH[0] = (self.UsefulProduction[0] + self.UsefulProductionRN[0]) / self.Pop[0]
        self.Solution_Q[0] = self.Production[0]
        return

    #
    # Adds nuclear power production and investment
    # Note BP conversion from GW*years to mln toe is used 0.2263 * 8.766
    #
    def _Add_Nuclear(self, t0):
        self.Production_Nuclear = self.Nuclear.GetVector(t0) * 0.2263 * 8.766
        for i in range( len( t0)):
            t = t0[i]
            if t < 1954:
                self.Production_Nuclear[i] = 0
                continue
            if t > self.Resource.Calibration_Year[-1]: break
            self.Production_Nuclear[i] = self.Resource.Calibration_Nuclear[i-self.offsetT]
        self.Investment_Nuclear = self.Nuclear.GetVector(t0+50) * 0.2263 * 8.766 / self.ERoEI_Nuclear 
        self.Production += self.Production_Nuclear
        self.UsefulProduction += self.Production_Nuclear
        self.UsefulProduction -= self.Investment_Nuclear 
        eNuc = self.Production_Nuclear/self.Pop
        self.Production_PH += eNuc
        self.Consumption_PH += eNuc - self.Investment_Nuclear/self.Pop  
        return

    #
    # Adds residential biofuels and animal power
    #
    def _Add_ResidentialBio_and_Animal(self, t0):
        self.Production_Bio = self.Biomass.GetVector(t0)
        self.Production_Animal = self.Animal_Power.GetVector(t0)
        eBio = self.Production_Bio/self.Pop + self.Production_Animal/self.Pop
        self.Production_PH += eBio
        self.Consumption_PH += eBio * (1-1/self.ERoEI_Biomass)
        return
           
#
# Solve numerically
#
Year = np.linspace( 1800, 2300, 501)
P = Population()
R = Resources()
eroei = Sigmoid( 501, 0.005, 2, 0)
E = Energy_Model_7( R, P.UN_Medium, eroei, 40)
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
return1930 = 0
consumption1930 = 0
for i in range( len( Year)):
    if Year[i] == 1930:
        consumption1930 = E.Consumption_PH[i]
        print( "In {:g} per head production  {:.0f} кг and consumption {:.0f} кг".format( Year[i], E.Production_PH[i]*1000, consumption1930*1000))
    if return1930 == 0 and consumption1930>0 and E.Consumption_PH[i] < consumption1930:
        return1930 = Year[i]
        print( "In {:g} per head production  {:.0f} кг and consumption {:.0f} кг".format( return1930, E.Production_PH[i]*1000, E.Consumption_PH[i]*1000))
        break

x_start, x_end = 1850, 2150

fig = plt.figure( figsize=(15,10))
fig.suptitle( 'Модель энергетики с добавкой ВИЭ и ЯЭ', fontsize=22)
gs = plt.GridSpec(2, 1, height_ratios=[1, 1]) 
ax1 = plt.subplot(gs[0])
ax2 = plt.subplot(gs[1])

ax1.set_title("Население и производство энергии")
ax1.errorbar( R.Calibration_Year, R.Calibration_Carbon, yerr=R.Calibration_Carbon*0.05, fmt=".", color="#404040")
ax1.errorbar( R.Calibration_Year, R.Calibration_Total, yerr=R.Calibration_Total*0.05, fmt=".", color="m")
ax1.plot( Year, E.Pop, "-", lw=2, color="b", label="Население (модель ООН)")
ax1.plot( Year, E.ProductionRN, "-", lw=2, color="g")
ax1.plot( Year, E.Production_Carbon, "-", lw=2, color="#404040", label="Уголь, нефть и газ")
ax1.plot( Year, E.Production, "-", lw=2, color="m", label="Низкоэнтропийная, включая ВИЭ и ЯЭ")
ax1.plot( Year, E.UsefulProduction_Carbon, "--", lw=2, color="#404040", label="За вычетом ERoEI")
ax1.plot( Year, E.UsefulProduction, "--", lw=2, color="m")
ax1.plot( [Year[maxYear],Year[maxYear]], [0,E.Production[maxYear]*1.1], "--", lw=1, color="k")
ax1.text( Year[maxYear]-75, E.Production[maxYear]*0.1, "Максимум энергии: {:.1f} млрд toe в {:g} году".format( E.Production[maxYear]/1000,Year[maxYear]))
ax1.text( 1900, 7500, "ERoEI ЯЭ  : {:.1f}".format( E.ERoEI_Nuclear))
ax1.text( 1900, 6000, "ERoEI ВИЭ: {:.1f}".format( E.ERoEI_Renewable))
ax1.set_xlim( x_start, x_end)
ax1.set_ylim( 0,20000)
ax1.set_ylabel("миллионов")
ax1.grid(True)
ax1.legend(loc=0)

ax2.set_title("Потребление и затраты (включая сжигание биомассы в быту)")
ax2.plot( Year,  E.Production_PH*1000, "-", lw=2, color="g", label="Энергии на душу")
ax2.plot( Year,  E.Consumption_PH*1000, "--", lw=2, color="g", label="Потребление (за вычетом ERoEI)")
ax2.plot( [Year[maxProd],Year[maxProd]], [0, E.Production_PH[maxProd]*1500], "--", lw=1, color="k")
ax2.plot( [1930, return1930], [ consumption1930*1000, consumption1930*1000], "-.", lw=1, color="k")
ax2.text( Year[maxProd] - 25,  E.Production_PH[maxProd]*1030, "Максимум энергии: {:.0f} кг на душу в {:g} году".format(1000* E.Production_PH[maxProd],Year[maxProd]))
ax2.text( 1945, consumption1930*700, "Потребление 1930 и {:g} гг: {:.0f} кг".format(return1930,consumption1930*1000))
ax2.set_xlim( x_start, x_end)
ax2.set_ylim( 0, 2200)
ax2.set_xlabel("Год")
ax2.set_ylabel("кг нефт. экв.")
ax2.grid(True)
ax2.legend(loc=2)

plt.savefig( ".\\Graphs\\figure_16_22.png")
fig.show()

