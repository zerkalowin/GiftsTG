import asyncio
import shutil
from json import dumps
from os import getenv
from pathlib import Path

from aiogram import Bot
from aiogram.types import Gift, Gifts

from models import SavedGift

BASE_OUTPUT_DIR = Path("/tmp/temp/gifts")
IMAGES_DIR = BASE_OUTPUT_DIR.joinpath("images")

def prepare_dirs():
    for output_dir in (BASE_OUTPUT_DIR, IMAGES_DIR):
        if not output_dir.exists():
            output_dir.mkdir()
    for filename in ("index.html", "style.css"):
        shutil.copyfile(src=f"web/{filename}", dst=BASE_OUTPUT_DIR.joinpath(f"{filename}"))


async def download_gifts(
        bot: Bot,
):
    data = dict()

    available_gifts: Gifts = await bot.get_available_gifts()
    gift: Gift
    for index, gift in enumerate(available_gifts.gifts):
        data[gift.id] = SavedGift(
            id=gift.id,
            price=gift.star_count,
            upgrade_price=gift.upgrade_star_count,
            remaining_count=gift.remaining_count,
            total_count=gift.total_count,
        ).to_dict()
        file_name = f"{gift.id}.jpg"
        await bot.download(
            file=gift.sticker.thumbnail.file_id,
            destination=IMAGES_DIR.joinpath(file_name).absolute(),
        )
        print(f"Downloaded {index + 1}/{len(available_gifts.gifts)}")
        await asyncio.sleep(1)
    with open(BASE_OUTPUT_DIR.joinpath("data.json"), "w") as f:
        f.write(dumps(list(data.values())))


async def main():
    prepare_dirs()
    async with Bot(token=getenv("BOT_TOKEN")) as bot:
        await download_gifts(bot)


if __name__ == '__main__':
    asyncio.run(main())
