import logging
from otree.api import BaseConstants, BaseSubsession, BaseGroup, BasePlayer, models
from common.OpenAIService import get_new_idea, get_queue_data
from common.common_data import AI_PROMPT, ERROR, SUGGESTION, PENDING

logger = logging.getLogger(__name__)
author = 'Scott Vincent'


class C(BaseConstants):
    NAME_IN_URL = 'dictai'
    PLAYERS_PER_GROUP = 2
    NUM_ROUNDS = 1
    ROLE_PROPOSER = 'Proposer'
    ROLE_RESPONDER = 'Responder'
    AI_PROMPT = AI_PROMPT


class Subsession(BaseSubsession):
    pass


def group_by_arrival_time_method(subsession: Subsession, waiting_players):
    if len(waiting_players) >= 2:
        players = waiting_players[:2]

        players[0].my_role = C.ROLE_PROPOSER
        players[1].my_role = C.ROLE_RESPONDER

        # TODO This is for debug only, this needs setting properly in session start
        players[0].participant.label = f"P-{players[0].id}"
        players[1].participant.label = f"P-{players[1].id}"

        return players


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    my_role = models.StringField()
    amount_to_give = models.CurrencyField(min=0, max=10,
                                          label="How much do you want to give to the other participant? (It can be any value "
                                                "between £0.00 and £10.00)")
    revised_amount_to_give = models.CurrencyField(min=0, max=10,
                                                  label="After seeing the AI's suggestion, how much do you want to give to the other "
                                                  "participant? (It can be any value between £0.00 and £10.00)")

    expected_amount_to_receive = models.CurrencyField(min=0, max=10,
                                                      label="How much do you expect to receive from the other participant? (It can be any"
                                                      " value between £0.00 and £10.00)")
    expected_will_change = models.BooleanField(
        label="Do you think the other participant will change the amount they give to you based on the AI's suggestion?",
        choices=[
            [True, "Yes"],
            [False, "No"],
        ])
    expected_new_amount_to_receive = models.CurrencyField(min=0, max=10,
                                                          label="After seeing the AI's suggestion, how much do you expect to receive "
                                                          "from the other participant? (It can be any value between £0.00 and £10.00)")

    ai_prompt_0 = models.LongStringField(initial="")
    ai_suggestion_0 = models.LongStringField(initial="")
    # The following is only required by the app for displaying messages such as timeouts
    ai_suggestion_0_error = models.LongStringField(initial="")

    def generate_AI_idea(self, idea_index):
        error_name = f'ai_suggestion_{idea_index}'
        idea_error = getattr(self, error_name + "_error")

        # If we have an error message from the time before, delete it
        if len(idea_error) != 0:
            setattr(self, f"{error_name}_error", '')

        # Store the prompt
        prompt_name = f'ai_prompt_{idea_index}'
        setattr(self, prompt_name, C.AI_PROMPT)

        # This method will kick the actual request off in a seperate process and run it async
        get_new_idea(self.participant.label or self.participant.code,
                     idea_index,
                     C.AI_PROMPT,
                     self.session.config['AI_timeout'],
                     self.session.config['use_canned_responses'])

    def get_AI_idea(self, idea_index: int):

        # Take a quick look on the queues to see if there is anything waiting
        queue_data = get_queue_data()
        if len(queue_data) != 0:
            self.process_queue_data(queue_data)

        # Now process the request
        field_name = f'ai_suggestion_{idea_index}'
        idea_text = getattr(self, field_name)
        idea_error = getattr(self, field_name + "_error")
        status = PENDING
        msg_text = ""

        if len(idea_error) != 0:
            status = ERROR
            msg_text = idea_error
        elif len(idea_text) != 0:
            status = SUGGESTION
            msg_text = idea_text

        logger.info(f"Returning status: {status}")
        return status, msg_text

    def process_queue_data(self, queue_data):

        # This method processes the queue data for any Player, not just self. To avoid excess lookups,
        # the data is grouped by player id
        for playerId, ideas in queue_data.items():

            player: Player = self.get_player_by_label(playerId)
            if player is None:
                logger.error(f"Could not find player with id: {playerId} to process AI ideas")
                continue

            for idea in ideas:
                field_name = f"ai_suggestion_{idea['index']}"
                text = idea['suggestion']
                if idea['status'] == ERROR:
                    setattr(player, f"{field_name}_error", text)
                else:
                    setattr(player, field_name, text)

    def get_player_by_label(self, label):
        for player in self.subsession.get_players():
            if player.participant.label == label:
                return player
        return None
