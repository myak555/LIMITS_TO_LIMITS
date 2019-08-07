from World3_Model import *


def Locate_Maximum( year, data):
    j = np.argmax(data)
    t = year[j]
    v = data[j]
    return j, t, v


def Produce_Region( Earth_Average, dataname, filename, title, vlim):
    Year, Coal_P, Oil_P, Gas_P, Total_P, Import, Population, Consumption_PC, Import_PC = Load_Calibration(
        "../Global Data/" + dataname,
        ["Year", "Coal_P", "Oil_P", "Gas_P", "Total_P", "Import", "Population", "Consumption_PC", "Import_PC"],
        separator = "\t")
    jC, tC, vC = Locate_Maximum( Year, Coal_P)
    jO, tO, vO = Locate_Maximum( Year, Oil_P)
    jG, tG, vG = Locate_Maximum( Year, Gas_P)
    jCons, tCons, vCons = Locate_Maximum( Year, Consumption_PC)
    jImp, tImp, vImp = Locate_Maximum( Year, Import_PC)
    jExp, tExp, vExp = Locate_Maximum( Year, -Import_PC)
    vExp = -vExp

    limits = 1965, 2020
    fig = plt.figure( figsize=(15,10))
    fig.suptitle('Ископаемое топливо: ' + title, fontsize=25)
    gs = plt.GridSpec(2, 1) 
    ax1 = plt.subplot(gs[0])
    ax2 = plt.subplot(gs[1])

    ax1.bar( Year, Gas_P, bottom=Coal_P+Oil_P, alpha=0.3, color="r",
             label="Природный газ: {:.1f} млн toe в {:.0f} г".format(vG, tG))
    ax1.bar( Year, Oil_P, bottom=Coal_P, alpha=0.3, color="g",
             label="Нефть и жидкости: {:.1f} млн toe в {:.0f} г".format(vO, tO) )
    ax1.bar( Year, Coal_P, alpha=0.3, color="k",
             label="Уголь: {:.1f} млн toe в {:.0f} г".format(vC, tC) )
    ax1.plot( [tC, tC], [0,vC], "--", lw=3, color="k")
    ax1.plot( [tO, tO], [0,vO+Coal_P[jO]], "--", lw=3, color="k")
    ax1.plot( [tG, tG], [0,vG+Oil_P[jG]+Coal_P[jG]], "--", lw=3, color="k")
    ax1.plot( [tC, tO, tG], [vC, vO+Coal_P[jO], vG+Oil_P[jG]+Coal_P[jG]], "o", lw=3, color="k")
    ax1.set_xlim( limits)
    ax1.set_ylim( 0, vlim)
    ax1.grid(True)
    ax1.legend(loc=0)
    ax1.set_ylabel("Добыча [млн т нефт.экв.]")

    ax2.bar( Year, Consumption_PC, alpha=0.3, color="g", label="Потребление: {:.0f} кг в {:.0f} г".format(vCons, tCons) )
    ax2.plot( Year, Earth_Average, "-", lw=2, color="k", label="Среднее потребление по планете")
    ax2.plot( [tCons, tCons], [0,vCons], "--", lw=3, color="k")
    ax2.plot( [1965, 2020], [vCons,vCons], "-.", lw=1, color="k")
    ax2.plot( [tCons], [vCons], "o", lw=3, color="k")
    if -vExp > vImp:
        ax2.bar( Year, Import_PC, alpha=0.3, color="r", label="Экспорт: {:.0f} кг в {:.0f} г".format(-vExp, tExp))
        ax2.plot( [tExp, tExp], [0,vExp], "--", lw=3, color="k")
        ax2.plot( [tExp], [vExp], "o", lw=3, color="k")
    else:
        ax2.bar( Year, Import_PC, alpha=0.5, color="r", label="Импорт: {:.0f} кг в {:.0f} г".format(vImp, tImp))
        ax2.plot( [tImp, tImp], [0,vImp], "--", lw=3, color="k")
        ax2.plot( [tImp], [vImp], "o", lw=3, color="k")
    ax2.set_xlim( limits)
    #ax2.set_ylim( 0, 15000)
    ax2.grid(True)
    ax2.legend(loc=0)
    ax2.set_xlabel("Год")
    ax2.set_ylabel("[кг нефт.экв. в год]")
    plt.savefig( "./Graphs/" + filename)
    return Population, Consumption_PC, Import_PC

P0 = Population()
R0 = Resources()
Earth_Average = 1000 * R0.Calibration_Carbon[75:] / P0.Calibration_Total[145:-1]

p_NAM, c_NAM, i_NAM = Produce_Region( Earth_Average,
                "Fossil_Fuel_Consumption_NAMR.txt",
                "figure_21_NAMR.png",
                "Северная Америка (включая Мексику)", 2500)    
p_SLAM, c_SLAM, i_SLAM = Produce_Region( Earth_Average,
                "Fossil_Fuel_Consumption_SLAM.txt",
                "figure_21_SLAM.png",
                "Латинская Америка (без Мексики)", 700)    
p_EUR, c_EUR, i_EUR = Produce_Region( Earth_Average,
                "Fossil_Fuel_Consumption_EURO.txt",
                "figure_21_EURO.png",
                "Европа (без стран бывш. СНГ)", 1200)    
p_FCIS, c_FCIS, i_FCIS = Produce_Region( Earth_Average,
                "Fossil_Fuel_Consumption_FCIS.txt",
                "figure_21_FCIS.png",
                "Страны бывших СССР/СНГ", 2000)    
p_MEA, c_MEA, i_MEA = Produce_Region( Earth_Average,
                "Fossil_Fuel_Consumption_MEAS.txt",
                "figure_21_MEAS.png",
                "Ближний Восток", 2500)    
p_AFR, c_AFR, i_AFR = Produce_Region( Earth_Average,
                "Fossil_Fuel_Consumption_AFRO.txt",
                "figure_21_AFRO.png",
                "Африка", 1000)    
p_CHIN, c_CHIN, i_CHIN = Produce_Region( Earth_Average,
                "Fossil_Fuel_Consumption_CHIN.txt",
                "figure_21_CHIN.png",
                "Геополитическая зона КНР", 2500)    
p_INDS, c_INDS, i_INDS = Produce_Region( Earth_Average,
                "Fossil_Fuel_Consumption_INDS.txt",
                "figure_21_INDS.png",
                "Индостан", 500)    
p_OAO, c_OAO, i_OAO = Produce_Region( Earth_Average,
                "Fossil_Fuel_Consumption_OAAO.txt",
                "figure_21_OAAO.png",
                "Азия и Океания (без КНР и Индостана)", 1200)    

fig = plt.figure( figsize=(15,15))
fig.suptitle('Ископаемое топливо: потребление и импорт/экспорт', fontsize=25)
gs = plt.GridSpec(1, 1) 
ax1 = plt.subplot(gs[0])

ax1.scatter( c_INDS, -i_INDS, s=p_INDS, alpha=0.1, color="y",
             label="Индостан")
ax1.plot( c_INDS, -i_INDS, "-", lw = 3, alpha = 0.3, color="y")
ax1.scatter( c_INDS[-1], -i_INDS[-1], s=p_INDS[-1], alpha=1, color="y")

ax1.scatter( c_CHIN, -i_CHIN, s=p_CHIN, alpha=0.1, color="r",
             label="Геополитическая зона КНР")
ax1.plot( c_CHIN, -i_CHIN, "-", lw = 3, alpha = 0.3, color="r")
ax1.scatter( c_CHIN[-1], -i_CHIN[-1], s=p_CHIN[-1], alpha=1, color="r")

ax1.scatter( c_AFR, -i_AFR, s=p_AFR, alpha=0.1, color="k",
             label="Африка")
ax1.plot( c_AFR, -i_AFR, "-", lw = 3, alpha = 0.3, color="k")
ax1.scatter( c_AFR[-1], -i_AFR[-1], s=p_AFR[-1], alpha=1, color="k")

ax1.scatter( c_OAO, -i_OAO, s=p_OAO, alpha=0.1, color="c",
             label="Азия и Океания (без КНР и Индостана)")
ax1.plot( c_OAO, -i_OAO, "-", lw = 3, alpha = 0.3, color="c")
ax1.scatter( c_OAO[-1], -i_OAO[-1], s=p_OAO[-1], alpha=1, color="c")

ax1.scatter( c_EUR, -i_EUR, s=p_EUR, alpha=0.1, color="orange",
             label="Европа (без стран бывш. СНГ)")
ax1.plot( c_EUR, -i_EUR, "-", lw = 3, alpha = 0.3, color="orange")
ax1.scatter( c_EUR[-1], -i_EUR[-1], s=p_EUR[-1], alpha=1, color="orange")

ax1.scatter( c_SLAM, -i_SLAM, s=p_SLAM, alpha=0.1, color="m",
             label="Латинская Америка (без Мексики)")
ax1.plot( c_SLAM, -i_SLAM, "-", lw = 3, alpha = 0.3, color="m")
ax1.scatter( c_SLAM[-1], -i_SLAM[-1], s=p_SLAM[-1], alpha=1, color="m")

ax1.scatter( c_NAM, -i_NAM, s=p_NAM, alpha=0.1, color="b",
             label="Северная Америка (включая Мексику)")
ax1.plot( c_NAM, -i_NAM, "-", lw = 3, alpha = 0.3, color="b")
ax1.scatter( c_NAM[-1], -i_NAM[-1], s=p_NAM[-1], alpha=1, color="b")

ax1.scatter( c_FCIS, -i_FCIS, s=p_FCIS, alpha=0.1, color="hotpink",
             label="Страны бывших СССР/СНГ")
ax1.plot( c_FCIS, -i_FCIS, "-", lw = 3, alpha = 0.3, color="hotpink")
ax1.scatter( c_FCIS[-1], -i_FCIS[-1], s=p_FCIS[-1], alpha=1, color="hotpink")

ax1.scatter( c_MEA, -i_MEA, s=p_MEA, alpha=0.1, color="g",
             label="Ближний Восток")
ax1.plot( c_MEA, -i_MEA, "-", lw = 3, alpha = 0.3, color="g")
ax1.scatter( c_MEA[-1], -i_MEA[-1], s=p_MEA[-1], alpha=1, color="g")

ax1.plot([Earth_Average[-1],Earth_Average[-1]], [-3000, 14000],
         "-.", lw=3, color="k", label="Среднемировое (2018 г)" )         

ax1.set_xscale( "log")
ax1.set_xlim( 100, 10000)
ax1.set_ylim( -3000, 14000)
ax1.grid(True)
ax1.legend(loc=0)
ax1.set_xlabel("Потребление [кг нефт.экв. на душу в год]")
ax1.set_ylabel("<--- Импорт [кг нефт.экв. на душу в год] Экспорт --->")
plt.savefig( "./Graphs/Consumption_vs_Export.png")

#if InteractiveModeOn: plt.show(True)
