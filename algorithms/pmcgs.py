from algorithms import Base
from common.game_interface import GameInterface
from common.globals import Globals

class PureMonteCarloGameSearch(Base):
    def choose_move(self, game: GameInterface, player,  verbosity=Globals.VerbosityLevels.NONE, simulations=0):
        # Implement PMCGS algorithm logic here
        return 1  # placeholder