from mcda import MCDA
from constants import MAX, MIN, LinearMinMax_, LinearMax_, LinearSum_, Vector_, EnhancedAccuracy_, Logarithmic_ 

def main():

    print("######### MCDA ############")

    print("\n@ Defining labels for Alternatives and Criteria")
    print("-------------------------------------------------")
    
    mcda = MCDA()

    mcda.dataframe([[250, 16, 12, 5],
                    [200, 16,  8, 3],
                    [300, 32, 16, 4],
                    [275, 32,  8, 4],
                    [225, 16,  16, 2]],
                   ["Mobile 1", "Mobile 2", "Mobile 3", "Mobile 4", "Mobile 5"],
                   ["COST", "STORAGE", "CAMERA", "DESIGN"]
                   )
    print(mcda.pretty_original())

    # mcda.set_weights_manually([0.5918, 0.2394, 0.1151, 0.0537])
    # mcda.set_weights_by_entropy()
    # mcda.set_weights_by_ranking_B_POW(0)
    
                                     # C1   C2     C3   C4 
    w_AHP = mcda.set_weights_by_AHP([[  1,    4,    5,   7],   # C1
                                     [1/4,    1,    3,   5],   # C2
                                     [1/5,  1/3,    1,   3],   # C3
                                     [1/7,  1/5,  1/3,   1]])  # C4
    print("AHP Returned:\n", w_AHP)
    mcda.set_signals([MIN, MAX, MAX, MAX])

    mcda.topsis()
    print("WEIGHTS:\n", mcda.weights)
    print("NORMALIZED:\n", mcda.pretty_normalized())
    print("WEIGHTED:\n", mcda.pretty_weighted())
    print("IDEAL SOLUTIONS:\n", mcda.pretty_Xis())
    print("RANKING TOPSIS with", mcda.normalization_method , ":\n", mcda.pretty_decision())

    mcda.topsis(LinearMinMax_)
    print("RANKING TOPSIS with", mcda.normalization_method, ":\n", mcda.pretty_decision())

    mcda.waspas(0.5, Vector_)
    print("RANKING WASPAS with", mcda.normalization_method, ":\n", mcda.pretty_decision())

main()