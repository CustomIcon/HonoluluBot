import aiohttp
from urllib.parse import unquote, urlparse
import re
from random import randint

from pyrogram.types import (InlineQuery, InlineQueryResultArticle, InlineQueryResultPhoto, InputTextMessageContent,
                            InlineKeyboardButton, InlineKeyboardMarkup)

from honolulubot import honolulubot

NEXT_OFFSET = 25
CACHE_TIME = 0

IMG = "https://telegra.ph/file/9712b3d6acea03a8f4c00.jpg"



DEFAULT_RESULTS = [
    InlineQueryResultArticle(
        title="About Honolulu",
        input_message_content=InputTextMessageContent(
            f"**Konichiwa~**\nこんにちは、ホノルルです。ダンボロー、カナチャン、ヤンデレから集めたNSFW画像を提供しています。あなたはインライン機能を介して私を使用することができます:)",
        ),
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("Community", url="https://t.me/YorkTownEagleUnion"),
                    InlineKeyboardButton("Creator", url="https://github.com/pokurt")
                ],
                [
                    InlineKeyboardButton('Inline Help', url='https://t.me/honolulubot?start=start')
                ]
            ]
        ),
        description="自分自身について",
        thumb_url=IMG,
    )
]

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:70.0) Gecko/20100101 Firefox/70.0"}


@honolulubot.on_inline_query()
async def inline(client, query: InlineQuery):
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
        async with aiohttp.ClientSession(headers=headers) as session:
            counter = randint(1, 10)
            while_counter = 1
            while while_counter <= 50:
                while_counter += 1
                async with session.get(f"https://yande.re/post.json?", params={"tags": tags, "random": "true", "page": counter}) as response:
                    data = await response.json()
                    counter += 1
                    count = 0
                    if len(data) == 0:
                        break
                    else:
                        for item in data:
                            count += 1
                            if count % 50 == 0:
                                break
                            if "file_url" in item:
                                picture_url = item["file_url"]
                                picture_name = re.sub('[<>:"/|?*]', " ", unquote(urlparse(picture_url).path.split("/")[-1]))
                                text = f'**{picture_name}**\n'
                                text += f'**Tags Matched:** {tags}'
                                buttons = [[InlineKeyboardButton('Source', url=picture_url)]]
                                results.append(InlineQueryResultPhoto(
                                    photo_url=picture_url,
                                    title=f"Result:{picture_name}",
                                    caption=text,
                                    description=f"Tags Matched: #{tags}",
                                    reply_markup=InlineKeyboardMarkup(buttons)))
                    await client.answer_inline_query(query.id,
                                                    results=results,
                                                    is_gallery=True,
                                                    cache_time=CACHE_TIME
                                                    )

    elif string.split()[0] == "kanachan":
        if len(string.split()) == 1:
            await client.answer_inline_query(query.id,
                                            results=results,
                                            switch_pm_text="Search for an image on Kanachan",
                                            switch_pm_parameter="start"
                                        )
            return
        tags = string.split(None, 1)[1].replace("#", '')
        async with aiohttp.ClientSession(headers=headers) as session:
            counter = randint(1, 10)
            while_counter = 1
            while while_counter <= 50:
                while_counter += 1
                async with session.get(f"https://konachan.com/post.json?", params={"tags": tags, "random": "true", "page": counter}) as response:
                    data = await response.json()
                    counter += 1
                    count = 0
                    if len(data) == 0:
                        break
                    else:
                        for item in data:
                            count += 1
                            if count % 50 == 0:
                                break
                            if "file_url" in item:
                                picture_url = item["file_url"]
                                picture_name = re.sub('[<>:"/|?*]', " ", unquote(urlparse(picture_url).path.split("/")[-1]))
                                text = f'**{picture_name}**\n'
                                text += f'**Tags Matched:** {tags}'
                                buttons = [[InlineKeyboardButton('Source', url=picture_url)]]
                                results.append(InlineQueryResultPhoto(
                                    photo_url=picture_url,
                                    title=f"Result:{picture_name}",
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
        async with aiohttp.ClientSession(headers=headers) as session:
            counter = randint(1, 10)
            while_counter = 1
            while while_counter <= 50:
                while_counter += 1
                async with session.get(f"https://danbooru.donmai.us/posts.json?",
                                        params={"tags": tags,
                                                "random": "true",
                                                "page": counter}
                                                ) as response:
                    data = await response.json()
                    counter += 1
                    count = 0
                    if len(data) == 0:
                        break
                    else:
                        for item in data:
                            count += 1
                            if count % 50 == 0:
                                break
                            if "file_url" in item:
                                picture_url = item["file_url"]
                                picture_name = re.sub('[<>:"/|?*]', " ", unquote(urlparse(picture_url).path.split("/")[-1]))
                                text = f'**{picture_name}**\n'
                                text += f'**Tags Matched:** {tags}'
                                buttons = [[InlineKeyboardButton('Source', url=picture_url)]]
                                results.append(InlineQueryResultPhoto(
                                    photo_url=picture_url,
                                    title=f"Result:{picture_name}",
                                    caption=text,
                                    description=f"Tags Matched: #{tags}",
                                    reply_markup=InlineKeyboardMarkup(buttons)))
                    await client.answer_inline_query(query.id,
                                                    results=results,
                                                    is_gallery=True,
                                                    cache_time=CACHE_TIME
                                                    )
    return