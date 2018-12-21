from Predictions import *

Reactor_Shutdown = Linear_Combo()
Reactor_Shutdown.Wavelets += [Hubbert( x0=2035.000, s0=0.30586, s1=0.46300, peak=31.700)]
Reactor_Shutdown.Wavelets += [Sigmoid( x0=2053.000, s0=0.64954, left=0.000, right=10.000)]
Reactor_Shutdown.Wavelets += [Hubbert( x0=2050.000, s0=0.33832, s1=0.34093, peak=5.469)]

# Needed for phenomenological model later
_Nuclear_Functions = Linear_Combo()
_Nuclear_Functions.Wavelets += [Weibull( 1968, .015, 2.2, 45000)]
_Nuclear_Functions.Wavelets += [Sigmoid( 2060, .05, 0, 1550)]
_Nuclear_Functions.Wavelets += [Hubbert( 2039, 0.3, 0.1, -370)]
_Nuclear_Functions.Wavelets += [Hubbert( 2012, 0.5, 0.1, -200)]

years = np.linspace(1800, 2300, 501)
MW_connected = np.zeros( len(years))
f_start = open("./Data/Nuclear_Reactor_Commissioning.txt")
for i in range(1000):
    s = f_start.readline()
    if len(s) <= 0: break
    ss = s.split("MW(e)")
    n = int(s[0:4])
    ss1 = ss[0].split('(')
    w = float( ss1[-1])
    MW_connected[n-1800] += w/1000
f_start.close()
prd = 10
growth = 1.02
for i in range(219,len(years)):
    MW_connected[i] += prd
    prd *= growth

MW_disconnected = np.zeros( len(years))
f_end = open("./Data/Nuclear_Reactor_Shutdown.txt")
for i in range(1000):
    s = f_end.readline()
    if len(s) <= 0: break
    ss = s.split("MW(e)")
    n = int(s[0:4])
    ss1 = ss[0].split('(')
    w = float( ss1[-1])
    MW_disconnected[n-1800] += w/1000
f_end.close()
for i in range(219,270):
    MW_disconnected[i] += Reactor_Shutdown.Compute(years[i])
for i in range(270,len(years)):
    MW_disconnected[i] += MW_connected[i-50]

w = 0
MW_operating = np.zeros( len(years))
for i in range( len(years)):
    w += MW_connected[i]
    w -= MW_disconnected[i]
    if w < 0:
        w = 0
        MW_disconnected[i] = 0
    MW_operating[i] = w
    #print( "{:g}\t{:.0f}\t{:.0f}\t{:.0f}".format(years[i],
    #    MW_connected[i],MW_disconnected[i],w/1000))

Production = MW_operating * 0.77
Pop = Population().UN_Medium.GetVector( years)

y, nuc = Load_Calibration("Energy_Calibration.csv", "Year", "Nuclear")
nuc *= 4419.2 / 24 / 365.25
for i in range(len(y)):
    j = int(y[i]-years[0])
    if j<0: continue
    Production[j] = nuc[i]

x_start, x_end = 1950, 2150

fig = plt.figure( figsize=(15,10))
fig.suptitle( 'Гражданские генерирующие мощности ядерной энергетики', fontsize=22)
gs = plt.GridSpec(2, 1, height_ratios=[2,1]) 
ax1 = plt.subplot(gs[0])
ax2 = plt.subplot(gs[1])

ax1.set_title("Ввод и вывод мощностей")
ax1.bar( years, MW_connected*10, 1, alpha=0.4, color="g", label="Ввод (x10)")
ax1.bar( years, -MW_disconnected*10, 1, alpha=0.4, color="r", label="Вывод (x10)")
ax1.bar( years[:219], MW_connected[:219]*10, 1, alpha=1, color="g")
ax1.bar( years[:219], -MW_disconnected[:219]*10, 1, alpha=1, color="r")
ax1.plot( years, MW_operating, "-", color="k", label="Рабочих мощностей")
ax1.errorbar( y, nuc, yerr=nuc*0.03, fmt=".", color="m", label="Выработка АЭС по данным ВР")
ax1.plot( years, Production, "--", color="m", label="Выработка АЭС (модель)")
#ax1.plot( years, _Nuclear_Functions.GetVector(years)*0.39/31.6*42, "--", color="y", label="Phenomenological Model")
ax1.set_xlim(x_start, x_end)
ax1.set_ylim( -400, 1000)
ax1.text( 2030, 50, "Рост/снижение по {:.1f}% в год".format((growth-1)*100))
ax1.set_ylabel("Гигаватт")
ax1.grid(True)
ax1.legend(loc=0)

ax2.set_title("Мощность на душу населения")
ax2.plot( years, Production*1000/Pop, "-", color="m")
ax2.set_xlim(x_start, x_end)
ax2.set_ylim( 0, 60)
ax2.set_xlabel("год")
ax2.set_ylabel("Ватт(электрич.)")
ax2.grid(True)

plt.savefig( ".\\Graphs\\figure_12_11.png")
fig.show()
