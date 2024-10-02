import os

from dotenv import load_dotenv

load_dotenv()

DB_PATH = os.environ.get('DB_PATH', './.cache/CIS.db')
DISCORD_TOKEN = os.environ['DISCORD_TOKEN']
