from DYNAMO_Prototypes import *

#
# Checks SMOOTH and DELAY3 implementation
#

Step_Function = PolicyParametrization(
    "_401_Step_Function",
    100, 120, "units")

SmoothOutput = SmoothVariable(
    "_402_Smooth_Output",
    "10",
    "units",
    "_401_Step_Function.K")

Delay3Output = DelayVariable(
    "_403_Delay_Output",
    "10",
    "units",
    "_401_Step_Function.K")

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
PlotVariable( Step_Function, DYNAMO_Engine.Model_Time,
    filename="./Test_Graphs/WORLD3_Subsystem_Test_{:s}.png",
    show=True)
PlotVariable( SmoothOutput, DYNAMO_Engine.Model_Time,
    filename="./Test_Graphs/WORLD3_Subsystem_Test_{:s}.png",
    show=True)
PlotVariable( Delay3Output, DYNAMO_Engine.Model_Time,
    filename="./Test_Graphs/WORLD3_Subsystem_Test_{:s}.png",
    show=True)
