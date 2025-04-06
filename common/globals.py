class Globals():
    APP_NAME = "CONNECT 4 - MCTS"

    class Players():
        R = "R"
        Y = "Y"
        O = "O"

    class Algorithms():
        UR = "UR"  # Uniform Random
        PMCGS = "PMCGS"  # Pure Monte Carlo Game Search
        UCT = "UCT"  # Upper Confidence bound for Trees
        UCTIMP = "UCTIMP" #UCT Improvement with column bias 
        UCTDEP = "UCTDEP" #UCT with depth bonus
        
    class VerbosityLevels():
        VERBOSE = "VERBOSE"
        BRIEF = "BRIEF"
        NONE = "NONE"
        ERROR = "ERROR"
        
