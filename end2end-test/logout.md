## Skenario 1: Logout berhasil
**Skenario**:
- User1 sudah login (token tersimpan).
- User1 menekan tombol “Logout” pada aplikasi ComKit.

**Harapan**:
- Sistem menghapus token/sesi (mis. localStorage/cookie).
- User1 diarahkan ke halaman Login (atau landing page publik).
- Jika User1 mencoba akses halaman protected (mis. /dashboard), sistem redirect ke Login.

**Hasil**:
- Benar (token terhapus, redirect ke login, halaman protected tidak bisa diakses tanpa login).
