from urllib.parse import unquote, urlparse
import re
from random import randint

from pyrogram.types import (
    InlineQueryResultArticle,
    InlineQueryResultPhoto,
    InputTextMessageContent,
    InlineKeyboardButton,
    InlineKeyboardMarkup
)

from honolulubot import honolulubot
from honolulubot.helpers.aiohttp import sauce

NEXT_OFFSET = 25
CACHE_TIME = 0

IMG = "https://telegra.ph/file/9712b3d6acea03a8f4c00.jpg"

DEFAULT_RESULTS = [
    InlineQueryResultArticle(
        title="About Honolulu",
        input_message_content=InputTextMessageContent(
            "**Konichiwa~**\nこんにちは、ホノルルです。ダンボロー、カナチャン、ヤンデレから集めたNSFW画像を提供しています。あなたはインライン機能を介して私を使用することができます:)",
        ),
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("Community", url="https://t.me/YorkTownEagleUnion"),
            InlineKeyboardButton("Creator", url="https://github.com/pokurt")],
            [InlineKeyboardButton('Yande.re', switch_inline_query_current_chat = 'yandere '),
            InlineKeyboardButton('Konachan', switch_inline_query_current_chat = 'konachan '),
            InlineKeyboardButton('Danbooru', switch_inline_query_current_chat = 'danbooru ')]]
        ),
        description="自分自身について",
        thumb_url=IMG,
    )
]


@honolulubot.on_inline_query()
async def inline(client, query):
    offset = int(query.offset or 0)
    results = []
    string = query.query.lower()
    if string == "":
        await query.answer(
            results=DEFAULT_RESULTS,
            cache_time=CACHE_TIME,
            switch_pm_text="How do I work",
            switch_pm_parameter="start",
        )

        return

    if string.split()[0] == "yandere":
        if len(string.split()) == 1:
            await client.answer_inline_query(query.id,
                                            results=results,
                                            switch_pm_text="Search for an image on Yande.re",
                                            switch_pm_parameter="start"
                                        )
            return
        tags = string.split(None, 1)[1].replace("#", '')
        counter = randint(1, 10)
        while_counter = 1
        while while_counter <= 50:
            while_counter += 1
            data = await sauce(tags, counter, url="https://yande.re/post.json?")
            counter += 1
            count = 0
            if len(data) == 0:
                break
            else:
                for item in data[offset: offset + NEXT_OFFSET]:
                    count += 1
                    if count % 50 == 0:
                        break
                    if "file_url" in item:
                        picture_url = item["file_url"]
                        text = f'**Post ID**: `{item["id"]}`\n'
                        text += f'**Author:** `{item["author"]}`\n'
                        text += f'**Score**: `{item["score"]}`'
                        buttons = [[InlineKeyboardButton('Source', url=f'https://yande.re/post/show/{item["id"]}')]]
                        results.append(InlineQueryResultPhoto(
                            photo_url=picture_url,
                            title=f'Result:{item["id"]}',
                            caption=text,
                            description=f"Tags Matched: #{tags}",
                            reply_markup=InlineKeyboardMarkup(buttons)))
            await client.answer_inline_query(query.id,
                                            results=results,
                                            is_gallery=True,
                                            cache_time=CACHE_TIME
                                            )

    elif string.split()[0] == "konachan":
        if len(string.split()) == 1:
            await client.answer_inline_query(query.id,
                                            results=results,
                                            switch_pm_text="Search for an image on Kanachan",
                                            switch_pm_parameter="start"
                                        )
            return
        tags = string.split(None, 1)[1].replace("#", '')
        counter = randint(1, 10)
        while_counter = 1
        while while_counter <= 50:
            while_counter += 1
            data = await sauce(tags, counter, url="https://konachan.com/post.json?")
            counter += 1
            count = 0
            if len(data) == 0:
                break
            else:
                for item in data[offset: offset + NEXT_OFFSET]:
                    count += 1
                    if count % 50 == 0:
                        break
                    if "file_url" in item:
                        picture_url = item["file_url"]
                        text = f'**Post ID**: `{item["id"]}`\n'
                        text += f'**Author:** `{item["author"]}`\n'
                        text += f'**Score**: `{item["score"]}`'
                        buttons = [[InlineKeyboardButton('Source', url=f'https://konachan.com/post/show/{item["id"]}')]]
                    results.append(InlineQueryResultPhoto(
                        photo_url=picture_url,
                        title=f'Result:{item["id"]}',
                        caption=text,
                        description=f"Tags Matched: #{tags}",
                        reply_markup=InlineKeyboardMarkup(buttons)))
            await client.answer_inline_query(query.id,
                                            results=results,
                                            is_gallery=True,
                                            cache_time=CACHE_TIME
                                        )
    elif string.split()[0] == "danbooru":
        if len(string.split()) == 1:
            await client.answer_inline_query(query.id,
                                            results=results,
                                            switch_pm_text="Search for an image on Danbooru",
                                            switch_pm_parameter="start"
                                        )
            return
        tags = string.split(None, 1)[1].replace("#", '')
        counter = randint(1, 10)
        while_counter = 1
        while while_counter <= 50:
            while_counter += 1
            data = await sauce(tags, counter, url="https://danbooru.donmai.us/posts.json?")
            counter += 1
            count = 0
            if len(data) == 0:
                break
            else:
                for item in data[offset: offset + NEXT_OFFSET]:
                    count += 1
                    if count % 50 == 0:
                        break
                    if "file_url" in item:
                        picture_url = item["file_url"]
                        text = f'**Post ID**: `{item["id"]}`\n'
                        text += f'**Author:** `{item["tag_string_artist"]}`\n'
                        text += f'**Score**: `{item["score"]}`'
                        buttons = [
                            [InlineKeyboardButton('Source', url=f'https://danbooru.donmai.us/posts/{item["id"]}'),
                            InlineKeyboardButton('Artist', url=f'https://danbooru.donmai.us/artists/{item["uploader_id"]}')]
                            ]
                        results.append(InlineQueryResultPhoto(
                            photo_url=picture_url,
                            title=f'Result:{item["id"]}',
                            caption=text,
                            description=f"Tags Matched: #{tags}",
                            reply_markup=InlineKeyboardMarkup(buttons)))
            await client.answer_inline_query(query.id,
                                            results=results,
                                            is_gallery=True,
                                            cache_time=CACHE_TIME
                                            )
    return