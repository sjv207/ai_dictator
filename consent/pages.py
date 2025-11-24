from .models import Player, C
from otree.api import Page
import logging
import math


logger = logging.getLogger(__name__)


class Consent(Page):
    timeout_seconds = C.CONSENT_TIMEOUT
    form_model = 'player'
    form_fields = ['consent']

    @staticmethod
    def vars_for_template(player: Player):
        return {'consent_timeout_min': math.ceil(C.CONSENT_TIMEOUT / 60),
                'review_ref': player.session.config['review_ref']}

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        if timeout_happened:
            player.consent = False
            player.participant.vars['state'] = "Non-Consenting"
        else:
            player.consent = True
            player.participant.vars['state'] = "Playing"

    @staticmethod
    def app_after_this_page(player: Player, upcoming_apps):
        if player.participant.vars['state'] == "Non-Consenting":
            logger.info("Player did not consent")
            return upcoming_apps[-1]


class Overview(Page):
    form_model = 'player'
    form_fields = ['browser_type', 'screen_size']


page_sequence = [Consent, Overview]
