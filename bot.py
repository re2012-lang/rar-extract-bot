import telebot
import rarfile
import os
import shutil

# توکن رباتت رو اینجا بذار
import os
TOKEN = os.getenv('BOT_TOKEN')

bot = telebot.TeleBot(TOKEN)

TEMP_DIR = 'temp_rar'
EXTRACT_DIR = 'extracted'
os.makedirs(TEMP_DIR, exist_ok=True)
os.makedirs(EXTRACT_DIR, exist_ok=True)

@bot.message_handler(content_types=['document'])
def handle_document(message):
    file_name = message.document.file_name.lower()
    if not file_name.endswith(('.rar', '.zip')):
        bot.reply_to(message, "فقط فایل RAR یا ZIP بفرست!")
        return

    bot.reply_to(message, "در حال دانلود و اکسترکت...")

    try:
        file_info = bot.get_file(message.document.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        rar_path = os.path.join(TEMP_DIR, message.document.file_name)
        
        with open(rar_path, 'wb') as f:
            f.write(downloaded_file)

        if os.path.exists(EXTRACT_DIR):
            shutil.rmtree(EXTRACT_DIR)
        os.makedirs(EXTRACT_DIR, exist_ok=True)

        with rarfile.RarFile(rar_path) as rf:
            rf.extractall(EXTRACT_DIR)

        bot.reply_to(message, "اکسترکت شد! فایل‌ها رو می‌فرستم...")

        for root, _, files in os.walk(EXTRACT_DIR):
            for file in files:
                file_path = os.path.join(root, file)
                with open(file_path, 'rb') as f:
                    bot.send_document(message.chat.id, f, caption=file)

        bot.send_message(message.chat.id, "همه فایل‌ها ارسال شد!")

    except rarfile.BadRarFile:
        bot.reply_to(message, "فایل خراب یا رمزدار است!")
    except Exception as e:
        bot.reply_to(message, f"خطا: {str(e)}")
    finally:
        if 'rar_path' in locals() and os.path.exists(rar_path):
            os.remove(rar_path)

print("ربات در حال اجراست...")
bot.infinity_polling()
