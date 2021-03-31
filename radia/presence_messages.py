import random

PRESENCE_MESSAGES = [
    "!help to get started",
    # Signup!
    "Signup for Low Ink!",
    "Signup for Swim or Sink!",
    "Signup for Testing Grounds!",
    "Signup for Unnamed Tournament!",
    # funny
    "Powered by High Ink!",
    "Investing in buying LUTI.",
    "Get your coffee grounds 45% off this weekend at Testing Grounds.",
    "Sink or Swim or Swim or Sink",
    "According to all known laws of aviation",
    # Round 4
    "Round 4, here we go again!",
    "The real round 4 were the friends we made along the way.",
    # uwu stuff
    "Sprinkles!",
    "Wawa!",
    # Socials
    "Twitter: @IPLSplatoon",
    "Twitch: twitch.tv/IPLSplatoon",
    "Battlefy: battlefy.com/inkling-performance-labs",
    "Patreon: patreon.com/IPLSplatoon",
    "Github: github.com/IPL-Splat",
    "Youtube: youtube.com/channel/UCFRVQSUskcsB5NjjIZKkWTA",
    "Facebook: facebook.com/IPLSplatoon",
    # People-specific
    "Icon by Ozei!",
    "Ban Kraken Mare",
    "I kid you not Hoeen, he turns himself into a pickle",
    "Go to sleep Lepto",
    "Skye passed out again",
    "Helpdesk needs you .jpg",
]


def get_presence_message():
    return random.choice(PRESENCE_MESSAGES)
