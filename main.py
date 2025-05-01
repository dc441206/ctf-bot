import os
from logging.handlers import TimedRotatingFileHandler

import discord
import logging

import traceback
from discord.ext import commands
from dotenv import dotenv_values
import ctf

# Load configuration
#
config = dotenv_values(".env")

DISCORD_TOKEN = config.get("token")
allowedchannel = config.get("allowedchannel")
allowedguild = config.get("allowedguild")
challenges_path = config.get("challenges.path")
# Configure bot
#
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents, help_command=None)   # creates the bot without default help command, and prefix `!` for a command

# Instantiate and configure additional stuff
#
challengeMgr = ctf.ChallengeManager(challenges_path)
os.makedirs("./logs", exist_ok = True)                  # Creates log directory if necessary

handler = TimedRotatingFileHandler("./logs/bot.log",            # Configures time based log rotation handler, that rotates logs every day, and keeps files from last 5 days
                                   when="d",
                                   interval=1,
                                   backupCount=5)

logging.basicConfig(format='%(asctime)s ::: %(message)s', handlers= [handler])


# commands definition
#
@bot.command()
async def submit(ctx, arg):
    if not is_allowed(ctx):
        return
    if arg.isalnum() and challengeMgr.getCurrentTask()["solution"] == arg:
        logging.info(
            f"Submission succeeded - User {ctx.author} submitted correct answer to task {challengeMgr.getCurrentTask()}")
        challengeMgr.incrementCounter()
        message = "Congratulations, this is correct answer"
    else:
        logging.info(f"Invalid submission to task {challengeMgr.getCurrentTask()} - given answer is {arg}")
        message = "Sorry, you need to try again"
    await ctx.send(message)


@bot.command()
async def help(ctx):
    if not is_allowed(ctx):
        return
    await ctx.send(ctf.HELP_MESSAGE)


@bot.command()
async def challenge(ctx):
    if not is_allowed(ctx):
        return
    if not challengeMgr.hasMoreChallenges():
        await ctx.send(ctf.NO_CHALLENGES)
    else:
        msg = challengeMgr.getCurrentTask()["challenge"]
        res = challengeMgr.getCurrentTask().get("resource")
        if res:
            await send_attachement(ctx, msg, res)
        else:
            await ctx.send(msg)


# Error handlers
#
@submit.error
async def submit_error(ctx: commands.Context, error: commands.CommandError):
    log_helper(ctx, error)
    if not is_allowed(ctx):
        return
    await ctx.send("Sorry, you need to try again")


@challenge.error
async def challenge_error(ctx: commands.Context, error: commands.CommandError):
    log_helper(ctx, error)


@help.error
async def help_error(ctx: commands.Context, error: commands.CommandError):
    log_helper(ctx, error)


@bot.event
async def on_command_error(ctx: commands.Context, error: commands.CommandError):
    #check if command exist, and if does use dedicated error handler
    for c in bot.commands:
        if c.name == ctx.command:
            return
    log_helper(ctx, error)

# Helper commands
#
async def send_attachement(ctx, msg, filepath):
    with open(filepath, "rb") as f:
        f = discord.File(f)
        await ctx.send(msg, file=f)


def is_allowed(ctx):            # function that checks does incoming message originated in allowed server and channel, NOTE: DMs does not have guild or channel
    value = hasattr(ctx.guild, 'name') and \
            allowedguild == ctx.guild.name and \
            hasattr(ctx.channel, 'name') and \
            allowedchannel == ctx.channel.name
    if value:
        return True
    author, channel, guild = extract_sender_details(ctx)
    logging.warning(f"Unauthorized call to the command from {author}@{channel}:::{guild}")  # Logs unauthorised requests
    return False

def log_helper(ctx, error):
    author, channel, guild = extract_sender_details(ctx)
    logging.error(
        f"Received invalid payload from [{author}@{channel}:::{guild}] contains [{ctx.view.buffer}] which caused error {error}")


def extract_sender_details(ctx):
    author = getattr(ctx.author, 'name', 'nobody')
    channel = getattr(ctx.channel, 'name', 'prv-msg')
    guild = getattr(ctx.guild, 'name', 'prv-msg')
    return author, channel, guild


# Run bot
bot.run(DISCORD_TOKEN)
