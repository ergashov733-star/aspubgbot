import os
import json
import time
import telebot
from telebot.types import (
    ReplyKeyboardMarkup, 
    KeyboardButton, 
    InlineKeyboardMarkup, 
    InlineKeyboardButton,
    InputMediaPhoto,
    InputMediaVideo
)

# 1. @BotFather dan olgan tokeningizni shu yerga yozing
BOT_TOKEN = "8693990535:AAHfEwKk_mwxo2JpB-2FDdPPsDpslOzaPHs"

# 2. O'zingizning Telegram ID raqamingiz (Faqat raqam yoziladi, qo'shtirnoqsiz)
# ID raqamingizni bilish uchun botga /id deb yozing
ADMIN_ID = 1884125930

bot = telebot.TeleBot(BOT_TOKEN)

# =========================================================
# BAZA BILAN ISHLASH
# =========================================================
BAZA_FAYL = "baza.json"

def bazani_oqish():
    if os.path.exists(BAZA_FAYL):
        with open(BAZA_FAYL, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"rasmlar": [], "videolar": []}

def bazaga_saqlash(data):
    with open(BAZA_FAYL, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

baza = bazani_oqish()

# =========================================================
# TUGMALAR (MENYU)
# =========================================================
main_menu = ReplyKeyboardMarkup(resize_keyboard=True)
main_menu.row(KeyboardButton("🎬 Videolar"), KeyboardButton("🖼 Rasmlar"))
main_menu.row(KeyboardButton("🌐 Saytlar"))

sites_menu = InlineKeyboardMarkup()
sites_menu.add(InlineKeyboardButton(text="🚀 1-sayt (Yumshakim)", url="https://yumshakim.netlify.app"))
sites_menu.add(InlineKeyboardButton(text="🚀 1-sayt (Yagonasevgim 1)", url="https://yagonasevgim1.netlify.app"))
sites_menu.add(InlineKeyboardButton(text="🚀 1-sayt (Yagonasevgim 2)", url="https://yagonasevgim.netlify.app"))
sites_menu.add(InlineKeyboardButton(text="🚀 1-sayt (Arazchim)", url="https://arazchi.netlify.app"))
sites_menu.add(InlineKeyboardButton(text="🚀 1-sayt (Sevinchim)", url="https://sevinchim.netlify.app"))
sites_menu.add(InlineKeyboardButton(text="🚀 1-sayt (Sevinchimga)", url="https://sevinchimga.netlify.app"))
sites_menu.add(InlineKeyboardButton(text="🚀 1-sayt (Bog'cha)", url="https://siniytraktor.netlify.app"))

# =========================================================
# ADMIN BUYRUQLARI (/id va /tozalash)
# =========================================================

@bot.message_handler(commands=['id'])
def get_my_id(message):
    bot.reply_to(
        message, 
        f"🆔 Sizning Telegram ID raqamingiz: `{message.from_user.id}`\n\n"
        "Shu raqamni koddagi ADMIN_ID joyiga yozib qo'ying!", 
        parse_mode="Markdown"
    )

@bot.message_handler(commands=['tozalash'])
def clear_database(message):
    if message.from_user.id == ADMIN_ID:
        baza["rasmlar"] = []
        baza["videolar"] = []
        bazaga_saqlash(baza)
        bot.reply_to(message, "🗑 Baza tozalindi! Yangi rasm va videolarni tashlashingiz mumkin.")

# =========================================================
# RASM VA VIDEOLARNI FAQAT ADMIN TASHLA OLADI
# =========================================================

@bot.message_handler(content_types=['photo'])
def save_photo(message):
    if message.from_user.id == ADMIN_ID:
        file_id = message.photo[-1].file_id
        if file_id not in baza["rasmlar"]:
            baza["rasmlar"].append(file_id)
            bazaga_saqlash(baza)
            bot.reply_to(message, f"✅ Rasm saqlandi! Jami rasmlar: {len(baza['rasmlar'])} ta")
        else:
            bot.reply_to(message, "⚠️ Bu rasm bazada mavjud!")
    else:
        bot.send_message(message.chat.id, "Pastdagi menyudan foydalaning 👇", reply_markup=main_menu)

@bot.message_handler(content_types=['video'])
def save_video(message):
    if message.from_user.id == ADMIN_ID:
        file_id = message.video.file_id
        if file_id not in baza["videolar"]:
            baza["videolar"].append(file_id)
            bazaga_saqlash(baza)
            bot.reply_to(message, f"✅ Video saqlandi! Jami videolar: {len(baza['videolar'])} ta")
        else:
            bot.reply_to(message, "⚠️ Bu video bazada mavjud!")
    else:
        bot.send_message(message.chat.id, "Pastdagi menyudan foydalaning 👇", reply_markup=main_menu)

# =========================================================
# TUGMALAR ISHLASHI
# =========================================================

@bot.message_handler(commands=['start'])
def start_command(message):
    bot.send_message(
        message.chat.id,
        f"Salom, {message.from_user.first_name}! 👋\n"
        "Kerakli bo'limni pastdagi tugmalar orqali tanlang:",
        reply_markup=main_menu
    )

@bot.message_handler(func=lambda message: message.text == "🖼 Rasmlar")
def send_photos(message):
    rasmlar = baza["rasmlar"]
    if not rasmlar:
        bot.send_message(message.chat.id, "📂 Hozircha rasmlar joylanmagan.")
        return

    bot.send_message(message.chat.id, f"⏳ Jami {len(rasmlar)} ta rasm yuklanmoqda...")
    
    for i in range(0, len(rasmlar), 10):
        qism = rasmlar[i:i+10]
        media_group = []
        for index, photo_id in enumerate(qism):
            if index == 0:
                media_group.append(InputMediaPhoto(photo_id, caption=f"🖼 Rasmlar ({i+1}-{i+len(qism)})"))
            else:
                media_group.append(InputMediaPhoto(photo_id))
        bot.send_media_group(message.chat.id, media_group)
        time.sleep(1)

@bot.message_handler(func=lambda message: message.text == "🎬 Videolar")
def send_videos(message):
    videolar = baza["videolar"]
    if not videolar:
        bot.send_message(message.chat.id, "📂 Hozircha videolar joylanmagan.")
        return

    bot.send_message(message.chat.id, f"⏳ Jami {len(videolar)} ta video yuklanmoqda...")
    
    for i in range(0, len(videolar), 10):
        qism = videolar[i:i+10]
        media_group = []
        for index, video_id in enumerate(qism):
            if index == 0:
                media_group.append(InputMediaVideo(video_id, caption=f"🎬 Videolar ({i+1}-{i+len(qism)})"))
            else:
                media_group.append(InputMediaVideo(video_id))
        bot.send_media_group(message.chat.id, media_group)
        time.sleep(1.5)

@bot.message_handler(func=lambda message: message.text == "🌐 Saytlar")
def send_sites(message):
    bot.send_message(
        message.chat.id,
        "🌐 Men tayyorlagan saytlar ro'yxati.\nKirish uchun ustiga bosing:",
        reply_markup=sites_menu
    )

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.send_message(
        message.chat.id,
        "Iltimos, pastdagi tugmalardan birini tanlang 👇",
        reply_markup=main_menu
    )

# =========================================================
# BOTNI ISHGA TUSHIRISH
# =========================================================

if __name__ == "__main__":
    print("Bot muvaffaqiyatli ishga tushdi...")
    bot.infinity_polling()