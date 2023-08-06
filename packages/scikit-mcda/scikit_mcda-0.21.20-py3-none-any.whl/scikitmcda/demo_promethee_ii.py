from promethee_II import *
from constants import MAX, MIN, LinearMinMax_, LinearMax_, LinearSum_, Vector_, EnhancedAccuracy_, Logarithmic_ 

def main():

    print("######### PROMETHEE_II ############")

    print("\n@ Defining labels for Alternatives and Criteria")
    print("-------------------------------------------------")
    
    promethee_ii = PROMETHEE_II()

    promethee_ii.dataframe([[250, 16, 12, 5],
                            [200, 16,  8, 3],
                            [300, 32, 16, 4],
                            [275, 32,  8, 2]],
                            ["Mobile 1", "Mobile 2", "Mobile 3", "Mobile 4"],
                            ["COST", "STORAGE", "CAMERA", "DESIGN"]
                            )
    print(promethee_ii.pretty_original())

    promethee_ii.set_weights_manually([0.35, 0.25, 0.25, 0.15])
    # promethee_ii.set_weights_by_entropy()
    # promethee_ii.set_weights_by_ranking_B_POW(0)
    
                                       # C1   C2     C3   C4 
#     w_AHP = promethee_ii.set_weights_by_AHP([[  1,    4,    5,   7],   # C1
#                                              [1/4,    1,    3,   5],   # C2
#                                              [1/5,  1/3,    1,   3],   # C3
#                                              [1/7,  1/5,  1/3,   1]])  # C4
#     print("AHP Returned:\n", w_AHP)
    promethee_ii.set_signals([MIN, MAX, MAX, MAX])

    promethee_ii.decide()
    print("WEIGHTS:\n", promethee_ii.weights)
    print("NORMALIZED:\n", promethee_ii.pretty_normalized())
    print("WEIGHTED:\n", promethee_ii.pretty_weighted())
    print("RANKING PROMETHEE_II with", promethee_ii.normalization_method , ":\n", promethee_ii.pretty_decision())

    promethee_ii.decide(Vector_)
    print("RANKING PROMETHEE_II with", promethee_ii.normalization_method, ":\n", promethee_ii.pretty_decision())

main()