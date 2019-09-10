from DYNAMO_Plotting import *


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
        """
        Prototype class must register here
        """
        self.Primary_Dictionary[func.Number] = func
        self.Secondary_Dictionary[func.Name] = func.Number
        return
    def byNumber( self, number):
        """
        Returns class by its number
        """
        if not number in self.Primary_Dictionary: return None
        return self.Primary_Dictionary[number]
    def byName( self, name):
        """
        Returns class by its name
        """
        if name is None: return None
        if not name in self.Secondary_Dictionary: return None
        number = self.Secondary_Dictionary[name]
        return self.Primary_Dictionary[number]
    def SortByType( self):
        """
        Must run after all declarations are done
        """
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
            if eq.Policy == "Policy":
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
    def ListEquations(self):
        """
        Lists all registered
        """
        print()
        print( "Equation list:")
        for num in self.Primary_Dictionary:
            print( "   " + str(self.byNumber(num)))
        print( "Primary contains: {:d}, secondary contains: {:d}".format(
            len(self.Primary_Dictionary), len(self.Secondary_Dictionary)))
        return
    def ListDictionary(self, dictionary_name):
        """
        Lists by type
        """
        if dictionary_name == "primary":
            ListEquations(self)
            return
        print()
        print( "Equation list <{:s}>:".format(dictionary_name))        
        dictionary = self.Parameters
        if dictionary_name == "tables": dictionary =  self.Tables 
        if dictionary_name == "levels": dictionary = self.Levels 
        if dictionary_name == "rates": dictionary = self.Rates 
        if dictionary_name == "smooths": dictionary = self.Smooths 
        if dictionary_name == "delays": dictionary = self.Delays
        if dictionary_name == "dependents": dictionary = self.Dependents        
        if dictionary_name == "changes": dictionary = self.ChangePolicies
        for i, num in enumerate(dictionary):
            print( "   {:03d}".format(i+1) + str(self.byNumber(num)))
        return
    def ListSolutionPath(self):
        """
        Lists all classes in order of evaluation
        """
        print()
        print( "Solution sequence:")
        for i, num in enumerate( self.SolutionPath):
            print( "   {:03d} ".format(i) + self.byNumber(num).Name)
        print( "Solution path contains: {:d}".format(
            len(self.SolutionPath)))
        return
    def _checkUndefinedDependenciesExist(self, equation, iStep):
        undef = equation.UndefinedDependencies()
        if len(undef) > 0:
            print("Achtung! Undefined dependencies {:03d} {:s}".format( iStep, equation.Name))
            for u in undef: print( "   " + u)
            return True
        return False
    def _addSequence(self, in_List, iStep, verbose):
        for number in in_List:
            equation = self.byNumber(number)
            if self._checkUndefinedDependenciesExist(equation, iStep):
                return True, iStep
            self.SolutionPath += [ number]
            if verbose:
                print("   {:03d} {:s}".format( iStep, equation.Name))
            iStep += 1
        return False, iStep
    def Produce_Solution_Path(self, verbose=False):
        """
        Locates the execution path
        """
        self.SolutionPath = []
        iStep = 0
        if verbose: print()
        print("Generating solution path")
        
        # parameters and level-types are presumed independent
        Error, iStep = self._addSequence(self.Parameters, iStep, verbose)
        if Error: return
        Error, iStep = self._addSequence(self.Levels, iStep, verbose)
        if Error: return
        to_solve = 0
        for number in self.Dependents:
            if number in self.SolutionPath: continue
            equation = self.byNumber(number)
            if self._checkUndefinedDependenciesExist(equation, iStep):
                return
            to_solve += 1
        to_solve_prev = to_solve
        for npass in range( 1, 101):
            if to_solve <= 0:
                if verbose: 
                    print( "   All {:d} solved".format(len(self.Dependents)))
                break
            if verbose:
                print( "   Pass {:d} to solve {:d} equations".format(npass, to_solve))           
            for number in self.Dependents:
                if number in self.SolutionPath: continue 
                equation = self.byNumber(number)
                if not equation.isResolved( self.SolutionPath): continue
                self.SolutionPath += [ number]
                to_solve -= 1
                if verbose: 
                    print("      {:03d} {{{:03d}}} {:s}".format( iStep, number, equation.Name))
                iStep += 1
            if to_solve == to_solve_prev:
                print( "   Got stuck at {:d} equations".format( to_solve))
                break        
            to_solve_prev = to_solve 

        if to_solve > 0:
            if verbose: print()
            print( "Achtung! Unresolved dependencies: ")
            for number in self.Dependents:
                if number in self.SolutionPath: continue 
                equation = self.byNumber(number)
                print( "      {{{:03}}} {:s}: ".format( equation.Number, equation.Name))
                print( "         ", equation.Dependencies)
            return

        # rate-types are presumed defined at this point
        self._addSequence(self.Rates, iStep, verbose)
        return
    def SubstituteJK(self, expression):
        """
        Substitutes the class variables
        This is to circumvent the jumps across the module
        boundaries in the class definition
        """
        for key in self.Secondary_Dictionary:
            if not key in expression: continue
            equation = self.byName(key)
            nJ = equation.Name + ".J"
            nK = equation.Name + ".K"
            if nJ in expression:
                expression = expression.replace( nJ, str( equation.J))
            if nK in expression:
                expression = expression.replace( nK, str( equation.K))
        return expression
    def EvaluateJK(self, expression, default_value=None):
        """
        Substitutes the class variables and evaluates expression
        """
        expression2 = self.SubstituteJK(expression)
        try:
            res = eval( expression2)
            return res
        except:
            print("Given      : " + expression)
            print("Substituted: " + expression2)
            return default_value
    def LockVariables(self):
        """
        Moves variables to the next iteration
        """
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
        """
        Resets the whole model
        """
        if verbose: print()
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
        """
        Most models need a warm-up to initialize all derivatives
        """
        if verbose: print()
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
        """
        Performs the model computation
        """
        if verbose: print()
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
    def Execute(self,
                dt = 1.0,
                start_time = 1900,
                stop_time = 2100,
                global_policy_year = 1975,
                global_stability_year = 4000,
                warmup_cycles = 10,
                verbose=False):
        """
        Full sequence for production runs
        """
        self.SortByType()
        self.Produce_Solution_Path(verbose)
        self.Reset( dt,
                    start_time,
                    stop_time,
                    global_policy_year,
                    global_stability_year,
                    verbose)
        self.Warmup(warmup_cycles,
                    verbose)
        self.Compute(verbose)
        return
    
        
DYNAMO_Engine = Engine()


class DYNAMO_Base:
    """
    DYNAMO prototype for all other function classes
    """
    def __init__(self,
                 fname,
                 ftype,
                 fpolicy,
                 funits,
                 fupdate,
                 fignore,
                 j, k):
        self.Number = self._extractNumber( fname)
        self.Name = fname
        self.Type = ftype
        self.Policy = fpolicy
        self.Units = funits
        self.UpdateFn = fupdate
        self.Dependencies = self._extractDependencies( fupdate, fignore)
        self.J = j
        self.K = k
        self.Data = []
        DYNAMO_Engine.Register(self)
        return
    def __str__(self):
        s = "{{{:03d}}}\t{:s} {:s} {:s} = ".format(
                self.Number, self.Policy, self.Type, self.Name)
        if self.K is None: s += "<None>"
        else: s += str( self.K)
        s += " [{:s}], {:d} data point(s)".format( self.Units, len( self.Data))
        return s
    def _extractNumber( self, line):
        if len(line) < 5: return 0
        tmp = line[1:4]
        try:
            return int( tmp)
        except:
            return 0
    def _extractDependencies( self, line, ignore):
        """
        class name starts with an underscore, then has 3-digit
        number, then any combination of letters, numbers and underscores
        """
        digits = "0123456789"
        symbols = digits + "_ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
        tmp = []
        pos = 0
        next_name = ""
        in_name = False
        for i, c in enumerate(line):
            in_symbols = c in symbols
            if not in_name and not in_symbols:
                continue
            if in_name and in_symbols:
                next_name += c
                continue
            if not in_name and in_symbols:
                in_name = True
                next_name += c
                continue
            in_name = False
            tmp += [next_name]
            next_name = ""
        ret = []
        for s in tmp:
            if s[0] != '_' : continue
            if not s[1] in digits: continue
            if not s[2] in digits: continue
            if not s[3] in digits: continue
            if s[4] != '_' : continue
            if s in ignore: continue
            ret += [s]
        return ret
    def UndefinedDependencies(self):
        tmp = []
        for dependence in self.Dependencies:
            if dependence in DYNAMO_Engine.Secondary_Dictionary: continue
            tmp += [dependence]
        return tmp
    def isResolved(self, in_List):
        for dependence in self.Dependencies:
            eq = DYNAMO_Engine.byName(dependence)
            if eq.Type == "Rate": continue # rates are presumed defined
            if not eq.Number in in_List: return False
        return True
    def Reset(self):
        self.J = None
        self.K = None
        self.Data = []
        return
    def Warmup(self):
        return
    def Update(self):
        self.Warmup()
        self.Data += [self.K]
        return
    def Lock(self):
        self.J = self.K
        return
   

class Parameter(DYNAMO_Base):
    """
    DYNAMO prototype for a fixed value
    """
    def __init__(self,
                 fname,
                 fvalue,
                 funits="unitless"):
        DYNAMO_Base.__init__(self,
                             fname,
                             "Parameter",
                             "Fixed",
                             funits,
                             "", [],
                             fvalue, fvalue)
        self.Value = fvalue
        self.Reset()
        return
    def Reset(self):
        self.J = self.Value
        self.K = self.Value
        self.Data = []
        return


class PolicyParametrization(DYNAMO_Base):
    """
    DYNAMO prototype for selecting parameter before and after policy implementation
    This is essentially a Heaviside step function aH(t-to)+b
    """
    def __init__(self,
                 fname,
                 value_before,
                 value_after,
                 funits="unitless"):
        DYNAMO_Base.__init__(self,
                             fname,
                             "Parameter",
                             "Policy",
                             funits,
                             "", [],
                             value_before, value_before)
        self.BeforePolicy = value_before
        self.AfterPolicy = value_after
        self.Reset()
        return
    def Reset(self):
        DYNAMO_Base.Reset(self)
        self.J = DYNAMO_Engine.SelectByGlobalPolicy(
            self.BeforePolicy,
            self.BeforePolicy,
            self.AfterPolicy,
            self.AfterPolicy)
        self.K = self.J
        self.Data = []
        return
    def Warmup(self):
        self.K = DYNAMO_Engine.SelectByGlobalPolicy(
            self.BeforePolicy,
            self.BeforePolicy,
            self.AfterPolicy,
            self.AfterPolicy)
        return


class TableParametrization(DYNAMO_Base):
    """
    DYNAMO prototype for a parametrization as
    a numeric table with linear interpolation between the values
    """
    def __init__(self,
                 fname,
                 fpoints, imin, imax,
                 funits="unitless",
                 fpoints_1940 = None,
                 fpoints_after_policy = None,
                 fupdate = "",
                 fignore = [],
                 initialValue = None):
        DYNAMO_Base.__init__(self,
                             fname,
                             "Table",
                             "Fixed",
                             funits,
                             fupdate,
                             fignore,
                             None, None)
        self.InitialValue = initialValue
        self.Points1940 = None
        self.PointsBefore = np.array( fpoints)
        self.PointsAfter = None
        if fpoints_1940 is not None:
            self.Points1940 = np.array( fpoints_1940)
        if fpoints_after_policy is not None:
            self.PointsAfter = np.array( fpoints_after_policy)
            self.PolicyInput = "Policy"
        self.Indices = np.linspace( imin, imax, len(fpoints))
        self.Delta = self.Indices[1]-self.Indices[0]
        return
    def Lookup( self, v):
        data = DYNAMO_Engine.SelectByGlobalPolicy(
            self.Points1940,
            self.PointsBefore,
            self.PointsAfter,
            self.PointsAfter)
        if data is None or len(data) != len(self.Indices):
            print("Achtung! Table " + self.Name + " is missing points")
            return None
        if v <= self.Indices[0] : return data[ 0]
        if v >= self.Indices[-1]: return data[-1]
        for i, vi in enumerate( self.Indices):
            if vi <= v and v < self.Indices[i+1]:
                f = (v-vi) / self.Delta
                return data[i]*(1-f) + data[i+1]*f
        return data[-1]
    def Warmup( self):
        v = DYNAMO_Engine.EvaluateJK( self.UpdateFn, self.InitialValue)
        if v is None:
            self.K = None
            print( "Achtung! Table " + self.Name)
            return
        self.K = self.Lookup( v)
        return


class LevelVariable(DYNAMO_Base):
    """
    DYNAMO prototype for a level variable
    it computes a derivative by fupdate and
    changes own value; all dependencies presumed
    resolved;
    """
    def __init__(self,
                 fname,
                 initialValue,
                 funits="unitless",
                 fupdate=""):
        DYNAMO_Base.__init__(self,
                             fname,
                             "Level",
                             "Variable",
                             funits,
                             fupdate,
                             [],
                             initialValue, initialValue)
        self.InitialValue = initialValue
        self.Reset()
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
        rate = DYNAMO_Engine.EvaluateJK( self.UpdateFn)
        if rate is None:
            print("Achtung! Level " + self.Name + " unable to compute rate " + self.UpdateFn)
            rate = 0.0
        self.K = self.J + rate * DYNAMO_Engine.dt
        self.Data += [self.K]
        return


class RateVariable(DYNAMO_Base):
    """
    DYNAMO prototype for a rate change variable
    """
    def __init__(self,
                 fname,
                 funits="unitless",
                 fupdate="",
                 fequilibrium=None):
        DYNAMO_Base.__init__(self,
                             fname,
                             "Rate",
                             "Variable",
                             funits,
                             fupdate,
                             [],
                             0, 0)
        self.EquilibriumFn = fequilibrium
        self.Reset()
        return
    def _selectUpdateFunction(self):
        fn = DYNAMO_Engine.SelectByGlobalPolicy(
            self.UpdateFn,
            self.UpdateFn,
            self.UpdateFn,
            self.EquilibriumFn)
        if fn is None or len(fn)<=0:
            print("Achtung! Rate " + self.Name + " has no update function")
            self.J = 0
            self.K = 0
            return None
        return fn
    def Reset(self):
        self.J = 0
        self.K = 0
        self.Data = []
        return
    def Warmup(self):
        fn = self._selectUpdateFunction()
        if fn is None: return
        self.K = DYNAMO_Engine.EvaluateJK( fn)
        if self.K is None:
            self.J = 0.0
            self.K = 0.0
            print( "Achtung! " + self.Name + ".J and .K replaced  with zeros in warm-up")
        self.J = self.K 
        return
    def Update(self):
        fn = self._selectUpdateFunction()
        if fn is None: return
        self.K = DYNAMO_Engine.EvaluateJK( fn)
        if self.K is None:
            self.K = 0.0
            print( "Achtung! " + self.Name + ".K replaced  with zeros in update")
        self.Data += [self.K]
        return


class AuxVariable(DYNAMO_Base):
    """
    DYNAMO prototype for an auxillary variable
    """
    def __init__(self,
                 fname,
                 funits="unitless",
                 fupdate = "",
                 fignore = [],
                 fequilibrium=None):
        DYNAMO_Base.__init__(self,
                             fname,
                             "Aux",
                             "Variable",
                             funits,
                             fupdate,
                             fignore,
                             None, None)
        self.EquilibriumFn = fequilibrium
        self.Reset()
        return
    def _selectUpdateFunction(self):
        fn = DYNAMO_Engine.SelectByGlobalPolicy(
            self.UpdateFn,
            self.UpdateFn,
            self.UpdateFn,
            self.EquilibriumFn)
        if fn is None:
            print("Achtung! Aux " + self.Name + " has no update function")
            self.J = None
            self.K = None
        return fn
    def Warmup(self):
        fn = self._selectUpdateFunction()
        if fn is None: return
        self.K = DYNAMO_Engine.EvaluateJK( fn)
        if self.K is None:
            print( "Achtung! " + self.Name + ".K is undefined")
        return

       
class SmoothVariable(DYNAMO_Base):
    """
    DYNAMO prototype for an auxillary dependency with smoothing
    if initialValue is not None, dependency is ignored; this is used to
    break determination cycles
    """
    def __init__(self,
                 fname,
                 fdelay="1.0",
                 funits="unitless",
                 fupdate="",
                 initialValue = None):
        DYNAMO_Base.__init__(self,
                             fname,
                             "Smooth",
                             "Variable",
                             funits,
                             fupdate,
                             [],
                             initialValue, initialValue)
        self.DelayFn = fdelay
        self.InitialValue = initialValue
        if initialValue is not None:
            self.Dependencies = []
        self.Reset()
        return
    def Reset(self):
        self.J = self.InitialValue
        self.K = self.InitialValue
        self.isFirstCall = True
        self.Data = []
        return
    def Warmup(self):
        if self.InitialValue is not None:
            self.J = self.InitialValue
            self.K = self.InitialValue
            return
        self.J = DYNAMO_Engine.EvaluateJK( self.UpdateFn)
        self.K = self.J
        if self.K is None:
            print( "Achtung! Smooth " + self.Name + " - value error")
        return
    def Update(self):
        if self.isFirstCall:
            self.J = DYNAMO_Engine.EvaluateJK( self.UpdateFn)
            self.K = self.J
            self.isFirstCall = False
            self.Data += [self.K]
            return
        v = DYNAMO_Engine.EvaluateJK( self.UpdateFn.replace(".K", ".J"))
        d1 = DYNAMO_Engine.dt / DYNAMO_Engine.EvaluateJK( self.DelayFn)
        d0 = (1-d1)
        self.K = d1 * self.J + d0 * v
        self.Data += [self.K]
        return


class DelayVariable(DYNAMO_Base):
    """
    DYNAMO prototype for third-order exponential delay Rate variables
    """
    def __init__(self,
                 fname,
                 fdelay="1.0",
                 funits="unitless",
                 fupdate="",
                 initialValue = None):
        DYNAMO_Base.__init__(self,
                             fname,
                             "Delay",
                             "Variable",
                             funits,
                             fupdate,
                             [],
                             initialValue, initialValue)
        self.DelayFn = fdelay
        self.InitialValue = initialValue
        if initialValue is not None:
            self.Dependencies = []
        self.Reset()
        return
    def Reset(self):
        self.J = self.InitialValue
        self.K = self.InitialValue
        self.isFirstCall = True
        self.alpha = self.InitialValue
        self.beta  = self.InitialValue
        self.gamma = self.InitialValue
        self.Data = []
        self.isFirstCall = True
        self.Data = []        
        return
    def Warmup(self):
        if self.InitialValue is not None:
            self.J = self.InitialValue
            self.K = self.InitialValue
        else:
            self.J = DYNAMO_Engine.EvaluateJK( self.UpdateFn)
            self.K = self.J
        if self.K is None:
            print( "Achtung! Delay " + self.Name + ".K not defined")
        self.alpha = self.K
        self.beta  = self.K
        self.gamma = self.K
        return
    def Update(self):
        if self.isFirstCall:
            self.J = DYNAMO_Engine.EvaluateJK( self.UpdateFn)
            self.K = self.J
            self.alpha = self.K
            self.beta  = self.K
            self.gamma = self.K
            self.isFirstCall = False
            self.Data += [self.K]
            return
        v = DYNAMO_Engine.EvaluateJK( self.UpdateFn.replace(".K", ".J"))
        d1 = DYNAMO_Engine.dt * 3 / DYNAMO_Engine.EvaluateJK( self.DelayFn)
        d0 = (1-d1)
        alphaK = d0 * self.alpha + d1 * v
        betaK  = d0 * self.beta  + d1 * self.alpha
        self.K = d0 * self.gamma + d1 * self.beta
        self.alpha = alphaK
        self.beta  = betaK
        self.gamma = self.K
        self.Data += [self.K]
        return


class meaningOfLife:
    """
    Ultimate Question of Life, The Universe, and Everything 
    """
    def __init__(self):
        self.J = 42
        self.K = 42


# Generic checks
if __name__ == "__main__":
    print()
    print("Check Parameter:")
    _042_Meaning_Of_Life = Parameter(
    "_042_Meaning_Of_Life", 42, "gigs")
    _042_Meaning_Of_Life.Reset()
    print("   Reset: ", _042_Meaning_Of_Life)
    _042_Meaning_Of_Life.Warmup()
    print("   Warmup: ", _042_Meaning_Of_Life)
    _042_Meaning_Of_Life.Update()
    print("   Update: ", _042_Meaning_Of_Life)
    _042_Meaning_Of_Life.Lock()
    print("   Lock: ", _042_Meaning_Of_Life.J, _042_Meaning_Of_Life.K, _042_Meaning_Of_Life)

    print()
    print("Check Policy Parametrization:")
    _201_foodPerCapita = PolicyParametrization(
        "foodPerCapita",
        800, 400, "kg / person / year")

    _201_foodPerCapita.Reset()
    print("   Reset: ", _201_foodPerCapita)
    _201_foodPerCapita.Warmup()
    print("   Warmup: ", _201_foodPerCapita)
    _201_foodPerCapita.Update()
    print("   Update: ", _201_foodPerCapita)
    _201_foodPerCapita.Lock()
    print("   Lock: ", _201_foodPerCapita.J, _201_foodPerCapita.K, _201_foodPerCapita)

    print()
    print("Check Table Parametrization:")
    _004_mortality0To14 = TableParametrization(
    "_004_mortality0To14",
    [0.0567, 0.0366, 0.0243, 0.0155, 0.0082, 0.0023, 0.0010],
    20, 80, "deaths / person / year",
    fupdate = "_042_Meaning_Of_Life.K")
    _004_mortality0To14.Reset()
    print("   Reset: ", _004_mortality0To14)
    _004_mortality0To14.Warmup()
    print("   Warmup: ", _004_mortality0To14)
    _004_mortality0To14.Update()
    print("   Update: ", _004_mortality0To14)
    _004_mortality0To14.Lock()
    print("   Lock: ", _004_mortality0To14.J, _004_mortality0To14.K, _004_mortality0To14)
    PlotTable( _004_mortality0To14, 0, 100, xLabel="(Test only) lifeExpectancy [years]", show=True)

    print()
    print("Check Level Variable:")
    _002_population0To14 = LevelVariable(
    "_002_population0To14",
    6.5e8, "persons",
    fupdate = "_030_birthsPerYear.J - "
                " - deathsPerYear0To14.J"
                " - maturationsPerYear14to15.J")
    _002_population0To14.Reset()
    print("   Reset: ", _002_population0To14)
    _002_population0To14.Warmup()
    print("   Warmup: ", _002_population0To14)
    _002_population0To14.Update()
    print("   Update: ", _004_mortality0To14)
    _002_population0To14.Lock()
    print("   Lock: ", _002_population0To14, _002_population0To14, _002_population0To14)

