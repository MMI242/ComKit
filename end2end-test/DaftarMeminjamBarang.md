## Skenario 1: Melihat daftar “Request Saya” (data tampil benar)

**Skenario**:
- User sudah login.
- User membuka menu My page/Request Saya.

**Harapan**:
- Sistem menampilkan daftar request milik user.
- Setiap card menampilkan data penting: nama item, kepada (owner), qty, tanggal pinjam, status.
- Tombol Cancel muncul untuk request yang masih bisa dibatalkan.

**Hasil**:
- Daftar request tampil dan informasi pada card sesuai dengan data request (nama item, owner, qty, tanggal, status), serta tombol Cancel muncul pada request yang eligible.

## Skenario 2: Cancel request yang masih “Pending/Mengupdate” (berhasil dibatalkan)

**Skenario**:
- User berada di halaman Mypage/Request Saya.
- User memilih salah satu request yang statusnya masih Pending/mengupdate.
- User2 menekan tombol Cancel (dan konfirmasi jika ada dialog).

**Harapan**:
- Sistem membatalkan request.
- Status berubah menjadi Canceled/Dibatalkan.
- Jika user refresh halaman, request tetap sudah dibatalkan.

**Hasil**:
- Request berhasil dibatalkan, status/list ter-update, notifikasi sukses tampil, dan perubahan tetap ada setelah refresh.

## Skenario 3: Cancel request yang sudah “Approved/Accepted” (ditolak)

**Skenario**:
- User membuka Request Saya.
- User mencoba membatalkan request yang statusnya sudah Approved/Accepted/Borrowed.

**Harapan**:
- Sistem menolak aksi cancel.
- Tombol Cancel tidak muncul/disabled.

**Hasil**:
- Cancel tidak bisa dilakukan, sistem menampilkan pesan yang sesuai / tombol nonaktif, dan status request tetap.

## Skenario 4: Status “mengupdate” (state loading/processing)

**Skenario**:
- User membuka Request Saya saat status request sedang “mengupdate” (processing).

**Harapan**:
- UI menampilkan indikator status yang jelas (mis. “mengupdate/loading”).
- Tombol Cancel bisa disabled sementara (opsional, jika aturan sistem begitu) untuk mencegah double action.
- Setelah update selesai, status berubah ke nilai final (Pending/Approved/Rejected) tanpa error UI.

**Hasil**:
- Indikator status tampil dengan benar, UI tidak freeze, dan status berubah normal setelah proses selesai.