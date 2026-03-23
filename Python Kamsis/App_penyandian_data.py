import streamlit as st
import base64

st.set_page_config(page_title="Kripto Hybrid", page_icon="🔐")

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
        mixed = ((ord(char) ^ prev) ^ key_val) % 256
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

def deteksi_ekstensi(bytes_data):
    if bytes_data.startswith(b'\x89PNG'): return '.png', 'image/png'
    elif bytes_data.startswith(b'\xff\xd8'): return '.jpg', 'image/jpeg'
    elif bytes_data.startswith(b'%PDF'): return '.pdf', 'application/pdf'
    elif bytes_data.startswith(b'PK\x03\x04'): return '.docx', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
    elif bytes_data.startswith(b'\xd0\xcf\x11\xe0'): return '.doc', 'application/msword'
    else: return '.txt', 'text/plain'

st.title("🔐 Kriptografi Hybrid")
st.markdown("Aplikasi simulasi **Enkripsi Berlapis (CBC-OFB)** yang diamankan dengan pertukaran kunci **RSA**.")

tab1, tab2 = st.tabs(["🔒 Enkripsi Pesan", "🔓 Dekripsi Pesan"])

with tab1:
    st.subheader("Masukkan Pesan Teks Rahasia")
    uploaded_txt = st.file_uploader("Pilih unggah file .txt (Opsional):", type=['txt'])
    isi_teks_default = ""
    
    if uploaded_txt is not None:
        isi_teks_default = uploaded_txt.getvalue().decode("utf-8")
        st.success("Teks dari file berhasil dimuat!")

    input_user = st.text_area("Ketik pesan atau biarkan terisi dari file:", value=isi_teks_default, height=100)
    
    if st.button("Enkripsi Teks Sekarang", type="primary"):
        if input_user:
            raw_encrypted_msg = dual_encrypt(input_user, session_key, iv)
            encrypted_session_key = rsa_encrypt(session_key, (e, n))
            b64_cipher = custom_b64encode(raw_encrypted_msg)
            
            st.success("Pesan berhasil dienkripsi!")
            st.write("**Kunci Sesi Terkunci (RSA):**")
            st.code(str(encrypted_session_key), language="text")
            st.write("**Pesan Terenkripsi (Base64):**")
            st.code(b64_cipher, language="text")
        else:
            st.warning("Pesan tidak boleh kosong.")

    st.divider()
    
    st.subheader("Atau Enkripsi File (Gambar / Dokumen)")
    uploaded_file = st.file_uploader("Unggah file rahasia:", type=['png', 'jpg', 'jpeg', 'doc', 'docx', 'pdf', 'txt'])
    
    if uploaded_file is not None:
        if st.button("Enkripsi File Sekarang", type="primary"):
            bytes_data = uploaded_file.getvalue()
            file_string = base64.b64encode(bytes_data).decode('utf-8')
            
            raw_encrypted_file = dual_encrypt(file_string, session_key, iv)
            encrypted_session_key = rsa_encrypt(session_key, (e, n))
            b64_cipher_file = custom_b64encode(raw_encrypted_file)
            
            st.success("File berhasil dienkripsi menjadi teks rahasia!")
            st.write("**Kunci Sesi Terkunci (RSA) untuk File:**")
            st.code(str(encrypted_session_key), language="text")
            st.write("**Teks Enkripsi File (Base64):**")
            st.code(b64_cipher_file, language="text")

with tab2:
    st.subheader("Buka Pesan Teks Rahasia")
    with st.form("form_dekripsi_teks"):
        b64_input = st.text_area("Masukkan Pesan Terenkripsi (Base64):", height=100)
        key_input = st.text_input("Masukkan Kunci Sesi (Angka RSA):")
        submitted_teks = st.form_submit_button("Dekripsi Teks Sekarang", type="primary")
        
        if submitted_teks:
            if b64_input and key_input:
                try:
                    key_int = int(key_input)
                    decrypted_session_key = rsa_decrypt(key_int, (d, n))
                    cipher_bytes = custom_b64decode(b64_input)
                    pesan_asli = dual_decrypt(cipher_bytes, decrypted_session_key, iv)
                    
                    st.success("Pesan teks berhasil dibuka!")
                    st.write(f"**Kunci Sesi Asli yang Didapat:** `{decrypted_session_key}`")
                    st.text_area("Isi Pesan Asli:", value=pesan_asli, height=100, disabled=True)
                except ValueError:
                    st.error("Gagal! Pastikan Kunci Sesi RSA hanya berupa angka.")
                except Exception:
                    st.error("Gagal membuka pesan. Pastikan teks Base64 utuh.")
            else:
                st.warning("Harap isi teks Base64 dan Kunci RSA.")

    st.divider()
    
    st.subheader("Buka File Rahasia (Gambar / Dokumen)")
    b64_file_input = st.text_area("Masukkan Teks Enkripsi File:", height=150)
    key_file_input = st.text_input("Masukkan Kunci Sesi (Angka RSA) untuk File:")
    
    if st.button("Dekripsi File Sekarang", type="primary", key="btn_dekripsi_file"):
        if b64_file_input and key_file_input:
            try:
                key_int = int(key_file_input)
                decrypted_session_key = rsa_decrypt(key_int, (d, n))
                
                cipher_bytes = custom_b64decode(b64_file_input)
                file_string = dual_decrypt(cipher_bytes, decrypted_session_key, iv)
                file_bytes = base64.b64decode(file_string)
                
                ekstensi_asli, tipe_mime = deteksi_ekstensi(file_bytes)
                nama_file_otomatis = f"file_rahasia_terbuka{ekstensi_asli}"
                
                st.success("File berhasil dipulihkan! Silakan unduh di bawah ini.")
                st.write(f"**Kunci Sesi Asli yang Didapat:** `{decrypted_session_key}`")
                
                st.download_button(
                    label=f"Unduh File ({ekstensi_asli})",
                    data=file_bytes,
                    file_name=nama_file_otomatis,
                    mime=tipe_mime
                )
            except Exception as e:
                st.error(f"Gagal! Pastikan kunci benar dan teks enkripsi file utuh. (Kode Error: {e})")
        else:
            st.warning("Harap isi teks Base64 dan Kunci RSA.")
