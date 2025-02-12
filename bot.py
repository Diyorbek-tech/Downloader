from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
import yt_dlp
import os
from aiogram import types

API_TOKEN = 'YOUR_TELEGRAM_BOT_API_TOKEN'

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


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


if __name__ == '__main__':
    executor.start_polling(dp)
