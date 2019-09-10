from WORLD3_Services_Subsystem import *

#
# This run checks the subsystems running together: 
#    - population,
#    - industry,
#    - services
# The agriculture outputs per capita
# is presumed constant (equations {202}-{207})
#


#
# LABOR SUBSYSTEM (equations {73}-{83})
#
lab073 = AuxVariable(
    73, "jobs", "persons",
    ["potentialJobsInIndustrialSector",
    "potentialJobsInAgriculturalSector",
    "potentialJobsInServiceSector"],
    lambda : \
    lab073.Kof("potentialJobsInIndustrialSector") + \
    lab073.Kof("potentialJobsInAgriculturalSector") + \
    lab078.Kof("potentialJobsInServiceSector"))

lab074 = AuxVariable(
    74, "potentialJobsInIndustrialSector", "persons",
    ["jobsPerIndustrialCapitalUnit"],
    lambda : \
    lab074.Kof("industrialCapital") * \
    lab074.Kof("jobsPerIndustrialCapitalUnit"))

lab075 = TableParametrization(
    75, "jobsPerIndustrialCapitalUnit",
    [0.00037, 0.00018, 0.00012, 0.00009, 0.00007, 0.00006],
    50, 800, "persons / dollar",
    dependencies = ["industrialOutputPerCapita"])

lab076 = AuxVariable(
    76, "potentialJobsInServiceSector", "persons",
    ["jobsPerServiceCapitalUnit"],
    lambda : \
    lab076.Kof("serviceCapital") * \
    lab076.Kof("jobsPerServiceCapitalUnit"))

lab077 = TableParametrization(
    77, "jobsPerServiceCapitalUnit",
    [.0011, 0.0006, 0.00035, 0.0002, 0.00015, 0.00015],
    50, 800, "persons / dollar",
    dependencies = ["serviceOutputPerCapita"])

lab078 = AuxVariable(
    78, "potentialJobsInAgriculturalSector", "persons",
    ["jobsPerHectare"],
    lambda : lab078.Kof("arableLand") * \
    lab078.Kof("jobsPerHectare"))

lab079 = TableParametrization(
    79, "jobsPerHectare",
    [2, 0.5, 0.4, 0.3, 0.27, 0.24, 0.2, 0.2],
    2, 30, "persons / hectare",
    dependencies = ["agriculturalInputsPerHectare"])

lab080 = AuxVariable(
    80, "laborForce", "persons",
    updatefn = lambda : \
    0.75 * (lab080.Kof("population15To44") + \
    lab080.Kof("population45To64"))) # 0.75 - participation fraction

lab081 = AuxVariable(
    81, "laborUtilizationFraction",
    dependencies = ["jobs", "laborForce"],
    updatefn = lambda : lab081.Kof("jobs") / \
    lab081.Kof("laborForce"))

lab082 = SmoothVariable(
    82, "laborUtilizationFractionDelayed",
    lambda: lab082.Kof("laborUtilizationFractionDelayTime"),
    dependencies = ["laborUtilizationFraction"])

lab083 = TableParametrization(
    83, "capitalUtilizationFraction",
    [1.0, 0.9, 0.7, 0.3, 0.1, 0.1], 1, 11,
    dependencies = ["laborUtilizationFractionDelayed"], # will be taken over by initialValue 
    updatefn = lambda : lab083.Kof("laborUtilizationFractionDelayed"),
    initialValue = 1.0)


#
# PARAMETERS
#
par158 = Parameter(
    158, "laborUtilizationFractionDelayTime", 2,
    [82], "years")


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
        205, "agriculturalInputsPerHectare", 1, 1,
        "dollars / hectare / year")

    par206 = PolicyParametrization(
        206, "fractionOfIndustrialOutputAllocatedToAgriculture", 0.2, 0.2,
        "unitless")

    par207 = Parameter(
        207, "arableLand", 0.9e9,
        [])

    #
    #Test_Run
    #
    DYNAMO_Engine.SortByType()
    DYNAMO_Engine.ListEquations()
    DYNAMO_Engine.Produce_Solution_Path( verbose = True)
    DYNAMO_Engine.ListSolutionPath()
    DYNAMO_Engine.Reset(
        dt=4, global_policy_year=2020,
        global_stability_year=2050,
        verbose = True)
    DYNAMO_Engine.Warmup( verbose = True)
    DYNAMO_Engine.Compute( verbose = True)
    PlotVariable( "population", DYNAMO_Engine.Model_Time,
                  filename="./Graphs/WORLD3_Subsystem_Test_{:s}.png", show=True)
