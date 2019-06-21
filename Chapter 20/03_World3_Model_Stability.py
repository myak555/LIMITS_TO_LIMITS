from World3_Model import *

def Check_Stability( P0, W3_base, filename, title, signal_Goods, signal_Food, signal_Services, limits = (1900, 2100)):
    model1 = W3_Population()
    model2 = W3_Population()
    l = len(W3_base.Time)
    POP_Actual_1 = np.zeros(l)
    Labor_Actual_1 = np.zeros(l)
    TFR_Actual_1 = np.zeros(l)
    LEB_Actual_1 = np.zeros(l)
    GoodsPC_Actual_1 = np.zeros(l)
    FoodPC_Actual_1 = np.zeros(l)
    ServicesPC_Actual_1 = np.zeros(l)
    POP_Actual_2 = np.zeros(l)
    Labor_Actual_2 = np.zeros(l)
    TFR_Actual_2 = np.zeros(l)
    LEB_Actual_2 = np.zeros(l)
    GoodsPC_Actual_2 = np.zeros(l)
    FoodPC_Actual_2 = np.zeros(l)
    ServicesPC_Actual_2 = np.zeros(l)
    conversion = 0.94
    for i,y in enumerate(W3_base.Time):
        POP_Actual_1[i] = model1.Demographics.Total
        Labor_Actual_1[i] = model1.Demographics.Labor
        TFR_Actual_1[i] = model1.TFR
        LEB_Actual_1[i] = model1.LEB
        GoodsPC_Actual_1[i] = model1.GoodsPC
        FoodPC_Actual_1[i] = model1.FoodPC
        ServicesPC_Actual_1[i] = model1.ServicesPC
        POP_Actual_2[i] = model2.Demographics.Total
        Labor_Actual_2[i] = model2.Demographics.Labor
        TFR_Actual_2[i] = model2.TFR
        LEB_Actual_2[i] = model2.LEB
        GoodsPC_Actual_2[i] = model2.GoodsPC
        FoodPC_Actual_2[i] = model2.FoodPC
        ServicesPC_Actual_2[i] = model2.ServicesPC
        model1.Compute_Next_Year(goods=W3_base.Goods[i]*conversion,
                                 food=W3_base.Food[i]*conversion,
                                 services=W3_base.Services[i]*conversion)
        model2.Compute_Next_Year(goods=W3_base.Goods[i]*conversion*signal_Goods[i],
                                 food=W3_base.Food[i]*conversion*signal_Food[i],
                                 services=W3_base.Services[i]*conversion*signal_Services[i])

    fig = plt.figure( figsize=(15,20))
    fig.suptitle( title, fontsize=25)
    gs = plt.GridSpec(4, 1) 
    ax1 = plt.subplot(gs[0])
    ax2 = plt.subplot(gs[1])
    ax3 = plt.subplot(gs[2])
    ax4 = plt.subplot(gs[3])

    ax1.plot( W3_base.Time, W3_base.Goods/1000, "--", lw=2, color="r")
    ax1.plot( W3_base.Time, W3_base.Goods*signal_Goods/1000, "-", lw=2, color="r", label="Промтовары [млрд т]")
    ax1.plot( W3_base.Time, W3_base.Food/1000, "--", lw=2, color="g")
    ax1.plot( W3_base.Time, W3_base.Food*signal_Food/1000, "-", lw=2, color="g", label="Продовольствие [млрд т]")
    ax1.plot( W3_base.Time, W3_base.Services/1000, "--", lw=2, color="m")
    ax1.plot( W3_base.Time, W3_base.Services*signal_Services/1000, "-", lw=2, color="m", label="Услуги [трлн усл.$]")
    ax1.set_xlim( limits)
    ax1.set_ylim( 0, 5)
    ax1.grid(True)
    ax1.legend(loc=0)
    ax1.set_ylabel("экономика всего")

    ax2.plot( W3_base.Time, GoodsPC_Actual_1, "--", lw=2, color="r")
    ax2.plot( W3_base.Time, GoodsPC_Actual_2, "-", lw=2, color="r", label="Промтовары [кг]")
    ax2.plot( W3_base.Time, FoodPC_Actual_1, "--", lw=2, color="g")
    ax2.plot( W3_base.Time, FoodPC_Actual_2, "-", lw=2, color="g", label="Продовольствие [кг]")
    ax2.plot( W3_base.Time, ServicesPC_Actual_1, "--", lw=2, color="m")
    ax2.plot( W3_base.Time, ServicesPC_Actual_2, "-", lw=2, color="m", label="Услуги [усл.$]")
    ax2.set_xlim( limits)
    ax2.set_ylim( 0, 600)
    ax2.grid(True)
    ax2.legend(loc=0)
    ax2.set_ylabel("на душу в год")

    ax3.plot( W3_base.Time, LEB_Actual_1, "--", lw=2, color="r")
    ax3.plot( W3_base.Time, LEB_Actual_2, "-", lw=2, color="r", label="LEB")
    ax3.plot( W3_base.Time, TFR_Actual_1*10, "--", lw=2, color="g")
    ax3.plot( W3_base.Time, TFR_Actual_2*10, "-", lw=2, color="g", label="TFR x 10")
    ax3.set_xlim( limits)
    ax3.set_ylim( 0, 85)
    ax3.set_ylabel("Демография")
    ax3.grid(True)
    ax3.legend(loc=0)

    ax4.plot( W3_base.Time, POP_Actual_1/1000, "--", lw=2, color="b", label="Базовая модель")
    ax4.plot( W3_base.Time, POP_Actual_2/1000, "-", lw=2, color="b", label="+ возмущение")
    ax4.plot( W3_base.Time, Labor_Actual_1/1000, "--", lw=2, color="r")
    ax4.plot( W3_base.Time, Labor_Actual_2/1000, "-", lw=2, color="r", label="В т.ч. трудоспособных")
    ax4.errorbar(P0.Calibration_Year, P0.Calibration_Total/1000, yerr=P0.Calibration_Yerr/1000,
                 fmt=".", color="k", label="Реальная")
    ax4.set_xlim( limits)
    ax4.set_ylim( 0, 12)
    ax4.grid(True)
    ax4.legend(loc=0)
    ax4.set_xlabel("Год")
    ax4.set_ylabel("Популяция, млрд")
    plt.savefig( filename)
    return

P0 = Population()
W3_mod = Interpolation_BAU_2002()
W3_mod.Solve( np.linspace(1890, 2100, 211))
P0.Solve(W3_mod.Time)
Unity = np.ones(len(W3_mod.Time))
Random_Noise = 0.8*Unity + 0.4*np.random.random(len(W3_mod.Time))
Crisis_2020 = Hubbert( 2020, 1, 1, -0.5, 1).GetVector(W3_mod.Time)
Collapse_2020 = Sigmoid( 2020, 1, 1, 0).GetVector(W3_mod.Time)
Partial5_2020 = Sigmoid( 2020, 1, 1, 0.5).GetVector(W3_mod.Time)
Partial1_2020 = Sigmoid( 2020, 1, 1, 0.1).GetVector(W3_mod.Time)
Doubling_2020 = Sigmoid( 2020, 1, 1, 2.0).GetVector(W3_mod.Time)

print("*** Random Noise Goods ***")
Check_Stability( P0, W3_mod, "./Graphs/figure_20_24.png",
                 "Случайное возмущение входной переменной Goods",
                 Random_Noise, Unity, Unity)

print("*** Random Noise Foods ***")
Check_Stability( P0, W3_mod, "./Graphs/figure_20_25.png",
                 "Случайное возмущение входной переменной Food",
                 Unity, Random_Noise, Unity)

print("*** Random Noise Services ***")
Check_Stability( P0, W3_mod, "./Graphs/figure_20_26.png",
                 "Случайное возмущение входной переменной Services",
                 Unity, Unity, Random_Noise)

print("*** Goods Crisis ***")
Check_Stability( P0, W3_mod, "./Graphs/figure_20_27.png",
                 "Кризис потребительских товаров",
                 Crisis_2020, Unity, Unity)

print("*** Food Crisis ***")
Check_Stability( P0, W3_mod, "./Graphs/figure_20_28.png",
                 "Продовольственный кризис",
                 Unity, Crisis_2020, Unity)

print("*** Social Crisis ***")
Check_Stability( P0, W3_mod, "./Graphs/figure_20_29.png",
                 "Социальный кризис",
                 Unity, Unity, Crisis_2020)

print("*** Goods Collapse ***")
Check_Stability( P0, W3_mod, "./Graphs/figure_20_30.png",
                 "Коллапс потребления",
                 Collapse_2020, Unity, Unity)

print("*** Food Collapse ***")
Check_Stability( P0, W3_mod, "./Graphs/figure_20_31.png",
                 "Продовольственный коллапс",
                 Unity, Collapse_2020, Unity)

print("*** Social Collapse ***")
Check_Stability( P0, W3_mod, "./Graphs/figure_20_32.png",
                 "Социальный коллапс",
                 Unity, Unity, Collapse_2020)

print("*** Cambodia Collapse ***")
Check_Stability( P0, W3_mod, "./Graphs/figure_20_33.png",
                 "Коллапс пол-потовской Кампучии",
                 Collapse_2020, Partial1_2020, Collapse_2020)

print("*** Goods doubling ***")
Check_Stability( P0, W3_mod, "./Graphs/figure_20_34.png",
                 "Удвоение промышленного потребления",
                 Doubling_2020, Unity, Unity)

print("*** Food doubling ***")
Check_Stability( P0, W3_mod, "./Graphs/figure_20_35.png",
                 "Удвоение продовольствия",
                 Unity, Doubling_2020, Unity)

print("*** Services doubling ***")
Check_Stability( P0, W3_mod, "./Graphs/figure_20_36.png",
                 "Удвоение услуг",
                 Unity, Unity, Doubling_2020)

if InteractiveModeOn: plt.show(True)
