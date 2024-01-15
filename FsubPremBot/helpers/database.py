from datetime import datetime, timedelta

from motor.motor_asyncio import AsyncIOMotorClient
from pytz import timezone

from FsubPremBot.config import MONGO_URL

# Initialize MongoDB client
mongo_client = AsyncIOMotorClient(MONGO_URL)
mongodb = mongo_client.fsubpremiumbot

# Initialize collections
botdb = mongodb.bot
user = mongodb.premium
resell = mongodb.seller
varsdb = mongodb.vars
userdb = mongodb.served
expiredDb = mongodb.expired


# Bot functions
async def add_bot(bot_id, api_id, api_hash, bot_token):
    await botdb.update_one(
        {"bot_id": bot_id},
        {
            "$set": {
                "api_id": api_id,
                "api_hash": api_hash,
                "bot_token": bot_token,
            }
        },
        upsert=True,
    )


async def get_bots():
    data = []
    async for bot in botdb.find({"bot_id": {"$exists": 1}}):
        data.append(
            dict(
                name=str(bot["bot_id"]),
                api_id=bot["api_id"],
                api_hash=bot["api_hash"],
                bot_token=bot["bot_token"],
            )
        )
    return data


async def remove_bot(bot_id):
    await botdb.delete_one({"bot_id": bot_id})


# Premium functions
async def get_premium():
    prem = await user.find_one({"prem": "prem"})
    return prem.get("list") if prem else []


async def add_premium(user_id):
    premium_list = await get_premium()
    premium_list.append(user_id)
    await user.update_one(
        {"prem": "prem"}, {"$set": {"list": premium_list}}, upsert=True
    )


async def remove_premium(user_id):
    premium_list = await get_premium()
    premium_list.remove(user_id)
    await user.update_one(
        {"prem": "prem"}, {"$set": {"list": premium_list}}, upsert=True
    )


async def remove_all_premium():
    await user.update_one({"prem": "prem"}, {"$set": {"list": []}})


# Reseller functions
async def get_seller():
    seller = await resell.find_one({"seller": "seller"})
    return seller.get("reseller") if seller else []


async def add_seller(user_id):
    reseller_list = await get_seller()
    reseller_list.append(user_id)
    await resell.update_one(
        {"seller": "seller"}, {"$set": {"reseller": reseller_list}}, upsert=True
    )


async def remove_seller(user_id):
    reseller_list = await get_seller()
    reseller_list.remove(user_id)
    await resell.update_one(
        {"seller": "seller"}, {"$set": {"reseller": reseller_list}}, upsert=True
    )


async def remove_all_seller():
    await resell.update_one({"seller": "seller"}, {"$set": {"reseller": []}})


# Vars functions
async def set_vars(bot_id, vars_name, value):
    update_data = {"$set": {f"vars.{vars_name}": value}}
    await varsdb.update_one({"_id": bot_id}, update_data, upsert=True)


async def get_vars(bot_id, vars_name):
    result = await varsdb.find_one({"_id": bot_id})
    return result.get("vars").get(vars_name) if result else None


async def remove_all_vars(bot_id):
    await varsdb.delete_one({"_id": bot_id})


async def all_vars(user_id):
    result = await varsdb.find_one({"_id": user_id})
    return result.get("vars") if result else None


# Served user functions
async def get_served_user(bot_id):
    served = await userdb.find_one({"user": bot_id})
    return served.get("list") if served else []


async def add_served_user(bot_id, user_id):
    served_list = await get_served_user(bot_id)
    served_list.append(user_id)
    await userdb.update_one(
        {"user": bot_id}, {"$set": {"list": served_list}}, upsert=True
    )


async def remove_served_user(bot_id, user_id):
    served_list = await get_served_user(bot_id)
    served_list.remove(user_id)
    await userdb.update_one(
        {"user": bot_id}, {"$set": {"list": served_list}}, upsert=True
    )


async def remove_all_user(bot_id):
    await userdb.update_one({"user": bot_id}, {"$set": {"list": []}})


# Expired functions
async def get_expired_date(bot_id):
    user = await expiredDb.find_one({"_id": bot_id})
    return user.get("expire_date") if user else None


async def set_expired_date(bot_id, expire_date):
    await expiredDb.update_one(
        {"_id": bot_id}, {"$set": {"expire_date": expire_date}}, upsert=True
    )


async def rem_expired_date(bot_id):
    await expiredDb.delete_one({"_id": bot_id})


async def add_exp_bot(bot_id, exp=30):
    have_exp = await get_expired_date(bot_id)
    now = datetime.now(timezone("Asia/Jakarta")) if not have_exp else have_exp
    expire_date = now + timedelta(days=exp)
    await set_expired_date(int(bot_id), expire_date)


async def add_vars_bot(bot_id, fsub_id, post_id, owner_id):
    await set_vars(int(bot_id), "CHANNEL_FSUB_ID", int(fsub_id))
    await set_vars(int(bot_id), "CHANNEL_POST_ID", int(post_id))
    await set_vars(int(bot_id), "OWNER_ID", int(owner_id))
