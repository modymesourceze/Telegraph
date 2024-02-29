import os
from pyrogram import Client, filters
from telegraph import upload_file
from config import Config
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

sbot = Client(
    "TelegraphUploader",
    api_id=Config.APP_ID,
    api_hash=Config.API_HASH,
    bot_token=Config.TG_BOT_TOKEN,
)

@sbot.on_message(filters.command("start"))
async def start(client, message):
    if message.chat.type == "private":
        await sbot.send_message(
            chat_id=message.chat.id,
            text="""<b>مرحبًا، أنا بوت تحويل الصور إلى تليجراف ميديا.
يمكنني تحميل الصور أو مقاطع الفيديو إلى تليجراف ميديا.
اضغط على زر المساعدة لمعرفة المزيد حول كيفية استخدامي</b>""",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("♆ المساعدة ♆", callback_data="help"),
                        InlineKeyboardButton("♆ قناة التحديثات ♆", url="https://t.me/EF_19"),
                    ],
                    [InlineKeyboardButton("♆ الدعم ♆", url="https://t.me/GY_19")],
                ]
            ),
            disable_web_page_preview=True,
            parse_mode="html",
        )

@sbot.on_message(filters.command("help"))
async def help(client, message):
    if message.chat.type == "private":
        await sbot.send_message(
            chat_id=message.chat.id,
            text="""<b>مساعدة بوت تليجراف ميديا!
ما عليك سوى إرسال صورة أو مقطع فيديو أقل من حجم ملف 5 ميجابايت،
سأقوم بتحميله إلى تلجراف ميديا.
~ @EF_19</b>""",
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton("♆ رجوع ♆", callback_data="start")]]
            ),
            disable_web_page_preview=True,
            parse_mode="html",
        )

@sbot.on_message(filters.command("about"))
async def about(client, message):
    if message.chat.type == "private":
        await sbot.send_message(
            chat_id=message.chat.id,
            text="""<b>حول بوت تليجراف ميديا!</b>
<b>♞ ⍣ المطور ⍣:</b> <a href="https://t.me/IC_19">⧛ 𓆩 『 🇾🇪⃤𝐀𝐁𝐃𝐔𝐋𝐋𝐀𝐇 个 ١9 』 𓆪 ⧚</a>
<b>♞ ⍣ الدعم ⍣:</b> <a href="https://t.me/GY_19">『 𝙺𝙸𝙽𝙶 』</a>""",
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton("♆ رجوع ♆", callback_data="help")]]
            ),
            disable_web_page_preview=True,
            parse_mode="html",
        )

@sbot.on_message(filters.photo)
async def telegraph_photo(client, message):
    msg = await message.reply_text("جاري تحويل الصورة إلى تليجراف ميديا...")
    download_location = await client.download_media(message=message, file_name="root/SBtg")
    try:
        response = upload_file(download_location)
    except:
        await msg.edit_text("يجب أن يكون حجم الملف أقل من 5 ميجابايت!")
    else:
        await msg.edit_text(
            f"**تم التحويل إلى تليجراف ميديا!**\n\n👉 [رابط الصورة](https://telegra.ph{response[0]})\n\nانضم هنا @EF_19",
            disable_web_page_preview=True,
        )
    finally:
        os.remove(download_location)

@sbot.on_message(filters.video)
async def telegraph_video(client, message):
    msg = await message.reply_text("جاري التحويل إلى تليجراف ميديا...")
    download_location = await client.download_media(message=message, file_name="root/SBtg")
    try:
        response = upload_file(download_location)
    except:
        await msg.edit_text("يجب أن يكون حجم الفيديو أقل من 5 ميجابايت!")
    else:
        await msg.edit_text(
            f"**تم التحويل إلى تليجراف ميديا!**\n\n👉 [رابط الفيديو](https://telegra.ph{response[0]})\n\nانضم هنا @EF_19",
            disable_web_page_preview=True,
        )
    finally:
        os.remove(download_location)

@sbot.on_message(filters.animation)
async def telegraph_gif(client, message):
    msg = await message.reply_text("جاري التحويل إلى تليجراف ميديا...")
    download_location = await client.download_media(message=message, file_name="root/SBtg")
    try:
        response = upload_file(download_location)
    except:
        await msg.edit_text("يجب أن يكون حجم الصورة المتحركة أقل من 5 ميجابايت!")
    else:
        await msg.edit_text(
            f"**تم التحويل إلى تليجراف ميديا!**\n\n👉 [رابط الصورة المتحركة](https://telegra.ph{response[0]})\n\nانضم هنا @EF_19",
            disable_web_page_preview=True,
        )
    finally:
        os.remove(download_location)

@sbot.on_callback_query()
async def button(bot, update):
    cb_data = update.data
    if "help" in cb_data:
        await update.message.delete()
        await help(bot, update.message)
    elif "about" in cb_data:
        await update.message.delete()
        await about(bot, update.message)
    elif "start" in cb_data:
        await update.message.delete()
        await start(bot, update.message)

print("Bot Started!")
print("Join @EF_19")

sbot.run()

