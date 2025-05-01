import json

# Tracks progress for the CTF
class ChallengeManager:
    currentTask = 0
    challenges = []

    # Instantiate object and loads challenges from file
    def __init__(self, filename):
        with open(filename) as f:
            self.challenges = json.load(f)


    def getCurrentTask(self):
        return self.challenges[self.currentTask]

    def incrementCounter(self):
        self.currentTask = self.currentTask + 1

    def hasMoreChallenges(self):
        return self.currentTask < len(self.challenges)

# Messages

NO_CHALLENGES = "No alien activities detected at this moment."

INIT_MESSAGE = """
Greetings brave earth defenders. Your planet is under great threat from outside space. Can you repel invaders and defend your planet?
  
"""

HELP_MESSAGE = """
This is a simple CTF Bot, it response to 3 commands:
- !help - shows this screen
- !challenge - shows details of current challenge
- !submit <solution> - accepts and evaluate submitted solution

Currently it does not keep the score, and it treats everyone on the channel as a single team.
Any further questions, please dm me
Have a fun!
"""