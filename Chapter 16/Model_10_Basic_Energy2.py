from Predictions import *

#
# Basic Energy Model (after C.Hall and K.Kleatgaard)
# Using investment and return functions defined as exponential decline
# Resource - actual energy production (mln toe)
# Population - population function (mln)
# q0>0 - assumed energy production at T0 (mln toe)
# URR - total recoverable resources (mln toe)
#
class Energy_Model_2:
    def __init__( self, Resource, Population, q0, URR=1400e3, ERoEI=20, d_invest=0.2, d_return=0.05):
        self.Resource = Resource
        self.Population = Population
        self.URR = URR
        self.q0 = q0
        self.ERoEI = ERoEI
        self.Return_Function = np.zeros( 100)
        for i in range( 1, len( self.Return_Function)):
            self.Return_Function[i] = (1-d_return)**(i-1)
        norm = ERoEI / np.sum( self.Return_Function)
        self.Return_Function *= norm
        self.Invest_Function = np.zeros( 100)
        for i in range( len( self.Invest_Function)):
            self.Invest_Function[i] = (1-d_invest)**i
        norm = -1 / np.sum( self.Invest_Function)
        self.Invest_Function *= norm
        self.Useful_Function = self.Return_Function + self.Invest_Function
        return
    def Solve( self, t0):
        self.Solution_Time = np.array( t0)
        self.Production = np.zeros( len(t0))
        self.ProductionCalibrated = np.zeros( len(t0))
        self.UsefulProduction = np.zeros( len(t0))
        self.Production_PH = np.zeros( len(t0))
        self.Consumption_PH = np.zeros( len(t0))
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
        norm_return = self.ProductionCalibrated[0] / self.Return_Function[1]
        for j in range( len( self.Return_Function)-1):
            self.Production[j] = norm_return * self.Return_Function[j+1]
            self.UsefulProduction[j] = self.Production[j] + norm_return * self.Invest_Function[j] 
        self.Production_PH[0] = self.Production[0] / self.Pop[0]
        self.Consumption_PH[0] = self.UsefulProduction[0] / self.Pop[0]
        
        # Propagate
        for i in range( 1,len(t0)-len(self.Return_Function)):
            if t0[i] > 2017:
                #break
                deltaQ = self.Production[i-1] * self.Pop[i] / self.Pop[i-1] - self.Production[i]   
            else:
                deltaQ = self.ProductionCalibrated[i] - self.Production[i]
            sump = np.sum( self.Production)
            if sump >= self.URR-self.ERoEI*deltaQ:
                deltaQ = 0
            if deltaQ < 0:
                print( "Degrowth: {:g} {:.1f}".format( t0[i], deltaQ) )
                deltaQ = 0
            norm_return = deltaQ / self.Return_Function[1]
            for j in range( len( self.Return_Function)):
                self.Production[i+j-1] += self.Return_Function[j] * norm_return
                self.UsefulProduction[i+j-1] += self.Useful_Function[j] * norm_return
            self.Production_PH[i] = self.Production[i] / self.Pop[i]
            self.Consumption_PH[i-1] = self.UsefulProduction[i-1] / self.Pop[i-1]

        # Compute presentations
        pop = self.Population.GetVector( t0)
        self.Solution_Q = np.array( self.Production)
        for i in range( 1,len( t0)):
            self.Solution_Q[i] += self.Solution_Q[i-1]
        return

#
# Solve numerically
#
Year = np.linspace( 1800, 2300, 501)
P = Population()
R = Resources()
E = Energy_Model_2( R, P.UN_Medium, 40)
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
        
YearS = np.linspace( 0, 99, len(E.Invest_Function))
fig = plt.figure( figsize=(15,6))
plt.plot( YearS, E.Invest_Function, "-", lw=2, color="r", label="Затраты")
plt.plot( YearS, E.Return_Function, "-", lw=2, color="g", label="Доходы")
plt.grid(True)
plt.xlabel("Год")
plt.xlim( -1, 100)
plt.legend(loc=0)
plt.savefig( "./Graphs/figure_16_10a.png")
fig.show()

x_start, x_end = 1850, 2150

fig = plt.figure( figsize=(15,15))
fig.suptitle( 'Простейшая модель энергетики', fontsize=22)
gs = plt.GridSpec(3, 1, height_ratios=[1, 1, 1]) 
ax1 = plt.subplot(gs[0])
ax2 = plt.subplot(gs[1])
ax3 = plt.subplot(gs[2])

ax1.set_title("Население и годовая добыча")
ax1.errorbar( R.Calibration_Year, R.Calibration_Carbon, yerr=R.Calibration_Carbon*0.05, fmt=".", color="k", label="Реальная добыча")
ax1.plot( Year, E.Pop, "-", lw=2, color="b", label="Население (модель ООН)")
ax1.plot( Year, E.Production, "-", lw=2, color="k", label="Годовая добыча")
ax1.plot( Year, E.UsefulProduction, "--", lw=2, color="k", label="За вычетом ERoEI")
ax1.plot( [Year[maxYear],Year[maxYear]], [0,E.Production[maxYear]*1.1], "--", lw=1, color="k")
ax1.text( Year[maxYear]-75, E.Production[maxYear]*0.1, "Максимум энергии: {:.1f} млрд toe в {:g} году".format( E.Production[maxYear]/1000,Year[maxYear]))
ax1.set_xlim( x_start, x_end)
ax1.set_ylim( 0,18000)
ax1.set_ylabel("миллионов")
ax1.grid(True)
ax1.legend(loc=0)

ax2.set_title("Извлекаемые запасы и накопленная добыча")
ax2.plot( [Year[0],Year[-1]], [E.URR/1000,E.URR/1000], "-.", lw=1, color="k", label="URR={:.0f} млрд тонн".format(E.URR/1000))
ax2.plot( Year, E.Solution_Q/1000, "-", lw=2, color="k", label="Накопленная добыча")
ax2.plot( [Year[endProd],Year[endProd]], [0,E.Solution_Q[endProd]*1.1/1000], "--", lw=1, color="k")
ax2.text( Year[endProd] - 150, E.URR/2000, "Окончание добычи: {:.0f} млрд toe в {:g} году".format( E.Solution_Q[endProd]/1000,Year[endProd]))
ax2.text( x_start + 10, 1000, "Фиксированный ERoEI: {:.1f}".format( E.ERoEI))
ax2.set_xlim(x_start, x_end)
ax2.set_ylim( 0, 1500)
ax2.set_ylabel("млрд тонн")
ax2.grid(True)
ax2.legend(loc=0)

ax3.set_title("Потребление и затраты")
ax3.plot( Year,  E.Production_PH*1000, "-", lw=2, color="k", label="Добыча на душу")
ax3.plot( Year,  E.Consumption_PH*1000, "--", lw=2, color="k", label="Потребление (за вычетом ERoEI)")
ax3.plot( [Year[maxProd],Year[maxProd]], [0, E.Production_PH[maxProd]*1500], "--", lw=1, color="k")
ax3.plot( [1930, return1930], [ consumption1930*1000, consumption1930*1000], "-.", lw=1, color="k")
ax3.text( Year[maxProd] - 25,  E.Production_PH[maxProd]*1030, "Максимум добычи: {:.0f} кг на душу в {:g} году".format(1000* E.Production_PH[maxProd],Year[maxProd]))
ax3.text( 1945, consumption1930*700, "Потребление 1930 и {:g} гг: {:.0f} кг".format(return1930,consumption1930*1000))
ax3.set_xlim( x_start, x_end)
ax3.set_ylim( 0, 2000)
ax3.set_xlabel("Год")
ax3.set_ylabel("кг нефт. экв.")
ax3.grid(True)
ax3.legend(loc=2)

plt.savefig( "./Graphs/figure_16_10.png")
fig.show()

