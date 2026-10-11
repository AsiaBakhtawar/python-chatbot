"""
partner - A friendly student helper chatbot
Built with Python (no API key needed).

How it feels human:
- It picks a random reply from several options, so it doesn't repeat itself.
- It remembers your name and the last topic.
- It notices feelings (stress, sadness) and responds kindly.
- It types its replies out letter by letter.
"""

import random
import re
import time
from datetime import datetime

BOT_NAME = "partner"
TYPING_EFFECT = True  # set to False if you want instant replies

JOKES = [
    "Why do programmers prefer dark mode? Because light attracts bugs!",
    "Why did the developer go broke? Because he used up all his cache.",
    "I would tell you a UDP joke, but you might not get it.",
    "There are 10 types of people: those who understand binary and those who don't.",
     "Why was the computer cold? It left its Windows open.",
]

# Each intent has regex patterns and several possible replies.
# {name} is replaced with the user's name.
INTENTS = [
    {
        "name": "greeting",
        "patterns": [r"\b(hi|hello|hey|salam|assalam)\b"],
        "responses": [
            "Hey {name}! Good to see you. What's on your mind?",
            "Hello {name}! How can I help you today?",
            "Hi {name}! Ready to work on your goals?",
        ],
    },
    {
        "name": "how_are_you",
        "patterns": [r"how are you", r"how r u", r"kaise ho", r"kese ho"],
        "responses": [
            "I'm doing great, thanks for asking! How about you, {name}?",
            "All good here! I'm always happy to chat. How are you?",
        ],
    },
    {
        "name": "feeling_low",
        "patterns": [r"\b(sad|stressed|stress|tired|anxious|worried|upset|overwhelmed)\b"],
        "responses": [
            "I'm sorry you're feeling that way, {name}. Take a deep breath. "
            "Maybe a short break or a walk could help.",
            "That sounds tough. Be kind to yourself, {name}. "
            "Talking to a friend or family member can really help too.",
        ],
    },
    {
        "name": "feeling_good",
        "patterns": [r"\b(happy|good|great|excited|fine|awesome)\b"],
        "responses": [
            "That's wonderful to hear, {name}!",
            "Love that energy! Let's make today productive.",
        ],
    },
    {
        "name": "internship",
        "patterns": [r"internship", r"intern\b", r"job"],
        "responses": [
            "For internships, try LinkedIn, Rozee.pk, and Wellfound. "
            "Keep your resume to one page and your GitHub active.",
            "A good start: build 2-3 small projects, put them on GitHub, "
            "and apply to a few places every week. Don't give up!",
        ],
    },
    {
        "name": "github",
        "patterns": [r"github", r"\bgit\b", r"repository", r"repo\b"],
        "responses": [
            "GitHub is where developers store and share code. "
            "A clean profile with projects really helps in applications.",
            "Tip: write a clear README for every project. "
            "It shows people what you built and how to run it.",
        ],
    },
    {
        "name": "python",
        "patterns": [r"python"],
        "responses": [
            "Python is a great language to start with. "
            "Practice a little every day and build small projects.",
            "Nice choice! Try building small things: a to-do app, a quiz, or a bot like me.",
        ],
    },
    {
        "name": "thanks",
        "patterns": [r"\b(thanks|thank you|shukriya|thx)\b"],
        "responses": [
            "You're welcome, {name}!",
            "Anytime! Happy to help.",
            "No problem at all!",
        ],
    },
    {
        "name": "who_are_you",
        "patterns": [r"who are you", r"your name", r"what are you"],
        "responses": [
            "I'm " + BOT_NAME + ", a chatbot made in Python. I'm still learning!",
        ],
    },
]

FALLBACKS = [
    "Hmm, I'm not sure about that yet. Can you say it another way?",
    "I didn't quite get that. Try asking about internships, GitHub, or Python.",
    "That's interesting! I'm still learning, so I can't answer that one yet.",
]


def say(text):
    """Print the bot's reply, with an optional typing effect."""
    print(f"{BOT_NAME}: ", end="")
    if TYPING_EFFECT:
        for char in text:
            print(char, end="", flush=True)
            time.sleep(0.015)
        print()
    else:
        print(text)


def get_reply(user_text, state):
    """Find the best reply for the user's message."""
    text = user_text.lower().strip()

    if not text:
        return "I'm listening... say something!"

    # Special commands
    if re.search(r"\bjoke\b", text) or (
        "another" in text and state["last"] == "joke"
    ):
        state["last"] = "joke"
        return random.choice(JOKES)

    if re.search(r"\btime\b", text):
        state["last"] = "time"
        return "It's " + datetime.now().strftime("%I:%M %p") + " right now."

    if re.search(r"\bdate\b|\btoday\b", text):
        state["last"] = "date"
        return "Today is " + datetime.now().strftime("%A, %d %B %Y") + "."

    # Check each intent's patterns
    for intent in INTENTS:
        for pattern in intent["patterns"]:
            if re.search(pattern, text):
                state["last"] = intent["name"]
                reply = random.choice(intent["responses"])
                return reply.format(name=state["name"])

    state["last"] = None
    return random.choice(FALLBACKS)


def main():
    print(f"=== {BOT_NAME}: Student Helper Bot ===")
    say("Hi! I'm " + BOT_NAME + ". What's your name?")
    name = input("You: ").strip().title() or "Friend"
    state = {"name": name, "last": None}

    say(f"Nice to meet you, {name}! You can chat with me, ask for a joke, "
        "or ask about internships. Type 'bye' to exit.")

    while True:
        user_text = input(f"{name}: ")

        if re.search(r"\b(bye|quit|exit|goodbye|allah hafiz)\b", user_text.lower()):
            say(f"Goodbye {name}! Best of luck with your internship search.")
            break

        say(get_reply(user_text, state))


if __name__ == "__main__":
    main()
