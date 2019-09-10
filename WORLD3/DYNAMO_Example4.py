from DYNAMO_Prototypes import *

#
# Checks SMOOTH implementation
#

Smooth3Input = PolicyParametrization(
    "_403_Smooth_Input",
    100, 120, "units")

Smooth3Output = DelayVariable(
    "_404_Smooth_Output",
    "10",
    "units",
    "_403_Smooth_Input.K")

DYNAMO_Engine.SortByType()
DYNAMO_Engine.ListEquations()
DYNAMO_Engine.Produce_Solution_Path( verbose = True)
#DYNAMO_Engine.ListSolutionPath()
DYNAMO_Engine.Reset( dt=0.5,
                     start_time = 1940,
                     stop_time = 1980,
                     global_policy_year = 1950)
#DYNAMO_Engine.Warmup( )
DYNAMO_Engine.Compute( )
PlotVariable( Smooth3Input, DYNAMO_Engine.Model_Time,
    filename="./Test_Graphs/WORLD3_Subsystem_Test_{:s}.png",
    show=True)
PlotVariable( Smooth3Output, DYNAMO_Engine.Model_Time,
    filename="./Test_Graphs/WORLD3_Subsystem_Test_{:s}.png",
    show=True)
