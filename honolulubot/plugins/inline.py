from urllib.parse import unquote, urlparse
import re
from random import randint
import asyncio
from hentai import Hentai, Format
from pyrogram import filters
import time

from pyrogram.types import (
    InlineQueryResultArticle,
    InlineQueryResultPhoto,
    InputTextMessageContent,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    InputMediaPhoto
)

from honolulubot import honolulubot
from honolulubot.helpers.nhentai import generate_hentai
from honolulubot.helpers.aiohttp import sauce

NEXT_OFFSET = 25
CACHE_TIME = 0

IMG = "https://telegra.ph/file/9712b3d6acea03a8f4c00.jpg"

message_lock = asyncio.Lock()
message_info = dict()
nhentai_search = dict()

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

    elif string.split()[0] == "nhentai":
        if len(string.split()) == 1:
            await client.answer_inline_query(query.id,
                                            results=results,
                                            switch_pm_text="Read nHentai on the go",
                                            switch_pm_parameter="start"
                                        )
            return
        search_query = int(string.split(None, 1)[1])
        if search_query:
            nhentai_search[query.from_user.id] = search_query
        doujin = Hentai(search_query)
        pages = doujin.image_urls
        for nhentai in pages:
            a = 0
            buttons = [InlineKeyboardButton('Back', 'nhentai_back'), InlineKeyboardButton(f'{a + 1}/{len(pages)}', 'nhentai_nop'), InlineKeyboardButton('Next', 'nhentai_next')]
            if not a:
                buttons.pop(0)
            if len(pages) == a + 1:
                buttons.pop()
            title = doujin.title(Format.Pretty).replace(' ', '_')
            results.append(InlineQueryResultPhoto(
                            photo_url=nhentai,
                            title=title,
                            reply_markup=InlineKeyboardMarkup([buttons])))
        await client.answer_inline_query(query.id,
                                        results=results,
                                        is_gallery=False)

    return


@honolulubot.on_callback_query(filters.regex('nhentai_(back|next)$'))
async def anilist_move(client, query):
    async with message_lock:
        page = 0
        opage = page
        if query.matches[0].group(1) == 'back':
            page -= 1
        elif query.matches[0].group(1) == 'next':
            page += 1
        if page != opage:
            doujin = Hentai(nhentai_search[query.from_user.id])
            pages = doujin.image_urls
            image = doujin.image_urls[page]
            buttons = [InlineKeyboardButton('Back', 'nhentai_back'), InlineKeyboardButton(f'{page + 1}/{len(pages)}', 'nhentai_nop'), InlineKeyboardButton('Next', 'nhentai_next')]
            if not page:
                buttons.pop(0)
            if len(pages) == page + 1:
                buttons.pop()
            await query.edit_message_media(InputMediaPhoto(image), reply_markup=InlineKeyboardMarkup([buttons]))
            message_info[query.id] = page
    await query.answer()


@honolulubot.on_callback_query(filters.regex('nhentai_nop$'))
async def anilist_nop(client, query):
    await query.answer(cache_time=3600)