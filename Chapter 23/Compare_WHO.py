from COVID_19_Parcing import *


def Mortality_Leaders():
    cc = Covid_Countries()
    fig = plt.figure( figsize=(15,15))
    fig.suptitle( 'Сравнение стран по смертности от COVID-19', fontsize=22)
    gs = plt.GridSpec(1, 1, height_ratios=[1]) 
    ax1 = plt.subplot(gs[0])
    cc.inputCountryFile( "Belgium", ax1)
    cc.inputCountryFile( "The United Kingdom", ax1)
    cc.inputCountryFile( "Spain", ax1)
    cc.inputCountryFile( "Italy", ax1)
    cc.inputCountryFile( "Sweden", ax1)
    cc.inputCountryFile( "France", ax1)
    cc.inputCountryFile( "Chile", ax1)
    cc.inputCountryFile( "United States of America", ax1)
    cc.inputCountryFile( "Peru", ax1)
    cc.inputCountryFile( "Brazil", ax1)    
    cc.inputCountryFile( "Ireland", ax1)
    cc.inputCountryFile( "Netherlands", ax1)
    cc.inputCountryFile( "Ecuador", ax1)
    cc.inputCountryFile( "Mexico", ax1)
    cc.inputCountryFile( "Panama", ax1)
    cc.inputCountryFile( "Canada", ax1)
    cc.inputCountryFile( "Armenia", ax1)
    cc.inputCountryFile( "North Macedonia", ax1)
    cc.inputCountryFile( "Switzerland", ax1)
    cc.inputCountryFile( "Luxembourg", ax1)
    cc.inputCountryFile( "Bolivia (Plurinational State of)", ax1)
    cc.inputCountryFile( "Republic of Moldova", ax1)
    cc.inputCountryFile( "Iran (Islamic Republic of)", ax1)
    cc.inputCountryFile( "Portugal", ax1)
    cc.inputCountryFile( "Kyrgyzstan", ax1)
    cc.inputCountryFile( "Colombia", ax1)
    cc.inputCountryFile( "French Guiana", ax1)
    cc.inputCountryFile( "Germany", ax1)
    cc.inputCountryFile( "Denmark", ax1)
    cc.inputCountryFile( "Romania", ax1)
    cc.inputCountryFile( "Russian Federation", ax1)
    ax1.plot([-55,20], [170,170], "--", lw=2, color="r")        
    ax1.text(-35, 159, "Типичная смертность от гриппа и пневмонии", color='r', fontsize=12)        
    ax1.plot([-55,20], [76.7,76.7], "-.", lw=2, color="r")        
    ax1.text(-35, 50, "Среднемировой уровень 76.7", color='r', fontsize=12)        
    ax1.set_xlabel('День с момента первой подтверждённой смерти')        
    ax1.set_ylabel('Смертей на млн')
    ax1.text(80,890, "площадь маркера пропорциональна населению", fontsize=11)
    ax1.grid(True)
    ax1.set_xlim(-55, 180)
    ax1.set_ylim(-50, 900)
    ax1.legend(loc=2, fontsize=11 )
    plt.savefig( "./Graphs/009_Deaths_Comparison_over_100.png")
    return

def Russian_Empire():
    cc = Covid_Countries()
    fig = plt.figure( figsize=(15,15))
    fig.suptitle( 'Сравнение стран бывш. Российской Империи по смертности от COVID-19', fontsize=22)
    gs = plt.GridSpec(1, 1, height_ratios=[1]) 
    ax1 = plt.subplot(gs[0])
    cc.inputCountryFile( "Armenia", ax1)
    cc.inputCountryFile( "Republic of Moldova", ax1)
    cc.inputCountryFile( "Kyrgyzstan", ax1)
    cc.inputCountryFile( "Russian Federation", ax1)
    cc.inputCountryFile( "Finland", ax1)
    cc.inputCountryFile( "Estonia", ax1)
    cc.inputCountryFile( "Belarus", ax1)
    cc.inputCountryFile( "Poland", ax1)
    cc.inputCountryFile( "Azerbaijan", ax1)
    cc.inputCountryFile( "Ukraine", ax1)
    cc.inputCountryFile( "Lithuania", ax1)
    cc.inputCountryFile( "Kazakhstan", ax1)
    cc.inputCountryFile( "Latvia", ax1)
    cc.inputCountryFile( "Tajikistan", ax1)
    cc.inputCountryFile( "Georgia", ax1)
    cc.inputCountryFile( "Uzbekistan", ax1)
    cc.inputCountryFile( "Turkmenistan", ax1)
    ax1.plot([-55,120], [170,170], "--", lw=2, color="r")        
    ax1.text(40, 167, "Типичная смертность от гриппа и пневмонии", color='r', fontsize=12)        
    ax1.plot([-20, 80], [76.7, 76.7], '-.', lw=2, color="r")        
    ax1.text(0, 70, 'Среднемировой уровень 76.7', color='r', fontsize=12)        
    ax1.set_xlabel('День с момента первой подтверждённой смерти или первого случая')        
    ax1.set_ylabel('Смертей на млн')
    ax1.text(65,137, "площадь маркера пропорциональна населению", fontsize=12)
    ax1.grid(True)
    ax1.set_xlim(-20,150)
    ax1.set_ylim(-3, 300)
    ax1.legend(loc=2, fontsize=12)
    plt.savefig( "./Graphs/010_Deaths_Comparison_CIS.png")
    return


def Minsk_Parade():
    cc = Covid_Countries()
    fig = plt.figure( figsize=(15,15))
    fig.suptitle( 'Парад Победы (над COVID-19) в Минске 9 мая 2020 г', fontsize=22)
    gs = plt.GridSpec(1, 1, height_ratios=[1]) 
    ax1 = plt.subplot(gs[0])
    cc.inputCountryFile( "Iran (Islamic Republic of)", ax1)
    cc.inputCountryFile( "Republic of Moldova", ax1)
    cc.inputCountryFile( "Hungary", ax1)
    cc.inputCountryFile( "Turkey", ax1)
    cc.inputCountryFile( "Armenia", ax1)
    cc.inputCountryFile( "Russian Federation", ax1)
    cc.inputCountryFile( "Serbia", ax1)
    cc.inputCountryFile( "United Arab Emirates", ax1)
    cc.inputCountryFile( "Belarus", ax1)
    cc.inputCountryFile( "Pakistan", ax1)
    cc.inputCountryFile( "Sudan", ax1)
    cc.inputCountryFile( "Azerbaijan", ax1)
    cc.inputCountryFile( "Slovakia", ax1)
    cc.inputCountryFile( "Tajikistan", ax1)
    cc.inputCountryFile( "China", ax1)
    cc.inputCountryFile( "Kyrgyzstan", ax1)
    cc.inputCountryFile( "Kazakhstan", ax1)
    cc.inputCountryFile( "occupied Palestinian territory", ax1)
    cc.inputCountryFile( "Libya", ax1)
    cc.inputCountryFile( "Venezuela (Bolivarian Republic of)", ax1)
    cc.inputCountryFile( "Viet Nam", ax1)
    cc.inputCountryFile( "Dem. People's Republic of Korea", ax1)
    ax1.set_xlabel('День с момента первой подтверждённой смерти или первого случая')        
    ax1.set_ylabel('Смертей на млн')
    ax1.text(-40,-1, "площадь маркера пропорциональна населению", fontsize=12)
    ax1.grid(True)
    ax1.set_xlim(-50, 160)
    ax1.set_ylim(-1.5, 17.5)
    ax1.legend(loc=2, fontsize=12)
    plt.savefig( "./Graphs/011_Deaths_Comparison_Minsk_Parade_Expanded.png")
    ax1.set_ylim(-3, 100)
    plt.savefig( "./Graphs/010_Deaths_Comparison_Minsk_Parade.png")
    return


def Middle_East():
    cc = Covid_Countries()
    fig = plt.figure( figsize=(15,15))
    fig.suptitle( 'COVID-19 на Ближнем Востоке', fontsize=22)
    gs = plt.GridSpec(1, 1, height_ratios=[1]) 
    ax1 = plt.subplot(gs[0])
    cc.inputCountryFile( "Iran (Islamic Republic of)", ax1, delay=0)
    cc.inputCountryFile( "Israel", ax1, delay=0)
    cc.inputCountryFile( "Iraq", ax1, delay=0)
    cc.inputCountryFile( "occupied Palestinian territory", ax1, delay=0)
    cc.inputCountryFile( "Syrian Arab Republic", ax1, delay=0)
    ##cc.inputCountryFile( "Republic of Moldova", ax1, delay=0)
    ##cc.inputCountryFile( "Serbia", ax1, delay=0)
    ##cc.inputCountryFile( "United Arab Emirates", ax1, delay=0)
    ##cc.inputCountryFile( "Armenia", ax1, delay=0)
    ##cc.inputCountryFile( "Belarus", ax1, delay=0)
    ##cc.inputCountryFile( "Russian Federation", ax1, delay=0)
    ##cc.inputCountryFile( "Slovakia", ax1, delay=0)
    ##cc.inputCountryFile( "Azerbaijan", ax1, delay=0)
    ##cc.inputCountryFile( "Pakistan", ax1, delay=0)
    ##cc.inputCountryFile( "China", ax1, delay=0)
    ##cc.inputCountryFile( "Sudan", ax1, delay=0)
    ##cc.inputCountryFile( "Libya", ax1, delay=0)
    ##cc.inputCountryFile( "Venezuela (Bolivarian Republic of)", ax1, delay=0)
    ##cc.inputCountryFile( "Viet Nam", ax1, delay=0)
    ##cc.inputCountryFile( "Dem. People's Republic of Korea", ax1, delay=0)
    ax1.set_xlabel('День с момента первой подтверждённой смерти или первого случая')        
    ax1.set_ylabel('Смертей на млн')
    ax1.text(-40,-1, "площадь маркера пропорциональна населению", fontsize=12)
    ax1.grid(True)
    ax1.set_xlim(-50, 125)
    ax1.set_ylim(-1.5, 17.5)
    ax1.legend(loc=2, fontsize=12)
    plt.savefig( "./Graphs/012_Deaths_Middle_East.png")

    return

def Leaders_DPA65():
    cc = Covid_Countries()
    fig = plt.figure( figsize=(15,15))
    fig.suptitle( 'Смертей от COVID-19 по отношению к смертности "65+" в 2019 г', fontsize=22)
    gs = plt.GridSpec(1, 1, height_ratios=[1]) 
    ax1 = plt.subplot(gs[0])
    cc.inputCountryFile( "Peru", ax1, method="dpa65")
    cc.inputCountryFile( "Ecuador", ax1, method="dpa65")
    cc.inputCountryFile( "Belgium", ax1, method="dpa65")
    cc.inputCountryFile( "Brazil", ax1, method="dpa65")
    cc.inputCountryFile( "Chile", ax1, method="dpa65")
    cc.inputCountryFile( "Qatar", ax1, method="dpa65")
    cc.inputCountryFile( "Mexico", ax1, method="dpa65")
    cc.inputCountryFile( "Panama", ax1, method="dpa65")
    cc.inputCountryFile( "The United Kingdom", ax1, method="dpa65")
    cc.inputCountryFile( "Spain", ax1, method="dpa65")
    cc.inputCountryFile( "United Arab Emirates", ax1, method="dpa65")
    cc.inputCountryFile( "Ireland", ax1, method="dpa65")
    cc.inputCountryFile( "Sweden", ax1, method="dpa65")
    cc.inputCountryFile( "Kuwait", ax1, method="dpa65")
    cc.inputCountryFile( "United States of America", ax1, method="dpa65")
    cc.inputCountryFile( "Bahrain", ax1, method="dpa65")
    cc.inputCountryFile( "Italy", ax1, method="dpa65")
    cc.inputCountryFile( "Bolivia (Plurinational State of)", ax1, method="dpa65")
    cc.inputCountryFile( "Oman", ax1, method="dpa65")
    cc.inputCountryFile( "France", ax1, method="dpa65")
    cc.inputCountryFile( "Iran (Islamic Republic of)", ax1, method="dpa65")
    cc.inputCountryFile( "Netherlands", ax1, method="dpa65")
    cc.inputCountryFile( "Iraq", ax1, method="dpa65")
    cc.inputCountryFile( "Honduras", ax1, method="dpa65")
    cc.inputCountryFile( "Kyrgyzstan", ax1, method="dpa65")
    cc.inputCountryFile( "Guatemala", ax1, method="dpa65")
    cc.inputCountryFile( "Saudi Arabia", ax1, method="dpa65")
    cc.inputCountryFile( "Colombia", ax1, method="dpa65")
    cc.inputCountryFile( "Canada", ax1, method="dpa65")
    cc.inputCountryFile( "Luxembourg", ax1, method="dpa65")
    cc.inputCountryFile( "Armenia", ax1, method="dpa65")
    cc.inputCountryFile( "Russian Federation", ax1, method="dpa65")

    ax1.plot([-45, 100], [1.80, 1.80], "--", lw=1 , color="r")
    ax1.text(-40, 1.90, "Среднемировое 1.80%", fontsize=12)   
    ax1.set_xlabel('День с момента первой подтверждённой смерти или первого случая')        
    ax1.set_ylabel('Смертей от COVID-19 к смертям 2019 года, %')
    ax1.text(-40,-0.5, "площадь маркера пропорциональна населению", fontsize=12)   
    ax1.grid(True)
    ax1.set_xlim(-45, 170)
    ax1.set_ylim(-1, 20.0)
    ax1.legend(loc=2, fontsize=11)
    plt.savefig( "./Graphs/013_Deaths_Leaders_DPA65.png")


def Russian_Empire_DPA65():
    cc = Covid_Countries()
    fig = plt.figure( figsize=(15,15))
    fig.suptitle( 'Смертей от COVID-19 по отношению к смертности "65+" в 2019 г', fontsize=22)
    gs = plt.GridSpec(1, 1, height_ratios=[1]) 
    ax1 = plt.subplot(gs[0])
    cc.inputCountryFile( "Kyrgyzstan", ax1, method="dpa65")
    cc.inputCountryFile( "Armenia", ax1, method="dpa65")
    cc.inputCountryFile( "Republic of Moldova", ax1, method="dpa65")
    cc.inputCountryFile( "Russian Federation", ax1, method="dpa65")
    cc.inputCountryFile( "Azerbaijan", ax1, method="dpa65")
    cc.inputCountryFile( "Finland", ax1, method="dpa65")
    cc.inputCountryFile( "Belarus", ax1, method="dpa65")
    cc.inputCountryFile( "Poland", ax1, method="dpa65")
    cc.inputCountryFile( "Estonia", ax1, method="dpa65")
    cc.inputCountryFile( "Kazakhstan", ax1, method="dpa65")
    cc.inputCountryFile( "Ukraine", ax1, method="dpa65")
    cc.inputCountryFile( "Tajikistan", ax1, method="dpa65")
    cc.inputCountryFile( "Lithuania", ax1, method="dpa65")
    cc.inputCountryFile( "Latvia", ax1, method="dpa65")
    cc.inputCountryFile( "Uzbekistan", ax1, method="dpa65")
    cc.inputCountryFile( "Georgia", ax1, method="dpa65")
    cc.inputCountryFile( "Turkmenistan", ax1, method="dpa65")
    ax1.plot([75, 160], [1.80, 1.80], "--", lw=1 , color="r")
    ax1.text(100, 1.80, "Среднемировое 1.80%", fontsize=12)   
    ax1.set_xlabel('День с момента первой подтверждённой смерти или первого случая')        
    ax1.set_ylabel('Смертей от COVID-19 к смертям 2019 года, %')
    ax1.text(-15,-0.025, "площадь маркера пропорциональна населению", fontsize=12)
    ax1.grid(True)
    ax1.set_xlim(-20,160)
    ax1.set_ylim(-0.05, 6.0)
    ax1.legend(loc=2, fontsize=11)
    plt.savefig( "./Graphs/014_Deaths_Comparison_CIS_DPA65.png")
    return

def Small_Countries_CAR():
    countries = [
        "Sint Maarten",
        "Montserrat",
        "Bermuda",
        "Saint Martin",
        "United States Virgin Islands",
        "Martinique",
        "British Virgin Islands",
        "Guadeloupe",
        "Antigua and Barbuda", 
        "Aruba",
        "Turks and Caicos Islands",
        "Bahamas",
        "Barbados",
        "Cayman Islands",
        "Curacao",
        "Saint Lucia",
        "Saint Vincent and the Grenadines",
        "Grenada",
        "Dominica",
        "Saint Kitts and Nevis",
        "Faroe Islands",
        "Bonaire, Sint Eustatius and Saba",
        "Anguilla",
        "Saint Barthelemy"]
    cc = Covid_Countries()
    fig = plt.figure( figsize=(15,15))
    fig.suptitle( 'COVID-19: малые территории Карибского Бассейна', fontsize=22)
    gs = plt.GridSpec(1, 1, height_ratios=[1]) 
    ax1 = plt.subplot(gs[0])
    averageDay = np.linspace( 1, 180, 180)
    averageCases = np.zeros( len( averageDay))
    averageDeaths = np.zeros( len( averageDay))
    totalPopulation = 0
    for c in countries:
        cc.inputCountryFile( c, ax1)
        cnt = cc.Countries[c]
        totalPopulation += cnt.Population / 1000
        for i, d in enumerate( cnt.Days):
            j = int(d)
            averageCases[j] += cnt.Cases[i]
            averageDeaths[j] += cnt.Deaths[i]
    shiftCases = np.nonzero(averageCases)[0]
    shiftDeaths = np.nonzero(averageDeaths)[0][0]
    lastDay = int( np.max(shiftCases))
    shiftCases = shiftCases[0]
    averageCases /= totalPopulation
    averageDeaths /= totalPopulation
    ax1.plot( averageDay[:lastDay]-shiftDeaths-1, averageDeaths[:lastDay], '-', lw=5, color='r', alpha=0.5, label="Среднее")
    ax1.set_xlabel('День с первого случая либо первой смерти')        
    ax1.set_ylabel('Смертей от COVID-19 на млн населения')
    ax1.text(50,-10, "площадь маркера пропорциональна населению", fontsize=12)
    ax1.grid(True)
    ax1.set_xlim(-40,120)
    ax1.set_ylim(-20, 160)
    ax1.legend(loc=2, fontsize=10)
    plt.savefig( "./Graphs/015_Small_CAR.png")
    return


def Small_Countries():
    cc = Covid_Countries()
    fig = plt.figure( figsize=(15,15))
    fig.suptitle( 'COVID-19 - малые страны и территории', fontsize=22)
    gs = plt.GridSpec(1, 1, height_ratios=[1]) 
    ax1 = plt.subplot(gs[0])
    #cc.inputCountryFile( "Diamond Princess", ax1)
    cc.inputCountryFile( "San Marino", ax1)
    cc.inputCountryFile( "Andorra", ax1)
    cc.inputCountryFile( "Sint Maarten", ax1)
    cc.inputCountryFile( "Isle of Man", ax1)
    cc.inputCountryFile( "Jersey", ax1)
    cc.inputCountryFile( "Montserrat", ax1)
    cc.inputCountryFile( "Guernsey", ax1)
    cc.inputCountryFile( "Bermuda", ax1)
    cc.inputCountryFile( "Saint Martin", ax1)
    cc.inputCountryFile( "United States Virgin Islands", ax1)
    cc.inputCountryFile( "Northern Mariana Islands (Commonwealth of the)", ax1)
    cc.inputCountryFile( "British Virgin Islands", ax1)
    cc.inputCountryFile( "Antigua and Barbuda", ax1)
    cc.inputCountryFile( "Aruba", ax1)
    cc.inputCountryFile( "Turks and Caicos Islands", ax1)
    cc.inputCountryFile( "Monaco", ax1)
    cc.inputCountryFile( "Liechtenstein", ax1)
    cc.inputCountryFile( "Cayman Islands", ax1)
    cc.inputCountryFile( "Holy See", ax1)
##Tokelau
##Falkland Islands (Malvinas)
##Saint Helena
##Saint Pierre and Miquelon
##Saint Barthelemy
##Nauru
##Tuvalu
##Wallis and Futuna Islands
##Anguilla
##Palau
##Bonaire, Sint Eustatius and Saba
##Gibraltar
##Faroe Islands
##Marshall Islands
##Greenland
##Saint Kitts and Nevis
##Dominica
##Seychelles
##Tonga
##Micronesia (Fed. States of)
##Grenada

    ax1.set_xlabel('День с момента первой подтверждённой смерти или первого случая')        
    ax1.set_ylabel('Смертей от COVID-19 на млн населения')
    ax1.text(50,-0.025, "площадь маркера пропорциональна населению", fontsize=12)
    ax1.grid(True)
    ax1.set_xlim(-20,120)
    #ax1.set_ylim(-0.05, 0.65)
    ax1.legend(loc=2, fontsize=12)
    plt.savefig( "./Graphs/015_Small_Countries.png")
    return

def Pair_Comparisons( countries, xl, xr, y0b, y0t, y1b, y1t, filename):
    cc = Covid_Countries()
    fig = plt.figure( figsize=(15,15))
    sTitle = 'COVID-19: '
    for c in countries:
        sTitle += c
        sTitle += ', '
    sTitle = sTitle[:-2]        
    fig.suptitle( sTitle, fontsize=22)
    gs = plt.GridSpec(2, 1, height_ratios=[1,1]) 
    ax0 = plt.subplot(gs[0])
    ax1 = plt.subplot(gs[1])
    averageDay = np.linspace( 1, 250, 250)
    averageCases = np.zeros( len( averageDay))
    averageDeaths = np.zeros( len( averageDay))
    totalPopulation = 0
    for c in countries:
        cc.inputCountryFile( c, ax1, ax0)
        cnt = cc.Countries[c]
        totalPopulation += cnt.Population / 1000
        #print( cnt.Days)
        for i, d in enumerate( cnt.Days):
            j = int(d)
            averageCases[j] += cnt.Cases[i]
            averageDeaths[j] += cnt.Deaths[i]
    shiftCases = np.nonzero(averageCases)[0]
    shiftDeaths = np.nonzero(averageDeaths)[0][0]
    lastDay = int( np.max(shiftCases))
    shiftCases = shiftCases[0]
    averageCases /= totalPopulation
    averageDeaths /= totalPopulation
    #print(averageDeaths, shift)
    ax0.plot( averageDay[:lastDay]-shiftDeaths-1, averageCases[:lastDay], '-', lw=5, color='r', alpha=0.5, label="Среднее")
    ax1.plot( averageDay[:lastDay]-shiftDeaths-1, averageDeaths[:lastDay], '-', lw=5, color='r', alpha=0.5, label="Среднее")
    if y1t > 110:
        ax1.text(xl+10, 100 - (y1t-y1b)*0.04, "Статистически-значимый уровень", color='r', alpha=0.5, fontsize=12)        
        ax1.plot([xl, xr],[100,100], '--', lw=3, color='r', alpha=0.5)
    ax1.set_xlabel('День с момента первой подтверждённой смерти или первого случая')        
    ax0.set_ylabel('Случаев на млн')
    ax1.set_ylabel('Смертей на млн')
    ax0.text((xr+xl)*0.5,(y0t+y0b)*0.05, "площадь маркера пропорциональна населению", fontsize=12)
    ax0.grid(True)
    ax1.grid(True)
    ax0.set_xlim(xl, xr)
    ax1.set_xlim(xl, xr)
    ax0.set_ylim( y0b, y0t)
    ax1.set_ylim( y1b, y1t)
    ax0.legend(loc=2, fontsize=12)
    ax1.legend(loc=2, fontsize=12)
    plt.savefig( "./Graphs" + filename + ".png")
    return

#Minsk_Parade()
Mortality_Leaders()
Leaders_DPA65()
Russian_Empire()
Russian_Empire_DPA65()

#Small_Countries()
#Pair_Comparisons(["Sint Maarten", "Saint Martin"],
#                 -20, 80, -100, 2100, 0, 400,
#                 "016_01_Comparison_Sent-Manrin_Sint_Maarten")
#Pair_Comparisons([ "Jersey", "Guernsey", "Isle of Man"],
#                 -20, 80, -100, 5000, 0, 300,
#                 "016_02_Channel_Islands_and_Man")
#Pair_Comparisons([ "Mayotte", "Reunion", "Seychelles"],
#                 -30, 100, -100, 8000, 0, 140,
#                 "016_03_Mayotte_Reunion_Seychelles")
#Pair_Comparisons([ "United States of America", "Canada", "Mexico"],
#                 0, 130, -100, 6000, 0, 400,
#                 "016_04_USA_Canada_Mexico")
#Pair_Comparisons([ "Estonia", "Lithuania", "Latvia"],
#                 -20, 100, -50, 1750, 0, 60,
#                 "016_05_Latvia_Lithuania_Estonia")
#Pair_Comparisons([ "Republic of Moldova", "Romania"],
#                 -20, 100, -50, 2500, 0, 100,
#                 "016_06_Moldova_Romania")
#Pair_Comparisons([ "Czechia", "Slovakia"],
#                 -20, 100, -50, 1000, 0, 40,
#                 "016_07_Czechia_Slovakia")
#Pair_Comparisons([ "Sweden", "Finland", "Norway"],
#                 -20, 100, -50, 4500, 0, 500,
#                 "016_08_Sweden_Finland_Norway")
#Pair_Comparisons([ "Netherlands", "Denmark"],
#                 -20, 100, -50, 3000, 0, 400,
#                 "016_09_Netherlands_Denmark")
#Pair_Comparisons([ "Cuba", "Puerto Rico"],
#                 -20, 100, -50, 1100, 0, 50,
#                 "016_10_Cuba_PuertoRico")
#Pair_Comparisons([ "Haiti", "Dominican Republic"],
#                 -20, 100, -50, 1750, 0, 50,
#                 "016_11_Haiti_DominicanRepublic")
#Pair_Comparisons([ "Spain", "Portugal"],
#                 -20, 100, -50, 6000, 0, 700,
#                 "016_12_Spain_Portugal")
#Pair_Comparisons([ "Bulgaria", "Greece"],
#                 -20, 100, -50, 400, 0, 25,
#                 "016_13_Bulgaria_Greece")
#Pair_Comparisons([ "Kosovo", "Serbia", "North Macedonia"],
#                 -20, 100, -50, 1500, 0, 80,
#                 "016_14_Kosovo_Serbia_Macedonia")
#Pair_Comparisons([ "Turkey", "Syrian Arab Republic", "Yemen"],
#                 -20, 100, -50, 2200, 0, 60,
#                 "016_15_Turkey_Syria_Yemen")
#Pair_Comparisons([ "Israel", "occupied Palestinian territory", "Lebanon"],
#                 -20, 100, -50, 2200, 0, 35,
#                 "016_16_Israel_Palestine_Lebanon")
#Pair_Comparisons([ "Pakistan", "Afghanistan"],
#                 -20, 100, -50, 700, 0, 10,
#                 "016_17_Pakistan_Afghanistan")
#Pair_Comparisons([ "Pakistan", "India", "Bangladesh"],
#                 -20, 100, -50, 450, 0, 10,
#                 "016_18_Pakistan_India_Bangladesh")
#Pair_Comparisons([ "Brazil", "Argentina"],
#                 -20, 100, -50, 3000, 0, 160,
#                 "016_19_Brazil_Argentina")
#Pair_Comparisons([ "Ecuador", "Peru", "Colombia"],
#                 -20, 100, -50, 5500, 0, 220,
#                 "016_20_Ecuador_Peru_Colombia")
#Pair_Comparisons([ "Nicaragua", "Costa Rica", "Panama"],
#                 -20, 100, -50, 3500, 0, 90,
#                 "016_21_Nicaragua_CostaRica_Panama")

Pair_Comparisons([ "Germany", "Russian Federation", "Austria"],
                 -20, 200, -50, 7000, 0, 150,
                 "016_22_Germany_Russia_Austria")

#Small_Countries_CAR()

if InteractiveModeOn: plt.show(True)
