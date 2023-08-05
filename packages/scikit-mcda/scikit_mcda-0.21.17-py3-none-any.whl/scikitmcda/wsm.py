from mcda import MCDA, pd, np

class WSM(MCDA):
    def __init__(self):
        super().__init__()        
    
    def decide(self, normalization_method=None):  
        self._MCDA__set_normalization_method(normalization_method)
        self._MCDA__normalize()
        self._MCDA__weighting_from_normalized()
        self.__wsm()
        return "wsm"


    def __wsm(self):
        wsm = pd.DataFrame(self.df_weighted.iloc[:, 1:])
        wsm = pd.DataFrame(wsm.sum(axis=1), columns=["WSM"])
        i = np.arange(1, len(self.df_original.index)+1, 1)
        df_concat_labels = pd.DataFrame(self.df_original.iloc[:,0]).join(wsm).sort_values(by=["WSM"], ascending=False, ignore_index=True)
        df_ranking = df_concat_labels.join(pd.DataFrame(i, columns=["rank"]))
        self.df_decision = df_ranking

