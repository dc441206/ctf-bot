# myCTF-Discord Bot

## Introduction

This is a bot for running jeopardy type CTFs on discord servers.
At this moment it provides set of challenges.
Challenges can be freely discuss on the server, as there are no scoring system in place.
If Challenge is solved, bot will move to next challenge.

## Requirements
Bot requires to run Python3 and pip installed on the host machine

## Installation

1. Clone Repository:

   To clone repository, you need to run command:

    `git clone https://github.com/dc441206/ctf-bot.git`

2. Create virtual environment and install dependencies
    
   Navigate to the source code directory, and to create virtual environment in Python, you need to execute command:

   `python3 -m venv bot-venv`.

   then install dependencies for the bot with command:

   `./bot-venv/bin/pip install -r requirements.txt` 

3. Register bot as discord app 

   You need to navigate to this page https://discord.com/developers/applications/ then create new application, and configure your bot details there

4. Configure the bot

   Bot configuration is in `.env` file, it should look like that

    >token=your_bot_app_token
    
    Token contains discord bot token that you should obtain after you register it in step 3 
     
    >allowedchannel=general
 
     Allowed channel is a channel where bot accepts commands. It is used to restrict bot activity to a single channel. It takes channel name as a value. 

    >allowedguild=your_guild
   
    Due current limitations, bot can be deployed only to a single server. So use this property to restrict bot activity to a single server. It takes server name as a value.  

## Prepare challenges
Challenges are stored in `ctf.py` file under property `CHALLENGES`. It is a list of challenges.

Each challenge is a dictionary with 2 compulsory and one optional fields.

    `challenge` - contains text of the challenge
    `resource` - it is optional field, it is used if challenge requires additional resource file
    `solution` - Expected solution to the puzzle, bear in mind it requires exact text, and it is case sensitive
## Run bot
To run bot, run command `bot-venv/bin/python3 main.py`






