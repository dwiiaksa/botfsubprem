import os

from dotenv import load_dotenv

load_dotenv(".env")

API_ID = int(os.environ.get("API_ID", "24556370"))
API_HASH = os.environ.get("API_HASH", "a3a701690d9c5f20b45fc063d475c21f")
BOT_TOKEN = os.environ.get("BOT_TOKEN", "6793568039:AAHcESFGEhS03wvIrY_4lyDtytIJPU8YKVI")
LOGS_MAKER_BOT = int(os.environ.get("LOGS_MAKER_BOT", "-1002080346445"))
MONGO_URL = os.environ.get("MONGO_URL", "mongodb+srv://Fsubprem:kESK5q156Ccb1tH7@cluster0.ppu2oiz.mongodb.net/?retryWrites=true&w=majority")
OWNER_ID = int(os.environ.get("OWNER_ID", "1768030466"))
