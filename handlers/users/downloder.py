import os
import logging
from aiogram.types import Message
from loader import dp
from aiogram import types
import yt_dlp
import browser_cookie3

# Cookies'ni saqlash uchun fayl
COOKIES_FILE = "/home/user/bots/Downloader/cookies.txt"


def save_cookies():
    """Chrome'dan cookies olib, Netscape formatida saqlash"""
    cookies = browser_cookie3.chrome()

    with open(COOKIES_FILE, "w") as f:
        # Header qo'shish (kommentariyalar)
        f.write("# Netscape format\n")
        f.write("# Format: domain    host_path    secure    expiry_time    name    value\n")

        # Har bir cookie uchun satr yaratish va faylga yozish
        for c in cookies:
            # Format: domain, path, secure, expiry, name, value
            line = f"{c.domain}\t{c.path}\t{c.secure}\t{c.expires}\t{c.name}\t{c.value}\n"
            f.write(line)


@dp.message_handler()
async def download(message: types.Message):
    url = message.text
    await message.reply("⏳ Yuklanmoqda...")

    dir_name = "downloads"
    os.makedirs(dir_name, exist_ok=True)

    # Cookies'ni yangilash
    save_cookies()

    ydl_opts = {
        "format": "best",
        "outtmpl": f"{dir_name}/%(title)s.%(ext)s",
        "concurrent_fragment_downloads": 5,
        "cookiefile": COOKIES_FILE  # Cookies'ni fayldan o'qish
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            file_info = ydl.extract_info(url, download=True)
            file_path = ydl.prepare_filename(file_info)  # To‘liq fayl yo‘lini olish

        if os.path.exists(file_path):
            with open(file_path, 'rb') as video:
                await message.answer_video(video=types.InputFile(video))
            os.remove(file_path)  # Foydalanuvchiga jo‘natilgach, faylni o‘chirish
        else:
            await message.reply("❌ Yuklab olishda xatolik yuz berdi: Fayl topilmadi.")

    except yt_dlp.utils.DownloadError as e:
        await message.reply(f"❌ Yuklab olishda xatolik yuz berdi: {str(e)}")
    except Exception as e:
        await message.reply(f"❌ Kutilmagan xatolik yuz berdi: {str(e)}")
