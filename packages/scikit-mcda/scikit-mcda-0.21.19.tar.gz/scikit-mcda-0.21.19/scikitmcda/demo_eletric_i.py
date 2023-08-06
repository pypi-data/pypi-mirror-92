from electre_i import *
from constants import MAX, MIN, LinearMinMax_, LinearMax_, LinearSum_, Vector_, EnhancedAccuracy_, Logarithmic_ 

def main():

    print("######### ELECTRE_I ############")

    print("\n@ Defining labels for Alternatives and Criteria")
    print("-------------------------------------------------")
    
    help(ELECTRE_I)
    
    electre_i = ELECTRE_I()

    electre_i.dataframe([[2,  8,  4,  4,  4],
                         [5,  7,  7,  7,  7],
                         [3,  2,  1,  2,  2],
                         [1,  2,  3,  1,  1],
                         [7,  6,  5,  5,  5]],
                        ["Alice", "Bruna", "Carlos", "Daniel", "Ester"],
                        ["Experiência Profissional", "Carisma", "Conhecimento Técnico", "Expressão Escrita", "Expressão Oral"]
                        )
    print(electre_i.pretty_original())

    electre_i.set_weights_manually([2, 1, 3, 2, 2], True)
    # waspas.set_weights_by_entropy()
    # waspas.set_weights_by_ranking_B_POW(0)
    
                                            # C1   C2     C3   C4 
    # w_AHP = electre_i.set_weights_by_AHP([[  1,    4,    5,   7],   # C1
    #                                       [1/4,    1,    3,   5],   # C2
    #                                       [1/5,  1/3,    1,   3],   # C3
    #                                       [1/7,  1/5,  1/3,   1]])  # C4
    # print("AHP Returned:\n", w_AHP)
    electre_i.set_signals([MAX, MAX, MAX, MAX, MAX])

    electre_i.decide()
    print("WEIGHTS:\n", electre_i.weights)
    print("NORMALIZED:\n", electre_i.pretty_normalized())
    print("CONCORDANCE MATRIX:\n", electre_i.pretty_concordance_matrix())
    print("DISCORDANCE MATRIX:\n", electre_i.pretty_discordance_matrix())
    print("CREDIBILITY MATRIX ELECTRE_I:\n", electre_i.pretty_credibility_matrix())
    print("OUTRANKING ELECTRE_I:\n", electre_i.pretty_decision())

    # electre_i.decide(Vector_)
    # print("RANKING ELECTRE_I with", electre_i.normalization_method, ":\n", electre_i.pretty_decision())

main()