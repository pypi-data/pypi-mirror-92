from aiowiki import Wikipya

import asyncio


# Так сейчас выглядит код для запуска теста
async def main_old():
    w = Wikipya("ru")
    s = await w.search("cmake")
    p = await w.getPage(s[0][0])

    print(w.parsePage(p))


# Этот код должен стать таким
async def main():
    wiki = Wikipya("ru")
    search = await wiki.search("cmake")
    page = await wiki.page(search[0])

    img = await page.image()
    print(img.source)


asyncio.run(main())
