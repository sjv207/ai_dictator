from os import environ


SESSION_CONFIGS = [
    dict(
        name='dictator',
        display_name="Full AI Dictator study",
        app_sequence=['ai_dictator', 'payment'],
        num_demo_participants=2,
        use_browser_bots=False,
    ),
]
ROOMS = [
    dict(
        name="ROOM1",
        display_name="Room1",
    ),
]

SESSION_CONFIG_DEFAULTS = dict(
    real_world_currency_per_point=1.00, participation_fee=3.00,
    use_canned_responses=True,
    AI_timeout=30.0,         # Seconds to wait for AI to respond
    review_ref="ABC-123",
    endowment=10.00
)

PARTICIPANT_FIELDS = []
SESSION_FIELDS = []

# ISO-639 code
# for example: de, fr, ja, ko, zh-hans
LANGUAGE_CODE = 'en'

# e.g. EUR, GBP, CNY, JPY
REAL_WORLD_CURRENCY_CODE = 'GBP'
USE_POINTS = False

ADMIN_USERNAME = 'admin'
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')

DEMO_PAGE_INTRO_HTML = """ """

SECRET_KEY = '7802915856047'
