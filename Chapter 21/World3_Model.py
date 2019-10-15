from Predictions import *

class W3_Demographics:
    """
    Describes demographics system similar to World3 implementation
    year0 - starting model year, increment 1 year
    population0 - total population in year 0
    tfr - total fertility rate before year 0
    leb - life expectancy at birth before year 0
    m2f - male:female ratio at birth before year 0
    dleb - male:female LEB difference, years
    """
    def __init__( self, year0=1890, population0=1530.880, tfr=5.4, leb=30, m2f=1.05, dleb=4):
        self.Year = year0
        self.Ages = np.linspace( 0,199, 200)
        self.Population_Male = np.ones( 200)
        self.Population_Female = np.ones( 200)
        self.Attrition_Model_Male = Bathtub( x0=5.0, s0=1.0, x1=80, s1=0.2, left=0.1, middle=0.01, right=0.20)
        self.Attrition_Model_Female = Bathtub( x0=5.0, s0=1.0, x1=80, s1=0.2, left=0.1, middle=0.01, right=0.20)
        self.Fertility_Model = Bathtub( x0=18.0, s0=1.0, x1=35, s1=0.4, left=0.0, middle=1, right=0)
        self.Workforce_Model = Bathtub( x0=16.0, s0=1.0, x1=65, s1=0.4, left=0.0, middle=0.9, right=0)
        self.TFR = tfr
        self.dLEB = dleb
        self.LEB_Male = Limit( leb-self.dLEB/2, 0, 150)
        self.LEB_Female = Limit( leb+self.dLEB/2, 0, 150)
        self.M2F = m2f
        self.__expectancy__ = Linear_Combo()
        self.__expectancy__.Wavelets += [Hubbert( x0=-10.0, s0=0.064, s1=0.064, peak= 0.370)]
        self.__expectancy__.Wavelets += [Hubbert( x0= 45.0, s0=0.095, s1=0.092, peak= 0.024)]
        self.__expectancy__.Wavelets += [Hubbert( x0= 14.0, s0=0.349, s1=0.214, peak=-0.018)]
        self.__expectancy__.Wavelets += [Hubbert( x0=  6.0, s0=1.162, s1=1.162, peak= 0.017)]
        self.__expectancy__.Wavelets += [Hubbert( x0= 82.0, s0=0.240, s1=0.240, peak=-0.009)]

        # create initial population
        for i in range( 300): self.Compute_Next_Year()
        self.Normalize( population0)
        self.Compute_Next_Year()
        self.Normalize( population0)
        self.Year = year0
        return
    def Set_Attrition_Model( self, attr=None):
        """
        Sets attrition coefficient vector based on LEB
        """
        if not attr is None:
            self.Attrition_Model_Male.Left = attr
            self.Attrition_Model_Male.Middle = attr * 0.1
            self.Attrition_Model_Female.Left = attr
            self.Attrition_Model_Female.Middle = attr * 0.1
            return
        if self.LEB_Male <= 0 or self.LEB_Female <= 0:
            self.Attrition_Model_Male.Left = 1.0
            self.Attrition_Model_Male.Middle = 0.5
            self.Attrition_Model_Female.Left = 1.0
            self.Attrition_Model_Female.Middle = 0.5
            return
        self.Attrition_Model_Male.Left = self.__expectancy__.Compute_Clipped(
            Limit( self.LEB_Male, 5, 85), min_y=0.001, max_y=0.300)
        self.Attrition_Model_Male.Middle = self.Attrition_Model_Male.Left * 0.1
        self.Attrition_Model_Female.Left = self.__expectancy__.Compute_Clipped(
            Limit( self.LEB_Female, 5, 85), min_y=0.001, max_y=0.300)
        self.Attrition_Model_Female.Middle = self.Attrition_Model_Female.Left * 0.1
        return
    def Compute_LEB(self, attrition, population):
        """
        Computes true and apparent LEB
        """
        leb_true = 0
        counter = 1
        for i in range(199):
            counter *= 1-attrition[i]
            leb_true += counter
        pSum = np.sum( population)
        if pSum <= 0: return leb_true, 0.0
        tmpLEB = attrition * population
        tmpLEB[-1] = population[-1]
        leb_apparent = np.sum( tmpLEB * self.Ages) / np.sum(tmpLEB)
        return leb_true, leb_apparent
    def Compute_Next_Year( self, tfr=None, leb=None, m2f=None, dleb=None):
        """
        Calculates next year in the model
        """
        self.Year += 1
        if not tfr is None: self.TFR = tfr
        if not dleb is None: self.dLEB = dleb
        if not leb is None:
            self.LEB_Male = Limit( leb-self.dLEB/2, 0, 150)
            self.LEB_Female = Limit( leb+self.dLEB/2, 0, 150)
        if not m2f is None: self.M2F = m2f
        self.Set_Attrition_Model()
        attrition_male = self.Attrition_Model_Male.GetVector( self.Ages)
        attrition_female = self.Attrition_Model_Female.GetVector( self.Ages)
        self.LEB_True_Male, self.LEB_Apparent_Male = self.Compute_LEB(
            attrition_male, self.Population_Male )
        self.LEB_True_Female, self.LEB_Apparent_Female = self.Compute_LEB(
            attrition_female, self.Population_Female )
        self.nDeath = np.sum( self.Population_Male * attrition_male)
        self.nDeath += np.sum( self.Population_Female * attrition_female)
        self.Population_Male = np.roll( self.Population_Male * (1-attrition_male), 1)
        self.Population_Female = np.roll( self.Population_Female * (1-attrition_female), 1)
        fertility = self.Fertility_Model.GetVector(self.Ages)
        nFertile = np.dot( self.Population_Female, fertility)
        self.nBirth = nFertile * self.TFR / np.sum( fertility)
        self.Population_Male[0] = self.nBirth * 0.5 * self.M2F
        self.Population_Female[0] = self.nBirth  - self.Population_Male[0]
        self.Compute_Totals()
        return
    def Normalize( self, norm):
        """
        Solution normalization after initial run
        """
        n = np.sum( self.Population_Male) + np.sum( self.Population_Female)
        if n <= 0.0: return
        n = norm/n
        self.Population_Male *= n
        self.Population_Female *= n
        self.Compute_Totals()
        return
    def Compute_Totals( self):
        """
        Computes total population and labour
        """
        self.Total_Male = np.sum(self.Population_Male)
        self.Total_Female = np.sum(self.Population_Female)
        self.Total = self.Total_Male + self.Total_Female
        workforce = self.Workforce_Model.GetVector(self.Ages)
        self.Labor = np.dot(self.Population_Male+self.Population_Female, workforce)
        return
    def Plot_Attrition_Function( self, filename = "./Graphs/figure_20_02.png"):
        """
        Test plot
        """
        fig = plt.figure( figsize=(15,8))
        fig.suptitle('Зависимость показателя возрастной смертности от LEB', fontsize=25)
        gs = plt.GridSpec(1, 1) 
        ax1 = plt.subplot(gs[0])
        leb = np.linspace( 0, 100, 101)
        a = self.__expectancy__.GetVector_Clipped( leb, 0.001, 0.3)
        ax1.plot( leb, a, "-", lw=2, color= "r")
        ax1.set_xlim( 0, 100)
        #ax1.set_ylim( 0, 0.25)
        ax1.grid(True)
        ax1.set_ylabel("Показатель смертности")
        ax1.set_xlabel("Ожидаемая продолжительность жизни [лет]")
        plt.savefig( filename)
        return
    def Plot_Demographic_Functions( self, filename = "./Graphs/figure_20_03.png"):
        """
        Test plot
        """
        fig = plt.figure( figsize=(15,15))
        fig.suptitle('Демографические зависимости в модели "World3"', fontsize=25)
        gs = plt.GridSpec(2, 1) 
        ax1 = plt.subplot(gs[0])
        ax2 = plt.subplot(gs[1])
        pv_Male = self.LEB_Male
        pv_Female = self.LEB_Female
        for leb in [10, 20, 30, 40, 50, 60, 70, 80, 90]:
            self.LEB_Male = leb - self.dLEB/2 
            self.LEB_Female = leb + self.dLEB/2
            self.Set_Attrition_Model()
            attrition = self.Attrition_Model_Male.GetVector( self.Ages) 
            attrition += self.Attrition_Model_Female.GetVector( self.Ages)
            attrition /= 2
            ax1.plot( self.Ages, attrition, "-", lw=2, label="LEB={:.0f} лет".format(leb))
        ax1.set_xlim( -30, 100)
        ax1.set_ylim( 0, 0.25)
        ax1.grid(True)
        ax1.set_ylabel("Коэффициент смертности")
        ax1.legend(loc=2)

        ax2.plot( self.Ages, self.Fertility_Model.GetVector(self.Ages),
                  "-", lw=2, label="Биологическая фертильность")
        ax2.plot( self.Ages, self.Workforce_Model.GetVector(self.Ages),
                  "-", lw=2, label="Работоспособный возраст")
        ax2.grid(True)
        ax2.set_xlim( -30, 100)
        ax2.set_xlabel("Возраст [лет]")
        ax2.set_ylabel("Часть популяции")
        ax2.legend(loc=2)
        plt.savefig( filename)
        self.LEB_Male = pv_Male
        self.LEB_Female = pv_Female
        return
        
class W3_Population():
    """
    Describes population system similar to World3 implementation
    year0 - starting model year, increment 1 year
    """
    def __init__( self, year0=1890, goodsPC=25.0, foodPC=270.0, servicesPC=100.0, biological_TFR=6.0, verbose=False):
        self.Year = year0
        self.Demographics = W3_Demographics(year0)
        self.Goods = goodsPC * self.Demographics.Total / 1000
        self.Food = foodPC * self.Demographics.Total / 1000
        self.Services = servicesPC * self.Demographics.Total / 1000
        self.Pollution = 0.0
        self.GoodsPC = goodsPC 
        self.FoodPC = foodPC
        self.ServicesPC = servicesPC
        self.LEB_Food_Model = Sigmoid( 0, 0.0050, -45, 45)
        self.LEB_Services_Model = Sigmoid( 200, 0.012, 1.0, 2.0)
        self.LEB_Services_Delay = Delay( delay=25, default_value = servicesPC)
        self.LEB_Services_Delay.Name = "Services Delay = 25 years"
        self.TFR_LEB_Model = Sigmoid( 55, 0.25, 2.8, 1.45)
        self.TFR_LEB_Delay = Delay( delay=50, default_value = 30)
        self.TFR_LEB_Delay.Name = "Demographic Delay = 50 years"
        self.TFR_Goods_Model = Sigmoid( 120, 0.05, 1.68, 1)
        self.TFR_Social_Delay = Delay( delay=40, default_value = 20)
        self.TFR_Social_Delay.Name = "Social Delay = 40 years"
        self.Family_Planning_Model = Sigmoid( 130, 0.03, biological_TFR, 1.0)
        self.Compute_LEB()
        self.Compute_TFR()
        if verbose:
            print( "Population in {:.0f}: ".format( year0))
            print( "   Males      {:>6.1f} mln".format( self.Demographics.Total_Male))
            print( "   Females    {:>6.1f} mln".format( self.Demographics.Total_Female))
            print( "   Total      {:>6.1f} mln".format( self.Demographics.Total))
            print( "   Labor      {:>6.1f} mln".format( self.Demographics.Labor))
            print( "   Male ratio {:>6.2f}:100".format( self.Demographics.Total_Male * 100 / self.Demographics.Total_Female))            
            print( "   LEB        {:>6.1f} years".format( self.LEB))            
            print( "   TFR        {:>6.1f}".format( self.TFR))            
            print( "Total consumption in {:.0f}: ".format( year0))
            print( "   Goods      {:>5.1f} mln tonn".format( self.Goods))
            print( "   Food       {:>5.1f} mln tonn".format( self.Food))
            print( "   Services  ${:>5.1f} bln".format( self.Services))
            print( "Per head consumption in {:.0f}: ".format( year0))
            print( "   Goods      {:>5.1f} kg".format( self.GoodsPC))
            print( "   Food       {:>5.1f} kg".format( self.FoodPC))
            print( "   Services  ${:>5.1f}".format( self.ServicesPC))
        return
    def Compute_LEB(self):
        """
        LEB parametrization - roughly corresponds to World3 v 2003
        """
        self.LEB = self.LEB_Food_Model.Compute( self.FoodPC)
        self.LEB *= self.LEB_Services_Model.Compute( self.LEB_Services_Delay.Get_Average())
        if self.LEB < 1.0: self.LEB = 1.0 
        return
    def Compute_TFR(self):
        """
        TFR parametrization - roughly corresponds to World3 v 2003
        """
        self.TFR = self.TFR_LEB_Model.Compute( self.TFR_LEB_Delay.Get_Average())
        self.TFR *= self.TFR_Goods_Model.Compute( self.TFR_Social_Delay.Get_Average())
        self.Family_Planning_Model.Right = self.TFR 
        self.TFR = self.Family_Planning_Model.Compute( self.ServicesPC)
        if self.TFR < 1.0: self.TFR = 1.0 
        return
    def Compute_Next_Year( self, goods=None, food=None, services=None, pollution=None, m2f=None, dleb=None):
        """
        Calculates next year in the model
        """
        self.Year += 1
        if not goods is None: self.Goods = goods
        if not food is None: self.Food = food
        if not services is None: self.Services = services
        if not pollution is None: self.Pollution = pollution
        self.GoodsPC = self.Goods * 1000.0 / self.Demographics.Total
        self.FoodPC = self.Food * 1000.0 / self.Demographics.Total
        self.ServicesPC = self.Services * 1000.0 / self.Demographics.Total
        self.LEB_Services_Delay.Set_Value(self.ServicesPC)
        self.Compute_LEB()
        self.TFR_LEB_Delay.Set_Value(self.LEB)
        self.TFR_Social_Delay.Set_Value(self.GoodsPC)
        self.Compute_TFR()
        self.Demographics.Compute_Next_Year(tfr=self.TFR, leb=self.LEB, m2f=m2f, dleb=dleb)
        return
    def Plot_LEB_Functions( self, filename = "./Graphs/figure_20_04.png"):
        """
        Test plot
        """
        fig = plt.figure( figsize=(15,8))
        fig.suptitle('Зависимость LEB от доступности продовольствия и услуг', fontsize=25)
        gs = plt.GridSpec(1, 1) 
        ax1 = plt.subplot(gs[0])
        food = np.linspace( 0, 800)
        LEB0 = self.LEB_Food_Model.GetVector( food)
        for services in [600, 500, 400, 300, 200, 100, 0]:
            LEB = LEB0 * self.LEB_Services_Model.Compute( services)
            ax1.plot( food, LEB, "-", lw=2, label="{:.0f} усл.$".format(services))
        ax1.set_xlim( food[0], food[-1])
        ax1.set_ylim( 0, 100)
        ax1.grid(True)
        ax1.legend(loc=0)
        ax1.set_xlabel("Продовольствие на душу [кг эквивалента в год]")
        ax1.set_ylabel("Ожидаемая продолжительность жизни [лет]")
        plt.savefig( filename)
        return
    def Plot_TFR_Functions( self, filename = "./Graphs/figure_20_05.png"):
        """
        Test plot
        """
        fig = plt.figure( figsize=(15,8))
        fig.suptitle('Зависимость TFR от LEB и доступности потребительских товаров', fontsize=25)
        gs = plt.GridSpec(1, 1) 
        ax1 = plt.subplot(gs[0])
        LEB0 = np.linspace( 0, 90, 201)
        TFR0 = self.TFR_LEB_Model.GetVector( LEB0)
        for goods in [0, 50, 100, 150, 200, 250]:
            TFR = TFR0 * self.TFR_Goods_Model.Compute( goods)
            ax1.plot( LEB0, TFR, "-", lw=2, label="{:.0f} кг/год".format(goods))
        ax1.set_xlim( LEB0[0], LEB0[-1])
        ax1.set_ylim( 0, 6)
        ax1.grid(True)
        ax1.legend(loc=0)
        ax1.set_xlabel(
            "Продожительность жизни в среднем за последние {:.0f} лет".format(len(self.TFR_LEB_Delay.Chain)))
        ax1.set_ylabel("Желаемое количество детей в семье")
        plt.savefig( filename)
        return
    def Plot_Calibration( self, filename = "./Graphs/figure_20_06.png"):
        """
        Test plot
        """
        P0 = Population()
        P1 = Interpolation_BAU_1972()
        P2 = Interpolation_BAU_2012()
        W3_mod = Interpolation_BAU_2002()
        W3_mod.Solve( np.linspace(1890, 2100, 211))
        P0.Solve(W3_mod.Time)
        P1.Solve(W3_mod.Time)
        P2.Solve(W3_mod.Time)

        l = len( W3_mod.Time)
        POP_Actual = np.zeros(l)
        TFR_Actual = np.zeros(l)
        LEB_Actual = np.zeros(l)
        GoodsPC_Actual = np.zeros(l)
        FoodPC_Actual = np.zeros(l)
        ServicesPC_Actual = np.zeros(l)
        conversion = 0.94
        for i,y in enumerate(W3_mod.Time):
            POP_Actual[i] = self.Demographics.Total
            TFR_Actual[i] = self.TFR
            LEB_Actual[i] = self.LEB
            GoodsPC_Actual[i] = self.GoodsPC
            FoodPC_Actual[i] = self.FoodPC
            ServicesPC_Actual[i] = self.ServicesPC
            self.Compute_Next_Year(goods=W3_mod.Goods[i]*conversion,
                                 food=W3_mod.Food[i]*conversion,
                                 services=W3_mod.Services[i]*conversion)
        LEB_Actual[0] = LEB_Actual[1]
        TFR_Actual[0] = TFR_Actual[1]

        limits = 1900, 2100

        fig = plt.figure( figsize=(15,15))
        fig.suptitle('Проверка модели "World3" 2003 г', fontsize=25)
        gs = plt.GridSpec(3, 1) 
        ax1 = plt.subplot(gs[0])
        ax2 = plt.subplot(gs[1])
        ax3 = plt.subplot(gs[2])

        ax1.plot( W3_mod.Time, W3_mod.Goods/1000, "-", lw=2, color="r", label="Промтовары [млрд т]")
        ax1.plot( W3_mod.Time, W3_mod.Food/1000, "-", lw=2, color="g", label="Продовольствие [млрд т]")
        ax1.plot( W3_mod.Time, W3_mod.Services/1000, "-", lw=2, color="m", label="Услуги [трлн усл.$]")
        j = np.argmax(W3_mod.Goods)
        t = W3_mod.Time[j]
        v = W3_mod.Goods[j] / 1000
        ax1.plot( [t, t], [v-0.5,v+0.5], "--", lw=1, color="r")
        ax1.text( t-10, v+0.6, "{:.1f} млрд т в {:.0f} году".format( v, t), fontsize=12, color="r")
        j = np.argmax(W3_mod.Food)
        t = W3_mod.Time[j]
        v = W3_mod.Food[j] / 1000
        ax1.plot( [t, t], [v-0.5,v+0.5], "--", lw=1, color="g")
        ax1.text( t-10, v-0.6, "{:.1f} млрд т в {:.0f} году".format( v, t), fontsize=12, color="g")
        j = np.argmax(W3_mod.Services)
        t = W3_mod.Time[j]
        v = W3_mod.Services[j] / 1000
        ax1.plot( [t, t], [v-0.5,v+0.5], "--", lw=1, color="m")
        ax1.text( t-45, v, "{:.1f} трлн усл.$ в {:.0f} году".format( v, t), fontsize=12, color="m")
        ax1.set_xlim( limits)
        ax1.set_ylim( 0, 5)
        ax1.grid(True)
        ax1.legend(loc=0)
        ax1.set_ylabel("экономика всего")

        ax2.plot( W3_mod.Time, W3_mod.GoodsPC, "--", lw=2, color="r")
        ax2.plot( W3_mod.Time, W3_mod.FoodPC, "--", lw=2, color="g")
        ax2.plot( W3_mod.Time, W3_mod.ServicesPC, "--", lw=2, color="m")
        ax2.plot( W3_mod.Time, GoodsPC_Actual, "-", lw=2, color="r", label="Промтовары [кг]")
        ax2.plot( W3_mod.Time, FoodPC_Actual, "-", lw=2, color="g", label="Продовольствие [кг]")
        ax2.plot( W3_mod.Time, ServicesPC_Actual, "-", lw=2, color="m", label="Услуги [усл. $]")
        j = np.argmax(GoodsPC_Actual)
        t = W3_mod.Time[j]
        v = GoodsPC_Actual[j]
        ax2.plot( [t, t], [v-100,v+70], "--", lw=1, color="r")
        ax2.text( t-10, v+80, "{:.0f} кг в {:.0f} году".format( v, t), fontsize=12, color="r")
        j = np.argmax(FoodPC_Actual)
        t = W3_mod.Time[j]
        v = FoodPC_Actual[j]
        ax2.plot( [t, t], [v-100,v+100], "--", lw=1, color="g")
        ax2.text( t-10, v-130, "{:.0f} кг в {:.0f} году".format( v, t), fontsize=12, color="g")
        j = np.argmax(ServicesPC_Actual)
        t = W3_mod.Time[j]
        v = ServicesPC_Actual[j]
        ax2.plot( [t, t], [v-100,v+40], "--", lw=1, color="m")
        ax2.text( t-20, v+50, "{:.0f} усл. $ в {:.0f} году".format( v, t), fontsize=12, color="m")
        ax2.set_xlim( limits)
        ax2.set_ylim( 0, 700)
        ax2.grid(True)
        ax2.legend(loc=0)
        ax2.set_ylabel("экономика на душу")

        ax3.plot( W3_mod.Time, POP_Actual/1000, "-", lw=2, color="b", label="наша модель")
        ax3.plot( W3_mod.Time, W3_mod.Population/1000, "--", lw=2, color="b", label="World3, 2003")
        #ax3.plot( W3_mod.Time[110:], P0.Solution_UN_Medium[110:]/1000, ".", lw=2, color="b", label="Средняя оценка ООН, 2015")
        #ax3.plot( W3_mod.Time, P1.Population/1000, "-.", lw=2, color="g", label="World3, 1972")
        #ax3.plot( W3_mod.Time, P2.Population/1000, "-.", lw=2, color="m", label="Й.Рандерс, 2012")
        ax3.errorbar(P0.Calibration_Year, P0.Calibration_Total/1000, yerr=P0.Calibration_Yerr/1000,
                     fmt=".", color="k", label="Реальная")
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
    print("*** Demographics Check ***")
    demo = W3_Demographics()
    demo.Plot_Attrition_Function()
    demo.Plot_Demographic_Functions()
    
    print("*** Population Check ***")
    model = W3_Population( verbose=True)
    model.Plot_LEB_Functions()
    model.Plot_TFR_Functions()
    model.Plot_Calibration()
    
    if InteractiveModeOn: plt.show(True)
