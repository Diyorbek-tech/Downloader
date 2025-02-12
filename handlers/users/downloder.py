import os
import logging
from aiogram.types import Message
from loader import dp
from aiogram import types
import yt_dlp


@dp.message_handler()
async def download(message: types.Message):
    url = message.text

    await message.reply("⏳ Yuklanmoqda...")

    dir_name = "downloads"
    os.makedirs(dir_name, exist_ok=True)

    ydl_opts = {
        "format": "best",
        "outtmpl": f"{dir_name}/%(title)s.%(ext)s",
        "concurrent_fragment_downloads": 5,
        "cookiefile": "/home/ubuntu/Downloader/cookies.txt"  # 'cookies' fayli yo'li
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            file_info = ydl.extract_info(url, download=True)
            file_name = ydl.prepare_filename(file_info)

        if os.path.exists(file_name):
            with open(file_name, 'rb') as video:
                await message.answer_video(video=types.InputFile(video))
            os.remove(file_name)
        else:
            await message.reply("❌ Yuklab olishda xatolik yuz berdi: Fayl topilmadi.")

    except yt_dlp.utils.DownloadError as e:
        await message.reply(f"❌ Yuklab olishda xatolik yuz berdi: {str(e)}")
    except Exception as e:
        await message.reply(f"❌ Kutilmagan xatolik yuz berdi: {str(e)}")
