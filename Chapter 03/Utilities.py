import sys
import numpy as np
from scipy.integrate import odeint
import matplotlib as mpl
if sys.platform.lower().startswith('win'):
    mpl.use('Qt5Agg')
    #print("Windows detected!")
import matplotlib.pyplot as plt
from matplotlib import rc

def Limit( y, min_y=0, max_y=1):
    """
    Basic limit function: crops value from min_y to max_y
    """
    if y < min_y: return min_y
    if y > max_y: return max_y
    return y

def Divide_Non_Zero( a, b, min_b=1e-6):
    """
    Performs a division, controlling the divisor to be non-zero
    """
    if b >= min_b: return a/b
    return a/min_b

class Control_Curve:
    """
    Base class for various modeling functions
    """
    def __init__( self):
        self.Name = "No name"
        self.__compute = None
        return
    def Compute( self, x):
        """
        Computes single value from variable x
        """
        if self.__compute is None: return x
        else: return self.__compute.Compute( x)
    def Compute_Cropped( self, x, min_y=0.0, max_y=1.0):
        """
        Computation with cropping
        """
        y = self.Compute( x)
        return Limit( y, min_y, max_y)
    def GetVector( self, x):
        """
        Calculates a numpy vector of given argument vector x
        """
        y = np.zeros(len(x))
        for i, vx in enumerate(x):
            y[i] = self.Compute( vx)
        return y
    def GetVector_Cropped( self, x, min_y=0.0, max_y=1.0):
        """
        Calculates a numpy vector of given argument vector x, crops to min_y, max_y
        """
        y = self.GetVector( x)
        return np.crop( y, min_y, max_y)
    def GetVector_Normalized( self, x, norm=1.0):
        """
        Calculates a numpy vector of given argument vector x, performs normalization
        """
        y = self.GetVector( x)
        n = np.sum( y)
        if -1e-6 < n and n < 1e-6: return y
        y *= norm / n
        return y * norm / n
    def GetVector_Integrated( self, x, norm=None, leftSum=0.0):
        """
        Calculates a numpy vector of given argument vector x,
        performs normalization and running summation
        """
        if norm is None:
            y = self.GetVector( x)
        else:
            y = self.GetVector_Normalized( x, norm)
        y[0] += leftSum
        for i in range( 1, len(y)):
            y[i] += y[i-1]
        return y
    def Plot( self, x1, x2, x_axis = "x", y_axis = "y",
              file_Name = None,
              coplot_x = None,
              coplot_y = None,
              no_screen = False):
        """
        Plots data, together with optional external curves
        """
        x = np.linspace(x1, x2, 301)
        y = self.GetVector( x)
        fig = plt.figure( figsize=(15,10))
        plt.xlabel(x_axis)
        plt.ylabel(y_axis)
        plt.grid(True)
        if (coplot_x is None) or (coplot_y is None):
            plt.plot( x, y, "-", lw=2, ms=7, mew=2)
        else: 
            plt.plot( x, y, "-", coplot_x, coplot_y, "r+", lw=2, ms=7, mew=2)
        plt.xlim( x1, x2)
        if not file_Name is None:
            plt.title( self.Name + " curve: " + file_Name)
            plt.savefig( file_Name + ".png")
        else:
            plt.title( self.Name + " curve")            
        if not no_screen: fig.show()
        else: plt.close("all")
        return

class Sigmoid( Control_Curve):
    """
    Defines a sigmoid curve
    y(x) = left + (right-left)/(1+exp(-slope*(x-x0))) + shift
    """
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
    def Compute( self, x):
        x -= self.X0
        if self.S1 != -999.0 and x>0: x *= -self.S1
        else: x *= -self.S0
        if x < -500.0: return self.Right + self.Shift
        if x > 500.0: return self.Left + self.Shift
        e = np.exp( x)
        y = self.Left + (self.Right-self.Left)/(1.0+e) + self.Shift
        return y
    def Plot( self, x1, x2, file_Name = None, coplot_x = None, coplot_y = None, no_screen = False):
        sx = "X₀={:g}, σ₀={:g}".format( self.X0, self.S0)
        sy = "L={:g}, R={:g}, Sh={:g}".format( self.Left, self.Right, self.Shift)
        Control_Curve.Plot( self, x1, x2, sx, sy, file_Name, coplot_x, coplot_y, no_screen) 
        return

class Bathtub( Control_Curve):
    """
    Defines a bathtub curve
    y(x) = Sigmoid1( x0, s0, left, middle) + Sigmoid2( x1, s1, 0, right-middle)
    """
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
    def Compute( self, x):
        s1 = Sigmoid( self.X0, self.S0, self.Left, self.Middle)
        s2 = Sigmoid( self.X1, self.S1, 0.0, self.Right-self.Middle)
        y = s1.Compute(x) + s2.Compute(x) + self.Shift
        return y
    def Plot( self, x1, x2, file_Name = None, coplot_x = None, coplot_y = None, no_screen = False):
        sx  = "X₀={:g}, σ₀={:g}, ".format( self.X0, self.S0)
        sx += "X₁={:g}, σ₁={:g}".format( self.X1, self.S1)
        sy = "L={:g}, ".format( self.Left)
        sy += " M={:g},".format( self.Middle)
        sy += " R={:g}".format( self.Right)
        sy += " Sh={:g}".format( self.Shift)
        Control_Curve.Plot( self, x1, x2, sx, sy, file_Name, coplot_x, coplot_y, no_screen) 
        return

class Hubbert( Control_Curve):
    """
    Defines a Hubbert curve
    y(x) = peak * 4 * exp( - slope * (x-x0) / (1+exp(- slope * (x-x0))^2
    """
    def __init__( self, x0=0.0, s0=1.0, s1=0.5, peak= 1.0, shift=0.0):
        self.Name = "Hubbert"
        self.X0 = x0
        self.S0 = s0
        self.S1 = s1
        self.Peak = peak
        self.Shift = shift
        Control_Curve.__compute = self
        return
    def Compute( self, x):
        x -= self.X0
        if x < 0.0: x *= -self.S0
        else: x *= -self.S1
        if x < -500.0: return self.Shift
        if x > 500.0: return self.Shift
        e = np.exp( x)
        y = 4.0 * self.Peak * e / (1+e) / (1+e) + self.Shift
        return y
    def Plot( self, x1, x2, file_Name = None, coplot_x = None, coplot_y = None, no_screen = False):
        sx = "X₀={:g}, σ₀={:g}, σ₁={:g}".format( self.X0, self.S0, self.S1)
        sy = "Peak={:g}, Sh={:g}".format( self.Peak, self.Shift)
        Control_Curve.Plot( self, x1, x2, sx, sy, file_Name, coplot_x, coplot_y, no_screen) 
        return

class GenHubbert( Control_Curve):
    """
    Defines a generalized Hubbert curve
    y(x) = peak * 4 * exp( - slope * gamma * (x-x0) / (1+exp(- slope * gamma * (x-x0))^(1/gamma + 1)
    """
    def __init__( self, x0=0.0, s0=1.0, gamma=1.0, peak= 1.0, shift=0.0):
        self.Name = "Generalized Hubbert"
        self.X0 = x0
        self.S0 = s0
        self.Gamma = gamma
        self.Peak = peak
        self.Shift = shift
        Control_Curve.__compute = self
        return
    def Compute( self, x):
        x -= self.X0
        x *= -self.S0
        x *= self.Gamma
        if x < -500.0: return self.Shift
        if x > 500.0: return self.Shift
        e = np.exp( x)
        y = 4.0 * self.Peak * e / ((1+e) ** (1+1/self.Gamma)) + self.Shift
        return y
    def Plot( self, x1, x2, file_Name = None, coplot_x = None, coplot_y = None, no_screen = False):
        sx = "X₀={:g}, σ₀={:g}, γ={:g}".format( self.X0, self.S0, self.Gamma)
        sy = "Peak={:g}, Sh={:g}".format( self.Peak, self.Shift)
        Control_Curve.Plot( self, x1, x2, sx, sy, file_Name, coplot_x, coplot_y, no_screen) 
        return

class Gauss( Control_Curve):
    """
    Defines a Gauss curve
    y(x) = peak * exp( - slope * (x-x0)^2)
    """
    def __init__( self, x0=0.0, s0=1.0, s1=0.5, peak= 1.0, shift=0.0):
        self.Name = "Gauss"
        self.X0 = x0
        self.S0 = s0
        self.S1 = s1
        self.Peak = peak
        self.Shift = shift
        Control_Curve.__compute = self
        return
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
    def Plot( self, x1, x2, file_Name = None, coplot_x = None, coplot_y = None, no_screen = False):
        sx = "X₀={:g}, σ₀={:g}, σ₁={:g}".format( self.X0, self.S0, self.S1)
        sy = "Peak={:g}, Sh={:g}".format( self.Peak, self.Shift)
        Control_Curve.Plot( self, x1, x2, sx, sy, file_Name, coplot_x, coplot_y, no_screen) 
        return

class Kapitsa( Control_Curve):
    """
    Defines a Karpitsa curve
    'Успехи физических наук' 139(1) 57-71, РАН, 1996
    y(x) = peak / (1 + (slope*(x0-x))^2)
    """
    def __init__( self, x0=0.0, s0=1.0, s1=0.5, peak= 1.0, shift=0.0):
        self.Name = "Kapitsa"
        self.X0 = x0
        self.S0 = s0
        self.S1 = s1
        self.Peak = peak
        self.Shift = shift
        Control_Curve.__compute = self
        return
    def Compute( self, x):
        x -= self.X0
        if x < 0.0: s = self.S0
        else: s = self.S1
        x *= x * s * s
        y = self.Peak / (x + 1.0) + self.Shift
        return y
    def Plot( self, x1, x2, file_Name = None, coplot_x = None, coplot_y = None, no_screen = False):
        sx = "X₀={:g}, σ₀={:g}, σ₁={:g}".format( self.X0, self.S0, self.S1)
        sy = "Peak={:g}, Sh={:g}".format( self.Peak, self.Shift)
        Control_Curve.Plot( self, x1, x2, sx, sy, file_Name, coplot_x, coplot_y, no_screen) 
        return

class KapitsaIntegral( Control_Curve):
    """
    Defines a Karpitsa integral curve
    'Успехи физических наук' 139(1) 57-71, РАН, 1996
    y(x) = K / tau * (0.5*pi - arctan((x0-x)/tau))
    """
    def __init__( self, x0=2007, K=186e3, tau=42, shift=0.0):
        self.Name = "Kapitsa Integral"
        self.X0 = x0
        self.Tau = tau
        self.Peak = K
        self.Shift = shift
        Control_Curve.__compute = self
        return
    def Compute( self, x):
        x -= self.X0
        y = np.pi*0.5 - np.arctan(-x/self.Tau)
        y *= self.Peak / self.Tau
        return y + self.Shift
    def Plot( self, x1, x2, file_Name = None, coplot_x = None, coplot_y = None, no_screen = False):
        sx = "X₀={:g}, τ={:g}".format( self.X0, self.Tau)
        sy = "K={:g}, Sh={:g}".format( self.Peak, self.Shift)
        Control_Curve.Plot( self, x1, x2, sx, sy, file_Name, coplot_x, coplot_y, no_screen) 
        return

class Weibull( Control_Curve):
    """
    Defines a Weibull curve
    y(x) = B * k * ( B * (x-x0))^(k-1)) * exp(-( B * (x-x0))^(k)))
    """
    def __init__( self, x0=0.0, b=1.0, k=2.0, peak=1.0, shift=0.0):
        self.Name = "Weibull"
        self.X0 = x0
        self.B = b
        self.K = k
        self.Peak = peak
        self.Shift = shift
        Control_Curve.__compute = self
        return
    def Compute( self, x):
        x -= self.X0
        if x <= 0.0: return self.Shift
        x *= self.B
        p1 = x ** self.K
        p2 = p1 / x
        p1 = np.exp( -p1)
        y = self.Peak * self.B * self.K * p1 * p2 + self.Shift
        return y
    def Plot( self, x1, x2, file_Name = None, coplot_x = None, coplot_y = None, no_screen = False):
        sx = "X₀={:g}, B={:g}".format( self.X0, self.B)
        sy = "K={:g}, Sh={:g}".format( self.K, self.Shift)
        Control_Curve.Plot( self, x1, x2, sx, sy, file_Name, coplot_x, coplot_y, no_screen) 
        return

class Gompertz( Control_Curve):
    """
    Defines a Gompertz curve
    y(x) = sigma * gamma * Q0 * exp(-sigma*exp(-gamma*(x-x0)))) * exp(-gamma*(x-x0))
    """
    def __init__( self, x0=0.0, sigma=1.0, gamma=1.0, peak=1.0, shift=0.0):
        self.Name = "Gompertz"
        self.X0 = x0
        self.Sigma = sigma
        self.Gamma = gamma
        self.Peak = peak
        self.Shift = shift
        Control_Curve.__compute = self
        return
    def Compute( self, x):
        x -= self.X0
        x *= -self.Gamma
        e = np.exp( x)
        e2 = np.exp( -self.Sigma*e)
        y = self.Peak * self.Sigma * self.Gamma * e * e2 
        return y + self.Shift
    def Plot( self, x1, x2, file_Name = None, coplot_x = None, coplot_y = None, no_screen = False):
        sx = "X₀={:g}, σ={:g}, γ={:g}".format( self.X0, self.Sigma, self.Gamma)
        sy = "Peak={:g}, Sh={:g}".format( self.Peak, self.Shift)
        Control_Curve.Plot( self, x1, x2, sx, sy, file_Name, coplot_x, coplot_y, no_screen) 
        return

class GompertzIntegral( Control_Curve):
    """
    Defines a Gompertz integral curve
    y(x) = Q0 * exp(-sigma*exp(-gamma*(x-x0))))
    """
    def __init__( self, x0=0.0, sigma=1.0, gamma=1.0, peak=1.0, shift=0.0):
        self.Name = "Gompertz Integral"
        self.X0 = x0
        self.Sigma = sigma
        self.Gamma = gamma
        self.Peak = peak
        self.Shift = shift
        Control_Curve.__compute = self
        return
    def Compute( self, x):
        x -= self.X0
        x *= -self.Gamma
        e = np.exp( x)
        e2 = np.exp( -self.Sigma*e)
        y = self.Peak * e2 
        return y + self.Shift
    def Plot( self, x1, x2, file_Name = None, coplot_x = None, coplot_y = None, no_screen = False):
        sx = "X₀={:g}, σ={:g}, γ={:g}".format( self.X0, self.Sigma, self.Gamma)
        sy = "Peak={:g}, Sh={:g}".format( self.Peak, self.Shift)
        Control_Curve.Plot( self, x1, x2, sx, sy, file_Name, coplot_x, coplot_y, no_screen) 
        return

class Linear_Combo (Control_Curve):
    """
    Provides interpolation as a linear combination
    of several Control_Curve functions
    """
    def __init__( self):
        self.Name = "Linear Combination"
        self.Wavelets = []
        return
    def Compute( self, x):
        tmp = 0.0
        for w in self.Wavelets:
            tmp += w.Compute( x)
        return tmp
    def Plot( self, x1, x2, file_Name = None, coplot_x = None, coplot_y = None, no_screen = False):
        sy = "{0:d} function(s)".format( len(self.Wavelets))
        Control_Curve.Plot( self, x1, x2, sy, "y", file_Name, coplot_x, coplot_y, no_screen)
        return

class Markov_Chain:
    """
    Defines Markov chain filter
    taus - number of characteristic delays
    """
    def __init__( self, taus, Years, Year0, time_shift=0):
        self.Years = Years
        self.Year0 = Year0
        self.Filter = self.GetRho(taus[0])
        offset = int( self.Year0 - self.Years[0]) 
        for tau in taus[1:]:
            self.Filter = np.convolve( self.Filter, self.GetRho(tau))[offset:offset+len(self.Years)]
        self.Filter = np.roll( self.Filter, time_shift)
        self.Filter /= np.sum(self.Filter)
        return        
    def GetRho(self, tau):
        Time = self.Years - self.Year0
        tmp = np.exp( -Time/tau)
        for i, y in enumerate(self.Years):
            if y >= self.Year0: break
            tmp[i] = 0.0
        norm = np.sum( tmp)
        return tmp/norm

def Delay():
    """
    Defines a time delay feature, corresponding to World3 implementation
    """
    def __init__( self, delay=10, default_value = 0.0):
        self.Name = "Delay"
        self.Chain = np.ones( delay) * default_value
        return
    def Set_Value( self, val):
        """
        Puts a value into the chain; pushes chain up
        """
        self.Chain = np.roll( self.Chain, 1)
        self.Chain[0] = val
        return
        """
        Retrieves a value from the chain
        """
    def Get_Value( self):
        return self.Chain[-1]

def Filter( x, start=-1, end=-1, matrix = [1,2,1]):
    """
    Defines a moving average filter
    """
    if start < 0: start = 0
    if end < 0: end = len( x)
    if end < start: end = start
    tmp = np.zeros(len(x))
    half_size = int(len( matrix)/2)
    tmp[:start] = x[:start] 
    for i in range( start, end):
        norm = 0.0
        for j, m in enumerate( matrix):
            k = i-half_size+j
            if k < 0: continue
            if k >= len( x): continue
            norm += m
            tmp[i] += m * x[k]
        tmp[i] /= norm
    tmp[end:] = x[end:]
    return tmp

def FilterN( x, start=-1, end=-1, N=3):
    """
    Defines a moving average filter with a simple unity matrix of length n
    """
    return Filter( x, start, end, np.ones(N))

def Cumulative( x, x0=0.0):
    """
    Returns a cumulative array
    """
    tmp = np.array(x)
    tmp[0] += x0
    for i in range( 1, len(tmp)):
        tmp[i] += tmp[i-1]
    return tmp

def Decimate( x, n):
    """
    Decimates an array using moving filter method
    """
    tmp1 = FilterN(x, N=n+n+1)
    tmp2 = []
    for i in range( 0, len(tmp1), n):
        tmp2 += [tmp1[i]]
    return np.array( tmp2)

def ArrayMerge( a, b):
    """
    Merges two arrays (either numpy or sets)
    Returns a numpy array
    """
    tmp = []
    for ia in a: tmp += [ia]
    for ib in b: tmp += [ib]
    return np.array( tmp)

def Strings_To_Array( Strings):
    """
    Converts strings into an array
    """
    tmp = []
    for s in Strings:
        try:
            d = float(s)
            tmp += [d]
        except:
            tmp += [0.0]
            print("Warning: float conversion error, value {:s}".format(s))
            continue
    return np.array( tmp)

def Load_Calibration( file_Name, var_Names, separator=',', verbose=False):
    """
    Loads data from a CSV file
    """
    dataStrings = Load_Calibration_Text( file_Name, var_Names, separator, verbose)
    tmp = ()
    for ds in dataStrings:
        tmp_d = Strings_To_Array( ds)
        tmp += (tmp_d,)
    return tmp

def Load_Calibration_Text( file_Name, var_Names, separator=',', verbose=False):
    """
    Loads text data from a CSV file
    """
    if verbose:
        print( "Parsing file: {:s}".format( file_Name)) 
    fin = open( file_Name)
    var_Found = []
    var_Indexes = []
    data_Arrays = []
    try:
        while True:
            s = fin.readline()
            if len(s) <= 0: break
            s = s.strip()
            if s.startswith( "#"): continue
            ss = s.split( separator)
            for n in var_Names:
                if not n in ss: continue
                for position, nf in enumerate(ss):
                    if nf != n: continue
                    var_Found += [ n]
                    var_Indexes += [position]
                    data_Arrays += [[]]
                    if verbose:
                        print( '   Found: variable "{:s}" at position {:d}'.format( n, position)) 
            break
        while True:
            s = fin.readline()
            if len(s) <= 0: break
            if s.startswith( "#"): continue
            s = s.strip()
            ss = s.split( separator)
            for i, position in enumerate(var_Indexes):
                if position >= len(ss): continue 
                data_Arrays[i] += [ss[position]]
    except:
        print ( "Error parsing file " + file_Name)
    fin.close()
    tmp = ()
    for i, n in enumerate( var_Found):
        d = data_Arrays[i]
        tmp += (d,)
        if verbose:
            print( '   Variable "{:s}" has {:d} rows'.format( n, len(d))) 
    return tmp

def Prepare_Russian_Font():
    """
    Makes sure matplotlib can write in Russian
    """
    # Use system default font
    #font = {'family': 'Verdana',
    font = { 'weight': 'normal',
        'size': '16'}
    rc('font', **font)
    mpl.rcParams['figure.dpi'] = 80
    if __name__ == "__main__":
        print( "Backend detected: {:s}".format( mpl.get_backend()))
    return

#
# Automatically sets Russian code for all users of Utility
# Comment out if Russian font not needed
#
Prepare_Russian_Font()
InteractiveModeOn = not ('-t' in sys.argv)

#
# Test code
#
if __name__ == "__main__":
    help( Limit)
    help( Divide_Non_Zero)
    help( Control_Curve)
    help( Sigmoid)
    help( Bathtub)
    help( Hubbert)
    help( GenHubbert)
    help( Gauss)
    help( Kapitsa)
    help( KapitsaIntegral)
    help( Weibull)
    help( Gompertz)
    help( GompertzIntegral)
    help( Linear_Combo)
    help( Markov_Chain)
    help( Delay)
    help( Filter)
    help( FilterN)
    help( Cumulative)
    help( Decimate)
    help( ArrayMerge)
    help( Strings_To_Array)
    help( Load_Calibration)
    help( Load_Calibration_Text)
    help( Prepare_Russian_Font)
    
    coplot_x = np.linspace( -15, 15, 301)
    coplot_y = None
    #coplot_y = np.sin( coplot_x / 3)
    F1 = Sigmoid( -1)
    F1.Plot( coplot_x[0], coplot_x[-1], "./Graphs/Test01_Sigmoid", coplot_x, coplot_y, no_screen = True)
    F2 = Bathtub()
    F2.Plot( coplot_x[0], coplot_x[-1], "./Graphs/Test02_Bathtub", coplot_x, F1.GetVector(coplot_x), no_screen = True)
    F3 = Hubbert()
    F3.Plot( coplot_x[0], coplot_x[-1], "./Graphs/Test03_Hubbert", no_screen = True)
    F4 = GenHubbert()
    F4.Plot( coplot_x[0], coplot_x[-1], "./Graphs/Test04_GenHubbert", no_screen = True)
    F5 = Gauss()
    F5.Plot( coplot_x[0], coplot_x[-1], "./Graphs/Test05_Gauss", no_screen = True)
    F6 = Kapitsa()
    F6.Plot( coplot_x[0], coplot_x[-1], "./Graphs/Test06_Kapitsa", no_screen = True)
    F7 = KapitsaIntegral()
    F7.Plot( 1800, 2200, "./Graphs/Test07_Kapitsa_Integral", no_screen = True)
    F8 = Weibull( x0=1968, b=0.015, k=2.2, peak=100)
    F8.Plot( 1900, 2100, "./Graphs/Test08_Weibull", no_screen = True)
    F9 = Gompertz()
    F9.Plot( coplot_x[0], coplot_x[-1], "./Graphs/Test09_Gompertz", no_screen = True)
    F10 = GompertzIntegral()
    F10.Plot( coplot_x[0], coplot_x[-1], "./Graphs/Test10_Gompertz_Integral", no_screen = True)
