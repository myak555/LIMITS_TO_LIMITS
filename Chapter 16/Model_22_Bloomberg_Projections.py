from Predictions import *
from scipy.misc import imread
import matplotlib.cbook as cbook
import os

Bloomberg_Years = np.array( [2010, 2013, 2015, 2020, 2025, 2030])
Bloomberg_Hydro = np.array( [93.2,142.8,164.3,208.5,242.0,279.0])
Bloomberg_Nuclear = np.array( [61.5,92.6,135.0,175.6,217.5,246.7])
Bloomberg_Solar = np.array( [60.3,85.4,119.5,157.1,194.2,235.4])
Bloomberg_Wind = np.array( [42.4,46.0,65.7,69.9,71.7,87.8])
Bloomberg_GeoBio = np.array( [6.0,12.5,12.5,14.3,11.9,11.4]) 

BP_Years = np.linspace( 2009, 2017, 9)
BP_GeoBio = np.array( [7.3,5.3,6.1,5.8,6.6,5.4,6.1,7.8,4.9])
BP_Wind = np.array( [35.1,31.2,39.6,47.3,33.3,48.5,65.5,50.6,47.1])
BP_Solar = np.array( [8.1,16.5,31.8,29.4,36.6,40.8,48.8,75.9,96.8])
BP_Nuclear = np.array( [-1.4,3.6,-7.4,1.6,-1.4,4.1,5.5,7.4,0.3])
BP_Hydro = np.array( [34.2,34.1,30.6,33.0,44.5,38.4,34.8,37.8,22.4])

fig = plt.figure( figsize=(15,10))
fig.suptitle( 'Оценки Bloomberg по вводу мощностей ВИЭ', fontsize=22)
gs = plt.GridSpec(1, 1, height_ratios=[1]) 
ax1 = plt.subplot(gs[0])
x_start, x_end = 2008, 2031

#img = imread( cbook.get_sample_data( os.getcwd() + '/2018-2018.png'))
ax1.set_title('Bloomberg против экономического отдела "ВР"')
#ax1.imshow(img, zorder=0, extent=[2017, 2029, -960, 3000],  interpolation='nearest', aspect='auto')
ax1.bar( Bloomberg_Years, Bloomberg_Hydro-Bloomberg_Nuclear, 0.35, bottom=Bloomberg_Nuclear, alpha=0.4, color="b", label="ГЭС и ГАЭС")
ax1.bar( Bloomberg_Years, Bloomberg_Nuclear-Bloomberg_Solar, 0.35, bottom=Bloomberg_Solar, alpha=0.4, color="m", label="Ядерная")
ax1.bar( Bloomberg_Years, Bloomberg_Solar-Bloomberg_Wind, 0.35, bottom=Bloomberg_Wind, alpha=0.4, color="y", label="Солнечная")
ax1.bar( Bloomberg_Years, Bloomberg_Wind-Bloomberg_GeoBio, 0.35, bottom=Bloomberg_GeoBio, alpha=0.4, color="#000055", label="Ветровая")
ax1.bar( Bloomberg_Years, Bloomberg_GeoBio, 0.35, alpha=0.4, color="#005500", label="Гео, мусор и био")
ax1.plot( BP_Years, BP_GeoBio, "-", color="#005500", lw=3, label="Линии - реальные значения BP-2018")
ax1.plot( BP_Years, BP_Wind+BP_GeoBio, "-", color="#000055", lw=3)
ax1.plot( BP_Years, BP_Solar+BP_Wind+BP_GeoBio, "-", color="y", lw=3)
ax1.plot( BP_Years, BP_Nuclear+BP_Solar+BP_Wind+BP_GeoBio, "-", color="m", lw=3)
ax1.plot( BP_Years, BP_Hydro+BP_Nuclear+BP_Solar+BP_Wind+BP_GeoBio, "-", color="b", lw=3)
ax1.plot( [2014,2014], [0, 200], "--", color="k", lw=2)
ax1.text( 2014.2, 190, "Год прогноза")
ax1.set_xlim( x_start, x_end)
ax1.set_ylim( 0,300)
ax1.set_ylabel("ГВт увеличения установленных мощностей в год")
ax1.grid(True)
ax1.legend(loc=2)

plt.savefig( "./Graphs/figure_16_22.png")
fig.show()

