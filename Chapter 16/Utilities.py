import numpy as np
from scipy.integrate import odeint
import matplotlib as mpl
mpl.use('Qt5Agg')
import matplotlib.pyplot as plt
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
#
class Sigmoid( Control_Curve):
    # constructor
    def __init__( self, x0=0.0, s0=1.0, left=0.0, right=1.0, shift=0.0, s1=-999.0):
        self.Name = "Sigmoid"
        self.X0 = x0
        self.S0 = s0
        self.S1 = s1
        self.Left = left
        self.Right = right
        self.Shift = shift
        Control_Curve.__compute = self
        return
    
    # computation
    def Compute( self, x):
        x -= self.X0
        if self.S1 != -999.0 and x>0: x *= -self.S1
        else: x *= -self.S0
        if x < -500.0: return self.Right + self.Shift
        if x > 500.0: return self.Left + self.Shift
        e = np.exp( x)
        y = self.Left + (self.Right-self.Left)/(1.0+e) + self.Shift
        return y

    # plots data, together with optional external data
    def Plot( self, x1, x2, file_Name = "", coplot_x = -1, coplot_y = -1, no_screen = False):
        sy = "X0={0:.4f}".format( self.X0)
        sy += " S0={0:.4f}".format( self.S0)
        sy += " L={0:.4f}".format( self.Left)
        sy += " R={0:.4f}".format( self.Right)
        sy += " Sh={0:.4f}".format( self.Shift)
        Control_Curve.Plot( self, x1, x2, sy, "y", file_Name, coplot_x, coplot_y, no_screen) 
        return

#
# Defines a bathtub curve
# y(x) = Sigmoid1( x0, s0, left, middle) + Sigmoid2( x1, s1, 0, right-middle)
#
class Bathtub( Control_Curve):
    # constructor
    def __init__( self, x0=-1.0, s0=1.0, x1 = 1.0, s1=0.5, left=0.0, middle=1.0, right=0.0, shift=0.0):
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
# y(x) = peak * 4 * exp( - slope * (x-x0) / (1+exp(- slope * (x-x0))^2
#
class Hubbert( Control_Curve):
    # constructor
    def __init__( self, x0=0.0, s0=1.0, s1=0.5, peak= 1.0, shift=0.0):
        self.Name = "Hubbert"
        self.X0 = x0
        self.S0 = s0
        self.S1 = s1
        self.Peak = peak
        self.Shift = shift
        Control_Curve.__compute = self
        return
    
    # computation
    def Compute( self, x):
        x -= self.X0
        if x < 0.0: x *= -self.S0
        else: x *= -self.S1
        if x < -500.0: return self.Shift
        if x > 500.0: return self.Shift
        e = np.exp( x)
        y = 4.0 * self.Peak * e / (1+e) / (1+e) + self.Shift
        return y

    # plots data, together with optional external data
    def Plot( self, x1, x2, file_Name = "", coplot_x = -1, coplot_y = -1, no_screen = False):
        sy = "X0={0:.4f}".format( self.X0)
        sy += " S0={0:.4f}".format( self.S0)
        sy += " S1={0:.4f}".format( self.S1)
        sy += " Peak={0:.4f}".format( self.Peak)
        sy += " Shift={0:.4f}".format( self.Shift)
        Control_Curve.Plot( self, x1, x2, sy, "y", file_Name, coplot_x, coplot_y, no_screen)
        return

#
# Defines a Gauss curve
# y(x) = peak * exp( - slope * (x-x0)^2)
#
class Gauss( Control_Curve):
    # constructor
    def __init__( self, x0=0.0, s0=1.0, s1=0.5, peak= 1.0, shift=0.0):
        self.Name = "Gauss"
        self.X0 = x0
        self.S0 = s0
        self.S1 = s1
        self.Peak = peak
        self.Shift = shift
        Control_Curve.__compute = self
        return
    
    # computation
    def Compute( self, x):
        x -= self.X0
        if x < 0.0: s = self.S0
        else: s = self.S1
        x *= x
        x *= -s
        if x < -500.0: return self.Shift
        if x > 500.0: return self.Shift
        e = np.exp(x)
        y = self.Peak * e + self.Shift
        return y

    # plots data, together with optional external data
    def Plot( self, x1, x2, file_Name = "", coplot_x = -1, coplot_y = -1, no_screen = False):
        sy = "X0={0:.4f}".format( self.X0)
        sy += " S0={0:.4f}".format( self.S0)
        sy += " S1={0:.4f}".format( self.S1)
        sy += " Peak={0:.4f}".format( self.Peak)
        sy += " Shift={0:.4f}".format( self.Shift)
        Control_Curve.Plot( self, x1, x2, sy, "y", file_Name, coplot_x, coplot_y, no_screen)
        return

#
# Defines a Karpitsa curve
# y(x) = peak / (1 + (slope*(x0-x))^2)
#
class Kapitsa( Control_Curve):
    # constructor
    def __init__( self, x0=0.0, s0=1.0, s1=0.5, peak= 1.0, shift=0.0):
        self.Name = "Kapitsa"
        self.X0 = x0
        self.S0 = s0
        self.S1 = s1
        self.Peak = peak
        self.Shift = shift
        Control_Curve.__compute = self
        return
    
    # computation
    def Compute( self, x):
        x -= self.X0
        if x < 0.0: s = self.S0
        else: s = self.S1
        x *= x * s * s
        y = self.Peak / (x + 1.0) + self.Shift
        return y

    # plots data, together with optional external data
    def Plot( self, x1, x2, file_Name = "", coplot_x = -1, coplot_y = -1, no_screen = False):
        sy = "X0={0:.4f}".format( self.X0)
        sy += " S0={0:.4f}".format( self.S0)
        sy += " S1={0:.4f}".format( self.S1)
        sy += " Peak={0:.4f}".format( self.Peak)
        sy += " Shift={0:.4f}".format( self.Shift)
        Control_Curve.Plot( self, x1, x2, sy, "y", file_Name, coplot_x, coplot_y, no_screen)
        return
#
# Defines a Karpitsa integral curve
# "Успехи физических наук" 139(1) 57-71, РАН, 1996
# y(x) = K / tau * (0.5*pi - arctan((x0-x)/tau))
#
class KapitsaIntegral( Control_Curve):
    # constructor
    def __init__( self, x0=2007, K=186e3, tau=42):
        self.Name = "Kapitsa Integral"
        self.X0 = x0
        self.Tau = tau
        self.Peak = K
        Control_Curve.__compute = self
        return
    
    # computation
    def Compute( self, x):
        x -= self.X0
        y = np.pi*0.5 - np.arctan(-x/self.Tau)
        y *= self.Peak / self.Tau
        return y

    # plots data, together with optional external data
    def Plot( self, x1, x2, file_Name = "", coplot_x = -1, coplot_y = -1, no_screen = False):
        sy = "X0={0:.4f}".format( self.X0)
        sy += " K={0:.4f}".format( self.Peak)
        sy += " tau={0:.4f}".format( self.Tau)
        Control_Curve.Plot( self, x1, x2, sy, "y", file_Name, coplot_x, coplot_y, no_screen)
        return

#
# Defines a Weibull curve
# y(x) = B * k * ( B * (x-x0))^(k-1)) * exp(-( B * (x-x0))^(k)))
#
class Weibull( Control_Curve):
    # constructor
    def __init__( self, x0=0.0, b=1.0, k=2.0, peak=1.0, shift=0.0):
        self.Name = "Weibull"
        self.X0 = x0
        self.B = b
        self.K = k
        self.Peak = peak
        self.Shift = shift
        Control_Curve.__compute = self
        return
    
    # computation
    def Compute( self, x):
        x -= self.X0
        if x <= 0.0: return self.Shift
        x *= self.B
        p1 = x ** self.K
        p2 = p1 / x
        p1 = np.exp( -p1)
        y = self.Peak * self.B * self.K * p1 * p2 + self.Shift
        return y

    # plots data, together with optional external data
    def Plot( self, x1, x2, file_Name = "", coplot_x = -1, coplot_y = -1, no_screen = False):
        sy = "X0={0:.4f}".format( self.X0)
        sy += " B={0:.4f}".format( self.B)
        sy += " K={0:.4f}".format( self.K)
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
# Defines a moving average filter
#
def Filter( x, start=-1, end=-1, matrix = [1,2,1]):
    if start < 0: start = 0
    if end < 0: end = len( x)
    if end < start: end = start
    tmp = np.zeros(len(x))
    half_size = int(len( matrix)/2)
    for i in range( start):
        tmp[i] = x[i]
    for i in range( start, end):
        norm = 0.0
        for j in range( len( matrix)):
            k = i-half_size+j
            if k < 0: continue
            if k >= len( x): continue
            norm += matrix[j]
            tmp[i] += matrix[j] * x[k]
        tmp[i] /= norm
    for i in range( end, len(x)):
        tmp[i] = x[i]
    return tmp

#
# Loads data from a CSV file
#
def Load_Calibration( file_Name, var1_Name, var2_Name, separator=','):
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
            ss = s.split( separator)
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
# Loads data from a CSV file
#
def Load_Calibration_Text( file_Name, var1_Name, var2_Name, separator=','):
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
            ss = s.split( separator)
            if var1_Index < 0 or var2_Index < 0: 
                for j in range(len(ss)):
                    if ss[j] == var1_Name: var1_Index = j
                    if ss[j] == var2_Name: var2_Index = j
                #print( "Found: {0:s} - {1:g}, {2:s} - {3:g}".format( var1_Name, var1_Index, var2_Name, var2_Index)) 
                continue
            if var1_Index < 0 or var1_Index >= len(ss): continue
            if var2_Index < 0 or var2_Index >= len(ss): continue
            var1 += [ss[var1_Index]]
            var2 += [ss[var2_Index]]
    except:
        print ( "Error parsing file " + file_Name)
    fin.close()
    #print( var1)
    #print( var2)
    return var1, var2

#
# Provides interpolation as a linear combination
# of several Control_Curve functions
#
class Linear_Combo (Control_Curve):
    def __init__( self):
        self.Name = "Linear Combination"
        self.Wavelets = []
        return

    # computation
    def Compute( self, x):
        tmp = 0.0
        for w in self.Wavelets:
            tmp += w.Compute( x)
        return tmp

    # plots data, together with optional external data
    def Plot( self, x1, x2, file_Name = "", coplot_x = -1, coplot_y = -1, no_screen = False):
        sy = "{0:g} function(s)".format( len(self.Wavelets))
        Control_Curve.Plot( self, x1, x2, sy, "y", file_Name, coplot_x, coplot_y, no_screen)
        return

#
# Makes sure matplotlib can write in Russian
#
def Prepare_Russian_Font():
    font = {'family': 'Verdana',
        'weight': 'normal',
        'size': '16'}
    rc('font', **font)
    mpl.rcParams['figure.dpi'] = 80
    #print( mpl.get_backend())
    return

#
# Test code
#
Prepare_Russian_Font()
##F = Sigmoid()
##F.Plot( -10.0, 10.0)
##F = Bathtub()
##F.Plot( -10.0, 10.0)
##F = Hubbert()
##F.Plot( -10.0, 10.0)
##F = Gauss()
##F.Plot( -10.0, 10.0)
##F = Kapitsa()
##F.Plot( -10.0, 10.0)
##F = Weibull( x0=1968, b=0.015, k=2.2, peak=100)
##F.Plot( 1900, 2100)
