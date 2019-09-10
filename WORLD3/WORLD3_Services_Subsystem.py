from WORLD3_Industry_Subsystem import *

#
# This run checks the population, industry, and services subsystems
# running together. The agriculture outputs per capita
# is presumed constant (equations {202}-{206})
#

#
# SERVICES SUBSYSTEM (equations {60}, {63}, {66}-{72})
#
svc060 = TableParametrization(
    60, "indicatedServiceOutputPerCapita",
    [40, 300, 640, 1000, 1220, 1450, 1650, 1800, 2000],
    0, 1600, "dollars / person / year",
    data_after_policy = [40, 300, 640, 1000, 1220, 1450, 1650, 1800, 2000],
    dependencies = ["industrialOutputPerCapita"])

#
# svc061, svc062 - used to be policy tables, now in {svc060}
#

svc063 = TableParametrization(
    63, "fractionOfIndustrialOutputAllocatedToServices",
    [0.3, 0.2, 0.1, 0.05, 0], 0, 2,
    data_after_policy = [0.3, 0.2, 0.1, 0.05, 0],
    dependencies = ["serviceOutputPerCapita",
                    "indicatedServiceOutputPerCapita"],
    updatefn = lambda : svc063.Kof("serviceOutputPerCapita") / \
    svc063.Kof("indicatedServiceOutputPerCapita"))

#
# svc064, svc065 - used to be policy tables, now in {svc063}
#

svc066 = RateVariable(
    66, "serviceCapitalInvestmentRate", "dollars / year",
    lambda : svc066.Kof("industrialOutput") * \
    svc066.Kof("fractionOfIndustrialOutputAllocatedToServices"))

svc067 = LevelVariable(
    67, "serviceCapital", 1.44e11, "dollars",
    updatefn = lambda : \
    svc067.Jof("serviceCapitalInvestmentRate") - \
    svc067.Jof("serviceCapitalDepreciationRate"))

svc068 = RateVariable(
    68, "serviceCapitalDepreciationRate", "dollars / year",
    lambda : svc068.Kof("serviceCapital") / \
    svc068.Kof("averageLifetimeOfServiceCapital"))

svc069 = PolicyParametrization(
    69, "averageLifetimeOfServiceCapital", 20, 20, "years")

svc070 = AuxVariable(
    70, "serviceOutput", "dollars / year",
    ["capitalUtilizationFraction", "serviceCapitalOutputRatio"],
    lambda : svc070.Kof("serviceCapital") * \
    svc070.Kof("capitalUtilizationFraction") / \
    svc070.Kof("serviceCapitalOutputRatio"))

svc071 = AuxVariable(
    71, "serviceOutputPerCapita", "dollars / person / year",
    ["serviceOutput", "population"],
    lambda : svc071.Kof("serviceOutput") / \
    svc071.Kof("population"))

svc072 = PolicyParametrization(
    72, "serviceCapitalOutputRatio", 1, 1, "years")

#
# No PARAMETERS declared for INDUSTRY
#

if __name__ == "__main__":

    #
    # FIXED PARAMETERS (this test only)
    #
    par202 = PolicyParametrization(
        202, "foodPerCapita", 800, 400,
        "kg / person / year")

    par203 = Parameter(
        203, "indexOfPersistentPollution", 1,
        [])

    par204 = PolicyParametrization(
        204, "fractionOfCapitalAllocatedToObtainingResources", 0.10, 0.10,
        "unitless")

    par205 = PolicyParametrization(
        205, "capitalUtilizationFraction", 0.7, 0.7,
        "unitless")

    par206 = PolicyParametrization(
        206, "fractionOfIndustrialOutputAllocatedToAgriculture", 0.2, 0.2,
        "unitless")

    #
    #Test_Run
    #
    DYNAMO_Engine.SortByType()
    DYNAMO_Engine.ListEquations()
    DYNAMO_Engine.Produce_Solution_Path( verbose = True)
    DYNAMO_Engine.ListSolutionPath()
    DYNAMO_Engine.Reset(
        dt=5, global_policy_year=2020,
        global_stability_year=2050,
        verbose = True)
    DYNAMO_Engine.Warmup( verbose = True)
    DYNAMO_Engine.Compute( verbose = True)
    PlotVariable( "population", DYNAMO_Engine.Model_Time,
                  filename="./Graphs/WORLD3_Subsystem_Test_{:s}.png", show=True)
