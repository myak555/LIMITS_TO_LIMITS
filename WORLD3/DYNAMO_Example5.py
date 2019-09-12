from DYNAMO_Prototypes import *

#
# Time function check
#

##IndustrialOutput = AuxVariable(
##    "_050_IndustrialOutput", "dollars / year",
##    fupdate = "_052_IndustrialCapital.K / 3"
##    "* (1 - _134_FractionOfCapitalAllocatedToObtainingResources.K)")
##
##IndustrialCapital = LevelVariable(
##    "_052_IndustrialCapital", "210e9", "dollars",
##    fupdate = "_050_IndustrialOutput.J * 0.25"
##    "- _052_IndustrialCapital.J / 14")
##

_501_Population_Reference = AuxVariable(
    "_501_Population_Reference", "persons",
    fupdate = "_601_Population_Digitized.K * 1.6e8")

_519_Population_Reference = AuxVariable(
    "_519_LifeExpectancy_Reference", "persons",
    fupdate = "_619_LifeExpectancy_Digitized.K * 0.8")

_549_IndustrialOutputPerCapita_Reference = AuxVariable(
    "_549_IndustrialOutputPerCapita_Reference", "dollars / person / year",
    fupdate = "_649_Goods_Digitized.K * 5")

_571_ServiceOutputPerCapita_Reference = AuxVariable(
    "_571_ServiceOutputPerCapita", "dollars / person / year",
    fupdate = "_671_Services_Digitized.K * 1e11 / _501_Population_Reference.K")

_588_FoodPerCapita_Reference = AuxVariable(
    "_588_FoodPerCapita_Reference", "kg / person / year",
    fupdate = "_688_FoodPerCapita_Digitized.K * 10")

_629_NonrenewableResources = AuxVariable(
    "_629_NonrenewableResources", "resource units",
    fupdate = "_729_Resources_Digitized.K * 1e10")

_643_IndexOfPersistentPollution = AuxVariable(
    "_643_IndexOfPersistentPollution", "unitless",
    fupdate = "_743_PollutionIndex_Digitized.K * 0.32")

_601_Population_Digitized = TableParametrization(
    "_601_Population_Digitized",
    [10.428, 10.963, 11.530, 12.032, 12.834,
    13.636, 14.439, 15.241, 16.364, 17.647,
    18.984, 20.588, 22.460, 24.332, 26.471,
    28.610, 31.016, 33.690, 36.631, 39.305,
    42.246, 45.187, 48.128, 51.070, 53.743,
    55.882, 57.487, 58.021, 57.487, 56.150,
    53.476, 50.267, 47.594, 44.920, 42.513,
    40.107, 38.235, 36.265, 34.492, 33.155, 31.818],
    1900, 2100,
    fupdate = "DYNAMO_Engine.time")

_619_LifeExpectancy_Digitized = TableParametrization(
    "_619_LifeExpectancy_Digitized",
    [41.176,40.642,40.642,40.909,40.909,
    41.176,41.711,42.246,47.594,49.733,
    50.802,51.872,53.476,55.080,56.952,
    58.824,60.963,62.567,63.904,64.973,
    66.578,67.914,69.251,70.856,71.925,
    71.925,70.321,66.043,59.626,52.674,
    45.989,43.583,43.048,40.107,38.235,
    36.898,35.829,35.027,34.492,34.225,34.225],
    1900, 2100,
    fupdate = "DYNAMO_Engine.time")

_649_Goods_Digitized = TableParametrization(
    "_649_Goods_Digitized",
    [8.824,10.160,10.963,12.299,13.636,
    15.241,17.112,19.251,21.390,23.262,
    25.134,27.540,29.947,32.353,35.294,
    38.235,40.909,43.316,45.989,48.930,
    51.604,54.545,57.754,60.428,61.230,
    59.358,52.139,39.305,32.353,26.471,
    21.658,17.914,14.973,12.567,10.428,
     8.556, 7.219, 6.150, 5.080, 4.011, 3.209],
    1900, 2100,
    fupdate = "DYNAMO_Engine.time")

_671_Services_Digitized = TableParametrization(
    "_671_Services_Digitized",
    [1.604,1.604,1.872,2.139,2.406,
    2.674,3.209,3.476,4.011,4.813,
    5.615,6.417,7.487,8.824,10.428,
    12.032,13.904,16.310,18.984,21.925,
    24.866,28.342,32.086,36.631,40.107,
    42.781,43.583,40.107,34.759,29.679,
    24.332,20.856,16.845,13.904,11.497,
    9.358,7.754,6.684,5.615,4.545,3.743],
    1900, 2100,
    fupdate = "DYNAMO_Engine.time")

_688_FoodPerCapita_Digitized = TableParametrization(
    "_688_FoodPerCapita_Digitized",
    [28.877,27.807,28.075,28.877,29.412,
    30.214,31.283,32.086,33.690,33.957,
    35.294,35.829,37.433,38.503,39.305,
    39.572,39.840,39.840,39.840,40.107,
    40.107,40.107,40.107,39.840,39.037,
    37.701,35.294,29.679,25.668,21.658,
    20.321,20.053,20.588,19.786,19.519,
    18.717,18.984,19.251,19.519,19.786,20.053],
    1900, 2100,
    fupdate = "DYNAMO_Engine.time")

_729_Resources_Digitized = TableParametrization(
    "_729_Resources_Digitized",
    [100.267,100.267,100.000,99.733,99.465,
    99.198,98.930,98.396,97.861,97.326,
    96.524,95.722,94.652,93.583,92.246,
    90.374,88.503,86.364,83.422,79.947,
    75.936,71.390,65.508,58.824,51.872,
    44.652,37.166,32.086,28.877,26.203,
    23.797,22.193,21.123,20.053,18.717,
    18.182,17.914,17.380,17.112,16.845,15.775],
    1900, 2100,
    fupdate = "DYNAMO_Engine.time")

_743_PollutionIndex_Digitized = TableParametrization(
    "_743_PollutionIndex_Digitized",
    [0.802,0.802,0.802,0.802,0.802,
    0.802,1.070,1.070,1.337,1.337,
    1.872,1.872,2.406,2.674,3.209,
    3.743,4.545,5.348,6.417,7.754,
    9.358,10.963,13.369,16.310,19.786,
    23.529,28.342,32.888,35.829,36.364,
    34.225,30.214,25.668,21.123,16.845,
    13.102,10.160,8.021,6.417,4.813,3.743],
    1900, 2100,
    fupdate = "DYNAMO_Engine.time")

DYNAMO_Engine.SortByType()
DYNAMO_Engine.ListEquations()
DYNAMO_Engine.Produce_Solution_Path( verbose = True)
DYNAMO_Engine.ListSolutionPath()
DYNAMO_Engine.Reset( dt=5)
DYNAMO_Engine.Warmup( )
DYNAMO_Engine.Compute( )

#PlotVariable( _501_Population_Reference, DYNAMO_Engine.Model_Time,
#    filename="./Test_Graphs/WORLD3_Subsystem_Test_{:s}.png",
#    show=True)

PlotVariable( _549_IndustrialOutputPerCapita_Reference, DYNAMO_Engine.Model_Time,
    filename="./Test_Graphs/WORLD3_Subsystem_Test_{:s}.png",
    show=True)
