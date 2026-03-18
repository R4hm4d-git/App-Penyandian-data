import base64
n = 3233
e = 65537
d = 2753

def rsa_encrypt(data_int, public_key):
    e, n = public_key
    return pow(data_int, e, n)

def rsa_decrypt(cipher_int, private_key):
    d, n = private_key
    return pow(cipher_int, d, n)

def xor_cbc_encrypt(plain_text, key_val, iv):
    encrypted_bytes = []
    prev = iv
    for char in plain_text:
        mixed = (ord(char) ^ key_val ^ prev) % 256
        encrypted_bytes.append(mixed)
        prev = mixed
    return encrypted_bytes

def xor_cbc_decrypt(cipher_bytes, key_val, iv):
    decrypted_text = ""
    prev = iv
    for byte in cipher_bytes:
        orig_char_code = (byte ^ key_val ^ prev) % 256
        decrypted_text += chr(orig_char_code)
        prev = byte
    return decrypted_text

def xor_ofb_encrypt(plain_text, key_val, iv):
    encrypted_bytes = []
    keystream = iv
    for char in plain_text:
        keystream = (keystream ^ key_val) % 256
        cipher_byte = (ord(char) ^ keystream) % 256
        encrypted_bytes.append(cipher_byte)
    return encrypted_bytes

def xor_ofb_decrypt(cipher_bytes, key_val, iv):
    decrypted_text = ""
    keystream = iv
    for byte in cipher_bytes:
        keystream = (keystream ^ key_val) % 256
        orig_char_code = (byte ^ keystream) % 256
        decrypted_text += chr(orig_char_code)
    return decrypted_text

def dual_encrypt(plain_text, key_val, iv):
    lapis1_bytes = xor_cbc_encrypt(plain_text, key_val, iv)
    lapis1_string = "".join(chr(b) for b in lapis1_bytes)
    lapis2_bytes = xor_ofb_encrypt(lapis1_string, key_val, iv)
    return lapis2_bytes

def dual_decrypt(cipher_bytes, key_val, iv):
    lapis1_string = xor_ofb_decrypt(cipher_bytes, key_val, iv)
    lapis1_bytes = [ord(c) for c in lapis1_string]
    pesan_asli = xor_cbc_decrypt(lapis1_bytes, key_val, iv)
    return pesan_asli

session_key = 150
iv = 42

input_user = input("Masukkan pesan yang ingin dikunci: ")

raw_encrypted_msg = dual_encrypt(input_user, session_key, iv)
encrypted_session_key = rsa_encrypt(session_key, (e, n))

b64_cipher = base64.b64encode(bytes(raw_encrypted_msg)).decode()

print(f"Kunci Sesi Terkunci (RSA) : {encrypted_session_key}")
print(f"Pesan Terenkripsi (Base64): {b64_cipher}")

decrypted_session_key = rsa_decrypt(encrypted_session_key, (d, n))

cipher_bytes = list(base64.b64decode(b64_cipher))
pesan_asli = dual_decrypt(cipher_bytes, decrypted_session_key, iv)

print(f"Kunci Sesi Berhasil Dibuka: {decrypted_session_key}")
print(f"Pesan Asli Ditemukan      : {pesan_asli}")
