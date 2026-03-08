## Skenario 1: Menginput field dengan credential yang benar
**Skenario**:
-   User1 mengisi semua field pada formulir registrasi dengan informasi yang benar 
-   User1 menekan tombol "Create Account".

**Harapan**:
- User1 berhasil masuk ke halaman konfirmasi atau dashboard setelah proses registrasi selesai.

**Hasil**: 
- Sistem mengarahkan User1 ke halaman konfirmasi akun atau dashboard, dan status registrasi berhasil.

## Skenario 2: Menginput field yang salah
**Skenario:** 
- User1 mengisi field dengan informasi yang salah, misalnya email yang sudah terdaftar atau format email yang tidak valid.
- User1 menekan tombol "Create Account".
 
**Harapan**:

- Sistem menampilkan pesan error yang sesuai, seperti "Email sudah terdaftar" atau "Format email tidak valid".

**Hasil**:
- Pesan error yang relevan ditampilkan kepada User1 untuk memberi tahu bahwa ada kesalahan pada input data.

## Skenario 3: Menginput field dengan tidak ada yang dikosongkan 
**Skenario**:
- User1 mencoba untuk menekan tombol "Create Account" tanpa mengisi salah satu field yang diperlukan. 
  
**Harapan**:
- Sistem menampilkan pesan error yang menunjukkan bahwa semua field harus diisi.
  
**Hasil**:
- Pesan error muncul di form, misalnya "Semua field harus diisi", dan User1 tidak dapat melanjutkan ke tahap berikutnya hingga semua field terisi dengan benar.
