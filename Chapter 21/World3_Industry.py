from World3_Model import *

class W3_Resources:
    """
    Describes resources subsystem similar to World3 implementation
    """
    def __init__( self, year0=1890, verbose=False):
        self.Initial_Fossil_Fuel = 1400e3           # mln tonn
        self.Fossil_Fuel = self.Initial_Fossil_Fuel
        self.Fossil_Fuel_Usage_Factor = Linear_Combo()
        self.Fossil_Fuel_Usage_Factor.Wavelets += [Hubbert( x0=1910, s0=0.090, s1=0.090, peak=7.7, shift=9.0)]
        self.Fossil_Fuel_Usage_Factor.Wavelets += [Hubbert( x0=1973, s0=0.130, s1=0.130, peak=6.5, shift=0.0)]
        self.Fossil_Fuel_Usage_Factor.Wavelets += [Hubbert( x0=2030, s0=0.130, s1=0.130, peak=3.5, shift=0.0)]
        #self.Fossil_Fuel_Usage_Factor = 11 #11
        self.Fossil_Fuel_Remaining_Fraction = 1
        self.Fossil_Fuel_Extraction = 0
        self.Midpoint = 0.60
        self.Sigma = 3
        self.FOCmax = 0.9
        self.FOC_Reserves_Model = Sigmoid( self.Midpoint, self.Sigma, self.FOCmax, 0.01)
        self.FOC = 0.0
        if verbose:
            print( "Resources in {:.0f}: ".format( year0))
            print( "   Fossil fuel                   {:>5.1f} mln tonn".format( self.Initial_Fossil_Fuel))
            print( "   Fossil fuel ERoEI midpoint    {:>5.2f}".format( self.Midpoint))
            print( "   Fossil fuel Sigma             {:>5.1f}".format( self.Sigma))
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
        self.Fossil_Fuel_Extraction = population.Goods * self.Fossil_Fuel_Usage_Factor.Compute(population.Demographics.Year)
        #print( population.Demographics.Year, self.Fossil_Fuel_Usage_Factor.Compute(population.Demographics.Year))
        self.Fossil_Fuel -= self.Fossil_Fuel_Extraction
        self.Fossil_Fuel = Limit( self.Fossil_Fuel, min_y=0, max_y=self.Initial_Fossil_Fuel)
        self.Fossil_Fuel_Remaining_Fraction = self.Fossil_Fuel / self.Initial_Fossil_Fuel
        self.FOC_Reserves_Model.X0 = self.Midpoint
        self.FOC_Reserves_Model.Sigma0 = self.Sigma
        self.FOC_Reserves_Model.Left = self.FOCmax
        self.FOC = self.FOC_Reserves_Model.Compute( self.Fossil_Fuel_Remaining_Fraction)
        return
    

class W3_Industrial_Capital:
    """
    Describes industrial capital subsystem 0.363, 0.465, 
    """
    def __init__( self, year0=1890, initial=100, lifetime=25, output_ratio=0.77, consumption_ratio=0.77, verbose=False):
        self.Total = initial
        self.Lifetime = lifetime # years
        self.Depreciation = 1-np.exp(-1.0/self.Lifetime)
        self.Output_Ratio = output_ratio
        self.Output = initial * output_ratio
        self.Investment = 0.0
        self.Consumption_Ratio = consumption_ratio
        self.Goods_Produced = self.Output * self.Consumption_Ratio * 0.3 # initial investment to agriculture
        if verbose:
            print( "Industrial capital in {:.0f}: ".format( year0))
            print( "   Total                 {:>5.1f} mln tonn".format( self.Total))
            print( "   Average lifetime      {:>5.1f} years".format( self.Lifetime))
            print( "   Average depreciation  {:>5.3f} per year".format( self.Depreciation))
            print( "   Output ratio          {:>5.3f}".format( self.Output_Ratio))
            print( "   Consumption ratio     {:>5.3f}".format( self.Consumption_Ratio))
            print( "   Goods produced        {:>5.3f}".format( self.Goods_Produced))
        return
    def Compute_Output( self, resources):
        self.Output = (1-resources.FOC) * self.Total * self.Output_Ratio
        return self.Output
    def Compute_Next_Year( self, remaining_output):
        """
        Calculates next year in the model
        """
        self.Goods_Produced = remaining_output * self.Consumption_Ratio
        self.Investment = remaining_output - self.Goods_Produced
        self.Total = self.Total*(1-self.Depreciation) + self.Investment 
        return


class W3_Service_Capital:
    """
    Describes service capital subsystem
    """
    def __init__( self, year0=1890, initial=100, lifetime=10, output_ratio=1.5, verbose=False):
        self.Total = initial
        self.Lifetime = lifetime # years
        self.Depreciation = 1-np.exp(-1.0/self.Lifetime)
        self.Output_Ratio = output_ratio
        self.Output = initial * output_ratio
        self.Investment = 0.0
        self.Indicated_Per_Capita_Model = Sigmoid( 250, 0.012, 0.35, 0.05)
        self.Indicated_Per_Capita = 500
        self.Indicated_Per_Capita_Min = 0.05
        self.Indicated_Per_Capita_Max = 0.30
        self.Indicated_Sigma = 2.0
        self.Indicated_Per_Capita_Model = Sigmoid( 1,
                                                   self.Indicated_Sigma,
                                                   self.Indicated_Per_Capita_Max,
                                                   self.Indicated_Per_Capita_Min)
        if verbose:
            print( "Service capital in {:.0f}: ".format( year0))
            print( "   Total                 {:>5.1f} mln tonn".format( self.Total))
            print( "   Average lifetime      {:>5.1f} years".format( self.Lifetime))
            print( "   Average depreciation  {:>5.3f} per year".format( self.Depreciation))
            print( "   Output ratio          {:>5.3f}".format( self.Output_Ratio))
            print( "   Indicated per capita  {:>5.0f} kg".format( self.Indicated_Per_Capita))
            print( "   Indicated sigma       {:>5.3f}".format( self.Indicated_Sigma))
            print( "   Inv.fraction max      {:>5.3f}".format( self.Indicated_Per_Capita_Max))
            print( "   Inv.fraction min      {:>5.3f}".format( self.Indicated_Per_Capita_Min))
        return
    def Plot_Investment_Functions( self, filename = "./Graphs/figure_21_03.png"):
        """
        Test plot
        """
        fig = plt.figure( figsize=(15,8))
        fig.suptitle('Зависимость инвестиций в капитал услуг от потребления', fontsize=25)
        gs = plt.GridSpec(1, 1) 
        ax1 = plt.subplot(gs[0])
        consumption_level = np.linspace( 0, 5, 101)
        ax1.plot( consumption_level, self.Indicated_Per_Capita_Model.GetVector(consumption_level),
                  "-", lw=2)
        ax1.set_xlim( 0, 5)
        ax1.set_ylim( 0, 1)
        ax1.grid(True)
        #ax1.legend(loc=0)
        ax1.set_xlabel("Уровень потребления от оптимума")
        ax1.set_ylabel("Доля промышленной продукции на инвестиции")
        plt.savefig( filename)
        return
    def Compute_Next_Year( self, population, this_year_industrial_output):
        """
        Calculates next year in the model
        """
        self.Indicated_Per_Capita_Model.S0 = self.Indicated_Sigma
        self.Indicated_Per_Capita_Model.Left = self.Indicated_Per_Capita_Max
        self.Indicated_Per_Capita_Model.Right = self.Indicated_Per_Capita_Min
        f = Divide_Non_Zero( population.ServicesPC, self.Indicated_Per_Capita)
        self.Investment = self.Indicated_Per_Capita_Model.Compute( f) * this_year_industrial_output
        #print(f, self.Indicated_Per_Capita_Model.Compute( f))
        self.Output = self.Total * self.Output_Ratio
        self.Total = self.Total * (1-self.Depreciation) + self.Investment
        return this_year_industrial_output - self.Investment


class W3_Agriculture_Capital:
    """
    Describes agriculture capital subsystem
    """
    def __init__( self, year0=1890, initial=100, lifetime=5, output_ratio=1.0, verbose=False):
        self.Total = initial
        self.Lifetime = lifetime # years
        self.Depreciation = 1-np.exp(-1.0/self.Lifetime)
        self.Output_Ratio = output_ratio
        self.Output = initial * output_ratio
        self.Investment = 0.0
        self.Indicated_Per_Capita = 350
        self.Indicated_Per_Capita_Min = 0.05
        self.Indicated_Per_Capita_Max = 0.55
        self.Indicated_Sigma = 5.0
        self.Indicated_Per_Capita_Model = Sigmoid( 1,
                                                   self.Indicated_Sigma,
                                                   self.Indicated_Per_Capita_Max,
                                                   self.Indicated_Per_Capita_Min)
        if verbose:
            print( "Agriculture capital in {:.0f}: ".format( year0))
            print( "   Total                 {:>5.1f} mln tonn".format( self.Total))
            print( "   Average lifetime      {:>5.1f} years".format( self.Lifetime))
            print( "   Average depreciation  {:>5.3f} per year".format( self.Depreciation))
            print( "   Indicated per capita  {:>5.0f} kg".format( self.Indicated_Per_Capita))
            print( "   Indicated sigma       {:>5.3f}".format( self.Indicated_Sigma))
            print( "   Inv.fraction max      {:>5.3f}".format( self.Indicated_Per_Capita_Max))
            print( "   Inv.fraction min      {:>5.3f}".format( self.Indicated_Per_Capita_Min))
        return
    def Plot_Investment_Functions( self, filename = "./Graphs/figure_21_04.png"):
        """
        Test plot
        """
        fig = plt.figure( figsize=(15,8))
        fig.suptitle('Зависимость инвестиций в сельское хозяйство от потребления', fontsize=25)
        gs = plt.GridSpec(1, 1) 
        ax1 = plt.subplot(gs[0])
        consumption_level = np.linspace( 0, 5, 101)
        ax1.plot( consumption_level, self.Indicated_Per_Capita_Model.GetVector(consumption_level),
                  "-", lw=2)
        ax1.set_xlim( 0, 5)
        ax1.set_ylim( 0, 1)
        ax1.grid(True)
        #ax1.legend(loc=0)
        ax1.set_xlabel("Уровень потребления от оптимума")
        ax1.set_ylabel("Доля промышленной продукции на инвестиции")
        plt.savefig( filename)
        return    
    def Compute_Next_Year( self, population, this_year_industrial_output):
        """
        Calculates next year in the model
        """
        self.Indicated_Per_Capita_Model.S0 = self.Indicated_Sigma
        self.Indicated_Per_Capita_Model.Left = self.Indicated_Per_Capita_Max
        self.Indicated_Per_Capita_Model.Right = self.Indicated_Per_Capita_Min
        f = Divide_Non_Zero( population.FoodPC, self.Indicated_Per_Capita)
        self.Investment = self.Indicated_Per_Capita_Model.Compute( f) * this_year_industrial_output
        self.Output = self.Total * self.Output_Ratio
        self.Total = self.Total * (1-self.Depreciation) + self.Investment
        return this_year_industrial_output - self.Investment


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
        Calculates next year in the model;
        Note that food is still a parametrization of the 2003 model
        and pollution is not used
        """
        self.Population.Compute_Next_Year( goods*0.94, food*0.94, services*0.94, pollution, m2f, dleb)
        #self.Population.Compute_Next_Year( goods*0.94, food*0.94, self.Service_Capital.Output, pollution, m2f, dleb)
        #self.Population.Compute_Next_Year( self.Industrial_Capital.Goods_Produced, food*0.94, services*0.94, pollution, m2f, dleb)
        #self.Population.Compute_Next_Year( self.Industrial_Capital.Goods_Produced, food, services, pollution, m2f, dleb)
        #self.Population.Compute_Next_Year( self.Industrial_Capital.Goods_Produced,
        #                                   food*0.94,
        #                                   self.Service_Capital.Output,
        #                                   pollution, m2f, dleb)
        self.Resources.Compute_Next_Year( self.Population)
        This_Year_Output = self.Industrial_Capital.Compute_Output( self.Resources)
        This_Year_Output = self.Agriculture_Capital.Compute_Next_Year( self.Population, This_Year_Output)
        This_Year_Output = self.Service_Capital.Compute_Next_Year( self.Population, This_Year_Output)
        self.Industrial_Capital.Compute_Next_Year( This_Year_Output)
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
        self.Fossil_Fuel_Rate = np.zeros(l)
        self.FOC_Actual = np.zeros(l)
        self.Industrial_Capital_Actual = np.zeros(l)
        self.Industrial_Output_Actual = np.zeros(l)
        self.Consumer_Goods_Output_Actual = np.zeros(l)
        self.Industrial_Investment = np.zeros(l)
        self.Service_Capital_Actual = np.zeros(l)
        self.Service_Output_Actual = np.zeros(l)
        self.Service_Investment = np.zeros(l)
        self.Agriculture_Capital_Actual = np.zeros(l)
        self.Agriculture_Output_Actual = np.zeros(l)
        self.Agriculture_Investment = np.zeros(l)
        self.GoodsPC_Actual = np.zeros(l)
        self.FoodPC_Actual = np.zeros(l)
        self.ServicesPC_Actual = np.zeros(l)
        return
    def Plot_Fossil_Fuel( self, filename = "./Graphs/figure_21_02.png"):
        """
        Test plot for fossil fuel production
        """
        self._prepare_check()
        conversion = 1
        for i,y in enumerate(self.W3_mod.Time):
            self.POP_Actual[i] = self.Population.Demographics.Total
            self.GoodsPC_Actual[i] = self.Population.GoodsPC
            self.FoodPC_Actual[i] = self.Population.FoodPC
            self.ServicesPC_Actual[i] = self.Population.ServicesPC
            self.Fossil_Fuel_Actual[i] = self.Resources.Fossil_Fuel
            self.Industrial_Capital_Actual[i] = self.Industrial_Capital.Total
            self.Agriculture_Capital_Actual[i] = self.Agriculture_Capital.Total
            self.Service_Capital_Actual[i] = self.Service_Capital.Total
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
    def Plot_Capital( self, filename = "./Graphs/figure_21_05.png"):
        """
        Test plot for capital and investment
        """
        self._prepare_check()
        conversion = 0.94
        for i,y in enumerate(self.W3_mod.Time):
            self.POP_Actual[i] = self.Population.Demographics.Total
            self.FOC_Actual[i] = self.Resources.FOC
            self.GoodsPC_Actual[i] = self.Population.GoodsPC
            self.FoodPC_Actual[i] = self.Population.FoodPC
            self.ServicesPC_Actual[i] = self.Population.ServicesPC
            self.Industrial_Capital_Actual[i] = self.Industrial_Capital.Total 
            self.Industrial_Investment[i] = self.Industrial_Capital.Investment 
            self.Industrial_Output_Actual[i] = self.Industrial_Capital.Output
            self.Consumer_Goods_Output_Actual[i] = self.Industrial_Capital.Goods_Produced
            self.Service_Capital_Actual[i] = self.Service_Capital.Total 
            self.Service_Investment[i] = self.Service_Capital.Investment 
            self.Service_Output_Actual[i] = self.Service_Capital.Output 
            self.Agriculture_Capital_Actual[i] = self.Agriculture_Capital.Total 
            self.Agriculture_Investment[i] = self.Agriculture_Capital.Investment 
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
        ax1.plot( self.W3_mod.Time, self.Industrial_Capital_Actual*self.FOC_Actual/1000, "-.", lw=2, color="r", label="В том числе добывающая")
        ax1.plot( self.W3_mod.Time, self.Agriculture_Capital_Actual/1000, "-", lw=3, color="g", label="Сельское хозяйство")
        ax1.plot( self.W3_mod.Time, self.Service_Capital_Actual/1000, "-", lw=3, color="m", label="Услуги")
        ax1.set_xlim( limits)
        ax1.grid(True)
        ax1.legend(loc=0)
        ax1.set_ylabel("Капитал [млрд т]")

        ax2.plot( self.W3_mod.Time, self.Industrial_Investment/1000, "-", lw=4, alpha=0.5, color="r", label="В промышленность")
        ax2.plot( self.W3_mod.Time, self.Agriculture_Investment/1000, "-", lw=4, alpha=0.5, color="g", label="В производство продовольствия")
        ax2.plot( self.W3_mod.Time, self.Service_Investment/1000, "-", lw=4, alpha=0.5, color="m", label='В "услуги"')
        ax2.set_xlim( limits)
        ax2.set_ylim( 0, 0.6)
        ax2.grid(True)
        ax2.legend(loc=0)
        ax2.set_ylabel("Инвестиции [млрд т]")

        ax3.plot( self.W3_mod.Time, self.W3_mod.Goods/1000, "-.", lw=2, color="r", label="Промтовары World3, 2003 [млрд т]")
        ax3.plot( self.W3_mod.Time, self.W3_mod.Food/1000, "-.", lw=2, color="g", label="Продовольствие World3, 2003 [млрд т]")
        ax3.plot( self.W3_mod.Time, self.W3_mod.Services/1000, "-.", lw=2, color="m", label="Услуги World3, 2003 [трлн усл.$]")
        ax3.plot( self.W3_mod.Time, self.Consumer_Goods_Output_Actual/1000, "-", lw=4, alpha=0.5, color="r", label="Наша модель")
        ax3.plot( self.W3_mod.Time, self.Agriculture_Output_Actual/1000, "-", lw=4, alpha=0.5, color="g")
        ax3.plot( self.W3_mod.Time, self.Service_Output_Actual/1000, "-", lw=4, alpha=0.5, color="m")
        ax3.set_xlim( limits)
        #ax3.set_ylim( 0, 1.5)
        ax3.grid(True)
        ax3.legend(loc=0)
        ax3.set_ylabel("Годовая выработка [единиц]")
        ax3.set_xlabel("Год")
        plt.savefig( filename)
        return
    def Plot_Production_and_Consumption( self, filename = "./Graphs/figure_21_06.png"):
        """
        Test plot for industrial capital
        """
        self._prepare_check()
        conversion = 1
        for i,y in enumerate(self.W3_mod.Time):
            self.POP_Actual[i] = self.Population.Demographics.Total
            self.Fossil_Fuel_Actual[i] = self.Resources.Fossil_Fuel 
            self.Fossil_Fuel_Rate[i] = self.Resources.Fossil_Fuel_Extraction
            self.FOC_Actual[i] = self.Resources.FOC
            self.GoodsPC_Actual[i] = self.Population.GoodsPC
            self.FoodPC_Actual[i] = self.Population.FoodPC
            self.ServicesPC_Actual[i] = self.Population.ServicesPC
            self.Industrial_Capital_Actual[i] = self.Industrial_Capital.Total 
            self.Industrial_Investment[i] = self.Industrial_Capital.Investment 
            self.Industrial_Output_Actual[i] = self.Industrial_Capital.Output
            self.Consumer_Goods_Output_Actual[i] = self.Industrial_Capital.Goods_Produced
            self.Service_Capital_Actual[i] = self.Service_Capital.Total 
            self.Service_Investment[i] = self.Service_Capital.Investment 
            self.Service_Output_Actual[i] = self.Service_Capital.Output 
            self.Agriculture_Capital_Actual[i] = self.Agriculture_Capital.Total 
            self.Agriculture_Investment[i] = self.Agriculture_Capital.Investment 
            self.Agriculture_Output_Actual[i] = self.Agriculture_Capital.Output 
            self.Compute_Next_Year(goods=self.W3_mod.Goods[i]*conversion,
                                 food=self.W3_mod.Food[i]*conversion,
                                 services=self.W3_mod.Services[i]*conversion)

        limits = 1900, 2100

        fig = plt.figure( figsize=(15,15))
        fig.suptitle('Проверка модели "World3": производство и потребление', fontsize=25)
        gs = plt.GridSpec(3, 1) 
        ax1 = plt.subplot(gs[0])
        ax2 = plt.subplot(gs[1])
        ax3 = plt.subplot(gs[2])

        ax1.plot( self.W3_mod.Time, self.Industrial_Capital_Actual/1000, "-", lw=3, color="r", label="Промышленность")
        ax1.plot( self.W3_mod.Time, self.Industrial_Capital_Actual*self.FOC_Actual/1000, "-.", lw=2, color="r", label="В том числе добывающая")
        ax1.plot( self.W3_mod.Time, self.Agriculture_Capital_Actual/1000, "-", lw=3, color="g", label="Сельское хозяйство")
        ax1.plot( self.W3_mod.Time, self.Service_Capital_Actual/1000, "-", lw=3, color="m", label="Услуги")
        ax1.set_xlim( limits)
##        ax2.set_ylim( 0, 700)
        ax1.grid(True)
        ax1.legend(loc=0)
        ax1.set_ylabel("Капитал [млрд т]")

        ax2.plot( self.W3_mod.Time, self.W3_mod.Goods/1000, "-.", lw=2, color="r", label="Промтовары World3, 2003 [млрд т]")
        ax2.plot( self.W3_mod.Time, self.W3_mod.Food/1000, "-.", lw=2, color="g", label="Продовольствие World3, 2003 [млрд т]")
        ax2.plot( self.W3_mod.Time, self.W3_mod.Services/1000, "-.", lw=2, color="m", label="Услуги World3, 2003 [трлн усл.$]")
        ax2.plot( self.W3_mod.Time, self.Consumer_Goods_Output_Actual/1000, "-", lw=4, alpha=0.5, color="r", label="Наша модель")
        ax2.plot( self.W3_mod.Time, self.Agriculture_Output_Actual/1000, "-", lw=4, alpha=0.5, color="g")
        ax2.plot( self.W3_mod.Time, self.Service_Output_Actual/1000, "-", lw=4, alpha=0.5, color="m")
        ax2.plot( self.W3_mod.Time, self.Fossil_Fuel_Rate/1000, "-", lw=4, alpha=0.5, color="k")
        ax2.errorbar( self.R0.Calibration_Year, self.R0.Calibration_Carbon/1000,
                      yerr=self.R0.Calibration_Carbon/20000, fmt=".", color="k", label="Реальная добыча [млрд т]")
        ax2.set_xlim( limits)
        #ax2.set_ylim( 0, 1.5)
        ax2.grid(True)
        ax2.legend(loc=0)
        ax2.set_ylabel("Годовая выработка [единиц]")

        #ax3.plot( self.W3_mod.Time, self.Industrial_Investment/1000, "-", lw=4, alpha=0.5, color="r", label="В промышленность")
        #ax3.plot( self.W3_mod.Time, self.Agriculture_Investment/1000, "-", lw=4, alpha=0.5, color="g", label="В производство продовольствия")
        #ax3.plot( self.W3_mod.Time, self.Service_Investment/1000, "-", lw=4, alpha=0.5, color="m", label='В "услуги"')
        #ax3.set_xlim( limits)
        #ax3.set_ylim( 0, 0.6)
        #ax3.grid(True)
        #ax3.legend(loc=0)
        #ax3.set_ylabel("Инвестиции [млрд т]")

##        ax3.plot( self.W3_mod.Time, self.P1.Population/1000, "-.", lw=2, color="b", label="World3, 1972")
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

    print("*** Fossil Fuel Check ***")
    #model = W3_Model( verbose=True)
    #model.Resources.Plot_FOC_Functions()
    #model.Plot_Fossil_Fuel()

    print("*** Capital Check ***")
    model = W3_Model( verbose=True)
    #model.Service_Capital.Plot_Investment_Functions()
    #model.Agriculture_Capital.Plot_Investment_Functions()
    #model.Plot_Capital()
    model.Plot_Production_and_Consumption()
    
    if InteractiveModeOn: plt.show(True)
