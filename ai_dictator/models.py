from random import randint
import time
import logging
from otree.api import BaseConstants, BaseSubsession, BaseGroup, BasePlayer, models
import uuid
from common.OpenAIService import get_new_idea, get_queue_data
from common.common_data import ERROR, IDEA, PENDING

logger = logging.getLogger(__name__)
author = 'Scott Vincent'


class C(BaseConstants):
    NAME_IN_URL = 'dictai'
    PLAYERS_PER_GROUP = 2
    NUM_ROUNDS = 1
    ROLE_PROPOSER = 'Proposer'
    ROLE_RESPONDER = 'Responder'


class Subsession(BaseSubsession):
    pass


def group_by_arrival_time_method(subsession: Subsession, waiting_players):
    if len(waiting_players) >= 2:
        players = waiting_players[:2]
        players[0].my_role = C.ROLE_PROPOSER
        players[1].my_role = C.ROLE_RESPONDER

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


    # The topic this player wrote the story for, from C.TOPIC
    # NOTE: The initial value is only required when testing the story standalone
    topic_index = models.IntegerField(initial=0)
    story = models.LongStringField()
    # The time in seconds they took to create the story
    story_time_s = models.IntegerField()

    ai_idea0 = models.LongStringField(initial="")
    ai_idea1 = models.LongStringField(initial="")
    ai_idea2 = models.LongStringField(initial="")

    # The following are only required by the app for displaying messages such as timeouts
    ai_idea0_error = models.LongStringField(initial="")
    ai_idea1_error = models.LongStringField(initial="")
    ai_idea2_error = models.LongStringField(initial="")

    def generate_AI_idea(self, idea_index):
        field_name = f'ai_idea{idea_index}'
        idea_text = getattr(self, field_name)
        idea_error = getattr(self, field_name + "_error")

        # If we have an error message from the time before, delete it
        if len(idea_error) != 0:
            setattr(self, f"{field_name}_error", '')

        # If the user hit's F5, the button will be re-enabled and their fetch timer will be killed off.
        # However, they have a pending request, so don't get another, but allowing them to click the button
        # starts a new timer and they will then pick up the existing response when it comes back.
        if len(idea_text) == 0:
            # This method will kick the actual request off in a seperate process and run it async
            get_new_idea(self.id_in_group,
                         idea_index,
                         self.topic_index,
                         self.session.config['AI_timeout'],
                         self.session.config['use_canned_responses'])

    def get_AI_idea(self, idea_index, re_view: bool):

        # Take a quick look on the queues to see if there is anything waiting
        queue_data = get_queue_data()
        if len(queue_data) != 0:
            self.process_queue_data(queue_data)

        # Now process the request
        field_name = f'ai_idea{idea_index}'
        idea_text = getattr(self, field_name)
        idea_error = getattr(self, field_name + "_error")
        status = PENDING
        msg_text = ""

        if len(idea_error) != 0:
            status = ERROR
            msg_text = idea_error
        elif len(idea_text) != 0:
            status = IDEA
            msg_text = idea_text

        logger.info(f"Returning status: {status}")
        return status, msg_text

    def create_story(self):

        # Randomly select a topic
        self.topic_index = randint(0, len(C.TOPICS) - 1)
        # The following is used on screens only, not required otherwise
        self.participant.vars['topic'] = C.TOPICS[self.topic_index]

        # Use this as the time the player started story writing
        self.participant.vars['story_start_t'] = int(time.time())

        # We also need to create the off model Story object now, so we can hang snapshots,
        # ai suggestions, and ai suggestion switching objects off it
        self.story_id = str(uuid.uuid4())   # Don't want a UUID object, just the value
        self.participant.vars['story_id'] = self.story_id

    def process_queue_data(self, queue_data):
        group: Group = self.group
        # This method processes the queue data for any Player, not just self. To avoid excess lookups,
        # the data is grouped by player id
        for playerId, ideas in queue_data.items():

            player: Player = group.get_player_by_id(playerId)
            for idea in ideas:
                field_name = f"ai_idea{idea['ideaIndex']}"
                text = idea['text']
                if idea['status'] == ERROR:
                    setattr(player, f"{field_name}_error", text)
                else:
                    setattr(player, field_name, text)
                    # Cache it in the participant for use in the follow-up app
                    self.participant.vars[field_name] = text
