from COVID_19_Parcing import *

cc = Covid_Countries()
for i in range(20,32):
    cc.Parse1( "2020_01_{:02d}".format(i))

# February (note format change)
for i in range(1,28):
    cc.Parse1( "2020_02_{:02d}".format(i))
cc.Parse2( "2020_02_28")
cc.Parse2( "2020_02_29")

# March (note WHO report errors)
cc.Parse2( "2020_03_01")
for i in range(2,16):
    cc.Parse3( "2020_03_{:02d}".format(i))
cc.Parse3( "2020_03_16") # This has 5 diff due to Gyana
cc.Parse3( "2020_03_17")
cc.Parse3( "2020_03_18")
cc.Parse3( "2020_03_19")
cc.Parse3( "2020_03_20") # 1 case diff San Vincent 
cc.Parse3( "2020_03_21")
cc.Parse3( "2020_03_22")
cc.Parse3( "2020_03_23")
cc.Parse3( "2020_03_24")
cc.Parse3( "2020_03_25") # Problematic (incorrect sum)
cc.Parse3( "2020_03_26")
cc.Parse3( "2020_03_27")
cc.Parse3( "2020_03_28")
cc.Parse3( "2020_03_29")
cc.Parse3( "2020_03_30")
cc.Parse3( "2020_03_31")

# April
for i in range(1,31):
    cc.Parse3( "2020_04_{:02d}".format(i))

# May
for i in range(1,32):
    cc.Parse3( "2020_05_{:02d}".format(i))

# June
for i in range(1,31):
   cc.Parse3( "2020_06_{:02d}".format(i))

# July
for i in range(1,5):
    cc.Parse3( "2020_07_{:02d}".format(i))

# strange format (once)
cc.Parse4( "2020_07_{:02d}".format(5))

# July
for i in range(6,32):
    cc.Parse3( "2020_07_{:02d}".format(i))

# August (the last WHO daily report is 16 Aug 2020)
for i in range(1,17):
    cc.Parse3( "2020_08_{:02d}".format(i))

cc.ParseWeekly("weekly_2020_08_23", ["2020_08_17","2020_08_18","2020_08_19","2020_08_20","2020_08_21","2020_08_22","2020_08_23"])

#cc.ParseWeekly("weekly_2020_10_25")

fout = open(".\Countries\_Processing report.txt", "w")
cc.applyMetadata( fout, "2020_08_{:02d}".format(i))
cc.reportByMortality( fout)
cc.outputCountryFiles()
# cc.reportByLatitude( fout)
# cc.reportByLEB( fout)
# cc.reportByDensity( fout)
# cc.reportByDPA( fout)
# cc.reportByGDP( fout)
# fout.close()

# if InteractiveModeOn: plt.show(True)
