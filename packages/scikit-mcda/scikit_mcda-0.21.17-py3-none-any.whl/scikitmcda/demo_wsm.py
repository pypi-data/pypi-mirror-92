from wsm import *
from constants import MAX, MIN, LinearMinMax_, LinearMax_, LinearSum_, Vector_, EnhancedAccuracy_, Logarithmic_ 

def main():

    print("######### WSM ############")

    print("\n@ Defining labels for Alternatives and Criteria")
    print("-------------------------------------------------")
    
    wsm = WSM()

    wsm.dataframe([[250, 16, 12, 5],
                      [200, 16,  8, 3],
                      [300, 32, 16, 4],
                      [275, 32,  8, 4],
                      [225, 16,  16, 2]],
                     ["Mobile 1", "Mobile 2", "Mobile 3", "Mobile 4", "Mobile 5"],
                     ["COST", "STORAGE", "CAMERA", "DESIGN"]
                     )
    print(wsm.pretty_original())

    # waspas.set_weights_manually([0.5918, 0.2394, 0.1151, 0.0537])
    # waspas.set_weights_by_entropy()
    # waspas.set_weights_by_ranking_B_POW(0)
    
                                       # C1   C2     C3   C4 
    w_AHP = wsm.set_weights_by_AHP([[  1,    4,    5,   7],   # C1
                                       [1/4,    1,    3,   5],   # C2
                                       [1/5,  1/3,    1,   3],   # C3
                                       [1/7,  1/5,  1/3,   1]])  # C4
    print("AHP Returned:\n", w_AHP)
    wsm.set_signals([MIN, MAX, MAX, MAX])

    wsm.decide()
    print("WEIGHTS:\n", wsm.weights)
    print("NORMALIZED:\n", wsm.pretty_normalized())
    print("WEIGHTED:\n", wsm.pretty_weighted())
    print("RANKING WSM with", wsm.normalization_method , ":\n", wsm.pretty_decision())

    wsm.decide(Vector_)
    print("RANKING WSM with", wsm.normalization_method, ":\n", wsm.pretty_decision())

main()