import asyncio
import os

import aiofiles
import discord
from dotenv import load_dotenv

load_dotenv()

bot_token = os.getenv('DISCORD_BOT_TOKEN')

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

users = set()
file_path = "./users.txt"


# Loading users from the file
async def loadUsers():
    global users
    async with aiofiles.open(file_path, "r") as file:
        async for line in file:
            users.add(line)


# Start the bot and load users to set
@client.event
async def on_ready():
    print(f"We have logged in as {client.user}")
    await loadUsers()


@client.event
async def on_message(message: discord.Message):
    # Do not read bot's message
    if message.author == client.user:
        return

    author = str(message.author)

    # Check if users is on file if not add it
    if author not in users:
        users.add(author)
        await message.channel.send("Your questions have been added")
        # Write usernames to users files
        async with aiofiles.open(file_path, "w") as file:
            await file.write(author + "\n")
        # Write questions on questions file
        async with aiofiles.open("questions.md", "w") as file:
            await file.write(message.content)
    else:
        # Send this message if user already sent a message
        await message.channel.send("You have already sent your questions")


client.run(bot_token)
