from Utilities import *

DYNAMO_Function_Dictionary = {}
DYNAMO_Function_Name_Dictionary = {}
DYNAMO_Parameter_Dictionary = {}
DYNAMO_Level_Dictionary = {}
DYNAMO_Aux_Dictionary = {}
DYNAMO_Aux_Name_Dictionary = {}
DYNAMO_Rate_Dictionary = {}
DYNAMO_Table_Dictionary = {}
DYNAMO_Smooth_Dictionary = {}
DYNAMO_Delay3_Dictionary = {}
DYNAMO_Policy_Dictionary = {}
DYNAMO_dt = 1.0
DYNAMO_start_time = 1900
DYNAMO_stop_time = 2100
DYNAMO_time = DYNAMO_start_time
DYNAMO_global_policy_year = 1975
DYNAMO_global_stability_year = 4000

def Select( t, t0, before, after):
    """
    Selects 'before' if t<t0 and 'after' if >=
    """
    if t >= t0: return after
    return before

def SelectByGlobalPolicy( cutoff, before, after, stable):
    """
    Selects 'before' before the global policy, b 'after' and 'stable'
    after stability is achieved
    """
    if cutoff is not None and DYNAMO_time < 1940:
        return cutoff
    if DYNAMO_time < DYNAMO_global_policy_year: return before
    if stable is not None and DYNAMO_time >= DYNAMO_global_stability_year:
        return stable
    if after is not None: return after
    return before

def GetDefault( value, default_value):
    """
    returns a default if the value is not specified
    """
    if value is None: return default_value
    return value


class Parameter:
    """
    DYNAMO prototype for a fixed value
    """
    def __init__(self,
                 number, name, Val,
                 equations = [],
                 units="unitless"):
        self.Number = number
        self.Name = name
        self.Type = "Parameter"
        self.Value = Val
        self.Equations = equations
        self.Units = units
        self.Dependencies = [] # depends on nothing
        self.J = self.Value
        self.K = self.Value
        DYNAMO_Function_Dictionary[ number] = self
        DYNAMO_Function_Name_Dictionary[ name] = self
        DYNAMO_Parameter_Dictionary[ number] = self
        return
    def Reset(self):
        return
    def Warmup(self):
        return
    def Update(self):
        self.Warmup()
        return self.K
    def Tick(self):
        return
    def __str__(self):
        s = "{{{:03d}}}\tParameter {:s} = {:g} [{:s}]".format(
            self.Number, self.Name, self.Value, self.Units)
        return s


class PolicyParametrization:
    """
    DYNAMO prototype for selecting parameter before and after policy implementation
    This is essentially a Heaviside step function aH(t-to)+b
    """
    def __init__(self, number, name, value_before, value_after, units="unitless"):
        self.Number = number
        self.Name = name
        self.Type = "Parameter"
        self.Units = units
        self.BeforePolicy = value_before
        self.AfterPolicy = value_after
        self.Dependencies = [] # depends only on model time
        DYNAMO_Function_Dictionary[ number] = self
        DYNAMO_Function_Name_Dictionary[ name] = self
        DYNAMO_Aux_Dictionary[ number] = self
        DYNAMO_Aux_Name_Dictionary[ name] = self
        DYNAMO_Policy_Dictionary[ number] = self
        return
    def Reset(self):
        self.J = SelectByGlobalPolicy( self.BeforePolicy,
                                       self.BeforePolicy,
                                       self.AfterPolicy,
                                       self.AfterPolicy)
        self.K = self.J
        return
    def Warmup(self):
        self.K = SelectByGlobalPolicy( self.BeforePolicy,
                                       self.BeforePolicy,
                                       self.AfterPolicy,
                                       self.AfterPolicy)
        return
    def Update(self):
        self.Warmup()
        return self.K
    def Tick(self):
        self.J = self.K
        return
    def __str__(self):
        s = "{{{:03d}}}\tPolicy {:s} changes from {:g} to {:g} [{:s}] in {:g}".format(
            self.Number, self.Name, self.BeforePolicy, self.AfterPolicy,
            self.Units, DYNAMO_global_policy_year)
        return s


class TableParametrization:
    """
    DYNAMO prototype for a parametrization as
    a numeric table with linear interpolation between the values
    """
    def __init__( self,
                  number, name,
                  data, imin, imax,
                  units="unitless",
                  data_1940 = None,
                  data_after_policy = None,
                  dependencies = [],
                  updatefn = None,
                  norm = 1.0):
        self.Number = number
        self.Name = name
        self.Type = "Aux"
        self.Units = units
        self.Norm = norm
        if data_1940 is not None:
            self.DataHistory = np.array( data_1940)
        else:
            self.DataHistory = None
        self.DataBefore = np.array( data)
        if data_after_policy is not None:
            self.DataAfter = np.array( data_after_policy)
            DYNAMO_Policy_Dictionary[ number] = self
        else:
            self.DataAfter = None
        self.Indices = np.linspace( imin, imax, len(data))
        self.Delta = self.Indices[1]-self.Indices[0]
        self.Dependencies = dependencies # may depend on model time as well
        self.K = None
        self.J = None
        self.UpdateFn = updatefn
        DYNAMO_Function_Dictionary[ number] = self
        DYNAMO_Function_Name_Dictionary[ name] = self
        DYNAMO_Aux_Dictionary[ number] = self
        DYNAMO_Aux_Name_Dictionary[ name] = self
        DYNAMO_Table_Dictionary[ number] = self
        return
    def Lookup( self, v):
        data = SelectByGlobalPolicy( self.DataHistory,
                                     self.DataBefore,
                                     self.DataAfter,
                                     self.DataAfter)
        if v is None: return None
        if v <= self.Indices[0] : return data[ 0]
        if v >= self.Indices[-1]: return data[-1]
        for i, vi in enumerate( self.Indices):
            if vi <= v and v < self.Indices[i+1]:
                f = (v-vi) / self.Delta
                return data[i]*(1-f) + data[i+1]*f
        return data[-1]
    def Reset(self):
        return None
    def Warmup(self):
        v = self.UpdateFn()
        if v is None and len( self.Dependencies) == 1:
            v = DYNAMO_Function_Name_Dictionary[self.Dependencies[0]].K
        if v is not None: v /= self.Norm
        self.K = self.Lookup( v)
        return
    def Update(self):
        self.Warmup();
        return self.K
    def Tick(self):
        self.J = self.K
        return
    def Plot(self, plotMin=None, plotMax=None, xLabel=None, filename="./Graphs/DYNAMO_{:s}.png"):
        print( "Plotting test table {:s}".format( self.Name))
        if plotMin is None: plotMin = self.Indices[0]  
        if plotMax is None: plotMax = self.Indices[-1]  
        xPlot = np.linspace( plotMin, plotMax, 101)
        yPlot = np.zeros( 101)
        for i, v in enumerate( xPlot): yPlot[i] = self.Lookup( v)       
        fig = plt.figure( figsize=(15,10))
        fig.suptitle('Проверка модели "World3": {:s}'.format(self.Name), fontsize=25)
        gs = plt.GridSpec(1, 1) 
        ax1 = plt.subplot(gs[0])
        ax1.plot( xPlot*self.Norm, yPlot, "-", lw=3, color="k")
        ax1.plot( self.Indices*self.Norm, self.DataBefore, "o", lw=2, color="r", label="Before policy")
        if self.DataAfter is not None:
            ax1.plot( self.Indices*self.Norm, self.DataAfter, "o", lw=2, color="b", label="After policy")
            ax1.legend(loc=0)
        if self.DataHistory is not None:
            ax1.plot( self.Indices*self.Norm, self.DataHistory, "o", lw=2, color="m", label="Prior to 1940")
            ax1.legend(loc=0)
        ax1.set_xlim( plotMin*self.Norm, plotMax*self.Norm)
        ax1.grid(True)
        if xLabel is not None:
            ax1.set_xlabel(xLabel)
        else:
            first_dependency = DYNAMO_Function_Name_Dictionary[self.Dependencies[0]]
            s = "{:s} [{:s}]".format(first_dependency.Name, first_dependency.Units)
            if self.Norm != 1.0: s += ", Norm = {:g}".format(self.Norm)
            ax1.set_xlabel(s)
        ax1.set_ylabel("{:s} [{:s}]".format(self.Name, self.Units))
        plt.savefig( filename.format(self.Name))
        plt.close('all')
        return
    def __str__(self):
        s = "{{{:03d}}}\tTable {:s} [{:s}]".format(
            self.Number, self.Name, self.Units)
        if self.DataHistory is not None:
            s += (" - changing in {:g}".format(1940))
        if self.DataAfter is not None:
            diff = self.DataAfter - self.DataBefore
            diff = np.sum( diff*diff)
            if diff > 0.0:
                s += (" - changing in {:g}".format(DYNAMO_global_policy_year))
            else:
                s += (" - no change in {:g}".format(DYNAMO_global_policy_year))
        return s


class LevelVariable:
    """
    DYNAMO prototype for a level variable
    """
    def __init__(self,
                 number, name, initVal,
                 units="unitless",
                 updatefn = None):
        self.Number = number
        self.Name = name
        self.Type = "Level"
        self.InitialValue = initVal
        self.Units = units
        self.UpdateFn = updatefn
        self.Dependencies = [] # depends only on model time step and rates
        self.Reset()
        DYNAMO_Function_Dictionary[ number] = self
        DYNAMO_Function_Name_Dictionary[ name] = self
        DYNAMO_Level_Dictionary[ number] = self
        return
    def Reset(self):
        self.J = self.InitialValue
        self.K = self.InitialValue
        self.Data = [self.K]
        return
    def Warmup(self):
        rate = 0.0
        if self.UpdateFn is not None:
            rate = self.UpdateFn()
        self.K = self.J + rate * DYNAMO_dt
        return
    def Update(self):
        self.Warmup()
        self.Data += [self.K]
        return self.K
    def Tick(self):
        self.J = self.K
        return
    def __str__(self):
        s = "{{{:03d}}}\tLevel {:s} = {:g} [{:s}] - {:d} data point(s)".format(
            self.Number, self.Name, self.K, self.Units, len(self.Data))
        return s


class RateVariable:
    """
    DYNAMO prototype for a rate change variable
    """
    def __init__(self,
                 number, name,
                 units="unitless",
                 updatefn=None,
                 equilibriumfn=None):
        self.Number = number
        self.Name = name
        self.Type = "Rate"
        self.Units = units
        self.Reset()
        self.UpdateFn = updatefn            
        self.EquilibriumFn = equilibriumfn
        self.Dependencies = [] # all dependencies are presumed resolved
        DYNAMO_Function_Dictionary[ number] = self
        DYNAMO_Function_Name_Dictionary[ name] = self
        DYNAMO_Rate_Dictionary[ number] = self
        return
    def Reset(self):
        self.J = None
        self.K = None
        self.Data = []
        return
    def Warmup(self):
        fn = SelectByGlobalPolicy( self.UpdateFn,
                                  self.UpdateFn,
                                  self.UpdateFn,
                                  self.EquilibriumFn)
        if fn is None:
            self.K = None
            return
        self.K = fn()
        return
    def Update(self):
        self.Warmup()
        self.Data += [self.K]
        return self.K
    def Tick(self):
        self.J = self.K
        return
    def __str__(self):
        if self.K is None:
            s = "{{{:03d}}}\tRate {:s} = <None> [{:s}] - {:d} data point(s)".format(
                self.Number, self.Name, self.Units, len(self.Data))
        else:    
            s = "{{{:03d}}}\tRate {:s} = {:g} [{:s}] - {:d} data point(s)".format(
                self.Number, self.Name, self.K, self.Units, len(self.Data))
        return s


class AuxVariable:
    """
    DYNAMO prototype for an auxillary variable
    """
    def __init__(self,
                 number, name,
                 units="unitless",
                 dependencies=[],
                 updatefn = None,
                 norm = 1.0,
                 equilibriumfn=None):
        self.Number = number
        self.Name = name
        self.Type = "Aux"
        self.Units = units
        self.Norm = norm
        self.Dependencies = dependencies
        self.Reset()
        self.UpdateFn = updatefn
        self.EquilibriumFn = equilibriumfn
        DYNAMO_Function_Dictionary[ number] = self
        DYNAMO_Function_Name_Dictionary[ name] = self
        DYNAMO_Aux_Dictionary[ number] = self
        DYNAMO_Aux_Name_Dictionary[ name] = self
        return
    def Reset(self):
        self.J = None
        self.K = None
        self.Data = []
        return
    def Warmup(self):
        fn = SelectByGlobalPolicy( self.UpdateFn,
                                   self.UpdateFn,
                                   self.UpdateFn,
                                   self.EquilibriumFn)

        self.K = None
        if fn is not None:
            self.K = fn()
        if self.K is not None: self.K / self.Norm 
        return
    def Update(self):
        self.Warmup()
        self.Data += [self.K]
        return self.K
    def Tick(self):
        self.J = self.K
        return
    def __str__(self):
        if self.K is None:
            s = "{{{:03d}}}\tAux {:s} = <None> [{:s}] - {:d} data point(s)".format(
                self.Number, self.Name, self.Units, len(self.Data))
        else:    
            s = "{{{:03d}}}\tAux {:s} = {:g} [{:s}] - {:d} data point(s)".format(
                self.Number, self.Name, self.K, self.Units, len(self.Data))
        return s

    def Plot( self, ModelTime, xLabel="Model time [years]", filename="./Graphs/WORLD3_{:s}.png"):
        print( "Plotting test for {:s}".format( self.Name))
        xPlot = []
        yPlot = []
        xNone = []
        for i, t in enumerate( ModelTime):
            if self.Data[i] is None:
                xNone += [t]
                continue
            xPlot += [t]
            yPlot += [self.Data[i]]
        xPlot = np.array(xPlot)
        yPlot = np.array(yPlot)
        yPlotMin = min(yPlot)
        yPlotMax = max(yPlot)
        fig = plt.figure( figsize=(15,10))
        fig.suptitle('Проверка модели "World3": {:s}'.format(self.Name), fontsize=25)
        gs = plt.GridSpec(1, 1) 
        ax1 = plt.subplot(gs[0])
        for x in xNone:
            ax1.plot( [x,x], [yPlotMin, yPlotMax], "--", lw=3, alpha= 0.5, color="k")
        ax1.plot( xPlot, yPlot, "o", lw=2, color="k")
        ax1.plot( xPlot, yPlot, "-", lw=4, color="b", alpha=0.7)
        ax1.set_xlim( ModelTime[0], ModelTime[-1])
        ax1.grid(True)
        ax1.set_xlabel(xLabel)
        ax1.set_ylabel("{:s} [{:s}]".format(self.Name, self.Units))
        plt.savefig( filename.format(self.Name))
        plt.close('all')
        return
       

class Smooth:
    """
    DYNAMO prototype for an auxillary dependency with smoothing
    """
    def __init__(self, name, number, delay, units="unitless"):
        self.Name = name
        self.Number = number
        self.Type = "Aux"
        self.Units = units
        self.Delay = delay
        self.Dependencies = []
        self.Reset()
        self.InitFn = None
        self.InputClass = None
        DYNAMO_Function_Dictionary[ number] = self
        DYNAMO_Function_Name_Dictionary[ name] = self
        DYNAMO_Aux_Dictionary[ number] = self
        DYNAMO_Aux_Name_Dictionary[ name] = self
        DYNAMO_Smooth_Dictionary[ number] = self
        return
    def Init(self):
        if self.InitFn is None: return
        self.InputClass = DYNAMO_Function_Name_Dictionary[ self.InitFn]
        if self.InputClass is None: return
        self.J = self.InputClass.K
        self.K = self.InputClass.K
        return
    def Reset(self):
        self.J = None
        self.K = None
        self.isFirstCall = True;
        return
    def Warmup(self):
        self.Init()
        return
    def Update(self):
        if self.InputClass is None: return
        if self.isFirstCall:
            self.J = self.InputClass.K
            self.K = self.InputClass.K
            self.isFirstCall = False;
            return self.K;
        self.K = self.J + DYNAMO_dt * (self.InputClass.J - self.J) / self.Delay;
        return self.K
    def Tick(self):
        self.J = self.K
        return


class Delay3:
    """
    DYNAMO prototype for third-order exponential delay Rate variables
    """
    def __init__(self, name, number, delay, units="unitless"):
        self.Name = name
        self.Number = number
        self.Type = "Aux"
        self.Units = units
        self.Delay_3 = delay / 3
        self.Dependencies = []
        self.Reset()
        self.InitFn = None
        self.InputClass = None
        DYNAMO_Function_Dictionary[ number] = self
        DYNAMO_Function_Name_Dictionary[ name] = self
        DYNAMO_Aux_Dictionary[ number] = self
        DYNAMO_Aux_Name_Dictionary[ name] = self
        DYNAMO_Delay3_Dictionary[ number] = self
        return
    def Init(self):
        if self.InitFn is None: return
        self.InputClass = DYNAMO_Function_Name_Dictionary[ self.InitFn]
        if self.InputClass is None: return
        self.J = self.InputClass.K
        self.K = self.InputClass.K
        self.alpha = (self.InputClass.J, self.InputClass.J)
        self.beta  = (self.InputClass.J, self.InputClass.J)
        self.gamma = (self.InputClass.J, self.InputClass.J)
        return
    def Reset(self):
        self.J = None
        self.K = None
        self.isFirstCall = True;
        self.alpha = (None, None)
        self.beta  = (None, None)
        self.gamma = (None, None)
        return
    def Warmup(self):
        self.Init()
        return
    def Update(self):
        if self.InputClass is None: return
        if self.isFirstCall:
            self.J = self.InputClass.K
            self.K = self.InputClass.K
            self.alpha = (self.InputClass.K, self.InputClass.K)
            self.beta  = (self.InputClass.K, self.InputClass.K)
            self.gamma = (self.InputClass.K, self.InputClass.K)
            self.isFirstCall = False;
            return self.K;
        alpha = self.alpha[0] + DYNAMO_dt * (self.InputClass.J - self.alpha[0]) / self.Delay_3;
        beta  = self.beta[0]  + DYNAMO_dt * (self.alpha[0]     - self.beta[0])  / self.Delay_3;
        gamma = self.gamma[0] + DYNAMO_dt * (self.beta[0]      - self.gamma[0]) / self.Delay_3;
        self.alpha = (self.alpha[1], alpha)
        self.beta  = (self.beta[1], beta)
        self.gamma = (self.gamma[1], gamma)
        self.K = gamma
        return self.K
    def Tick(self):
        self.J = self.K
        return

class meaningOfLife:
    def __init__(self):
        self.K = 42


# Generic checks
if __name__ == "__main__":
    
    mortality0To14 = TableParametrization(
        4, "mortality0To14",
        [0.0567, 0.0366, 0.0243, 0.0155, 0.0082, 0.0023, 0.0010],
        20, 80, "deaths / person / year",
        dependencies = ["lifeExpectancy"])
    mortality0To14.Plot( 0, 100, xLabel="Test lifeExpectancy [years]")
    
    if InteractiveModeOn: plt.show(True)
