from COVID_19_Parcing import *

def Population_USA( YearM):
    popYear = np.linspace( 1979, 2021, 43)
    popUSA = np.array([
        227.600, 229.763, 231.939, 234.133, 236.344,
        238.574, 240.824, 243.099, 245.403, 247.740,
        250.113, 252.530, 254.975, 257.454, 260.020,
        262.742, 265.659, 268.803, 272.137, 275.543,
        278.862, 281.983, 284.852, 287.507, 290.028,
        292.539, 295.130, 297.827, 300.595, 303.374,
        306.076, 308.641, 311.051, 313.335, 315.537,
        317.719, 319.929, 322.180, 324.459, 326.767,
        329.093, 331.432, 333.783])
    return np.interp(YearM, popYear, popUSA)


def Population_Structure_USA():
    popLabel = ["До 1 года", "1-4 года", "5-14 лет","15-24 года", 
        "25-34 года", "35-44 года", "45-54 года", "55-64 года",
        "65-74 года", "75-84 года", "85 лет и старше"]
    popLabelEng = ["Under 1 year", "1-4 years", "5-14 years","15-24 years", 
        "25-34 years", "35-44 years", "45-54 years", "55-64 years",
        "65-74 years", "75-84 years", "85 years and over"]
    popColors = ["#00FF00", "#00D700", "#009B00","#007300", 
        "#00FFFF", "#00D7D7", "#00AFAF", "#007373",
        "#FFFF00", "#C3C300", "#737300"]
    popStructureTotal = np.array([
        3.784, 15.586, 40.973, 42.595, 46.066, 42.146, 40.402, 42.459, 32.616, 16.512, 6.739])
    popStructureMale = np.array([
        1.935, 7.968, 20.933, 21.750, 23.442, 21.052, 19.943, 20.520, 15.224, 7.254, 2.446])
    popStructureFemale = np.array([
        1.848, 7.618, 20.040, 20.844, 22.624, 21.094, 20.459, 21.940, 17.392, 9.258, 4.293])
    popStructureFemale = np.array([
        3.784, 15.586, 40.973, 42.595, 46.066, 42.146, 40.402, 42.459, 32.616, 16.512, 6.739])
    return popLabel, popLabelEng, popColors, popStructureTotal #, popStructureMale, popStructureFemale


def Load_Operative_Data( age):
    f = open( "./Data/Provisional_COVID-19_Death_Counts_by_Sex__Age__and_Week.csv")
    f.readline()
    Weeks = []
    Dates = []
    Age0_tot = []
    Age0_cov = []
    while True:
        s = f.readline()
        if len(s) <= 0: break
        s = s.strip()
        ss = s.split(',')
        if ss[4] != "All Sex": continue
        if ss[5] == age:
            Weeks += [float(ss[2])]
            Dates += [ss[3]]
            Age0_tot += [float(ss[6])]
            Age0_cov += [float(ss[7])]
    f.close()
    return np.array( Weeks), np.array( Age0_tot), np.array( Age0_cov)


def Absolute_Deaths( USA_Covid_19, USA_2020, Deaths2020):
    Year, Deaths = Load_Calibration( "./Data/US_Deaths_1997_2019.csv", ["Year","Deaths"], separator="\t")
    YearM, DeathsM = Load_Calibration( "./Data/US_Deaths_1993_2019_monthly.csv", ["Year","Eq_months"], separator="\t")
    YearW, WeekW, DeathsW = Load_Calibration( "./Data/US_Deaths_2017_2020_weekly_CDC.csv", ["Year", "Week", "Deaths_me"], separator="\t")
    YearW += WeekW/52
    DeathsW = FilterN(DeathsW, N=5)
    YearWI = np.linspace(2018.042, 2020.458, 30)
    DeathsWI = np.interp(YearWI, YearW, DeathsW)
    Labels = []
    for y in Year: Labels += ["{:.0f}".format(y)]
    Labels += ["2020"]
    Labels += ["2021"]
    fig = plt.figure( figsize=(15,10))
    fig.suptitle( 'Абсолютная смертность в США 1997-2019', fontsize=22)
    gs = plt.GridSpec(1, 1, height_ratios=[1]) 
    ax1 = plt.subplot(gs[0])
    ax1.bar(Year[:-1]+0.5, Deaths[:-1]/12000, width=1, color="b",
            alpha=0.5, label="Абсолютная смертность (отчёты демографического комитета США, 1998-2019)")
    ax1.bar([Year[-1]+0.5], [Deaths[-1]/12000],
            width=1, color="b", alpha=0.1, label="Абсолютная смертность в 2019 г. (оценка ООН, 2020)")
    ax1.bar([Year[-1]+1.5], [Deaths2020/12000],
            width=1, color="k", alpha=0.1, label="Абсолютная смертность в 2020 г. (предварительная оценка ООН)")
    ax1.plot(YearM, DeathsM, ".", color="b", alpha=0.5, label="Месячные данные за 1993-2018 и 3 месяца 2019 в публичном доступе")
    ax1.plot(YearM, DeathsM, "-", lw=1, color="b", alpha=0.5)
    ax1.plot(YearWI, DeathsWI/1000, ".", color="m", alpha=0.5, label="Оперативные данные CDC за 2017-2019 и 6 месяцев 2020 в публичном доступе")
    ax1.plot(YearWI, DeathsWI/1000, "-", color="m", alpha=0.5)
    for i, d in enumerate(Deaths):
        ax1.text( Year[i]+0.07, 155, "{:.3f}".format(d/1e6), fontsize=9)
    ax1.text( 2020.07, 155, "{:.3f}".format(Deaths2020/1e6), fontsize=9)
    ax1.bar(USA_2020+1/24, USA_Covid_19/1000, width=1/12, color="m", alpha=1, label="Смертей от COVID-19 с февраля по июль 2020 г (месячные суммы)")        
    ax1.set_xlabel('Год')        
    ax1.set_ylabel('Тысяч умерших в месяц')
    ax1.annotate("Миллионов умерших в год",
            xy=( Year[2]+0.5, 151), xycoords='data',
            xytext = (Year[10]+0.5, 141), textcoords='data',
            arrowprops=dict(facecolor='black', shrink=0.1, width=2),
            horizontalalignment='right', verticalalignment='top', fontsize=12)
    ax1.annotate("Официально-зарегистирированные смерти от COVID-19 (ВОЗ)",
            xy=( 2020.1, USA_Covid_19[3]/1000), xycoords='data',
            xytext = (Year[19]+0.5, 100), textcoords='data',
            arrowprops=dict(facecolor='black', shrink=0.01, width=2),
            horizontalalignment='right', verticalalignment='top', fontsize=18)
    ax1.annotate("Эпидемия гриппа в декабре 2018 - феврале 2019 г",
            xy=( 2018, 281), xycoords='data',
            xytext = (2007, 280), textcoords='data',
            arrowprops=dict(facecolor='black', shrink=0.01, width=2),
            horizontalalignment='left', verticalalignment='top', fontsize=12)
    ax1.annotate("Пик смертности во второй половине апреля 2020 г",
            xy=( 2020.2, 322), xycoords='data',
            xytext = (2007, 300), textcoords='data',
            arrowprops=dict(facecolor='black', shrink=0.01, width=2),
            horizontalalignment='left', verticalalignment='top', fontsize=12)
    ax1.grid(True)
    ax1.set_xlim(1997, 2022)
    ax1.set_xticks(np.linspace(1997,2021,25))
    ax1.set_xticklabels( Labels, fontsize=9)
    ax1.set_ylim(0, 350)
    ax1.legend(loc=3, fontsize=12 )
    plt.savefig( "./Graphs/201_Absolute_Deaths.png")
    return

def Mortality( USA_Covid_19, USA_2020, Deaths2020):
    YearM, DeathsM = Load_Calibration( "./Data/US_Deaths_1980_2020_monthly.csv", ["Year","Eq_months"], separator="\t")
    popUSA_interpolated = Population_USA( YearM)
    mortality = DeathsM * 1000 / popUSA_interpolated 
    fig = plt.figure( figsize=(15,15))
    fig.suptitle( 'Месячные коэффиценты смертности в США 1980-2019', fontsize=22)
    gs = plt.GridSpec(2, 1, height_ratios=[1,1]) 
    ax1 = plt.subplot(gs[0])
    ax2 = plt.subplot(gs[1])
    ax1.plot(YearM, DeathsM, ".", color="b", alpha=0.5, label="Месячные данные за 1980-2018 и 3 месяца 2019 и оперативные данные CDC 2019/20")
    ax1.plot(YearM, DeathsM, "-", lw=1, color="b", alpha=0.5)
    ax1.plot(YearM, popUSA_interpolated, "-", color="g", lw=2, alpha=0.5, label="Население США, ООН")
    ax1.set_ylabel('Умерших в месяц, тысяч / население, млн')
    ax1.grid(True)
    ax1.set_xlim(1980, 2022)
    ax1.set_ylim(100, 350)
    ax1.legend(loc=3, fontsize=12 )

    mortality_sm = FilterN( mortality, N=37)
    ax2.plot(YearM, mortality, "-", color="b", lw=2, alpha=0.3, label="Meсячная смертность")
    ax2.plot(YearM, mortality_sm, "--", color="k", lw=2, alpha=1, label="Смертность без сезонных вариаций")
    ax2.fill_between(YearM, mortality, y2=0, color="b", alpha=0.3)
    ax2.bar(USA_2020+1/24, USA_Covid_19/330, width=1/12, color="m", alpha=1, label="Смертей от COVID-19 с февраля по июль 2020 г (месячные суммы)")        
    ax2.set_xlim(1980, 2022)
    ax2.set_ylim(0, 1000)
    ax2.grid(True)
    ax2.legend(loc=0, fontsize=12 )
    ax2.set_ylabel('Умерших в месяц на 1 млн населения')
    ax2.set_xlabel('Год')        

    plt.savefig( "./Graphs/207_Absolute_Deaths.png")
    return

def Mortality_Overlay( USA_Covid_19, USA_2020, Deaths2020):
    YearM, DeathsMR, DeathsM = Load_Calibration( "./Data/US_Deaths_1980_2020_monthly.csv", ["Year","Deaths","Eq_months"], separator="\t")
    popUSA_interpolated = Population_USA( YearM)
    mortality = DeathsM * 1000 / popUSA_interpolated
    mortalityR = DeathsMR * 1000 / popUSA_interpolated
    averages = np.zeros(12)
    averagesR = np.zeros(12)
    stdevs = np.zeros(12)
    stdevsR = np.zeros(12)
    for m in range( 12):
        readings = []
        readingsR = []
        for y in range( 1980, 2020):
            j = (y-1980)*12+m
            readings += [ mortality[j]]
            readingsR += [ mortalityR[j]]
        readings = np.array(readings)
        readingsR = np.array(readingsR)
        averages[m] = np.average(readings)
        averagesR[m] = np.average(readingsR)
        stdevs[m] = np.std(readings)
        stdevsR[m] = np.std(readingsR)
    fig = plt.figure( figsize=(15,15))
    fig.suptitle( 'Месячные коэффиценты смертности в США 1980-2019', fontsize=22)
    gs = plt.GridSpec(2, 1, height_ratios=[1,1]) 
    ax1 = plt.subplot(gs[0])
    ax2 = plt.subplot(gs[1])

    ax1.plot(YearM-1980, DeathsM, "-", lw=1, color="b", alpha=0.5, label="Астрономичеческие месяцы")
    ax1.plot(YearM-1980, DeathsMR, "-", lw=1, color="r", alpha=0.5, label="Календарные месяцы")
    for i in range( 1981, 2020):
        ax1.plot(YearM-i, DeathsM, "-", lw=1, color="b", alpha=0.5)
        ax1.plot(YearM-i, DeathsMR, "-", lw=1, color="r", alpha=0.5)
    ax1.plot(YearM-2020, DeathsM, "-", lw=3, color="m" )
    ax1.plot(YearM-2020, DeathsM, "o", lw=3, color="m", label = "Оперативные данные 2020 г" )
    months = np.linspace(0.0416666667, 0.9583333333, 12)
    monthLabels = ["Я","Ф","М","А","М","И","И","А","С","О","Н","Д"]
    ax1.set_xticks(months)
    ax1.set_xticklabels( monthLabels, fontsize=12)
    ax1.set_ylabel('Умерших в месяц, тысяч / население, млн')
    ax1.grid(True)
    ax1.set_xlim(-1/12, 1+1/12)
    ax1.set_ylim(150, 350)
    ax1.legend(loc=1, fontsize=12 )

    for i in range( 1980, 2020):
        ax2.plot(YearM-i, mortality, "-", lw=1, color="b", alpha=0.3)
    ax2.plot(months, averages, "-", lw=3, color="b", label="Среднее за 40 лет (астрономические месяцы)")
    ax2.plot(months, averagesR, "-", lw=3, color="r", alpha=0.5, label="Среднее за 40 лет (календарные месяцы)")
    ax2.fill_between(months, averages+2*stdevs, averages+-2*stdevs, color="b", alpha=0.2, label="2 стандартных отклонения")
    ax2.plot(YearM-2020, mortality, "-", lw=3, color="m")
    ax2.plot(YearM-2020, mortality, "o", lw=3, color="m", label="Оперативные данные 2020 г")
    ax2.set_xticks( months)
    ax2.set_xticklabels( monthLabels, fontsize=12)
    ax2.set_xlim(-1/12, 1+1/12)
    ax2.set_ylim(600, 1000)
    ax2.grid(True)
    ax2.legend(loc=1, fontsize=12 )
    ax2.set_ylabel('Умерших в месяц на 1 млн населения')
    ax2.set_xlabel('Год')        

    plt.savefig( "./Graphs/208_Overlay_Deaths.png")
    return


def Mortality_By_Age( USA_Covid_19, USA_2020, Deaths2020):
    popLabels, popLabelsEng, popColor, Pop  =  Population_Structure_USA()
    YearM, DeathsM = Load_Calibration( "./Data/US_Deaths_1980_2020_monthly.csv", ["Year", "Eq_months"], separator="\t")
    popUSA_interpolated = Population_USA( YearM)
    mortality = DeathsM * 1000 / popUSA_interpolated
    averages = np.zeros(12)
    stdevs = np.zeros(12)
    for m in range( 12):
        readings = []
        for y in range( 1980, 2020):
            j = (y-1980)*12+m
            readings += [ mortality[j]]
        readings = np.array(readings)
        averages[m] = np.average(readings)
        stdevs[m] = np.std(readings)
    months = np.linspace(0.0416666667, 0.9583333333, 12)
    monthLabels = ["Я","Ф","М","А","М","И","И","А","С","О","Н","Д"]

    fig = plt.figure( figsize=(15,15))
    fig.suptitle( 'Месячные коэффиценты смертности в США 1980-2019', fontsize=22)
    gs = plt.GridSpec(2, 1, height_ratios=[1,1]) 
    ax1 = plt.subplot(gs[0])
    ax2 = plt.subplot(gs[1])

#     ax1.plot(YearM-2017, DeathsM, "-", lw=3, color="y", alpha=0.5, label="Умерших в 2017")
#     ax1.plot(YearM-2018, DeathsM, "-", lw=3, color="y", alpha=0.5, label="Умерших в 2018")
#     ax1.plot(YearM-2019, DeathsM, "-", lw=3, color="y", alpha=0.5, label="Умерших в 2019")
#     ax1.plot(YearM-2020, DeathsM, "-", lw=3, color="m" )
#     ax1.plot(YearM-2020, DeathsM, "o", lw=3, color="m", label = "Оперативные данные 2020 г" )
#     prevCurve = None
#     for i, a in enumerate( popLabelsEng):
#         Week, ageDeaths, ageCOVID = Load_Operative_Data( a)
#         Week = (Week-0.5)*7/366*(months[11]-months[0])+months[0]
#         Curve = ageDeaths*366/7/12/1000
#         Week = Week[:-2]
#         Curve = Curve[:-2]
#         y0 = 0.0
#         if prevCurve is not None:
#             Curve += prevCurve
#             y0 = prevCurve 
#         ax1.fill_between(Week, Curve, y0, color=popColor[i], alpha=0.2, label=popLabels[i])
#         prevCurve = Curve
#     ax1.set_xticks(months)
#     ax1.set_xticklabels( monthLabels, fontsize=12)
#     ax1.set_ylabel('Умерших в месяц, тысяч / население, млн')
#     ax1.grid(True)
#     ax1.set_xlim(-1/12, 1+1/12)
#     ax1.set_ylim(0, 350)
#     ax1.legend(loc=1, fontsize=12 )

    ax1.plot(months, averages, "-", lw=3, color="b", label="Среднее за 40 лет (астрономические месяцы)")
    ax1.fill_between(months, averages+2*stdevs, averages+-2*stdevs, color="b", alpha=0.2, label="2 стандартных отклонения")
    ax1.plot(YearM-2020, mortality, "-", lw=3, color="m")
    ax1.plot(YearM-2020, mortality, "o", lw=3, color="m", label="Оперативные данные 2020 г")
    ax1.text( 0.46, 125, "Смертей исключая диагностированный COVID-19")
    prevCurve = None
    for i, a in enumerate( popLabelsEng):
        Week, ageDeaths, ageCOVID = Load_Operative_Data( a)
        Week = (Week-0.5)*7/366*(months[11]-months[0])+months[0]
        Curve = (ageDeaths-ageCOVID)*366/7/12/331.432
        Week = Week[:-3]
        Curve = Curve[:-3]
        y0 = 0.0
        if prevCurve is not None:
            Curve += prevCurve
            y0 = prevCurve 
        ax1.fill_between(Week, Curve, y0, color=popColor[i], alpha=0.2, label=popLabels[i])
        prevCurve = Curve
    ax1.set_xticks( months)
    ax1.set_xticklabels( monthLabels, fontsize=12)
    ax1.set_xlim(-1/12, 1+1/12)
    ax1.set_ylim(0, 1100)
    ax1.grid(True)
    ax1.legend(loc=1, fontsize=12 )
    ax1.set_ylabel('Умерших в месяц на 1 млн населения')
    #ax2.set_xlabel('Год')        

    ax2.plot(months, averages, "-", lw=3, color="b", label="Среднее за 40 лет (астрономические месяцы)")
    ax2.fill_between(months, averages+2*stdevs, averages+-2*stdevs, color="b", alpha=0.2, label="2 стандартных отклонения")
    ax2.plot(YearM-2020, mortality, "-", lw=3, color="m")
    ax2.plot(YearM-2020, mortality, "o", lw=3, color="m", label="Оперативные данные 2020 г")
    ax2.text( 0.46, 125, "Всего смертей")
    prevCurve = None
    for i, a in enumerate( popLabelsEng):
        Week, ageDeaths, ageCOVID = Load_Operative_Data( a)
        Week = (Week-0.5)*7/366*(months[11]-months[0])+months[0]
        Curve = ageDeaths*366/7/12/331.432
        Week = Week[:-3]
        Curve = Curve[:-3]
        y0 = 0.0
        if prevCurve is not None:
            Curve += prevCurve
            y0 = prevCurve 
        ax2.fill_between(Week, Curve, y0, color=popColor[i], alpha=0.2, label=popLabels[i])
        prevCurve = Curve
    ax2.set_xticks( months)
    ax2.set_xticklabels( monthLabels, fontsize=12)
    ax2.set_xlim(-1/12, 1+1/12)
    ax2.set_ylim(0, 1100)
    ax2.grid(True)
    ax2.legend(loc=1, fontsize=12 )
    ax2.set_ylabel('Умерших в месяц на 1 млн населения')
    ax2.set_xlabel('Год')        

    plt.savefig( "./Graphs/209_Deaths_By_Age.png")
    return


def HeartOncology( USA_Covid_19, USA_2020):
    Year, Heart, Oncology = Load_Calibration( "./Data/US_Deaths_1997_2019.csv", ["Year","Heart","Oncology"], separator="\t")
    Labels = []
    for y in Year: Labels += ["{:.0f}".format(y)]
    Labels += ["2020"]
    Labels += ["2021"]
    #print(Year)
    #print(Deaths)
    fig = plt.figure( figsize=(15,10))
    fig.suptitle( 'Причины смертности в США 1998-2017', fontsize=22)
    gs = plt.GridSpec(1, 1, height_ratios=[1]) 
    ax1 = plt.subplot(gs[0])
    ax1.bar(Year[1:-2]+0.5, Heart[1:-2]/12, width=1, color="r",
            alpha=0.25, label="Сердечно-сосудистые заболевания")
    ax1.bar(Year[1:-2]+0.5, Oncology[1:-2]/12, bottom=Heart[1:-2]/12, width=1, color="g",
            alpha=0.25, label="Онкологические заболевания")
    for i, d in enumerate(Heart[1:-2]):
        ax1.text( Year[i+1]+0.2, d/12-10, "{:.0f}".format(d), fontsize=9)
        ax1.text( Year[i+1]+0.2, (d+Oncology[i+1])/12-10, "{:.0f}".format(Oncology[i+1]), fontsize=9)
    ax1.bar(USA_2020+1/24, USA_Covid_19, width=1/12, color="m", alpha=1, label="Смертей от COVID-19 в 2020 г")        
    ax1.set_xlabel('Год')        
    ax1.set_ylabel('Умерших на 1 млн населения в месяц')
    ax1.annotate("Умерших на 1 млн населения в год",
            xy=( Year[2]+0.5, Heart[2]/13), xycoords='data',
            xytext = (Year[10]+0.5, Heart[10]/14), textcoords='data',
            arrowprops=dict(facecolor='black', shrink=0.1, width=2),
            horizontalalignment='right', verticalalignment='top', fontsize=12)
    ax1.annotate("Смерти от COVID-19 по месяцам на 1 млн населения ({:.1f} за 7 мес. 2020 г)".format(sum(USA_Covid_19)),
            xy=( 2020.1, USA_Covid_19[3]), xycoords='data',
            xytext = (2017, 275), textcoords='data',
            arrowprops=dict(facecolor='black', shrink=0.01, width=2),
            horizontalalignment='right', verticalalignment='top', fontsize=12)
    ax1.grid(True)
    ax1.set_xlim(1997, 2022)
    ax1.set_xticks(np.linspace(1997,2021,25))
    ax1.set_xticklabels( Labels, fontsize=9)
    ax1.set_ylim(0, 420)
    ax1.legend(loc=3, fontsize=12 )
    plt.savefig( "./Graphs/202_Heart_and_Onco.png")
    return

def Accidents( USA_Covid_19, USA_2020):
    Year, Accidents, Suicide, Homicide = Load_Calibration( "./Data/US_Deaths_1997_2019.csv",
            ["Year","Accidents", "Suicide", "Homicide"], separator="\t")
    Labels = []
    for y in Year: Labels += ["{:.0f}".format(y)]
    Labels += ["2020"]
    Labels += ["2021"]
    #print(Year)
    #print(Deaths)
    fig = plt.figure( figsize=(15,10))
    fig.suptitle( 'Причины смертности в США 1998-2017', fontsize=22)
    gs = plt.GridSpec(1, 1, height_ratios=[1]) 
    ax1 = plt.subplot(gs[0])
    ax1.bar(Year[1:-2]+0.5, Accidents[1:-2]/12, width=1, color="y",
            alpha=0.25, label="Происшествия и травмы, в т.ч. ДТП")
    ax1.bar(Year[1:-2]+0.5, Suicide[1:-2]/12, bottom=Accidents[1:-2]/12, width=1, color="b",
            alpha=0.25, label="Самоубийства")
    ax1.bar(Year[1:-2]+0.5, Homicide[1:-2]/12, bottom=(Suicide[1:-2]+Accidents[1:-2])/12, width=1, color="r",
            alpha=0.25, label="Убийства и охрана порядка")
    for i, d in enumerate(Accidents[1:-2]):
        ax1.text( Year[i+1]+0.2, d/12-10, "{:.0f}".format(d), fontsize=9)
        ax1.text( Year[i+1]+0.2, (d+Suicide[i+1])/12-6, "{:.0f}".format(Suicide[i+1]), fontsize=9)
        ax1.text( Year[i+1]+0.2, (d+Suicide[i+1]+Homicide[i+1])/12+2, "{:.0f}".format(Homicide[i+1]), fontsize=9)
    ax1.bar(USA_2020+1/24, USA_Covid_19, width=1/12, color="m", alpha=1, label="Смертей от COVID-19 в 2020 г")        
    ax1.set_xlabel('Год')        
    ax1.set_ylabel('Умерших на 1 млн населения в месяц')
    ax1.annotate("Умерших на 1 млн населения в год",
            xy=( Year[2]+0.5, 45), xycoords='data',
            xytext = (2010, 80), textcoords='data',
            arrowprops=dict(facecolor='black', shrink=0.1, width=2),
            horizontalalignment='right', verticalalignment='top', fontsize=12)
    ax1.annotate("Смерти от COVID-19 по месяцам на 1 млн населения ({:.1f} за 7 мес. 2020 г)".format(sum(USA_Covid_19)),
            xy=( 2020.1, USA_Covid_19[3]), xycoords='data',
            xytext = (2017, 140), textcoords='data',
            arrowprops=dict(facecolor='black', shrink=0.01, width=2),
            horizontalalignment='right', verticalalignment='top', fontsize=12)
    ax1.grid(True)
    ax1.set_xlim(1997, 2022)
    ax1.set_xticks(np.linspace(1997,2021,25))
    ax1.set_xticklabels( Labels, fontsize=9)
    ax1.set_ylim(0, 175)
    ax1.legend(loc=2, fontsize=12 )
    plt.savefig( "./Graphs/203_Accidents_Suicide_and_Homicide.png")
    return


def Respiratory( USA_Covid_19, USA_2020):
    Year, Chronic, InflPneumo, Septicemia, Pneumonitis = Load_Calibration( "./Data/US_Deaths_1997_2019.csv",
            ["Year","Chronic respiratory", "Influenza+Pneumonia", "Septicemia", "Pneumonitis"], separator="\t")
    Labels = []
    for y in Year: Labels += ["{:.0f}".format(y)]
    Labels += ["2020"]
    Labels += ["2021"]
    #print(Year)
    #print(Deaths)
    fig = plt.figure( figsize=(15,10))
    fig.suptitle( 'Причины смертности в США 1998-2017', fontsize=22)
    gs = plt.GridSpec(1, 1, height_ratios=[1]) 
    ax1 = plt.subplot(gs[0])
    ax1.bar(Year[1:-2]+0.5, Chronic[1:-2]/12, width=1, color="y",
            alpha=0.25, label="Хронические респираторные, в т.ч. туберкулёз")
    ax1.bar(Year[1:-2]+0.5, InflPneumo[1:-2]/12, bottom=Chronic[1:-2]/12, width=1, color="b",
            alpha=0.25, label="Инфлюэнца и пневмонии")
    ax1.bar(Year[1:-2]+0.5, Septicemia[1:-2]/12, bottom=(InflPneumo[1:-2]+Chronic[1:-2])/12,
            width=1, color="r", alpha=0.25, label="Септицимия, в т.ч. менингит")
    ax1.bar(Year[1:-2]+0.5, Pneumonitis[1:-2]/12, bottom=(InflPneumo[1:-2]+Chronic[1:-2]+Septicemia[1:-2])/12,
            width=1, color="g", alpha=0.25, label="Плевриты, в т.ч. невыясненной природы")
    for i, d in enumerate(Chronic[1:-2]):
        ax1.text( Year[i+1]+0.2, d/12-10, "{:.0f}".format(d), fontsize=9)
        ax1.text( Year[i+1]+0.2, (d+InflPneumo[i+1])/12-6, "{:.0f}".format(InflPneumo[i+1]), fontsize=9)
        ax1.text( Year[i+1]+0.2, (d+InflPneumo[i+1]+Septicemia[i+1])/12-6, "{:.0f}".format(Septicemia[i+1]), fontsize=9)
        ax1.text( Year[i+1]+0.2, (d+InflPneumo[i+1]+Septicemia[i+1]+Pneumonitis[i+1])/12+2, "{:.0f}".format(Pneumonitis[i+1]), fontsize=9)
    ax1.bar(USA_2020+1/24, USA_Covid_19, width=1/12, color="m", alpha=1, label="Смертей от COVID-19 в 2020 г")        
    ax1.set_xlabel('Год')        
    ax1.set_ylabel('Умерших на 1 млн населения в месяц')
    ax1.annotate("Умерших на 1 млн населения в год",
            xy=( Year[2]+0.5, 45), xycoords='data',
            xytext = (2010, 80), textcoords='data',
            arrowprops=dict(facecolor='black', shrink=0.1, width=2),
            horizontalalignment='right', verticalalignment='top', fontsize=12)
    ax1.annotate("Смерти от COVID-19 по месяцам на 1 млн населения ({:.1f} за 7 мес. 2020 г)".format(sum(USA_Covid_19)),
            xy=( 2020.1, USA_Covid_19[3]), xycoords='data',
            xytext = (2017, 140), textcoords='data',
            arrowprops=dict(facecolor='black', shrink=0.01, width=2),
            horizontalalignment='right', verticalalignment='top', fontsize=12)
    ax1.grid(True)
    ax1.set_xlim(1997, 2022)
    ax1.set_xticks(np.linspace(1997,2021,25))
    ax1.set_xticklabels( Labels, fontsize=9)
    ax1.set_ylim(0, 175)
    ax1.legend(loc=2, fontsize=12 )
    plt.savefig( "./Graphs/204_Respiratory.png")
    return


def Cerebrovascular( USA_Covid_19, USA_2020):
    Year, Cerebrovascular, Alzheimer, Diabetes, Kidney,	Liver, Hypertension, Parkinson = Load_Calibration( "./Data/US_Deaths_1997_2019.csv",
            ["Year","Cerebrovascular", "Alzheimer", "Diabetes", "Kidney", "Liver", "Hypertension", "Parkinson"], separator="\t")
    Cerebrovascular += Hypertension
    Alzheimer += Parkinson
    Diabetes += Kidney + Liver
    Labels = []
    for y in Year: Labels += ["{:.0f}".format(y)]
    Labels += ["2020"]
    Labels += ["2021"]
    #print(Year)
    #print(Deaths)
    fig = plt.figure( figsize=(15,10))
    fig.suptitle( 'Причины смертности в США 1998-2017', fontsize=22)
    gs = plt.GridSpec(1, 1, height_ratios=[1]) 
    ax1 = plt.subplot(gs[0])
    ax1.bar(Year[1:-2]+0.5, Cerebrovascular[1:-2]/12, width=1, color="y",
            alpha=0.25, label="Инсульты и гипертония")
    ax1.bar(Year[1:-2]+0.5, Alzheimer[1:-2]/12, bottom=Cerebrovascular[1:-2]/12, width=1, color="b",
            alpha=0.25, label="Старческий маразм, болезни Альцгеймерa и Паркинсона")
    ax1.bar(Year[1:-2]+0.5, Diabetes[1:-2]/12, bottom=(Alzheimer[1:-2]+Cerebrovascular[1:-2])/12,
            width=1, color="r", alpha=0.25, label="Диабет, заболевания почек и печени")
    for i, d in enumerate(Cerebrovascular[1:-2]):
        ax1.text( Year[i+1]+0.2, d/12-10, "{:.0f}".format(d), fontsize=9)
        ax1.text( Year[i+1]+0.2, (d+Alzheimer[i+1])/12-6, "{:.0f}".format(Alzheimer[i+1]), fontsize=9)
        ax1.text( Year[i+1]+0.2, (d+Alzheimer[i+1]+Diabetes[i+1])/12+2, "{:.0f}".format(Diabetes[i+1]), fontsize=9)
    ax1.bar(USA_2020+1/24, USA_Covid_19, width=1/12, color="m", alpha=1, label="Смертей от COVID-19 в 2020 г")        
    ax1.set_xlabel('Год')        
    ax1.set_ylabel('Умерших на 1 млн населения в месяц')
    ax1.annotate("Умерших на 1 млн населения в год",
            xy=( Year[2]+0.5, 114), xycoords='data',
            xytext = (2010, 80), textcoords='data',
            arrowprops=dict(facecolor='black', shrink=0.1, width=2),
            horizontalalignment='right', verticalalignment='top', fontsize=12)
    ax1.annotate("Смерти от COVID-19 по месяцам на 1 млн населения ({:.1f} за 7 мес. 2020 г)".format(sum(USA_Covid_19)),
            xy=( 2020.1, USA_Covid_19[3]), xycoords='data',
            xytext = (2017, 140), textcoords='data',
            arrowprops=dict(facecolor='black', shrink=0.01, width=2),
            horizontalalignment='right', verticalalignment='top', fontsize=12)
    ax1.grid(True)
    ax1.set_xlim(1997, 2022)
    ax1.set_xticks(np.linspace(1997,2021,25))
    ax1.set_xticklabels( Labels, fontsize=9)
    ax1.set_ylim(0, 175)
    ax1.legend(loc=2, fontsize=12 )
    plt.savefig( "./Graphs/205_Stroke_Marasmus_and_Diabetes.png")
    return


def TheRest( USA_Covid_19, USA_2020):
    Year, Others = Load_Calibration( "./Data/US_Deaths_1997_2019.csv",
            ["Year","Others"], separator="\t")
    Labels = []
    for y in Year: Labels += ["{:.0f}".format(y)]
    Labels += ["2020"]
    Labels += ["2021"]
    #print(Year)
    #print(Deaths)
    fig = plt.figure( figsize=(15,10))
    fig.suptitle( 'Причины смертности в США 1998-2017', fontsize=22)
    gs = plt.GridSpec(1, 1, height_ratios=[1]) 
    ax1 = plt.subplot(gs[0])
    ax1.bar(Year[1:-2]+0.5, Others[1:-2]/12, width=1, color="y",
            alpha=0.25, label="Остальные заболевания и состояния")
    for i, d in enumerate(Others[1:-2]):
        ax1.text( Year[i+1]+0.2, d/12-10, "{:.0f}".format(d), fontsize=9)
    ax1.bar(USA_2020+1/24, USA_Covid_19, width=1/12, color="m", alpha=1, label="Смертей от COVID-19 в 2020 г")        
    ax1.set_xlabel('Год')        
    ax1.set_ylabel('Умерших на 1 млн населения в месяц')
    ax1.annotate("Умерших на 1 млн населения в год",
            xy=( Year[2]+0.5, 100), xycoords='data',
            xytext = (2010, 80), textcoords='data',
            arrowprops=dict(facecolor='black', shrink=0.1, width=2),
            horizontalalignment='right', verticalalignment='top', fontsize=12)
    ax1.annotate("Смерти от COVID-19 по месяцам на 1 млн населения ({:.1f} за 7 мес. 2020 г)".format(sum(USA_Covid_19)),
            xy=( 2020.1, USA_Covid_19[3]), xycoords='data',
            xytext = (2017, 150), textcoords='data',
            arrowprops=dict(facecolor='black', shrink=0.01, width=2),
            horizontalalignment='right', verticalalignment='top', fontsize=12)
    ax1.grid(True)
    ax1.set_xlim(1997, 2022)
    ax1.set_xticks(np.linspace(1997,2021,25))
    ax1.set_xticklabels( Labels, fontsize=9)
    ax1.set_ylim(0, 175)
    ax1.legend(loc=2, fontsize=12 )
    plt.savefig( "./Graphs/206_All_Other_Diagnoses.png")
    return


USA_Covid_19 = np.array( [0,0,2398,52939,48628,22238,23851])
USA_2020 = np.linspace( 2020, 2020+6/12, len(USA_Covid_19))
Deaths2020 = 8890*332

Absolute_Deaths( USA_Covid_19, USA_2020, Deaths2020)
Mortality( USA_Covid_19, USA_2020, Deaths2020)
Mortality_Overlay( USA_Covid_19, USA_2020, Deaths2020)
Mortality_By_Age( USA_Covid_19, USA_2020, Deaths2020)
HeartOncology( USA_Covid_19/331, USA_2020)
Accidents( USA_Covid_19/331, USA_2020)
Respiratory( USA_Covid_19/331, USA_2020)
Cerebrovascular( USA_Covid_19/331, USA_2020)
TheRest( USA_Covid_19/331, USA_2020)

if InteractiveModeOn: plt.show(True)
