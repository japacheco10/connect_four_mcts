import logging, traceback
from common.utils import Utils
from connect_4 import Connect4

logger = None

def main():
    try:
        logger.debug("Init Start")
        input_file, verbosity, iterations = Utils.validate_arguments()
        algorithm_name, current_player, board = Utils.load_game_settings(input_file)
        game = Connect4(algorithm_name, current_player, board, verbosity, iterations)
        logger.debug("Init End")
        logger.debug("Starting Game")
        game.run()
        logger.debug("Ending Game")
    except:
        logger.error("Uncaught exception: %s", traceback.format_exc())

if __name__ == "__main__":
    Utils.init()
    logger = logging.getLogger(__name__)
    main()
