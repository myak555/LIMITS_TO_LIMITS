from Predictions import *

class W3_Demographics:
    """
    Describes demographics system similar to World3 implementation
    year0 - starting model year, increment 1 year
    population0 - total population in year 0
    tfr - total fertility rate before year 0
    leb - life expectancy at birth before year 0
    m2f - male:female ratio at birth before year 0
    """
    def __init__( self, year0=1890, population0=1530.880, tfr=5.4, leb=30, m2f=1.05):
        self.Year = year0
        self.Ages = np.linspace( 0,199, 200)
        self.Population_Male = np.ones( 200)
        self.Population_Female = np.ones( 200)
        self.Attrition_Model_Male = Bathtub( x0=5.0, s0=1.0, x1=80, s1=0.2, left=0.1, middle=0.01, right=0.20)
        self.Attrition_Model_Female = Bathtub( x0=5.0, s0=1.0, x1=80, s1=0.2, left=0.1, middle=0.01, right=0.20)
        self.Fertility_Model = Bathtub( x0=18.0, s0=1.0, x1=35, s1=0.4, left=0.0, middle=1, right=0)
        self.Workforce_Model = Bathtub( x0=16.0, s0=1.0, x1=65, s1=0.4, left=0.0, middle=1, right=0)
        self.TFR = tfr
        self.LEB_Male = leb-2
        self.LEB_Female = leb+2
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
        if not attr is None:
            self.Attrition_Model_Male.Left = attr
            self.Attrition_Model_Male.Middle = attr * 0.1
            self.Attrition_Model_Female.Left = attr
            self.Attrition_Model_Female.Middle = attr * 0.1
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
    def Compute_Next_Year( self, tfr=None, leb=None, m2f=None):
        self.Year += 1
        if not tfr is None: self.TFR = tfr
        if not leb is None:
            self.LEB_Male = leb-2
            self.LEB_Female = leb+2
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
        self.Total = np.sum(self.Population_Male) + np.sum(self.Population_Female)
        workforce = self.Workforce_Model.GetVector(self.Ages)
        self.Labor = np.dot(self.Population_Male+self.Population_Female, workforce)
        return
    def Normalize( self, norm):
        n = np.sum( self.Population_Male) + np.sum( self.Population_Female)
        if n <= 0.0: return
        n = norm/n
        self.Population_Male *= n
        self.Population_Female *= n
        self.Total = np.sum(self.Population_Male) + np.sum(self.Population_Female)
        workforce = self.Workforce_Model.GetVector(self.Ages)
        self.Labor = np.dot(self.Population_Male+self.Population_Female, workforce)
        return

class W3_Population():
    """
    Describes population system similar to World3 implementation
    year0 - starting model year, increment 1 year
    this preliminary version uses per-capita inputs for calibration
    """
    def __init__( self, year0=1890, goodsPC=25, foodPC=270, servicesPC=100, biological_TFR=6.0):
        self.Demographics = W3_Demographics(year0)
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
        return
    def Compute_LEB(self):
        self.LEB = self.LEB_Food_Model.Compute( self.FoodPC)
        self.LEB *= self.LEB_Services_Model.Compute( self.LEB_Services_Delay.Get_Average())
        if self.LEB < 1.0: self.LEB = 1.0 
        return
    def Compute_TFR(self):
        self.TFR = self.TFR_LEB_Model.Compute( self.TFR_LEB_Delay.Get_Average())
        self.TFR *= self.TFR_Goods_Model.Compute( self.TFR_Social_Delay.Get_Average())
        self.Family_Planning_Model.Right = self.TFR 
        self.TFR = self.Family_Planning_Model.Compute( self.ServicesPC)
        if self.TFR < 1.0: self.TFR = 1.0 
        return
    def Compute_Next_Year( self, goodsPC=None, foodPC=None, servicesPC=None, m2f=None):
        if not goodsPC is None: self.GoodsPC = goodsPC
        if not foodPC is None: self.FoodPC = foodPC
        if not servicesPC is None: self.ServicesPC = servicesPC
        self.LEB_Services_Delay.Set_Value(self.ServicesPC)
        self.Compute_LEB()
        self.TFR_LEB_Delay.Set_Value(self.LEB)
        self.TFR_Social_Delay.Set_Value(self.GoodsPC)
        self.Compute_TFR()
        self.Demographics.Compute_Next_Year(tfr=self.TFR, leb=self.LEB, m2f=m2f)
        return
    def Plot_Calibration( self, filename = "./Graphs/figure_20_01.png"):
        tfr = Linear_Combo()
        tfr.Wavelets += [Sigmoid( x0=1975.000, s0=0.07740, left=5.400, right=2.350)]
        tfr.Wavelets += [Hubbert( x0=1967.000, s0=0.29510, s1=0.24133, peak=0.631)]
        tfr.Wavelets += [Hubbert( x0=1987.000, s0=0.43047, s1=0.43047, peak=0.211)]
        tfr.Wavelets += [Hubbert( x0=1998.000, s0=0.53144, s1=0.31381, peak=-0.074)]
        tfr.Wavelets += [Hubbert( x0=1955.000, s0=1.00000, s1=1.00000, peak=-0.057)]
        tfr.Wavelets += [Hubbert( x0=1962.000, s0=1.00000, s1=1.00000, peak=0.048)]
        tfr.Wavelets += [Hubbert( x0=1978.000, s0=1.00000, s1=1.00000, peak=-0.030)]
        tfr.Wavelets += [Hubbert( x0=2014.000, s0=0.59049, s1=0.59049, peak=0.017)]
        tfr.Wavelets += [Hubbert( x0=1955, s0=0.2, s1=0.09, peak=0.5)]

        tfr2 = Linear_Combo()
        tfr2.Wavelets += [Sigmoid( x0=1970.000, s0=0.07740, left=5.400, right=3.00)]
        tfr2.Wavelets += [Sigmoid( x0=2010.000, s0=0.3, left=0, right=-1.6)]
        tfr2.Wavelets += [Sigmoid( x0=2060.000, s0=0.2, left=0, right=4.5)]

        leb = Linear_Combo()
        leb.Wavelets  = [Sigmoid( x0=1965.000, s0=0.03183, left=26.500, right=80.400)]
        leb.Wavelets += [Hubbert( x0=1975.000, s0=0.18500, s1=0.13500, peak=1.632)]
        leb.Wavelets += [Hubbert( x0=2000.000, s0=0.28000, s1=0.31000, peak=-1.000)]
        leb.Wavelets += [Hubbert( x0=1961.000, s0=0.15009, s1=0.47500, peak=-1.700)]
        leb.Wavelets += [Hubbert( x0=1948, s0=0.1, s1=1, peak=-7)]
              
        P0 = Population()
        P1 = Interpolation_BAU_1972()
        P2 = Interpolation_BAU_2012()
        W3_mod = Interpolation_BAU_2002()
        W3_mod.Solve( np.linspace(1890, 2100, 211))
        P0.Solve(W3_mod.Time)
        P1.Solve(W3_mod.Time)
        P2.Solve(W3_mod.Time)

        l = len(W3_mod.Time)
        POP_Actual = np.zeros(l)
        TFR_Actual = np.zeros(l)
        LEB_Actual = np.zeros(l)
        for i,y in enumerate(W3_mod.Time):
            POP_Actual[i] = W3.Demographics.Total
            TFR_Actual[i] = W3.TFR
            LEB_Actual[i] = W3.LEB
            W3.Compute_Next_Year(goodsPC=W3_mod.GoodsPC[i], foodPC=W3_mod.FoodPC[i], servicesPC=W3_mod.ServicesPC[i])
        LEB_Actual[0] = LEB_Actual[1]
        TFR_Actual[0] = TFR_Actual[1]
        LEB_Estimate = leb.GetVector( W3_mod.Time)
        TFR_Estimate = tfr.GetVector( W3_mod.Time)
        TFR_Model = tfr2.GetVector( W3_mod.Time)

        limits = 1900, 2100

        fig = plt.figure( figsize=(15,15))
        fig.suptitle('Проверка модели "World3" 2003 г', fontsize=25)
        gs = plt.GridSpec(3, 1) 
        ax1 = plt.subplot(gs[0])
        ax2 = plt.subplot(gs[1])
        ax3 = plt.subplot(gs[2])

        ax1.set_title("Потребление в модели World3 2003 года", fontsize=18)
        ax1.plot( W3_mod.Time, W3_mod.GoodsPC, "-", lw=2, color="r", label="Промтовары [кг]")
        ax1.plot( W3_mod.Time, W3_mod.FoodPC, "-", lw=2, color="g", label="Продовольствие [кг]")
        ax1.plot( W3_mod.Time, W3_mod.ServicesPC, "-", lw=2, color="m", label="Услуги [усл. $]")
        j = np.argmax(W3_mod.GoodsPC)
        t = W3_mod.Time[j]
        v = W3_mod.GoodsPC[j]
        ax1.plot( [t, t], [v-100,v+70], "--", lw=1, color="r")
        ax1.text( t-10, v+80, "{:.0f} кг в {:.0f} году".format( v, t), fontsize=12, color="r")
        j = np.argmax(W3_mod.FoodPC)
        t = W3_mod.Time[j]
        v = W3_mod.FoodPC[j]
        ax1.plot( [t, t], [v-100,v+100], "--", lw=1, color="g")
        ax1.text( t-10, v-130, "{:.0f} кг в {:.0f} году".format( v, t), fontsize=12, color="g")
        j = np.argmax(W3_mod.ServicesPC)
        t = W3_mod.Time[j]
        v = W3_mod.ServicesPC[j]
        ax1.plot( [t, t], [v-100,v+40], "--", lw=1, color="m")
        ax1.text( t-20, v+50, "{:.0f} усл. $ в {:.0f} году".format( v, t), fontsize=12, color="m")
        ax1.set_xlim( limits)
        ax1.set_ylim( 0, 700)
        ax1.grid(True)
        ax1.legend(loc=0)

        ax2.plot( W3_mod.Time, LEB_Actual, "-", lw=2, color="b")
        ax2.plot( W3_mod.Time, W3_mod.LEB, "--", lw=2, color="b")
        ax2.plot( W3_mod.Time, LEB_Estimate, ".", lw=2, color="b")
        ax2.text( limits[0]+2, LEB_Estimate[0]+6, "LEB", color="b", fontsize=20)
        ax2.plot( W3_mod.Time, TFR_Actual*10, "-", lw=2, color="g", label="наша модель")
        ax2.plot( W3_mod.Time, TFR_Model*10, "--", lw=2, color="g", label="World3, 2003")
        ax2.plot( W3_mod.Time, TFR_Estimate*10, ".", lw=2, color="g", label="ООН, 2015")
        ax2.text( limits[0]+2, TFR_Estimate[0]*10+6, "TFR x 10", color="g", fontsize=20)
        ax2.set_xlim( limits)
        ax2.set_ylim( 0, 85)
        ax2.set_ylabel("Демография")
        ax2.grid(True)
        ax2.legend(loc=0)

        ax3.plot( W3_mod.Time, POP_Actual/1020, "-", lw=2, color="b", label="наша модель")
        ax3.plot( W3_mod.Time, W3_mod.Population/1020, "--", lw=2, color="b", label="World3, 2003")
        ax3.plot( W3_mod.Time[110:], P0.Solution_UN_Medium[110:]/1000, ".", lw=2, color="b", label="Средняя оценка ООН, 2015")
        ax3.plot( W3_mod.Time, P1.Population/1000, "-.", lw=2, color="g", label="World3, 1972")
        ax3.plot( W3_mod.Time, P2.Population/1000, "-.", lw=2, color="m", label="Й.Рандерс, 2012")
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

    def Plot_Comparison( self, filename = "./Graphs/figure_20_01a.png"):
        cYear,cPopulation,cChildren,cLEB,cTFR,cIndustrialPC,cServicesPC,cFoodPC = Load_Calibration(
            "./Data/Life_Quality_Checks.csv",
            ['Time','_001_Population','_002_Population0To14','_019_LifeExpectancy','_032_TotalFertility',
             '_049_IndustrialOutputPerCapita','_071_ServiceOutputPerCapita','_088_FoodPerCapita'])
        tfr = Linear_Combo()
        tfr.Wavelets += [Sigmoid( x0=1975.000, s0=0.07740, left=5.400, right=2.350)]
        tfr.Wavelets += [Hubbert( x0=1967.000, s0=0.29510, s1=0.24133, peak=0.631)]
        tfr.Wavelets += [Hubbert( x0=1987.000, s0=0.43047, s1=0.43047, peak=0.211)]
        tfr.Wavelets += [Hubbert( x0=1998.000, s0=0.53144, s1=0.31381, peak=-0.074)]
        tfr.Wavelets += [Hubbert( x0=1955.000, s0=1.00000, s1=1.00000, peak=-0.057)]
        tfr.Wavelets += [Hubbert( x0=1962.000, s0=1.00000, s1=1.00000, peak=0.048)]
        tfr.Wavelets += [Hubbert( x0=1978.000, s0=1.00000, s1=1.00000, peak=-0.030)]
        tfr.Wavelets += [Hubbert( x0=2014.000, s0=0.59049, s1=0.59049, peak=0.017)]
        tfr.Wavelets += [Hubbert( x0=1955, s0=0.2, s1=0.09, peak=0.5)]

        tfr2 = Linear_Combo()
        tfr2.Wavelets += [Sigmoid( x0=1970.000, s0=0.07740, left=5.400, right=3.00)]
        tfr2.Wavelets += [Sigmoid( x0=2010.000, s0=0.3, left=0, right=-1.6)]
        tfr2.Wavelets += [Sigmoid( x0=2060.000, s0=0.2, left=0, right=4.5)]

        leb = Linear_Combo()
        leb.Wavelets  = [Sigmoid( x0=1965.000, s0=0.03183, left=26.500, right=80.400)]
        leb.Wavelets += [Hubbert( x0=1975.000, s0=0.18500, s1=0.13500, peak=1.632)]
        leb.Wavelets += [Hubbert( x0=2000.000, s0=0.28000, s1=0.31000, peak=-1.000)]
        leb.Wavelets += [Hubbert( x0=1961.000, s0=0.15009, s1=0.47500, peak=-1.700)]
        leb.Wavelets += [Hubbert( x0=1948, s0=0.1, s1=1, peak=-7)]
              
        P0 = Population()
        W3_mod = Interpolation_BAU_2002()
        W3_mod.Solve( np.linspace(1890, 2100, 211))
        P0.Solve(W3_mod.Time)

        l = len(W3_mod.Time)
        POP_Actual = np.zeros(l)
        TFR_Actual = np.zeros(l)
        LEB_Actual = np.zeros(l)
        for i,y in enumerate(W3_mod.Time):
            POP_Actual[i] = self.Demographics.Total
            TFR_Actual[i] = self.TFR
            LEB_Actual[i] = self.LEB
            W3.Compute_Next_Year(goodsPC=W3_mod.GoodsPC[i], foodPC=W3_mod.FoodPC[i], servicesPC=W3_mod.ServicesPC[i])
        LEB_Actual[0] = LEB_Actual[1]
        TFR_Actual[0] = TFR_Actual[1]
        LEB_Estimate = leb.GetVector( W3_mod.Time)
        TFR_Estimate = tfr.GetVector( W3_mod.Time)
        TFR_Model = tfr2.GetVector( W3_mod.Time)

        limits = 1900, 2100

        fig = plt.figure( figsize=(15,15))
        fig.suptitle('Проверка модели "World3" 2003 г', fontsize=25)
        gs = plt.GridSpec(3, 1) 
        ax1 = plt.subplot(gs[0])
        ax2 = plt.subplot(gs[1])
        ax3 = plt.subplot(gs[2])

        ax1.set_title("Потребление в модели World3 2003 года", fontsize=18)
        ax1.plot( W3_mod.Time, W3_mod.GoodsPC, "-", lw=2, color="r", label="Промтовары [кг]")
        ax1.plot( W3_mod.Time, W3_mod.ServicesPC, "-", lw=2, color="y", label="Услуги [усл. $]")
        ax1.plot( W3_mod.Time, W3_mod.FoodPC, "-", lw=2, color="g", label="Продовольствие [кг]")
        ax1.plot( cYear, cIndustrialPC, "o", lw=2, color="r", alpha=0.5, label="BAU World3")
        ax1.plot( cYear, cServicesPC, "o", lw=2, color="y", alpha=0.5)
        ax1.plot( cYear, cFoodPC, "o", lw=2, color="g", alpha=0.5)
        ax1.set_xlim( limits)
        ax1.set_ylim( 0, 700)
        ax1.grid(True)
        ax1.legend(loc=0)

        ax2.plot( W3_mod.Time, LEB_Actual, "-", lw=2, color="b")
        ax2.plot( cYear, cLEB, "o", lw=2, color="b", alpha=0.5)
        #ax2.plot( W3_mod.Time, W3_mod.LEB, "--", lw=2, color="b")
        #ax2.plot( W3_mod.Time, LEB_Estimate, ".", lw=2, color="b")
        ax2.text( limits[0]+2, LEB_Estimate[0]+6, "LEB", color="b", fontsize=20)
        ax2.plot( W3_mod.Time, TFR_Actual*10, "-", lw=2, color="g", label="наша модель")
        ax2.plot( cYear, cTFR*10, "o", lw=2, color="g", alpha=0.5, label="BAU World3")
        #ax2.plot( W3_mod.Time, TFR_Model*10, "--", lw=2, color="g", label="World3, 2003")
        #ax2.plot( W3_mod.Time, TFR_Estimate*10, ".", lw=2, color="g", label="ООН, 2015")
        ax2.text( limits[0]+2, TFR_Estimate[0]*10+6, "TFR x 10", color="g", fontsize=20)
        ax2.set_xlim( limits)
        ax2.set_ylim( 0, 85)
        ax2.set_ylabel("Демография")
        ax2.grid(True)
        ax2.legend(loc=0)

        ax3.plot( W3_mod.Time, POP_Actual/1000, "-", lw=2, color="b", label="наша модель")
        #ax3.plot( W3_mod.Time, W3_mod.Population/1000, "--", lw=2, color="b", label="World3, 2003")
        #ax3.plot( cYear, cPopulation/1.05e9, "o", lw=2, color="b", alpha=0.5, label="BAU World3")
        ax3.plot( cYear, cPopulation/1.00e9, "o", lw=2, color="b", alpha=0.5, label="BAU World3")
        ax3.plot( cYear, cChildren/1.00e9, "o", lw=2, color="g", alpha=0.5, label="Дети до 15 лет")
        #ax3.plot( W3_mod.Time[110:], P0.Solution_UN_Medium[110:]/1000, ".", lw=2, color="b", label="Средняя оценка ООН, 2015")
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


W3 = W3_Population()
#W3.Plot_Calibration()
W3.Plot_Comparison()
if InteractiveModeOn: plt.show(True)
