from Population import *

strName = "Новой Зеландии" 
dataName = "./Data/New_Zealand.csv"
nRight = 180
detection = 1.4/10.7

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
Detected_Model.Wavelets += [Hubbert( x0=110.0, s0=1.000, s1=1.000, peak=7)]
Detected_Model.Wavelets += [Hubbert( x0=119.5, s0=0.430, s1=0.300, peak=77)]
Detected_Model.Wavelets += [Hubbert( x0=125.0, s0=1.000, s1=0.200, peak=18)]
Detected_Model_Rate = Detected_Model.GetVector(time)
Detected_Model_Cum = Cumulative( Detected_Model_Rate)

Infected_Model = Linear_Combo()
Infected_Model.Wavelets += [Hubbert( x0=105.0, s0=0.255, s1=0.155, peak=120)]
Infected_Model.Wavelets += [Hubbert( x0=115.0, s0=0.255, s1=0.155, peak=80)]
Infected_Model_Rate = Infected_Model.GetVector(time)
Infected_Model_Cum = Cumulative( Infected_Model_Rate)
#for d,r in enumerate(Infected_Model_Rate):
#    print("{:d}\t{:.1f}".format(d, r))

#Bluff_Wedding = Linear_Combo()
#Bluff_Wedding.Wavelets += [Sigmoid( x0=121.5, s0=0.500, s1=0.500, left=0, right=87)]
#Bluff_Wedding_Cum = Bluff_Wedding.GetVector(time)

IDR = 0.005
survival_rate = 1-IDR
symptomatic = 0.5
Contageous_function = Bathtub( x0=5.0, s0=1.6, x1 = 14.0, s1=0.8, left=0.0, middle=0.95, right=0.0).GetVector(time)
Symptom_function = Bathtub( x0=7.0, s0=0.95, x1 = 28.0, s1=0.6, left=0.0, middle=symptomatic, right=0.0).GetVector(time)
Severe_function = Bathtub( x0=18.0, s0=1.0, x1 = 28.0, s1=0.6, left=0.0, middle=IDR*3, right=0.0).GetVector(time)
#Death_function = Sigmoid( x0=30.0, s0=0.13, left=0, right=IDR).GetVector(time)
Death_function = Sigmoid( x0=28.0, s0=2.0, left=0, right=IDR).GetVector(time)
Immune_function = Sigmoid( x0=12.0, s0=0.5, left=0, right=survival_rate).GetVector(time)
Recovery_function = np.ones(len(time))*(symptomatic)
Recovery_function -= Death_function 
Recovery_function = np.clip( Recovery_function - Symptom_function, 0, symptomatic)  
a = np.argmax(Symptom_function)
Recovery_function[0:a] = 0.0

Contageous_Model_Cum = np.convolve( Infected_Model_Rate, Contageous_function)[:len(time)]
Symptomatic_Model_Cum = np.convolve( Infected_Model_Rate, Symptom_function)[:len(time)]
Severe_Model_Cum = np.convolve( Infected_Model_Rate, Severe_function)[:len(time)]
Recovery_Model_Cum = np.convolve( Infected_Model_Rate, Recovery_function)[:len(time)]
Severe_Model_Cum = np.convolve( Infected_Model_Rate, Severe_function)[:len(time)]
Death_Model_Cum = np.convolve( Infected_Model_Rate, Death_function)[:len(time)]

xlimits =(0,184)
norm = 1e-3

fig = plt.figure( figsize=(15,15))
fig.suptitle( 'Вспышки COVID-19 в {:s}'.format(strName), fontsize=22)
gs = plt.GridSpec(3, 1, height_ratios=[1, 1, 1]) 
ax1 = plt.subplot(gs[0])
ax2 = plt.subplot(gs[1])
ax3 = plt.subplot(gs[2])

ax1.plot( Day, WHO_Cases*norm, 'o', lw=5, color='g', label="Случаи-ВОЗ")
ax1.plot( time, Infected_Model_Cum*norm, '--', color='g', lw=3, label="Инфицировано (мoдель)")
ax1.plot( time, Contageous_Model_Cum*norm, '-.', color='g', lw=3, label="Заразных (мoдель)")
ax1.plot( time, Symptomatic_Model_Cum*norm, '-', color='m', lw=3, label="Больных (мoдель)")
ax1.plot( time, Recovery_Model_Cum*norm, '-', color='y', lw=3, label="Выздоровевших (мoдель)")
ax1.plot( time, Detected_Model_Cum*norm, '-', color='g', lw=3, label="Выявлено (мoдель)")
#ax1.plot( time, Bluff_Wedding_Cum*norm, '.', color='g', lw=3, label="Венчание в Bluff")

#ax1.plot( time, Exp_Model*norm, '-.', color='g', lw=2, label="Экспонента бледнолисых")
ax1.annotate('Первый подтверждённый случай 28 февраля',
                xy=(90,10*norm),xytext=(5,500*norm),
                arrowprops=dict(arrowstyle='-|>', fc="k", ec="k", lw=1.5),
                bbox=dict(pad=1, facecolor="none", edgecolor="none"))
ax1.annotate('Более 4 тыс инфицировано',
                xy=(175,Infected_Model_Cum[175]*norm),xytext=(125,6000*norm),
                arrowprops=dict(arrowstyle='-|>', fc="k", ec="k", lw=1.5),
                bbox=dict(pad=1, facecolor="none", edgecolor="none"))
ax1.annotate('Около 2 тыс имели симптомы',
                xy=(175,Recovery_Model_Cum[175]*norm),xytext=(75,5500*norm),
                arrowprops=dict(arrowstyle='-|>', fc="k", ec="k", lw=1.5),
                bbox=dict(pad=1, facecolor="none", edgecolor="none"))
ax1.set_xlim( xlimits)
ax1.set_ylim( 0, 5000*norm)
ax1.set_ylabel("тысяч инфицированных")
ax1.grid(True)
ax1.legend(loc=0)

ax2.plot( [121, 126, 128, 129, 131, 134, 140, 141, 143,145],
          [12,13,15,13,14,15,20,18,14,8],
          'o', lw=5, color='r', label="Тяжёлые (макс. 5 на ИВЛ)")
ax2.plot( Day, WHO_Deaths, 'o', lw=5, color='k', label="Смерти-ВОЗ")
ax2.plot( time, Severe_Model_Cum, '-', color='r', lw=3, label="Тяжёлых и критических пациентов (мoдель)")
ax2.plot( time, Death_Model_Cum, '-', color='k', lw=2, label="Смерти (модель)")
#ax2.annotate('Ожидаемый cIFR={:.1f}%'.format(Model_Deaths[-1]*100/Model_WHO_Cases[-1]),
#                xy=(175,Model_Deaths[-1]),xytext=(130,Model_Deaths[-1]*0.5),
#                arrowprops=dict(arrowstyle='-|>', fc="k", ec="k", lw=1.5),
#                bbox=dict(pad=1, facecolor="none", edgecolor="none"))
ax2.annotate('Первая смерть 29 марта',
                xy=(120,1),xytext=(5,5),
                arrowprops=dict(arrowstyle='-|>', fc="k", ec="k", lw=1.5),
                bbox=dict(pad=1, facecolor="none", edgecolor="none"))
ax2.set_xlim( xlimits)
ax2.set_ylim( 0, 25)
ax2.set_ylabel("пациентов")
ax2.grid(True)
ax2.legend(loc=0)

ax3.plot( Day, WHO_Cases_Rate, "o", lw=2, color='g', label="Подтверждённые случаи (ВОЗ)")
ax3.plot( Day+0.5, dCdt, "--", lw=2, color='k', label="Производная случаев ВОЗ")
ax3.plot( time, Detected_Model_Rate, "-", lw=2, color='g', label="Подтверждённые случаи (модель)")
ax3.plot( time, Infected_Model_Rate, "--", lw=3, color='g', label="Заразились (модель)")
ax3.plot( [70,90], [2,2], "-", lw=5, color='k')

ax3.annotate('Первый случай завезён с 8 по 28 февраля',
                xy=(80,2),xytext=(-10,-50),
                arrowprops=dict(arrowstyle='-|>', fc="k", ec="k", lw=1.5),
                bbox=dict(pad=1, facecolor="none", edgecolor="none"))
ax3.set_xlim( xlimits)
ax3.set_ylim( 0, 200)
ax3.set_xlabel("День эпидемии (0 соответствует 30 ноября 2019 г)")
ax3.set_ylabel("в сутки")
ax3.grid(True)
ax3.legend(loc=0)

plt.savefig( "./Graphs/figure_07_New_Zealand.png")

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
    ax2.set_ylim( 0, 0.02)
    ax2.set_xlabel("День после заражения")
    ax2.set_ylabel("Часть заразившихся")
    ax2.grid(True)
    ax2.legend(loc=0)
    plt.savefig( "./Graphs/figure_23_07.png")

if InteractiveModeOn: plt.show(True)
