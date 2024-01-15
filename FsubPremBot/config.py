import os

from dotenv import load_dotenv

load_dotenv(".env")

API_ID = int(os.environ.get("API_ID", "9774346"))
API_HASH = os.environ.get("API_HASH", "a92aed7d74654a563af4b07efbcd88e9")
BOT_TOKEN = os.environ.get("BOT_TOKEN", "6246079632:AAGuHanpE6Q-rbgPsFOiHfFyeZvElc8Cnz4")
LOGS_MAKER_BOT = int(os.environ.get("LOGS_MAKER_BOT", "-1001617596145"))
MONGO_URL = os.environ.get("MONGO_URL", "mongodb+srv://pss:Rextor99@cluster0.ifynkre.mongodb.net/?retryWrites=true&w=majority")
OWNER_ID = int(os.environ.get("OWNER_ID", "968410597"))
