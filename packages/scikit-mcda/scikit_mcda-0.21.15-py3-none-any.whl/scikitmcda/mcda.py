'''
#########################################################
# SCI-KIT-MCDA Library                                  #
# Author: Antonio Horta                                 #
# https://gitlab.com/cybercrafter/scikit-mcda           #
# Cybercrafter ® 2021                                   #
#########################################################
'''

import pandas as pd
import numpy as np
import copy
from tabulate import tabulate
from constants import *

class MCDA:
    """
    Class: MCDA: Multi-Criteria Decision Aid
    """
    def __init__(self):
        self.df_original = 0
        self.weights = []
        self.signals = []
        self.normalization_method = None
        self.df_normalized = 0
        self.df_weighted = 0
        self.df_pis = []
        self.df_nis = []
        self.df_closeness = 0
        self.df_decision = []

    def dataframe(self, alt_data, alt_labels=[], criteria_label=[]):

        # define state labels if not exists
        if criteria_label == []:
            for s in range(0, len(alt_data[0])):
                state_label.append("C" + str(s+1))

        # define alternative labels if not exists
        if alt_labels == []:
            for a in range(0, len(alt_data)):
                alt_labels.append("A" + str(a+1))

        df_data = pd.DataFrame(data=alt_data, columns=criteria_label)
        df_data.insert(loc=0,
                    column='alternatives',
                    value=alt_labels)
        dfo = df_data

        self.df_original = copy.copy(dfo)
        self.df_calc = copy.copy(dfo)
        self.decision = []

    def set_weights_manually(self, weights):
        if self.__check_weights(weights) is True:
            self.weights = weights
        else:
            raise ValueError("Invalid weights! Each weight must be float between 0 and 1 and same number of criteria")

    def set_weights_by_ranking_A(self):
        """
        The criteria must be ordered by importance c1 > c2 > c3 ... 
        Wj = {1 / rj} / {∑[1 / rk], where k range is 1 to n}
        """
        n = len(self.df_original.columns) - 1
        r = np.arange(1, n+1, 1).tolist()
        W = []
        b = 0
        for k in r: # b = ∑[1 / rk]
            b = b + (1 / k)
        for j in r: # Wj = {1 / rj} / b
            W.append((1 / j) / b)
        
        self.weights = W

    def set_weights_by_ranking_B(self):
        """
        The criteria must be ordered by importance c1 > c2 > c3 ... 
        Wj = {n -rj + 1} / {∑[ n - rk + 1], where k range is 1 to n}
        """
        n = len(self.df_original.columns) - 1
        r = np.arange(1, n+1, 1).tolist()
        W = []
        b = 0
        for k in r: # b = ∑[ n - rk + 1]
            b = b + (n - k + 1)
        for j in r: # Wj = {n -rj + 1} / b
            W.append((n - j + 1) / b)
        
        self.weights = W

    def set_weights_by_ranking_C(self):
        """
        The criteria must be ordered by importance c1 > c2 > c3 ... 
        Wj = {1 / n} * {∑[ 1 / K ], where K range is j to n}
        """
        n = len(self.df_original.columns) - 1
        r = np.arange(1, n+1, 1)
        r = r[::-1].tolist()

        W = []
        b = 0
        a = 1 / n
        for k in r: # b = ∑[ 1 / K ]
            b = b + (1 / k)
            W.insert(0, a * b)
        
        self.weights = W

    def set_weights_by_ranking_B_POW(self, P=0):
        """
        The criteria must be ordered by importance c1 > c2 > c3 ... 
        Wj = {n -rj + 1}P / {∑[ n - rk + 1]P, where k range is 1 to n}
        """
        n = len(self.df_original.columns) - 1
        r = np.arange(1, n+1, 1).tolist()
        W = []
        b = 0
        for k in r: # b = ∑[ n - rk + 1]
            b = b + pow((n - k + 1),P)
        for j in r: # Wj = {n -rj + 1} / b
            W.append(pow((n - j + 1), P) / b)
  
        self.weights = W

    def set_weights_by_entropy(self, normalization_method_for_entropy=LinearSum_):
        
        # Save current norm method
        current_norm_method = self.normalization_method

        # appy new norm method for entropy and apply
        self.__set_normalization_method(normalization_method_for_entropy)

        self.__normalize()
        x, y = self.df_normalized.iloc[:,1:].shape
        entropies = np.empty(y)

        for i, col in enumerate(self.df_normalized.iloc[:,1:].T):
            if np.any(col == 0):
                entropies[i] = 0
            else:
                entropies[i] = -np.sum(col * np.log(col))
        entropies = entropies / np.log(x)

        result = 1 - entropies
        
        # set entropy weights
        self.weights = (result/np.sum(result)).tolist()


        #back current nor method
        self.normalization_method = current_norm_method

    def set_weights_by_AHP(self, saaty_preference_matrix):
        if self.__check_AHP_matrix(saaty_preference_matrix) is True:  
            saaty_preference_matrix = pd.DataFrame(saaty_preference_matrix)
            priority_vector = (saaty_preference_matrix / saaty_preference_matrix.sum(axis=0)).mean(axis=1)
            sum_of_weights = (saaty_preference_matrix * priority_vector).sum(axis=1)    
            lambda_max = (sum_of_weights/priority_vector).mean()
            n = len(priority_vector)
            CI = (lambda_max - n)/(n -1) 
            CR = CI/SAATY_RI[n-1]
        if CR <= 0.1:
            self.weights = priority_vector.values.tolist()
            return {"consistency": True, "lambda": lambda_max, "CIndex": CI, "CRatio": CR}
        else:
            return {"consistency": False, "lambda": lambda_max, "CIndex": CI, "CRatio": CR}
                  
    def set_signals(self, signals):
        if self.__check_signals(signals) is True:
            self.signals = signals
        else:
            raise ValueError("Invalid signals! It's must be a list of 1 or -1")

    def topsis(self, normalization_method=TopsisOriginal_):
        self.__set_normalization_method(normalization_method)      
        self.__normalize()
        self.__weighting_from_normalized()
        self.__xis()
        self.__topsis()
        return "topsis"

    def wsm(self, normalization_method=None):  
        self.__set_normalization_method(normalization_method)        
        self.__normalize()
        self.__weighting_from_normalized()
        self.__wsm()
        return "wsm"

    def wpm(self, normalization_method=None):  
        self.__set_normalization_method(normalization_method)        
        self.__normalize()
        self.__weighting_from_normalized()
        self.__wpm()
        return "wsm"

    def waspas(self, lambda_=0.5, normalization_method=None):
        if self.__check_lambda(lambda_) is True:
            self.__set_normalization_method(normalization_method)
            self.__normalize()
            self.__weighting_from_normalized()
            self.__waspas(lambda_)
            return "waspas"

    def __set_normalization_method(self, normalization_method):
        if normalization_method in NORMALIZATION_METHODS:
            self.normalization_method = normalization_method 
        elif normalization_method is None:
            self.normalization_method == None
        else:
            raise ValueError("Invalid parameter! Use a method defined in constants. e.g. normalization_D, zScore etc...")

    def __normalize(self):
        if self.normalization_method == Vector_:
            self.__norm_Vector()
        elif self.normalization_method == LinearSum_:
            self.__norm_LinearSum()
        elif self.normalization_method == LinearMinMax_:
            self.__norm_LinearMinMax()
        elif self.normalization_method == LinearMax_:
            self.__norm_LinearMax()
        elif self.normalization_method == EnhancedAccuracy_:
            self.__norm_EnhancedAccuracy()
        elif self.normalization_method == Logarithmic_:
            self.__norm_Logarithmic()
        elif self.normalization_method == TopsisOriginal_:
            self.__norm_TopsisOriginal()
        else:
            self.df_normalized = self.df_original

    def __norm_ZScore(self):
        normalized = (self.df_original.iloc[:, 1:] - self.df_original.iloc[:, 1:].mean(axis=0))/self.df_original.iloc[:, 1:].std(axis=0)
        self.df_normalized = pd.DataFrame(self.df_original.iloc[:, 0]).join(normalized)

    def __norm_EnhancedAccuracy(self):
        # _max for maximizing 
        normalized_max = 1 - (self.df_original.iloc[:, 1:].max(axis=0)-self.df_original.iloc[:, 1:])/((self.df_original.iloc[:, 1:].max(axis=0)-self.df_original.iloc[:, 1:]).sum(axis=0))
        # _min for minimizing 
        normalized_min = 1 - (self.df_original.iloc[:, 1:]-self.df_original.iloc[:, 1:].min(axis=0))/((self.df_original.iloc[:, 1:]-self.df_original.iloc[:, 1:].min(axis=0)).sum(axis=0))
        
        # make nomalized matrix based in signals
        normalized = pd.DataFrame(self.df_original.iloc[:, 0])
        i = 0
        for s in self.signals:
            if s == 1:
                normalized = normalized.join(normalized_max.iloc[:, i])
            else:
                normalized = normalized.join(normalized_min.iloc[:, i])
            i = i + 1
        
        self.df_normalized = normalized

    def __norm_Logarithmic(self):
        # _max for maximizing 
        normalized_max = np.log2(self.df_original.iloc[:, 1:]) / np.log2( np.log2(self.df_original.iloc[:, 1:]).prod(axis = 0) * self.df_original.iloc[:, 1:] )
        # _min for minimizing 
        normalized_min = 1 - ( (1 - normalized_max) / ( normalized_max.shape[0] - 1) )
        # make nomalized matrix based in signals
        normalized = pd.DataFrame(self.df_original.iloc[:, 0])
        i = 0
        for s in self.signals:
            if s == 1:
                normalized = normalized.join(normalized_max.iloc[:, i])
            else:
                normalized = normalized.join(normalized_min.iloc[:, i])
            i = i + 1
        
        self.df_normalized = normalized

    def __norm_LinearMax(self):
        # _max for maximizing 
        normalized_max = (self.df_original.iloc[:, 1:]/self.df_original.iloc[:, 1:].max(axis=0))
        # _min for minimizing 
        normalized_min = (self.df_original.iloc[:, 1:].min(axis=0)/self.df_original.iloc[:, 1:])
        
        # make nomalized matrix based in signals
        normalized = pd.DataFrame(self.df_original.iloc[:, 0])
        i = 0
        for s in self.signals:
            if s == 1:
                normalized = normalized.join(normalized_max.iloc[:, i])
            else:
                normalized = normalized.join(normalized_min.iloc[:, i])
            i = i + 1
        
        self.df_normalized = normalized

    def __norm_LinearMinMax(self):
        # _max for maximizing 
        normalized_max = (self.df_original.iloc[:, 1:]-self.df_original.iloc[:, 1:].min(axis=0))/(self.df_original.iloc[:, 1:].max(axis=0)-self.df_original.iloc[:, 1:].min(axis=0))
        # _min for minimizing 
        normalized_min = (self.df_original.iloc[:, 1:].max(axis=0)-self.df_original.iloc[:, 1:])/(self.df_original.iloc[:, 1:].max(axis=0)-self.df_original.iloc[:, 1:].min(axis=0))
        
        # make nomalized matrix based in signals
        normalized = pd.DataFrame(self.df_original.iloc[:, 0])
        i = 0
        for s in self.signals:
            if s == 1:
                normalized = normalized.join(normalized_max.iloc[:, i])
            else:
                normalized = normalized.join(normalized_min.iloc[:, i])
            i = i + 1
        
        self.df_normalized = normalized

    def __norm_LinearSum(self):
        # _max for maximizing 
        normalized_max = self.df_original.iloc[:, 1:]/self.df_original.iloc[:, 1:].sum(axis=0)
        # _min for minimizing 
        normalized_min = (1/self.df_original.iloc[:, 1:])/(1/self.df_original.iloc[:, 1:]).sum(axis=0)
        
        # make nomalized matrix based in signals
        normalized = pd.DataFrame(self.df_original.iloc[:, 0])
        i = 0
        for s in self.signals:
            if s == 1:
                normalized = normalized.join(normalized_max.iloc[:, i])
            else:
                normalized = normalized.join(normalized_min.iloc[:, i])
            i = i + 1
        
        self.df_normalized = normalized

    def __norm_Vector(self):
        # _max for maximizing 
        normalized_max = self.df_original.iloc[:, 1:]/np.sqrt(self.df_original.iloc[:, 1:].pow(2).sum(axis=0))
        # _min for minimizing 
        normalized_min = 1 - self.df_original.iloc[:, 1:]/np.sqrt(self.df_original.iloc[:, 1:].pow(2).sum(axis=0))
       
        # make nomalized matrix based in signals
        normalized = pd.DataFrame(self.df_original.iloc[:, 0])
        i = 0
        for s in self.signals:
            if s == 1:
                normalized = normalized.join(normalized_max.iloc[:, i])
            else:
                normalized = normalized.join(normalized_min.iloc[:, i])
            i = i + 1
        
        self.df_normalized = normalized

    def __norm_TopsisOriginal(self):
        # _max for maximizing 
        normalized_topsis = self.df_original.iloc[:, 1:]/np.sqrt(self.df_original.iloc[:, 1:].pow(2).sum(axis=0))
        
        # make nomalized matrix based in signals
        normalized = pd.DataFrame(self.df_original.iloc[:, 0])
        normalized = normalized.join(normalized_topsis.iloc[:, :])
        
        self.df_normalized = normalized

    def __weighting_from_normalized(self):
        weighted = self.df_normalized.iloc[:, 1:] * self.weights
        self.df_weighted = pd.DataFrame(self.df_original.iloc[:,0]).join(weighted)
         
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
        df_concat_labels = pd.DataFrame(self.df_original.iloc[:,0]).join(closeness).sort_values(by=["performance score"], ascending=False, ignore_index=True)
        df_ranking = df_concat_labels.join(pd.DataFrame(i, columns=["rank"]))
        self.df_decision = df_ranking

    def __waspas(self, lambda_):
        w_df = pd.DataFrame(self.df_weighted.iloc[:, 1:])       
       
        q_wsm = pd.DataFrame(w_df.sum(axis=1), columns=["WSM"]) * lambda_
        q_wpm = pd.DataFrame(w_df.prod(axis=1), columns=["WPM"]) * (1 - lambda_) 

        waspas = q_wsm.iloc[:,0] + q_wpm.iloc[:,0]
        label = "WASPAS (λ " + str(lambda_) + " )" 
        waspas_df = pd.DataFrame(waspas, columns=[label]) 

        i = np.arange(1, len(self.df_original.index)+1, 1)
        df_concat_labels = pd.DataFrame(self.df_original.iloc[:,0]).join(waspas_df).sort_values(by=[label], ascending=False, ignore_index=True)
        df_ranking = df_concat_labels.join(pd.DataFrame(i, columns=["rank"]))
        
        self.df_decision = df_ranking

    def __wsm(self):
        wsm = pd.DataFrame(self.df_weighted.iloc[:, 1:])
        wsm = pd.DataFrame(wsm.sum(axis=1), columns=["WSM"])
        i = np.arange(1, len(self.df_original.index)+1, 1)
        df_concat_labels = pd.DataFrame(self.df_original.iloc[:,0]).join(wsm).sort_values(by=["WSM"], ascending=False, ignore_index=True)
        df_ranking = df_concat_labels.join(pd.DataFrame(i, columns=["rank"]))
        self.df_decision = df_ranking

    def __wpm(self):
        wpm = pd.DataFrame(self.df_weighted.iloc[:, 1:])
        wpm = pd.DataFrame(wpm.prod(axis=1), columns=["WPM"])
        i = np.arange(1, len(self.df_original.index)+1, 1)
        df_concat_labels = pd.DataFrame(self.df_original.iloc[:,0]).join(wpm).sort_values(by=["WPM"], ascending=False, ignore_index=True)
        df_ranking = df_concat_labels.join(pd.DataFrame(i, columns=["rank"]))
        self.df_decision = df_ranking

    def __check_lambda(self, lambda_):
        result = False
        if type(lambda_) == float:
            if (lambda_ >= 0 and lambda_ <= 1):
                result = True
            else:
                raise ValueError("Lambda must be a value between 0 and 1!")                
        return result

    def __check_weights(self, weights):
        result = False
        if type(weights) == list:
            if len(self.df_original.columns.tolist()) - 1 == len(weights) \
               and all(isinstance(n, float) for n in weights) \
               and all((n >= 0 and n <= 1) for n in weights) \
               and round(sum(weights)) == 1:
                result = True
        return result

    def __check_signals(self, signals):
        result = False
        if type(signals) == list:
            if len(self.df_original.columns.tolist()) - 1 == len(signals) \
               and all(isinstance(n, int) for n in signals) \
               and all((n == 1 or n == -1) for n in signals):                
                result = True
        return result

    def __check_AHP_matrix(self, saaty_preference_matrix):
        if type(saaty_preference_matrix) == list:  
            saaty_preference_matrix = pd.DataFrame(saaty_preference_matrix)
            x, y = saaty_preference_matrix.shape 
            n = len(self.df_original.columns.values) -1
            if False in saaty_preference_matrix.iloc[:, :].isin(SAATY_SCALE).values or x != y or y != n:
                raise ValueError("Value not in Saaty Scale os wrong dimentions in matrix")
            else:
                for i in range(x):
                    for j in range(y):
                        if saaty_preference_matrix.iloc[i, j] == 1/saaty_preference_matrix.iloc[j, i] \
                           or saaty_preference_matrix.iloc[j, i] == 1/saaty_preference_matrix.iloc[i, j] \
                           or (saaty_preference_matrix.iloc[j, i] == 1 and i == j): 
                            pass
                        else:
                            raise ValueError("Incoherent values of preferences", saaty_preference_matrix.iloc[i, j], )
        return True

    def pretty_original(self, tablefmt='psql'):
        return tabulate(self.df_original, headers='keys', tablefmt=tablefmt)

    def pretty_normalized(self, tablefmt='psql'):
        return tabulate(self.df_normalized, headers='keys', tablefmt=tablefmt)

    def pretty_weighted(self, tablefmt='psql'):
        return tabulate(self.df_weighted, headers='keys', tablefmt=tablefmt)

    def pretty_Xis(self, tablefmt='psql'):
        return tabulate(pd.DataFrame(self.df_pis, columns=['PIS']).join(pd.DataFrame(self.df_nis, columns=["NIS"])).T, headers='keys', tablefmt=tablefmt)
    
    def pretty_decision(self, tablefmt='psql'):
        return tabulate(self.df_decision, headers='keys', tablefmt=tablefmt)
        

