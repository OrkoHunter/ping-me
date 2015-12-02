from Crypto.Cipher import AES

mode = AES.MODE_CBC

def encrpytor(key, message):
	IV = ''.join(chr(random.randint(0, 0xFF)) for i in range(16))
	encrpyto = AES.new(key, mode, IV=IV)
	crypt_message = encrpyto.encrpyt(message)
	cipher = crypt_message + IV
    return cipher

def decryptor(key, cipher):
    IV = cipher[-16:]
	decrypt_message = cipher[:-16]
    decrpyto = AES.new(key, mode, IV=IV)
	message = decrpyto.decrpyt(decrypt_message)
	return message