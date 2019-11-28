from Crypto.Cipher import AES
import hashlib
import base64


def get_encrypt_data(raw_data, key, iv):
    raw_data_base64 = base64.b64encode(raw_data.encode('utf-8'))
    # 16byte
    if len(raw_data_base64) % 16 != 0:
        raw_data_base64_16byte = raw_data_base64
        for i in range(16 - (len(raw_data_base64) % 16)):
            raw_data_base64_16byte += '_'.encode('utf-8')
    else:
        raw_data_base64_16byte = raw_data_base64
    secret_key = hashlib.sha256(key.encode('utf-8')).digest()
    iv = hashlib.md5(iv.encode('utf-8')).digest()
    crypto = AES.new(secret_key, AES.MODE_CBC, iv)
    cipher_data = crypto.encrypt(raw_data_base64_16byte)
    cipher_data_base64 = base64.b64encode(cipher_data)

    return cipher_data_base64


def get_decrypt_data(cipher_data_base64, key, iv):
    cipher_data = base64.b64decode(cipher_data_base64)
    secret_key = hashlib.sha256(key.encode('utf-8')).digest()
    iv = hashlib.md5(iv.encode('utf-8')).digest()
    crypto = AES.new(secret_key, AES.MODE_CBC, iv)
    raw_data_base64_16byte = crypto.decrypt(cipher_data).decode('utf-8')
    raw_data_base64 = raw_data_base64_16byte.split("_")[0]
    raw_data = base64.b64decode(raw_data_base64)

    return raw_data