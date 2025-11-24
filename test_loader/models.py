from otree.api import *
import logging
from common.common_data import COMMON_TOPICS

logger = logging.getLogger('gossipModels')



class C(BaseConstants):
    NAME_IN_URL = 'test_loader'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1
    TOPICS = COMMON_TOPICS


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    pass
