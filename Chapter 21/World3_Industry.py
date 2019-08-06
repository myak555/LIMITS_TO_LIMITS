from World3_Model import *

class W3_Capital():
    """
    Describes capital subsystem similar to World3 implementation
    year0 - starting model year, increment 1 year
    """
    def __init__( self, year0=1890, goodsPC=25.0, foodPC=270.0, servicesPC=100.0, biological_TFR=6.0, verbose=False):
        self.Population = W3_Population( year0, goodsPC, foodPC, servicesPC, biological_TFR, verbose)
##        if verbose:
##            print( "Total consumption in {:.0f}: ".format( year0))
##            print( "   Goods      {:>5.1f} mln tonn".format( self.Population.Goods))
##            print( "   Food       {:>5.1f} mln tonn".format( self.Population.Food))
##            print( "   Services  ${:>5.1f} bln".format( self.Population.Services))
##            print( "Per head consumption in {:.0f}: ".format( year0))
##            print( "   Goods      {:>5.1f} kg".format( self.Population.GoodsPC))
##            print( "   Food       {:>5.1f} kg".format( self.Population.FoodPC))
##            print( "   Services  ${:>5.1f}".format( self.Population.ServicesPC))
        return
    def Compute_Next_Year( self, goods=None, food=None, services=None, pollution=None, m2f=None, dleb=None):
        """
        Calculates next year in the model
        """
        self.Population.Compute_Next_Year( goods, food, services, pollution, m2f, dleb)
        return
##    def Plot_LEB_Functions( self, filename = "./Graphs/figure_20_04.png"):
##        """
##        Test plot
##        """
##        fig = plt.figure( figsize=(15,8))
##        fig.suptitle('Зависимость LEB от доступности продовольствия и услуг', fontsize=25)
##        gs = plt.GridSpec(1, 1) 
##        ax1 = plt.subplot(gs[0])
##        food = np.linspace( 0, 800)
##        LEB0 = self.LEB_Food_Model.GetVector( food)
##        for services in [600, 500, 400, 300, 200, 100, 0]:
##            LEB = LEB0 * self.LEB_Services_Model.Compute( services)
##            ax1.plot( food, LEB, "-", lw=2, label="{:.0f} усл.$".format(services))
##        ax1.set_xlim( food[0], food[-1])
##        ax1.set_ylim( 0, 100)
##        ax1.grid(True)
##        ax1.legend(loc=0)
##        ax1.set_xlabel("Продовольствие на душу [кг эквивалента в год]")
##        ax1.set_ylabel("Ожидаемая продолжительность жизни [лет]")
##        plt.savefig( filename)
##        return
    def Plot_Fossil_Fuel( self, filename = "./Graphs/figure_21_01.png"):
        """
        Test plot for fossil fuel production
        """
        P0 = Population()
        P1 = Interpolation_BAU_1972()
        P2 = Interpolation_BAU_2012()
        R0 = Resources()
        W3_mod = Interpolation_BAU_2002()
        W3_mod.Solve( np.linspace(1890, 2100, 211))
        P0.Solve(W3_mod.Time)
        P1.Solve(W3_mod.Time)
        P2.Solve(W3_mod.Time)
        R0.Solve(W3_mod.Time)

        l = len( W3_mod.Time)
        POP_Actual = np.zeros(l)
        Industrial_Capital_Actual = np.zeros(l)
        Industrial_Output_Actual = np.zeros(l)
        GoodsPC_Actual = np.zeros(l)
        FoodPC_Actual = np.zeros(l)
        ServicesPC_Actual = np.zeros(l)
        conversion = 0.94
        for i,y in enumerate(W3_mod.Time):
            POP_Actual[i] = self.Population.Demographics.Total
            GoodsPC_Actual[i] = self.Population.GoodsPC
            FoodPC_Actual[i] = self.Population.FoodPC
            ServicesPC_Actual[i] = self.Population.ServicesPC
            self.Population.Compute_Next_Year(goods=W3_mod.Goods[i]*conversion,
                                 food=W3_mod.Food[i]*conversion,
                                 services=W3_mod.Services[i]*conversion)

        limits = 1900, 2100

        fig = plt.figure( figsize=(15,15))
        fig.suptitle('Проверка модели "World3": ископаемое топливо', fontsize=25)
        gs = plt.GridSpec(3, 1) 
        ax1 = plt.subplot(gs[0])
        ax2 = plt.subplot(gs[1])
        ax3 = plt.subplot(gs[2])

        #ax1.plot( W3_mod.Time, Industrial_Capital_Actual, "-", lw=2, color="r")
        ax1.plot( W3_mod.Time, P1.Resources/1000, "-.", lw=2, color="b", label="World3, 1972")
        ax1.plot( W3_mod.Time, W3_mod.Resources/1000, ".", lw=1, color="b", label="World3, 2003")
        ax1.plot( W3_mod.Time, P2.Resources/1000, "--", lw=2, color="b", label="Й.Рандерс, 2012")
        #ax1.plot( W3_mod.Time, P2.Resources, "--", lw=2, color="b")
##        ax2.plot( W3_mod.Time, W3_mod.ServicesPC, "--", lw=2, color="m")
##        ax2.plot( W3_mod.Time, GoodsPC_Actual, "-", lw=2, color="r", label="Промтовары [кг]")
##        ax2.plot( W3_mod.Time, FoodPC_Actual, "-", lw=2, color="g", label="Продовольствие [кг]")
##        ax2.plot( W3_mod.Time, ServicesPC_Actual, "-", lw=2, color="m", label="Услуги [усл. $]")
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
        ax1.set_ylabel("Извлекаемые запасы [млрд т]")

        ax2.plot( W3_mod.Time, P1.Energy/1000, "-.", lw=2, color="b", label="World3, 1972")
        ax2.plot( W3_mod.Time, W3_mod.Energy/1000, ".", lw=2, color="b", label="World3, 2003")
        ax2.plot( W3_mod.Time, P2.Energy_Carbon/1000, "--", lw=2, color="b", label="Й.Рандерс, 2012")
        #ax2.plot( W3_mod.Time, W3_mod.Goods/1000, "-.", lw=2, color="r", label="Промтовары World3, 2003 [млрд т]")
        #ax2.plot( W3_mod.Time, W3_mod.Food/1000, "-.", lw=2, color="g", label="Продовольствие World3, 2003 [млрд т]")
        #ax2.plot( W3_mod.Time, W3_mod.Services/1000, "-.", lw=2, color="m", label="Услуги World3, 2003 [трлн усл.$]")
        ax2.errorbar( R0.Calibration_Year, R0.Calibration_Carbon/1000, yerr=R0.Calibration_Carbon/20000, fmt=".", color="k", label="Реальная добыча [млрд т]")
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
        ax2.set_ylim( 0, 25)
        ax2.grid(True)
        ax2.legend(loc=0)
        ax2.set_ylabel("Годовая добыча [млрд т]")

        ax3.plot( W3_mod.Time, P1.Population/1000, "-.", lw=2, color="b", label="World3, 1972")
        ax3.plot( W3_mod.Time, W3_mod.Population/1000, ".", lw=1, color="b", label="World3, 2003")
        ax3.plot( W3_mod.Time[110:], P0.Solution_UN_Medium[110:]/1000, "-.", lw=2, color="r",  alpha=0.5, label="Средняя оценка ООН, 2015")
        ax3.plot( W3_mod.Time, P2.Population/1000, "--", lw=2, color="b", label="Й.Рандерс, 2012")
        ax3.plot( W3_mod.Time, POP_Actual/1000, "-", lw=4, color="g", alpha=0.5, label="наша модель")
        ax3.errorbar(P0.Calibration_Year, P0.Calibration_Total/1000, yerr=P0.Calibration_Yerr/1000,
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
    model = W3_Capital( verbose=True)
    model.Plot_Fossil_Fuel()
    #print("*** Industry Check ***")
    
    if InteractiveModeOn: plt.show(True)
