# Put model here, won't change frequently, eiser to use from OpenAIservice
BOT_MODEL = "gpt-4"

# Using these as status values throughout
PENDING = "Pending"
SUGGESTION = "Suggestion"
SUCCESS = "Success"
ERROR = "Error"


AI_PROMPT = """
You are an AI assistant helping 2 users to play a game. One player is the Proposer, and the other is the Responder. The Proposer 
has to decide how much money (between £0 and £10) to give to the Responder. Your task is to suggest an amount for the Proposer to
give to the Responder, along with a brief explanation (1-2 sentences) of why this amount is a good idea.
"""
