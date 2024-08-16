import json
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend
import base64
import os

# يجب أن يكون مفتاح التشفير نفسه المستخدم في التشفير
key = b'asmdncjncjewac1a4a45a14a84d15xa1'  # استخدم المفتاح الصحيح هنا


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


def decrypt_phone_number(encrypted_phone: str) -> str:
    # تحويل البيانات المشفرة من base64
    encrypted_phone_bytes = base64.b64decode(encrypted_phone)

    # استخراج iv من البيانات المشفرة
    iv = encrypted_phone_bytes[:16]
    encrypted_phone_bytes = encrypted_phone_bytes[16:]

    # إعداد التشفير
    cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
    decryptor = cipher.decryptor()

    # فك التشفير
    decrypted_padded_phone = decryptor.update(encrypted_phone_bytes) + decryptor.finalize()

    # إزالة padding
    unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
    try:
        decrypted_phone = unpadder.update(decrypted_padded_phone) + unpadder.finalize()
    except ValueError as e:
        print(f"Padding error: {e}")
        return None

    return decrypted_phone.decode('utf-8')


def read_and_decrypt_data():
    # قراءة البيانات من ملف JSON
    with open("phone_numbers.json", "r") as f:
        for line in f:
            data = json.loads(line)
            encrypted_phone = data['encrypted_phone']
            decrypted_phone = decrypt_phone_number(encrypted_phone)
            if decrypted_phone:
                print(f"User ID: {data['user_id']}, Phone Number: {decrypted_phone}")
            else:
                print(f"Failed to decrypt phone number for User ID: {data['user_id']}")


if __name__ == '__main__':
    read_and_decrypt_data()
