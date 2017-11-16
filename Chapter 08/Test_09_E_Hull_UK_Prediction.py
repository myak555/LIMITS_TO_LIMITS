from Population import *

Calibration_Year, Calibration_Total = Load_Calibration( "UK_Coal_Production.csv", "Year", "Total")
Calibration_Total, Calibration_Delta = Load_Calibration( "UK_Coal_Production.csv", "Total", "Delta")
URR0 = np.sum(Calibration_Total)
dURR = np.sum(Calibration_Delta)
Prediction_Year = [1830,1860,1880,1900,1920,1940,1960,1980,2000,2020,2034]
Prediction_Total = [30,72,144,288,576,1152,2304,4608,9216,18432,42979]

T = np.linspace( 1800, 2100, 301)
Q1 = Hubbert( 1924,0.043,0.040,280,0).GetVector(T)
URR1 = np.sum( Q1)
Q2 = Weibull( total=26500, x0=1810, s=0.0078, k=3.4).GetVector(T)
URR2 = np.sum( Q2)

Prepare_Russian_Font()
fig = plt.figure( figsize=(15,10))
plt.plot( Prediction_Year, Prediction_Total, "--", color="r", lw=2, label="Предсказание Эдварда Халла 1861 г: 79'843 млн тонн")
plt.plot( T, Q1, "-", color="g", lw=2, label="Кривая Хабберта: {:5.0f} млн тонн".format(URR1))
plt.plot( T, Q2, "-", color="r", lw=2, label="Кривая Вейбулла: {:5.0f} млн тонн".format(URR2))
plt.errorbar( Calibration_Year, Calibration_Total, yerr=Calibration_Delta, fmt='.', color="b", label="Реальная добыча 1830-2015: {:5.0f} +/- {:5.0f} млн тонн".format(URR0, dURR))
plt.xlabel("Годы")
plt.xlim( 1800, 2050)
plt.ylabel("Добыча [миллионов тонн в год]")
plt.ylim( 0, 600)
plt.title( "Добыча угля в Великобритании")
plt.grid(True)
plt.legend(loc=0)
plt.savefig( ".\\Graphs\\figure_08_09.png")
fig.show()
