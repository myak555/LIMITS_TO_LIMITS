from Predictions import *
import fnmatch


class Covid_Country:
    def __init__(self, name):
        self.Name = name
        self.Dates = []
        self.Cases = []
        self.Deaths = []
        self.Days = []
        self.Status = "No cases"
        self.Latitude = -999
        self.Population = -999
        self.Territory = -999
        self.Mortality = -999
        self.LEB = -999
        self.DPA = -999
        self.DPA65 = -999
        self.GDP = -999
        self.GDP_PPP = -999
        return
    def addData( self, date, ss):
        try:
            self.Dates += [date]
            self.Cases += [int(ss[1].replace(' ', ''))]
            self.Deaths += [int(ss[2].replace(' ', ''))]
            self.Status = ss[3].strip()
        except:
            print("Strange conversion: {:s}, {:s}, {:s}, {:s}, {:s}, {:s}". format( self.Name, date, ss[0], ss[1], ss[2], ss[3]))
        return
    def addDataWeek( self, dates, ss):
        try:
            newCases = int(ss[1].replace(' ', ''))
            newDeaths = int(ss[2].replace(' ', ''))
            self.Status = ss[3].strip()
        except:
            print("Strange conversion: {:s}, {:s}, {:s}, {:s}, {:s}, {:s}". format( self.Name, dates[-1], ss[0], ss[1], ss[2], ss[3]))
        oldCases = self.Cases[-1]
        oldDeaths = self.Deaths[-1]
        nDays = len( dates)
        deltaCases = (newCases - oldCases) // nDays 
        deltaDeaths = (newDeaths - oldDeaths) // nDays
        for d in dates[:-1]:
            oldCases += deltaCases 
            oldDeaths += deltaDeaths 
            self.Dates += [d]
            self.Cases += [oldCases]
            self.Deaths += [oldDeaths]
        self.Dates += [dates[-1]]
        self.Cases += [newCases]
        self.Deaths += [newDeaths]        
        return
    def getYLimitsCases(self, val0, val1):
        if val0 == val1: return (val0-1, val1+10)
        return (val0,val1*1.05)
    def getYLimitsDeaths(self, val0, val1):
        if val0 == val1: return (val0-1, val1+10)
        return (val0,val1*1.05)
    def getRussianStatus(self):
        if self.Status == "No cases": return "Случаев нет"
        if self.Status == "Pending": return "Не определились"
        if self.Status == "Sporadic cases": return "Отдельные случаи"
        if self.Status == "Clusters of cases": return "Изолированные вспышки"
        if self.Status == "Community transmission": return "Эпидемия"
        return self.Status
    def convertDate( self, date_str):
        months = [31, 29, 31, 30, 31, 30, 30, 31, 30, 31, 30, 31]
        ss = date_str.split("_")
        year = int(ss[0])
        month = int(ss[1])
        day = int(ss[2])
        if year < 2020: day -= 365
        for i in range(month-1):
            day += months[i]
        return day
    def getSundays( self, last_day):
        days = []
        for i in range( 5, last_day, 7):
            days += [i]
        return days
    def loadFile( self, ax1=None, ax2=None, method="mortality"):
        print( "Inputting: {:s}".format(self.Name))
        f = open( ".\Countries\{:s}.txt".format( self.Name))
        self.First_Death = None
        while True:
            s = f.readline()
            if len(s) <= 0: break
            s = s.strip()
            if s.startswith("# Latitude"):
                self.Latitude = float( s.split(' = ')[1])
                continue
            if s.startswith("# Population"):
                self.Population = float( s.split(' = ')[1])
                continue
            if s.startswith("# Territory"):
                self.Territory = float( s.split(' = ')[1])
                continue
            if s.startswith("# LEB"):
                self.LEB = float( s.split(' = ')[1])
                continue
            if s.startswith("# DPA "):
                self.DPA = float( s.split(' = ')[1])
                continue
            if s.startswith("# DPA65"):
                self.DPA65 = float( s.split(' = ')[1])
                continue
            if s.startswith("# GDP "):
                self.GDP = float( s.split(' = ')[1])
                continue
            if s.startswith("# GDP_PPP"):
                self.GDP_PPP = float( s.split(' = ')[1])
                continue            
            if s.startswith("# First_Case"):
                self.First_Case = s.split(' = ')[1]
                continue            
            if s.startswith("# First_Death"):
                self.First_Death = s.split(' = ')[1]
                continue            
            if s.startswith("# Status"):
                self.Status = s.split(' = ')[1]
                continue
            if s.startswith("# COVID-19 Mortality"):
                self.Mortality = s.split(' = ')[1]
                continue
            if s.startswith("#"): continue
            if s.startswith("Date\t"): continue
            ss = s.split('\t')
            self.Dates += [ss[0]]
            self.Days += [self.convertDate( ss[0])]
            self.Cases += [int(ss[1])]
            self.Deaths += [int(ss[2])]
        f.close()
        days = []
        cpm = []
        dpm = []
        for i, d in enumerate(self.Dates):
            if method == "dpa65" and self.DPA65 <= 0: continue
            days += [ self.convertDate( d)]
            cpm += [self.Cases[i] / self.Population]
            if method == "dpa65":
                dpm += [self.Deaths[i] * 0.1 / self.DPA65]
            else:
                dpm += [self.Deaths[i] / self.Population]
        if self.First_Death is not None:
            days = np.array(days) - self.convertDate( self.First_Death)
        else:
            days = np.array(days) - self.convertDate( self.Dates[0])            
        cpm = np.array(cpm) * 1000
        dpm = np.array(dpm) * 1000
        self.Days = np.array(self.Days)
        self.dCases = np.zeros(len(cpm))
        self.dDeaths = np.zeros(len(dpm))
        self.dCases[0] = cpm[0]
        self.dDeaths[0] = dpm[0]
        for i in range( 1,len(dpm)):
            self.dCases[i] = cpm[i]-cpm[i-1]
            self.dDeaths[i] = dpm[i]-dpm[i-1]
            #print( "{:.2f}".format( self.dDeaths[i]))
        # optional plotting    
        if ax1 is None: return
        if method == "dpa65":
            ax1.plot(days, dpm, 'o', lw=3, alpha=0.5,
                    label="{:s}: {:d}/{:0.0f}".format(self.Name,
                    self.Deaths[-1], self.DPA65))
        else:
            pformat = "{:s}: {:d}/{:d}, {:0.1f} млн"
            pop = self.Population/1000
            if self.Population < 1000: 
                pformat = "{:s}: {:d}/{:d}, {:0.1f} тыс"
                pop = self.Population                
            ax1.plot(days, dpm, 'o', lw=3, alpha=0.5,
                    label=pformat.format(self.Name,
                    self.Deaths[-1], self.Cases[-1], pop))
        ax1.annotate(self.Name, (days[-1]+1, dpm[i]), fontsize=12)
        ax1.scatter( [days[-1]], [dpm[-1]], [8*(self.Population**0.5)], c="g", alpha=0.3, marker='s')
        if ax2 is None: return
        ax2.plot(days, cpm, 'o', lw=3, alpha=0.5,
                    label="{:s}: {:d}/{:d} = {:.2f}%".format(self.Name,
                    self.Deaths[-1], self.Cases[-1], self.Deaths[-1]*100.0/self.Cases[-1]))
        ax2.annotate( self.Name, (days[-1]+1, cpm[i]), fontsize=12)
        ax2.scatter( [days[-1]], [cpm[-1]], [8*(self.Population**0.5)], c="g", alpha=0.3, marker='s')        
        return
    def outputFile( self):
        print( "Outputting: {:s}".format(self.Name))
        f = open( ".\Countries\{:s}.txt".format( self.Name), "w")
        f.write("#\n")
        f.write("# COVID-19 Country file (official WHO count)\n")
        f.write("# Country = {:s}\n".format(self.Name))
        f.write("# Latitude = {:.1f}\n".format(self.Latitude))
        f.write("# Population = {:.3f}\n".format(self.Population))
        f.write("# Territory = {:.1f}\n".format(self.Territory))
        f.write("# LEB = {:.1f}\n".format(self.LEB))
        f.write("# DPA = {:.0f}\n".format(self.DPA))
        f.write("# DPA65 = {:.0f}\n".format(self.DPA65))
        f.write("# GDP = {:.1f}\n".format(self.GDP))
        f.write("# GDP_PPP = {:.1f}\n".format(self.GDP_PPP))
        f.write("# COVID-19 Mortality = {:.1f}\n".format(self.Mortality))
        jCase = 0
        jDeath = 0
        for i,d in enumerate(self.Dates):
            if self.Cases[i] <= 0: continue
            f.write("# First_Case = {:s}\n".format(d))
            jCase = i
            break
        for i,d in enumerate(self.Dates):
            if self.Deaths[i] <= 0: continue
            f.write("# First_Death = {:s}\n".format(d))
            jDeath = i
            break
        for i in range( len(self.Dates)-1, jCase, -1):
            if self.Cases[i] <= 0: continue
            f.write("# Last_Case = {:s}\n".format(d))
            break
        for i in range( len(self.Dates)-1, jDeath, -1):
            if self.Deaths[i] <= 0: continue
            f.write("# Last_Death = {:s}\n".format(d))
            break
        f.write("# Status as of {:s} = {:s}\n".format(self.Dates[-1], self.Status))        
        f.write("#\n")
        f.write("Date\tConf_Cases\tConf_Deaths\n")
        days = []
        cpm = []
        dpm = []
        for i, d in enumerate(self.Dates):
            s = "{:s}\t{:d}\t{:d}\n".format( d, self.Cases[i], self.Deaths[i])
            days += [ self.convertDate( d)]
            cpm += [ self.Cases[i] / self.Population]
            dpm += [self.Deaths[i] / self.Population]            
            f.write(s)
        f.close()
        if len(days) == 1 and self.Cases[0] == 0: return
        cpm = np.array(cpm) * 1000
        dcpm = np.array(cpm)
        dpm = np.array(dpm) * 1000
        ddpm = np.array(dpm)
        for i in range(1, len(cpm)):
            if days[i] - days[i-1] > 1:
                print("Warning: {:s} has a gap between {:s} and {:s}".format(self.Name, self.Dates[i-1],self.Dates[i]))
            dcpm[i] -= cpm[i-1]
            ddpm[i] -= dpm[i-1]
        all_sundays = self.getSundays( days[-1])
        sundays = []
        sunday_dcpm = []
        sunday_ddpm = []
        for i, d in enumerate(days):
            if not d in all_sundays: continue
            sundays += [d]
            sunday_dcpm += [dcpm[i]]
            sunday_ddpm += [ddpm[i]]
        sunday_dcpm = np.array(sunday_dcpm)
        sunday_ddpm = np.array(sunday_ddpm)            
        limits = (1, 366)
        last_Date = self.Dates[-1].replace('_','-')
        fig = plt.figure( figsize=(15,15))
        fig.suptitle( 'COVID-19 {:s}'.format(self.Name), fontsize=22)
        gs = plt.GridSpec(3, 1, height_ratios=[2, 2, 1]) 
        ax1 = plt.subplot(gs[0])
        ax3 = plt.subplot(gs[2])
        ax1.plot(days, cpm, 'o', lw=3, color='g', alpha=1, label="Подтверждённые случаи")
        ax1.bar(days, dcpm * 10, align='center', color='g', width=1, alpha=0.5, label="За день x 10")
        if len(sundays) >= 1:
            ax1.scatter( sundays, sunday_dcpm * 10, np.ones(len(sundays))*300, c="g", alpha=1, marker='+', label="Воскресенье")
        if self.Name == "China":
            ax1.plot([45,45],[0,100], "--", color='k', label="Хубейский палец дяди Си")
            ax1.legend(loc=2, fontsize=11)
        else:
            ax1.legend(loc=3, fontsize=11)
        ax1.set_ylabel('на млн населения')        
        ax1.set_xlim( limits)
        ylimits = self.getYLimitsCases(min(dcpm*10), max(max(cpm), max(dcpm*10)))
        ax1.set_ylim( ylimits)
        ax3.text( limits[0]+1, 10,
                  "Население = {:.1f} тыс.".format( self.Population))
        ax3.text( limits[0]+1, 9,
                  "Случаев на {:s} = {:.0f}".format(last_Date, self.Cases[-1]))
        ax3.text( limits[0]+1, 8,
                  "Собственный статус = {:s}".format(self.getRussianStatus()))
        ax1.grid(True)
        ax2 = plt.subplot(gs[1])
        ax2.plot(days, dpm, 'o', lw=3, color='k', alpha=1, label="Подтверждённые смерти")
        ax2.bar(days, ddpm * 10, align='center', color='r', width=1, alpha=0.4, label="За день x 10")
        if len(sundays) >= 1:
            ax2.scatter( sundays, sunday_ddpm * 10, 300, c="k", alpha=1, marker='+')
        if self.Name == "China":
            ax2.plot([108,108],[0,10], "--", color='r', label="ВОЗ на коленках выпросила у КНР 1300 трупов")
        d65 = self.DPA65 / 0.365 / self.Population
        if d65 > 0 and max( ddpm) >= d65:
            ax2.plot([days[0],days[-1]],[d65*10,d65*10], "--", color='r')            
            ax2.text( (limits[0] + limits[1])/2, d65*10.5, "Средняя смертность 65+ за день в 2019 г {:.1f} х 10".format(d65), color='r', alpha=0.5, fontsize=11)
        ylimits = self.getYLimitsDeaths(min(ddpm*10), max(max(dpm), max(ddpm*10)))
        ax2.set_ylim( ylimits)
        if ylimits[1] > 170:
            ax2.plot([days[0], days[-1]], [170, 170], '-.', lw=1, color='k', alpha=1)
            ax2.text( (limits[0] + limits[1])/2, 169, "Типичная среднегодовая смертность от гриппа и пневмонии", color='k', alpha=0.5, fontsize=11)
        if ylimits[1] > 800:
            ax2.plot([days[0], days[-1]], [800, 800], '--', lw=2, color='k', alpha=1)
            ax2.text( (limits[0] + limits[1])/2, 798, "Типичная среднегодовая смертность от всех лёгочных заболеваний", color='k', alpha=0.5, fontsize=11)
        if self.Deaths[-1] > 0:
            ax3.text( limits[0]+1, 7,
                      "Смертей от COVID-19 на {:s} = {:.0f}".format(last_Date, self.Deaths[-1]))
        else:
            ax3.text( limits[0]+1, 7,
                      'От простуды "COVID-19" на {:s} никто не умер'.format(last_Date))            
        ax3.text( limits[0]+1, 6,
                  "Кажущийся CFR на {:s} = {:.2f}%".format(last_Date, self.Deaths[-1]*100/self.Cases[-1]))
        if self.DPA65 > 0:
            ax3.text( limits[0]+1, 5,
                  "Умерло в 2019 г (всех возрастов от любых причин) = {:.0f}".format( self.DPA))
            ax3.text( limits[0]+1, 4,
                  "Умерло в 2019 г в возрасте 65 и старше (от любых причин) = {:.0f}".format( self.DPA65))
        if self.Name == "China":
            ax2.legend(loc=4, fontsize=11)
        else:
            ax2.legend(loc=3, fontsize=11)
        ax2.set_ylabel('на млн населения')
        ax2.set_xlim( limits)
        ax2.grid(True)

        ax3.set_xlabel('день года: 1 - 1 января 2020')
        ax3.set_xlim( limits)
        ax3.set_ylim( 3.5, 11)
        ax3.set_yticks([])
        ax3.grid(True)

        plt.savefig( ".\Countries\{:s}.png".format( self.Name))
        plt.close('all')
        return
    def __str__( self):
        s = "{:s}\t{:s}\t{:d}\t{:d}\t{:s}".format( self.Name,
            self.Dates[0], self.Cases[-1], self.Deaths[-1], self.Status) 
        return s


class Covid_Countries:
    def __init__(self):
        self.Countries = {}
        return
    def addData( self, date, s):
        ss = s.split('\t')
        name = ss[0]
        if not name in self.Countries:
            self.Countries[name] = Covid_Country( name) 
        self.Countries[name].addData(date, ss)
        return 
    def applyMetadata( self, output_file, last_date):
        countries, pop, leb, lat, ter, dpa, d65, gdp, gdp_ppp = Load_Calibration_Text(".\Countries\_Countries_Metadata.txt",
                              ["Country", "Population", "LEB", "Latitude",
                               "Territory", "Deaths_pa", "Deaths_over_65",
                               "GDP", "GDP_PPP"],
                              separator='\t')
        s = "В Специальной Олимпиаде не участвуют:"
        print(s)
        print()
        output_file.write(s+"\n\n")
        fmt = "{:40s}\t{:>15s}\t{:>16s}"
        s = fmt.format("Страна", "Население (тыс)", "Территория (км2)")
        print( s)
        output_file.write(s+"\n")
        pop_tot = 0
        ter_tot = 0
        missing = []
        for i, c in enumerate( countries):
            if not c in self.Countries:
                pop_tot += float(pop[i])
                ter_tot += float(ter[i])
                s = fmt.format(c, pop[i], ter[i])
                print( s)
                output_file.write(s+"\n")
                ac = Covid_Country( c)
                ac.addData(last_date, [c,"0","0","No cases"])
                ac.Latitude = float(lat[i])
                ac.Population = float(pop[i])
                ac.Territory = float(ter[i])
                ac.LEB = float(leb[i])
                ac.DPA = float(dpa[i])
                ac.DPA65 = float(d65[i])
                ac.GDP = float(gdp[i])
                ac.GDP_PPP = float(gdp_ppp[i])
                missing += [ac]
                continue
            cc = self.Countries[c]
            cc.Latitude = float(lat[i])
            cc.Population = float(pop[i])
            cc.Territory = float(ter[i])
            cc.LEB = float(leb[i])
            cc.DPA = float(dpa[i])
            cc.DPA65 = float(d65[i])
            cc.GDP = float(gdp[i])
            cc.GDP_PPP = float(gdp_ppp[i])
        s = "{:40s}\t{:>15.3f}\t{:>16.1f}".format("Total:", pop_tot, ter_tot)
        print( s)
        output_file.write(s+"\n")
        print()
        for ac in missing:
           self.Countries[ac.Name] = ac 
        s = "Участники Специальной Олимпиады без смертей:"
        print(s)
        print()
        output_file.write("\n" +s+"\n\n")
        fmt = "{:40s}\t{:>15s}\t{:>15s}\t{:>15s}\t{:>16s}"
        fmt2 = "{:40s}\t{:>15.2f}\t{:>15d}\t{:>15.2f}\t{:>16.1f}"
        s = fmt.format("Страна", "Население (тыс)", "Случаев", "Случаев на млн", "Территория (км2)")
        print( s)
        output_file.write(s+"\n")
        pop_tot = 0
        cases_tot = 0
        ter_tot = 0
        days = np.linspace( 1, 366, 366)
        cases = np.zeros( len(days))
        dcases = np.zeros( len(days))
        for i, c in enumerate( countries):
            cc = self.Countries[c]
            if cc.Cases[-1] <= 0: continue
            if cc.Deaths[-1] > 0: continue
            pop_tot += cc.Population
            ter_tot += cc.Territory
            cases_tot += cc.Cases[-1]
            for j, d in enumerate(cc.Dates):
                k = cc.convertDate( d)
                cases[k] += cc.Cases[j] 
            s = fmt2.format(cc.Name[:40], cc.Population, cc.Cases[-1], cc.Cases[-1]*1000/cc.Population,cc.Territory)
            print( s)
            output_file.write(s+"\n")
        s = fmt2.format("Total:", pop_tot, cases_tot, cases_tot*1000/pop_tot,ter_tot)
        print( s)
        output_file.write(s+"\n")
        print()
        for i in range(len(days)-1,0,-1):
            if cases[i] <= 0: continue
            lastData = i+1
            break
        for i in range(1,lastData):
            dcases[i-1]=cases[i]-cases[i-1]
        limits = (19, 241)
        ylimits1 = (0, 2000)
        last_Date = last_date.replace('_','-')
        fig = plt.figure( figsize=(15,10))
        fig.suptitle( 'Страны без смертей от COVID-19 на {:s}'.format(last_Date), fontsize=22)
        gs = plt.GridSpec(1, 1) 
        ax1 = plt.subplot(gs[0])
        ax1.plot(days[:lastData], cases[:lastData], 'o', lw=3, color='g', alpha=1, label="Подтверждённые случаи")
        ax1.bar(days[:lastData], dcases[:lastData]*10, align='center', color='g', width=1, alpha=0.5, label="За день x 10")
        ax1.legend(loc=2)
        ax1.set_ylabel('случаев всего')        
        ax1.set_xlim( limits)
        ax1.set_ylim( ylimits1)
        ax1.text( limits[0]*1.1, ylimits1[1] * 0.75,
                  "Население = {:.1f} тыс.".format( pop_tot))
        ax1.text( limits[0]*1.1, ylimits1[1] * 0.70,
                  "Случаев нa {:s} = {:.0f}".format(last_Date, cases_tot))
        ax1.grid(True)
        ax1.set_xlabel('день года: 1 - 1 января 2020')
        plt.savefig( "./Graphs/101_Countries_Zero_Deaths.png")

        s = "Малые страны:"
        print(s)
        print()
        output_file.write("\n" + s+"\n\n")
        fmt = "{:40s}\t{:>15s}\t{:>15s}\t{:>15s}\t{:>16s}"
        fmt2 = "{:40s}\t{:>15.2f}\t{:>15d}\t{:>15.2f}\t{:>16.1f}"
        s = fmt.format("Страна", "Население (тыс)", "Смертей", "Смертей на млн", "Территория (км2)")
        print( s)
        output_file.write(s+"\n")
        pop_tot = 0
        cases_tot = 0
        deaths_tot = 0
        ter_tot = 0
        cases = np.zeros( len(days))
        dcases = np.zeros( len(days))
        deaths = np.zeros( len(days))
        ddeaths = np.zeros( len(days))
        for i, c in enumerate( countries):
            cc = self.Countries[c]
            if cc.Population >= 1000: continue
            pop_tot += cc.Population
            ter_tot += cc.Territory
            cases_tot += cc.Cases[-1]
            deaths_tot += cc.Deaths[-1]
            for j, d in enumerate(cc.Dates):
                k = cc.convertDate( d)
                cases[k] += cc.Cases[j] 
                deaths[k] += cc.Deaths[j] 
            s = fmt2.format(cc.Name[:40], cc.Population, cc.Deaths[-1], cc.Deaths[-1]*1000/cc.Population,cc.Territory)
            print( s)
            output_file.write(s+"\n")
        s = fmt2.format("Total:", pop_tot, deaths_tot, deaths_tot*1000/pop_tot,ter_tot)
        print( s)
        output_file.write(s+"\n")
        print()
        for i in range(len(days)-1,0,-1):
            if cases[i] <= 0: continue
            lastData = i+1
            break
        for i in range(1,lastData):
            dcases[i-1]=cases[i]-cases[i-1]
            ddeaths[i-1]=deaths[i]-deaths[i-1]
        limits = (19, 241)
        ylimits1 = (0, 1500)
        ylimits2 = (0, 35)
        last_Date = last_date.replace('_','-')
        fig = plt.figure( figsize=(15,15))
        fig.suptitle( 'COVID-19 в малых странах', fontsize=22)
        gs = plt.GridSpec(2, 1, height_ratios=[1,1]) 
        ax1 = plt.subplot(gs[0])
        ax2 = plt.subplot(gs[1])
        
        ax1.plot(days[:lastData], cases[:lastData]*1000/pop_tot,
                 'o', lw=3, color='g', alpha=1, label="Подтверждённые случаи")
        ax1.bar(days[:lastData], dcases[:lastData]*10000/pop_tot,
                align='center', color='g', width=1, alpha=0.5, label="За день x 10")
        ax1.legend(loc=2)
        ax1.set_ylabel('случаев на млн населения')        
        ax1.set_xlim( limits)
        ax1.set_ylim( ylimits1)
        ax1.text( limits[0]*1.1, ylimits1[1] * 0.75,
                  "Население = {:.1f} тыс.".format( pop_tot))
        ax1.text( limits[0]*1.1, ylimits1[1] * 0.70,
                  "Случаев нa {:s} = {:.0f}".format(last_Date, cases_tot))
        ax1.grid(True)

        model = Hubbert(x0=99.0, s0=0.13, s1=0.055, peak=5.9).GetVector(days)
        model_cum = Cumulative(model/10)
        ax2.plot(days[:lastData], deaths[:lastData]*1000/pop_tot,
                 'o', lw=3, color='k', alpha=1, label="Подтверждённых смертей")
        ax2.plot(days, model,
                 '--', lw=2, color='r', alpha=1, label="Модель")
        ax2.plot(days, model_cum,
                 '-', lw=3, color='r', alpha=1)
        ax2.bar(days[:lastData], ddeaths[:lastData]*10000/pop_tot,
                align='center', color='k', width=1, alpha=0.5, label="За день x 10")
        ax2.legend(loc=2)
        ax2.set_ylabel('смертей на млн населения')        
        ax2.set_xlim( limits)
        ax2.set_ylim( ylimits2)
        ax2.text( limits[0]*1.1, ylimits2[1] * 0.70,
                  "Смертей нa {:s} = {:.0f}".format(last_Date, deaths_tot))
        ax2.text( limits[0]*1.1, ylimits2[1] * 0.65,
                  "Кажущийся CFR = {:.2f}%".format( deaths_tot*100/cases_tot))
        ax2.grid(True)
        ax2.set_xlabel('день года: 1 - 1 января 2020')
        plt.savefig( "./Graphs/102_Small_Countries.png")
        return
    def inputCountryFile( self, name, ax1, ax2=None, method="mortality"):
        if not name in self.Countries:
            self.Countries[name] = Covid_Country( name) 
        self.Countries[name].loadFile( ax1, ax2, method)
        return
    def outputCountryFiles( self):
        alist = list( self.Countries.values())
        alist.sort( key=lambda x: x.Name, reverse=False)
        for i, c in enumerate(alist):
            c.outputFile()
        return
    def reportByMortality( self, output_file):
        alist = list( self.Countries.values())
        alist.sort( key=lambda x: x.Name, reverse=False)
        for i, c in enumerate(alist):
            if c.Population <= 0:
                print( "Warning: {:s} population = {:.3f}".format(c.Name, c.Population))
            c.Mortality = c.Deaths[-1] * 1000 / c.Population
        alist.sort( key=lambda x: x.Mortality, reverse=True)
        output_file.write("\nСмертей от COVID-19 на миллион населения\n\n")
        fmt1 = "{:40s}\t{:>15s}\t{:>13s}\t{:>7s}\t{:>14s}\n"
        fmt2 = "{:40s}\t{:>15.3f}\t{:>13d}\t{:>7d}\t{:>14.2f}\n"
        s = fmt1.format("Страна/территория", "Население (тыс)", "Подтв.случаев", "Смертей", "Смертей на млн")
        output_file.write( s)
        pop_tot = 0
        cas_tot = 0
        dea_tot = 0
        for i, c in enumerate( alist):
            s = fmt2.format(c.Name[:40], c.Population, c.Cases[-1], c.Deaths[-1], c.Mortality)
            output_file.write( s)
            pop_tot += c.Population
            cas_tot += c.Cases[-1]
            dea_tot += c.Deaths[-1]
        s = fmt2.format("Total:", pop_tot, cas_tot, dea_tot, dea_tot * 1000 / pop_tot)
        output_file.write( s)
        print(cas_tot, dea_tot)
        return
    def reportByLatitude( self, output_file):
        lat_bins = ["90N-55N",
                    "54N-45N",
                    "44N-35N",
                    "34N-25N",
                    "24N-15N",
                    "14N-05N",
                    "04N-05S",
                    "06S-15S",
                    "16S-25S",
                    "26S-90S"]
        lat_vbins = [55, 45, 35, 25, 15, 5, -5, -15, -25, -90]
        pop_bins = np.zeros(len(lat_bins))
        cas_bins = np.zeros(len(lat_bins))
        dea_bins = np.zeros(len(lat_bins))
        alist = list( self.Countries.values())
        lats = []
        morts = []
        pops = []
        names = []
        for i, c in enumerate(alist):
            lats += [c.Latitude]
            morts += [max( c.Mortality, 0.1)]
            pops += [max(np.sqrt( c.Population)*10,50)]
            names += [ c.Name]
            for j, l in enumerate(lat_vbins):
                if c.Latitude < l: continue
                pop_bins[j] += c.Population 
                cas_bins[j] += c.Cases[-1]
                dea_bins[j] += c.Deaths[-1]
                break
        output_file.write("\nРаспределение COVID-19 от широты\n\n")
        fmt1 = "{:20s}\t{:>15s}\t{:>13s}\t{:>7s}\t{:>14s}\t{:>14s}\n"
        fmt2 = "{:20s}\t{:>15.3f}\t{:>13.0f}\t{:>7.0f}\t{:>14.2f}\t{:>14.2f}\n"
        s = fmt1.format("Широта местности", "Население (тыс)", "Подтв.случаев", "Смертей", "Случаев на млн", "Смертей на млн")
        output_file.write( s)
        pop_tot = 0
        cas_tot = 0
        dea_tot = 0
        for i, la in enumerate( lat_bins):
            s = fmt2.format(la, pop_bins[i], cas_bins[i], dea_bins[i],
                            cas_bins[i]*1000/pop_bins[i], dea_bins[i]*1000/pop_bins[i])
            output_file.write( s)
            pop_tot += pop_bins[i]
            cas_tot += cas_bins[i]
            dea_tot += dea_bins[i]
        cas_pm = cas_bins * 1000 / pop_bins
        dea_pm = dea_bins * 1000 / pop_bins
        cas_pm_tot = cas_tot * 1000 / pop_tot
        dea_pm_tot = dea_tot * 1000 / pop_tot
        s = fmt2.format("Total:", pop_tot, cas_tot, dea_tot, cas_pm_tot, dea_pm_tot)
        output_file.write( s)
        #
        # bar
        #
        plot_bins = np.linspace( 0, 9, 10)
        fig = plt.figure( figsize=(15,15))
        fig.suptitle( 'Распределение COVID-19 от широты', fontsize=22)
        gs = plt.GridSpec(2, 1, height_ratios=[1, 1]) 
        ax1 = plt.subplot(gs[0])
        ax1.barh(plot_bins, pop_bins/1000, align='center', color='b', alpha=0.5)
        ax1.set_yticks(plot_bins)
        ax1.set_yticklabels(lat_bins)
        ax1.invert_yaxis()
        ax1.set_xlabel('млн человек')
        ax1.set_ylabel('широта')        
        ax1.set_xlim( 0, 2500)
        ax1.grid(True)
        ax2 = plt.subplot(gs[1])
        ax2.barh(plot_bins, cas_pm, align='center', color='y', alpha=0.5, label="подтверждённые случаи")
        ax2.barh(plot_bins, dea_pm*10, align='center', color='k', alpha=0.5, height=0.33, label="подтверждённые смерти х 10")
        ax2.set_yticks(plot_bins)
        ax2.set_yticklabels(lat_bins)
        ax2.invert_yaxis()
        ax2.set_xlabel('подтверждённых случаев / смертей на 1 млн')
        ax2.set_ylabel('широта')        
        #ax2.set_xlim( 0, 2100)
        ax2.legend(loc=0)
        ax2.grid(True)
        plt.savefig( "./Graphs/001_COVID19_Latitude.png")
        #
        # distribution
        #
        fig = plt.figure( figsize=(15,15))
        fig.suptitle( 'Распределение COVID-19 от широты', fontsize=22)
        gs = plt.GridSpec(1, 1, height_ratios=[1]) 
        ax1 = plt.subplot(gs[0])
        ax1.scatter( morts, lats, pops, c="g", alpha=0.3, marker='s')
        for i, txt in enumerate(names):
            ax1.annotate(txt, (morts[i]*1.1, lats[i]), fontsize=10)
        ax1.set_xscale("log")
        ax1.set_xlabel('смертей на млн')
        ax1.set_ylabel('широта')        
        ax1.set_xlim( 0.09, 4000)
        ax1.set_ylim( -60, 70)
        ax1.grid(True)
        ax1.text(10,-50, "площадь маркера пропорциональна населению")
        #ax1.text(1000,33, "Diamond Princess", fontsize=12)
        plt.savefig( "./Graphs/002_COVID19_LatitudeXY.png")
        return
    def reportByLEB( self, output_file):
        leb_bins = ["80+",
                    "79-75",
                    "74-70",
                    "69-65",
                    "64-60",
                    "59-55",
                    "54-"]
        leb_vbins = [80, 75, 70, 65, 60, 55, 0]
        pop_bins = np.zeros(len(leb_bins))
        cas_bins = np.zeros(len(leb_bins))
        dea_bins = np.zeros(len(leb_bins))
        alist = list( self.Countries.values())
        lebs = []
        morts = []
        pops = []
        names = []
        for i, c in enumerate(alist):
            if c.LEB <= 0:
                #print(c.Name)
                continue
            lebs += [c.LEB]
            morts += [max( c.Mortality, 0.1)]
            pops += [max(np.sqrt( c.Population)*10,50)]
            names += [ c.Name]
            for j, l in enumerate(leb_vbins):
                if c.LEB < l: continue
                pop_bins[j] += c.Population 
                cas_bins[j] += c.Cases[-1]
                dea_bins[j] += c.Deaths[-1]
                break
        output_file.write("\nРаспределение COVID-19 от ожидаемой продолжительности жизни\n\n")
        fmt1 = "{:20s}\t{:>15s}\t{:>13s}\t{:>7s}\t{:>14s}\t{:>14s}\n"
        fmt2 = "{:20s}\t{:>15.3f}\t{:>13.0f}\t{:>7.0f}\t{:>14.2f}\t{:>14.2f}\n"
        s = fmt1.format("LEB", "Население (тыс)", "Подтв.случаев", "Смертей", "Случаев на млн", "Смертей на млн")
        output_file.write( s)
        pop_tot = 0
        cas_tot = 0
        dea_tot = 0
        for i, la in enumerate( leb_bins):
            s = fmt2.format(la, pop_bins[i], cas_bins[i], dea_bins[i],
                            cas_bins[i]*1000/pop_bins[i], dea_bins[i]*1000/pop_bins[i])
            output_file.write( s)
            pop_tot += pop_bins[i]
            cas_tot += cas_bins[i]
            dea_tot += dea_bins[i]
        cas_pm = cas_bins * 1000 / pop_bins
        dea_pm = dea_bins * 1000 / pop_bins
        cas_pm_tot = cas_tot * 1000 / pop_tot
        dea_pm_tot = dea_tot * 1000 / pop_tot
        s = fmt2.format("Total:", pop_tot, cas_tot, dea_tot, cas_pm_tot, dea_pm_tot)
        output_file.write( s)
        #
        # bar
        #
        plot_bins = np.linspace( 0, len(leb_bins)-1, len(leb_bins))
        fig = plt.figure( figsize=(15,15))
        fig.suptitle( 'Распределение COVID-19 от LEB', fontsize=22)
        gs = plt.GridSpec(2, 1, height_ratios=[1, 1]) 
        ax1 = plt.subplot(gs[0])
        ax1.barh(plot_bins, pop_bins/1000, align='center', color='b', alpha=0.5)
        ax1.set_yticks(plot_bins)
        ax1.set_yticklabels(leb_bins)
        ax1.invert_yaxis()
        ax1.set_xlabel('млн человек')
        ax1.set_ylabel('ожидаемая продолжительность жизни')        
        ax1.set_xlim( 0, 3000)
        ax1.grid(True)
        ax2 = plt.subplot(gs[1])
        ax2.barh(plot_bins, cas_pm, align='center', color='y', alpha=0.5, label="подтверждённые случаи")
        ax2.barh(plot_bins, dea_pm*10, align='center', color='k', alpha=0.5, height=0.33, label="подтверждённые смерти х 10")
        ax2.set_yticks(plot_bins)
        ax2.set_yticklabels(leb_bins)
        ax2.invert_yaxis()
        ax2.set_xlabel('подтверждённых случаев / смертей на 1 млн')
        ax2.set_ylabel('ожидаемая продолжительность жизни')        
        #ax2.set_xlim( 0, 2100)
        ax2.legend(loc=0)
        ax2.grid(True)
        plt.savefig( "./Graphs/003_COVID19_LEB.png")
        #
        # distribution
        #
        fig = plt.figure( figsize=(15,15))
        fig.suptitle( 'Распределение COVID-19 от LEB', fontsize=22)
        gs = plt.GridSpec(1, 1, height_ratios=[1]) 
        ax1 = plt.subplot(gs[0])
        ax1.scatter( morts, lebs, pops, c="g", alpha=0.3, marker='s')
        for i, txt in enumerate(names):
            ax1.annotate(txt, (morts[i]*1.1, lebs[i]), fontsize=10)
        ax1.set_xscale("log")
        ax1.set_xlabel('смертей на млн')
        ax1.set_ylabel('ожидаемая продолжительность жизни')        
        ax1.set_xlim( 0.09, 1000)
        ax1.set_ylim( 50, 90)
        ax1.grid(True)
        ax1.text(8,55, "площадь маркера пропорциональна населению")
        plt.savefig( "./Graphs/004_COVID19_LEB_XY.png")
        return
    def reportByDensity( self, output_file):
        alist = list( self.Countries.values())
        dens = []
        morts = []
        pops = []
        names = []
        for i, c in enumerate(alist):
            if c.Territory <= 0:
                continue
            dens += [c.Population * 1000 / c.Territory]
            morts += [max( c.Mortality, 0.1)]
            pops += [max(np.sqrt( c.Population)*10,50)]
            names += [ c.Name]
        #
        # distribution 1
        #
        fig = plt.figure( figsize=(15,15))
        fig.suptitle( 'Распределение COVID-19 от плотности населения', fontsize=22)
        gs = plt.GridSpec(1, 1, height_ratios=[1]) 
        ax1 = plt.subplot(gs[0])
        ax1.scatter( morts, dens, pops, c="g", alpha=0.3, marker='s')
        for i, txt in enumerate(names):
            ax1.annotate(txt, (morts[i]*1.1, dens[i]), fontsize=10)
        ax1.set_xscale("log")
        ax1.set_yscale("log")
        ax1.set_xlabel('смертей на млн')
        ax1.set_ylabel('плотность населения, 1/км2')        
        ax1.set_xlim( 0.09, 4000)
        ax1.set_ylim( 0.02, 400000)
        ax1.grid(True)
        ax1.text(10,0.05, "площадь маркера пропорциональна населению")
        plt.savefig( "./Graphs/005_COVID19_Dens_XY.png")
        #
        # distribution 2
        #
        fig = plt.figure( figsize=(15,15))
        fig.suptitle( 'Распределение COVID-19 от плотности населения', fontsize=22)
        gs = plt.GridSpec(1, 1, height_ratios=[1]) 
        ax1 = plt.subplot(gs[0])
        ax1.scatter( morts, dens, pops, c="g", alpha=0.3, marker='s')
        for i, txt in enumerate(names):
            ax1.annotate(txt, (morts[i]*1.1, dens[i]), fontsize=10)
        ax1.set_xscale("log")
        ax1.set_yscale("log")
        ax1.set_xlabel('смертей на млн')
        ax1.set_ylabel('плотность населения, 1/км2')        
        ax1.set_xlim( 0.09, 4000)
        ax1.set_ylim( 1, 10000)
        ax1.grid(True)
        ax1.text(10,1.7, "площадь маркера пропорциональна населению")
        plt.savefig( "./Graphs/006_COVID19_Dens_XY_Expanded.png")
        return
    def reportByDPA( self, output_file):
        alist = list( self.Countries.values())
        alist.sort( key=lambda x: x.Name, reverse=False)
        blist = []
        for i, c in enumerate(alist):
            if c.DPA <= 0:
                #print(c.Name)
                continue
            c.Relative_Mortality = c.Deaths[-1] * 100 / c.DPA
            c.Relative_Mortality65 = c.Deaths[-1] * 100 / c.DPA65
            blist += [c]
        blist.sort( key=lambda x: x.Relative_Mortality, reverse=True)
        output_file.write("\nСмерти от COVID-19 как доля от смертей 2019 г\n\n")
        fmt1 = "{:40s}\t{:>15s}\t{:>16s}\t{:>19s}\t{:>21s}\n"
        fmt2 = "{:40s}\t{:>15.3f}\t{:>16.0f}\t{:>19.0f}\t{:>21.2f}\n"
        s = fmt1.format("Страна/территория", "Население (тыс)", "Смертей в 2019 г", "Смертей от COVID-19", "% к смертности 2019 г")
        output_file.write( s)
        pop_tot = 0
        dea_tot = 0
        mor_tot = 0
        mor65_tot = 0
        for i, c in enumerate( blist):
            s = fmt2.format(c.Name[:40], c.Population, c.DPA, c.Deaths[-1], c.Relative_Mortality)
            output_file.write( s)
            pop_tot += c.Population
            dea_tot += c.Deaths[-1]
            mor_tot += c.DPA
            mor65_tot += c.DPA65
        s = fmt2.format("Total:", pop_tot, mor_tot, dea_tot, dea_tot * 100 / mor_tot)
        output_file.write( s)
        blist.sort( key=lambda x: x.Relative_Mortality65, reverse=True)
        output_file.write("\nСмерти от COVID-19 как доля от старческих смертей 2019 г\n\n")
        fmt1 = "{:40s}\t{:>15s}\t{:>16s}\t{:>19s}\t{:>21s}\n"
        fmt2 = "{:40s}\t{:>15.3f}\t{:>16.0f}\t{:>19.0f}\t{:>21.2f}\n"
        s = fmt1.format("Страна/территория", "Население (тыс)", "Смертей в 2019 г", "Смертей от COVID-19", "% к смертности 2019 г")
        output_file.write( s)
        pop_tot = 0
        dea_tot = 0
        mor_tot = 0
        mor65_tot = 0
        for i, c in enumerate( blist):
            s = fmt2.format(c.Name[:40], c.Population, c.DPA65, c.Deaths[-1], c.Relative_Mortality65)
            output_file.write( s)
            pop_tot += c.Population
            dea_tot += c.Deaths[-1]
            mor_tot += c.DPA
            mor65_tot += c.DPA65
        s = fmt2.format("Total:", pop_tot, mor65_tot, dea_tot, dea_tot * 100 / mor65_tot)
        output_file.write( s)
        return
    def reportByGDP( self, output_file):
        alist = list( self.Countries.values())
        gdps = []
        gdp_ppps = []
        morts = []
        pops = []
        names = []
        for i, c in enumerate(alist):
            if c.GDP <= 0:
                #print(c.Name)
                continue
            gdps += [c.GDP]
            gdp_ppps += [c.GDP_PPP]
            morts += [max( c.Mortality, 0.1)]
            pops += [max(np.sqrt( c.Population)*10,50)]
            names += [ c.Name]
        #
        # distribution 1
        #
        fig = plt.figure( figsize=(15,15))
        fig.suptitle( 'Распределение COVID-19 от GDP', fontsize=22)
        gs = plt.GridSpec(1, 1, height_ratios=[1]) 
        ax1 = plt.subplot(gs[0])
        ax1.scatter( morts, gdps, pops, c="g", alpha=0.3, marker='s')
        for i, txt in enumerate(names):
            ax1.annotate(txt, (morts[i]*1.1, gdps[i]), fontsize=10)
        ax1.set_xscale("log")
        ax1.set_yscale("log")
        ax1.set_xlabel('смертей на млн')
        ax1.set_ylabel('GDP, $/год/душу')        
        ax1.set_xlim( 0.09, 4000)
        #ax1.set_ylim( 0.02, 400000)
        ax1.grid(True)
        ax1.text(10,400, "площадь маркера пропорциональна населению")
        plt.savefig( "./Graphs/007_COVID19_GDP_XY.png")
        #
        # distribution 2
        #
        fig = plt.figure( figsize=(15,15))
        fig.suptitle( 'Распределение COVID-19 от GDP (PPP)', fontsize=22)
        gs = plt.GridSpec(1, 1, height_ratios=[1]) 
        ax1 = plt.subplot(gs[0])
        ax1.scatter( morts, gdp_ppps, pops, c="g", alpha=0.3, marker='s')
        for i, txt in enumerate(names):
            ax1.annotate(txt, (morts[i]*1.1, gdp_ppps[i]), fontsize=10)
        ax1.set_xscale("log")
        ax1.set_yscale("log")
        ax1.set_xlabel('смертей на млн')
        ax1.set_ylabel('GDP (PPP), $/год/душу')        
        ax1.set_xlim( 0.09, 4000)
        #ax1.set_ylim( 1, 10000)
        ax1.grid(True)
        ax1.text(10,400, "площадь маркера пропорциональна населению")
        plt.savefig( "./Graphs/008_COVID19_GDPPPP_XY.png")
        return
    def outputCountryList( self):
        f = open( ".\Countries\_Countries_COVID19.txt", "w")
        f.write("#\n")
        f.write("# COVID-19 Country data (official WHO count)\n")
        f.write("#\n")
        f.write("Country\tFirst_Case\tConf_Cases\tConf_Deaths\tStatus\n")
        alist = list( self.Countries.values())
        alist.sort( key=lambda x: x.Name, reverse=False)
        for c in alist:
            f.write( str(c) + "\n")
        f.close()
        return
    def Parse1( self, fname):
        sn = "/{:s}.txt".format( fname)
        f1 = open( "./Raw" + sn)
        f2 = open( "./Preparsed" + sn, "w")
        while True:
            sacc = f1.readline()
            if len(sacc) <= 0: break
            sacc = sacc.strip() + "\tInitial Report"
            #print( sacc)
            self.addData( fname, sacc)
            f2.write("{:s}\n".format(sacc))
        f1.close()
        f2.close()
        return
    def Parse2( self, fname):
        exclusions = {"Africa", "Western Pacific Region"}
        removals = [" ‡"]
        replaces = [("International conveyance (Diamond Princess)", "Diamond Princess"),
                    ("Other*", "Diamond Princess")]
        positions_take = {1, 2, 3}
        positions_ignore = {}
        sn = "/{:s}.txt".format( fname)
        f1 = open( "./Raw" + sn)
        f2 = open( "./Preparsed" + sn, "w")
        position = 0
        while True:
            s = f1.readline()
            if len(s) <= 0: break
            s = s.strip()
            if s.startswith("Reporting Cou"): continue
            if s in exclusions: continue
            if position == 0:
                sacc = s
                position += 1
                continue
            if position in positions_take:
                sacc += "\t"
                ss = s.split(' ')
                sacc += ss[0]
                position += 1
                continue
            if position in positions_ignore:
                position += 1
                continue
            if position >= 4:
                for i, r in enumerate( removals):
                    if not r in sacc: continue
                    sacc = sacc.replace(r, "")
                for i, r in enumerate( replaces):
                    if not r[0] in sacc: continue
                    sacc = sacc.replace(r[0], r[1])
                #print(sacc)
                self.addData( fname, sacc)
                f2.write("{:s}\n".format(sacc))
                position = 0
                continue
        f1.close()
        f2.close()
        return    
    def Parse3( self, fname):
        exclusions = {"Africa", "Western Pacific Region", "Region of the Americas", "Eastern Mediterranean Region", "Eastern Mediterranean", "Americas",
        "Territoriesii", "Europe", "South-East Asia", "Western Pacific",  "Reporting Country/Territory/Area", "Total confirmed* cases",
        "Total confirmed* new cases", "Total deaths", "Total new deaths", "Transmission classificationi", "Days since last reported case"}
        removals = ["††","[1]", " ‡", "¶", "^^"]
        replaces = [("International conveyance (Diamond Princess)", "Diamond Princess"),
                    ("Other*", "Diamond Princess"),
                    ("Other†", "Diamond Princess"),
                    ("International conveyance (Diamond Princess) ‡", "Diamond Princess"),
                    ("the United Kingdom","The United Kingdom"),
                    ("the United","United"),
                    ("Occupied Palestinian Territory", "occupied Palestinian territory")]
        positions_take = {1, 3, 5}
        positions_ignore = {2, 4}
        sn = "/{:s}.txt".format( fname)
        f1 = open( "./Raw" + sn)
        f2 = open( "./Preparsed" + sn, "w")
        position = 0
        while True:
            s = f1.readline()
            if len(s) <= 0: break
            s = s.strip()
            if s.startswith("Reporting Cou"): continue
            if s in exclusions: continue
            if position == 0:
                sacc = s
                position += 1
                continue
            if position in positions_take:
                sacc += "\t"
                sacc += s
                position += 1
                continue
            if position in positions_ignore:
                position += 1
                continue
            if position >= 6:
                for i, r in enumerate( removals):
                    if not r in sacc: continue
                    sacc = sacc.replace(r, "")
                for i, r in enumerate( replaces):
                    if not r[0] in sacc: continue
                    sacc = sacc.replace(r[0], r[1])
                self.addData( fname, sacc)
                #print(sacc)
                f2.write("{:s}\n".format(sacc))
                position = 0
                continue
        f1.close()
        f2.close()
        return
    def Parse4( self, fname):
        exclusions = ["Africa", "Western Pacific Region", "Region of the Americas", "Eastern Mediterranean Region",
                "Subtotal for all regions", "Grand total", "Americas"]
        removals = ["††","[1]", " ‡", "¶", "^^"]
        replaces = [("International conveyance (Diamond Princess)", "Diamond Princess"),
                    ("Other*", "Diamond Princess"),
                    ("International conveyance (Diamond Princess) ‡", "Diamond Princess"),
                    ("the United Kingdom","The United Kingdom"),
                    ("the United","United"),
                    ("Occupied Palestinian Territory", "occupied Palestinian territory")]
        treps = ["Community transmission",
                    "Clusters of cases",
                    "Sporadic cases",
                    "No cases",
                    "Not applicable",
                    "Pending"]
        sn = "/{:s}.txt".format( fname)
        f1 = open( "./Raw" + sn)
        f2 = open( "./Preparsed" + sn, "w")
        while(True):
            s = f1.readline()
            if len(s) <= 0: break
            s = s.strip()
            isEx = False
            for i, r in enumerate( exclusions):
                if not s.startswith(r): continue
                isEx = True
                break
            if isEx: continue
            sstatus = "Unknown"
            for i, r in enumerate( treps):
                if not r in s: continue
                sstatus = r
                s = s[:s.find(r)-1]
                break
            for i, r in enumerate( replaces):
                if not r[0] in s: continue
                s = s.replace(r[0], r[1])
            sfoo = s.split( ' ')
            if len( sfoo) < 5: continue
            sacc = sfoo[0]
            sbar = []
            for i, sa in enumerate( sfoo[1:]):
                if sa[:1] in "-1234567890":
                    sbar += [sa]
                    continue
                sacc += " " + sa
            sfoo = []    
            if len(sbar) >= 8:
                sacc += '\t' + sbar[0] + sbar[1] + sbar[2] + '\t' + sbar[5] + sbar[6] + '\t' + sstatus 
                self.addData( fname, sacc)
                f2.write("{:s}\n".format(sacc))
                continue;
            if len(sbar) == 7:
                sacc += '\t' + sbar[0] + sbar[1] + '\t' + sbar[4] + sbar[5] + '\t' + sstatus 
                self.addData( fname, sacc)
                f2.write("{:s}\n".format(sacc))
                continue;
            if len(sbar) == 6:
                sacc += '\t' + sbar[0] + sbar[1] + '\t' + sbar[3] + sbar[4] + '\t' + sstatus 
                self.addData( fname, sacc)
                f2.write("{:s}\n".format(sacc))
                continue;
            if len(sbar) == 5:
                sacc += '\t' + sbar[0] + sbar[1] + '\t' + sbar[3] + '\t' + sstatus 
                self.addData( fname, sacc)
                f2.write("{:s}\n".format(sacc))
                continue;
            if len(sbar) == 4:
                sacc += '\t' + sbar[0] + '\t' + sbar[2] + '\t' + sstatus 
                self.addData( fname, sacc)
                f2.write("{:s}\n".format(sacc))
                continue;
            print("Error: {:s}".format(sacc))
            continue
        f1.close()
        f2.close()
        return
    def ParseWeekly( self, fname, dates):
        exclusions0 = ["Reporting Country/Territory/Area",
                 "New cases in last 7 days",
                 "Cumulative cases",
                 "Cumulative cases per 1 million population",
                 "New deaths in last 7 days",
                 "Cumulative deaths",
                 "Cumulative deaths per 1 million population",
                 "Transmission classification",
                 "Territoriesii"]
        exclusions4 = ["Subtotal for all regions"]
        exclusions6 = ["Africa",
                       "Americas",
                       "Eastern Mediterranean",
                       "Europe",
                       "Western Pacific",
                       "South-East Asia"]
        cycleBreak = ["Grand total"]
        removals = [ "[1]"]
        replaces = [ ("Cote D’Ivoire", "Cote d’Ivoire"),
                    ("Democratic Republic of The Congo", "Democratic Republic of the Congo"),
                    ("Lao People'S Democratic Republic", "Lao People's Democratic Republic"),
                    ("Solomon Islands", "Solomon Islands"),
                    ("Northern Mariana Islands (Commonwealth of The)", "Northern Mariana Islands (Commonwealth of the)"),
                    ("Wallis and Futuna", "Wallis and Futuna Islands"),
                    ("Other†", "Diamond Princess"),
                    ("Occupied Palestinian territory", "occupied Palestinian territory")]
        date = fname.replace("weekly_20","20")
        sn = "/{:s}.txt".format( fname)
        f1 = open( "./Raw" + sn)
        f2 = open( "./Preparsed" + sn, "w")
        while(True):
            s = f1.readline()
            if len(s) <= 0: break
            s = s.strip()
            if s in cycleBreak: break
            if s in exclusions0:
                continue
            if s in exclusions4:
                for i in range(4): f1.readline()
                continue
            if s in exclusions6:
                for i in range(6): f1.readline()
                continue
            for r in removals:
                s = s.replace( r, "")
            for r in replaces:
                s = s.replace( r[0], r[1])
            if not s in self.Countries:
                print( "New territory: " + s)
                self.Countries[s] = Covid_Country(s)
            country = self.Countries[s]
            ss = [f1.readline()] # new cases
            ss += [f1.readline().strip()] # total cases
            if s == "Diamond Princess": 
                f1.readline() # new deaths
                ss += [f1.readline().strip()] # total deaths
                ss += ["No cases"]
            else:
                f1.readline() # cum cases per million
                f1.readline() # new deaths
                ss += [f1.readline().strip()] # total deaths
                f1.readline() # cum deaths per million
                ss += [f1.readline().strip()]
            country.addDataWeek( dates, ss)
        f1.close()
        f2.close()
        return
