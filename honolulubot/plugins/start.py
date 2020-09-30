from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from honolulubot import honolulubot

text = """
Hello [{firstname}](tg://user?id={userid})
My name is Honolulu, I was made give users like you lewdful images from different sources with tags given to give you pleasure UwU
"""
@honolulubot.on_message(filters.command("start"))
async def alive(_, message):
    buttons = [[InlineKeyboardButton('Search Yande.re', switch_inline_query_current_chat = 'yandere '),
                InlineKeyboardButton('Search Kanachan', switch_inline_query_current_chat = 'kanachan '),
                InlineKeyboardButton('Search Danbooru', switch_inline_query_current_chat = 'danbooru ')
                ]]
    await message.reply(text.format(firstname=message.from_user.first_name,
                                    userid=message.from_user.id),
                        reply_markup=InlineKeyboardMarkup(buttons))
