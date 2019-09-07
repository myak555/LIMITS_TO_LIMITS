from Utilities import *


class Engine:
    """
    Singleton class for function handling
    """
    def __init__(self):
        self.Primary_Dictionary = {} # equation by number 
        self.Secondary_Dictionary = {} # number by name 
        self.Parameters = {} # here and below: name by number
        self.Tables = {} 
        self.Levels = {} 
        self.Rates = {} 
        self.Smooths = {} 
        self.Delays = {}
        self.Dependents = {}        
        self.ChangePolicies = {}
        self.dt = 1.0
        self.start_time = 1900
        self.stop_time = 2100
        self.time = self.start_time
        self.global_policy_year = 1975
        self.global_stability_year = 4000
        self.Model_Time = []
        return
    def Register( self, func):
        self.Primary_Dictionary[func.Number] = func
        self.Secondary_Dictionary[func.Name] = func.Number
        return
    def byNumber( self, number):
        if not number in self.Primary_Dictionary: return None
        return self.Primary_Dictionary[number]
    def byName( self, name):
        if name is None: return None
        if not name in self.Secondary_Dictionary: return None
        number = self.Secondary_Dictionary[name]
        return self.Primary_Dictionary[number]
    def SortByType( self):
        for name in self.Secondary_Dictionary:
            eq = self.byName( name)
            if eq.Type == "Parameter":
                self.Parameters[eq.Number] = eq.Name  
            if eq.Type == "Table":
                self.Tables[eq.Number] = eq.Name  
                self.Dependents[eq.Number] = eq.Name
            if eq.Type == "Level":
                self.Levels[eq.Number] = eq.Name  
            if eq.Type == "Rate":
                self.Rates[eq.Number] = eq.Name  
            if eq.Type == "Smooth":
                self.Smooths[eq.Number] = eq.Name  
                self.Dependents[eq.Number] = eq.Name
            if eq.Type == "Delay":
                self.Delays[eq.Number] = eq.Name  
                self.Dependents[eq.Number] = eq.Name
            if eq.Type == "Aux":
                self.Dependents[eq.Number] = eq.Name
            if eq.PolicyInput == "Policy":
                self.Dependents[eq.Number] = eq.Name
                self.ChangePolicies[eq.Number] = eq.Name  
        return
    def SelectByGlobalPolicy( self, cutoff, before, after, stable):
        """
        Selects 'before' before the global policy, b 'after' and 'stable'
        after stability is achieved
        """
        if cutoff is not None and self.time < 1940:
            return cutoff
        if before is not None and self.time < self.global_policy_year:
            return before
        if stable is not None and self.time >= self.global_stability_year:
            return stable
        if after is not None: return after
        return before
    def Produce_Solution_Path(self, verbose=False):
        self.SolutionPath = []
        iStep = 0
        print("Generating solution path")
        
        # parameters and level-types are presumed independent
        for number in self.Parameters:
            self.SolutionPath += [ number]
            if verbose:
                print("   {:03d} {{{:03d}}} {:s}".format( iStep, number, self.byNumber(number).Name))
            iStep += 1
        for number in self.Levels:
            self.SolutionPath += [ number]
            if verbose:
                print("   {:03d} {{{:03d}}} {:s}".format( iStep, number, self.byNumber(number).Name))
            iStep += 1

        to_solve = len(self.Dependents)
        to_solve_prev = to_solve
        for npass in range( 1, 101):
            if verbose:
                print()
                print( "   Pass {:d} to solve {:d} equations".format(npass, to_solve))
            for number in self.Dependents:
                if number in self.SolutionPath: continue 
                equation = self.byNumber(number)
                dependencies_resolved = True
                for dependence in equation.Dependencies:
                    if self.Secondary_Dictionary[dependence] in self.SolutionPath: continue
                    dependencies_resolved = False
                    break
                if not dependencies_resolved: continue
                self.SolutionPath += [ number]
                to_solve -= 1
                if verbose: 
                    print("   {:03d} {{{:03d}}} {:s}".format( iStep, number, equation.Name))
                iStep += 1
            if to_solve <= 0:
                if verbose: 
                    print()
                    print( "   All {:d} solved".format(len(self.Dependents)))
                break
            if to_solve == to_solve_prev:
                print()
                print( "   Got stuck at {:d} equations".format( to_solve))
                break        
            to_solve_prev = to_solve 

        if to_solve > 0:
            print()
            print( "   Unresolved dependencies: ")
            for number in self.Dependents:
                if number in self.SolutionPath: continue 
                equation = self.byNumber(number)
                print( "      {{{:03}}} {:s}: ".format( equation.Number, equation.Name))
                print( "         ", equation.Dependencies)
            return

        # rate-types are presumed defined at this point
        for number in self.Rates:
            self.SolutionPath += [ number]
            if verbose:
                print("   {:03d} {{{:03d}}} {:s}".format( iStep, number, self.byNumber(number).Name))
            iStep += 1
        return
    def LockVariables(self):
        undefined_count = 0
        for num in self.Primary_Dictionary:
            equation = self.Primary_Dictionary[num]
            equation.Lock()
            if (equation.J is None) or (equation.K is None):
                undefined_count += 1
        return undefined_count
    def Reset(self,
             dt = 1.0,
             start_time = 1900,
             stop_time = 2100,
             global_policy_year = 1975,
             global_stability_year = 4000,
             verbose=False):
        print("DYNAMO reset")
        self.dt = dt
        self.start_time = start_time
        self.stop_time = stop_time
        self.time = start_time
        self.global_policy_year = global_policy_year
        self.global_stability_year = global_stability_year
        self.Model_Time = []
        if verbose:
            print( "   Model from {:.0f} to {:.0f}".format(self.start_time, self.stop_time) )
            print( "   Time step {:.1f} year(s)".format(self.dt) )
            print( "   Global policy in {:.1f}".format(self.global_policy_year) )
            print( "   Stability forced in {:.1f}".format(self.global_stability_year) )
        for num in self.Primary_Dictionary:
            equation = self.Primary_Dictionary[num]
            equation.Reset()
            if verbose:
                print( "   {:s} reset".format(equation.Name) )
        return
    def Warmup(self, cycles = 10, verbose=False):
        print("DYNAMO Warm-up")
        for num in self.Parameters:
            self.Primary_Dictionary[num].Warmup()
        for i in range(cycles):
            for num in self.SolutionPath:
                self.Primary_Dictionary[num].Warmup()                
            undefined = self.LockVariables()
            if verbose:
                print( "   Warmup pass {:d}: {:d} undefined".format(i+1, undefined) )
        return
    def Compute(self, verbose=False):
        print("DYNAMO Running")
        while self.time <= self.stop_time:
            self.Model_Time += [self.time]
            for num in self.SolutionPath:
                self.Primary_Dictionary[num].Update()                
            undefined = self.LockVariables()
            if verbose:
                if undefined == 0:
                    print( "   {:.1f}: all defined".format(self.Model_Time[-1]) )
                else:
                    print( "   {:.1f}: {:d} undefined".format(self.Model_Time[-1], undefined) )
            self.time += self.dt
        return
    
        
DYNAMO_Engine = Engine()


class Parameter:
    """
    DYNAMO prototype for a fixed value
    """
    def __init__(self,
                 number, name,
                 Val,
                 usedIn = [],
                 units="unitless"):
        self.Number = number
        self.Name = name
        self.Type = "Parameter"
        self.PolicyInput = "Fixed"
        self.Value = Val
        self.UsedIn = usedIn
        self.Units = units
        self.Dependencies = [] # depends on nothing
        self.J = self.Value
        self.K = self.Value
        DYNAMO_Engine.Register(self)
        return
    def Reset(self):
        return
    def Warmup(self):
        return
    def Update(self):
        self.Warmup()
        return self.K
    def Lock(self):
        return
    def __str__(self):
        s = "{{{:03d}}}\t{:s} {:s} {:s} = {:g} [{:s}]".format(
            self.Number, self.PolicyInput, self.Type, self.Name, self.Value, self.Units)
        return s


class PolicyParametrization:
    """
    DYNAMO prototype for selecting parameter before and after policy implementation
    This is essentially a Heaviside step function aH(t-to)+b
    """
    def __init__(self,
                 number, name,
                 value_before, value_after,
                 units="unitless"):
        self.Number = number
        self.Name = name
        self.Type = "Parameter"
        self.PolicyInput = "Policy"
        self.Units = units
        self.BeforePolicy = value_before
        self.AfterPolicy = value_after
        self.Dependencies = [] # depends only on model time
        DYNAMO_Engine.Register(self)
        return
    def Reset(self):
        self.J = DYNAMO_Engine.SelectByGlobalPolicy(
            self.BeforePolicy,
            self.BeforePolicy,
            self.AfterPolicy,
            self.AfterPolicy)
        self.K = self.J
        return
    def Warmup(self):
        self.K = DYNAMO_Engine.SelectByGlobalPolicy(
            self.BeforePolicy,
            self.BeforePolicy,
            self.AfterPolicy,
            self.AfterPolicy)
        return
    def Update(self):
        self.Warmup()
        return self.K
    def Lock(self):
        self.J = self.K
        return
    def __str__(self):
        s = "{{{:03d}}}\t{:s} {:s} {:s} changes from {:g} to {:g} [{:s}] in {:g}".format(
            self.Number, self.PolicyInput, self.Type, self.Name, self.BeforePolicy, self.AfterPolicy,
            self.Units, DYNAMO_Engine.global_policy_year)
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
                  normfn = lambda: 1.0,
                  initialValue = None):
        self.Number = number
        self.Name = name
        self.Type = "Table"
        self.PolicyInput = "Fixed"
        self.Units = units
        self.NormFn = normfn
        self.InitialValue = initialValue
        if data_1940 is not None:
            self.DataHistory = np.array( data_1940)
        else:
            self.DataHistory = None
        self.DataBefore = np.array( data)
        if data_after_policy is not None:
            self.DataAfter = np.array( data_after_policy)
            self.PolicyInput = "Policy"
        else:
            self.DataAfter = None
        self.Indices = np.linspace( imin, imax, len(data))
        self.Delta = self.Indices[1]-self.Indices[0]
        self.Dependencies = []
        if self.InitialValue is None:
            self.Dependencies = dependencies # may depend on model time as well
        self.UpdateFn = updatefn
        self.K = self.InitialValue
        self.J = self.InitialValue
        DYNAMO_Engine.Register(self)
        return
    def Lookup( self, v):
        data = DYNAMO_Engine.SelectByGlobalPolicy(
            self.DataHistory,
            self.DataBefore,
            self.DataAfter,
            self.DataAfter)
        if v <= self.Indices[0] : return data[ 0]
        if v >= self.Indices[-1]: return data[-1]
        for i, vi in enumerate( self.Indices):
            if vi <= v and v < self.Indices[i+1]:
                f = (v-vi) / self.Delta
                return data[i]*(1-f) + data[i+1]*f
        return data[-1]
    def Reset(self):
        return
    def Warmup(self):
        v = self.InitialValue
        try:
            if v is None and self.UpdateFn is None:
                v = DYNAMO_Engine.byName( self.Dependencies[0]).K
            if v is None and self.UpdateFn is not None:
                v = self.UpdateFn()
        except:
            v = self.InitialValue
        if v is not None: v /= self.NormFn()
        if v is None:
            self.K = None
            print( "Table Achtung! " + self.Name)
            return
        self.K = self.Lookup( v)
        return
    def Update(self):
        self.Warmup();
        return self.K
    def Lock(self):
        self.J = self.K
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
                s += (" - changing in {:g}".format(DYNAMO_Engine.global_policy_year))
            else:
                s += (" - no change in {:g}".format(DYNAMO_Engine.global_policy_year))
        return s


class LevelVariable:
    """
    DYNAMO prototype for a level variable
    """
    def __init__(self,
                 number, name,
                 initialValue,
                 units="unitless",
                 updatefn = None):
        self.Number = number
        self.Name = name
        self.Type = "Level"
        self.PolicyInput = "None"
        self.InitialValue = initialValue
        self.Units = units
        self.UpdateFn = updatefn
        self.Dependencies = [] # depends only on model time step and rates
        self.Reset()
        DYNAMO_Engine.Register(self)
        return
    def Reset(self):
        self.J = self.InitialValue
        self.K = self.InitialValue
        self.Data = []
        return
    def Warmup(self):
        self.J = self.InitialValue
        self.K = self.InitialValue
        return
    def Update(self):
        rate = 0.0
        try:
            if self.UpdateFn is not None: rate = self.UpdateFn()
        except:
            print("Level Achtung! " + self.Name)
            rate = 0.0
        self.K = self.J + rate * DYNAMO_Engine.dt
        self.Data += [self.K]
        return self.K
    def Lock(self):
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
        self.PolicyInput = "None"
        self.Units = units
        self.Reset()
        self.UpdateFn = updatefn            
        self.EquilibriumFn = equilibriumfn
        self.Dependencies = [] # all dependencies are presumed resolved
        DYNAMO_Engine.Register(self)
        return
    def Reset(self):
        self.J = None
        self.K = None
        self.Data = []
        return
    def Warmup(self):
        fn = DYNAMO_Engine.SelectByGlobalPolicy(
            self.UpdateFn,
            self.UpdateFn,
            self.UpdateFn,
            self.EquilibriumFn)
        if fn is None:
            print("ERROR: Rate " + self.Name + " has no update function")
            self.K = None
            return
        try:
            self.K = fn()
        except:
            self.J = 0.0
            self.K = 0.0
            print( "Warning:" + self.Name + ".J and .K replaced  with zeros in warm-up")
        return
    def Update(self):
        fn = DYNAMO_Engine.SelectByGlobalPolicy(
            self.UpdateFn,
            self.UpdateFn,
            self.UpdateFn,
            self.EquilibriumFn)
        if fn is None:
            print("ERROR: Rate " + self.Name + " has no update function")
            self.K = None
            return
        try:
            self.K = fn()
        except:
            self.K = 0.0
            print( "Warning:" + self.Name + ".K replaced with zero in update")
        self.Data += [self.K]
        return self.K
    def Lock(self):
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
                 normfn = lambda: 1.0,
                 equilibriumfn=None):
        self.Number = number
        self.Name = name
        self.Type = "Aux"
        self.PolicyInput = "None"
        self.Units = units
        self.NormFn = normfn
        self.Dependencies = dependencies
        self.Reset()
        self.UpdateFn = updatefn
        self.EquilibriumFn = equilibriumfn
        DYNAMO_Engine.Register(self)
        return
    def Op(self, name):
        return DYNAMO_Engine.byName(name)
    def Reset(self):
        self.J = None
        self.K = None
        self.Data = []
        return
    def Warmup(self):
        fn = DYNAMO_Engine.SelectByGlobalPolicy(
            self.UpdateFn,
            self.UpdateFn,
            self.UpdateFn,
            self.EquilibriumFn)
        self.K = None
        try:
            if fn is not None: self.K = fn()
        except:
            print("Warning: K is undefined " + self.Name)
        if self.K is not None: self.K / self.NormFn() 
        return
    def Update(self):
        self.Warmup()
        self.Data += [self.K]
        return self.K
    def Lock(self):
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

       
class SmoothVariable:
    """
    DYNAMO prototype for an auxillary dependency with smoothing
    if initialValue is not None, dependency is ignored; this is used to
    break determination cycles
    """
    def __init__(self,
                 number, name,
                 delayfn=lambda: 1.0,
                 units="unitless",
                 dependencies=[],
                 initialValue = None):
        self.Number = number
        self.Name = name
        self.Type = "Smooth"
        self.PolicyInput = "None"
        self.Units = units
        self.DelayFn = delayfn
        self.InitialValue = initialValue
        self.InitFn = dependencies[0]
        self.Dependencies = []
        if initialValue is None:
            self.Dependencies = dependencies
        self.Reset()
        DYNAMO_Engine.Register(self)
        return
    def Init(self):
        InputClass = DYNAMO_Engine.byName( self.InitFn)
        if InputClass is None:
            print( "Smooth " + self.Name + " - input class not defined")
        if self.InitialValue is not None:
            self.J = self.InitialValue
            self.K = self.InitialValue
            return
        self.J = InputClass.K
        self.K = InputClass.K
        if self.K is None:
            print( "Smooth K Achtung! " + self.Name)
        return
    def Reset(self):
        self.J = self.InitialValue
        self.K = self.InitialValue
        self.isFirstCall = True;
        return
    def Warmup(self):
        self.Init()
        return
    def Update(self):
        InputClass = DYNAMO_Engine.byName( self.InitFn)
        if InputClass is None:
            print( "Smooth " + self.Name + " - input class not defined")
        if self.isFirstCall:
            self.J = InputClass.K
            self.K = InputClass.K
            self.isFirstCall = False;
            return self.K;
        self.K = self.J + DYNAMO_Engine.dt * (InputClass.J - self.J) / self.DelayFn();
        return self.K
    def Lock(self):
        self.J = self.K
        return
    def __str__(self):
        s = "{{{:03d}}}\t{:s} {:s} J = ".format( self.Number, self.Type, self.Name)
        if self.J is None: s += "<None>, K = "
        else: s += "{:g}, K = ".format(self.J)
        if self.K is None: s += "<None>"
        else: s += "{:g}".format(self.K)
        s += " [{:s}]".format(self.Units)
        return s


class DelayVariable:
    """
    DYNAMO prototype for third-order exponential delay Rate variables
    """
    def __init__(self,
                 number, name,
                 delayfn=lambda: 1.0,
                 units="unitless",
                 dependencies=[],
                 initialValue = None):
        self.Number = number
        self.Name = name
        self.Type = "Delay"
        self.PolicyInput = "None"
        self.Units = units
        self.DelayFn = delayfn
        self.InitialValue = initialValue
        self.InitFn = dependencies[0]
        self.Dependencies = []
        if initialValue is None:
            self.Dependencies = dependencies
        self.Reset()
        DYNAMO_Engine.Register(self)
        return
    def Init(self):
        InputClass = DYNAMO_Engine.byName( self.InitFn)
        if InputClass is None:
            print( "Delay " + self.Name + " - input class not defined")
            return
        if self.InitialValue is not None:
            self.J = self.InitialValue
            self.K = self.InitialValue
        else:
            self.J = InputClass.K
            self.K = InputClass.K
        if self.K is None:
            print( "Delay K Achtung! " + self.Name)
        self.alpha = (self.K, self.K)
        self.beta  = (self.K, self.K)
        self.gamma = (self.K, self.K)
        return
    def Reset(self):
        self.J = self.InitialValue
        self.K = self.InitialValue
        self.isFirstCall = True;
        self.alpha = (self.InitialValue, self.InitialValue)
        self.beta  = (self.InitialValue, self.InitialValue)
        self.gamma = (self.InitialValue, self.InitialValue)
        return
    def Warmup(self):
        self.Init()
        return
    def Update(self):
        InputClass = DYNAMO_Engine.byName( self.InitFn)
        if InputClass is None:
            print( "Delay " + self.Name + " - input class not defined")
        if self.isFirstCall:
            self.J = InputClass.K
            self.K = InputClass.K
            self.alpha = (InputClass.K, InputClass.K)
            self.beta  = (InputClass.K, InputClass.K)
            self.gamma = (InputClass.K, InputClass.K)
            self.isFirstCall = False;
            return self.K;
        Delay_3 = self.DelayFn() / 3
        alpha = self.alpha[0] + DYNAMO_Engine.dt * (InputClass.J  - self.alpha[0]) / Delay_3;
        beta  = self.beta[0]  + DYNAMO_Engine.dt * (self.alpha[0] - self.beta[0])  / Delay_3;
        gamma = self.gamma[0] + DYNAMO_Engine.dt * (self.beta[0]  - self.gamma[0]) / Delay_3;
        self.alpha = (self.alpha[1], alpha)
        self.beta  = (self.beta[1], beta)
        self.gamma = (self.gamma[1], gamma)
        self.K = gamma
        return self.K
    def Lock(self):
        self.J = self.K
        return
    def __str__(self):
        s = "{{{:03d}}}\t{:s} {:s} J = ".format( self.Number, self.Type, self.Name)
        if self.J is None: s += "<None>, K = "
        else: s += "{:g}, K = ".format(self.J)
        if self.K is None: s += "<None>"
        else: s += "{:g}".format(self.K)
        s += " [{:s}]".format(self.Units)
        return s


class meaningOfLife:
    """
    Ultimate Question of Life, The Universe, and Everything 
    """
    def __init__(self):
        self.J = 42
        self.K = 42


def PlotTable(
    table,
    plotMin=None, plotMax=None,
    xLabel=None,
    filename="./Graphs/DYNAMO_{:s}.png",
    show=False):
    """
    Plots a table against a primary argument
    """
    print( "   Plotting test table {:s}".format( table.Name))
    if plotMin is None: plotMin = table.Indices[0]  
    if plotMax is None: plotMax = table.Indices[-1]  
    xPlot = np.linspace( plotMin, plotMax, 101)
    yPlot = np.zeros( 101)
    for i, v in enumerate( xPlot): yPlot[i] = table.Lookup( v)       
    norm = table.NormFn()
    fig = plt.figure( figsize=(15,10))
    fig.suptitle('DYNAMO Table Parametrization: {:s}'.format(table.Name), fontsize=25)
    gs = plt.GridSpec(1, 1) 
    ax1 = plt.subplot(gs[0])
    ax1.plot( xPlot*norm, yPlot, "-", lw=3, color="k")
    ax1.plot( table.Indices*norm, table.DataBefore, "o", lw=2, color="r", label="Before policy")
    if table.DataAfter is not None:
        ax1.plot( table.Indices*norm, table.DataAfter, "o", lw=2, color="b", label="After policy")
        ax1.legend(loc=0)
    if table.DataHistory is not None:
        ax1.plot( table.Indices*norm, table.DataHistory, "o", lw=2, color="m", label="Prior to 1940")
        ax1.legend(loc=0)
    ax1.set_xlim( plotMin*norm, plotMax*norm)
    ax1.grid(True)
    if xLabel is not None:
        ax1.set_xlabel(xLabel)
    else:
        first_dependency = DYNAMO_Engine.byName( table.Dependencies[0])
        s = "{:s} [{:s}]".format(first_dependency.Name, first_dependency.Units)
        if norm != 1.0: s += ", Norm = {:g}".format(norm)
        ax1.set_xlabel(s)
    ax1.set_ylabel("{:s} [{:s}]".format(table.Name, table.Units))
    plt.savefig( filename.format(table.Name))
    if show: plt.show()
    else: plt.close('all')
    return


def PlotVariable(
    variable,
    ModelTime,
    xLabel="Model time [years]",
    filename="./Graphs/MODEL_{:s}.png",
    show=False):
    """
    Plots a variable against model time
    """
    print( "    Plotting {:s} [{:s}] against {:s}".format( variable.Name, variable.Units, xLabel))
    xPlot = []
    yPlot = []
    xNone = []
    for i, t in enumerate( ModelTime):
        if variable.Data[i] is None:
            xNone += [t]
            continue
        xPlot += [t]
        yPlot += [variable.Data[i]]
    xPlot = np.array(xPlot)
    yPlot = np.array(yPlot)
    yPlotMin = min(yPlot)
    yPlotMax = max(yPlot)
    fig = plt.figure( figsize=(15,10))
    fig.suptitle('DYNAMO Variable: {:s}'.format(variable.Name), fontsize=25)
    gs = plt.GridSpec(1, 1) 
    ax1 = plt.subplot(gs[0])
    for x in xNone:
        ax1.plot( [x,x], [yPlotMin, yPlotMax], "--", lw=3, alpha= 0.5, color="k")
    ax1.plot( xPlot, yPlot, "o", lw=2, color="k")
    ax1.plot( xPlot, yPlot, "-", lw=4, color="b", alpha=0.7)
    ax1.set_xlim( ModelTime[0], ModelTime[-1])
    ax1.grid(True)
    ax1.set_xlabel(xLabel)
    ax1.set_ylabel("{:s} [{:s}]".format(variable.Name, variable.Units))
    plt.savefig( filename.format(variable.Name))
    if show: plt.show()
    else: plt.close('all')
    return


# Generic checks
if __name__ == "__main__":
    print()
    print("Check Parameter:")
    subsistenceFoodPerCapita = Parameter(
        151, "subsistenceFoodPerCapita", 230,
        [20, 127], "kilograms / person / year")
    subsistenceFoodPerCapita.Reset()
    print("   Reset: ", subsistenceFoodPerCapita)
    subsistenceFoodPerCapita.Warmup()
    print("   Warmup: ", subsistenceFoodPerCapita)
    subsistenceFoodPerCapita.Update()
    print("   Update: ", subsistenceFoodPerCapita.Update(), subsistenceFoodPerCapita)
    subsistenceFoodPerCapita.Lock()
    print("   Lock: ", subsistenceFoodPerCapita.J, subsistenceFoodPerCapita.K, subsistenceFoodPerCapita)

    print()
    print("Check Policy Parametrization:")
    lifeExpectancy = PolicyParametrization(
        51, "lifeExpectancy", 42, 43, units="years")
    lifeExpectancy.Reset()
    print("   Reset: ", lifeExpectancy)
    lifeExpectancy.Warmup()
    print("   Warmup: ", lifeExpectancy)
    lifeExpectancy.Update()
    print("   Update: ", lifeExpectancy.Update(), lifeExpectancy)
    lifeExpectancy.Lock()
    print("   Lock: ", lifeExpectancy.J, lifeExpectancy.K, lifeExpectancy)

    print()
    print("Check Table Parametrization:")
    mortality0To14 = TableParametrization(
        4, "mortality0To14",
        [0.0567, 0.0366, 0.0243, 0.0155, 0.0082, 0.0023, 0.0010],
        20, 80, "deaths / person / year",
        dependencies = ["lifeExpectancy"])
    mortality0To14.Reset()
    print("   Reset: ", mortality0To14)
    mortality0To14.Warmup()
    print("   Warmup: ", mortality0To14)
    mortality0To14.Update()
    print("   Update: ", mortality0To14.Update(), mortality0To14)
    mortality0To14.Lock()
    print("   Lock: ", mortality0To14.J, mortality0To14.K, mortality0To14)
    PlotTable( mortality0To14, 0, 100, xLabel="(Test only) lifeExpectancy [years]", show=True)
