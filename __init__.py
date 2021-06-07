from nonebot import *
from . import main

bot = get_bot()


@bot.on_message("group")
async def entranceFunction(context):
    msg = str(context["message"])
    userGroup = context["group_id"]
    await main.getMessage(bot, userGroup, msg)
