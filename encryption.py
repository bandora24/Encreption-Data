import json
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend
import base64
import os

# توليد مفتاح التشفير
key = b'asmdncjncjewac1a4a45a14a84d15xa1'

def encrypt_phone_number(phone_number: str) -> str:
    # إعداد التشفير
    iv = os.urandom(16)
    cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
    encryptor = cipher.encryptor()

    # إضافة padding للبيانات
    padder = padding.PKCS7(algorithms.AES.block_size).padder()
    padded_data = padder.update(phone_number.encode('utf-8')) + padder.finalize()

    # التشفير
    encrypted_phone = encryptor.update(padded_data) + encryptor.finalize()

    # دمج iv مع البيانات المشفرة ثم تحويلها إلى base64
    return base64.b64encode(iv + encrypted_phone).decode('utf-8')

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('مرحبًا! من فضلك أرسل لي رقم هاتفك.')

async def save_phone(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    phone_number = update.message.text
    encrypted_phone = encrypt_phone_number(phone_number)

    data = {"user_id": update.message.from_user.id, "encrypted_phone": encrypted_phone}

    # حفظ الرقم المشفر في ملف JSON
    with open("phone_numbers.json", "a") as f:
        json.dump(data, f)
        f.write("\n")

    await update.message.reply_text('تم استلام رقم هاتفك وتخزينه بأمان.')

def main() -> None:
    # ضع هنا الـ Token الخاص بالبوت
    application = Application.builder().token("7472129592:AAF9kYzYZ1Ak_kevDLeWJwE5Rgsm2gpPdhw").build()

    # تعريف الأوامر
    application.add_handler(CommandHandler("start", start))

    # معالجة الرسائل النصية (لتلقي رقم الهاتف)
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, save_phone))

    # بدء تشغيل البوت
    application.run_polling()

if __name__ == '__main__':
    main()
