from Utilities import *

def GetFile( data_name, sum_data_EIA, sum_well_HP, sum_well_HA, sum_well_P, sum_well_A, proj_name="Hughes2014"):
    bft2bmy = 0.3048**3 * 365
    Y,AEO2016,Hughes,Actual = Load_Calibration(
        data_name,
        ["Year", "AEO2016", proj_name, "Actual"])
    AEO2016 *= bft2bmy 
    Hughes *= bft2bmy
    Actual *= bft2bmy
    sp = int( Y[0] - 1994)
    for i in range( sp, len(sum_data_EIA)):
        sum_data_EIA[i] += AEO2016[i-sp]
        sum_well_HP[i] += Hughes[i-sp]
        sum_well_HA[i] += Actual[i-sp]
    dumm = Load_Calibration( data_name, ["Wells_Plan", "Wells_Actual"])
    if len(dumm) != 2: return np.array( sum_well_HP)
    (WP,WA) = dumm
    if len(WP) < 1: return np.array( sum_well_HP)
    for i in range( sp, len(sum_data_EIA)):
        sum_well_P[i] += WP[i-sp]
        sum_well_A[i] += WA[i-sp]
    return np.array( sum_well_HP)

def GetGas( name_en, data_name, metric = True):
    Year, AEO2014, AEO2015, AEO2016, Hughes2014, Actual, WP, WA = Load_Calibration(
        data_name,
        ["Year", "AEO2014", "AEO2015", "AEO2016", "Hughes2014", "Actual", "Wells_Plan", "Wells_Actual"])
    YC,PC = Load_Calibration( "./Data/US12_US_Tight_Gas_EIA.csv", ["Year", name_en])
    if metric:
        ft2m = 0.3048**3
        AEO2014 *= ft2m   
        AEO2015 *= ft2m   
        AEO2016 *= ft2m   
        Hughes2014 *= ft2m   
        Actual *= ft2m   
        AEO2014 *= 365   
        AEO2015 *= 365   
        AEO2016 *= 365   
        Hughes2014 *= 365   
        Actual *= 365   
    return Year, AEO2014, AEO2015, AEO2016, Hughes2014, Actual, WP, WA, YC, PC

def GetOil( name_en, data_name, metric = True):
    Year, AEO2014, AEO2015, AEO2016, Hughes2014, Actual, WP, WA = Load_Calibration(
        data_name,
        ["Year", "AEO2014", "AEO2015", "AEO2016", "Hughes2014", "Actual", "Wells_Plan", "Wells_Actual"])
    YC,PC = Load_Calibration( "./Data/US22_US_Tight_Oil_EIA.csv", ["Year", name_en])
    if metric:
        b2t = 0.159 * 0.827 
        bd2ty = b2t * 365 
        AEO2014 *= bd2ty    
        AEO2015 *= bd2ty   
        AEO2016 *= bd2ty   
        Hughes2014 *= bd2ty   
        Actual *= bd2ty   
        PC *= b2t
    else:
        PC /= 365
    return Year, AEO2014, AEO2015, AEO2016, Hughes2014, Actual, WP, WA, YC, PC

def Get_Oil_Others( ):
    Year,AEO2016 = Load_Calibration( "./Data/US20_Others_Oil.csv", ["Year", "AEO2016"]) 
    YC,PC1,PC2,PC3,PC4,PC5,PC6,PC7 = Load_Calibration(
        "./Data/US22_US_Tight_Oil_EIA.csv",
        ["Year", "Monterey", "Granite_Wash", "Marcellus", "Haynesville", "Yeso_Glorieta", "Delaware", "Utica"])
    PC = PC1 + PC2 + PC3 + PC4 + PC5 + PC6 + PC7
    b2t = 0.159 * 0.827 
    bd2ty = b2t * 365
    AEO2016 *= bd2ty 
    PC *= b2t
    return Year, AEO2016, np.zeros(len(Year)), YC, PC 

def GetFile_Oil( data_name, field_name, sum_data_EIA, sum_well, sum_actual):
    Y,AEO2016,Actual,Wells = Load_Calibration(
        data_name,
        ["Year", "AEO2016", "Actual", "Wells_Actual"])
    YC,PC = Load_Calibration( "./Data/US22_US_Tight_Oil_EIA.csv", ["Year", field_name])
    b2t = 0.159 * 0.827 
    bd2ty = b2t * 365
    AEO2016 *= bd2ty 
    PC *= b2t
    return sum_data_EIA+AEO2016, sum_well+Wells, sum_actual+PC 
