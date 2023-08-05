from mcda import MCDA, pd, np, Vector_

class TOPSIS(MCDA):
    def __init__(self):
        self.df_pis = []
        self.df_nis = []
        self.df_closeness = 0
        super().__init__()        
    
    def decide(self, normalization_method=Vector_):
        self._MCDA__set_normalization_method(normalization_method)      
        self._MCDA__normalize(True)
        self._MCDA__weighting_from_normalized()
        self.__xis()
        self.__topsis()
        return "topsis"
         
    def __xis(self):
        pis = pd.DataFrame(self.df_weighted.iloc[:, 1:] * self.signals).max(axis=0) * self.signals
        self.df_pis = pis
        nis = pd.DataFrame(self.df_weighted.iloc[:, 1:] * self.signals).min(axis=0) * self.signals
        self.df_nis = nis

    def __topsis(self):
        dp = np.sqrt(self.df_weighted.iloc[:, 1:].sub(self.df_pis).pow(2).sum(axis=1))
        dn = np.sqrt(self.df_weighted.iloc[:, 1:].sub(self.df_nis).pow(2).sum(axis=1))
        closeness = pd.DataFrame(dn.div(dp+dn), columns=["performance score"])
        i = np.arange(1, len(self.df_original.index)+1, 1)
        df_ranking = pd.DataFrame(self.df_original.iloc[:,0]).join(closeness).sort_values(by=["performance score"], ascending=False)
        df_ranking["rank"] = i

        self.df_decision = df_ranking.sort_index()
