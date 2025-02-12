import asyncio
from json import dumps
from os import getenv
from pathlib import Path

from aiogram import Bot
from aiogram.types import Gift, Gifts

from models import SavedGift


async def download_gifts(
        bot: Bot,
        base_output_dir: Path,
):
    images_dir = base_output_dir.joinpath("images")
    for output_dir in (base_output_dir, images_dir):
        if not output_dir.exists():
            output_dir.mkdir()

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
            destination=images_dir.joinpath(file_name).absolute(),
        )
        print(f"Downloaded {index + 1}/{len(available_gifts.gifts)}")
        await asyncio.sleep(1)
    with open(base_output_dir.joinpath("data.json"), "w") as f:
        f.write(dumps(list(data.values())))


async def main():
    async with Bot(token=getenv("BOT_TOKEN")) as bot:
        await download_gifts(bot, base_output_dir=Path("/tmp/temp/gifts"))


if __name__ == '__main__':
    asyncio.run(main())
