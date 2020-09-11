import os
from dotenv import load_dotenv
from bot import Bot

if __name__ == "__main__":
    load_dotenv()
    token = os.getenv("DISCORD_BOT_TOKEN")

    bot = Bot()
    bot.run(token)
