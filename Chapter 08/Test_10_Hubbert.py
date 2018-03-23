from Population import *

#
# Описывает производство минерального сырья по кривой Hабберта
#
class Resource_Hubbert:
    def __init__( self, Total=1200e3, t0=2025, sigma=0.039):
        self.Total = Total
        self.Function = Hubbert( t0, sigma, sigma, 1)
        return
    def Solve( self, t):
        self.Solution_Time = t
        self.Solution_Q = self.Function.GetVector( t)
        norm = self.Total/np.sum( self.Solution_Q)
        self.Solution_Q *= norm
        return self.Solution_Q

#
# Описывает производство минерального сырья по кривой Гаусса
#
class Resource_Gauss:
    def __init__( self, Total=1200e3, t0=2025, sigma=0.00030):
        self.Total = Total
        self.T0 = t0
        self.Sigma = sigma
        return
    def Solve( self, t):
        self.Solution_Time = t
        self.Solution_Q = t - self.T0
        self.Solution_Q *= -self.Sigma * self.Solution_Q
        self.Solution_Q = np.exp( self.Solution_Q)
        norm = self.Total/np.sum( self.Solution_Q)
        self.Solution_Q *= norm
        return self.Solution_Q

#
# Описывает производство минерального сырья по кривой Капицы
#
class Resource_Kapitsa:
    def __init__( self, Total=1200e3, t0=2025, sigma=0.030):
        self.Total = Total
        self.T0 = t0
        self.Sigma = sigma
        return
    def Solve( self, t):
        self.Solution_Time = t
        self.Solution_Q = self.Sigma * (self.T0 - t)
        self.Solution_Q *= self.Solution_Q
        self.Solution_Q = self.Sigma / (self.Solution_Q + 1)
        norm = self.Total/np.sum( self.Solution_Q)
        self.Solution_Q *= norm
        return self.Solution_Q

#
# Описывает производство минерального сырья по кривой Вейбулла
#
class Resource_Weibull:
    def __init__( self, Total=1200e3, t0=1897, sigma=0.007, k=3.5):
        self.Total = Total
        self.Function = Weibull( t0, sigma, k, Total)
        return
    def Solve( self, t):
        self.Solution_Time = t
        self.Solution_Q = self.Function.GetVector( t)
        norm = self.Total/np.sum( self.Solution_Q)
        self.Solution_Q *= norm
        return self.Solution_Q

T_Cal, Coal_Cal = Load_Calibration( "Energy_Calibration.csv", "Year", "Coal")
Oil_Cal, Gas_Cal = Load_Calibration( "Energy_Calibration.csv", "Oil", "Gas")
Oil_Cal += Coal_Cal
Gas_Cal += Oil_Cal

P0 = Population()
T = np.linspace( 1800, 2200, 401)
Q0 = Resource_Hubbert()
Q0_Data = Q0.Solve( T)
Q1 = Resource_Gauss()
Q1_Data = Q1.Solve( T)
Q2 = Resource_Kapitsa()
Q2_Data = Q2.Solve( T)
Q3 = Resource_Weibull()
Q3_Data = Q3.Solve( T)

fig = plt.figure( figsize=(15,10))
plt.plot( T, Q0_Data, "-", lw=1, color="r", label="Симметричная кривая Хабберта URR=1.20")
plt.plot( T, Q3_Data, "-", lw=1, color="g", label="Kривая Вейбулла URR=1.20")
plt.plot( T, Q1_Data, "-", lw=1, color="b", label="Kривая Гаусса URR=1.20")
plt.plot( T, Q2_Data, "--", lw=1, color="b", label="Kривая Капицы URR=1.20")
plt.errorbar( T_Cal, Coal_Cal, yerr=Coal_Cal*0.01, fmt='.', color="black", label="Кам. уголь (включая торф)")
plt.errorbar( T_Cal, Oil_Cal, yerr=Oil_Cal*0.01, fmt='.', color="g", label="+ Нефть (включая битум и жидкости)")
plt.errorbar( T_Cal, Gas_Cal, yerr=Gas_Cal*0.01, fmt='.', color="r", label="+ Природный газ")
plt.xlabel("Годы")
plt.xlim( 1800, 2100)
plt.ylabel("Добыча [миллионов toe в год]")
plt.ylim( 0, 13000)
plt.title( 'Аппроксимация мировой добычи углеводородного топлива')
plt.grid(True)
plt.legend(loc=0)
plt.savefig( ".\\Graphs\\figure_08_10.png")
fig.show()
