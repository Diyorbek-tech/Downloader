import os
import logging
from aiogram.types import Message
from loader import dp
import yt_dlp


@dp.message_handler()
async def download(message: Message):
    url = message.text

    await message.reply("⏳")

    dir_name = "downloads"
    os.makedirs(dir_name, exist_ok=True)

    ydl_opts = {
        "format": "best",
        "outtmpl": f"{dir_name}/%(title)s.%(ext)s",
        "concurrent_fragment_downloads": 5
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            file = ydl.extract_info(url, download=True)
            file_name = ydl.prepare_filename(file)
        with open(file_name, 'rb') as video:
            await message.answer_video(video)

        os.remove(file_name)

    except Exception as e:
        logging.exception(e)
        await message.reply("❌ Xatolik yuz berdi")
