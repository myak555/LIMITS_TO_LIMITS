from Population import *

#
# Феноменологическая модель населения Великобритании
#
class Population_UK:
    def __init__( self):
        self.Functions = []
        self.Functions += [Sigmoid( 1945, 0.021, 20, 70.5)]
        self.Functions += [Hubbert( 2020, 0.20, 0.10, 5)]
        self.Functions += [Hubbert( 1972, 0.05, 0.17, 3.3)]
        self.Functions += [Hubbert( 1940, 0.4, 0.3, 5)]
        self.Functions += [Hubbert( 1911, 0.15, 0.10, 5)]
        self.Functions += [Hubbert( 1890, 0.10, 0.25, 4.5)]
        self.Functions += [Hubbert( 1841, 0.60, 0.10, 1.5)]
        return
    def Solve( self, t):
        self.Time = t
        self.Total = self.Functions[0].GetVector( t)
        for i in range( 1, len(self.Functions)):
            self.Total += self.Functions[i].GetVector( t)
        return self.Total

#
# Феноменологическая модель производства угля Великобританией
#
class Coal_UK:
    def __init__( self):
        self.Functions = []
        self.Functions += [Hubbert( 1920, 0.042, 0.055, 165)]
        self.Functions += [Hubbert( 2010, 0.8, 0.6, 3)]
        self.Functions += [Hubbert( 1980, 0.5, 0.13, 45)]
        self.Functions += [Hubbert( 1963, 1, 0.15, 25)]
        self.Functions += [Hubbert( 1954, 0.32, 0.13, 63)]
        return
    def Solve( self, t):
        self.Time = t
        self.Total = self.Functions[0].GetVector( t)
        for i in range( 1, len(self.Functions)):
            self.Total += self.Functions[i].GetVector( t)
        for i in range( 1, len(self.Time)):
            if self.Time[i] < 2017: continue
            self.Total[i] = 0.0
        self.URR = np.sum( self.Total) 
        return self.Total

#
# Феноменологическая модель потребления угля Великобританией
#
class Coal_UK_Cons:
    def __init__( self):
        self.Functions = []
        self.Functions += [Hubbert( 1920, 0.042, 0.055, 165)]
        self.Functions += [Hubbert( 2012, 0.8, 0.6, 32)]
        self.Functions += [Hubbert( 2006, 0.3, 0.8, 27)]
        self.Functions += [Hubbert( 1988, 0.8, 0.2, 25)]
        self.Functions += [Hubbert( 1980, 0.5, 0.13, 28)]
        self.Functions += [Hubbert( 1963, 1, 0.15, 25)]
        self.Functions += [Hubbert( 1954, 0.32, 0.11, 63)]
        self.Functions += [Hubbert( 1938, 1, 1, 15)]
        return
    def Solve( self, t):
        self.Time = t
        self.Total = self.Functions[0].GetVector( t)
        for i in range( 1, len(self.Functions)):
            self.Total += self.Functions[i].GetVector( t)
        for i in range( 1, len(self.Time)):
            if self.Time[i] < 2018: continue
            self.Total[i] = 0.0
        self.URR = np.sum( self.Total) 
        return self.Total

#
# Феноменологическая модель производства нефти Великобританией
#
class Oil_UK:
    def __init__( self):
        self.Functions = []
        self.Functions += [Hubbert( 1979, 1, 0.45, 60)]
        self.Functions += [Hubbert( 1985.5, 0.48, 0.3, 118)]
        self.Functions += [Hubbert( 1995, 0.7, 0.15, 105)]
        self.Functions += [Hubbert( 1999, 1.2, 0.9, 35)]
        self.Functions += [Hubbert( 2003, 1, 0.8, 25)]
        self.Functions += [Hubbert( 2008, 1, 0.4, 25)]
        self.Functions += [Hubbert( 2017, 0.8, 0.4, 35)]
        return
    def Solve( self, t):
        self.Time = t
        self.Total = self.Functions[0].GetVector( t)
        for i in range( 1, len(self.Functions)):
            self.Total += self.Functions[i].GetVector( t)
        self.URR = np.sum( self.Total) 
        return self.Total

#
# Феноменологическая модель потребления нефти Великобританией
#
class Oil_UK_Cons:
    def __init__( self):
        self.Functions = []
        self.Functions += [Hubbert( 1944, 0.5, 0.1, 20)]
        self.Functions += [Hubbert( 1973, 0.18, 0.6, 103)]
        self.Functions += [Hubbert( 1979, 0.6, 0.1, 83)]
        self.Functions += [Hubbert( 1982, 1, 1, -12)]
        self.Functions += [Hubbert( 1992, 0.5, 0.05, 26)]
        self.Functions += [Hubbert( 1998, 0.5, 1, 10)]
        self.Functions += [Hubbert( 2007, 0.3, 0.1, 42)]
        self.Functions += [Hubbert( 2017, 0.8, 0.4, 14)]
        return
    def Solve( self, t):
        self.Time = t
        self.Total = self.Functions[0].GetVector( t)
        for i in range( 1, len(self.Functions)):
            self.Total += self.Functions[i].GetVector( t)
        self.URR = np.sum( self.Total) 
        return self.Total

#
# Феноменологическая модель производства газа Великобританией
#
class Gas_UK:
    def __init__( self):
        self.Functions = []
        self.Functions += [Hubbert( 2000.5, 0.3, 0.2, 94)]
        self.Functions += [Hubbert( 1977, 0.33, 0.14, 34)]
        self.Functions += [Hubbert( 1987, 1, 0.7, 12)]
        self.Functions += [Hubbert( 1992, 1, 0.9, 10)]
        self.Functions += [Hubbert( 2008, 1, 0.4, 5)]
        self.Functions += [Hubbert( 2017, 0.8, 0.4, 28)]
        return
    def Solve( self, t):
        self.Time = t
        self.Total = self.Functions[0].GetVector( t)
        for i in range( 1, len(self.Functions)):
            self.Total += self.Functions[i].GetVector( t)
        self.URR = np.sum( self.Total) 
        return self.Total

#
# Феноменологическая модель потребления газа Великобританией
#
class Gas_UK_Cons:
    def __init__( self):
        self.Functions = []
        self.Functions += [Hubbert( 2001, 0.2, 0.1, 96)]
        self.Functions += [Hubbert( 1973, 1, 1, 5)]
        self.Functions += [Hubbert( 1979, 0.3, 0.2, 40)]
        self.Functions += [Hubbert( 1986, 1, 0.7, 9)]
        self.Functions += [Hubbert( 2008, 1, 0.4, 5)]
        self.Functions += [Hubbert( 2017, 0.8, 0.4, 8)]
        return
    def Solve( self, t):
        self.Time = t
        self.Total = self.Functions[0].GetVector( t)
        for i in range( 1, len(self.Functions)):
            self.Total += self.Functions[i].GetVector( t)
        self.URR = np.sum( self.Total) 
        return self.Total

#
# Феноменологическая модель потребления ядерной энергии Великобританией
#
class Nuc_UK_Cons:
    def __init__( self):
        self.Functions = []
        self.Functions += [Sigmoid( 1985, 0.15, 0, 22.5)]
        self.Functions += [Hubbert( 1968, 0.8, 0.2, 4.5)]
        self.Functions += [Hubbert( 1993, 1, 1, 2)]
        self.Functions += [Hubbert( 1997, 1, 0.5, 4)]
        self.Functions += [Hubbert( 2000, 1, 1, -4)]
        self.Functions += [Hubbert( 2008, 0.9, 2, -9)]
        self.Functions += [Hubbert( 2010, 1.5, 2, -5)]
        self.Functions += [Hubbert( 2014, .7, .6, -8)]
        return
    def Solve( self, t):
        self.Time = t
        self.Total = self.Functions[0].GetVector( t)
        for i in range( 1, len(self.Functions)):
            self.Total += self.Functions[i].GetVector( t)
        self.URR = np.sum( self.Total) 
        return self.Total

#
# Феноменологическая модель потребления гидро энергии Великобританией
#
class Hydro_UK_Cons:
    def __init__( self):
        self.Functions = []
        self.Functions += [Sigmoid( 1850, 0.1, 0, 1.1)]
        return
    def Solve( self, t):
        self.Time = t
        self.Total = self.Functions[0].GetVector( t)
        for i in range( 1, len(self.Functions)):
            self.Total += self.Functions[i].GetVector( t)
        self.URR = np.sum( self.Total) 
        return self.Total

#
# Феноменологическая модель потребления остальной возобновляемой энергии Великобританией
#
class Renewable_UK_Cons:
    def __init__( self):
        self.Functions = []
        self.Functions += [Sigmoid( 2018, 0.26, 0, 50)]
        self.Functions += [Hubbert( 2005, 1, 1, 1)]
        self.Functions += [Hubbert( 2020, 1, 1, -3)]
        return
    def Solve( self, t):
        self.Time = t
        self.Total = self.Functions[0].GetVector( t)
        for i in range( 1, len(self.Functions)):
            self.Total += self.Functions[i].GetVector( t)
        self.URR = np.sum( self.Total) 
        return self.Total

T0, Pop = Load_Calibration( "UK_Population_and_Energy.csv", "Year", "population")
P1 = Population_UK()
P1.Solve( np.linspace( 1800, 2100, 301))

C_Coal, C_Oil = Load_Calibration( "UK_Population_and_Energy.csv", "coal_cons", "oil_cons")
C_Gas, P_Coal = Load_Calibration( "UK_Population_and_Energy.csv", "gas_cons", "coal_prod")
P_Oil, P_Gas = Load_Calibration( "UK_Population_and_Energy.csv", "oil_prod", "gas_prod")
C_Nuc, C_Hyd = Load_Calibration( "UK_Population_and_Energy.csv", "nuclear", "hydro")
C_Ren, C_Tot = Load_Calibration( "UK_Population_and_Energy.csv", "other_renew", "other_renew")

C0 = Coal_UK_Cons()
C0.Solve( np.linspace( 1800, 2100, 301))
C1 = Oil_UK_Cons()
C1.Solve( np.linspace( 1800, 2100, 301))
C2 = Gas_UK_Cons()
C2.Solve( np.linspace( 1800, 2100, 301))
C3 = Nuc_UK_Cons()
C3.Solve( np.linspace( 1800, 2100, 301))
C4 = Hydro_UK_Cons()
C4.Solve( np.linspace( 1800, 2100, 301))
C5 = Renewable_UK_Cons()
C5.Solve( np.linspace( 1800, 2100, 301))

Prepare_Russian_Font()
fig = plt.figure( figsize=(15,10))
plt.plot( C3.Time, C3.Total, "-", lw=2, color="m", label="Потребление ядерной энергии (модель)")
plt.plot( C4.Time, C4.Total, "-", lw=2, color="b", label="Потребление гидро энергии (модель)")
plt.plot( C5.Time, C5.Total, "-", lw=2, color="y", label="Потребление возобновляемой кроме гидро")
plt.errorbar( T0, C_Nuc, yerr=1, fmt='.', color="m", label="Выработка ядерной энергии (BP)")
plt.errorbar( T0, C_Hyd, yerr=1, fmt='.', color="b", label='Выработка гидро энергии (BP)')
plt.errorbar( T0, C_Ren, yerr=1, fmt='.', color="y", label="Возобновляемые кроме гидро")
plt.xlabel("Годы")
plt.xlim( 1850, 2100)
plt.ylabel("Миллионов тонн нефтяного эквивалента")
plt.ylim( 0, 50)
plt.title( 'Потребление ядерной и возобновляемой энергии Великобританией')
plt.grid(True)
plt.legend(loc=0)
plt.savefig( ".\\Graphs\\figure_12_04.png")
fig.show()
