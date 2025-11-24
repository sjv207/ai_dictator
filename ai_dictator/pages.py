from .models import Player, C
from otree.api import Page, WaitPage
import logging


logger = logging.getLogger(__name__)


class GroupingWaitPage(WaitPage):
    group_by_arrival_time = True
    body_text = "Waiting for another participant to join the game... Please be patient, and stay on this page."


class IntroductionProp(Page):
    form_model = 'player'
    form_fields = ['amount_to_give']

    @staticmethod
    def is_displayed(player: Player):
        return player.my_role == C.ROLE_PROPOSER


class IntroductionResp(Page):
    form_model = 'player'
    form_fields = ['expected_amount_to_receive']

    @staticmethod
    def is_displayed(player: Player):
        return player.my_role == C.ROLE_RESPONDER


class PropAi(Page):
    form_model = 'player'
    form_fields = ['revised_amount_to_give']

    @staticmethod
    def is_displayed(player: Player):
        return player.my_role == C.ROLE_PROPOSER


class RespAi(Page):
    form_model = 'player'
    form_fields = ['expected_new_amount_to_receive', 'expected_will_change']

    @staticmethod
    def is_displayed(player: Player):
        return player.my_role == C.ROLE_RESPONDER

page_sequence = [GroupingWaitPage, IntroductionProp, IntroductionResp, PropAi, RespAi]