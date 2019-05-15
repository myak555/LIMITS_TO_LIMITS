from Utilities import *
import scipy.stats as stat

def Plot_Raw( filename):
    print( "Processing " + filename)
    Age, T_Pub, Depth, Proxy, Age_M09, Age_error = Load_Calibration(
        "./Climate_Proxy/" + filename,
        ["Age_Pub", "Temp_Pub", "Depth", "Proxy", "Age_Marine09", "Age_error"], separator="\t")
    if not np.all(np.diff(Age) > 0):
        print( "Age not increasing: " + filename)
        return
    resolution = (Age[-1]-Age[0]) / (Depth[-1]-Depth[0])
    aver = np.average(T_Pub)
    Age_Corr = np.linspace( Age_M09[0], Age_M09[-1], 50)
    T_Corr = np.interp( Age_Corr, Age_M09, T_Pub, left=aver, right=aver)
    Age_Error_Corr = np.average(Age_error)

    fig = plt.figure( figsize=(15,15))
    fig.suptitle("Raw data: " + filename, fontsize=36)
    ax1 = plt.subplot(212)
    ax1.margins(0)           # Default margin is 0.05, value 0 means fit
    ax2 = plt.subplot(221)
    ax3 = plt.subplot(222)

    age_limits = int( -max(Age))+1950, 2020
    limits = [min(T_Corr), max(T_Corr)]
    younger_drias = [1950-12900, 1950-11700]
    HCO = [1950-9000, 1950-5000]
    ax1.set_title('Temperature', fontsize=22)
    ax1.errorbar( 1950-Age, T_Pub, xerr=Age_error, yerr=1, alpha=0.5, fmt=".", color="r", label="As published")
    ax1.errorbar( 1950-Age_M09, T_Pub, xerr=Age_error, yerr=1, alpha=0.5, fmt=".", color="b", label="Authors shifted")
    ax1.plot( 1950-Age_Corr, T_Corr, "--", lw=3, color="k")
    if younger_drias[1] > age_limits[0]:
        ax1.plot( [younger_drias[0],younger_drias[0]], limits, "-.", lw=2, color="y")
        ax1.plot( [younger_drias[1],younger_drias[1]], limits, "-.", lw=2, color="y")
        ax1.text( younger_drias[0]+20, limits[0], "Y.Dryas", color="y")
    ax1.plot( [HCO[0],HCO[0]], limits, "-.", lw=2, color="r")
    ax1.plot( [HCO[1],HCO[1]], limits, "-.", lw=2, color="r")
    ax1.text( HCO[0]+20, limits[0], "HCO", color="r")
    ax1.plot( [-250,-250], limits, "-.", lw=2, color="g")
    ax1.plot( [400,400], limits, "-.", lw=2, color="g")
    ax1.text( -250+20, limits[0], "RWP", color="g")
    ax1.plot( [1300,1300], limits, "-.", lw=2, color="b")
    ax1.plot( [1870,1870], limits, "-.", lw=2, color="b")
    ax1.text( 1300+20, limits[0], "LIA", color="b")
    ax1.set_xlim( age_limits)
    ax1.set_xlabel("Year (-BC/+AD)")
    ax1.set_ylabel("[ºC]")
    ax1.grid(True)

    ax2.set_title('Age ( {:.1f} year(s)/cm)'.format(resolution), fontsize=22)
    ax2.errorbar( -Age, -Age_M09, xerr=Age_error, yerr=Age_error, alpha=0.5, fmt=".", color="g")
    reg = stat.linregress(-Age, -Age_M09)
    ends = np.array([-Age[0], -Age[-1]])
    ax2.plot( ends, reg.slope*ends + reg.intercept, "--", color="k", label="{:.3f}x{:+.1f}".format(reg.slope, reg.intercept))
    ax2.set_ylabel("Age (authors shifted)")
    ax2.set_xlabel("Age (source)")
    ax2.legend(loc=0)
    ax2.grid(True)

    ax3.set_title('Proxy', fontsize=22)
    ax3.errorbar( Proxy, T_Pub, yerr=1, alpha=0.5, fmt=".", color="g")
    reg = stat.linregress( Proxy, T_Pub)
    ends = np.array([ min( Proxy), max(Proxy)])
    ax3.plot( ends, reg.slope*ends + reg.intercept, "--", color="k", label="{:.3f}x{:+.1f}".format(reg.slope, reg.intercept))
    ax3.set_xlabel("Proxy value (source)")
    ax3.set_ylabel("[ºC] (source)")
    ax3.legend(loc=0)
    ax3.grid(True)
    plt.savefig( "./Climate_Graphs/{:s}".format(filename.replace(".txt", ".png")))
    #fig.show()
    plt.close('all')

filenames = []

filenames += ["001_GeoB5844-2.txt"]
filenames += ["002_ODP-1019D.txt"]
filenames += ["003_SO136-GC11.txt"]
filenames += ["004_JR51GC-35.txt"]
filenames += ["005_ME005A-43JC.txt"]
filenames += ["006_MD95-2043.txt"]
filenames += ["007_M39-008.txt"]
filenames += ["008_MD95-2011.txt"]
filenames += ["009_ODP 984.txt"]
filenames += ["010_GeoB 7702-3.txt"]
filenames += ["011_Moose Lake.txt"]
filenames += ["012_ODP 658C.txt"]
filenames += ["013_Composite_MD95-2011.txt"]
filenames += ["013b_Composite_HM79-4.txt"]
filenames += ["014_IOW225517.txt"]
filenames += ["015_IOW225514.txt"]
filenames += ["016_M25_4-KL11.txt"]
filenames += ["017_ODP 1084B.txt"]
filenames += ["018_AD91-17.txt"]
filenames += ["019_74KL.txt"]
filenames += ["020_74KL.txt"]
filenames += ["021_NIOP-905.txt"]
filenames += ["022_NIOP-905.txt"]
filenames += ["023_Composite_MD01-2421.txt"]
filenames += ["023b_Composite_KR02-06.txt"]
filenames += ["023c_Composite_KR02-06 StA.txt"]
filenames += ["024_GeoB 3910.txt"]

filenames += ["025_Dome C, Antarctica.txt"]

filenames += ["026_GeoB 7139-2.txt"]

filenames += ["027_Dome F, Antarctica.txt"]
filenames += ["027b_Dome F, Antarctica.txt"]

filenames += ["028_18287-3.txt"]
filenames += ["029_GeoB 1023-5.txt"]
filenames += ["030_GeoB 5901-2.txt"]
filenames += ["031_KY07_04_01.txt"]
filenames += ["032_Hanging Lake.txt"]
filenames += ["033_GeoB 3313-1.txt"]
filenames += ["034_Lake 850.txt"]
filenames += ["035_Lake Nujulla.txt"]
filenames += ["036_PL07-39PC.txt"]
filenames += ["037_MD02-2529.txt"]
filenames += ["038_MD98-2165.txt"]
filenames += ["039_MD79-257.txt"]
filenames += ["040_BJ8 13GGC.txt"]
filenames += ["041_BJ8 70GGC.txt"]
filenames += ["042_MD95-2015.txt"]
filenames += ["043_Homestead Scarp.txt"]
filenames += ["044_Mount Honey.txt"]
filenames += ["045_GeoB 10038-4.txt"]
filenames += ["046_TN05-17.txt"]
filenames += ["047_MD97-2120.txt"]
filenames += ["048_MD97-2121.txt"]
filenames += ["049_17940.txt"]

filenames += ["050_Vostok, Antarctica.txt"]

filenames += ["051_D13822.txt"]
filenames += ["052_M35003-4.txt"]
filenames += ["053_OCE326-GGC26.txt"]
filenames += ["054_OCE326-GGC30.txt"]
filenames += ["055_CH07-98-GGC19.txt"]
filenames += ["056_GIK23258-2.txt"]
filenames += ["057_GeoB 6518-1.txt"]
filenames += ["058_Flarken Lake.txt"]
filenames += ["059_Tsuolbmajavri Lake.txt"]
filenames += ["060_MD01-2390.txt"]

##filenames += ["061_EDML.txt"]

filenames += ["062_MD98-2176.txt"]
filenames += ["063_MD98-2181.txt"]
filenames += ["064_A7.txt"]
filenames += ["065_RAPID-12-1K.txt"]
filenames += ["066_NP04-KH3, -KH4.txt"]

filenames += ["067_Agassiz & Renland.txt"]
filenames += ["067b_Agassiz & Renland.txt"]

filenames += ["068_GeoB6518-1.txt"]
filenames += ["069_MD03-2707.txt"]
filenames += ["070_GeoB 3129.txt"]
filenames += ["071_GeoB 4905.txt"]
filenames += ["072_MD01-2378.txt"]
filenames += ["073_MD02-2575.txt"]

for f in filenames:
    Plot_Raw( f)
