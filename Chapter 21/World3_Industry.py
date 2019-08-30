from World3_Model import *

class W3_Resources:
    """
    Describes resources subsystem similar to World3 implementation
    """
    def __init__( self, year0=1890, verbose=False):
        self.Initial_Fossil_Fuel = 1400e3           # mln tonn
        self.Fossil_Fuel = self.Initial_Fossil_Fuel
        self.Fossil_Fuel_Usage_Factor = 11
        self.Fossil_Fuel_Remaining_Fraction = 1
        self.Fossil_Fuel_Extraction = 0
        self.FOC_Reserves_Model = Sigmoid( 0.5, 10, 0.01, 0.60)
        if verbose:
            print( "Resources in {:.0f}: ".format( year0))
            print( "   Fossil fuel                   {:>5.1f} mln tonn".format( self.Initial_Fossil_Fuel))
        return
    def Plot_FOC_Functions( self, filename = "./Graphs/figure_21_01.png"):
        """
        Test plot
        """
        fig = plt.figure( figsize=(15,8))
        fig.suptitle('Зависимость FOC от истощения ископаемого топлива', fontsize=25)
        gs = plt.GridSpec(1, 1) 
        ax1 = plt.subplot(gs[0])
        fraction_remaining = np.linspace( 0, 1, 101)
        ax1.plot( fraction_remaining, self.FOC_Reserves_Model.GetVector(fraction_remaining),
                  "-", lw=2)
        ax1.set_xlim( 0, 1)
        ax1.set_ylim( 0, 1)
        ax1.grid(True)
        #ax1.legend(loc=0)
        ax1.set_xlabel("Остаток ископаемого топлива")
        ax1.set_ylabel("Доля промышленного капитала на извлечение")
        plt.savefig( filename)
        return
    def Compute_Next_Year( self, population):
        """
        Calculates next year in the model
        """
        self.Fossil_Fuel_Extraction = population.Goods * self.Fossil_Fuel_Usage_Factor
        self.Fossil_Fuel -= self.Fossil_Fuel_Extraction
        self.Fossil_Fuel = Limit( self.Fossil_Fuel, min_y=0, max_y=self.Initial_Fossil_Fuel)
        self.Fossil_Fuel_Remaining_Fraction = self.Fossil_Fuel / self.Initial_Fossil_Fuel
        self.FOC = self.FOC_Reserves_Model.Compute( self.Fossil_Fuel_Remaining_Fraction)
        return
    

class W3_Industrial_Capital:
    """
    Describes industrial capital subsystem
    """
    def __init__( self, year0=1890, initial=100, lifetime=25, output_ratio=1.0, verbose=False):
        self.Total = initial
        self.Lifetime = lifetime # years
        self.Depreciation = 1-np.exp(-1.0/self.Lifetime)
        self.Output_Ratio = output_ratio
        self.Output = 0.0
        if verbose:
            print( "Industrial capital in {:.0f}: ".format( year0))
            print( "   Total                 {:>5.1f} mln tonn".format( self.Total))
            print( "   Average lifetime      {:>5.1f} years".format( self.Lifetime))
            print( "   Average depreciation  {:>5.3f} per year".format( self.Depreciation))
        return
    def Compute_Next_Year( self, resources, investment=0):
        """
        Calculates next year in the model
        """
        self.Output = resources.FOC * self.Total * self.Output_Ratio
        self.Total = self.Total * (1-self.Depreciation) + investment
        return


class W3_Service_Capital:
    """
    Describes service capital subsystem
    """
    def __init__( self, year0=1890, initial=100, lifetime=10, output_ratio=1.0, verbose=False):
        self.Total = initial
        self.Lifetime = lifetime # years
        self.Depreciation = 1-np.exp(-1.0/self.Lifetime)
        self.Output_Ratio = output_ratio
        self.Output = 0.0
        self.Indicated_Per_Capita_Model = Sigmoid( 250, 0.012, 0.35, 0.05)
        self.Indicated_Per_Capita_Model.Plot(0,600)
        if verbose:
            print( "Service capital in {:.0f}: ".format( year0))
            print( "   Total                 {:>5.1f} mln tonn".format( self.Total))
            print( "   Average lifetime      {:>5.1f} years".format( self.Lifetime))
            print( "   Average depreciation  {:>5.3f} per year".format( self.Depreciation))
        return
    def Compute_Indicated_Investment( self, population):
        """
        Calculates indicative part of industrial output dedicated to service capital
        """
        return self.Indicated_Food_Per_Capita_Model.Compute( population.FoodPC)
    def Compute_Next_Year( self, resources, investment=0):
        """
        Calculates next year in the model
        """
        self.Output = self.Total * self.Output_Ratio
        self.Total = self.Total * (1-self.Depreciation) + investment
        return


class W3_Agriculture_Capital:
    """
    Describes service capital subsystem
    """
    def __init__( self, year0=1890, initial=100, lifetime=15, output_ratio=1.0, verbose=False):
        self.Total = initial
        self.Lifetime = lifetime # years
        self.Depreciation = 1-np.exp(-1.0/self.Lifetime)
        self.Output_Ratio = output_ratio
        self.Output = 0.0
        self.Indicated_Per_Capita_Model = Sigmoid( 250, 0.012, 0.55, 0.05)
        #self.Indicated_Per_Capita_Model.Plot(0,600)
        if verbose:
            print( "Agriculture capital in {:.0f}: ".format( year0))
            print( "   Total                 {:>5.1f} mln tonn".format( self.Total))
            print( "   Average lifetime      {:>5.1f} years".format( self.Lifetime))
            print( "   Average depreciation  {:>5.3f} per year".format( self.Depreciation))
        return
    def Compute_Indicated_Investment( self, population):
        """
        Calculates indicative part of industrial output dedicated to agriculture capital
        """
        return self.Indicated_Per_Capita_Model.Compute( population.FoodPC)
    def Compute_Next_Year( self, resources, investment=0):
        """
        Calculates next year in the model
        """
        self.Output = self.Total * self.Output_Ratio
        self.Total = self.Total * (1-self.Depreciation) + investment
        return


class W3_Model:
    """
    Describes capital subsystem similar to World3 implementation
    year0 - starting model year, increment 1 year
    """
    def __init__( self, year0=1890, goodsPC=25.0, foodPC=270.0, servicesPC=100.0, biological_TFR=6.0, verbose=False):
        self.Population = W3_Population( year0, goodsPC, foodPC, servicesPC, biological_TFR, verbose)
        self.Resources = W3_Resources( year0, verbose=verbose)
        self.Industrial_Capital = W3_Industrial_Capital( year0, verbose=verbose)        
        self.Service_Capital = W3_Service_Capital( year0, verbose=verbose)        
        self.Agriculture_Capital = W3_Agriculture_Capital( year0, verbose=verbose)        
        return
    def Compute_Next_Year( self, goods=None, food=None, services=None, pollution=None, m2f=None, dleb=None):
        """
        Calculates next year in the model
        """
        #
        # fake parameter for testing
        #
        reinvestment_last_year = 0.15 * goods
        self.Population.Compute_Next_Year( goods, food, services, pollution, m2f, dleb)
        self.Resources.Compute_Next_Year( self.Population)
        self.Industrial_Capital.Compute_Next_Year( self.Resources, reinvestment_last_year)
        self.Service_Capital.Compute_Next_Year( self.Resources, reinvestment_last_year)
        self.Agriculture_Capital.Compute_Next_Year( self.Resources, reinvestment_last_year)
        return
    def _prepare_check(self):
        self.P0 = Population()
        self.P1 = Interpolation_BAU_1972()
        self.P2 = Interpolation_BAU_2012()
        self.R0 = Resources()
        self.W3_mod = Interpolation_BAU_2002()
        self.W3_mod.Solve( np.linspace(1890, 2100, 211))
        self.P0.Solve(self.W3_mod.Time)
        self.P1.Solve(self.W3_mod.Time)
        self.P2.Solve(self.W3_mod.Time)
        self.R0.Solve(self.W3_mod.Time)
        l = len( self.W3_mod.Time)
        self.POP_Actual = np.zeros(l)
        self.Fossil_Fuel_Actual = np.zeros(l)
        self.Industrial_Capital_Actual = np.zeros(l)
        self.Industrial_Output_Actual = np.zeros(l)
        self.Service_Capital_Actual = np.zeros(l)
        self.Service_Output_Actual = np.zeros(l)
        self.Agriculture_Capital_Actual = np.zeros(l)
        self.Agriculture_Output_Actual = np.zeros(l)
        self.GoodsPC_Actual = np.zeros(l)
        self.FoodPC_Actual = np.zeros(l)
        self.ServicesPC_Actual = np.zeros(l)
        return
    def Plot_Fossil_Fuel( self, filename = "./Graphs/figure_21_02.png"):
        """
        Test plot for fossil fuel production
        """
        self._prepare_check()
        conversion = 0.94
        for i,y in enumerate(self.W3_mod.Time):
            self.POP_Actual[i] = self.Population.Demographics.Total
            self.GoodsPC_Actual[i] = self.Population.GoodsPC
            self.FoodPC_Actual[i] = self.Population.FoodPC
            self.ServicesPC_Actual[i] = self.Population.ServicesPC
            self.Fossil_Fuel_Actual[i] = self.Resources.Fossil_Fuel 
            self.Compute_Next_Year(goods=self.W3_mod.Goods[i]*conversion,
                                 food=self.W3_mod.Food[i]*conversion,
                                 services=self.W3_mod.Services[i]*conversion)
        limits = 1900, 2100

        fig = plt.figure( figsize=(15,15))
        fig.suptitle('Проверка модели "World3": ископаемое топливо', fontsize=25)
        gs = plt.GridSpec(3, 1) 
        ax1 = plt.subplot(gs[0])
        ax2 = plt.subplot(gs[1])
        ax3 = plt.subplot(gs[2])

        ax1.plot( self.W3_mod.Time, self.P1.Resources/1000, "-.", lw=2, color="b", label="World3, 1972")
        ax1.plot( self.W3_mod.Time, self.W3_mod.Resources/1000, ".", lw=1, color="b", label="World3, 2003")
        ax1.plot( self.W3_mod.Time, self.P2.Resources/1000, "--", lw=2, color="b", label="Й.Рандерс, 2012")
        ax1.plot( self.W3_mod.Time, self.Fossil_Fuel_Actual/1000, "-", lw=3, color="g", label="Наша модель")
        ax1.set_xlim( limits)
##        ax2.set_ylim( 0, 700)
        ax1.grid(True)
        ax1.legend(loc=0)
        ax1.set_ylabel("Извлекаемые запасы [млрд т]")

        ax2.plot( self.W3_mod.Time, self.P1.Energy/1000, "-.", lw=2, color="b", label="World3, 1972")
        ax2.plot( self.W3_mod.Time, self.W3_mod.Energy/1000, ".", lw=2, color="b", label="World3, 2003")
        ax2.plot( self.W3_mod.Time, self.P2.Energy_Carbon/1000, "--", lw=2, color="b", label="Й.Рандерс, 2012")
        ax2.plot( self.W3_mod.Time, -Rate(self.Fossil_Fuel_Actual)/1000, "-", lw=3, color="g", label="Наша модель")
        ax2.errorbar( self.R0.Calibration_Year, self.R0.Calibration_Carbon/1000,
                      yerr=self.R0.Calibration_Carbon/20000, fmt=".", color="k", label="Реальная добыча [млрд т]")
        ax2.set_xlim( limits)
        ax2.set_ylim( 0, 25)
        ax2.grid(True)
        ax2.legend(loc=0)
        ax2.set_ylabel("Годовая добыча [млрд т]")

        ax3.plot( self.W3_mod.Time, self.P1.Population/1000, "-.", lw=2, color="b", label="World3, 1972")
        ax3.plot( self.W3_mod.Time, self.W3_mod.Population/1000, ".", lw=1, color="b", label="World3, 2003")
        ax3.plot( self.W3_mod.Time[110:], self.P0.Solution_UN_Medium[110:]/1000,
                  "-.", lw=2, color="r",  alpha=0.5, label="Средняя оценка ООН, 2015")
        ax3.plot( self.W3_mod.Time, self.P2.Population/1000, "--", lw=2, color="b", label="Й.Рандерс, 2012")
        ax3.plot( self.W3_mod.Time, self.POP_Actual/1000, "-", lw=4, color="g", alpha=0.5, label="наша модель")
        ax3.errorbar(self.P0.Calibration_Year, self.P0.Calibration_Total/1000, yerr=self.P0.Calibration_Yerr/1000,
                     fmt=".", color="k", label="Реальная популяция (ООН)")
        ax3.set_xlim( limits)
        ax3.set_ylim( 0, 12)
        ax3.grid(True)
        ax3.legend(loc=0)
        ax3.set_xlabel("Год")
        ax3.set_ylabel("популяция, млрд")
        plt.savefig( filename)
        return

    def Plot_Capital( self, filename = "./Graphs/figure_21_03.png"):
        """
        Test plot for industrial capital
        """
        self._prepare_check()
        conversion = 0.94
        for i,y in enumerate(self.W3_mod.Time):
            self.POP_Actual[i] = self.Population.Demographics.Total
            self.GoodsPC_Actual[i] = self.Population.GoodsPC
            self.FoodPC_Actual[i] = self.Population.FoodPC
            self.ServicesPC_Actual[i] = self.Population.ServicesPC
            self.Industrial_Capital_Actual[i] = self.Industrial_Capital.Total 
            self.Industrial_Output_Actual[i] = self.Industrial_Capital.Output 
            self.Service_Capital_Actual[i] = self.Service_Capital.Total 
            self.Service_Output_Actual[i] = self.Service_Capital.Output 
            self.Agriculture_Capital_Actual[i] = self.Agriculture_Capital.Total 
            self.Agriculture_Output_Actual[i] = self.Agriculture_Capital.Output 
            self.Compute_Next_Year(goods=self.W3_mod.Goods[i]*conversion,
                                 food=self.W3_mod.Food[i]*conversion,
                                 services=self.W3_mod.Services[i]*conversion)

        limits = 1900, 2100

        fig = plt.figure( figsize=(15,15))
        fig.suptitle('Проверка модели "World3": капитал и производство', fontsize=25)
        gs = plt.GridSpec(3, 1) 
        ax1 = plt.subplot(gs[0])
        ax2 = plt.subplot(gs[1])
        ax3 = plt.subplot(gs[2])

        ax1.plot( self.W3_mod.Time, self.Industrial_Capital_Actual/1000, "-", lw=3, color="r", label="Промышленность")
        ax1.plot( self.W3_mod.Time, self.Agriculture_Capital_Actual/1000, "-", lw=3, color="g", label="Сельское хозяйство")
        ax1.plot( self.W3_mod.Time, self.Service_Capital_Actual/1000, "-", lw=3, color="m", label="Услуги")
##        j = np.argmax(GoodsPC_Actual)
##        t = W3_mod.Time[j]
##        v = GoodsPC_Actual[j]
##        ax2.plot( [t, t], [v-100,v+70], "--", lw=1, color="r")
##        ax2.text( t-10, v+80, "{:.0f} кг в {:.0f} году".format( v, t), fontsize=12, color="r")
##        j = np.argmax(FoodPC_Actual)
##        t = W3_mod.Time[j]
##        v = FoodPC_Actual[j]
##        ax2.plot( [t, t], [v-100,v+100], "--", lw=1, color="g")
##        ax2.text( t-10, v-130, "{:.0f} кг в {:.0f} году".format( v, t), fontsize=12, color="g")
##        j = np.argmax(ServicesPC_Actual)
##        t = W3_mod.Time[j]
##        v = ServicesPC_Actual[j]
##        ax2.plot( [t, t], [v-100,v+40], "--", lw=1, color="m")
##        ax2.text( t-20, v+50, "{:.0f} усл. $ в {:.0f} году".format( v, t), fontsize=12, color="m")
        ax1.set_xlim( limits)
##        ax2.set_ylim( 0, 700)
        ax1.grid(True)
        ax1.legend(loc=0)
        ax1.set_ylabel("Капитал [млрд т]")

        ax2.plot( self.W3_mod.Time, self.W3_mod.Goods/1000, "-.", lw=2, color="r", label="Промтовары World3, 2003 [млрд т]")
        ax2.plot( self.W3_mod.Time, self.W3_mod.Food/1000, "-.", lw=2, color="g", label="Продовольствие World3, 2003 [млрд т]")
        ax2.plot( self.W3_mod.Time, self.W3_mod.Services/1000, "-.", lw=2, color="m", label="Услуги World3, 2003 [трлн усл.$]")
        ax2.plot( self.W3_mod.Time, self.Industrial_Output_Actual/1000, "-", lw=4, alpha=0.5, color="r", label="Наша модель")
        ax2.plot( self.W3_mod.Time, self.Service_Output_Actual/1000, "-", lw=4, alpha=0.5, color="g")
        ax2.plot( self.W3_mod.Time, self.Agriculture_Output_Actual/1000, "-", lw=4, alpha=0.5, color="m")
        #j = np.argmax(W3_mod.Goods)
        #t = W3_mod.Time[j]
        #v = W3_mod.Goods[j] / 1000
        #ax2.plot( [t, t], [v-0.5,v+0.5], "--", lw=1, color="r")
        #ax2.text( t-10, v+0.6, "{:.1f} млрд т в {:.0f} году".format( v, t), fontsize=12, color="r")
        #j = np.argmax(W3_mod.Food)
        #t = W3_mod.Time[j]
        #v = W3_mod.Food[j] / 1000
        #ax2.plot( [t, t], [v-0.5,v+0.5], "--", lw=1, color="g")
        #ax2.text( t-10, v-0.6, "{:.1f} млрд т в {:.0f} году".format( v, t), fontsize=12, color="g")
        #j = np.argmax(W3_mod.Services)
        #t = W3_mod.Time[j]
        #v = W3_mod.Services[j] / 1000
        #ax2.plot( [t, t], [v-0.5,v+0.5], "--", lw=1, color="m")
        #ax2.text( t-45, v, "{:.1f} трлн усл.$ в {:.0f} году".format( v, t), fontsize=12, color="m")
        ax2.set_xlim( limits)
        #ax2.set_ylim( 0, 1.5)
        ax2.grid(True)
        ax2.legend(loc=0)
        ax2.set_ylabel("Годовая выработка [единиц]")

        ax3.plot( self.W3_mod.Time, self.P1.Population/1000, "-.", lw=2, color="b", label="World3, 1972")
        ax3.plot( self.W3_mod.Time, self.W3_mod.Population/1000, ".", lw=1, color="b", label="World3, 2003")
        ax3.plot( self.W3_mod.Time[110:], self.P0.Solution_UN_Medium[110:]/1000, "-.", lw=2, color="r",  alpha=0.5, label="Средняя оценка ООН, 2015")
        ax3.plot( self.W3_mod.Time, self.P2.Population/1000, "--", lw=2, color="b", label="Й.Рандерс, 2012")
        ax3.plot( self.W3_mod.Time, self.POP_Actual/1000, "-", lw=4, color="g", alpha=0.5, label="наша модель")
        ax3.errorbar(self.P0.Calibration_Year, self.P0.Calibration_Total/1000, yerr=self.P0.Calibration_Yerr/1000,
                     fmt=".", color="k", label="Реальная популяция (ООН)")
        ax3.set_xlim( limits)
        ax3.set_ylim( 0, 12)
        ax3.grid(True)
        ax3.legend(loc=0)
        ax3.set_xlabel("Год")
        ax3.set_ylabel("популяция, млрд")
        plt.savefig( filename)
        return


# Generic checks
if __name__ == "__main__":

    #print("*** Fossil Fuel Check ***")
    #model = W3_Model( verbose=True)
    #model.Resources.Plot_FOC_Functions()
    #model.Plot_Fossil_Fuel()

    print("*** Capital Check ***")
    ac = W3_Agriculture_Capital()
    
    #model = W3_Model( verbose=True)
    #model.Plot_Capital()
    
    #if InteractiveModeOn: plt.show(True)
