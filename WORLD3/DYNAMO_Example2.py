from DYNAMO_Prototypes import *

#
# Solves Malthus-Verhulst equation
#

_002_Population = LevelVariable(
    "_002_Population",
    1e8, "persons",
    fupdate = "_003_Growth_Rate.J"
    " * (1 - _002_Population.J / _004_Population_Optimum.J)"
    " * _002_Population.J")

_003_Growth_Rate = Parameter(
    "_003_Growth_Rate",
    0.10, "person / person / year")

_004_Population_Optimum = Parameter(
    "_004_Population_Optimum",
    2e9, "persons")

DYNAMO_Engine.SortByType()
DYNAMO_Engine.ListEquations()
DYNAMO_Engine.Produce_Solution_Path( verbose = True)
DYNAMO_Engine.ListSolutionPath()
DYNAMO_Engine.Reset( dt=5)
DYNAMO_Engine.Warmup( )
DYNAMO_Engine.Compute( )
PlotVariable( _002_Population, DYNAMO_Engine.Model_Time,
    filename="./Test_Graphs/WORLD3_Subsystem_Test_{:s}.png",
    show=True)
