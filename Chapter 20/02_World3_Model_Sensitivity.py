from World3_Model import *

def Check_Sensitivity( P0, W3_base, mode1, model2, model3, filename, title, p1, p2, p3, limits = (1900, 2100)):
    l = len(W3_base.Time)
    POP_Actual_1 = np.zeros(l)
    TFR_Actual_1 = np.zeros(l)
    LEB_Actual_1 = np.zeros(l)
    GoodsPC_Actual_1 = np.zeros(l)
    FoodPC_Actual_1 = np.zeros(l)
    ServicesPC_Actual_1 = np.zeros(l)
    POP_Actual_2 = np.zeros(l)
    TFR_Actual_2 = np.zeros(l)
    LEB_Actual_2 = np.zeros(l)
    GoodsPC_Actual_2 = np.zeros(l)
    FoodPC_Actual_2 = np.zeros(l)
    ServicesPC_Actual_2 = np.zeros(l)
    POP_Actual_3 = np.zeros(l)
    TFR_Actual_3 = np.zeros(l)
    LEB_Actual_3 = np.zeros(l)
    GoodsPC_Actual_3 = np.zeros(l)
    FoodPC_Actual_3 = np.zeros(l)
    ServicesPC_Actual_3 = np.zeros(l)
    conversion = 0.94
    for i,y in enumerate(W3_base.Time):
        POP_Actual_1[i] = model1.Demographics.Total
        TFR_Actual_1[i] = model1.TFR
        LEB_Actual_1[i] = model1.LEB
        GoodsPC_Actual_1[i] = model1.GoodsPC
        FoodPC_Actual_1[i] = model1.FoodPC
        ServicesPC_Actual_1[i] = model1.ServicesPC
        POP_Actual_2[i] = model2.Demographics.Total
        TFR_Actual_2[i] = model2.TFR
        LEB_Actual_2[i] = model2.LEB
        GoodsPC_Actual_2[i] = model2.GoodsPC
        FoodPC_Actual_2[i] = model2.FoodPC
        ServicesPC_Actual_2[i] = model2.ServicesPC
        POP_Actual_3[i] = model3.Demographics.Total
        TFR_Actual_3[i] = model3.TFR
        LEB_Actual_3[i] = model3.LEB
        GoodsPC_Actual_3[i] = model3.GoodsPC
        FoodPC_Actual_3[i] = model3.FoodPC
        ServicesPC_Actual_3[i] = model3.ServicesPC
        model1.Compute_Next_Year(goods=W3_base.Goods[i]*conversion,
                                 food=W3_base.Food[i]*conversion,
                                 services=W3_base.Services[i]*conversion)
        model2.Compute_Next_Year(goods=W3_base.Goods[i]*conversion,
                                 food=W3_base.Food[i]*conversion,
                                 services=W3_base.Services[i]*conversion)
        model3.Compute_Next_Year(goods=W3_base.Goods[i]*conversion,
                                 food=W3_base.Food[i]*conversion,
                                 services=W3_base.Services[i]*conversion)

    fig = plt.figure( figsize=(15,10))
    fig.suptitle( title, fontsize=25)
    gs = plt.GridSpec(2, 1) 
    ax2 = plt.subplot(gs[0])
    ax3 = plt.subplot(gs[1])

    ax2.plot( W3_base.Time, LEB_Actual_1, "-.", lw=2, color="r", label="LEB")
    ax2.plot( W3_base.Time, LEB_Actual_2, "-", lw=2, color="r")
    ax2.plot( W3_base.Time, LEB_Actual_3, "--", lw=2, color="r")
    ax2.plot( W3_base.Time, TFR_Actual_1*10, "-.", lw=2, color="g", label="TFR x 10")
    ax2.plot( W3_base.Time, TFR_Actual_2*10, "-", lw=2, color="g")
    ax2.plot( W3_base.Time, TFR_Actual_3*10, "--", lw=2, color="g")
    ax2.set_xlim( limits)
    ax2.set_ylim( 0, 85)
    ax2.set_ylabel("Демография")
    ax2.grid(True)
    ax2.legend(loc=0)

    ax3.plot( W3_base.Time, POP_Actual_1/1000, "-.", lw=2, color="b", label=p1)
    ax3.plot( W3_base.Time, POP_Actual_2/1000, "-", lw=2, color="b", label=p2)
    ax3.plot( W3_base.Time, POP_Actual_3/1000, "--", lw=2, color="b", label=p3)
    ax3.errorbar(P0.Calibration_Year, P0.Calibration_Total/1000, yerr=P0.Calibration_Yerr/1000,
                 fmt=".", color="k", label="Реальная")
    ax3.set_xlim( limits)
    ax3.set_ylim( 0, 12)
    ax3.grid(True)
    ax3.legend(loc=0)
    ax3.set_xlabel("Год")
    ax3.set_ylabel("Популяция, млрд")
    plt.savefig( filename)
    return

P0 = Population()
W3_mod = Interpolation_BAU_2002()
W3_mod.Solve( np.linspace(1890, 2100, 211))
P0.Solve(W3_mod.Time)

print("*** Sigma 1 Sensitivity Check ***")
model1 = W3_Population()
model2 = W3_Population()
model3 = W3_Population()
model1.LEB_Food_Model.S0 = 0.0045
model3.LEB_Food_Model.S0 = 0.0055
Check_Sensitivity( P0, W3_mod, model1, model2, model3, "./Graphs/figure_20_07.png",
                     "Чувствительность модели к параметру σ₁",
                     "σ₁=0.0045", "σ₁=0.0050", "σ₁=0.0055")

print("*** LEBmax Sensitivity Check ***")
model1 = W3_Population()
model2 = W3_Population()
model3 = W3_Population()
model1.LEB_Food_Model.Left = -40
model3.LEB_Food_Model.Left = -50
model1.LEB_Food_Model.Right = 40
model3.LEB_Food_Model.Right = 50
Check_Sensitivity( P0, W3_mod, model1, model2, model3, "./Graphs/figure_20_08.png",
                     "Чувствительность модели к параметру LEBmax",
                     "LEBmax=80 лет", "LEBmax=90 лет", "LEBmax=100 лет")

print("*** Sigma 2 Sensitivity Check ***")
model1 = W3_Population()
model2 = W3_Population()
model3 = W3_Population()
model1.LEB_Services_Model.S0 = 0.010
model3.LEB_Services_Model.S0 = 0.014
Check_Sensitivity( P0, W3_mod, model1, model2, model3, "./Graphs/figure_20_09.png",
                     "Чувствительность модели к параметру σ₂",
                     "σ₂=0.010", "σ₂=0.012", "σ₂=0.014")

print("*** X 2 Sensitivity Check ***")
model1 = W3_Population()
model2 = W3_Population()
model3 = W3_Population()
model1.LEB_Services_Model.X0 = 180
model3.LEB_Services_Model.X0 = 220
Check_Sensitivity( P0, W3_mod, model1, model2, model3, "./Graphs/figure_20_10.png",
                     "Чувствительность модели к параметру x₂",
                     "x₂=180", "x₂=200", "x₂=220")

print("*** Tau 2 Sensitivity Check ***")
model1 = W3_Population()
model2 = W3_Population()
model3 = W3_Population()
model1.LEB_Services_Delay = Delay( delay=15, default_value = model1.ServicesPC)
model3.LEB_Services_Delay = Delay( delay=35, default_value = model3.ServicesPC)
Check_Sensitivity( P0, W3_mod, model1, model2, model3, "./Graphs/figure_20_11.png",
                     "Чувствительность модели к параметру τ₂",
                     "τ₂=15 лет", "τ₂=25 лет", "τ₂=35 лет")

print("*** Sigma 3 Sensitivity Check ***")
model1 = W3_Population()
model2 = W3_Population()
model3 = W3_Population()
model1.TFR_LEB_Model.S0 = 0.10
model3.TFR_LEB_Model.S0 = 0.40
Check_Sensitivity( P0, W3_mod, model1, model2, model3, "./Graphs/figure_20_12.png",
                     "Чувствительность модели к параметру σ₃",
                     "σ₃=0.10", "σ₃=0.25", "σ₃=0.40")

print("*** X 3 Sensitivity Check ***")
model1 = W3_Population()
model2 = W3_Population()
model3 = W3_Population()
model1.TFR_LEB_Model.X0 = 45
model3.TFR_LEB_Model.X0 = 65
Check_Sensitivity( P0, W3_mod, model1, model2, model3, "./Graphs/figure_20_13.png",
                     "Чувствительность модели к параметру x₃",
                     "x₃=45", "x₃=55", "x₃=65")

print("*** Tau 3 Sensitivity Check ***")
model1 = W3_Population()
model2 = W3_Population()
model3 = W3_Population()
model1.TFR_LEB_Delay = Delay( delay=25, default_value = 30)
model3.TFR_LEB_Delay = Delay( delay=75, default_value = 30)
Check_Sensitivity( P0, W3_mod, model1, model2, model3, "./Graphs/figure_20_14.png",
                     "Чувствительность модели к параметру τ₃",
                     "τ₃=25 лет", "τ₃=50 лет", "τ₃=75 лет")

print("*** DFRmin Sensitivity Check ***")
model1 = W3_Population()
model2 = W3_Population()
model3 = W3_Population()
model1.TFR_LEB_Model.Right = 1.0
model3.TFR_LEB_Model.Right = 2.0
Check_Sensitivity( P0, W3_mod, model1, model2, model3, "./Graphs/figure_20_15.png",
                     "Чувствительность модели к параметру DFRmin",
                     "DFRmin=1.0", "DFRmin=1.45", "DFRmin=2.0")

print("*** DFRmax Sensitivity Check ***")
model1 = W3_Population()
model2 = W3_Population()
model3 = W3_Population()
model1.TFR_LEB_Model.Left = 4.2/1.68
model3.TFR_LEB_Model.Left = 5.2/1.68
Check_Sensitivity( P0, W3_mod, model1, model2, model3, "./Graphs/figure_20_16.png",
                     "Чувствительность модели к параметру DFRmax",
                     "DFRmax=4.2", "DFRmax=4.7", "DFRmax=5.2")

print("*** Sigma 4 Sensitivity Check ***")
model1 = W3_Population()
model2 = W3_Population()
model3 = W3_Population()
model1.TFR_Goods_Model.S0 = 0.03
model3.TFR_Goods_Model.S0 = 0.07
Check_Sensitivity( P0, W3_mod, model1, model2, model3, "./Graphs/figure_20_17.png",
                     "Чувствительность модели к параметру σ₄",
                     "σ₄=0.03", "σ₄=0.05", "σ₄=0.07")

print("*** X4 Sensitivity Check ***")
model1 = W3_Population()
model2 = W3_Population()
model3 = W3_Population()
model1.TFR_Goods_Model.X0 = 100
model3.TFR_Goods_Model.X0 = 140
Check_Sensitivity( P0, W3_mod, model1, model2, model3, "./Graphs/figure_20_18.png",
                     "Чувствительность модели к параметру x₄",
                     "x₄=100", "x₄=120", "x₄=140")

print("*** Tau 4 Sensitivity Check ***")
model1 = W3_Population()
model2 = W3_Population()
model3 = W3_Population()
model1.TFR_Social_Delay = Delay( delay=25, default_value = 20)
model3.TFR_Social_Delay = Delay( delay=75, default_value = 20)
Check_Sensitivity( P0, W3_mod, model1, model2, model3, "./Graphs/figure_20_19.png",
                     "Чувствительность модели к параметру τ₄",
                     "τ₄=20 лет", "τ₄=40 лет", "τ₄=60 лет")

print("*** Sigma 5 Sensitivity Check ***")
model1 = W3_Population()
model2 = W3_Population()
model3 = W3_Population()
model1.Family_Planning_Model.S0 = 0.03
model3.Family_Planning_Model.S0 = 0.07
Check_Sensitivity( P0, W3_mod, model1, model2, model3, "./Graphs/figure_20_20.png",
                     "Чувствительность модели к параметру σ₅",
                     "σ₅=0.01", "σ₅=0.03", "σ₅=0.05")

print("*** X 5 Sensitivity Check ***")
model1 = W3_Population()
model2 = W3_Population()
model3 = W3_Population()
model1.Family_Planning_Model.X0 = 100
model3.Family_Planning_Model.X0 = 160
Check_Sensitivity( P0, W3_mod, model1, model2, model3, "./Graphs/figure_20_21.png",
                     "Чувствительность модели к параметру x₅",
                     "x₅=100", "x₅=130", "x₅=160")

print("*** TFRmax Sensitivity Check ***")
model1 = W3_Population()
model2 = W3_Population()
model3 = W3_Population()
model1.Family_Planning_Model.Left = 5
model3.Family_Planning_Model.Left = 8
Check_Sensitivity( P0, W3_mod, model1, model2, model3, "./Graphs/figure_20_22.png",
                     "Чувствительность модели к параметру TFRmax",
                     "TFRmax=5", "TFRmax=6", "TFRmax=8")

print("*** X3 - DFRmax Sensitivity Check ***")
model1 = W3_Population()
model2 = W3_Population()
model3 = W3_Population()
model1.TFR_LEB_Model.X0 = 45
model1.TFR_LEB_Model.Left = 5.5/1.68
model3.TFR_LEB_Model.X0 = 65
model3.TFR_LEB_Model.Left = 4.3/1.68
Check_Sensitivity( P0, W3_mod, model1, model2, model3, "./Graphs/figure_20_23.png",
                     "Чувствительность модели к параметрам x₃ и DFRmax",
                     "x₃=45, DFRmax=5.5", "x₃=55, DFRmax=4.7", "x₃=65, DFRmax=4.3")

if InteractiveModeOn: plt.show(True)
