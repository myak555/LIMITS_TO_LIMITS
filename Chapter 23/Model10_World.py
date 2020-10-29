from Population import *
import datetime as dti

strName = "мире" 
dataName = "./Data/World.csv"
nRight = 180
detection = 1.4/10.7

Day, WHO_Cases, WHO_Deaths, WHO_Cases_Rate, WHO_Death_Rate = Load_Calibration(dataName,
    ["day","cases","deaths","dCases","dDeaths"], separator='\t')
for limit,d in enumerate( WHO_Deaths):
    if d<0: break
Day = Day[0:limit]
WHO_Cases = WHO_Cases[0:limit]
WHO_Deaths = WHO_Deaths[0:limit]
WHO_Cases_Rate = WHO_Cases_Rate[0:limit]
WHO_Death_Rate = WHO_Death_Rate[0:limit]
    
time = np.linspace(0, 365, 366)

Exp_Model = np.exp(0.23*(time-82))

Detected_Model = Linear_Combo()
# China and world primary
Detected_Model.Wavelets += [Hubbert( x0=68, s0=0.26, s1=0.30, peak=3400)]
#Detected_Model.Wavelets += [Hubbert( x0=132, s0=0.13, s1=0.12, peak=70000)]
Detected_Model.Wavelets += [Hubbert( x0=138, s0=0.13, s1=0.12, peak=75000)]
# Minor
Detected_Model.Wavelets += [Hubbert( x0=110, s0=0.45, s1=0.90, peak=20000)]
Detected_Model.Wavelets += [Hubbert( x0=117, s0=0.90, s1=0.90, peak=30000)]
Detected_Model.Wavelets += [Hubbert( x0=121, s0=0.90, s1=0.90, peak=30000)]
Detected_Model.Wavelets += [Hubbert( x0=126, s0=0.90, s1=0.90, peak=35000)]
Detected_Model.Wavelets += [Hubbert( x0=132, s0=0.90, s1=1.10, peak=23000)]
Detected_Model.Wavelets += [Hubbert( x0=140, s0=1.50, s1=0.80, peak=10000)]
Detected_Model.Wavelets += [Hubbert( x0=148, s0=0.80, s1=0.90, peak=35000)]
Detected_Model.Wavelets += [Hubbert( x0=153, s0=0.90, s1=0.60, peak=35000)]
Detected_Model.Wavelets += [Hubbert( x0=160, s0=0.60, s1=0.60, peak=35000)]
Detected_Model.Wavelets += [Hubbert( x0=167, s0=0.60, s1=0.60, peak=30000)]
Detected_Model.Wavelets += [Hubbert( x0=174, s0=0.60, s1=0.60, peak=20000)]
Detected_Model.Wavelets += [Hubbert( x0=181, s0=0.60, s1=0.60, peak=10000)]
Detected_Model.Wavelets += [Hubbert( x0=187, s0=0.60, s1=0.60, peak=5000)]

Detected_Model_Rate = Detected_Model.GetVector(time)
Detected_Model_Cum = Cumulative( Detected_Model_Rate)

Death_Model_emp = Linear_Combo()
# China and world primary
Death_Model_emp.Wavelets += [Hubbert( x0=79, s0=0.120, s1=0.300, peak=110)]
Death_Model_emp.Wavelets += [Hubbert( x0=138, s0=0.130, s1=0.120, peak=5500)]
# Minor
Death_Model_emp.Wavelets += [Hubbert( x0=110, s0=0.75, s1=1.000, peak=700)]
Death_Model_emp.Wavelets += [Hubbert( x0=117, s0=1.00, s1=1.000, peak=800)]
Death_Model_emp.Wavelets += [Hubbert( x0=121, s0=1.00, s1=1.000, peak=1200)]
Death_Model_emp.Wavelets += [Hubbert( x0=126, s0=1.00, s1=1.000, peak=2500)]
Death_Model_emp.Wavelets += [Hubbert( x0=132, s0=1.00, s1=1.000, peak=2500)]
Death_Model_emp.Wavelets += [Hubbert( x0=139, s0=1.00, s1=1.000, peak=2200)]
Death_Model_emp.Wavelets += [Hubbert( x0=146, s0=1.00, s1=0.500, peak=2000)]
Death_Model_emp.Wavelets += [Hubbert( x0=153, s0=1.00, s1=0.500, peak=1800)]
Death_Model_emp.Wavelets += [Hubbert( x0=160, s0=1.00, s1=0.500, peak=1200)]
Death_Model_emp.Wavelets += [Hubbert( x0=167, s0=1.00, s1=0.500, peak=800)]
Death_Model_emp.Wavelets += [Hubbert( x0=174, s0=1.00, s1=0.500, peak=500)]
Death_Model_emp.Wavelets += [Hubbert( x0=181, s0=1.00, s1=0.100, peak=200)]
Death_Model_emp_Rate = Death_Model_emp.GetVector(time)
Death_Model_emp_Cum = Cumulative( Death_Model_emp_Rate)

Infected_Model = Linear_Combo()
Infected_Model.Wavelets += [Hubbert( x0=105, s0=0.255, s1=0.255, peak=150000)]

##Infected_Model.Wavelets += [Hubbert( x0=61, s0=0.255, s1=0.200, peak=5000)]
##Infected_Model.Wavelets += [Hubbert( x0=125, s0=0.120, s1=0.200, peak=80000)]
##Infected_Model.Wavelets += [Hubbert( x0=140, s0=0.200, s1=0.100, peak=60000)]
Infected_Model_Rate = Infected_Model.GetVector(time)
Infected_Model_Cum = Cumulative( Infected_Model_Rate)
#for d,r in enumerate(Infected_Model_Rate):
#    print("{:d}\t{:.1f}".format(d, r))

IDR = 0.004
survival_rate = 1-IDR
symptomatic = 0.5
Contageous_function = Bathtub( x0=5.0, s0=1.6, x1 = 14.0, s1=0.8, left=0.0, middle=0.95, right=0.0).GetVector(time)
Symptom_function = Bathtub( x0=7.0, s0=0.95, x1 = 28.0, s1=0.6, left=0.0, middle=symptomatic, right=0.0).GetVector(time)
Severe_function = Bathtub( x0=18.0, s0=1.0, x1 = 28.0, s1=0.6, left=0.0, middle=IDR, right=0.0).GetVector(time)
Death_function = Sigmoid( x0=30.0, s0=0.13, left=0, right=IDR).GetVector(time)
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

xlimits =(30,230)
norm1 = 1e-6
norm2 = 1e-3

fig = plt.figure( figsize=(15,15))
fig.suptitle( 'Пандемия COVID-19 в {:s}'.format(strName), fontsize=22)
gs = plt.GridSpec(3, 1, height_ratios=[1, 1, 1]) 
ax1 = plt.subplot(gs[0])
ax2 = plt.subplot(gs[1])
ax3 = plt.subplot(gs[2])

ax1.bar( Day, WHO_Cases*norm1, width=1, color='g', alpha=0.3, label="Случаи-ВОЗ")
#ax1.plot( time, Infected_Model_Cum*norm1, '--', color='g', lw=2, label="Инфицировано (мoдель)")
ax1.bar( Day, WHO_Deaths*norm1*10, width=1, color='k', alpha=0.3, label="Смерти-ВОЗ x 10")
#ax1.plot( time, Contageous_Model_Cum*norm, '-.', color='g', lw=3, label="Заразных (мoдель)")
#ax1.plot( time, Symptomatic_Model_Cum*norm, '-', color='m', lw=3, label="Больных (мoдель)")
#ax1.plot( time, Recovery_Model_Cum*norm, '-', color='y', lw=3, label="Выздоровевших (мoдель)")
ax1.plot( time, Detected_Model_Cum*norm1, '-', color='g', lw=2, label="Выявлено (мoдель)")
ax1.plot( time, Death_Model_emp_Cum*norm1*10, '-', color='k', lw=2, label="Смертей (мoдель) x 10")
#ax1.plot( time, Exp_Model*norm, '-.', color='g', lw=2, label="Экспонента бледнолисых")
#ax1.annotate('Около 32 тыс инфицировано',
#                xy=(175,Infected_Model_Cum[175]*norm),xytext=(100,50000*norm),
#                arrowprops=dict(arrowstyle='-|>', fc="k", ec="k", lw=1.5),
#                bbox=dict(pad=1, facecolor="none", edgecolor="none"))
#ax1.annotate('Не более 20 тыс имели симптомы',
#                xy=(175,Recovery_Model_Cum[175]*norm),xytext=(50,45000*norm),
#                arrowprops=dict(arrowstyle='-|>', fc="k", ec="k", lw=1.5),
#                bbox=dict(pad=1, facecolor="none", edgecolor="none"))
ax1.set_xlim( xlimits)
ax1.set_ylim( 0, 6)
ax1.set_ylabel("миллионов")
ax1.grid(True)
ax1.legend(loc=0)

##ax2.plot( [132], [30], 'o', lw=5, color='r', label="Пациентов в интенсивной терапии (21 на ИВЛ)")
ax2.bar( Day, WHO_Death_Rate*norm2, width=1, color='k', alpha=0.3, label="Смерти-ВОЗ")
##ax2.plot( time, Severe_Model_Cum, '-', color='r', lw=3, label="Тяжёлых и критических пациентов (мoдель)")
ax2.plot( time, Death_Model_emp_Rate*norm2, '-', color='k', lw=2, label="Смерти (модель)")
###ax2.annotate('Ожидаемый cIFR={:.1f}%'.format(Model_Deaths[-1]*100/Model_WHO_Cases[-1]),
###                xy=(175,Model_Deaths[-1]),xytext=(130,Model_Deaths[-1]*0.5),
###                arrowprops=dict(arrowstyle='-|>', fc="k", ec="k", lw=1.5),
###                bbox=dict(pad=1, facecolor="none", edgecolor="none"))
##ax2.annotate('Первая смерть 20 февраля',
##                xy=(72,1),xytext=(5,50),
##                arrowprops=dict(arrowstyle='-|>', fc="k", ec="k", lw=1.5),
##                bbox=dict(pad=1, facecolor="none", edgecolor="none"))
ax2.set_xlim( xlimits)
ax2.set_ylim( 0, 9)
ax2.set_ylabel("тысяч в сутки")
ax2.grid(True)
ax2.legend(loc=0)

ax3.bar( Day, WHO_Cases_Rate*norm2, width=1, color='g', alpha=0.3, label="Подтверждённые случаи (ВОЗ)")
#ax3.plot( Day, WHO_Cases_Rate*norm2, ".", lw=2, color='g', label="Подтверждённые случаи (ВОЗ)")
ax3.plot( time, Detected_Model_Rate*norm2, "-", lw=2, color='g', label="Подтверждённые случаи (модель)")
#ax3.plot( time, Infected_Model_Rate*norm2, "--", lw=3, color='g', label="Заразились (модель)")
##ax3.plot( [41,51], [10,10], "-", lw=5, color='k')
##ax3.plot( [109,109], [0,1000], "--", lw=3, color='k', label="Первые противоэпидемические мероприятия")
##
##ax3.annotate('Первый случай завезён с 15 по 25 января',
##                xy=(46,10),xytext=(10,300),
##                arrowprops=dict(arrowstyle='-|>', fc="k", ec="k", lw=1.5),
##                bbox=dict(pad=1, facecolor="none", edgecolor="none"))
##ax3.annotate('Первыe вспышки быстро локализованы',
##                xy=(59,20),xytext=(10,500),
##                arrowprops=dict(arrowstyle='-|>', fc="k", ec="k", lw=1.5),
##                bbox=dict(pad=1, facecolor="none", edgecolor="none"))
##ax3.annotate('Ruby Princess 8 марта (158 вероятных, 2 положительных)',
##                xy=(99,10),xytext=(5,-400),
##                arrowprops=dict(arrowstyle='-|>', fc="k", ec="k", lw=1.5),
##                bbox=dict(pad=1, facecolor="none", edgecolor="none"))
##ax3.annotate('Ruby Princess + 2 лайнера 18-19 марта (более 3000 вероятных, 620 положительных)',
##                xy=(110,10),xytext=(30,-500),
##                arrowprops=dict(arrowstyle='-|>', fc="k", ec="k", lw=1.5),
##                bbox=dict(pad=1, facecolor="none", edgecolor="none"))
##ax3.annotate('Выборы в Квинследе 28 марта',
##                xy=(119,10),xytext=(65,-600),
##                arrowprops=dict(arrowstyle='-|>', fc="k", ec="k", lw=1.5),
##                bbox=dict(pad=1, facecolor="none", edgecolor="none"))
ax3.annotate('Первый подтверждённый случай и первая смерть 30 декабря',
                xy=(30,0.1),xytext=(29,-35),
                arrowprops=dict(arrowstyle='-|>', fc="k", ec="k", lw=1.5),
                bbox=dict(pad=1, facecolor="none", edgecolor="none"))
ax3.set_xlim( xlimits)
ax3.set_ylim( 0, 100)
ax3.set_xlabel("День эпидемии (0 соответствует 30 ноября 2019 г)")
ax3.set_ylabel("тысяч в сутки")
ax3.grid(True)
ax3.legend(loc=0)

plt.savefig( "./Graphs/figure_10_World.png")

if False:
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
    ax2.set_ylim( 0, 0.01)
    ax2.set_xlabel("День после заражения")
    ax2.set_ylabel("Часть заразившихся")
    ax2.grid(True)
    ax2.legend(loc=0)
    plt.savefig( "./Graphs/Model_Parameters_07.png")

if InteractiveModeOn: plt.show(True)
