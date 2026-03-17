Kriptografi Hibrida: RSA & CBC-OFB

Aplikasi penyandian data digital berbasis command-line (CLI) yang mengimplementasikan arsitektur Kriptografi Hibrida. Sistem ini menggabungkan kecepatan enkripsi simetris (Cascade CBC-OFB) dengan keamanan distribusi kunci asimetris (RSA). 

Fitur Utama
Arsitektur Hibrida: Mengatasi masalah key distribution pada algoritma simetris dan masalah performa komputasi pada algoritma asimetris.
Dual Block Cipher: Menggunakan dua mode operasi secara berjenjang:
  1. CBC (Cipher Block Chaining)
  2. OFB (Output Feedback)
Encoding: Menggunakan Base64 untuk memastikan hasil enkripsi (ciphertext) aman ditampilkan di terminal dan tidak mengalami kerusakan karakter (*non-printable characters*).

Arsitektur Sistem
1. Pembangkitan Kunci Sesi: Sistem membuat Session Key simetris secara otomatis.
2. Enkripsi Pesan (Simetris):Teks asli (plaintext) dienkripsi menggunakan mode CBC, kemudian hasilnya dienkripsi kembali menggunakan mode OFB dengan Session Key.
3. Enkripsi Kunci (Asimetris):Session Key yang digunakan pada langkah 2 dibungkus/dienkripsi menggunakan algoritma RSA.
4. Dekripsi:Menggunakan Private Key RSA untuk membuka *Session Key, yang kemudian digunakan untuk membuka gembok OFB dan CBC secara mundur.

Cara Penggunaan
1. Jalankan kode lalu input plaintext yang akan dienkripsi