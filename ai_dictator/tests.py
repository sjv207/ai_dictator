from otree.api import Bot
from .pages import TenWords, StoryT
from .models import C
import logging

logger = logging.getLogger(__name__)


class PlayerBot(Bot):

    def play_round(self):
        yield TenWords, dict(word1="Sun",
                             word2="Sun",
                             word3="Sun",
                             word4="Sun",
                             word5="Sun",
                             word6="Sun",
                             word7="Sun",
                             word8="Sun",
                             word9="Sun",
                             word10="Sun",
                             )
        yield StoryT, dict(story="This is a story about a great big fat Pirate. He had 4 legs, and a ship made of solid gold"
                           "- he was more of a submariner than a surface pirate really. If only he'd made the ship out of wood,"
                           "not only would it have floated, but it would have moved too. So there he was, sat on the bottom of "
                           "ocean, with no passing ships to plunder. Until one day, whilst he was polishing his big shiny canon,"
                           " a squid swam past with a shipwreck in its ten tickles. Oi, said the BFP, where did you get that, is there any left?"
                           "Ha, said the squid, if you hadn't made your stupid boat out of gold, you could have had this easy!"
                           "Go pull your fingers, shouted the pirate, and got back to his polishing.")

        # Identifiable test data, don't need to make a GPT request. This is needed further down the line
        if self.player.participant.condition == C.CONDITIONS[1]:
            self.player.participant.vars['ai_idea0'] = "AI 0 Idea"

        elif self.player.participant.condition == C.CONDITIONS[2]:
            self.player.participant.vars['ai_idea0'] = "AI 0 Idea"
            self.player.participant.vars['ai_idea1'] = "AI 1 Idea"
            self.player.participant.vars['ai_idea2'] = "AI 2 Idea"
            self.player.participant.vars['ai_idea3'] = "AI 3 Idea"
            self.player.participant.vars['ai_idea4'] = "AI 4 Idea"
