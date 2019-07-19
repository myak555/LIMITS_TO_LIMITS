from Predictions import *

class Population_World3:
    """
    Описывает популяцию матрицей Лесли с шагом 1 год
    year0 - начальный год модели
    population0 - общее население в начальном году
    tfr - количество живых родов в среднем у женщщны
    leb - ожидаемая продолжительность жизни при рождении
    m2f - отношение мальчики:девочки при рождении
    """
    def __init__( self, year0=1890, population0=1530.880, tfr=5.4, leb=30, m2f=1.05):
        self.Year = year0
        self.Ages = np.linspace( 0,199, 200)
        self.Population_Male = np.ones( 200)
        self.Population_Female = np.ones( 200)
        self.Attrition_Model_Male = Bathtub( x0=5.0, s0=1.0, x1=80, s1=0.2, left=0.1, middle=0.01, right=0.20)
        self.Attrition_Model_Female = Bathtub( x0=5.0, s0=1.0, x1=80, s1=0.2, left=0.1, middle=0.01, right=0.20)
        self.Fertility_Model = Bathtub( x0=18.0, s0=1.0, x1=35, s1=0.4, left=0.0, middle=1, right=0)
        self.TFR = tfr
        self.LEB_Male = leb-2
        self.LEB_Female = leb+2
        self.M2F = m2f
        self.__expectancy__ = Linear_Combo()
        self.__expectancy__.Wavelets += [Hubbert( x0=-10.0, s0=0.064, s1=0.064, peak= 0.370)]
        self.__expectancy__.Wavelets += [Hubbert( x0= 45.0, s0=0.095, s1=0.092, peak= 0.024)]
        self.__expectancy__.Wavelets += [Hubbert( x0= 14.0, s0=0.349, s1=0.214, peak=-0.018)]
        self.__expectancy__.Wavelets += [Hubbert( x0=  6.0, s0=1.162, s1=1.162, peak= 0.017)]
        self.__expectancy__.Wavelets += [Hubbert( x0= 82.0, s0=0.240, s1=0.240, peak=-0.009)]

        # create initial population
        for i in range( 300): self.Compute_Next_Year()
        self.Normalize( population0)
        self.Compute_Next_Year()
        self.Normalize( population0)
        self.Year = year0
        return
    def Set_Attrition_Model( self, attr=None):
        if not attr is None:
            self.Attrition_Model_Male.Left = attr
            self.Attrition_Model_Male.Middle = attr * 0.1
            self.Attrition_Model_Female.Left = attr
            self.Attrition_Model_Female.Middle = attr * 0.1
            return
        self.Attrition_Model_Male.Left = self.__expectancy__.Compute_Clipped(
            Limit( self.LEB_Male, 5, 85), min_y=0.001, max_y=0.300)
        self.Attrition_Model_Male.Middle = self.Attrition_Model_Male.Left * 0.1
        self.Attrition_Model_Female.Left = self.__expectancy__.Compute_Clipped(
            Limit( self.LEB_Female, 5, 85), min_y=0.001, max_y=0.300)
        self.Attrition_Model_Female.Middle = self.Attrition_Model_Female.Left * 0.1
        return
    def Compute_LEB(self, attrition, population):
        """
        Computes true and apparent LEB
        """
        leb_true = 0
        counter = 1
        for i in range(199):
            counter *= 1-attrition[i]
            leb_true += counter
        pSum = np.sum( population)
        if pSum <= 0: return leb_true, 0.0
        tmpLEB = attrition * population
        tmpLEB[-1] = population[-1]
        leb_apparent = np.sum( tmpLEB * self.Ages) / np.sum(tmpLEB)
        return leb_true, leb_apparent
    def Compute_Next_Year( self, tfr=None, leb_male=None, leb_female=None, m2f=None,):
        self.Year += 1
        if not tfr is None: self.TFR = tfr
        if not leb_male is None: self.LEB_Male = leb_male
        if not leb_female is None: self.LEB_Female = leb_female
        if not m2f is None: self.M2F = m2f
        self.Set_Attrition_Model()
        attrition_male = self.Attrition_Model_Male.GetVector( self.Ages)
        attrition_female = self.Attrition_Model_Female.GetVector( self.Ages)
        self.LEB_True_Male, self.LEB_Apparent_Male = self.Compute_LEB(
            attrition_male, self.Population_Male )
        self.LEB_True_Female, self.LEB_Apparent_Female = self.Compute_LEB(
            attrition_female, self.Population_Female )
        self.nDeath = np.sum( self.Population_Male * attrition_male)
        self.nDeath += np.sum( self.Population_Female * attrition_female)
        self.Population_Male = np.roll( self.Population_Male * (1-attrition_male), 1)
        self.Population_Female = np.roll( self.Population_Female * (1-attrition_female), 1)
        fertility = self.Fertility_Model.GetVector(self.Ages)
        nFertile = np.dot( self.Population_Female, fertility)
        self.nBirth = nFertile * self.TFR / np.sum( fertility)
        self.Population_Male[0] = self.nBirth * 0.5 * self.M2F
        self.Population_Female[0] = self.nBirth  - self.Population_Male[0]
        self.Total = np.sum(self.Population_Male) + np.sum(self.Population_Female)
        return
    def Normalize( self, norm):
        n = np.sum( self.Population_Male) + np.sum( self.Population_Female)
        if n <= 0.0: return
        n = norm/n
        self.Population_Male *= n
        self.Population_Female *= n
        self.Total = np.sum(self.Population_Male) + np.sum(self.Population_Female)
        return
