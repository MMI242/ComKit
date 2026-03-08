## Skenario 1: Menginput field dengan credential yang benar (login)

**Skenario**:
- User1 membuka aplikasi ComKit dan menuju ke halaman login.
- User1 mengisi field dengan username dan password yang sudah terdaftar dengan benar.
- User1 menekan tombol "Login".

**Harapan**:
- User1 berhasil masuk ke dashboard atau halaman utama aplikasi setelah proses login selesai.

**Hasil**:
- Sistem mengarahkan User1 ke dashboard atau halaman utama aplikasi, dan status login berhasil.

## Skenario 2: Menginput field yang salah
**Skenario**:
- User1 mengisi field dengan informasi login yang salah.
- User1 menekan tombol "Login".

**Harapan**:
- Sistem menampilkan pesan error yang sesuai, seperti "username atau password salah".

**Hasil**:
- Pesan error yang relevan ditampilkan kepada User1, memberi tahu bahwa ada kesalahan dalam input data login.

## Skenario 3: Menginput field dengan tidak ada yang dikosongkan
**Skenario**:
- User1 mencoba untuk menekan tombol "Login" tanpa mengisi salah satu field yang diperlukan.
  
**Harapan**:
- Sistem menampilkan pesan error yang menunjukkan bahwa semua field harus diisi.

**Hasil**:
- Pesan error muncul di form dan User1 tidak dapat melanjutkan hingga kedua field terisi dengan benar.