import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint
from matplotlib import rc

#
# defines basic limit function
#
def Limit( y, min_y=0, max_y=1):
    if y < min_y: return min_y
    if y > max_y: return max_y
    return y

#
# performs a division, controlling the b to be non-zero
#
def Divide_Non_Zero( a, b, min_b=1e-6):
    if b >= min_b: return a/b
    return a/min_b

#
# defines basic round function
#
def Round( y, factor=1e-6):
    y = np.floor( y / factor)
    return y * factor

#
# defines a curve with plotting cpability
#
class Control_Curve:
    # constructor
    def __init__( self):
        self.Name = "No name"
        self.__compute = 0

    # computation
    def Compute( self, x):
        if self.__compute == 0: return x
        else: return self.__compute.Compute( x)

    # computation with limits
    def Compute_Limit( self, x, min=0.0, max=1.0):
        y = self.Compute( x)
        return Limit( y, min, max)

    # calculates a numpy vector of given vector x
    def GetVector( self, x):
        y = np.linspace(0, 1.0, len(x))
        for i in range( len(x)):
            y[i] = self.Compute( x[i])
        return y

    # plots data, together with optional external data
    def Plot( self, x1, x2, x_axis = "x", y_axis = "y", file_Name = "", coplot_x = -1, coplot_y = -1, no_screen = False):
        x = np.linspace(x1, x2, 301)
        y = self.GetVector( x)
        if coplot_x != -1 and coplot_y != -1: plt.plot( x, y, "-", coplot_x, coplot_y, "r+", lw=2, ms=7, mew=2)
        else: plt.plot( x, y, "-", lw=2, ms=7, mew=2)
        plt.xlabel(x_axis)
        plt.ylabel(y_axis)
        plt.title( self.Name + " curve: " + file_Name)
        plt.grid(True)
        if file_Name != "": plt.savefig( file_Name + ".png")
        if not no_screen: plt.show()
        plt.clf()
        return

#
# Defines a sigmoid curve
# y(x) = left + (right-left)/(1+exp(-slope*(x-x0))) + shift
# or a generalized sigmoid:
# y(x) = left + (right-left)/(c0+c1*exp(-slope*(x-x0)))**(1/skew) + shift
#
class Sigmoid( Control_Curve):
    # constructor
    def __init__( self, x0=0.0, s0=1.0, left=0.0, right=1.0, shift=0.0, c0=1, c1=1, skew=1):
        self.Name = "Sigmoid"
        self.X0 = x0
        self.S0 = s0
        self.Left = left
        self.Right = right
        self.Shift = shift
        self.C0 = c0
        self.C1 = c1
        self.Skew = skew
        Control_Curve.__compute = self
        return
    
    # computation
    def Compute( self, x):
        e = np.exp( -self.S0*(x-self.X0))
        e = (self.C0 + self.C1*e) ** (-1/self.Skew)
        y = self.Left + (self.Right-self.Left) * e + self.Shift
        return y

    # plots data, together with optional external data
    def Plot( self, x1, x2, file_Name = "", coplot_x = -1, coplot_y = -1, no_screen = False):
        sy = "X0={0:.4f}".format( self.X0)
        sy += " S0={0:.4f}".format( self.S0)
        sy += " L={0:.4f}".format( self.Left)
        sy += " R={0:.4f}".format( self.Right)
        sy += " Sh={0:.4f}".format( self.Shift)
        sy += " C0={0:.4f}".format( self.C0)
        sy += " C1={0:.4f}".format( self.C1)
        sy += " Skew={0:.4f}".format( self.Skew)
        Control_Curve.Plot( self, x1, x2, sy, "y", file_Name, coplot_x, coplot_y, no_screen) 
        return

#
# Defines a bathtub curve
# y(x) = Sigmoid1( x0, s0, left, middle) + Sigmoid2( x1, s1, 0, right-middle)
#
class Bathtub( Control_Curve):
    # constructor
    def __init__( self, x0=-1.0, s0=1.0, x1 = 1.0, s1=1.0, left=0.0, middle=1.0, right=0.0, shift=0.0):
        self.Name = "Bathtub"
        self.X0 = x0
        self.X1 = x1
        self.S0 = s0
        self.S1 = s1
        self.Left = left
        self.Middle = middle
        self.Right = right
        self.Shift = shift
        Control_Curve.__compute = self
        return
    
    # computation
    def Compute( self, x):
        s1 = Sigmoid( self.X0, self.S0, self.Left, self.Middle)
        s2 = Sigmoid( self.X1, self.S1, 0.0, self.Right-self.Middle)
        y = s1.Compute(x) + s2.Compute(x) + self.Shift
        return y

    # plots data, together with optional external data
    def Plot( self, x1, x2, file_Name = "", coplot_x = -1, coplot_y = -1, no_screen = False):
        sy = "X0={0:.4f}".format( self.X0)
        sy += " S0={0:.4f}".format( self.S0)
        sy += " X1={0:.4f}".format( self.X1)
        sy += " S1={0:.4f}".format( self.S1)
        sy += " L={0:.4f}".format( self.Left)
        sy += " M={0:.4f}".format( self.Middle)
        sy += " R={0:.4f}".format( self.Right)
        sy += " Sh={0:.4f}".format( self.Shift)
        Control_Curve.Plot( self, x1, x2, sy, "y", file_Name, coplot_x, coplot_y, no_screen) 
        return

#
# Defines a Hubbert curve
# y(x) = shift + peak * 4 * exp( - slope * (x-x0)) / (1+exp(- slope * (x-x0))**2
# or a generalized Hubbert curve
# y(x) = shift + peak * exp( - slope*(x-x0)) / skew * [(C0+C1)/(C0+C1*exp(- slope*(x-x0))]**(1+1/skew)
#
class Hubbert( Control_Curve):
    # constructor
    def __init__( self, x0=0.0, s0=1.0, s1=1.0, peak= 1.0, shift=0.0, c0=1, c1=1, skew=1):
        self.Name = "Hubbert"
        self.X0 = x0
        self.S0 = s0
        self.S1 = s1
        self.Peak = peak
        self.Shift = shift
        self.C0 = c0
        self.C1 = c1
        self.Skew = skew
        Control_Curve.__compute = self
        return
    
    # computation
    def Compute( self, x):
        n = 1/self.Skew+1
        x -= self.X0
        P0 = self.Peak * self.C1 * ((1 + self.Skew) ** n) / self.Skew
        if x < 0.0: x *= self.S0
        else: x *= self.S1
        e0 = np.exp( -x)
        e1 = (self.C0 + self.C1*e0) ** n
        y = P0 * e0 / e1 + self.Shift
        return y

    # plots data, together with optional external data
    def Plot( self, x1, x2, file_Name = "", coplot_x = -1, coplot_y = -1, no_screen = False):
        sy = "X0={0:.4f}".format( self.X0)
        sy += " S0={0:.4f}".format( self.S0)
        sy += " S1={0:.4f}".format( self.S1)
        sy += " Peak={0:.4f}".format( self.Peak)
        sy += " Shift={0:.4f}".format( self.Shift)
        sy += " C0={0:.4f}".format( self.C0)
        sy += " C1={0:.4f}".format( self.C1)
        sy += " Skew={0:.4f}".format( self.Skew)
        Control_Curve.Plot( self, x1, x2, sy, "y", file_Name, coplot_x, coplot_y, no_screen)
        return

#
# Defines a Weibull curve
# y(x) = s * k * (s * (x-x0))**(k-1) * exp( - s * (x-x0)**k
#
class Weibull( Control_Curve):
    # constructor
    def __init__( self, x0=0.0, s=1.0, k=2.0, total= 1.0, shift=0.0):
        self.Name = "Weibull"
        self.X0 = x0
        self.S = s
        self.K = k
        self.Total = total
        self.Shift = shift
        Control_Curve.__compute = self
        return
    
    # computation
    def Compute( self, x):
        x -= self.X0
        if x < 0.0: return 0.0
        x *= self.S
        xk1 = x ** (self.K-1)
        e = np.exp( -xk1*x)
        y = self.Total * self.S * self.K * xk1 * e
        return y + self.Shift

    # plots data, together with optional external data
    def Plot( self, x1, x2, file_Name = "", coplot_x = -1, coplot_y = -1, no_screen = False):
        sy = "X0={0:.4f}".format( self.X0)
        sy += " S={0:.4f}".format( self.S)
        sy += " K={0:.4f}".format( self.K)
        sy += " Total={0:.4f}".format( self.Total)
        sy += " Shift={0:.4f}".format( self.Shift)
        Control_Curve.Plot( self, x1, x2, sy, "y", file_Name, coplot_x, coplot_y, no_screen)
        return

#
# Defines a time delay feature, corresponding to World3 implementation
#
def Delay():
    # constructor
    def __init__( self, delay=10, default_value = 0.0):
        self.Name = "Delay"
        self.Chain = np.ones( delay) * default_value
        return

    # Sets a value into the chain; pushes chain up
    def Set_Value( self, val):
        self.Chain = np.roll( self.Chain, 1)
        self.Chain[0] = val
        return

    def Get_Value( self):
        L = len(self.Chain)-1
        return self.Chain[L]

#
# Loads data from a CSV file
#
def Load_Calibration( file_Name, var1_Name, var2_Name):
    fin = open( file_Name)
    var1_Index = -1
    var2_Index = -1
    var1 = []
    var2 = []
    try:
        for i in range( 1000000):
            s = fin.readline()
            if len(s) <= 0: break
            if s.startswith( "#"): continue
            s = s.strip()
            ss = s.split( ",")
            if var1_Index < 0 or var2_Index < 0: 
                for j in range(len(ss)):
                    if ss[j] == var1_Name: var1_Index = j
                    if ss[j] == var2_Name: var2_Index = j
                #print( "Found: {0:s} - {1:g}, {2:s} - {3:g}".format( var1_Name, var1_Index, var2_Name, var2_Index)) 
                continue
            if var1_Index < 0 or var1_Index >= len(ss): continue
            if var2_Index < 0 or var2_Index >= len(ss): continue
            v1 = float( ss[var1_Index])
            v2 = float( ss[var2_Index])
            var1 += [v1]
            var2 += [v2]
    except:
        print ( "Error parsing file " + file_Name)
    fin.close()
    #print( var1)
    #print( var2)
    return np.array( var1), np.array( var2)

#
# Makes sure matplotlib can write in Russian
#
def Prepare_Russian_Font():
    font = {'family': 'Verdana',
        'weight': 'normal',
        'size': '16'}
    rc('font', **font)
    return
