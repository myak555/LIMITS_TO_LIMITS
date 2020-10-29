from Population import *

strName = "Южной Корее" 
dataName = ".\Data\South_Korea.csv"
nRight = 180
detection = 1.4/10.7

ChurchIS=np.array([
    52,65,183,340,484,
    523,614,758,863,1582,
    2131,2431,2719,3020,3464,
    3935,4301,4484,4627,4719,
    4732,4758,4797,5020,5020,
    5020,5020,5020,5046,5046,
    5046,5059,5059,5072,5085,
    5085,5085,5085,5085,5163,
    5176,5176])
ChurchIS_rate=np.array([0,
    13,118,157,144,39,
    91,144,105,719,549,
    300,288,301,444,471,
    366,183,143,92,13,
    26,39,223,0,13,
    0,0,26,0,0,
    13,0,13,13,0,
    0,0,0,78,13,
    0])
dayChIS=np.linspace(80,121,42)

Day, WHO_Cases, WHO_Deaths = Load_Calibration(dataName, ["day","cases","deaths"], separator='\t')
for limit,d in enumerate( WHO_Deaths):
    if d<0: break
Day = Day[0:limit]
WHO_Cases = WHO_Cases[0:limit]
WHO_Deaths = WHO_Deaths[0:limit]
WHO_Cases_Rate=np.zeros(limit)
WHO_Death_Rate=np.zeros(limit)
for i in range(1,limit):
    WHO_Cases_Rate[i] = WHO_Cases[i] - WHO_Cases[i-1] 
    WHO_Death_Rate[i] = WHO_Deaths[i] - WHO_Deaths[i-1] 
dCdt = Rate(Filter(WHO_Cases, matrix=[1,1,2,1,1]))

#for d,r in enumerate(WHO_Cases_Rate):
#    print("{:d}\t{:.1f}".format(d, r))
    
time = np.linspace(0, 183, 184)

Exp_Model = np.exp(0.25*(time-60))
Exp_Model_Deaths = np.exp(0.14*(time-71))

Detected_Model = Linear_Combo()
Detected_Model.Wavelets += [Hubbert( x0=92.0, s0=0.430, s1=0.311, peak=618)]
Detected_Model.Wavelets += [Hubbert( x0=84.5, s0=0.990, s1=1.067, peak=61)]
Detected_Model.Wavelets += [Hubbert( x0=98.0, s0=1.000, s1=0.426, peak=161)]
Detected_Model.Wavelets += [Hubbert( x0=110.5, s0=0.573, s1=0.525, peak=120)]
Detected_Model.Wavelets += [Hubbert( x0=104.5, s0=1.000, s1=1.000, peak=27)]
Detected_Model.Wavelets += [Hubbert( x0=119.0, s0=0.618, s1=0.255, peak=106)]
Detected_Model.Wavelets += [Hubbert( x0=130.0, s0=0.618, s1=0.155, peak=30)]
Detected_Model_Rate = Detected_Model.GetVector(time)
Detected_Model_Cum = Cumulative( Detected_Model_Rate)

Infected_Model = Linear_Combo()
Infected_Model.Wavelets += [Hubbert( x0=62+17, s0=0.255, s1=0.150, peak=1200)]
Infected_Model.Wavelets += [Hubbert( x0=98.0, s0=0.255, s1=0.426, peak=300)]
Infected_Model.Wavelets += [Hubbert( x0=110.5, s0=0.573, s1=0.525, peak=80)]
Infected_Model.Wavelets += [Hubbert( x0=104.5, s0=1.000, s1=1.000, peak=27)]
Infected_Model.Wavelets += [Hubbert( x0=119.0, s0=0.618, s1=0.255, peak=106)]
Infected_Model.Wavelets += [Hubbert( x0=130.0, s0=0.618, s1=0.155, peak=30)]
Infected_Model_Rate = Infected_Model.GetVector(time)
Infected_Model_Cum = Cumulative( Infected_Model_Rate)
#for d,r in enumerate(Infected_Model_Rate):
#    print("{:d}\t{:.1f}".format(d, r))

IDR = 0.0082
survival_rate = 1-IDR
symptomatic = 0.5
Contageous_function = Bathtub( x0=5.0, s0=1.6, x1 = 14.0, s1=0.8, left=0.0, middle=0.95, right=0.0).GetVector(time)
Symptom_function = Bathtub( x0=7.0, s0=0.95, x1 = 28.0, s1=0.6, left=0.0, middle=symptomatic, right=0.0).GetVector(time)
Severe_function = Bathtub( x0=18.0, s0=1.0, x1 = 28.0, s1=0.6, left=0.0, middle=IDR*3, right=0.0).GetVector(time)
Death_function = Sigmoid( x0=30.0, s0=0.13, left=0, right=IDR).GetVector(time)
Immune_function = Sigmoid( x0=12.0, s0=0.5, left=0, right=survival_rate).GetVector(time)
Recovery_function = np.ones(len(time))*(symptomatic)
Recovery_function -= Death_function 
Recovery_function = np.clip( Recovery_function - Symptom_function, 0, symptomatic)  
a = np.argmax(Symptom_function)
Recovery_function[0:a] = 0.0

##IDR = 0.008
##survival_rate = 1-IDR
##symptomatic = 0.5
##Contageous_function = Bathtub( x0=5.0, s0=1.6, x1 = 14.0, s1=0.8, left=0.0, middle=0.95, right=0.0).GetVector(time)
##Symptom_function = Bathtub( x0=7.0, s0=0.95, x1 = 23.0, s1=0.6, left=0.0, middle=symptomatic, right=0.0).GetVector(time)
##Severe_function = Bathtub( x0=12.0, s0=1.0, x1 = 23.0, s1=0.6, left=0.0, middle=0.075, right=0.0).GetVector(time)
##Death_function = Sigmoid( x0=30.0, s0=0.13, left=0, right=IDR).GetVector(time)
##Immune_function = Sigmoid( x0=12.0, s0=0.5, left=0, right=survival_rate).GetVector(time)
##Recovery_function = np.ones(len(time))*(symptomatic)
##Recovery_function -= Death_function 
##Recovery_function = np.clip( Recovery_function - Symptom_function, 0, symptomatic)  
##a = np.argmax(Symptom_function)
##Recovery_function[0:a] = 0.0

Contageous_Model_Cum = np.convolve( Infected_Model_Rate, Contageous_function)[:len(time)]
Symptomatic_Model_Cum = np.convolve( Infected_Model_Rate, Symptom_function)[:len(time)]
Severe_Model_Cum = np.convolve( Infected_Model_Rate, Severe_function)[:len(time)]
Recovery_Model_Cum = np.convolve( Infected_Model_Rate, Recovery_function)[:len(time)]
Severe_Model_Cum = np.convolve( Infected_Model_Rate, Severe_function)[:len(time)]
Death_Model_Cum = np.convolve( Infected_Model_Rate, Death_function)[:len(time)]

xlimits =(0,184)
norm = 1e-3

fig = plt.figure( figsize=(15,15))
fig.suptitle( 'Вспышки COVID-19 в {:s}, эпидемия в Даэгу'.format(strName), fontsize=22)
gs = plt.GridSpec(3, 1, height_ratios=[1, 1, 1]) 
ax1 = plt.subplot(gs[0])
ax2 = plt.subplot(gs[1])
ax3 = plt.subplot(gs[2])

ax1.plot( Day, WHO_Cases*norm, 'o', lw=5, color='g', label="Случаи-ВОЗ")
ax1.plot( dayChIS, ChurchIS*norm, '.', lw=5, color='g', label="Случаи-секта И.-Ш.")
ax1.plot( time, Infected_Model_Cum*norm, '--', color='g', lw=3, label="Инфицировано (мoдель)")
ax1.plot( time, Contageous_Model_Cum*norm, '-.', color='g', lw=3, label="Заразных (мoдель)")
ax1.plot( time, Symptomatic_Model_Cum*norm, '-', color='m', lw=3, label="Больных (мoдель)")
ax1.plot( time, Recovery_Model_Cum*norm, '-', color='y', lw=3, label="Выздоровевших (мoдель)")
ax1.plot( time, Detected_Model_Cum*norm, '-', color='g', lw=3, label="Выявлено (мoдель)")
#ax1.plot( time, Exp_Model*norm, '-.', color='g', lw=2, label="Экспонента бледнолисых")
ax1.annotate('Первый подтверждённый случай 20 января',
                xy=(51,10*norm),xytext=(5,3000*norm),
                arrowprops=dict(arrowstyle='-|>', fc="k", ec="k", lw=1.5),
                bbox=dict(pad=1, facecolor="none", edgecolor="none"))
ax1.annotate('Более 30 тыс инфицировано',
                xy=(120,Infected_Model_Cum[120]*norm),xytext=(50,36500*norm),
                arrowprops=dict(arrowstyle='-|>', fc="k", ec="k", lw=1.5),
                bbox=dict(pad=1, facecolor="none", edgecolor="none"))
ax1.annotate('Не более 15 тыс имели симптомы',
                xy=(120,Recovery_Model_Cum[120]*norm),xytext=(100,38000*norm),
                arrowprops=dict(arrowstyle='-|>', fc="k", ec="k", lw=1.5),
                bbox=dict(pad=1, facecolor="none", edgecolor="none"))
ax1.set_xlim( xlimits)
ax1.set_ylim( 0, 35000*norm)
ax1.set_ylabel("тысяч инфицированных")
ax1.grid(True)
ax1.legend(loc=0)

ax2.plot( Day, WHO_Deaths, 'o', lw=5, color='k', label="Смерти-ВОЗ")
ax2.plot( time, Severe_Model_Cum, '-', color='r', lw=3, label="Тяжёлых и критических пациентов (мoдель)")
ax2.plot( time, Death_Model_Cum, '-', color='k', lw=2, label="Смерти (модель)")
#ax2.annotate('Ожидаемый cIFR={:.1f}%'.format(Model_Deaths[-1]*100/Model_WHO_Cases[-1]),
#                xy=(175,Model_Deaths[-1]),xytext=(130,Model_Deaths[-1]*0.5),
#                arrowprops=dict(arrowstyle='-|>', fc="k", ec="k", lw=1.5),
#                bbox=dict(pad=1, facecolor="none", edgecolor="none"))
ax2.annotate('Первая смерть 20 февраля',
                xy=(72,10),xytext=(5,50),
                arrowprops=dict(arrowstyle='-|>', fc="k", ec="k", lw=1.5),
                bbox=dict(pad=1, facecolor="none", edgecolor="none"))
ax2.set_xlim( xlimits)
ax2.set_ylim( 0, 400)
ax2.set_ylabel("пациентов")
ax2.grid(True)
ax2.legend(loc=0)

ax3.plot( Day, WHO_Cases_Rate, "o", lw=2, color='g', label="Подтверждённые случаи (ВОЗ)")
ax3.plot( dayChIS, ChurchIS_rate, ".", lw=2, color='g', label="В т.ч. члены секты И.-Ш. (IDCRC)")
ax3.plot( Day+0.5, dCdt, "--", lw=2, color='k', label="Производная случаев ВОЗ")
ax3.plot( time, Detected_Model_Rate, "-", lw=2, color='g', label="Подтверждённые случаи (модель)")
ax3.plot( time, Infected_Model_Rate, "--", lw=3, color='g', label="Заразились (модель)")
ax3.plot( [41,51], [50,50], "-", lw=5, color='k')

ax3.annotate('Первый случай завезён с 10 по 20 января',
                xy=(46,50),xytext=(-10,-500),
                arrowprops=dict(arrowstyle='-|>', fc="k", ec="k", lw=1.5),
                bbox=dict(pad=1, facecolor="none", edgecolor="none"))
ax3.annotate('Вероятный периодический завоз с немедленной изоляцией',
                xy=(130,88),xytext=(60,-400),
                arrowprops=dict(arrowstyle='-|>', fc="k", ec="k", lw=1.5),
                bbox=dict(pad=1, facecolor="none", edgecolor="none"))
ax3.annotate('Собрания "Церкви Иисуса Шинчеонджи" 7-17 февраля',
                xy=(79,1200),xytext=(5,1400),
                arrowprops=dict(arrowstyle='-|>', fc="k", ec="k", lw=1.5),
                bbox=dict(pad=1, facecolor="none", edgecolor="none"))
ax3.annotate('Все новые случаи - привозные',xy=(112,110),xytext=(125,250),
                arrowprops=dict(arrowstyle='-|>', fc="k", ec="k", lw=1.5),
                bbox=dict(pad=1, facecolor="none", edgecolor="none"))
ax3.set_xlim( xlimits)
ax3.set_ylim( 0, 1500)
ax3.set_xlabel("День эпидемии (0 соответствует 30 ноября 2019 г)")
ax3.set_ylabel("в сутки")
ax3.grid(True)
ax3.legend(loc=0)

plt.savefig( "./Graphs/figure_01_SKorea.png")

if True:
    fig = plt.figure( figsize=(15,10))
    fig.suptitle( 'Параметры заразности, симптомов и летальности', fontsize=22)
    gs = plt.GridSpec(2, 1, height_ratios=[1,1])
    ax1 = plt.subplot(gs[0])
    ax2 = plt.subplot(gs[1])
    ax1.plot( time, Contageous_function, "-", lw=2, color='g',
              label="Заразность")
    ax1.plot( time, Symptom_function, "-", lw=2 , color='m',
              label="Симптомы")
    ax1.plot( time, Severe_function, "-", lw=2, color='r',
              label="В том числе, тяжёлых")
    ax1.plot( time, Recovery_function, "-", lw=2 , color='y',
              label="Выздоровление")
    ax1.set_xlim( 0, 75)
    ax1.set_ylim( 0, 1.0)
    ax1.set_ylabel("Часть заразившихся")
    ax1.grid(True)
    ax1.legend(loc=0)
    ax2.plot( time, Severe_function, "-", lw=3, color='r',
              label="Тяжёлых и критических пациентов")
    ax2.plot( time, Death_function, "-", lw=3 , color='k',
          label="Умерших")
    ax2.set_xlim( 0, 75)
    ax2.set_ylim( 0, 0.08)
    ax2.set_xlabel("День после заражения")
    ax2.set_ylabel("Часть заразившихся")
    ax2.grid(True)
    ax2.legend(loc=0)
    #plt.savefig( "./Graphs/figure_23_06a.png")

if InteractiveModeOn: plt.show(True)
