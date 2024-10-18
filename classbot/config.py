import os

from dotenv import load_dotenv

load_dotenv()

DB_PATH = os.environ.get('DB_PATH', './cisbot.db')
DISCORD_TOKEN = os.environ['DISCORD_TOKEN']

HELP_MESSAGE = '🤖 This is your CIS 340 Bot, I am here to help...\n' + '- ⏱️ `timeleft` to see the time left for the deadline\n' + '- 📤 `submit` after sending this command send your markdown formatted questions! (You are only able to submit once!)\n'
SUBMITTED_MESSAGE = 'Your questions have been submitted\n' + 'It may take up to 5 minutes to see a change but you can check out the questions here:\n' + 'https://fabiohj7.github.io/CISbot/'
