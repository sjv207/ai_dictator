from .models import Player, C
from otree.api import Page
import logging


logger = logging.getLogger(__name__)


class ConsentDropout(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.participant.vars['state'] == "Non-Consenting"


class Me(Page):
    form_model = 'player'

    @staticmethod
    def get_form_fields(player: Player):
        ai_tools = [tool['name'] for tool in C.AI_TOOLS]
        ai_cats = [categories['name'] for categories in C.AI_CATEGORIES]
        return ['creative', 'creative_job', 'comfort', 'technologies', 'ai_tools_other_name', ] + ai_tools + ai_cats

    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == C.NUM_ROUNDS

    @staticmethod
    def error_message(player: Player, values):
        tools_count = 0
        cats_count = 0

        for tools in C.AI_TOOLS:
            if values[tools['name']]:
                tools_count += 1

        for cats in C.AI_CATEGORIES:
            if values[cats['name']]:
                cats_count += 1
        if tools_count == 0 or cats_count == 0:
            return "You must select at least 1 option from both AI tools, and from AI Categories"


class Demographics(Page):
    form_model = 'player'
    form_fields = [
        'gender',
        'gender_other',
        'age',
        'education',
        'employment',
        'job_title',
        'income',
        'comments',
    ]

    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == C.NUM_ROUNDS

    @staticmethod
    def error_message(player: Player, values):
        error_messages = dict()

        gender = values['gender']
        other = values['gender_other']
        logger.info(f"Checking other gender validity. Gender: {gender}, Other: {other}, len: {len(other)}")
        if gender == 'Other (please specify below)' and len(other) == 0:
            logger.info("Failed")
            error_messages['gender'] = "Please specify the Other gender here"
            return error_messages


class Finally(Page):
    pass


page_sequence = [ConsentDropout, Me, Demographics, Finally]
