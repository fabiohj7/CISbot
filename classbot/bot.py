import os
import subprocess
import time
from datetime import datetime, timedelta

import aiofiles
import discord

from . import config, database

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

questions_handler = {}

# Due date here
target_datetime = datetime(2024, 11, 25, 23, 30, 0)


# Start the bot and load users to set
@client.event
async def on_ready():
    print(f"We have logged in as {client.user}")


@client.event
async def on_message(message: discord.Message):
    # Do not read bot's message
    if message.author == client.user:
        return

    # Just use the DM channel
    if not isinstance(message.channel, discord.DMChannel):
        return

    author = str(message.author)
    content = message.content.lower().strip()

    section = database.get_section_by_user(author)
    print(section)

    # Add section
    if section == None:
        await message.channel.send(
            "I don't recognize you what, section are you?")
        await check_section(message)
        return

    # Get all the users
    users = database.get_users()
    if author in questions_handler and questions_handler[author]:
        await submission(message)
        questions_handler[author] = False
        return

    if content == 'help':
        await message.channel.send(config.HELP_MESSAGE)
        return
    elif content == 'timeleft':
        await timeleft(message)
        return

    elif content == 'submit':
        if author not in users:
            questions_handler[author] = True
            await message.channel.send("Submit your questions with a message: "
                                       )
            return
        else:
            await message.channel.send("You have already sent your questions")
            return

    # Send message if command not recognized
    await message.channel.send(
        "Hmm... I don't know what you are saying," +
        " use the `help` command to see the available commands")


async def submission(message: discord.Message):
    if message.author == client.user:
        return
    if not isinstance(message.channel, discord.DMChannel):
        return

    author = str(message.author)
    content = message.content.lower()

    database.add_users(author, content)
    print(f"Added {author} with message {content}")
    await message.channel.send("Adding your questions...")
    content = formatContent(message.content)
    print(content)
    async with aiofiles.open("./questions.md", "a") as file:
        await file.write(content + "\n")
    subprocess.run(["git", "add", "questions.md"])
    subprocess.run(["git", "commit", "-m", "Add questions"])
    subprocess.run(["git", "push", "origin", "main"])
    await message.channel.send(config.SUBMITTED_MESSAGE)


async def check_section(message):
    if message.author == client.user:
        return
    if not isinstance(message.channel, discord.DMChannel):
        return

    author = str(message.author)
    content = message.content
    content = content.lower().strip()
    if content != "section1" or content != "section2" and not tries:
        await message.channel.send("That section does not exist!")
        return

    database.add_section(author, content)


async def timeleft(message):

    now = datetime.now()
    time_remaining = target_datetime - now

    if time_remaining.total_seconds() > 0:
        days = time_remaining.days
        hours, remainder = divmod(time_remaining.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)

        await message.channel.send(
            f"Time left until deadline: `{days} days, {hours} hours, {minutes} minutes, {seconds} seconds`"
        )
    else:
        await message.channel.send("The deadline has passed 😭")


def formatContent(content):
    lines = content.split('\n')

    final = ''
    for line in lines:
        if line == '':
            continue
        if line[0] == '#':
            final += line + "\n"
            continue
        line = line.strip()
        line = line + "  \n"
        final += line

    return final


client.run(config.DISCORD_TOKEN)
