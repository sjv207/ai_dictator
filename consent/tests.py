from otree.api import *
from .pages import *
import logging

logger = logging.getLogger(__name__)


class PlayerBot(Bot):

    def play_round(self):

        yield Consent, dict(consent= False,)
        yield Overview, dict(browser_type='Type', screen_size='Size', overview_comp_q=2)

