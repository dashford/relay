from src.subscribers.wsdcgq12lm import WSDCGQ12LM


class Factory:

    @staticmethod
    def create_subscriber(type, logger):
        if type == 'WSDCGQ12LM':
            return WSDCGQ12LM(logger=logger)
