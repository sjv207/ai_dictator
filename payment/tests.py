from otree.api import *
from .pages import *
import logging

logger = logging.getLogger(__name__)


class PlayerBot(Bot):

    def play_round(self):

        if self.player.participant.vars['state'] == "Non-Consenting":
            yield ConsentDropout
        yield Me, dict(creative=2,
                        creative_job=2,
                        comfort=2,
                        technologies=2,
                        ai_tools_None='ai_tools_None',
                        ai_tools_other_name='None',
                        ai_catagories_None='ai_catagories_None')

        yield Demographics, dict(gender="Male",
                                    gender_other=None,
                                    age=25,
                                    education="A levels",
                                    employment='Employed full time',
                                    job_title='The guv',
                                    income='Less than £10,000',
                                    )        

        # yield Finally

