from random import randint
import random
from otree.api import *

from common.common_data import AUTO_CONDITIONS
from .models import Player, WaitPage, C
import time
import logging

logger = logging.getLogger(__name__)


# Just using this page to load the participant params that are set in the consent app
class LoaderWait(WaitPage):
    @staticmethod
    def app_after_this_page(player: Player, upcoming_apps):
        logger.info("++++++++++++++++++++++++++++++++++++++")
        topic_index = 0
        player.participant.vars['topic'] = C.TOPICS[topic_index]
        player.participant.vars['story_start_t'] = int(time.time())
        player.participant.vars['state'] = "Playing"
        player.participant.vars['ai_idea0'] = ''
        player.participant.vars['ai_idea1'] = ''
        player.participant.vars['ai_idea2'] = ''
        player.participant.vars['ai_idea3'] = ''
        player.participant.vars['ai_idea4'] = ''
        player.participant.vars['condition'] = random.choice(AUTO_CONDITIONS)


page_sequence = [LoaderWait]
