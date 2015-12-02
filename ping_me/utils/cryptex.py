from Crypto.Cipher import AES
import base64
import random

mode = AES.MODE_CBC

def encryptor(key, message):
    IV = ''.join(chr(random.randint(0, 0xFF)) for i in range(16))
    encrypto = AES.new(key, mode, IV=IV)
    crypt_message = encrypto.encrypt(message)
    cipher = crypt_message + IV
    return base64.b64encode(cipher)

def decryptor(key, cipher):
    cipher = base64.b64decode(cipher)
    IV = cipher[-16:]
    decrypt_message = cipher[:-16]
    decrpyto = AES.new(key, mode, IV=IV)
    message = decrpyto.decrypt(decrypt_message)
    return message
