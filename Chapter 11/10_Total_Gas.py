from Utilities import *

def GetFile( data_name, sum_data_EIA, sum_well_HP, sum_well_HA, sum_well_P, sum_well_A, proj_name="Hughes2014"):
    bft2bmy = 0.3048**3 * 365
    Y,AEO2016 = Load_Calibration( data_name, "Year", "AEO2016") 
    Hughes,Actual = Load_Calibration( data_name, proj_name, "Actual")
    AEO2016 *= bft2bmy 
    Hughes *= bft2bmy
    Actual *= bft2bmy
    sp = int( Y[0] - 1994)
    for i in range( sp, len(sum_data_EIA)):
        sum_data_EIA[i] += AEO2016[i-sp]
        sum_well_HP[i] += Hughes[i-sp]
        sum_well_HA[i] += Actual[i-sp]
    WP,WA = Load_Calibration( data_name, "Wells_Plan", "Wells_Actual")
    if len(WP) < 1: return np.array( sum_well_HP)
    for i in range( sp, len(sum_data_EIA)):
        sum_well_P[i] += WP[i-sp]
        sum_well_A[i] += WA[i-sp]
    return np.array( sum_well_HP)

Year = np.linspace( 1994, 2040, 47)
sum_EIA = np.zeros( len( Year))
sum_HP = np.zeros( len( Year))
sum_HA = np.zeros( len( Year))
sum_WP = np.ones( len( Year)) * 20000
sum_WA = np.ones( len( Year)) * 20000
f1_Barnett = GetFile( "01_Barnett_Gas.csv", sum_EIA, sum_HP, sum_HA, sum_WP, sum_WA)
f2_Marcellus = GetFile( "02_Marcellus_Gas.csv", sum_EIA, sum_HP, sum_HA, sum_WP, sum_WA)
f3_Haynesville = GetFile( "03_Haynesville_Gas.csv", sum_EIA, sum_HP, sum_HA, sum_WP, sum_WA)
f4_EagleFord = GetFile( "04_EagleFord_Gas.csv", sum_EIA, sum_HP, sum_HA, sum_WP, sum_WA)
f5_Fayetteville = GetFile( "05_Fayetteville_Gas.csv", sum_EIA, sum_HP, sum_HA, sum_WP, sum_WA)
f6_Woodford = GetFile( "06_Woodford_Gas.csv", sum_EIA, sum_HP, sum_HA, sum_WP, sum_WA)
f7_Bakken = GetFile( "07_Bakken_Gas.csv", sum_EIA, sum_HP, sum_HA, sum_WP, sum_WA)
f8_Utica = GetFile( "08_Utica_Gas.csv", sum_EIA, sum_HP, sum_HA, sum_WP, sum_WA, proj_name="Yakimov2017")
f9_Others = GetFile( "09_Others_Gas.csv", sum_EIA, sum_HP, sum_HA, sum_WP, sum_WA)
for i in range( 6):
    sum_HP[i] += 19.6
    sum_HA[i] += 19.6

Y_BP = np.linspace( 1994, 2016, 23)
P_BP = np.array( [533.0,526.7,533.9,535.3,538.7,533.3,543.2,555.5,536.0,540.8,526.4,511.1,524.0,545.6,570.8,584.0,603.6,648.5,680.5,685.4,733.1,766.2,749.2])

Prepare_Russian_Font()
fig = plt.figure( figsize=(15,10))
fig.suptitle( 'Добыча "сланцевого" газа в США', fontsize=22)
gs = plt.GridSpec(2, 1, height_ratios=[2, 1]) 
ax1 = plt.subplot(gs[0])
ax2 = plt.subplot(gs[1])

ax1.plot( Y_BP, P_BP, "-", lw=3, color='r', label="Добыча в США всего (ВР)")
ax1.plot( Year, sum_EIA, "--", lw=2, color='r', label="AEO-2016 ({:.2f} 10¹² м³)".format(np.sum(sum_EIA)/1000))
ax1.plot( Year, sum_HP, "-", lw=3, color='m', label="Hughes ({:.2f} 10¹² м³)".format(np.sum(sum_HP)/1000))
ax1.plot( Year, f1_Barnett, "--", lw=1, color='k')
ax1.plot( Year, f2_Marcellus, "--", lw=1, color='k')
ax1.plot( Year, f3_Haynesville, "--", lw=1, color='k')
ax1.plot( Year, f4_EagleFord, "--", lw=1, color='k')
ax1.plot( Year, f5_Fayetteville, "--", lw=1, color='k')
ax1.plot( Year, f6_Woodford, "--", lw=1, color='k')
ax1.plot( Year, f7_Bakken, "--", lw=1, color='k')
ax1.plot( Year, f8_Utica, "--", lw=1, color='k')
ax1.errorbar( Year[:-24], sum_HA[:-24], yerr=sum_HA[:-24]*.05, fmt='o', color="k")
ax1.set_xlim( 1994, 2040)
ax1.set_ylim( 0, 1000)
ax1.set_ylabel("Млрд м³ в год")
ax1.grid(True)
ax1.set_title( "Добыча газа")
ax1.legend(loc=2)
ax1.annotate("Барнетт", xy=(2019.5, 6), xytext=(2030, 320), arrowprops=dict(facecolor='black', shrink=0.05))
ax1.annotate("Марцеллус", xy=(2019.5, 95), xytext=(2030, 360), arrowprops=dict(facecolor='black', shrink=0.05))
ax1.annotate("Хайнесвилль", xy=(2019.5, 190), xytext=(2030, 400), arrowprops=dict(facecolor='black', shrink=0.05))
ax1.annotate("Иглфорд", xy=(2019.5, 230), xytext=(2030, 440), arrowprops=dict(facecolor='black', shrink=0.05))
ax1.annotate("Файеттевилль", xy=(2019.5, 275), xytext=(2030, 480), arrowprops=dict(facecolor='black', shrink=0.05))
ax1.annotate("Вудфорд", xy=(2019.5, 300), xytext=(2030, 520), arrowprops=dict(facecolor='black', shrink=0.05))
ax1.annotate("Баккен", xy=(2019.5, 315), xytext=(2030, 560), arrowprops=dict(facecolor='black', shrink=0.05))
ax1.annotate("Ютика", xy=(2019.5, 353), xytext=(2030, 600), arrowprops=dict(facecolor='black', shrink=0.05))
ax1.annotate("Антрим/остальные", xy=(2019.5, 390), xytext=(2030, 640), arrowprops=dict(facecolor='black', shrink=0.05))
ax1.annotate("Реальная добыча ({:.2f} 10¹² м³)".format(np.sum(sum_HA[:-24])/1000), xy=(2011, 260), xytext=(1995, 400), arrowprops=dict(facecolor='black', shrink=0.05))

ax2.plot( Year, sum_WP/1000, "--", lw=3, color='r', label="По плану")
ax2.errorbar( Year[:-24], sum_WA[:-24]/1000, yerr=.1, fmt='o', color="k", label="Реальных")
ax2.set_xlim( 1994, 2040)
##ax2.set_ylim( 0, 35)
ax2.set_xlabel("Годы")
ax2.set_ylabel("Тысяч скважин")
ax2.grid(True)
ax2.set_title( "Количество скважин в эксплуатации")
ax2.legend(loc=0)

plt.savefig( ".\\Graphs\\figure_11_10.png")
fig.show()
