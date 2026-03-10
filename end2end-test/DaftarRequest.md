## Skenario 1: Melihat daftar Request Masuk (data tampil benar)

**Skenario**:
- User1 (owner item) sudah login.
- User1 membuka halaman Request Masuk.

**Harapan**:
- Sistem menampilkan daftar request yang ditujukan ke user1.
- Setiap card menampilkan: nama item, dari (requester), qty, tanggal, dan status.
- Tombol Approve dan Reject muncul untuk request yang statusnya masih bisa diproses (mis. pending/mengupdate).

**Hasil**:
- Daftar request masuk tampil, informasi pada card sesuai, dan tombol Approve/Reject muncul pada request yang eligible.

## Skenario 2: Approve request (berhasil)

**Skenario**:
- User1 membuka Request Masuk.
- User1 memilih salah satu request dengan status pending/mengupdate.
- User1 menekan tombol Approve.

**Harapan**:
- Sistem mengubah status request menjadi Approved/Disetujui.
- Muncul notifikasi sukses.
- Item terkait berubah status ketersediaannya sesuai aturan sistem (mis. jadi Dipinjam/Reserved).
- Setelah refresh, status tetap approved (persisted).

**Hasil**:
- Request berhasil di-approve, status berubah menjadi Approved, notifikasi sukses tampil, dan status item ikut ter-update sesuai aturan.

## Skenario 3: Reject request (berhasil)

**Skenario**:
- User1 membuka Request Masuk.
- User1 memilih request yang statusnya masih pending/mengupdate.
- User1 menekan tombol Reject.

**Harapan**:
- Sistem mengubah status request menjadi Rejected/Ditolak.
- Muncul notifikasi sukses.
- Item tetap Tersedia (jika belum ada approval lain).
- Setelah refresh, status tetap rejected.

**Hasil**:
- Request berhasil ditolak, status berubah menjadi Rejected, notifikasi sukses tampil, dan item tetap tersedia.

## Skenario 4: Owner menandai barang “Sudah Dikembalikan” (success flow)

**Skenario**:
- User1 (owner) sudah login.
- Ada request masuk dari User2 yang statusnya menyetujui/approved (barang sedang dipinjam).
- User1 membuka halaman Request Masuk dan melihat card request tersebut.
- User1 menekan tombol Sudah Dikembalikan.

**Harapan**:
- Sistem mengubah status transaksi/request menjadi Returned/Sudah dikembalikan.
- Muncul notifikasi sukses.
- Item kembali ke status Tersedia/Available (atau qty bertambah kembali sesuai aturan).
- Tombol “Sudah Dikembalikan” hilang/disabled setelah sukses (tidak bisa diklik lagi).
- Setelah refresh, status tetap “sudah dikembalikan” (persisted).

**Hasil**:
- Status request berubah menjadi Returned/Sudah dikembalikan, notifikasi sukses tampil, item kembali tersedia, tombol tidak bisa dipakai lagi, dan status tetap benar setelah refresh.