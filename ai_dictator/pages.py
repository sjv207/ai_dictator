from common.common_data import PENDING
from .models import Player, C, store_final_decision
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

    @staticmethod
    def live_method(player: Player, data):
        req_type = data['type']
        responses = []

        if req_type == "generate":
            index = data['index']
            logger.info(f"Going to fetch a new AI suggestion for player: {player.id}, for index: {index}")

            # Have we already requested a suggestion?
            prompt_name = f'ai_prompt_{index}'
            prompt_text = getattr(player, prompt_name)
            error_name = f'ai_suggestion_{index}_error'
            error_text = getattr(player, error_name)

            # A page refresh will cause the suggestion to be regenerated...
            if prompt_text != "" and error_text == "":
                logger.info("AI suggestion already exists, not generating a new one.")
                status, suggestion = player.get_AI_idea(index)
                response = {"status": status, "text": suggestion, "index": index}
                responses.append(response)
                return {player.id_in_group: {"responses": responses}}

            else:
                player.generate_AI_idea(index)
                response = {"status": PENDING, "text": "", "index": index}
                responses.append(response)

        elif req_type == "poll":
            # Only need to send back the indexes of the ideas that have content or errors
            logger.info(f"Polling for: {data['pendingIndexes']}")

            for pending_index in data['pendingIndexes']:
                status, text = player.get_AI_idea(pending_index)
                if status != PENDING:
                    response = {"status": status, "text": text, "index": pending_index}
                    responses.append(response)

            if len(responses) == 0:
                # Don't trouble the page if there is no data
                return

        # logger.info(f"Live return data: {responses}")
        return {player.id_in_group: {"responses": responses}}


class RespAi(Page):
    form_model = 'player'
    form_fields = ['expected_new_amount_to_receive', 'expected_will_change']

    @staticmethod
    def is_displayed(player: Player):
        return player.my_role == C.ROLE_RESPONDER


class PropWaitPage(WaitPage):
    after_all_players_arrive = store_final_decision


page_sequence = [
    GroupingWaitPage, IntroductionProp, IntroductionResp,
    PropAi, RespAi, PropWaitPage]
