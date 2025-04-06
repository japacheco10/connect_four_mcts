class Globals():
    APP_NAME = "CONNECT 4 - MCTS"

    class Players():
        R = "R"
        Y = "Y"
        O = "O"

    class Algorithms():
        UR = "UR"  # Uniform Random
        PMCGS = "PMCGS"  # Pure Monte Carlo Game Search
        PMCGS_P = "PMCGS_P"  # Pure Monte Carlo Game Search Parallel
        UCT = "UCT"  # Upper Confidence bound for Trees
        UCT_P = "UCT_P"  # Upper Confidence bound for Trees Parallel

    class VerbosityLevels():
        VERBOSE = "VERBOSE"
        BRIEF = "BRIEF"
        NONE = "NONE"
        ERROR = "ERROR"
        
