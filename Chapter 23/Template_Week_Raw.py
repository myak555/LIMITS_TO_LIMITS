#
# WHO keeps changing the file formats...
# This is to pre-edit the crap
#

template = "weekly_2020_08_23"
filename = "weekly_2020_08_23"

StatusDelimiters = ["Community transmission",
                    "Clusters of cases",
                    "Sporadic cases",
                    "No cases",
                    "Pending"]

class Territory:
    def __init__( self, f):
        self.Name = f.readline().strip()
        if len( self.Name) <= 1:
            self.Name = "FINISHED"
            return
        self.WeeklyCases = f.readline().strip()
        self.TotalCases = f.readline().strip()
        self.CasesPerMillion = f.readline().strip()
        self.WeeklyDeaths = f.readline().strip()
        self.TotalDeaths = f.readline().strip()
        self.DeathsPerMillion = f.readline().strip().replace("<", "")
        self.Status = f.readline().strip()
        try:
            self.nWeeklyCases = int( self.WeeklyCases)
            self.nTotalCases = int( self.TotalCases)
            self.nCasesPerMillion = int( self.CasesPerMillion)
            self.nWeeklyDeaths = int( self.WeeklyDeaths)
            self.nTotalDeaths = int( self.TotalDeaths)
            self.nDeathsPerMillion = int( self.DeathsPerMillion)
            self.Population = float( self.nTotalCases) / float( self.nCasesPerMillion) 
        except:
            print( self.Name + " : NUMERIC ERROR")
            return
        if self.Status in StatusDelimiters:
            print( self.Name + " : " + self.Status)
        else: 
            print( self.Name + " : STATUS UNKNOWN")
        return


f1 = open( "./Raw/{:s}.txt".format( template))
#f2 = open( "./Raw/{:s}.raw2".format( filename), "w")

Garbage = ["Reporting Country/Territory/Area New cases in last 7 days ",
                "Cumulative cases Cumulative cases per 1 million population ",
                "New deaths in last 7 days Cumulative deaths: ",
                "Cumulative deaths per 1 million population Transmission classification ",
                "Territoriesii "]

Territories = {}
for i in range( 1000):
    t = Territory( f1)
    if t.Name == "FINISHED": break
    if t.Name in Territories:
        print( "Duplicate: " + t.Name)
        break
    Territories[t.Name] = t
print( "Total of {:d} territories".format(len(Territories)))

# for g in Garbage:
#     buff = buff.replace( g, "")
# for d in Delimiters:
#     buff = buff.replace( " "+d+" ", "\n"+d+"\n")

# f2.write( buff)

# f1.close()
# f2.close()

# f1 = open( "./Raw/{:s}.raw2".format( filename))
# f2 = open( "./Raw/{:s}.txt".format( filename), "w")
# for i in range( 100000):
#     s = f1.readline()
#     if len(s) <= 0: break
#     s = s.strip()
#     if s in Delimiters:
#         f2.write( s + "\n")
#         continue
#     for j, c in enumerate( s):
#         if not c in "0123456789": continue
#         f2.write( s[:j-1] + "\n")
#         ss = s[j:].split(" ")
#         ls = len(ss) 
#         if ls <= 6:
#             for su in ss: f2.write( su + "\n")
#             break
#         if ls == 7:
#             f2.write( ss[0] + "\n")
#             f2.write( ss[1] + ss[2] + "\n")
#             f2.write( ss[3] + "\n")
#             f2.write( ss[4] + "\n")
#             f2.write( ss[5] + "\n")
#             f2.write( ss[6] + "\n")
#             break
#         if ls == 8:
#             f2.write( ss[0] + ss[1] + "\n")
#             f2.write( ss[2] + ss[3] + "\n")
#             f2.write( ss[4] + "\n")
#             f2.write( ss[5] + "\n")
#             f2.write( ss[6] + "\n")
#             f2.write( ss[7] + "\n")
#             break
#         if ls == 9:
#             f2.write( ss[0] + ss[1] + "\n")
#             f2.write( ss[2] + ss[3] + "\n")
#             f2.write( ss[4] + "\n")
#             f2.write( ss[5] + "\n")
#             f2.write( ss[6] + ss[7] + "\n")
#             f2.write( ss[8] + "\n")
#             break
#         for su in ss: f2.write( su + "\n")
#         break

f1.close()
#f2.close()
