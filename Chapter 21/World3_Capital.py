from World3_Model import *

class W3_Resources:
    """
    Describes resources subsystem similar to World3 implementation
    TODO: change defaults
    """
    def __init__( self, year0=1890, x6=560, sigma6=0.00485, x7=0.28, sigma7=11, focMax=1.0, verbose=False):
        self.Year = year0
        self.Initial_Fossil_Fuel = 1200e3           # mln tonn
        self.Fossil_Fuel = self.Initial_Fossil_Fuel
        #self.Fossil_Fuel_Usage_Factor = Sigmoid( x6*0.43, sigma6, 0, 7)
        self.Fossil_Fuel_Usage_Factor = Sigmoid( 0, 0.003, -7, 7, 0.1)
        self.Fossil_Fuel_Remaining_Fraction = 1
        self.Fossil_Fuel_Extraction = 0
        self.FOC_Reserves_Model = Sigmoid( x7, sigma7, focMax, 0.05)
        self.FOC = 0.0
        self.Calibration_Norm = 1 # 12.0/14.3
        if verbose:
            print( "Resources in {:.0f}: ".format( year0))
            print( "   Fossil fuel                   {:>5.1f} mln toe".format( self.Initial_Fossil_Fuel))
            print( "   Fossil fuel ERoEI midpoint    {:>5.2f} toe / capita / year".format( self.Fossil_Fuel_Usage_Factor.X0))
            print( "   Fossil fuel Sigma             {:>5.1f}".format( self.Fossil_Fuel_Usage_Factor.S0))
            print( "   Fossil fuel ERoEI midpoint    {:>5.2f}".format( self.FOC_Reserves_Model.X0))
            print( "   Fossil fuel Sigma             {:>5.1f}".format( self.FOC_Reserves_Model.S0))
        return
    def Plot_Usage_Function( self, filename = "./Graphs/figure_21_01.png"):
        """
        Test plot
        """
        fig = plt.figure( figsize=(15,8))
        fig.suptitle('Извлечение ресурсов от промышленного производства', fontsize=25)
        gs = plt.GridSpec(1, 1) 
        ax1 = plt.subplot(gs[0])
        industrial_output_per_capita = np.linspace( 0, 1750, 101)
        ax1.plot( industrial_output_per_capita, self.Fossil_Fuel_Usage_Factor.GetVector(industrial_output_per_capita),
                  "-", lw=2)
        ax1.set_xlim( 0, 1750)
        ax1.set_ylim( 0, 7)
        ax1.grid(True)
        #ax1.legend(loc=0)
        ax1.set_xlabel("Валовый промышленный продукт на душу населения в год")
        ax1.set_ylabel("Интенсивность извлечения ресурсов")
        plt.savefig( filename)
        return
    def Plot_FOC_Function( self, filename = "./Graphs/figure_21_02.png"):
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
        #self.Fossil_Fuel_Extraction = population.Demographics.Total \
        #    * self.Fossil_Fuel_Usage_Factor.Compute( population.GoodsPC / 0.43)
        self.Fossil_Fuel_Extraction = population.Demographics.Total \
            * self.Fossil_Fuel_Usage_Factor.Compute( population.GoodsPC)
        self.Fossil_Fuel_Extraction *= self.Calibration_Norm
        self.Fossil_Fuel -= self.Fossil_Fuel_Extraction
        self.Fossil_Fuel = Limit( self.Fossil_Fuel, min_y=0, max_y=self.Initial_Fossil_Fuel)
        self.Fossil_Fuel_Remaining_Fraction = self.Fossil_Fuel / self.Initial_Fossil_Fuel
        self.FOC = self.FOC_Reserves_Model.Compute( self.Fossil_Fuel_Remaining_Fraction)
        self.Year += 1
        return
    

class W3_Industrial_Capital:
    """
    Describes industrial capital subsystem
    """
    def __init__( self, year0=1890, initial=100, lifetime=14, output_ratio=2.8, consumption_ratio=0.45, verbose=False):
        self.Year = year0
        self.Total = initial
        self.Lifetime = lifetime # years
        self.Depreciation = 1-np.exp(-1.0/self.Lifetime)
        self.Output_Ratio = output_ratio
        self.Output = initial * 0.95 / output_ratio # mln tonn
        self.Consumption_Ratio = consumption_ratio
        self.Investment = 0.0
        self.Services_Investment = 0.0
        self.Agriculture_Investment = 0.0
        self.Goods_Produced = self.Output * self.Consumption_Ratio
        self.F08 = Sigmoid( 0, 0.00215, -1080, 1080, 230)
        self.F09 = Sigmoid( 0, 2.088, 0.8, 0.0)
        self.F10 = Sigmoid( 0, 0.00178, -2100, 2100)
        self.F11 = Sigmoid( 0, 1.600, 0.6, 0.0)
        if verbose:
            print( "Industrial capital in {:.0f}: ".format( year0))
            print( "   Total                 {:>5.1f} mln tonn".format( self.Total))
            print( "   Average lifetime      {:>5.1f} years".format( self.Lifetime))
            print( "   Average depreciation  {:>5.3f} per year".format( self.Depreciation))
            print( "   Output ratio          {:>5.3f}".format( self.Output_Ratio))
            print( "   Consumption ratio     {:>5.3f}".format( self.Consumption_Ratio))
            print( "   Goods produced        {:>5.3f}".format( self.Goods_Produced))
        return
    def Compute_Next_Year( self, resources, population):
        """
        Calculates next year in the model
        """
        self.Output = (1-resources.FOC) * self.Total / self.Output_Ratio
        self.OutputPC = 1000.0 * self.Output / population.Demographics.Total
        self.Indicated_FoodPC = self.F08.Compute(self.OutputPC)
        self.Indicated_ServicesPC = self.F10.Compute(self.OutputPC)
        #print("{:.0f}\t{:.1f}\t{:.1f}\t{:.1f}\t{:.1f}\t{:.1f}\t{:.1f}".format(
        #    self.Year, self.Output, self.OutputPC,
        #    self.Indicated_FoodPC, population.FoodPC,
        #    self.Indicated_ServicesPC, population.ServicesPC,
        #    self.Total))
        self.Allocation_To_Agriculture = self.F09.Compute(
            population.FoodPC / self.Indicated_FoodPC)
        remainder = Limit( 1 - self.Allocation_To_Agriculture)
        self.Allocation_To_Services = min(remainder,
            self.F11.Compute( population.ServicesPC / self.Indicated_ServicesPC))
        remainder = Limit( remainder - self.Allocation_To_Services)
        self.Allocation_To_Consumption = min(remainder, self.Consumption_Ratio)
        self.Allocation_To_Reinvestment = Limit( remainder - self.Allocation_To_Consumption)
        self.Investment = self.Allocation_To_Reinvestment * self.Output 
        self.Services_Investment = self.Allocation_To_Services * self.Output
        self.Agriculture_Investment = self.Allocation_To_Agriculture * self.Output
        self.Goods_Produced = self.Allocation_To_Consumption * self.Output
        self.Total = self.Total*(1-self.Depreciation) + self.Investment
##        print("{:.0f}\t{:.3f}\t{:.3f}\t{:.3f}\t{:.3f}".format(
##            self.Year,
##            self.Allocation_To_Agriculture,
##            self.Allocation_To_Services,
##            self.Allocation_To_Consumption,
##            self.Allocation_To_Reinvestment))
        self.Year += 1
        return
    def Plot_Indicative_Functions( self, filename = "./Graphs/figure_21_04.png"):
        """
        Test plot
        """
        fig = plt.figure( figsize=(15,8))
        fig.suptitle('Ожидаемый уровень жизни от промышленного производства', fontsize=25)
        gs = plt.GridSpec(1, 1) 
        ax1 = plt.subplot(gs[0])
        industrial_OutputPC = np.linspace( 0, 1750, 101)
        ax1.plot( industrial_OutputPC, self.F08.GetVector(industrial_OutputPC),
                  "-", lw=2, color="g", label="Продовольствие, кг")
        ax1.plot( industrial_OutputPC, self.F10.GetVector(industrial_OutputPC),
                  "-", lw=2, color="y", label="Услуги, УД")
        ax1.set_xlim( 0, 1750)
        ax1.set_ylim( 0, 2200)
        ax1.grid(True)
        ax1.legend(loc=0)
        ax1.set_xlabel("Валовый промышленный продукт на душу населения в год")
        ax1.set_ylabel("Ожидаемое благосостояние")
        plt.savefig( filename)
        return
    def Plot_Investment_Functions( self, filename = "./Graphs/figure_21_05.png"):
        """
        Test plot
        """
        fig = plt.figure( figsize=(15,8))
        fig.suptitle('Распределение инвестиций', fontsize=25)
        gs = plt.GridSpec(1, 1) 
        ax1 = plt.subplot(gs[0])
        ratio_to_indicative = np.linspace( 0, 6, 101)
        ax1.plot( ratio_to_indicative, self.F09.GetVector(ratio_to_indicative),
                  "-", lw=2, color="g", label="Сельское хозяйство")
        ax1.plot( ratio_to_indicative, self.F11.GetVector(ratio_to_indicative),
                  "-", lw=2, color="y", label="Услуги")
        ax1.plot( [ratio_to_indicative[0], ratio_to_indicative[-1]],
                  [self.Consumption_Ratio, self.Consumption_Ratio],
                  "-", lw=2, color="b", label="Потребительские товары")
        ax1.set_xlim( 0, 6)
        ax1.set_ylim( 0, 0.6)
        ax1.grid(True)
        ax1.legend(loc=0)
        ax1.set_xlabel("Отношение реально произведёного к ожидаемому")
        ax1.set_ylabel("Доля затрат в промышленном производстве")
        plt.savefig( filename)
        return


class W3_Service_Capital:
    """
    Describes service capital subsystem
    """
    def __init__( self, year0=1890, initial=200, lifetime=20, output_ratio=2.8, verbose=False):
        self.Total = initial
        self.Lifetime = lifetime # years
        self.Depreciation = 1-np.exp(-1.0/self.Lifetime)
        self.Output_Ratio = output_ratio
        self.Output = initial / output_ratio
        self.Investment = 0.0
        if verbose:
            print( "Service capital in {:.0f}: ".format( year0))
            print( "   Total                 {:>5.1f} mln tonn".format( self.Total))
            print( "   Average lifetime      {:>5.1f} years".format( self.Lifetime))
            print( "   Average depreciation  {:>5.3f} per year".format( self.Depreciation))
            print( "   Output ratio          {:>5.3f}".format( self.Output_Ratio))
        return
    def Compute_Next_Year( self, population, investment):
        """
        Calculates next year in the model
        """
        self.Output = self.Total / self.Output_Ratio
        self.Investment = investment
        self.Total = self.Total * (1-self.Depreciation) + self.Investment
        return


class W3_Agriculture_Capital:
    """
    Describes agriculture capital subsystem
    """
    def __init__( self, year0=1890, initial=100, lifetime=5, output_ratio=1.0, verbose=False):
        self.Total = initial
        self.Lifetime = lifetime # years
        self.Depreciation = 1-np.exp(-1.0/self.Lifetime)
        self.Investment = 0.0
        if verbose:
            print( "Agriculture capital in {:.0f}: ".format( year0))
            print( "   Total                 {:>5.1f} mln tonn".format( self.Total))
            print( "   Average lifetime      {:>5.1f} years".format( self.Lifetime))
            print( "   Average depreciation  {:>5.3f} per year".format( self.Depreciation))
        return
    def Compute_Next_Year( self, population, investment):
        """
        Calculates next year in the model
        """
        self.Investment = investment
        self.Total = self.Total * (1-self.Depreciation) + self.Investment
        return


class W3_Model:
    """
    Describes capital subsystem similar to World3 implementation
    year0 - starting model year, increment 1 year
    """
    def __init__( self, year0=1890, goodsPC=25.0, foodPC=270.0, servicesPC=100.0, biological_TFR=6.0, verbose=False):
        self.Year = year0
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
        self.Population.Compute_Next_Year( self.Industrial_Capital.Output,
                                           food, self.Service_Capital.Output, pollution, m2f, dleb)
        self.Resources.Compute_Next_Year( self.Population)
        self.Industrial_Capital.Compute_Next_Year( self.Resources, self.Population)
        self.Service_Capital.Compute_Next_Year( self.Population, self.Industrial_Capital.Services_Investment)
        self.Agriculture_Capital.Compute_Next_Year( self.Population, self.Industrial_Capital.Agriculture_Investment)
        self.Year += 1
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
    def Test_Fossil_Fuel( self, filename = "./Graphs/figure_21_03.png"):
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
    def Test_Capital( self, filename = "./Graphs/figure_21_06.png"):
        """
        Test plot for capital and investment
        """
        self._prepare_check()
        Y, ICap, SCap, IOut, SOut = Load_Calibration( "./Data/Capital_Checks.csv",
            ["Time", "_052_IndustrialCapital","_067_ServiceCapital",
            "_050_IndustrialOutput", "_070_ServiceOutput"])
        conversion = 1.0
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
            self.Service_Investment[i] = self.Industrial_Capital.Services_Investment
            self.Service_Output_Actual[i] = self.Service_Capital.Output 
            self.Agriculture_Capital_Actual[i] = self.Agriculture_Capital.Total 
            self.Agriculture_Investment[i] = self.Industrial_Capital.Agriculture_Investment 
            self.Agriculture_Output_Actual[i] = self.W3_mod.Food[i]*conversion 
            self.Compute_Next_Year(goods=self.W3_mod.Goods[i]*conversion,
                                 food=self.W3_mod.FoodPC[i]*self.Population.Demographics.Total/1000,
                                 services=self.W3_mod.Services[i]*conversion)

        limits = 1900, 2100

        fig = plt.figure( figsize=(15,15))
        fig.suptitle('Проверка модели "World3": капитал и производство', fontsize=25)
        gs = plt.GridSpec(3, 1) 
        ax1 = plt.subplot(gs[0])
        ax2 = plt.subplot(gs[1])
        ax3 = plt.subplot(gs[2])

        ax1.plot( self.W3_mod.Time, self.POP_Actual, ".", lw=1, color="m", label="Население [млн]")
        ax1.plot( self.W3_mod.Time, self.W3_mod.Population, "-.", lw=6, color="m", alpha=0.3)
        ax1.plot( self.W3_mod.Time, self.Industrial_Capital_Actual, "-", lw=3, color="b", label="Промышленность")
        ax1.plot( self.W3_mod.Time, self.Industrial_Capital_Actual*self.FOC_Actual, "-.", lw=2, color="b", label="В том числе добывающая")
        ax1.plot( Y, ICap/1e9, "-.", lw=6, color="b", alpha=0.3)
        ax1.plot( self.W3_mod.Time, self.Service_Capital_Actual, "-", lw=3, color="y", label="Услуги")
        ax1.plot( Y, SCap/1e9, "-.", lw=6, color="y", alpha=0.3)
        ax1.plot( self.W3_mod.Time, self.Agriculture_Capital_Actual, "-", lw=3, color="g", label="Сельское хоз-во")
        ax1.set_xlim( limits)
        ax1.set_ylim( 0, 11000)
        ax1.grid(True)
        ax1.legend(loc=0)
        ax1.set_ylabel("Капитал [млн т]")

        ax2.plot( self.W3_mod.Time, self.Industrial_Investment, "-", lw=4, alpha=0.5, color="b", label="Инвестиции в промышленность")
        ax2.plot( self.W3_mod.Time, self.Service_Investment, "-", lw=4, alpha=0.5, color="y", label='Инвестиции в "услуги"')
        ax2.plot( self.W3_mod.Time, self.Agriculture_Investment, "-", lw=4, alpha=0.5, color="g", label="Инвестиции в сельское хоз-во")
        ax2.plot( self.W3_mod.Time, self.Consumer_Goods_Output_Actual, "-", lw=3, alpha=0.5, color="r", label="Потребительские товары")
        ax2.set_xlim( limits)
        ax2.set_ylim( 0, 1300)
        ax2.grid(True)
        ax2.legend(loc=0)
        ax2.set_ylabel("Инвестиции [млн т]")

##        ax3.plot( self.W3_mod.Time, self.W3_mod.GoodsPC, "-.", lw=2, color="b", label="Промтовары World3, 2003 [кг / душу / год]")
##        ax3.plot( self.W3_mod.Time, self.W3_mod.ServicesPC, "-.", lw=2, color="y", label="Услуги World3, 2003 [УД / душу / год]")
##        ax3.plot( self.W3_mod.Time, self.W3_mod.FoodPC, "-.", lw=2, color="g", label="Продовольствие World3, 2003 [кг / душу / год]")
##        ax3.plot( self.W3_mod.Time, self.GoodsPC_Actual, "-", lw=4, alpha=0.5, color="b", label="Наша модель")
##        ax3.plot( self.W3_mod.Time, self.ServicesPC_Actual, "-", lw=4, alpha=0.5, color="y")
##        ax3.plot( self.W3_mod.Time, self.FoodPC_Actual, "-", lw=4, alpha=0.5, color="g")
        ax3.plot( self.W3_mod.Time, self.W3_mod.Goods, "-.", lw=2, color="b", label="Промтовары World3, 2003 [млн тонн / год]")
        ax3.plot( self.W3_mod.Time, self.W3_mod.Services, "-.", lw=2, color="y", label="Услуги World3, 2003 [трлн УД / год]")
        ax3.plot( self.W3_mod.Time, self.W3_mod.Food, "-.", lw=2, color="g", label="Продовольствие World3, 2003 [млн тонн / год]")
        ax3.plot( self.W3_mod.Time, self.Industrial_Output_Actual, "-", lw=4, alpha=0.5, color="b", label="Наша модель")
        ax3.plot( self.W3_mod.Time, self.Service_Output_Actual, "-", lw=4, alpha=0.5, color="y")
        #ax3.plot( self.W3_mod.Time, self.Agriculture_Output_Actual, "-", lw=4, alpha=0.5, color="g")
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
    #model.Resources.Plot_Usage_Function()
    #model.Resources.Plot_FOC_Function()
    #model.Test_Fossil_Fuel()

    print("*** Capital Check ***")
    model = W3_Model( verbose=True)
    #model.Industrial_Capital.Plot_Indicative_Functions()
    #model.Industrial_Capital.Plot_Investment_Functions()
    #model.Service_Capital.Plot_Investment_Functions()
    #model.Agriculture_Capital.Plot_Investment_Functions()
    model.Test_Capital()
    #model.Plot_Production_and_Consumption()
    
    if InteractiveModeOn: plt.show(True)
