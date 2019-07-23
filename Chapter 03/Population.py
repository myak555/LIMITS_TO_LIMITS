from Utilities import *

class Population:
    """
    Describes population (as a Malthus-Velhurst equation solution AKA Shark Fin)
    Peak_Year - peak population year
    Peak_Value - peak population value
    L_Slope - left slope
    R_Slope - right slope
    Additionaly creates three approximate UN solutions using linear combinations of Sigmoid and Hubbert functions 
    """
    def __init__( self, Peak_Year=2057, Peak_Value=8000, L_Slope=0.028, R_Slope=0.080):
        self._Model0 = Linear_Combo()
        self._Model0.Wavelets += [Bathtub( -650,0.0025,2200,0.004,30,260,4250)]
        self._Model0.Wavelets += [Hubbert( Peak_Year, L_Slope, R_Slope, Peak_Value)]
        self._Model0.Wavelets += [Hubbert( 1950, 0.2, 0.2, -250)]
        self._Model0.Wavelets += [Hubbert( 2000, 0.1, 0.2, 150)]
        self._Model0.Wavelets += [Hubbert( 1970, 0.3, 0.3, -50)]
        self._Model0.Wavelets += [Hubbert( 1870, 0.1, 0.05, 120)]
        self._Model0.Wavelets += [Hubbert( 1930, 0.2, 0.2, -50)]
        self.Name = "PyWorld 2017"
        self.Calibration_Year, self.Calibration_Total, self.Calibration_Yerr = Load_Calibration(
            "../Global Data/Population_Calibration.csv", ["Year", "Population", "Yerror"])
        self.UN_Low = Linear_Combo()
        self.UN_Low.Name = "UN Low Case"
        self.UN_Low.Wavelets += [ Sigmoid( x0=2002.0, s0=0.03300, left=980.000, right=11600.000, shift=0.000)]
        self.UN_Low.Wavelets += [ Hubbert( x0=1855.5, s0=0.07523, s1=0.10878, peak=182.819, shift=0.000)]
        self.UN_Low.Wavelets += [ Hubbert( x0=1903.0, s0=0.06400, s1=0.06400, peak=353.000, shift=0.000)]
        self.UN_Low.Wavelets += [ Hubbert( x0=1951.0, s0=0.17975, s1=0.21109, peak=-118.000, shift=0.000)]
        self.UN_Low.Wavelets += [ Hubbert( x0=1964.0, s0=0.30994, s1=0.34868, peak=-69.500, shift=0.000)]
        self.UN_Low.Wavelets += [ Hubbert( x0=1992.0, s0=0.30994, s1=0.31987, peak=79.000, shift=0.000)]
        self.UN_Low.Wavelets += [ Hubbert( x0=2010.0, s0=0.36475, s1=0.13208, peak=-32.500, shift=0.000)]
        self.UN_Low.Wavelets += [ Hubbert( x0=2037.8, s0=0.16307, s1=0.10332, peak=-31.025, shift=0.000)]
        self.UN_Low.Wavelets += [ Sigmoid( x0=2085.0, s0=0.04452, left=0.000, right=-6116.317, shift=0.000)]
        self.UN_Low.Wavelets += [ Hubbert( x0=2017.0, s0=0.16677, s1=0.20335, peak=155.000, shift=0.000)]
        self.UN_Low.Wavelets += [ Hubbert( x0=2062.0, s0=0.11881, s1=0.12884, peak=-128.000, shift=0.000)]
        self.UN_Medium = Linear_Combo()
        self.UN_Medium.Name = "UN Medium Case"
        self.UN_Medium.Wavelets += [ Sigmoid( x0=2002.0, s0=0.03300, left=980.000, right=11600.000, shift=0.000)]
        self.UN_Medium.Wavelets += [ Hubbert( x0=1855.5, s0=0.07523, s1=0.10878, peak=182.819, shift=0.000)]
        self.UN_Medium.Wavelets += [ Hubbert( x0=1903.0, s0=0.06400, s1=0.06400, peak=353.000, shift=0.000)]
        self.UN_Medium.Wavelets += [ Hubbert( x0=1951.0, s0=0.17975, s1=0.21109, peak=-118.000, shift=0.000)]
        self.UN_Medium.Wavelets += [ Hubbert( x0=1964.0, s0=0.30994, s1=0.34868, peak=-69.500, shift=0.000)]
        self.UN_Medium.Wavelets += [ Hubbert( x0=1992.0, s0=0.30994, s1=0.31987, peak=79.000, shift=0.000)]
        self.UN_Medium.Wavelets += [ Hubbert( x0=2010.0, s0=0.36475, s1=0.13208, peak=-32.500, shift=0.000)]
        self.UN_Medium.Wavelets += [ Hubbert( x0=2037.8, s0=0.16307, s1=0.10332, peak=-31.025, shift=0.000)]
        self.UN_High = Linear_Combo()
        self.UN_High.Name = "UN High Case"
        self.UN_High.Wavelets += [ Sigmoid( x0=2002.000, s0=0.03300, left=980.000, right=11600.000, shift=0.000)]
        self.UN_High.Wavelets += [ Hubbert( x0=1855.500, s0=0.07523, s1=0.10878, peak=182.819, shift=0.000)]
        self.UN_High.Wavelets += [ Hubbert( x0=1903.000, s0=0.06400, s1=0.06400, peak=353.000, shift=0.000)]
        self.UN_High.Wavelets += [ Hubbert( x0=1951.000, s0=0.17975, s1=0.21109, peak=-118.000, shift=0.000)]
        self.UN_High.Wavelets += [ Hubbert( x0=1964.000, s0=0.30994, s1=0.34868, peak=-69.500, shift=0.000)]
        self.UN_High.Wavelets += [ Hubbert( x0=1992.000, s0=0.30994, s1=0.31987, peak=79.000, shift=0.000)]
        self.UN_High.Wavelets += [ Hubbert( x0=2010.000, s0=0.36475, s1=0.13208, peak=-32.500, shift=0.000)]
        self.UN_High.Wavelets += [ Hubbert( x0=2037.800, s0=0.16307, s1=0.10332, peak=-31.025, shift=0.000)]
        self.UN_High.Wavelets += [ Sigmoid( x0=2085.000, s0=0.05121, left=0.000, right=8218.938, shift=0.000)]
        self.UN_High.Wavelets += [ Hubbert( x0=2017.000, s0=0.22877, s1=0.27615, peak=-116.000, shift=0.000)]
        self.UN_High.Wavelets += [ Hubbert( x0=2056.000, s0=0.13014, s1=0.20680, peak=80.975, shift=0.000)]
        self.UN_High.Wavelets += [ Hubbert( x0=2088.000, s0=0.14967, s1=0.20132, peak=-171.671, shift=0.000)]
        self.Velhurst_Analytical = Sigmoid( 1997, 0.0370, 1390, 10500)
        self.Velhurst_Analytical.Name = "Velhurst Analytical"
        self.Kapitsa_Analytical = KapitsaIntegral( 2003, 176e3, 44)
        self.Kapitsa_Analytical.Name = "Kapitsa Analytical"
        return
    def LoadHistorical(self):
        """
        Loads historical data from file ../Global Data/Earth_Historical.csv
        """
        self.Historical_Year, self.Historical_Total, self.Historical_Yerr = Load_Calibration(
            "../Global Data/Earth_Historical.csv", ["Year", "Population", "Yerror"])
    def Solve( self, t0):
        """
        Creates the solution vector
        """
        self.Solution_Year = t0
        self.Solution_Total = self._Model0.GetVector( t0)
        self.Solution_UN_Low = self.UN_Low.GetVector( t0)
        self.Solution_UN_Medium = self.UN_Medium.GetVector( t0)
        self.Solution_UN_High = self.UN_High.GetVector( t0)
        return self.Solution_Total
    def Compute( self, t):
        """
        Computes the approximation
        """
        tmp = self._Model0.Compute( t)
        return tmp

class Country_Dictionary:
    def __init__(self):
        self.__dict_EngRus = {
            "AFRICA": "АФРИКА",
            "ASIA": "АЗИЯ",
            "Afghanistan": "Афганистан",
            "Albania": "Албания",
            "Algeria": "Алжир",
            "American Samoa": "Американское Самоа",
            "Andorra": "Андорра",
            "Angola": "Ангола",
            "Anguilla": "Ангилья",
            "Antarctica": "Антарктида",
            "Antigua and Barbuda": "Антигуа и Барбуда",
            "Argentina": "Аргентина",
            "Armenia": "Армения",
            "Aruba": "Аруба",
            "Australia": "Австралия",
            "Australia/New Zealand": "Австралия/Новая Зеландия",
            "Austria": "Австрия",
            "Azerbaijan": "Азербайджан",
            "Bahamas": "Багамские о-ва",
            "Bahrain": "Бахрейн",
            "Bangladesh": "Бангладеш",
            "Barbados": "Барбадос",
            "Belarus": "Беларусь",
            "Belgium": "Бельгия",
            "Belize": "Белиз",
            "Benin": "Бенин",
            "Bermuda": "Бермудские о-ва",
            "Bhutan": "Бутан",
            "Bolivia (Plurinational State of)": "Боливия",
            "Bosnia and Herzegovina": "Босния и Герцеговина",
            "Botswana": "Ботсвана",
            "Brazil": "Бразилия",
            "British Virgin Islands": "Британские Виргинские о-ва",
            "Brunei Darussalam": "Бруней-Даруссалам",
            "Bulgaria": "Болгария",
            "Burkina Faso": "Буркина-Фасо",
            "Burundi": "Бурунди",
            "Cabo Verde": "Кабо Верде",
            "Cambodia": "Камбоджа",
            "Cameroon": "Камерун",
            "Canada": "Канада",
            "Caribbean": "страны Карибского бассейна",
            "Caribbean Netherlands": "Карибские о-ва Нидерландов",
            "Cayman Islands": "Каймановы о-ва",
            "Central African Republic": "Центрально-Африканская Республика",
            "Central America": "Центральная Америка",
            "Central Asia": "Центральная Азия",
            "Chad": "Чад",
            "Channel Islands": "Нормандские о-ва",
            "Chile": "Чили",
            "China": "КНР",
            "China, Hong Kong SAR": "КНР, САР Гонконг",
            "China, Macao SAR": "КНР, Макао",
            "China, Taiwan Province of China": "Тайвань (как провинция КНР)",
            "Colombia": "Колумбия",
            "Comoros": "Коморские о-ва",
            "Congo": "Конго",
            "Cook Islands": "о-ва Кука",
            "Costa Rica": "Коста Рика",
            "Cote d'Ivoire": "Берег Слоновой Кости",
            "Croatia": "Хорватия",
            "Cuba": "Куба",
            "Curacao": "Кюрасао",
            "Cyprus": "Кипр",
            "Czechia": "Чехия",
            "Dem. People's Republic of Korea": "КНДР",
            "Democratic Republic of the Congo": "Демократическая Республика Конго",
            "Denmark": "Дания",
            "Djibouti": "Джибути",
            "Dominica": "Доминика",
            "Dominican Republic": "Доминиканская Республика",
            "EUROPE": "ЕВРОПА",
            "Eastern Africa": "Восточная Африка",
            "Eastern Asia": "Восточная Азия",
            "Eastern Europe": "Восточная Европа",
            "Ecuador": "Эквадор",
            "Egypt": "Египет",
            "El Salvador": "Эль Сальвадор",
            "Equatorial Guinea": "Экваториальная Гвинея",
            "Eritrea": "Эритрея",
            "Estonia": "Эстония",
            "Ethiopia": "Эфиопия",
            "Faeroe Islands": "Фарерские о-ва",
            "Falkland Islands (Malvinas)": "Фолклендские (Мальвинские) о-ва",
            "Fiji": "Фиджи",
            "Finland": "Финляндия",
            "France": "Франция",
            "French Guiana": "Французская Гвиана",
            "French Polynesia": "Французская Полинезия",
            "GPA_Africa": "GPA_Africa",
            "GPA_China": "GPA_China",
            "GPA_Eiropean_Union": "GPA_Eiropean_Union",
            "GPA_Europe": "GPA_Europe",
            "GPA_Former_CIS": "GPA_Former_CIS",
            "GPA_G20": "GPA_G20",
            "GPA_G4": "GPA_G4",
            "GPA_G7": "GPA_G7",
            "GPA_Indostan": "GPA_Indostan",
            "GPA_Middle_East": "GPA_Middle_East",
            "GPA_North_America": "GPA_North_America",
            "GPA_OECD": "GPA_OECD",
            "GPA_OPEC": "GPA_OPEC",
            "GPA_Other_Asia_Oceania": "GPA_Other_Asia_Oceania",
            "GPA_Permanent5": "GPA_Permanent5",
            "GPA_South_America": "GPA_South_America",
            "Gabon": "Габон",
            "Gambia": "Гамбия",
            "Georgia": "Грузия",
            "Germany": "Германия",
            "Ghana": "Гана",
            "Gibraltar": "Гибралтар",
            "Greece": "Греция",
            "Greenland": "Гренландия",
            "Grenada": "Гренада",
            "Guadeloupe": "Гваделупа",
            "Guam": "Гуам",
            "Guatemala": "Гватемала",
            "Guinea": "Гвинея",
            "Guinea-Bissau": "Гвинея-Бисау",
            "Guyana": "Гайана",
            "Haiti": "Гаити",
            "High-income countries": "Страны с высоким уровнем дохода",
            "Holy See": "Ватикан",
            "Honduras": "Гондурас",
            "Hungary": "Венгрия",
            "Iceland": "Исландия",
            "India": "Индия",
            "Indonesia": "Индонезия",
            "Iran (Islamic Republic of)": "Иран (Исламская Республика)",
            "Iraq": "Ирак",
            "Ireland": "Ирландия",
            "Isle of Man": "Остров Мэн",
            "Israel": "Израиль",
            "Italy": "Италия",
            "Jamaica": "Ямайка",
            "Japan": "Япония",
            "Jordan": "Иордания",
            "Kazakhstan": "Казахстан",
            "Kenya": "Кения",
            "Kiribati": "Кирибати",
            "Kuwait": "Кувейт",
            "Kyrgyzstan": "Кыргызстан",
            "LATIN AMERICA AND THE CARIBBEAN": "ЛАТИНСКАЯ АМЕРИКА И КАРИБСКИЙ БАССЕЙН",
            "Lao People's Democratic Republic": "Лаосская Народно-Демократическая Республика",
            "Latvia": "Латвия",
            "Least developed countries": "Беднейшие страны",
            "Lebanon": "Ливан",
            "Lesotho": "Лесото",
            "Less developed regions": "Менее развитые регионы",
            "Less developed regions, excluding China": "Менее развитые регионы, кроме Китая",
            "Less developed regions, excluding least developed countries": "Менее развитые регионы, исключая беднейшие страны",
            "Liberia": "Либерия",
            "Libya": "Ливия",
            "Liechtenstein": "Лихтенштейн",
            "Lithuania": "Литва",
            "Low-income countries": "Страны с низким уровнем дохода",
            "Lower-middle-income countries": "Страны с доходом ниже среднего",
            "Luxembourg": "Люксембург",
            "Madagascar": "Мадагаскар",
            "Malawi": "Малави",
            "Malaysia": "Малайзия",
            "Maldives": "Мальдивы",
            "Mali": "Мали",
            "Malta": "Мальта",
            "Marshall Islands": "Маршалловы о-ва",
            "Martinique": "Мартиника",
            "Mauritania": "Мавритания",
            "Mauritius": "Маврикий",
            "Mayotte": "Майотта",
            "Melanesia": "Меланезия",
            "Mexico": "Мексика",
            "Micronesia": "Микронезия",
            "Micronesia (Fed. States of)": "Микронезия (Федеративные Штаты)",
            "Middle Africa": "Средняя Африка",
            "Middle-income countries": "Страны со средним уровнем дохода",
            "Monaco": "Монако",
            "Mongolia": "Монголия",
            "Montenegro": "Черногория",
            "Montserrat": "Монсеррат",
            "More developed regions": "Более развитые регионы",
            "Morocco": "Марокко",
            "Mozambique": "Мозамбик",
            "Myanmar": "Мьянма (Бирма)",
            "NORTHERN AMERICA": "СЕВЕРНАЯ АМЕРИКА",
            "Namibia": "Намибия",
            "Nauru": "Науру",
            "Nepal": "Непал",
            "Netherlands": "Нидерланды",
            "New Caledonia": "Новая Каледония",
            "New Zealand": "Новая Зеландия",
            "Nicaragua": "Никарагуа",
            "Niger": "Нигер",
            "Nigeria": "Нигерия",
            "Niue": "О-в Ниуэ",
            "Northern Africa": "Северная Африка",
            "Northern Europe": "Северная Европа",
            "Northern Mariana Islands": "Северные Марианские о-ва",
            "Norway": "Норвегия",
            "OCEANIA": "ОКЕАНИЯ",
            "Oman": "Оман",
            "Pakistan": "Пакистан",
            "Palau": "Палау",
            "Panama": "Панама",
            "Papua New Guinea": "Папуа - Новая Гвинея",
            "Paraguay": "Парагвай",
            "Peru": "Перу",
            "Philippines": "Филиппины",
            "Poland": "Польша",
            "Polynesia": "Полинезия",
            "Portugal": "Португалия",
            "Puerto Rico": "Пуэрто-Рико",
            "Qatar": "Катар",
            "Republic of Korea": "Южная Корея",
            "Republic of Moldova": "Молдова",
            "Reunion": "О-в Реюньон",
            "Romania": "Румыния",
            "Russian Federation": "Российская Федерация",
            "Rwanda": "Руанда",
            "Saint Helena": "О-в Святой Елены",
            "Saint Kitts and Nevis": "Сент-Китс и Невис",
            "Saint Lucia": "Санкт-Люсия",
            "Saint Pierre and Miquelon": "Сен-Пьер и Микелон",
            "Saint Vincent and the Grenadines": "Св.Винсент и Гренадины",
            "Samoa": "Самоа",
            "San Marino": "Сан-Марино",
            "Sao Tome and Principe": "Сан-Томе и Принсипи",
            "Saudi Arabia": "Саудовская Аравия",
            "Senegal": "Сенегал",
            "Serbia": "Сербия",
            "Seychelles": "Сейшельские о-ва",
            "Sierra Leone": "Сьерра-Леоне",
            "Singapore": "Сингапур",
            "Sint Maarten (Dutch part)": "Синт-Мартен (голландская часть)",
            "Slovakia": "Словакия",
            "Slovenia": "Словения",
            "Solomon Islands": "Соломоновы о-ва",
            "Somalia": "Сомали",
            "South Africa": "ЮАР",
            "South America": "Южная Америка",
            "South Sudan": "Южный Судан",
            "South-Central Asia": "Южная и Центральная Азия",
            "South-Eastern Asia": "Юго-Восточная Азия",
            "Southern Africa": "Южная Африка",
            "Southern Asia": "Южная Азия",
            "Southern Europe": "Южная Европа",
            "Spain": "Испания",
            "Sri Lanka": "Шри-Ланка",
            "State of Palestine": "Палестинские территории",
            "Sub-Saharan Africa": "Южная Сахара",
            "Sudan": "Судан",
            "Suriname": "Суринам",
            "Swaziland": "Свазиленд",
            "Sweden": "Швеция",
            "Switzerland": "Швейцария",
            "Syrian Arab Republic": "Сирийская Арабская Республика",
            "TFYR Macedonia": "Македония",
            "Tajikistan": "Таджикистан",
            "Thailand": "Таиланд",
            "Timor-Leste": "Восточный Тимор",
            "Togo": "Того",
            "Tokelau": "Токелау",
            "Tonga": "Тонга",
            "Trinidad and Tobago": "Тринидад и Тобаго",
            "Tunisia": "Тунис",
            "Turkey": "Турция",
            "Turkmenistan": "Туркменистан",
            "Turks and Caicos Islands": "о-ва Теркс и Кайкос",
            "Tuvalu": "Тувалу",
            "Uganda": "Уганда",
            "Ukraine": "Украина",
            "United Arab Emirates": "ОАЭ",
            "United Kingdom": "Великобритания",
            "United Republic of Tanzania": "Танзания",
            "United States Virgin Islands": "Американские Виргинские о-ва",
            "United States of America": "США",
            "Upper-middle-income countries": "Страны с уровнем дохода выше среднего",
            "Uruguay": "Уругвай",
            "Uzbekistan": "Узбекистан",
            "Vanuatu": "Вануату",
            "Venezuela (Bolivarian Republic of)": "Венесуэла",
            "Viet Nam": "Вьетнам",
            "WORLD": "МИР",
            "Wallis and Futuna Islands": "О-ва Уоллис и Футуна",
            "Western Africa": "Западная Африка",
            "Western Asia": "Западная Азия",
            "Western Europe": "западная Европа",
            "Western Sahara": "Западная Сахара",
            "Yemen": "Йемен",
            "Zambia": "Замбия",
            "Zimbabwe": "Зимбабве",
            "Minor islands and territories*": "Малые острова и территории*",
            "Former Czechoslovakia": "Бывшая Чехославакия",
            "Former Serbia and Montenegro": "Бывшая Сербия и Черногория",
            "Former U.S.S.R.": "Бывший СССР",
            "Former Yugoslavia": "Бывшая Югославия",
            "Germany (Offshore)": "Германия (морские)",
            "Germany, East": "Бывшая ГДР",
            "Germany, West": "Бывшая ФРГ",
            "Hawaiian Trade Zone": "Бывшая Гавайская торговая зона",
            "Kosovo": "Косово",
            "Netherlands (Offshore)": "Нидерланды (морские)",
            "United Kingdom (Offshore)": "Великобритания (морские)",
            "Sudan and South Sudan": "Судан и Южный Судан",
            "US Pacific Islands": "Тихоокеанские о-ва США",
            "North Cyprus": "Кипр (северный)",
            "Somaliland": "Сомалиленд",
            "French ocean territories": "Французские океанические владения"}
        self.__set_LowAccuracy = [
            "WORLD",
            "Less developed regions",
            "Least developed countries",
            "Less developed regions, excluding least developed countries",
            "Less developed regions, excluding China",
            "Low-income countries",
            "Sub-Saharan Africa",
            "AFRICA",
            "Eastern Africa",
            "Burundi",
            "Comoros",
            "Djibouti",
            "Eritrea",
            "Ethiopia",
            "Kenya",
            "Madagascar",
            "Malawi",
            "Mauritius",
            "Mayotte",
            "Mozambique",
            "Rwanda",
            "Seychelles",
            "Somalia",
            "South Sudan",
            "Uganda",
            "United Republic of Tanzania",
            "Zambia",
            "Zimbabwe",
            "Middle Africa",
            "Angola",
            "Cameroon",
            "Central African Republic",
            "Chad",
            "Congo",
            "Democratic Republic of the Congo",
            "Equatorial Guinea",
            "Gabon",
            "Sao Tome and Principe",
            "Northern Africa",
            "Algeria",
            "Egypt",
            "Libya",
            "Morocco",
            "Sudan",
            "Tunisia",
            "Western Sahara",
            "Southern Africa",
            "Botswana",
            "Lesotho",
            "Namibia",
            "South Africa",
            "Swaziland",
            "Western Africa",
            "Benin",
            "Burkina Faso",
            "Cabo Verde",
            "Cote d'Ivoire",
            "Gambia",
            "Ghana",
            "Guinea",
            "Guinea-Bissau",
            "Liberia",
            "Mali",
            "Mauritania",
            "Niger",
            "Nigeria",
            "Saint Helena",
            "Senegal",
            "Sierra Leone",
            "Togo",
            "ASIA",
            "Eastern Asia",
            "Mongolia",
            "South-Central Asia",
            "Central Asia",
            "Kyrgyzstan",
            "Tajikistan",
            "Turkmenistan",
            "Uzbekistan",
            "Southern Asia",
            "Afghanistan",
            "Bangladesh",
            "Bhutan",
            "India",
            "Iran (Islamic Republic of)",
            "Nepal",
            "Pakistan",
            "Sri Lanka",
            "South-Eastern Asia",
            "Cambodia",
            "Indonesia",
            "Lao People's Democratic Republic",
            "Myanmar",
            "Philippines",
            "Timor-Leste",
            "Western Asia",
            "Iraq",
            "Jordan",
            "Lebanon",
            "State of Palestine",
            "Syrian Arab Republic",
            "Yemen",
            "LATIN AMERICA AND THE CARIBBEAN",
            "Haiti",
            "GPA_Africa",
            "GPA_Former_CIS",
            "GPA_Indostan",
            "GPA_Other_Asia",
            "GPA_Middle_East",
            "GPA_South_America"]
        self.__gpa_Africa = [
            "Burundi",
            "Comoros",
            "Djibouti",
            "Eritrea",
            "Ethiopia",
            "Kenya",
            "Madagascar",
            "Malawi",
            "Mauritius",
            "Mayotte",
            "Mozambique",
            "Reunion",
            "Rwanda",
            "Seychelles",
            "Somalia",
            "South Sudan",
            "Uganda",
            "United Republic of Tanzania",
            "Zambia",
            "Zimbabwe",
            "Angola",
            "Cameroon",
            "Central African Republic",
            "Chad",
            "Congo",
            "Democratic Republic of the Congo",
            "Equatorial Guinea",
            "Gabon",
            "Sao Tome and Principe",
            "Algeria",
            "Egypt",
            "Libya",
            "Morocco",
            "Sudan",
            "Tunisia",
            "Western Sahara",
            "Botswana",
            "Lesotho",
            "Namibia",
            "South Africa",
            "Swaziland",
            "Benin",
            "Burkina Faso",
            "Cabo Verde",
            "Cote d'Ivoire",
            "Gambia",
            "Ghana",
            "Guinea",
            "Guinea-Bissau",
            "Liberia",
            "Mali",
            "Mauritania",
            "Niger",
            "Nigeria",
            "Saint Helena",
            "Senegal",
            "Sierra Leone",
            "Togo"]
        self.__gpa_China = [
            "China",
            "China, Hong Kong SAR",
            "China, Macao SAR",
            "China, Taiwan Province of China",
            "Mongolia",
            "Nepal"]
        self.__gpa_Former_CIS = [
            "Armenia",
            "Azerbaijan",
            "Georgia",
            "Kazakhstan",
            "Kyrgyzstan",
            "Tajikistan",
            "Turkmenistan",
            "Uzbekistan",
            "Belarus",
            "Republic of Moldova",
            "Russian Federation",
            "Ukraine",
            "Estonia",
            "Latvia",
            "Lithuania"]
        self.__gpa_Other_Europe = [
            "Turkey",
            "Channel Islands",
            "Faeroe Islands",
            "Iceland",
            "Isle of Man",
            "Norway",
            "United Kingdom",
            "Albania",
            "Andorra",
            "Bosnia and Herzegovina",
            "Gibraltar",
            "Holy See",
            "Montenegro",
            "San Marino",
            "Serbia",
            "TFYR Macedonia",
            "Liechtenstein",
            "Monaco",
            "Switzerland"]
        self.__gpa_Indostan = [
            "Bangladesh",
            "India",
            "Maldives",
            "Pakistan",
            "Sri Lanka"]
        self.__gpa_Other_Asia = [
            "Dem. People's Republic of Korea",
            "Japan",
            "Republic of Korea",
            "Afghanistan",
            "Bhutan",
            "Brunei Darussalam",
            "Cambodia",
            "Indonesia",
            "Lao People's Democratic Republic",
            "Malaysia",
            "Myanmar",
            "Philippines",
            "Singapore",
            "Thailand",
            "Timor-Leste",
            "Viet Nam",
            "American Samoa",
            "Australia",
            "Cook Islands",
            "Fiji",
            "French Polynesia",
            "Guam",
            "Kiribati",
            "Marshall Islands",
            "Micronesia (Fed. States of)",
            "Nauru",
            "New Caledonia",
            "New Zealand",
            "Niue",
            "Northern Mariana Islands",
            "Palau",
            "Papua New Guinea",
            "Samoa",
            "Solomon Islands",
            "Tokelau",
            "Tonga",
            "Tuvalu",
            "Vanuatu",
            "Wallis and Futuna Islands"]
        self.__gpa_Middle_East = [
            "Bahrain",
            "Iran (Islamic Republic of)",
            "Iraq",
            "Israel",
            "Jordan",
            "Kuwait",
            "Lebanon",
            "Oman",
            "State of Palestine",
            "Qatar",
            "Saudi Arabia",
            "Syrian Arab Republic",
            "United Arab Emirates",
            "Yemen"]
        self.__gpa_South_America = [
            "Dominica",
            "Dominican Republic",
            "Grenada",
            "Guadeloupe",
            "Haiti",
            "Jamaica",
            "Martinique",
            "Montserrat",
            "Puerto Rico",
            "Saint Kitts and Nevis",
            "Saint Lucia",
            "Saint Vincent and the Grenadines",
            "Sint Maarten (Dutch part)",
            "Trinidad and Tobago",
            "Turks and Caicos Islands",
            "Belize",
            "El Salvador",
            "Costa Rica",
            "Guatemala",
            "Honduras",
            "Nicaragua",
            "Panama",
            "Argentina",
            "Bolivia (Plurinational State of)",
            "Brazil",
            "Chile",
            "Colombia",
            "Ecuador",
            "Falkland Islands (Malvinas)",
            "French Guiana",
            "Guyana",
            "Paraguay",
            "Peru",
            "Suriname",
            "Uruguay",
            "Venezuela (Bolivarian Republic of)",
            "Anguilla",
            "Antigua and Barbuda",
            "Aruba",
            "Bahamas",
            "Barbados",
            "British Virgin Islands",
            "Caribbean Netherlands",
            "Cayman Islands",
            "Cuba",
            "Curacao"]
        self.__gpa_North_America = [
            "Bermuda",
            "Canada",
            "Greenland",
            "Saint Pierre and Miquelon",
            "United States of America",
            "United States Virgin Islands",
            "Mexico"]
        self.__gpa_P5 = [
            "China",
            "China, Hong Kong SAR",
            "China, Macao SAR",
            "France",
            "Russia",
            "United Kingdom",
            "United States of America"]
        self.__gpa_OPEC = [
            "Algeria",
            "Angola",
            "Ecuador",
            "Equatorial Guinea",
            "Gabon",
            "Iran",
            "Iraq",
            "Kuwait",
            "Libya",
            "Nigeria",
            "Republic of the Congo",
            "Saudi Arabia",
            "United Arab Emirates",
            "Venezuela"]
        self.__gpa_OECD = [
            "Australia",
            "Austria",
            "Belgium",
            "Canada",
            "Chile",
            "Czechia",
            "Denmark",
            "Estonia",
            "Finland",
            "France",
            "Germany",
            "Greece",
            "Hungary",
            "Iceland",
            "Ireland",
            "Israel",
            "Italy",
            "Japan",
            "Latvia",
            "Lithuania",
            "Luxembourg",
            "Mexico",
            "Netherlands",
            "NewZealand",
            "Norway",
            "Poland",
            "Portugal",
            "Republic of Korea",
            "Slovakia",
            "Slovenia",
            "Spain",
            "Sweden",
            "Switzerland",
            "Turkey",
            "United Kingdom",
            "United States of America"]
        self.__gpa_European_Union = [
            "Austria",
            "Belgium",
            "Bulgaria",
            "Croatia",
            "Cyprus",
            "Czechia",
            "Denmark",
            "Estonia",
            "Finland",
            "France",
            "Germany",
            "Greece",
            "Hungary",
            "Ireland",
            "Italy",
            "Latvia",
            "Lithuania",
            "Luxembourg",
            "Malta",
            "Netherlands",
            "Poland",
            "Portugal",
            "Romania",
            "Slovakia",
            "Slovenia",
            "Spain",
            "Sweden"]
        self.__gpa_G20 = [
            "Argentina",
            "Australia",
            "Brazil",
            "Canada",
            "China",
            "India",
            "Indonesia",
            "Japan",
            "Mexico",
            "Russia",
            "Saudi Arabia",
            "South Africa",
            "South Korea",
            "Turkey",
            "United Kingdom",
            "United States of America"]
        self.__gpa_G7 = [
            "Canada",
            "France",
            "Germany",
            "Italy",
            "Japan",
            "United Kingdom",
            "United States of America"]
        self.__gpa_G4 = [
            "Brazil",
            "Germany",
            "India",
            "Japan"]
        self.__set_Africa = [
            "AFRICA",
            "Eastern Africa",
            "Middle Africa",
            "Northern Africa",
            "Southern Africa",
            "Western Africa"] 
        self.__set_Asia = [
            "ASIA",
            "Eastern Asia",
            "South-Central Asia",
            "Central Asia",
            "Southern Asia",
            "South-Eastern Asia",
            "Western Asia",
            "Kazakhstan",
            "Kyrgyzstan",
            "Tajikistan",
            "Turkmenistan",
            "Uzbekistan",
            "Armenia",
            "Azerbaijan",
            "Cyprus",
            "Georgia",
            "Turkey"]
        self.__set_Oceania = [
            "OCEANIA",
            "Australia/New Zealand",
            "Melanesia",
            "Micronesia",
            "Polynesia",
            "Australia",
            "New Zealand",
            "Fiji",
            "New Caledonia",
            "Papua New Guinea",
            "Solomon Islands",
            "Vanuatu",
            "Guam",
            "Kiribati",
            "Marshall Islands",
            "Micronesia (Fed. States of)",
            "Nauru",
            "Northern Mariana Islands",
            "Palau",
            "American Samoa",
            "Cook Islands",
            "French Polynesia",
            "Niue",
            "Samoa",
            "Tokelau",
            "Tonga",
            "Tuvalu",
            "Wallis and Futuna Islands"]
        self.__set_Northern_America = [
            "NORTHERN AMERICA",
            "Canada",
            "Greenland",
            "Saint Pierre and Miquelon",
            "United States of America"]
        self.__set_Europe = [
            "EUROPE",
            "Eastern Europe",
            "Northern Europe",
            "Southern Europe",
            "Western Europe",
            "Belarus",
            "Republic of Moldova",
            "Russian Federation",
            "Ukraine",
            "Channel Islands",
            "Faeroe Islands",
            "Iceland",
            "Isle of Man",
            "Norway",
            "United Kingdom",
            "Albania",
            "Andorra",
            "Bosnia and Herzegovina",
            "Gibraltar",
            "Holy See",
            "Montenegro",
            "San Marino",
            "Serbia",
            "TFYR Macedonia",
            "Liechtenstein",
            "Monaco",
            "Switzerland"]
        self.__set_Latin_America = [
            "LATIN AMERICA AND THE CARIBBEAN",
            "Caribbean",
            "United States Virgin Islands",
            "Central America",
            "Mexico",
            "South America",
            "Bermuda"]
        self.__set_Small_Territory = [
            "Anguilla",
            "American Samoa",
            "Antigua and Barbuda",
            "Aruba",
            "Barbados",
            "Bermuda",
            "Cabo Verde",
            "Cayman Islands",
            "China, Hong Kong SAR",
            "China, Macao SAR",
            "Comoros",
            "Cook Islands",
            "Dominica",
            "Faeroe Islands",
            "French Polynesia",
            "Gibraltar",
            "Grenada",
            "Guadeloupe",
            "Guam",
            "Kiribati",
            "Maldives",
            "Malta",
            "Martinique",
            "Mauritius",
            "Micronesia",
            "Micronesia (Fed. States of)",
            "Montserrat",
            "Nauru",
            "Caribbean Netherlands",
            "Niue",
            "Reunion",
            "Saint Helena",
            "Saint Kitts and Nevis",
            "Saint Lucia",
            "Saint Pierre and Miquelon",
            "Saint Vincent and the Grenadines",
            "Samoa",
            "Sao Tome and Principe",
            "Seychelles",
            "Singapore",
            "Tonga",
            "Turks and Caicos Islands",
            "Tuvalu",
            "United States Virgin Islands",
            "Wallis and Futuna Islands"]
        self.__set_Aggregate = [
            "AFRICA",
            "ASIA",
            "Australia/New Zealand",
            "Caribbean",
            "Central America",
            "Central Asia",
            "EUROPE",
            "Eastern Africa",
            "Eastern Asia",
            "Eastern Europe",
            "GPA_Africa",
            "GPA_China",
            "GPA_Eiropean_Union",
            "GPA_Europe",
            "GPA_Former_CIS",
            "GPA_G20",
            "GPA_G4",
            "GPA_G7",
            "GPA_Indostan",
            "GPA_Middle_East",
            "GPA_North_America",
            "GPA_OECD",
            "GPA_OPEC",
            "GPA_Other_Asia_Oceania",
            "GPA_Permanent5",
            "GPA_South_America",
            "High-income countries",
            "LATIN AMERICA AND THE CARIBBEAN",
            "Least developed countries",
            "Less developed regions",
            "Less developed regions, excluding China",
            "Less developed regions, excluding least developed countries",
            "Low-income countries",
            "Lower-middle-income countries",
            "Melanesia",
            "Middle Africa",
            "Middle-income countries",
            "Micronesia",
            "More developed regions",
            "NORTHERN AMERICA",
            "Northern Africa",
            "Northern Europe",
            "OCEANIA",
            "Polynesia",
            "South America",
            "South-Central Asia",
            "South-Eastern Asia",
            "Southern Africa",
            "Southern Asia",
            "Southern Europe",
            "Sub-Saharan Africa",
            "Upper-middle-income countries",
            "WORLD",
            "Western Africa",
            "Western Asia",
            "Western Europe"]
        return
    def English_2_Russian( self, name):
        try:
            return self.__dict_EngRus[name]
        except:
            return "Не переводится: " + name
        return
    def Russian_2_English( self, name):
        for eng, rus in self.__dict_EngRus.items():
            if rus == name: return( eng)
        return "Cannot translate: " + name
    def GetAccuracy( self, name):
        """
        Returns the estimated data accuracy
        """
        if name in self.__set_LowAccuracy: return 0.015
        return 0.005
    def is_region_Africa_gpa( self, name):
        """
        Returns true for countries in Africa geopolitical area
        """
        return name in self.__gpa_Africa
    def is_region_China_gpa( self, name):
        """
        Returns true for countries belonging to China geopolitical area
        """
        return name in self.__gpa_China
    def is_region_Former_CIS_gpa( self, name):
        """
        Returns true for countries belonging to the former CIS geopolitical area
        """
        return name in self.__gpa_Former_CIS
    def is_region_Europe_gpa( self, name):
        """
        Returns true for countries belonging to Europe geopolitical area (BP considers Turkey as a part of Europe)
        """
        if name in ["Turkey", "Cyprus"]: return True
        if name in self.__gpa_Former_CIS: return False
        if name in self.__gpa_European_Union: return True
        return name in self.__gpa_Other_Europe
    def is_region_Indostan_gpa( self, name):
        """
        Returns true for countries belonging to Indostan geopolitical area
        """
        return name in self.__gpa_Indostan
    def is_region_Other_Asia_gpa( self, name):
        """
        Returns true for countries belonging to the rest of Asia and Oceania
        besides China and Indostan geopolitical areas
        """
        return name in self.__gpa_Other_Asia
    def is_region_Middle_East_gpa( self, name):
        """
        Returns true for countries belonging to the Middle East geopolitical area
        """
        return name in self.__gpa_Middle_East
    def is_region_South_America_gpa( self, name):
        """
        Returns true for countries belonging to the South America geopolitical area
        """
        return name in self.__gpa_South_America
    def is_region_North_America_gpa( self, name):
        """
        Returns true for countries belonging to the North America geopolitical area
        """
        return name in self.__gpa_North_America
    def is_region_P5_gpa( self, name):
        """
        Returns true for countries belonging to the permanent members of the UN Security Council
        """
        return name in self.__gpa_P5
    def is_region_OPEC_gpa( self, name):
        """
        Returns true for countries belonging to the OPEC members
        """
        return name in self.__gpa_OPEC
    def is_region_OECD_gpa( self, name):
        """
        Returns true for countries belonging to OECD
        """
        return name in self.__gpa_OECD
    def is_region_European_Union_gpa( self, name):
        """
        Returns true for countries belonging to the EU
        """
        return name in self.__gpa_European_Union
    def is_region_G20_gpa( self, name):
        """
        Returns true for countries belonging to the "Big 20"
        """
        if self.is_region_European_Union_gpa( name): return True
        return name in self.__gpa_G20
    def is_region_G7_gpa( self, name):
        """
        Returns true for countries belonging to the "Big 7"
        """
        return name in self.__gpa_G7
    def is_region_G4_gpa( self, name):
        """
        Returns true for countries belonging to the "Block of four" in the UN
        """
        return name in self.__gpa_G4
    def is_Africa( self, name):
        """
        Returns true for any entity in Africa
        """
        if self.is_region_Africa_gpa( name): return True
        return name in self.__set_Africa
    def is_Asia( self, name):
        """
        Returns true for entity in Asia (the UN presumes Turkey to be a part of Asia)
        """
        if self.is_region_China_gpa( name): return True
        if self.is_region_Indostan_gpa( name): return True
        if self.is_region_Other_Asia_gpa( name): return True
        if self.is_region_Middle_East_gpa( name): return True
        return name in self.__set_Asia
    def is_Oceania( self, name):
        """
        Returns true for entity in Oceania
        """
        return name in self.__set_Oceania
    def is_Northern_America( self, name):
        """
        Returns true for entity in North America
        """
        return name in self.__set_Northern_America
    def is_Europe( self, name):
        """
        Returns true for entity in Europe
        """
        if self.is_region_European_Union_gpa( name): return True
        return name in self.__set_Europe
    def is_Latin_America( self, name):
        """
        Returns true for entity in Latin America (by the UN definition)
        """
        if self.is_region_South_America_gpa( name): return True
        return name in self.__set_Latin_America        
    def is_Small_Territory( self, name):
        """
        Returns true for entity is a small island or territory (in EIA stats)
        """
        return name in self.__set_Small_Territory
    def is_Aggregate( self, name):
        """
        Returns true for entity is an aggregate
        """
        return name in self.__set_Aggregate
    def get_BP_Region( self, name):
        """
        Converts country name into one of the BP regions
        """
        if self.is_region_Africa_gpa(name): return "AFR"
        if self.is_region_Europe_gpa(name): return "EUR"
        if self.is_region_Former_CIS_gpa(name): return "CIS"
        if self.is_region_Middle_East_gpa(name): return "MEA"
        if self.is_region_South_America_gpa(name): return "SAM"
        if self.is_region_North_America_gpa(name): return "NAM"
        if self.is_region_China_gpa(name) or self.is_region_Indostan_gpa(name) or self.is_region_Other_Asia_gpa(name):
            return  "APAC"
        return "WORLD"

class Entity_UN:
    """
    Рrovides a programmatic interface to the UN country statistical data and future estimates
    The current UN statistics is from 1950 to 2015.
    The future estimates are from 2016 till 2100.
    """
    def __init__( self, country_dictionary, time, estimate="", low="", med="", high=""):
        self.Name = "Noname"
        self.RussianName = "Неизвестно"
        self.Time = time
        self.Population = np.zeros(len(time))
        self.Population_Low = np.zeros(len(time))
        self.Population_High = np.zeros(len(time))
        self.YError = np.zeros(len(time))
        self.Land_Area = -999.25
        self.Total_Area = -999.25
        self.Short_Name = self.Name 
        self.Code = "NONAME"
        if len(estimate) < 1: return
        estimate = estimate.strip()
        low = low.strip()
        med = med.strip()
        high = high.strip()
        estimate_S = estimate.split("\t")
        low_S = low.split("\t")
        med_S = med.split("\t")
        high_S = high.split("\t")
        self.Name = estimate_S[1]
        self.Short_Name = self.Name
        self.RussianName = country_dictionary.English_2_Russian( self.Name)
        acc = country_dictionary.GetAccuracy( self.Name)
        for i in range( 2,len(estimate_S)):
            j = 148 + i
            self.Population[j] = float(estimate_S[i])/1000.0
            self.Population_Low[j] = self.Population[j] * (1.0-acc)
            self.Population_High[j] = self.Population[j] * (1.0+acc)
            self.YError[j] = self.Population[j] * acc
        for i in range( 3,len(med_S)):
            j = 213 + i
            self.Population[j] = float(med_S[i])/1000.0
            self.Population_Low[j] = float(low_S[i])/1000.0 * (1.0-acc)
            self.Population_High[j] = float(high_S[i])/1000.0 * (1.0+acc)
            self.YError[j] = (self.Population_High[j]-self.Population_Low[j])/2.0
        return
    def Save( self, name):
        """
        Saves the entity as a CSV file
        """
        name1 = name + "_UN_Mid.csv"
        name2 = name + "_UN_Low.csv"
        name3 = name + "_UN_Hig.csv"
        f_out1 = self.__openFile__( name1, "Medium estimate")
        f_out2 = self.__openFile__( name2, "Low estimate")
        f_out3 = self.__openFile__( name3, "High estimate")
        for i, t in enumerate(self.Time):
            t = "{:4d}".format( int(t))
            f_out1.write( "{:s},{:.3f}\n".format(t, self.Population[i]))
            f_out2.write( "{:s},{:.3f}\n".format(t, self.Population_Low[i]))
            f_out3.write( "{:s},{:.3f}\n".format(t, self.Population_High[i]))
        f_out1.close()
        f_out2.close()
        f_out3.close()
        return
    def SmoothTail( self):
        self.Population = Filter( self.Population, 0, 150, [1,1,1,2,2,2,1,1,1])
        return
    def AppendPre1950( self, data, smoothing, cal=1.0):
        print( "In year {:d} UN = {:.1f} OWID = {:.1f}".format( int(self.Time[150]), self.Population[150], data[150]))
        Calibration = np.sum( self.Population[150:170] / data[150:170]) / 20.0
        print( self.Name + " calibration: " + str(Calibration))
        acc = 3.0 * self.GetAccuracy()
        self.Population[:150] = data[:150] * cal
        for i in range(smoothing): self.SmoothTail()
        self.Population_Low[:150] = self.Population[:150] * (1.0-acc)
        self.Population_High[:150] = self.Population[:150] * (1.0+acc)
        self.YError[:150] = self.Population[:150] * acc
        return
    def __openFile__( self, name, description):
        f_out = open( name, "w", encoding="cp1251")
        f_out.write( "#\n")
        f_out.write( "# " + description + "\n")
        f_out.write( "#\n")
        f_out.write( "# Horizontal conversion = 150,1080,1800,2100,year\n")
        f_out.write( "# Vertical conversion = 713,97,0,7000,mln\n")
        f_out.write( "#\n")
        f_out.write( "Year,Population\n")
        return f_out
    def GetLandUsage(self):
        lu1 = self.Land_Area / (self.Population + 1e-6) / 100
        lu2 = self.Land_Area / (self.Population_Low + 1e-6) / 100
        lu3 = self.Land_Area / (self.Population_High + 1e-6) / 100
        return lu1, lu2, lu3

class Population_UN:
    """
    Рrovides a programmatic interface to the UN country statistical data and future estimates
    The current statistics is from 1950 to 2015.
    The future estimates are from 2019 till 2100.
    This class reads UN data bases, extracts entries
    """
    def __init__( self):
        self.Country_Dictionary = Country_Dictionary()
        f0 = open("../Global Data/UN_RAW_1950_2015.txt", encoding="cp1251")
        f1 = open("../Global Data/UN_LOW_2015_2100.txt", encoding="cp1251")
        f2 = open("../Global Data/UN_MED_2015_2100.txt", encoding="cp1251")
        f3 = open("../Global Data/UN_HIG_2015_2100.txt", encoding="cp1251")
        f0.readline()
        f1.readline()
        f2.readline()
        f3.readline()
        self.Time = np.linspace(1800,2100,301)
        self.Entities = []
        for i in range(1000):
            s0 = f0.readline()    
            s1 = f1.readline()    
            s2 = f2.readline()    
            s3 = f3.readline()
            if len(s0) <= 0:
                print( "Read lines: " + str(i))
                break
            e = Entity_UN( self.Country_Dictionary,self.Time,s0,s1,s2,s3)
            self.Entities += [e]
        f0.close()
        f1.close()
        f2.close()
        f3.close()
        print( "Processed: " + str(len(self.Entities)))
        for e in self.Entities:
            if self.Country_Dictionary.is_Africa( e.Name): continue
            if self.Country_Dictionary.is_Asia(e.Name): continue
            if self.Country_Dictionary.is_Oceania(e.Name): continue
            if self.Country_Dictionary.is_Northern_America(e.Name): continue
            if self.Country_Dictionary.is_Latin_America(e.Name): continue
            if self.Country_Dictionary.is_Europe(e.Name): continue
            if self.Country_Dictionary.is_Aggregate(e.Name): continue
            print( e.Name)
        self.Country_Codes, self.Short_Names, self.Long_Names, Area_Land_Sea, Area_Land = Load_Calibration_Text(
            "../Global Data/Country_Area.txt", ["Code", "Short_Name", "Country_Name", "Land_and_Sea", "Land"], "\t")
        Area_Land_Sea = Strings_To_Array(Area_Land_Sea)
        Area_Land = Strings_To_Array(Area_Land)
        for i, longName in enumerate( self.Long_Names):
            ent = self.GetEntity( longName)
            if " not found" in ent.Name: continue
            ent.Land_Area = Area_Land[i]
            ent.Total_Area = Area_Land_Sea[i]
            ent.Short_Name = self.Short_Names[i]
            ent.Code = self.Country_Codes[i]
        self.MakeAggregateEntity( "GPA_Africa", "gpaAFR", "GPAAFR", self.Country_Dictionary.is_region_Africa_gpa)
        self.MakeAggregateEntity( "GPA_China", "gpaCHI", "GPACHI", self.Country_Dictionary.is_region_China_gpa)
        self.MakeAggregateEntity( "GPA_Former_CIS", "gpaCIS", "GPACIS", self.Country_Dictionary.is_region_Former_CIS_gpa)
        self.MakeAggregateEntity( "GPA_Europe", "gpaEUR", "GPAEUR", self.Country_Dictionary.is_region_Europe_gpa)
        self.MakeAggregateEntity( "GPA_Indostan", "gpaIND", "GPAIND", self.Country_Dictionary.is_region_Indostan_gpa)
        self.MakeAggregateEntity( "GPA_Other_Asia_Oceania", "gpaOAO", "GPAOAO", self.Country_Dictionary.is_region_Other_Asia_gpa)
        self.MakeAggregateEntity( "GPA_Middle_East", "gpaMEA", "GPAMEA", self.Country_Dictionary.is_region_Middle_East_gpa)
        self.MakeAggregateEntity( "GPA_South_America", "gpaSAM", "GPASAM", self.Country_Dictionary.is_region_South_America_gpa)
        self.MakeAggregateEntity( "GPA_North_America", "gpaNAM", "GPANAM", self.Country_Dictionary.is_region_North_America_gpa)
        self.MakeAggregateEntity( "GPA_Permanent5", "gpaP5", "GPAP5", self.Country_Dictionary.is_region_P5_gpa)
        self.MakeAggregateEntity( "GPA_OPEC", "gpaOPEC", "GPAOPEC", self.Country_Dictionary.is_region_OPEC_gpa)
        self.MakeAggregateEntity( "GPA_OECD", "gpaOECD", "GPAOECD", self.Country_Dictionary.is_region_OECD_gpa)
        self.MakeAggregateEntity( "GPA_Eiropean_Union", "gpaEU", "GPAEU", self.Country_Dictionary.is_region_European_Union_gpa)
        self.MakeAggregateEntity( "GPA_G20", "gpaG20", "GPAG20", self.Country_Dictionary.is_region_G20_gpa)
        self.MakeAggregateEntity( "GPA_G7", "gpaG7", "GPAG7", self.Country_Dictionary.is_region_G7_gpa)
        self.MakeAggregateEntity( "GPA_G4", "gpaG4", "GPAG4", self.Country_Dictionary.is_region_G4_gpa)
        return
    def MakeAggregateEntity(self, name, short_name, code, condition):
        region_entity = Entity_UN( self.Country_Dictionary, self.Time)
        region_entity.Name = name
        region_entity.Land_Area = 0.0
        region_entity.Total_Area = 0.0
        region_entity.Short_Name = short_name 
        region_entity.Code = code
        for ent in self.Entities:
            if not condition(ent.Name): continue
            region_entity.Land_Area += ent.Land_Area
            region_entity.Total_Area += ent.Total_Area
            region_entity.Population += ent.Population
            region_entity.Population_Low += ent.Population_Low
            region_entity.Population_High += ent.Population_High
            region_entity.YError += ent.YError
        self.Entities += [region_entity]
        return
    def GetEntity( self, name):
        n = name.lower()
        for e in self.Entities:
            if e.Name.lower() == n: return e
            if e.Short_Name.lower() == n: return e
            if e.Code != "NONAME" and e.Code.lower() == n: return e
        return Entity_UN(self.Country_Dictionary, self.Time, "0\t" + name + " not found","0\tnull","0\tnull","0\tnull")

class Country_Fertility():
    """
    Describes fertility in single country, based on the UN data
    """
    def __init__( self, name, year, tfr, leb):
        self.Name = name
        self.Data = {year: (float(year), float(tfr), float(leb))}
        #print("{:s} created".format( self.Name))
        return
    def Add_TFR( self, year, tfr):
        if year in self.Data:
            d = self.Data[year]
            self.Data[year] = (float(year), float(tfr), d[2])
            return
        self.Data[year] = (float(year), float(tfr), -999.0)        
        return
    def Add_LEB( self, year, leb):
        if year in self.Data:
            d = self.Data[year]
            self.Data[year] = (float(year), d[1], float(leb))
            return
        self.Data[year] = (float(year), -999.0, float(leb))        
        return
    def Get_TFR_vs_Year( self):
        tmp_y = []
        tmp_t = []
        for i, v in self.Data.items():
            if v[1] < 0: continue
            tmp_y += [v[0]]
            tmp_t += [v[1]]
        return np.array(tmp_y), np.array(tmp_t)
    def Get_LEB_vs_Year( self, lim=1950):
        tmp_y = []
        tmp_l = []
        for i, v in self.Data.items():
            if v[2] < 0: continue
            if v[0] < lim: continue
            tmp_y += [v[0]]
            tmp_l += [v[2]]
        return np.array(tmp_y), np.array(tmp_l)
    def Get_TFR_vs_LEB( self):
        tmp_t = []
        tmp_l = []
        for i, v in self.Data.items():
            if v[1] < 0: continue
            if v[2] < 0: continue
            tmp_t += [v[1]]
            tmp_l += [v[2]]
        return np.array(tmp_l), np.array(tmp_t)

class UN_Fertility():
    """
    Programmatic access to the UN fertility data
    """
    def __init__( self):
        self.Countries = {}
        country, year, leb = Load_Calibration_Text("../Global Data/UN_LEB_Estimates.csv", ["Entity","Year","LEB"], "\t")
        for i, c in enumerate(country):
            if not c in self.Countries:
                self.Countries[c] = Country_Fertility( c, year[i], -999.0, leb[i])
                continue
            self.Countries[c].Add_LEB( year[i], leb[i])
        country, year, tfr = Load_Calibration_Text("../Global Data/UN_TFR_Estimates.csv", ["Entity","Year","TFR"], "\t")
        for i, c in enumerate(country):
            if not c in self.Countries:
                self.Countries[c] = Country_Fertility( c, year[i], tfr[i], -999.0)
                continue
            self.Countries[c].Add_TFR( year[i], tfr[i])
        self.Exceptions = ["French Guiana",
            "Israel",
            "Kazakhstan",
            "Kyrgyzstan",
            "Mongolia",
            "Niger",
            "Nigeria",
            "Syria",
            "Tajikistan",
            "Timor-Leste",
            "Turkmenistan",
            "Zimbabwe"]
        self.Group_2a = ["Afghanistan",
            "Angola",
            "Bangladesh",
            "Benin",
            "Bhutan",
            "Burkina Faso",
            "Burundi",
            "Cameroon",
            "Central African Republic",
            "Chad",
            "Comoros",
            "Congo",
            "Cote d'Ivoire",
            "Democratic Republic of the Congo",
            "Djibouti",
            "Egypt",
            "Equatorial Guinea",
            "Eritrea",
            "Ethiopia",
            "Gabon",
            "Gambia",
            "Ghana",
            "Guinea-Bissau",
            "Guinea",
            "Haiti",
            "Iraq",
            "Jordan",
            "Kenya",
            "Kiribati",
            "Laos",
            "Lesotho",
            "Liberia",
            "Madagascar",
            "Malawi",
            "Mali",
            "Mauritania",
            "Mayotte",
            "Melanesia",
            "Micronesia (Fed. States of)",
            "Micronesia",
            "Mozambique",
            "Namibia",
            "Pakistan",
            "Palestine",
            "Papua New Guinea",
            "Philippines",
            "Rwanda",
            "Samoa",
            "Sao Tome and Principe",
            "Senegal",
            "Sierra Leone",
            "Solomon Islands",
            "Somalia",
            "South Sudan",
            "Sudan",
            "Swaziland",
            "Tanzania",
            "Togo",
            "Tonga",
            "Uganda",
            "Vanuatu",
            "Yemen",
            "Zambia"]
        self.Group_2b = ["Algeria",
            "Bahrain",
            "Belize",
            "Bolivia",
            "Botswana",
            "Cabo Verde",
            "Cambodia",
            "Colombia",
            "Dominican Republic",
            "Ecuador",
            "El Salvador",
            "Fiji",
            "French Polynesia",
            "Guatemala",
            "Honduras",
            "India",
            "Indonesia",
            "Iran",
            "Libya",
            "Maldives",
            "Mauritius",
            "Mexico",
            "Morocco",
            "Myanmar",
            "Nepal",
            "New Caledonia",
            "Nicaragua",
            "Oman",
            "Panama",
            "Paraguay",
            "Peru",
            "Polynesia",
            "Reunion",
            "Saint Vincent and the Grenadines",
            "Saudi Arabia",
            "South Africa",
            "Suriname",
            "Thailand",
            "Tunisia",
            "Turkey",
            "United Arab Emirates",
            "Western Sahara"]
        self.Group_3 = ["Albania",
            "Antigua and Barbuda",
            "Argentina",
            "Armenia",
            "Aruba",
            "Australia",
            "Azerbaijan",
            "Bahamas",
            "Barbados",
            "Bosnia and Herzegovina",
            "Brazil",
            "Brunei",
            "Canada",
            "Chile",
            "China, Hong Kong SAR",
            "China, Macao SAR",
            "China",
            "Costa Rica",
            "Cuba",
            "Curacao",
            "Cyprus",
            "Dem. People's Republic of Korea",
            "Finland",
            "Grenada",
            "Guadeloupe",
            "Guam",
            "Guyana",
            "Iceland",
            "Ireland",
            "Jamaica",
            "Japan",
            "Kuwait",
            "Lebanon",
            "Macedonia",
            "Malaysia",
            "Malta",
            "Martinique",
            "Moldova",
            "Montenegro",
            "Netherlands",
            "New Zealand",
            "Norway",
            "Poland",
            "Portugal",
            "Puerto Rico",
            "Qatar",
            "Republic of Korea",
            "Romania",
            "Saint Lucia",
            "Serbia",
            "Seychelles",
            "Singapore",
            "Slovakia",
            "Slovenia",
            "Sri Lanka",
            "Taiwan",
            "Trinidad and Tobago",
            "United States of America",
            "United States Virgin Islands",
            "Uruguay",
            "Uzbekistan",
            "Venezuela",
            "Vietnam"]
        self.Group_4 = ["Austria",
            "Belarus",
            "Belgium",
            "Bulgaria",
            "Channel Islands",
            "Croatia",
            "Czechia",
            "Denmark",
            "Estonia",
            "France",
            "Georgia",
            "Germany",
            "Greece",
            "Hungary",
            "Italy",
            "Latvia",
            "Lithuania",
            "Luxembourg",
            "Russia",
            "Spain",
            "Sweden",
            "Switzerland",
            "Ukraine",
            "United Kingdom"]
        self.Regions = ["Africa",
            "Asia",
            "Caribbean",
            "Central America",
            "Central Asia",
            "Eastern Africa",
            "Eastern Asia",
            "Eastern Europe",
            "Europe",
            "High-income countries",
            "Latin America and the Caribbean",
            "Least developed countries",
            "Less developed regions, excluding China",
            "Less developed regions, excluding least developed countries",
            "Less developed regions",
            "Low-income countries",
            "Lower-middle-income countries",
            "Middle Africa",
            "Middle-income countries",
            "More developed regions",
            "Northern Africa",
            "Northern America",
            "Northern Europe",
            "Oceania",
            "South America",
            "South-Central Asia",
            "South-Eastern Asia",
            "Southern Africa",
            "Southern Asia",
            "Southern Europe",
            "Sub-Saharan Africa",
            "Upper-middle-income countries",
            "Western Africa",
            "Western Asia",
            "Western Europe",
            "World"]
        self.Areas = ["Africa",
            "Asia",
            "Europe",
            "Latin America and the Caribbean",
            "Northern America",
            "Oceania",
            "World"]
        return

#
# Test code
#
if __name__ == "__main__":
    help( Population)
    help( Country_Dictionary)
    help( Entity_UN)
    help( Population_UN)
    
    pun = Population_UN()
    World = pun.GetEntity("WORLD")
    y = np.where( World.Time==2018.0)[0][0]
    check = 0.0
    print("World split by geopolitical blocks:")
    for c in [ "gpaAFR", "gpaCHI", "gpaCIS", "gpaEUR", "gpaIND", "gpaOAO", "gpaMEA", "gpaSAM", "gpaNAM"]:
        ent = pun.GetEntity(c)
        print("   {:s} population in {:g}: {:.3f}".format( ent.Name, ent.Time[y], ent.Population[y]))
        check += ent.Population[y]
    print("   World population in 2018: {:.3f}".format( World.Population[y]))
    print("   World check: {:.3f}".format( check))

    check = 0.0
    print("World split by UN regions:")
    for c in [ "AFRICA", "ASIA", "EUROPE", "LATIN AMERICA AND THE CARIBBEAN","NORTHERN AMERICA","OCEANIA"]:
        ent = pun.GetEntity(c)
        print("   {:s} population in {:g}: {:.3f}".format( ent.Name, ent.Time[y], ent.Population[y]))
        check += ent.Population[y]
    print("   World population in 2018: {:.3f}".format( World.Population[y]))
    print("   World check: {:.3f}".format( check))

    print( "Africa:\t\t\t{:>8.3f}\t{:>8.3f}".format(
        pun.GetEntity("gpaAFR").Population[y],
        pun.GetEntity("AFRICA").Population[y]))
    print( "Americas:\t\t{:>8.3f}\t{:>8.3f}".format(
        pun.GetEntity("gpaSAM").Population[y]+
        pun.GetEntity("gpaNAM").Population[y],
        pun.GetEntity("NORTHERN AMERICA").Population[y]+
        pun.GetEntity("LATIN AMERICA AND THE CARIBBEAN").Population[y]))
    print( "Eurasia:\t\t{:>8.3f}\t{:>8.3f}".format(
        pun.GetEntity("gpaCHI").Population[y]+
        pun.GetEntity("gpaCIS").Population[y]+
        pun.GetEntity("gpaEUR").Population[y]+
        pun.GetEntity("gpaIND").Population[y]+
        pun.GetEntity("gpaOAO").Population[y]+
        pun.GetEntity("gpaMEA").Population[y],
        pun.GetEntity("ASIA").Population[y]+
        pun.GetEntity("OCEANIA").Population[y]+
        pun.GetEntity("EUROPE").Population[y]))
    print( "Europe:\t\t\t{:>8.3f}\t{:>8.3f}".format(
        pun.GetEntity("gpaEUR").Population[y]+
        pun.GetEntity("Belarus").Population[y]+
        pun.GetEntity("Republic of Moldova").Population[y]+
        pun.GetEntity("Russian Federation").Population[y]+
        pun.GetEntity("Ukraine").Population[y]+
        pun.GetEntity("Estonia").Population[y]+
        pun.GetEntity("Latvia").Population[y]+
        pun.GetEntity("Lithuania").Population[y]-
        pun.GetEntity("Turkey").Population[y]-
        pun.GetEntity("Cyprus").Population[y],
        pun.GetEntity("EUROPE").Population[y]))
    print( "Asia and Oceania:\t{:>8.3f}\t{:>8.3f}".format(
        pun.GetEntity("gpaOAO").Population[y]+
        pun.GetEntity("gpaMEA").Population[y]+
        pun.GetEntity("gpaCHI").Population[y]+
        pun.GetEntity("gpaIND").Population[y]+
        pun.GetEntity("Turkey").Population[y]+
        pun.GetEntity("Cyprus").Population[y]+
        pun.GetEntity("Armenia").Population[y]+
        pun.GetEntity("Azerbaijan").Population[y]+
        pun.GetEntity("Georgia").Population[y]+
        pun.GetEntity("Kazakhstan").Population[y]+
        pun.GetEntity("Kyrgyzstan").Population[y]+
        pun.GetEntity("Tajikistan").Population[y]+
        pun.GetEntity("Turkmenistan").Population[y]+
        pun.GetEntity("Uzbekistan").Population[y],
        pun.GetEntity("ASIA").Population[y]+
        pun.GetEntity("OCEANIA").Population[y]))
