import streamlit as st

st.set_page_config(page_title="Kripto Hibrida", page_icon="🔐")

B64_CHARS = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"

def custom_b64encode(data_bytes):
    result = ""
    padding = 0
    
    for i in range(0, len(data_bytes), 3):
        chunk = data_bytes[i:i+3]
        
        if len(chunk) == 3:
            n = (chunk[0] << 16) + (chunk[1] << 8) + chunk[2]
        elif len(chunk) == 2:
            n = (chunk[0] << 16) + (chunk[1] << 8)
            padding = 1
        elif len(chunk) == 1:
            n = (chunk[0] << 16)
            padding = 2
            
        n1 = (n >> 18) & 63
        n2 = (n >> 12) & 63
        n3 = (n >> 6) & 63
        n4 = n & 63
        
        result += B64_CHARS[n1] + B64_CHARS[n2]
        if padding == 2:
            result += "=="
        elif padding == 1:
            result += B64_CHARS[n3] + "="
        else:
            result += B64_CHARS[n3] + B64_CHARS[n4]
            
    return result

def custom_b64decode(b64_string):
    result = []
    
    b64_string = b64_string.replace('=', '')
    
    for i in range(0, len(b64_string), 4):
        chunk = b64_string[i:i+4]
        
        n = 0
        for j in range(len(chunk)):
            n += B64_CHARS.index(chunk[j]) << (18 - 6 * j)
            
        result.append((n >> 16) & 255)
        if len(chunk) > 2:
            result.append((n >> 8) & 255)
        if len(chunk) > 3:
            result.append(n & 255)
            
    return result
    
n = 3233
e = 65537
d = 2753
session_key = 150
iv = 42

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
        mixed = ((ord(char) ^ key_val) ^ prev) % 256
        encrypted_bytes.append(mixed)
        prev = mixed
    return encrypted_bytes

def xor_cbc_decrypt(cipher_bytes, key_val, iv):
    decrypted_text = ""
    prev = iv
    for byte in cipher_bytes:
        orig_char_code = ((byte ^ key_val) ^ prev) % 256
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
    key_val_2 = (key_val + 7) % 256 
    lapis2_bytes = xor_ofb_encrypt(lapis1_string, key_val_2, iv)
    return lapis2_bytes

def dual_decrypt(cipher_bytes, key_val, iv):
    key_val_2 = (key_val + 7) % 256
    lapis1_string = xor_ofb_decrypt(cipher_bytes, key_val_2, iv)
    lapis1_bytes = [ord(c) for c in lapis1_string]
    pesan_asli = xor_cbc_decrypt(lapis1_bytes, key_val, iv)
    return pesan_asli

st.title("🔐 Kriptografi Hibrida")
st.markdown("Aplikasi simulasi **Enkripsi Berlapis (CBC-OFB)** yang diamankan dengan pertukaran kunci **RSA**.")

tab1, tab2 = st.tabs(["🔒 Enkripsi Pesan", "🔓 Dekripsi Pesan"])

with tab1:
    st.subheader("Masukkan Pesan Rahasia")
    input_user = st.text_area("Ketik pesan di sini:", height=100)
    
    if st.button("Enkripsi Sekarang", type="primary"):
        if input_user:
            raw_encrypted_msg = dual_encrypt(input_user, session_key, iv)
            encrypted_session_key = rsa_encrypt(session_key, (e, n))
            
            b64_cipher = custom_b64encode(raw_encrypted_msg)
            
            st.success("Pesan berhasil dienkripsi!")
            st.text_input("Kunci Sesi Terkunci (RSA):", value=str(encrypted_session_key), disabled=True)
            st.text_area("Pesan Terenkripsi (Base64):", value=b64_cipher, height=100, disabled=True)
            st.info("Silakan salin kedua data di atas untuk melakukan dekripsi di tab sebelah.")
        else:
            st.warning("Pesan tidak boleh kosong.")

with tab2:
    st.subheader("Buka Pesan Rahasia")
    b64_input = st.text_area("Masukkan Pesan Terenkripsi (Base64):", height=100)
    key_input = st.text_input("Masukkan Kunci Sesi (Angka RSA):")
    
    if st.button("Dekripsi Sekarang", type="primary"):
        if b64_input and key_input:
            try:
                key_int = int(key_input)
                decrypted_session_key = rsa_decrypt(key_int, (d, n))
                
                cipher_bytes = custom_b64decode(b64_input)
                
                pesan_asli = dual_decrypt(cipher_bytes, decrypted_session_key, iv)
                
                st.success("Pesan berhasil dibuka!")
                st.write(f"**Kunci Sesi Asli yang Didapat:** `{decrypted_session_key}`")
                st.text_area("Isi Pesan Asli:", value=pesan_asli, height=100, disabled=True)
                
            except ValueError:
                st.error("Gagal! Pastikan Kunci Sesi RSA hanya berupa angka.")
            except Exception as err:
                st.error("Gagal membuka pesan. Pastikan teks Base64 utuh dan tidak terpotong.")
        else:
            st.warning("Harap isi teks Base64 dan Kunci RSA.")