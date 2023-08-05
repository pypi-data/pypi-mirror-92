from dmuu import DMUU
import pprint
from tabulate import tabulate


def main():

    print("######### DMMU ############")

    print("\n@ Defining labels for Alternatives and States")
    print("-----------------------------------------------")
    
    dmuu = DMUU()


    dmuu.dataframe([[5000, 2000, 100],
                    [50, 50, 500]],
                   ["ALT_A", "ALT_B"],
                   ["STATE A", "STATE B", "STATE C"]
                   )
    print(dmuu.pretty_original())

    print("\n@ Specifying the criteria method")
    print("----------------------------------")
    dmuu.minimax_regret()
    print("\nCalc:\n")
    print(dmuu.pretty_calc())
    print("\nResult:\n")
    print(dmuu.pretty_decision())


    print("\n@ Many crietria methods")
    print("------------------------------")
    dmuu.decision_making([dmuu.maximax(), dmuu.maximin(), dmuu.hurwicz(0.8), dmuu.minimax_regret()])
    print("\nCalc:\n")
    print(dmuu.pretty_calc())
    print("\nResult:\n")
    print(dmuu.pretty_decision())

    dmuu.calc_clean()
    print("\nClean Calc:\n")
    print(dmuu.pretty_calc())

    print("Attributes:\n")
    print(vars(dmuu))

    print(dmuu.pretty_decision())

main()