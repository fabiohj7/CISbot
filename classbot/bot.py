import asyncio
import os

import aiofiles
import discord

from . import config, database

bot_token = os.getenv('DISCORD_BOT_TOKEN')

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

users = database.get_users()


# Start the bot and load users to set
@client.event
async def on_ready():
    print(f"We have logged in as {client.user}")


@client.event
async def on_message(message: discord.Message):
    # Do not read bot's message
    if message.author == client.user:
        return

    if not isinstance(message.channel, discord.DMChannel):
        return

    author = str(message.author)

    # Check if users is on file if not add it
    if author not in users:
        database.add_users(author, message.content)
        print(f"Added {author} with message {message.content}")
        await message.channel.send("Adding your questions...")

        async aiofiles.open("./questions.md", "w")

    else:
        # Send this message if user already sent a message
        await message.channel.send("You have already sent your questions")


client.run(config.DISCORD_TOKEN)
