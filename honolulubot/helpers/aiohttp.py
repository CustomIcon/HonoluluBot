import aiohttp


headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:70.0) Gecko/20100101 Firefox/70.0"
}


async def sauce(tags, counter, url):
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.get(
            url,
            params={
                "tags": tags,
                "random": "true",
                "page": counter}
                ) as response:
                data = await response.json()
                return data
