from DYNAMO_Prototypes import *

#
# Checks DELAY3 implementation
#

Delay3Input = PolicyParametrization(
    "_401_Delay_Input",
    100, 120, "units")

Delay3Output = DelayVariable(
    "_402_Delay_Output",
    "10",
    "units",
    "_401_Delay_Input.K")

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
PlotVariable( Delay3Input, DYNAMO_Engine.Model_Time,
    filename="./Test_Graphs/WORLD3_Subsystem_Test_{:s}.png",
    show=True)
PlotVariable( Delay3Output, DYNAMO_Engine.Model_Time,
    filename="./Test_Graphs/WORLD3_Subsystem_Test_{:s}.png",
    show=True)
