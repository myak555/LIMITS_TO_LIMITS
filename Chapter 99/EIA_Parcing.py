import fnmatch
from Predictions import *


class API_MetadataCode:
    def __init__(self, s):
        args = s.split("\t")
        if len(args) < 14:
            self.Code = None
            return
        self.Code = args[0] 
        self.Region = args[1]
        self.Group = int( args[2])
        self.Order = int( args[3])
        self.EnglishName = args[4]
        self.RussianName = args[5]
        self.Population = args[6]
        self.Territory = args[7]
        self.GDP = args[8]
        self.GDP_PPP = args[9]
        self.Peak_Year = args[10]
        self.Peak_Production = args[11]
        self.Production_2020 = args[12]
        self.Pick_Production = args[13]
        return

 
class EIA_Country:
    def __init__(self, code=None):
        self.Code = code
        self.Name = "Unknown"
        self.RussianName = "Неизвестно"
        self.Region = None
        self.Group = None
        self.Order = None
        self.Population = 0.0
        self.Territory = 0.0
        self.GDP = 0.0
        self.GDP_PPP = 0.0
        self.Peak_Year = None
        self.Peak_Production = None
        self.Production_2020 = None
        self.Pick_Production = False
        self.Total = []
        self.CNOL = []
        self.Crude = []
        self.NGPL = []
        self.Other = []
        self.ProcessingGain = []
        self.Historical_Data = []
        return

    def readFile(self, file, metadata, lnMax):
        s = file.readline().strip()
        if not s.startswith(","): return
        if s.startswith(',"'):
            self.Name = s[2:].split('"')[0]
        else:
            self.Name = s.split(',')[1]
        file.readline() # skip "Production"
        s = file.readline().strip()
        if s.startswith("none"): self.Code = "None"
        else:
            ss = s.split("INTL.53-1-")
            self.Code = ss[1].split("-TB")[0]
        if self.Name == "Kosovo": self.Code = "KOS"
        if self.Name == "Micronesia": self.Code = "MICN"
        if self.Name == "Northern Mariana Islands": self.Code = "NMI"
        if self.Name == "Tuvalu": self.Code = "TVL"
        if self.Name == "U.S. Territories": self.Code = "USIT"
        self.Total = self.ProcessLine(s, lnMax)     
        s = file.readline().strip()
        if len(s) <= 0: return
        self.CNOL = self.ProcessLine(s, lnMax)
        s = file.readline().strip()
        if len(s) <= 0: return
        self.Crude = self.ProcessLine(s, lnMax)
        s = file.readline().strip()
        if len(s) <= 0: return
        self.NGPL = self.ProcessLine(s, lnMax)
        s = file.readline().strip()
        if len(s) <= 0: return
        self.Other = self.ProcessLine(s, lnMax)
        s = file.readline().strip()
        if len(s) <= 0: return
        self.ProcessingGain = self.ProcessLine(s, lnMax)
        self.applyMetadata(metadata)
        if self.Code == "CAN": self.RemoveTarSand()
        return
        
    def Load_BP_Data(self):
        BP_Listed = ["Canada",
            "Mexico",
            "United States of America",
            "Argentina",
            "Brazil",
            "Colombia",
            "Ecuador",
            "Peru",
            "Trinidad and Tobago",
            "Venezuela (Bolivarian Republic of)",
            "Denmark",
            "Italy",
            "Norway",
            "Romania",
            "The United Kingdom",
            "Azerbaijan",
            "Kazakhstan",
            "Russian Federation",
            "Turkmenistan",
            "Uzbekistan",
            "Iran (Islamic Republic of)",
            "Iraq",
            "Kuwait",
            "Oman",
            "Qatar",
            "Saudi Arabia",
            "Syrian Arab Republic",
            "United Arab Emirates",
            "Yemen",
            "Algeria",
            "Angola",
            "Chad",
            "Congo",
            "Egypt",
            "Equatorial Guinea",
            "Gabon",
            "Libya",
            "Nigeria",
            "South Sudan",
            "Sudan",
            "Tunisia",
            "Australia",
            "Brunei Darussalam",
            "China",
            "India",
            "Indonesia",
            "Malaysia",
            "Thailand",
            "Viet Nam"]
        if not self.Name in BP_Listed:
            self.BP_Year = []
            self.BP_CnC = []
            return
        print("Load BP for: {:s}".format(self.Name))
        self.BP_Year, self.BP_CnC = Load_Calibration("./Data/BP_Comparison_2021.csv", ["Year", self.Name], separator="\t")
        if len(self.BP_CnC) <= 0:
            print("Warning, no BP data: {:s}".format(self.Name))        
        return

    def applyMetadata(self, metadata):
        if self.Code is None:
            print("Code is None")
            return
        if not self.Code in metadata:
            print( "Code {:s} ({:s}) is not in metadata".format(self.Code, self.Name))
            return
        m = metadata[self.Code]
        self.Name = m.EnglishName
        self.RussianName = m.RussianName
        self.Region = m.Region
        self.Group = int( m.Group)
        self.Order = int( m.Order)
        self.Population = float( m.Population)
        self.Territory = float( m.Territory)
        self.GDP = float(m.GDP)
        self.GDP_PPP = float(m.GDP_PPP)
        self.Peak_Year = m.Peak_Year
        try:
            self.Peak_Production = float( m.Peak_Production)
        except:
            self.Peak_Production = -999.25
        try:
            self.Production_2020 = float( m.Production_2020)
        except:
            self.Production_2020 = -999.25
        self.Pick_Production = m.Pick_Production == "Yes"
        self.Load_BP_Data()
        return

    def SaveCrude(self, filename, years):
        f = open(filename, "wt")
        f.write( "Year\tCrude\tNGPL\n")
        for i, y in enumerate( years):
            f.write( "{:.0f}\t{:.1f}\t{:.1f}\n".format(y, self.Crude[i],self.NGPL[i]))
        f.close()
        return

    def ProcessLine( self, s, lnMax):
        tmp = []
        s = s.replace('        Total petroleum and other liquids (Mb/d)', '')
        s = s.replace('"            Crude oil, NGPL, and other liquids (Mb/d)"', '')
        s = s.replace('                Crude oil including lease condensate (Mb/d)', '')
        s = s.replace('                NGPL (Mb/d)', '')
        s = s.replace('                Other liquids (Mb/d)', '')
        s = s.replace('            Refinery processing gain (Mb/d)', '')
        ss = s.split(',')
        tmp = []
        for s in ss[2:]:
            if len(tmp) >= lnMax: break
            if len(s) <= 0 or s == "--" or s == "NA":
                tmp += [-999.25]
                continue
            if s == "(s)":
                tmp += [0.01]
                continue
            tmp += [float(s)]
        return np.array( tmp)

    def Plot( self, years, folder):
        yTotal, dTotal = self.GetAvailable( years, self.Total)
        yCrude, dCrude = self.GetAvailable( years, self.Crude)
        yNGPL, dNGPL = self.GetAvailable( years, self.NGPL)
        yOther, dOther = self.GetAvailable( years, self.Other)
        if len(yTotal) <= 0 and len(yCrude) <= 0 and len(yNGPL) <= 0 and len(yOther) <= 0:
            #print( "{:s} has no production data".format(self.Name))
            return
        dTotal *= 0.835 # 0.835
        dCrude *= 0.875 # 0.835
        dNGPL *= 0.760
        dOther *= 0.835
        fig = plt.figure( figsize=(15,10))
        fig.suptitle( 'Добыча нефти и жидкостей: {:s}'.format( self.RussianName), fontsize=22)
        gs = plt.GridSpec(1, 1, height_ratios=[1]) 
        ax1 = plt.subplot(gs[0])
        maxScale = 0
        if len(yTotal) > 0:
            ax1.bar( yTotal, dTotal, width=1, color="y", alpha=0.2, label='Всего')
            maxScale = max( maxScale, max( dTotal))
        if len(yCrude) > 0:
            ax1.plot( yCrude, dCrude, '-', lw=4, color="g", label='Нефти и конденсата')
            ax1.scatter( yCrude, dCrude, 100, c="g", marker='s')
            maxScale = max( maxScale, max( dCrude))
        if len(yNGPL) > 0:
            ax1.plot( yNGPL, dNGPL, '-', lw=3, color="r", label='ШФЛУ')
            ax1.scatter( yNGPL, dNGPL, 50, c="r", marker='s')
            maxScale = max( maxScale, max( dNGPL))
        if len(yOther) > 0:
            ax1.bar( yOther, dOther, width=1, color="y", alpha=0.5, label='Прочих')
            maxScale = max( maxScale, max( dOther))
        lHist = len( self.Historical_Data ) 
        if lHist > 0:
            ax1.plot( np.linspace( 1980, 1979+lHist, lHist), self.Historical_Data*0.365*0.159*0.875,
            '-.', lw=2, color="k", label='Данные EIA {:d} г'.format(lHist+1980))
        if len(self.BP_CnC) > 0:
            ax1.plot( self.BP_Year, self.BP_CnC, '-.', lw=3, color="b", label='БП, 2021')
            ax1.scatter( self.BP_Year, self.BP_CnC, 30, c="b", marker='s')
            ax1.text( self.BP_Year[-1], self.BP_CnC[-1], "{:.1f}".format(self.BP_CnC[-1]), color="b")
            maxScale = max( maxScale, max( self.BP_CnC))
        ax1.set_xlabel('Годы')
        ax1.set_ylabel('млн тонн в год')    
        ax1.set_xlim( 1970, 2030)
        ax1.set_ylim( 0, maxScale*1.3)
        ax1.text( 2005, maxScale * 1.25, 
                "Население: {:.1f} тыс.".format( self.Population))
        ax1.text( 2005, maxScale * 1.20, 
                "Территория: {:.1f} км²".format( self.Territory))
        if self.Group == 1 and len(yCrude) >= 1:
            ax1.text( 2005, maxScale * 1.15, 
                "Добычи в {:.0f} году нет".format( yCrude[-1]))
        elif self.Group != 1 and len(yCrude) >= 1:
            if self.Pick_Production: self.Production_2020 = dCrude[-1]
            ax1.text( 2005, maxScale * 1.15, 
                "Добыча в {:.0f} году: {:.3f} млн т".format( yCrude[-1], self.Production_2020))
        else: 
            ax1.text( 2005, maxScale * 1.15, "Добычи нет")            
        peakYear = float(self.Peak_Year)
        if peakYear > 0:
            ax1.plot( [peakYear, peakYear], [0, maxScale], '--', lw=1, color="k")
            if self.Peak_Production < 0.0:
                self.Peak_Production = max( dCrude)
            ax1.text( 2005, maxScale*1.10, 
                "Пик добычи: {:.3f} млн т. в {:s} г".format( self.Peak_Production, self.Peak_Year))
            if self.Production_2020 > 0 and peakYear < yCrude[-1]:
                ax1.text( 2005, maxScale*1.05, 
                    "Добыча {:.0f} г к пику: {:.1f}%".format( yCrude[-1], self.Production_2020*100/self.Peak_Production))
        ax1.grid(True)
        ax1.legend(loc=2)
        plt.savefig( folder + self.Name + ".png")
        plt.close('all')
        return

    #
    # Returnes data in mln m3
    #
    def GetAvailable( self, years, data):
        start = len(data)
        stop = start
        for i, d in enumerate(data):
            if d <= 0.0: continue
            start = i
            break
        for i in range( len(data)-1, start):
            if d <= 0.0: continue
            stop = i
            break
        return years[start:stop], data[start:stop]*0.365*0.159
    #
    # Removes tar sand from crude (Canada only)
    #
    def RemoveTarSand( self):
        Year, Total = Load_Calibration( "../Global Data/Canada_Tar_Sand_Production.csv", ["Year", "Total"], separator='\t')
        print( self.Crude)
        print( len(self.Crude))
        self.Crude -= Total[1973-int(Year[0]):]
        return

class EIA_Countries:
    def __init__(self, fileName):
        print()
        print( "Loading {:s}".format( fileName))
        self.loadMetadata( "./Data/_API_Metadata.csv")
        print( "Loaded {:d} country codes from _API_Metadata.csv".format( len(self.Metadata)))
        self.Countries = {}
        self.Years = []
        f = open( fileName)
        f.readline()
        s = f.readline().strip()
        ss = s.split(',')
        for s in ss[2:]:
            self.Years += [float(s)]
        self.Years = np.array( self.Years)
        lnMax = len(self.Years)
        print( "Years from {:.0f} to {:.0f} ({:d})".format( self.Years[0], self.Years[-1], lnMax))
        for i in range(1000):
            c = EIA_Country()
            c.readFile(f, self.Metadata, lnMax)
            #print( c.Name, c.Code, len(c.Total))
            if c.Code is None: break
            if c.Code in self.Countries:
                print("{:s} already in the set".format(c.Code))
            else:
                self.Countries[c.Code] = c
                #print("Parsed {:4s}: {:s}".format(c.Code,c.Name))
        f.close()
        return
    def loadMetadata(self, filename):
        f = open (filename, encoding="UTF-8")
        self.Metadata = {}
        self.TotalPopulation = 0.0
        self.TotalLandMass = 0.0
        self.AverageGDP = 0.0
        self.AverageGDPppp = 0.0
        while True:
            s = f.readline()
            if len(s) <= 0: break
            s = s.strip()
            if s.startswith('#'): continue 
            if s.startswith('Code\t'): continue 
            m = API_MetadataCode( s)
            if m.Code is None: break
            self.Metadata[m.Code] = m
            if m.Group <= 0: continue
            if m.Code == "MINI": continue
            p = float( m.Population)
            t = float( m.Territory)
            g = float( m.GDP)
            gp = float( m.GDP_PPP)
            if p<0 or t<0 or g<0 or gp<0:
                print("Warning: {:s} has negative values".format(m.Code))
            else:
                self.TotalPopulation += p
                self.TotalLandMass += t
                self.AverageGDP += g*p
                self.AverageGDPppp += gp*p
            #print("Added: {:s}: {:s} ({:s}))".format(m.Code, m.EnglishName, m.RussianName))
        self.AverageGDP /= self.TotalPopulation
        self.AverageGDPppp /= self.TotalPopulation
        print("Total population: {:.1f} mln".format( self.TotalPopulation/1000))
        print("Total land mass: {:.3f} mln km²".format( self.TotalLandMass/1e6))
        print("Average GDP per capita: ${:.0f}".format( self.AverageGDP))
        print("Average GDP_PPP per capita: ${:.0f}".format( self.AverageGDPppp))
        f.close()
        return
    def loadHistorical(self, filename):
        count = 0
        f = open (filename, encoding="UTF-8")
        while True:
            s = f.readline()
            if len(s) <= 0: break
            s = s.strip()
            if s.startswith('#'): continue 
            if s.startswith('Code\t'): continue
            ss = s.split("\t")
            code = ss[0]
            name = ss[2]
            if not code in self.Countries:
                print( "Code {:s} not found".format(code, name))
                continue
            c = self.Countries[code]
            tmp = []
            for d in ss[3:] : tmp += [float(d)]
            c.Historical_Data = np.array(tmp)
            count += 1
            #print("Added historical: {:s} ({:s})".format(code, c.Name))
        f.close()
        print("Added historical data for {:d} territories".format(count))
        return
    def combineProduction( self, src1, src2, dest):
        dest.Total = np.clip( dest.Total, 0.0, None)
        dest.Total += np.clip( src1.Total, 0.0, None)
        dest.Total += np.clip( src2.Total, 0.0, None)
        dest.CNOL = np.clip( dest.CNOL, 0.0, None)
        dest.CNOL += np.clip( src1.CNOL, 0.0, None)
        dest.CNOL += np.clip( src2.CNOL, 0.0, None)
        dest.Crude = np.clip( dest.Crude, 0.0, None)
        dest.Crude += np.clip( src1.Crude, 0.0, None)
        dest.Crude += np.clip( src2.Crude, 0.0, None)
        dest.NGPL = np.clip( dest.NGPL, 0.0, None)
        dest.NGPL += np.clip( src1.NGPL, 0.0, None)
        dest.NGPL += np.clip( src2.NGPL, 0.0, None)
        dest.Other = np.clip( dest.Other, 0.0, None)
        dest.Other += np.clip( src1.Other, 0.0, None)
        dest.Other += np.clip( src2.Other, 0.0, None)
        dest.ProcessingGain = np.clip( dest.ProcessingGain, 0.0, None)
        dest.ProcessingGain += np.clip( src1.ProcessingGain, 0.0, None)
        dest.ProcessingGain += np.clip( src2.ProcessingGain, 0.0, None)
        return
    def splitProduction( self, src, dest, proportions):
        src.Total = np.clip( src.Total, 0.0, None)
        src.CNOL = np.clip( src.CNOL, 0.0, None)
        src.Crude = np.clip( src.Crude, 0.0, None)
        src.NGPL = np.clip( src.NGPL, 0.0, None)
        src.Other = np.clip( src.Other, 0.0, None)
        src.ProcessingGain = np.clip( src.ProcessingGain, 0.0, None)
        for i, p in enumerate(proportions):
            d = dest[i]
            d.Total = np.clip( d.Total, 0.0, None) + p*src.Total
            d.CNOL = np.clip( d.CNOL, 0.0, None) + p*src.CNOL
            d.Crude = np.clip( d.Crude, 0.0, None) + p*src.Crude
            d.NGPL = np.clip( d.NGPL, 0.0, None) + p*src.NGPL
            d.Other = np.clip( d.Other, 0.0, None) + p*src.Other
            d.ProcessingGain = np.clip( d.ProcessingGain, 0.0, None) + p*src.ProcessingGain
        return
    def processDeprecated(self, foldername):
        print( "Combining East and West Germany")
        c1 = self.Countries["DDR"]
        c2 = self.Countries["DEUW"]
        c3 = self.Countries["DEU"]
        self.combineProduction( c1, c2, c3)
        c1.Plot( self.Years, foldername)
        c2.Plot( self.Years, foldername)
        c3.Plot( self.Years, foldername)
        print( "Splitting Czechia and Slovakia")
        c1 = self.Countries["CSK"]
        c2 = self.Countries["CZE"]
        c3 = self.Countries["SVK"]
        self.splitProduction( c1, [c2,c3], [0.6, 0.4])
        c1.Plot( self.Years, foldername)
        c2.Plot( self.Years, foldername)
        c3.Plot( self.Years, foldername)
        print( "Processing former Serbia and Montenegro")
        c1 = self.Countries["SCG"]
        c2 = self.Countries["MNE"]
        c3 = self.Countries["SRB"]
        self.combineProduction( c1, c2, c3)
        c1.Plot( self.Years, foldername)
        c2.Plot( self.Years, foldername)
        c3.Plot( self.Years, foldername)
        print( "Splitting former Yugoslavia")
        c1 = self.Countries["YUG"]
        c2 = self.Countries["SRB"]
        c3 = self.Countries["HRV"]
        self.splitProduction( c1, [c2,c3], [0.4, 0.6])
        c1.Plot( self.Years, foldername)
        c2.Plot( self.Years, foldername)
        c3.Plot( self.Years, foldername)
        print( "Splitting former USSR")
        c1 = self.Countries["SUN"]
        c2 = self.Countries["RUS"]
        c3 = self.Countries["KAZ"]
        c4 = self.Countries["AZE"]
        c5 = self.Countries["LTU"]
        c6 = self.Countries["GEO"]
        c7 = self.Countries["TJK"]
        c8 = self.Countries["TKM"]
        c9 = self.Countries["BLR"]
        c10 = self.Countries["UKR"]
        c11 = self.Countries["KGZ"]
        c12 = self.Countries["UZB"]
        # EST, MDA, LVA, ARM - group 1, no production
        splitList = [c2, c3, c4, c5, c6, c7, c8, c9, c10, c11, c12]
        sumprod = 0.0
        for c in splitList: sumprod += max(c.Crude[19], 0)
        #print(c1.Crude[18], sumprod)
        splits = []
        for c in splitList:
            splits += [c.Crude[19]/sumprod]
            #print( "{:s} = {:.4f}".format(c.Name, splits[-1]))
        self.splitProduction( c1, splitList, splits)
        c1.Plot( self.Years, foldername)
        for c in splitList:
            c.Plot( self.Years, foldername)
        print("Deprecated processed")
        return
    def processSmallTerritories(self, foldername):
        count = 0
        f = open( foldername+"_Report.txt", "wb")
        processing_order = []
        for code in self.Countries:
            country = self.Countries[code]
            if country.Region != "SMALL": continue
            if country.Code == "MINI": continue
            processing_order += [ country]
        processing_order.sort( key=lambda x: x.Order)
        combined = EIA_Country( "MINI")
        combined.applyMetadata( self.Metadata)
        l = len( self.Years)
        combined.Total = np.zeros(l)
        combined.CNOL = np.zeros(l)
        combined.Crude = np.zeros(l)
        combined.NGPL = np.zeros(l)
        combined.Other = np.zeros(l)
        combined.ProcessingGain = np.zeros(l)
        combined.Population = 0.0
        combined.Territory = 0.0
        combined.GDP = 0.0
        combined.GDP_PPP = 0.0
        for country in processing_order:
            country.Plot( self.Years, foldername )
            s = "{:s}\t{:s}".format( country.Code, country.RussianName)
            s += "\t"
            s += "\t"
            s += "\t"
            s += "\t"
            s += "\t{:.1f}".format( country.Population)
            s += "\t{:.3f}%".format( country.Population * 100 / self.TotalPopulation)
            s += "\t{:.0f}".format( country.Territory)
            s += "\t{:.3f}%".format( country.Territory * 100 / self.TotalLandMass)
            #print(s)
            s += "\r\n"
            f.write(s.encode("UTF-8"))
            combined.Population += country.Population
            combined.Territory += country.Territory
            combined.GDP += country.GDP * country.Population
            combined.GDP_PPP += country.GDP_PPP * country.Population
            combined.Total += np.clip( country.Total, 0.0, None)
            combined.CNOL += np.clip( country.CNOL, 0.0, None)
            combined.Crude += np.clip( country.Crude, 0.0, None)
            combined.NGPL += np.clip( country.NGPL, 0.0, None)
            combined.Other += np.clip( country.Other, 0.0, None)
            combined.ProcessingGain = np.clip( country.ProcessingGain, 0.0, None)
            count += 1
        combined.GDP /=  combined.Population 
        combined.GDP_PPP /=  combined.Population 
        self.Countries[ combined.Code] = combined
        s = "\tВсего малые территории:"
        s += "\t" # no peak year
        s += "\t" # no peak value
        s += "\t" # no last year production
        s += "\t" # no % to peak
        s += "\t{:.1f}".format( combined.Population)
        s += "\t{:.2f}%".format( combined.Population * 100 / self.TotalPopulation)
        s += "\t{:.0f}".format( combined.Territory)
        s += "\t{:.2f}%".format( combined.Territory * 100 / self.TotalLandMass)
        print(s)
        s += "\r\n"
        f.write(s.encode("UTF-8"))
        f.close()
        combined.Plot( self.Years, foldername )
        print("Small countries GDP = ${:.0f} per capita".format( combined.GDP))
        print("Small countries GDP PPP = ${:.0f} per capita".format( combined.GDP_PPP))
        print("{:d} small territories processed".format(count))
        return
    def processGroup1(self, foldername):
        count = 0
        f = open( foldername+"_Report.txt", "wb")
        processing_order = []
        for code in self.Countries:
            country = self.Countries[code]
            if country.Group != 1: continue
            if country.Region == "SMALL" and country.Code != "MINI": continue
            processing_order += [ country]
        processing_order.sort( key=lambda x: x.Order)
        combined = EIA_Country( "GRP1")
        combined.applyMetadata( self.Metadata)
        l = len( self.Years)
        combined.Total = np.zeros(l)
        combined.CNOL = np.zeros(l)
        combined.Crude = np.zeros(l)
        combined.NGPL = np.zeros(l)
        combined.Other = np.zeros(l)
        combined.ProcessingGain = np.zeros(l)
        combined.Population = 0.0
        combined.Territory = 0.0
        combined.GDP = 0.0
        combined.GDP_PPP = 0.0
        for country in processing_order:
            country.Plot( self.Years, foldername )
            s = "{:s}\t{:s}".format( country.Code, country.RussianName)
            s += "\t" + country.Peak_Year.replace('-999', '')
            if country.Peak_Production > 0.0:
                s += "\t{:.1f}".format( country.Peak_Production)
            else:
                s += "\t"
            s += "\t"
            s += "\t"
            s += "\t{:.1f}".format( country.Population)
            s += "\t{:.2f}%".format( country.Population * 100 / self.TotalPopulation)
            s += "\t{:.0f}".format( country.Territory)
            s += "\t{:.2f}%".format( country.Territory * 100 / self.TotalLandMass)
            #print(s)
            s += "\r\n"
            f.write(s.encode("UTF-8"))
            combined.Population += country.Population
            combined.Territory += country.Territory
            combined.GDP += country.GDP * country.Population
            combined.GDP_PPP += country.GDP_PPP * country.Population
            combined.Total += np.clip( country.Total, 0.0, None)
            combined.CNOL += np.clip( country.CNOL, 0.0, None)
            combined.Crude += np.clip( country.Crude, 0.0, None)
            combined.NGPL += np.clip( country.NGPL, 0.0, None)
            combined.Other += np.clip( country.Other, 0.0, None)
            combined.ProcessingGain = np.clip( country.ProcessingGain, 0.0, None)
            count += 1
        combined.GDP /=  combined.Population 
        combined.GDP_PPP /=  combined.Population 
        self.Countries[ combined.Code] = combined
        s = "\tВсего группа 1:"
        s += "\t{:s}".format(combined.Peak_Year)
        s += "\t{:.1f}".format(combined.Peak_Production)
        s += "\t"
        s += "\t"
        s += "\t{:.1f}".format( combined.Population)
        s += "\t{:.2f}%".format( combined.Population * 100 / self.TotalPopulation)
        s += "\t{:.0f}".format( combined.Territory)
        s += "\t{:.2f}%".format( combined.Territory * 100 / self.TotalLandMass)
        print(s)
        s += "\r\n"
        f.write(s.encode("UTF-8"))
        f.close()
        combined.Plot( self.Years, foldername )
        combined.SaveCrude( "./Data/Crude_Group_1.csv", self.Years)
        print("Group 1 GDP = ${:.0f} per capita".format( combined.GDP))
        print("Group 1 GDP PPP = ${:.0f} per capita".format( combined.GDP_PPP))
        print("{:d} countries of Group 1 processed".format(count))
        return
    def processGroup2(self, foldername):
        count = 0
        f = open( foldername+"_Report.txt", "wb")
        processing_order = []
        for code in self.Countries:
            country = self.Countries[code]
            if country.Group != 2: continue
            processing_order += [ country]
        processing_order.sort( key=lambda x: x.Order)
        combined = EIA_Country( "GRP2")
        combined.applyMetadata( self.Metadata)
        l = len( self.Years)
        combined.Total = np.zeros(l)
        combined.CNOL = np.zeros(l)
        combined.Crude = np.zeros(l)
        combined.NGPL = np.zeros(l)
        combined.Other = np.zeros(l)
        combined.ProcessingGain = np.zeros(l)
        combined.Population = 0.0
        combined.Territory = 0.0
        combined.GDP = 0.0
        combined.GDP_PPP = 0.0
        for country in processing_order:
            country.Plot( self.Years, foldername )
            s = "{:s}\t{:s}".format( country.Code, country.RussianName)
            s += "\t" + country.Peak_Year.replace('-999', '')
            s += "\t{:.2f}".format( country.Peak_Production)
            s += "\t{:.2f}".format( country.Production_2020)
            s += "\t{:.2f}%".format( country.Production_2020*100/country.Peak_Production)
            s += "\t{:.1f}".format( country.Population)
            s += "\t{:.2f}%".format( country.Population * 100 / self.TotalPopulation)
            s += "\t{:.0f}".format( country.Territory)
            s += "\t{:.2f}%".format( country.Territory * 100 / self.TotalLandMass)
            print(s)
            s += "\r\n"
            f.write(s.encode("UTF-8"))
            combined.Population += country.Population
            combined.Territory += country.Territory
            combined.GDP += country.GDP * country.Population
            combined.GDP_PPP += country.GDP_PPP * country.Population
            combined.Total += np.clip( country.Total, 0.0, None)
            combined.CNOL += np.clip( country.CNOL, 0.0, None)
            combined.Crude += np.clip( country.Crude, 0.0, None)
            combined.NGPL += np.clip( country.NGPL, 0.0, None)
            combined.Other += np.clip( country.Other, 0.0, None)
            combined.ProcessingGain = np.clip( country.ProcessingGain, 0.0, None)
            count += 1
        combined.GDP /=  combined.Population 
        combined.GDP_PPP /=  combined.Population 
        self.Countries[ combined.Code] = combined
        s = "\tВсего группа 2:"
        s += "\t{:s}".format(combined.Peak_Year)
        s += "\t{:.2f}".format(combined.Peak_Production)
        s += "\t{:.2f}".format( combined.Production_2020)
        s += "\t{:.2f}%".format( combined.Production_2020*100/combined.Peak_Production)
        s += "\t{:.1f}".format( combined.Population)
        s += "\t{:.2f}%".format( combined.Population * 100 / self.TotalPopulation)
        s += "\t{:.0f}".format( combined.Territory)
        s += "\t{:.2f}%".format( combined.Territory * 100 / self.TotalLandMass)
        print(s)
        s += "\r\n"
        f.write(s.encode("UTF-8"))
        f.close()
        combined.Plot( self.Years, foldername )
        combined.SaveCrude( "./Data/Crude_Group_2.csv", self.Years)
        print("Group 2 GDP = ${:.0f} per capita".format( combined.GDP))
        print("Group 2 GDP PPP = ${:.0f} per capita".format( combined.GDP_PPP))
        print("{:d} countries of Group 2 processed".format(count))
        return
    def processGroup3(self, foldername):
        count = 0
        f = open( foldername+"_Report.txt", "wb")
        processing_order = []
        for code in self.Countries:
            country = self.Countries[code]
            if country.Group != 3: continue
            processing_order += [ country]
        processing_order.sort( key=lambda x: x.Order)
        combined = EIA_Country( "GRP3")
        combined.applyMetadata( self.Metadata)
        l = len( self.Years)
        combined.Total = np.zeros(l)
        combined.CNOL = np.zeros(l)
        combined.Crude = np.zeros(l)
        combined.NGPL = np.zeros(l)
        combined.Other = np.zeros(l)
        combined.ProcessingGain = np.zeros(l)
        combined.Population = 0.0
        combined.Territory = 0.0
        combined.GDP = 0.0
        combined.GDP_PPP = 0.0
        for country in processing_order:
            country.Plot( self.Years, foldername )
            s = "{:s}\t{:s}".format( country.Code, country.RussianName)
            s += "\t" + country.Peak_Year
            s += "\t{:.2f}".format( country.Peak_Production)
            s += "\t{:.2f}".format( country.Production_2020)
            s += "\t{:.2f}%".format( country.Production_2020*100/country.Peak_Production)
            s += "\t{:.1f}".format( country.Population)
            s += "\t{:.2f}%".format( country.Population * 100 / self.TotalPopulation)
            s += "\t{:.0f}".format( country.Territory)
            s += "\t{:.2f}%".format( country.Territory * 100 / self.TotalLandMass)
            print(s)
            s += "\r\n"
            f.write(s.encode("UTF-8"))
            combined.Population += country.Population
            combined.Territory += country.Territory
            combined.GDP += country.GDP * country.Population
            combined.GDP_PPP += country.GDP_PPP * country.Population
            combined.Total += np.clip( country.Total, 0.0, None)
            combined.CNOL += np.clip( country.CNOL, 0.0, None)
            combined.Crude += np.clip( country.Crude, 0.0, None)
            combined.NGPL += np.clip( country.NGPL, 0.0, None)
            combined.Other += np.clip( country.Other, 0.0, None)
            combined.ProcessingGain = np.clip( country.ProcessingGain, 0.0, None)
            count += 1
        combined.GDP /=  combined.Population 
        combined.GDP_PPP /=  combined.Population 
        self.Countries[ combined.Code] = combined
        s = "\tВсего группа 3:"
        s += "\t{:s}".format(combined.Peak_Year)
        s += "\t{:.2f}".format(combined.Peak_Production)
        s += "\t{:.2f}".format( combined.Production_2020)
        s += "\t{:.2f}%".format( combined.Production_2020*100/combined.Peak_Production)
        s += "\t{:.1f}".format( combined.Population)
        s += "\t{:.2f}%".format( combined.Population * 100 / self.TotalPopulation)
        s += "\t{:.0f}".format( combined.Territory)
        s += "\t{:.2f}%".format( combined.Territory * 100 / self.TotalLandMass)
        print(s)
        s += "\r\n"
        f.write(s.encode("UTF-8"))
        f.close()
        combined.Plot( self.Years, foldername )
        combined.SaveCrude( "./Data/Crude_Group_3.csv", self.Years)
        print("Group 3 GDP = ${:.0f} per capita".format( combined.GDP))
        print("Group 3 GDP PPP = ${:.0f} per capita".format( combined.GDP_PPP))
        print("{:d} countries of Group 3 processed".format(count))
        return

    def processTopProducers(self, foldername, cutoff):
        count = 0
        f = open( foldername+"_Report.txt", "wb")
        processing_order = []
        for code in self.Countries:
            country = self.Countries[code]
            if country.Group != 2 and country.Group != 3: continue
            if country.Production_2020 <= cutoff: continue
            processing_order += [ country]
        processing_order.sort( key=lambda x: x.Order)
        combined = EIA_Country( "TOPPRD")
        combined.applyMetadata( self.Metadata)
        l = len( self.Years)
        combined.Total = np.zeros(l)
        combined.CNOL = np.zeros(l)
        combined.Crude = np.zeros(l)
        combined.NGPL = np.zeros(l)
        combined.Other = np.zeros(l)
        combined.ProcessingGain = np.zeros(l)
        combined.Population = 0.0
        combined.Territory = 0.0
        combined.GDP = 0.0
        combined.GDP_PPP = 0.0
        for country in processing_order:
            country.Plot( self.Years, foldername )
            s = "{:s}\t{:s}".format( country.Code, country.RussianName)
            s += "\t" + country.Peak_Year
            s += "\t{:.2f}".format( country.Peak_Production)
            s += "\t{:.2f}".format( country.Production_2020)
            s += "\t{:.2f}%".format( country.Production_2020*100/country.Peak_Production)
            s += "\t{:.1f}".format( country.Population)
            s += "\t{:.2f}%".format( country.Population * 100 / self.TotalPopulation)
            s += "\t{:.0f}".format( country.Territory)
            s += "\t{:.2f}%".format( country.Territory * 100 / self.TotalLandMass)
            print(s)
            s += "\r\n"
            f.write(s.encode("UTF-8"))
            combined.Population += country.Population
            combined.Territory += country.Territory
            combined.GDP += country.GDP * country.Population
            combined.GDP_PPP += country.GDP_PPP * country.Population
            combined.Total += np.clip( country.Total, 0.0, None)
            combined.CNOL += np.clip( country.CNOL, 0.0, None)
            combined.Crude += np.clip( country.Crude, 0.0, None)
            combined.NGPL += np.clip( country.NGPL, 0.0, None)
            combined.Other += np.clip( country.Other, 0.0, None)
            combined.ProcessingGain = np.clip( country.ProcessingGain, 0.0, None)
            count += 1
        combined.GDP /=  combined.Population 
        combined.GDP_PPP /=  combined.Population 
        self.Countries[ combined.Code] = combined
        s = "\tВсего крупные производители:"
        s += "\t{:s}".format(combined.Peak_Year)
        s += "\t{:.2f}".format(combined.Peak_Production)
        s += "\t{:.2f}".format( combined.Production_2020)
        s += "\t{:.2f}%".format( combined.Production_2020*100/combined.Peak_Production)
        s += "\t{:.1f}".format( combined.Population)
        s += "\t{:.2f}%".format( combined.Population * 100 / self.TotalPopulation)
        s += "\t{:.0f}".format( combined.Territory)
        s += "\t{:.2f}%".format( combined.Territory * 100 / self.TotalLandMass)
        print(s)
        s += "\r\n"
        f.write(s.encode("UTF-8"))
        f.close()
        combined.Plot( self.Years, foldername )
        combined.SaveCrude( "./Data/Crude_Top_Producers.csv", self.Years)
        print("Top Producers GDP = ${:.0f} per capita".format( combined.GDP))
        print("Top Producers GDP PPP = ${:.0f} per capita".format( combined.GDP_PPP))
        print("{:d} top producers processed".format(count))
        return
        
    def processGroupPlot(self, foldername):
        Year,Groups12,Group3,TopProducers,BP_Total = Load_Calibration("./Data/Groups_123_Estimates.csv",
            ["Year","Groups12", "Group3","TopProducers","BP_Total"], separator="\t")
        fig = plt.figure( figsize=(15,10))
        fig.suptitle( 'Добыча нефти и лицензионного конденсата по группам', fontsize=22)
        gs = plt.GridSpec(1, 1, height_ratios=[1]) 
        ax1 = plt.subplot(gs[0])
        ax1.bar( Year, Groups12, width=0.75, color="b", alpha=0.1, label='Группы 1 и 2 (пик до 2011 г)')
        ax1.bar( Year, Group3, bottom=Groups12, width=0.75, color="g", alpha=0.1, label='Группa 3 (пик после 2010 г либо не пройден)')
        ax1.plot( Year, TopProducers, "-", lw=2, color="r", label='20 стран с добычей более 1% от мировой 2018 г')
        ax1.plot( Year, BP_Total, "-", lw=2, color="k", label='Добыча всех "жидкостей" по данным "БП"')
        ax1.set_xlabel('Год')
        ax1.set_ylabel('млн тонн в год')    
        ax1.set_xlim( 1964, 2024)
        ax1.text( 1990, 500, "Площадь 87.8 млн км²")
        ax1.text( 1990, 2000, "Площадь 62.7 млн км²")
        ax1.text( 1967, 100, "Чёрная нефть и лицензионный конденсат", fontsize=12)
        ax1.grid(True)
        ax1.legend(loc=2)
        plt.savefig( foldername + "99_01_Group_Plot.png")
        plt.close('all')
        return
    def processRegion(self, foldername, regname):
        count = 0
        f = open( foldername + "_Report_" + regname + ".txt", "wb")
        processing_order = []
        for code in self.Countries:
            country = self.Countries[code]
            print(country.Code, country.Region, regname)
            if country.Region != regname: continue
            print( code)
            processing_order += [ country]
        processing_order.sort( key=lambda x: x.Order)
        combined = EIA_Country( "GRP"+regname)
        combined.applyMetadata( self.Metadata)
        l = len( self.Years)
        combined.Total = np.zeros(l)
        combined.CNOL = np.zeros(l)
        combined.Crude = np.zeros(l)
        combined.NGPL = np.zeros(l)
        combined.Other = np.zeros(l)
        combined.ProcessingGain = np.zeros(l)
        combined.Population = 0.0
        combined.Territory = 0.0
        combined.GDP = 0.0
        combined.GDP_PPP = 0.0
        for country in processing_order:
            #country.Plot( self.Years, foldername )
            s = "{:s}\t{:s}".format( country.Code, country.RussianName)
            s += "\t" + country.Peak_Year
            s += "\t{:.2f}".format( country.Peak_Production)
            s += "\t{:.2f}".format( country.Production_2020)
            s += "\t{:.2f}%".format( country.Production_2020*100/country.Peak_Production)
            s += "\t{:.1f}".format( country.Population)
            s += "\t{:.2f}%".format( country.Population * 100 / self.TotalPopulation)
            s += "\t{:.0f}".format( country.Territory)
            s += "\t{:.2f}%".format( country.Territory * 100 / self.TotalLandMass)
            print(s)
            s += "\r\n"
            f.write(s.encode("UTF-8"))
            combined.Population += country.Population
            combined.Territory += country.Territory
            combined.GDP += country.GDP * country.Population
            combined.GDP_PPP += country.GDP_PPP * country.Population
            combined.Total += np.clip( country.Total, 0.0, None)
            combined.CNOL += np.clip( country.CNOL, 0.0, None)
            combined.Crude += np.clip( country.Crude, 0.0, None)
            combined.NGPL += np.clip( country.NGPL, 0.0, None)
            combined.Other += np.clip( country.Other, 0.0, None)
            combined.ProcessingGain = np.clip( country.ProcessingGain, 0.0, None)
            count += 1
        combined.GDP /=  combined.Population 
        combined.GDP_PPP /=  combined.Population 
        self.Countries[ combined.Code] = combined
        s = "\tВсего {:s}:".format(combined.Name)
        s += "\t{:s}".format(combined.Peak_Year)
        s += "\t{:.2f}".format(combined.Peak_Production)
        s += "\t{:.2f}".format( combined.Production_2020)
        s += "\t{:.2f}%".format( combined.Production_2020*100/combined.Peak_Production)
        s += "\t{:.1f}".format( combined.Population)
        s += "\t{:.2f}%".format( combined.Population * 100 / self.TotalPopulation)
        s += "\t{:.0f}".format( combined.Territory)
        s += "\t{:.2f}%".format( combined.Territory * 100 / self.TotalLandMass)
        print(s)
        s += "\r\n"
        f.write(s.encode("UTF-8"))
        f.close()
        combined.Plot( self.Years, foldername )
        combined.SaveCrude( "./Data/Crude_Top_Producers.csv", self.Years)
        print("{:s} GDP = ${:.0f} per capita".format( combined.Name, combined.GDP))
        print("{:s} GDP PPP = ${:.0f} per capita".format( combined.Name, combined.GDP_PPP))
        print("{:s} max production = {:.2f} in {:.0f}".format(
            combined.Name, max(combined.Crude)*0.365*0.159*0.875, np.argmax(combined.Crude)+1973))
        print("{:d} countries in {:s} processed".format(count, combined.Name))
        return

#data_2019 = EIA_Countries("./Data/Oil_and_Lease_Condensate_Production_2019.csv")
#data_2020 = EIA_Countries("./Data/Oil_and_Lease_Condensate_Production_2020.csv")
data_2021 = EIA_Countries("./Data/Oil_and_Lease_Condensate_Production_2021.csv")
data_2021.loadHistorical( "./Data/EIA_Comparison_2015.csv")
data_2021.processDeprecated( "./Deprecated/")
data_2021.processSmallTerritories( "./Small_Territories/")
data_2021.processGroup1( "./Group_1/")
data_2021.processGroup2( "./Group_2/")
data_2021.processGroup3( "./Group_3/")
data_2021.processTopProducers( "./Top_Producers/", 38.5)
data_2021.processGroupPlot( "./Graphs/")
data_2021.processRegion( "./Graphs/", "AFR")
data_2021.processRegion( "./Graphs/", "NAM")
data_2021.processRegion( "./Graphs/", "SAM")
data_2021.processRegion( "./Graphs/", "EUR")
data_2021.processRegion( "./Graphs/", "CIS")
data_2021.processRegion( "./Graphs/", "MEA")
data_2021.processRegion( "./Graphs/", "ASA")
data_2021.processRegion( "./Graphs/", "CHI")
data_2021.processRegion( "./Graphs/", "IND")
print("Processing completed")
