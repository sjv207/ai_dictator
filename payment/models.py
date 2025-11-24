from otree.api import models, widgets, BaseConstants, BaseGroup, BasePlayer, BaseSubsession
import logging

logger = logging.getLogger(__name__)
author = 'Scott Vincent'


def make_field(label):
    return models.IntegerField(label=label, choices=C.LIKERT9, widget=widgets.RadioSelect)


class C(BaseConstants):
    NAME_IN_URL = 'payment'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1
    LIKERT9 = [[i + 1, ""] for i in range(9)]
    AI_TOOLS = [
        dict(name='ai_tools_None', label='None'),
        dict(name='ai_tools_ChatGPT', label='ChatGPT'),
        dict(name='ai_tools_DallE', label='Dall-E'),
        dict(name='ai_tools_OpenAI', label='OpenAI\'s playground (e.g. DaVinci, Currie, Ada)'),
        dict(name='ai_tools_StableDiffusion', label='Stable Diffusion'),
        dict(name='ai_tools_NightCafe', label='NightCafe'),
        dict(name='ai_tools_Jasper', label='Jasper'),
        dict(name='ai_tools_BingChat', label='Microsoft Bing Chat'),
        dict(name='ai_tools_GoogleBard', label='Google Bard'),
        dict(name='ai_tools_YouCom', label='You.com'),
        dict(name='ai_tools_Midjourney', label='Midjourney'),
        dict(name='ai_tools_Other', label='Other',),
    ]
    AI_CATEGORIES = [
        dict(name='ai_catagories_None', label='None'),
        dict(name='ai_catagories_Text', label='Text'),
        dict(name='ai_catagories_Image', label='Image'),
        dict(name='ai_catagories_Audio', label='Audio'),
        dict(name='ai_catagories_Music', label='Music'),
        dict(name='ai_catagories_Video', label='Video'),
    ]


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    creative = make_field("How creative do you consider yourself?")
    creative_job = make_field("How much creativity is required in your job?")
    comfort = make_field("How comfortable are you with new technologies?")
    technologies = make_field("How much (if at all) have you previously engaged with AI or similar technologies?")

    ai_tools_None = models.BooleanField(blank=True)
    ai_tools_ChatGPT = models.BooleanField(blank=True)
    ai_tools_DallE = models.BooleanField(blank=True)
    ai_tools_OpenAI = models.BooleanField(blank=True)
    ai_tools_StableDiffusion = models.BooleanField(blank=True)
    ai_tools_NightCafe = models.BooleanField(blank=True)
    ai_tools_Jasper = models.BooleanField(blank=True)
    ai_tools_BingChat = models.BooleanField(blank=True)
    ai_tools_GoogleBard = models.BooleanField(blank=True)
    ai_tools_YouCom = models.BooleanField(blank=True)
    ai_tools_Midjourney = models.BooleanField(blank=True)
    ai_tools_Other = models.BooleanField(blank=True)
    ai_tools_other_name = models.StringField(blank=True)

    ai_catagories_Text = models.BooleanField(blank=True)
    ai_catagories_Image = models.BooleanField(blank=True)
    ai_catagories_Audio = models.BooleanField(blank=True)
    ai_catagories_Music = models.BooleanField(blank=True)
    ai_catagories_Video = models.BooleanField(blank=True)
    ai_catagories_None = models.BooleanField(blank=True)

    gender = models.StringField(choices=['Female', 'Male', 'Prefer not to say', 'Other (please specify below)'],
                                label="What gender do you identify with?",
                                widget=widgets.RadioSelect)
    gender_other = models.StringField(label="Other gender", blank=True)
    age = models.IntegerField(label="What is your current age? (enter a number of years)", min=18, max=110)
    education = models.StringField(choices=["Less than A levels",
                                            "Vocational training",
                                            "A levels",
                                            "Undergraduate degree",
                                            "Postgraduate Master's degree",
                                            "Professional degree (e.g. MBA, JD)",
                                            "Doctorate",
                                            ],
                                   label="What is your highest level of education?",
                                   widget=widgets.RadioSelect)
    employment = models.StringField(choices=['Employed full time',
                                             'Employed part time',
                                             'Unemployed looking for work',
                                             'Unemployed not looking for work',
                                             'Retired',
                                             'Student',
                                             'Disabled',
                                             ],
                                    label="What is your current employment status?",
                                    widget=widgets.RadioSelect)
    job_title = models.StringField(label="What is your current job title?")
    income = models.StringField(choices=['Less than £10,000',
                                         '£10,000-£24,999',
                                         '£25,000-£49,999',
                                         '£50,000-£74,999',
                                         '£75,000-£99,999',
                                         '£100,000-£124,999',
                                         '£125,000-£149,999',
                                         'More than £150,00',
                                         ],
                                label="What is your current annual income?",
                                widget=widgets.RadioSelect)
    comments = models.LongStringField(label="Do you have any additional comments about this survey?", blank=True)
