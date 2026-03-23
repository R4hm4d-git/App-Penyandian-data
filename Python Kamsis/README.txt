Kriptografi Hibrida: RSA & CBC-OFB

Aplikasi penyandian data digital berbasis web yang mengimplementasikan arsitektur Kriptografi Hybrid (Gabungan). Sistem ini menggabungkan kecepatan enkripsi simetris (CBC-OFB) dengan keamanan distribusi kunci asimetris (RSA). 

Fitur Utama
Arsitektur Hybrid: Mengatasi masalah key distribution pada algoritma simetris dan masalah performa komputasi pada algoritma asimetris.
Dual Block Cipher: Menggunakan dua mode operasi secara berjenjang:
  1. CBC (Cipher Block Chaining)
  2. OFB (Output Feedback)
Encoding: Menggunakan Base64 untuk memastikan hasil enkripsi (ciphertext) aman ditampilkan dan tidak mengalami kerusakan karakter (*non-printable characters*).
Universal File Support: Mendukung penyandian teks murni maupun file dokumen dan gambar secara langsung.
Auto-Format: Sistem secara cerdas mampu menebak dan mengembalikan format file hasil dekripsi (seperti .png, .jpg, .pdf, .docx) ke wujud aslinya secara otomatis.

Arsitektur Sistem
1. Pembangkitan Kunci Sesi: Sistem menggunakan Session Key simetris yang telah didefinisikan pada program.
2. Enkripsi Pesan (Simetris):Teks asli (plaintext) dienkripsi menggunakan mode CBC, kemudian hasilnya dienkripsi kembali menggunakan mode OFB dengan Session Key.
3. Enkripsi Kunci (Asimetris):Session Key yang digunakan pada langkah 2 dibungkus/dienkripsi menggunakan algoritma RSA.
4. Dekripsi:Menggunakan Private Key RSA untuk membuka *Session Key, yang kemudian digunakan untuk membuka gembok OFB dan CBC secara mundur.

Cara Penggunaan
1. Buka web, pada tab enkripsi pilih enkripsi txt, text atau gambar dan docs
2. Upload file untuk txt, gambar dan docs, khusus untuk text cukup diketik saja (disarankan 1 enkripsi pada waktu yang sama)
3. Tekan tombol enkripsi
4. Setelah enkripsi akan diberi ciphertext dan kunci sesi yang akan digunakan untuk dekripsi (jangan lupa kunci enkripsi)
5. Copy ciphertext pada tab deskripsi lalu masukkan kunci sesi yang sudah di enkripsi
6. Tekan tombol deskripsi
7. Pesan plaintext dan kunci sesi asli akan diberi kepada user untuk deskripsi txt dan text
8. Untuk gambar/docs akan diberi file aslinya yang dapat didownload dan kunsi sesi aslinya, dan khusus untuk gambar akan diberi preview gambar sebelum file didownload