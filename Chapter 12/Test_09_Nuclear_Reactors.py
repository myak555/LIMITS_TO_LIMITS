from Predictions import *

f_out = open( "./Data/Nuclear_Reactor_Shutdowns_Summary.txt", "w")
f_out.write("#\n")
f_out.write("# REACTORS SHUTDOWN:\n")
f_out.write("#\n")
f_out.write("Year_Connected\tYear_Shutdown\tYears_Operating\tInstalled_Power\tName\n")
Added_Data = []
Comm_Data = []
Name_Data = []
f_start = open("./Data/Nuclear_Reactor_Commissioning.txt")
for i in range(1000):
    s = f_start.readline()
    if len(s) <= 0: break
    Comm_Data += [s.strip()]
    ss = s.split(" \t")
    name = ss[0].strip()
    Added_Data += [name]
    Name_Data += [name[5:]]
f_start.close()


f_end = open("./Data/Nuclear_Reactor_Shutdown.txt")
Removed_Data = []
for i in range(1000):
    s = f_end.readline()
    if len(s) <= 0: break
    s = s.strip()
    ss = s.split(" \t")
    name = ss[0]
    name = name[5:].strip()
    Removed_Data += [name]
    for a in Added_Data:
        if name in a:
            outs = a[0:4] + "\t"
            r = s.split(" MW(e)")[0]
            rr = r.split(' \t(')
            outs += rr[0][0:4] + "\t"
            outs += str( int( rr[0][0:5])-int(a[0:5])) + "\t"
            outs += rr[1].strip() + "\t"
            outs += rr[0][5:]  + "\n"
            f_out.write(outs)
            break
f_end.close()
f_out.close()

Reactor_Years = []
Reactor_MW = []
f_out = open( "./Data/Nuclear_Reactor_Operating_Summary.txt", "w")
for i in range( len(Comm_Data)):
    if Name_Data[i] in Removed_Data: continue
    outs = Comm_Data[i][0:4] + "\t"
    Reactor_Years += [int(Comm_Data[i][0:4])]    
    r = Comm_Data[i].split(" MW(e)")[0]
    rr = r.split(' \t(')
    outs += rr[1].strip() + "\t"
    Reactor_MW += [int(rr[1].strip())]    
    outs += rr[0][5:] + "\n"
    f_out.write(outs)
f_out.close()

Ages = np.linspace(1969,2018,50)
RAges = np.zeros(50)
PAges = np.zeros(50)
Powers = np.linspace(50,1750,36)
RPowers = np.zeros(36)
for i in range( len(Reactor_Years)):
    ry = Reactor_Years[i]-1969
    RAges[ry] += 1
    PAges[ry] += Reactor_MW[i]/1000
for rw in Reactor_MW:
    RPowers[int(rw/50)] += 1

years = np.linspace(1954, 2018, 65)
plants_connected = np.zeros( len(years))
MW_connected = np.zeros( len(years))
f_start = open("./Data/Nuclear_Reactor_Commissioning.txt")
for i in range(1000):
    s = f_start.readline()
    if len(s) <= 0: break
    ss = s.split("MW(e)")
    n = int(s[0:4])
    ss1 = ss[0].split('(')
    w = float( ss1[-1])
    plants_connected[n-1954] += 1
    MW_connected[n-1954] += w
f_start.close()

plants_disconnected = np.zeros( len(years))
MW_disconnected = np.zeros( len(years))
f_end = open("./Data/Nuclear_Reactor_Shutdown.txt")
for i in range(1000):
    s = f_end.readline()
    if len(s) <= 0: break
    ss = s.split("MW(e)")
    n = int(s[0:4])
    ss1 = ss[0].split('(')
    w = float( ss1[-1])
    #print( "{:g}\t{:g}".format( n, w)) 
    plants_disconnected[n-1954] += 1
    MW_disconnected[n-1954] += w
f_end.close()

p, w = 0, 0
plants_operating = np.zeros( len(plants_connected))
MW_operating = np.zeros( len(plants_connected))
for i in range( len(plants_operating)):
    p += plants_connected[i]
    p -= plants_disconnected[i]
    plants_operating[i] = p
    w += MW_connected[i]
    w -= MW_disconnected[i]
    MW_operating[i] = w
    print( "{:g}\t{:g}\t{:g}\t{:.0f}\t{:.0f}\t{:.0f}".format(years[i],
        plants_connected[i],plants_disconnected[i],
        MW_connected[i],MW_disconnected[i],w/1000))

y, nuc = Load_Calibration("Energy_Calibration.csv", "Year", "Nuclear")
nuc *= 4419.2 / 24 / 365.25

y1, nuc1 = Load_Calibration("./Data/Civil_Nuclear_Energy_Generation.csv", "Year", "Nuclear_Generation")
nuc1 *= 1000 / 24 / 365.25

x_start, x_end = 1950, 2020

fig = plt.figure( figsize=(15,10))
fig.suptitle( 'Гражданские генерирующие мощности ядерной энергетики', fontsize=22)
gs = plt.GridSpec(2, 1, height_ratios=[1, 1]) 
ax1 = plt.subplot(gs[0])
ax2 = plt.subplot(gs[1])

ax1.set_title("Ввод и вывод реакторов")
ax1.bar( years, plants_connected * 10, 0.35, alpha=0.4, color="g", label="Ввод (x10)")
ax1.bar( years, -plants_disconnected * 10, 0.35, alpha=0.4, color="r", label="Вывод (x10)")
ax1.plot( years, plants_operating, "-", color="k", label="Рабочих реакторов")
ax1.plot( years, MW_operating/plants_operating, "--", color="k", label="Средняя мощность реактора (МВт)")
ax1.plot( [1986,1986], [-150,900], "--", color="m")
ax1.plot( [2010,2010], [-150,900], "--", color="m")
ax1.text( 1986.5, 600, "Чернобыль", color="m")
ax1.text( 2010.5, 600, "Фукусима-1", color="m")
ax1.set_xlim( x_start, x_end)
ax1.set_ylim( -150,900)
ax1.set_ylabel("единиц")
ax1.grid(True)
ax1.legend(loc=0)

ax2.set_title("Ввод и вывод мощностей")
ax2.bar( years, MW_connected/100, 0.35, alpha=0.4, color="g", label="Ввод (x10)")
ax2.bar( years, -MW_disconnected/100, 0.35, alpha=0.4, color="r", label="Вывод (x10)")
ax2.plot( years, MW_operating/1000, "-", color="k", label="Рабочих мощностей")
ax2.plot( y, nuc, "-.", color="k", label="Выработка АЭС по данным ВР")
ax2.plot( y1, nuc1, "--", color="k", label="Выработка АЭС по данным WNA")
ax2.set_xlim(x_start, x_end)
#ax2.set_ylim( 0, 1500)
ax2.set_xlabel("Год")
ax2.set_ylabel("Гигаватт")
ax2.grid(True)
ax2.legend(loc=0)

plt.savefig( ".\\Graphs\\figure_12_09.png")
fig.show()

fig1 = plt.figure( figsize=(15,12))
fig1.suptitle( 'Распределение реакторов', fontsize=22)
gs = plt.GridSpec(2, 1, height_ratios=[1, 1]) 
ax1 = plt.subplot(gs[0])
ax2 = plt.subplot(gs[1])

ax1.set_title("По году ввода в эксплуатацию")
ax1.bar( Ages, RAges, 0.35, alpha=0.4, color="r", label="Всего: {:g}".format(np.sum(RAges)))
ax1.plot( Ages, PAges, "-", color="m", lw=3, label="Установленная мощность (ГВт)")
ax1.set_xlim( 1965, 2020)
ax1.set_ylim( 0,40)
ax1.set_xlabel("Год запуска")
ax1.set_ylabel("единиц")
ax1.legend(loc=0)
ax1.grid(True)

ax2.set_title("По установленной мощности")
ax2.bar( Powers+50, RPowers, 50, alpha=0.4, color="m", label="Средняя: {:.0f} МВт".format(np.average(Reactor_MW)))
ax2.set_xlim(0, 1750)
ax2.set_ylim( 0, 60)
ax2.set_xlabel("Мощность, МВт")
ax2.set_ylabel("единиц")
ax2.legend(loc=0)
ax2.grid(True)

plt.savefig( ".\\Graphs\\figure_12_10.png")
fig1.show()

