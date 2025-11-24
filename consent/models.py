from os import environ
import random
from otree.api import BaseConstants, BaseSubsession, BaseGroup, BasePlayer, models, widgets
import logging

logger = logging.getLogger(__name__)
author = 'Scott Vincent'


class C(BaseConstants):
    NAME_IN_URL = 'consent'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1
    CONSENT_TIMEOUT = int(environ.get('CONSENT_TIMEOUT', 120))  # This is in seconds


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    consent = models.BooleanField(widget=widgets.CheckboxInput, default=False, initial=False)

    browser_type = models.StringField(blank=True)
    screen_size = models.StringField(blank=True)
