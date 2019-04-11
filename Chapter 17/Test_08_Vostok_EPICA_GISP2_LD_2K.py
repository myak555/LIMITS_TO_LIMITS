from Utilities import *

class AgeTemp():
    def __init__(self, a, t):
        self.a = a
        self.t = t

def GetData( filename):
    Age, T_Pub = Load_Calibration( "./Climate_Proxy/" + filename, "Age_Pub", "Temp_Pub", separator="\t")
    Depth, Proxy = Load_Calibration( "./Climate_Proxy/" + filename, "Depth", "Proxy", separator="\t")
    if not np.all(np.diff(Age) > 0):
        print( "Age not increasing: " + filename)
        return
    Age = 1950 - Age
    A1 = []
    D1 = []
    T1 = []
    for i in range(len(Age)):
        if Age[i] < 0: continue
        A1 += [ Age[i]]
        D1 += [ Depth[i]]
        T1 += [ T_Pub[i]]
    A1 = np.array(A1)
    T1 = np.array(T1)
    ResolutionD = (A1[-1]-A1[0])/(D1[0]-D1[-1])
    ResolutionT = (A1[0]-A1[-1])/ (len(T1)+1)
    print( "{:s}, ages: {:.0f} to {:.0f}, Resolution: {:.1f} y/cm, {:.1f} y/point".format( filename, Age[-1], Age[0], ResolutionD, ResolutionT))
    print( "   min {:.1f}, max {:.1f}, average {:.1f}, stdev {:.1f}".format( min(T1), max(T1), np.average(T1), np.std(T1)))
    return A1, T1, ResolutionT, np.average(T1)
  
filenames = []
filenames += ["011_Moose Lake.txt"]
filenames += ["023_Composite_MD01-2421.txt"]
filenames += ["023b_Composite_KR02-06.txt"]
filenames += ["023c_Composite_KR02-06 StA.txt"]
filenames += ["034_Lake 850.txt"]
filenames += ["035_Lake Nujulla.txt"]
filenames += ["043_Homestead Scarp.txt"]
filenames += ["044_Mount Honey.txt"]
filenames += ["058_Flarken Lake.txt"]
filenames += ["059_Tsuolbmajavri Lake.txt"]
filenames += ["067b_Agassiz & Renland.txt"]

shifts = []
shifts += [0.3]
shifts += [0.7]
shifts += [0.3]
shifts += [0.7]
shifts += [0.4]
shifts += [0.0]
shifts += [-0.1]
shifts += [0.1]
shifts += [0.1]
shifts += [0.1]
shifts += [0.0]

scales = np.ones( len(filenames))
scales[-1] = 0.3

Ages = []
Temperatures = []
Age_Errors = []
Averages = []
for f in filenames:
    a, t, rt, at = GetData( f) 
    Ages += [a]
    Temperatures += [t]
    Age_Errors += [rt/3]
    Averages += [at]

AT = []
for i in range( len(filenames)):
    Ao = Ages[i]
    To = (Temperatures[i]-Averages[i]+shifts[i])*scales[i]
    for j in range(len(To)):
        AT += [ AgeTemp( Ao[j],To[j])]
AT = sorted( AT, key=lambda x: x.a)
A2 = []
T2 = []
for i in range( len(AT)):
    A2 += [AT[i].a]
    T2 += [AT[i].t]
A3 = np.linspace( 0, 2000, 2001)
T3 = np.interp(A3, np.array(A2), np.array(T2))
T3 = Filter(T3, matrix=np.ones(101))

Frozen_Thames = [1408, 1435, 1506, 1514, 1537, 1565,
                 1595, 1608, 1621, 1635, 1649, 1655,
                 1663, 1666, 1677, 1684, 1695, 1709,
                 1716, 1740, 1768, 1776, 1785, 1788,
                 1795, 1814]

filename1 = "./Climate_Proxy/LD_CA_Correlation.txt"
Y_CE, T_CE = Load_Calibration( filename1, "Year", "CE_Year_Average", separator="\t")
Y_LD, T_LD = Load_Calibration( filename1, "Year", "LD_d18O", separator="\t")
Y_CE = Y_CE[:360]
T_CE = T_CE[:360]
Y_LD = Y_LD[23:]
T_LD = T_LD[23:]+31
T_CE40 = Filter(T_CE, matrix=np.ones(41))
T_CE_Baseline = np.average(T_CE[128:259])
T_LD40 = Filter(T_LD, matrix=np.ones(41))

limits = 0, 2030
fig = plt.figure( figsize=(15,15))
gs = plt.GridSpec(2, 1, height_ratios=[2,1]) 
ax1 = plt.subplot(gs[0])
ax2 = plt.subplot(gs[1])

ax1.set_title('Температурные прокси из статьи Marcott et al, 2013', fontsize=22)
for i in range( len(filenames)):
    if i == 10:
        ax1.errorbar( Ages[i], Temperatures[i]-12, xerr=Age_Errors[i], yerr=1, alpha=0.5, fmt=".", label=filenames[i])
    else:
        ax1.errorbar( Ages[i], Temperatures[i], xerr=Age_Errors[i], yerr=1, alpha=0.5, fmt=".", label=filenames[i])
ax1.errorbar( Y_CE, T_CE, yerr=0.1, alpha=0.2, fmt="o", color="k", label="Центральная Англия")
ax1.set_xlim( limits)
ax1.set_ylim( -15, 20)
ax1.set_yticks( [-10, 0, 10])
ax1.set_ylabel("[ºЦ]")
ax1.legend(loc=3)
ax1.grid(True)

for i in range( len(filenames)):
    alp = 0.3
    l = 2
    if i==0 or i==10:
        alp = 1
    ax2.plot( Ages[i], (Temperatures[i]-Averages[i]+shifts[i])*scales[i], "-", lw=l, alpha=alp)
ax2.plot( Y_CE, T_CE40-T_CE_Baseline, "-", lw=3, color="k", alpha=1, label="Центральная Англия (41-точечный фильтр)")
#ax2.plot( Y_LD, T_LD40-8.8, "-", lw=3, color="y", alpha=1, label="Law Dome (41-точечный фильтр)")
for ft in Frozen_Thames:
    ax2.plot( [ft, ft], [2,1], "-", lw=3, alpha=0.3, color="b")
ax2.text( Frozen_Thames[0]+100, 2.1, "Лёд на Темзе", color="b", fontsize=10)
for y in range(985,1455,5):
    ax2.plot( [y, y], [2,1.7], "-", lw=3, alpha=0.3, color="g")
ax2.text( 985, 2.1, "Викинги в Гренландии", color="g", fontsize=10)
for y in range(475,805,5):
    ax2.plot( [y, y], [2,1.5], "-", lw=3, alpha=0.3, color="k")
ax2.text( 475, 2.1, "Тёмные века", color="k", fontsize=10)
#ax2.plot( A3, T3, "--", lw=4, color="r", alpha=1, label="Усреднение прокси")
ax2.set_xlim( limits)
ax2.set_ylim( -2,2)
ax2.set_ylabel("Аномалия [ºЦ]")
ax2.legend(loc=0)
ax2.grid(True)
ax2.set_xlabel("год")

plt.savefig( ".\\Graphs\\figure_17_08.png")
fig.show()
