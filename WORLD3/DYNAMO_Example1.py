from DYNAMO_Prototypes import *

#
# Solves exponential equation
#

_001_Population = LevelVariable(
    "_001_Population",
    1e8, "persons",
    fupdate = "_002_Growth_Rate.J * _001_Population.J")

_002_Growth_Rate = Parameter(
    "_002_Growth_Rate",
    0.03, "person / person / year")

DYNAMO_Engine.SortByType()
DYNAMO_Engine.ListEquations()
DYNAMO_Engine.Produce_Solution_Path( verbose = True)
DYNAMO_Engine.ListSolutionPath()
DYNAMO_Engine.Reset( dt=5)
DYNAMO_Engine.Warmup( )
DYNAMO_Engine.Compute( )
PlotVariable( _001_Population, DYNAMO_Engine.Model_Time,
    filename="./Test_Graphs/WORLD3_Subsystem_Test_{:s}.png",
    show=True)
