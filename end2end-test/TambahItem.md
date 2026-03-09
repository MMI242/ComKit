## Skenario 1: Tambahkan item baru dengan input valid (sukses)

**Skenario**:
- User sudah login dan berada di menu Item Saya.
- User klik Tambah Item Baru (form modal terbuka).
- User mengisi field wajib: Nama Item, Deskripsi, Quantity, Unit, memilih Type (Pinjam/Bagikan), memilih Status (Tersedia/Dipinjam).
- (Opsional) User1 upload Foto.
- User klik tombol Tambah Item.

**Harapan**:
- Sistem menyimpan item baru.
- Modal tertutup / form reset.
- Muncul notifikasi sukses.
- Item baru tampil di daftar Item Saya dengan data sesuai input.

**Hasil**:
- Item berhasil ditambahkan, notifikasi sukses tampil, modal tertutup (atau form ter-reset), dan item muncul di daftar Item Saya sesuai data yang diinput.

## Skenario 2: Tambahkan item baru dengan field wajib kosong (validasi gagal)

**Skenario**:
- User membuka form Tambah Item Baru.
- User membiarkan salah satu field wajib kosong (contoh: Deskripsi atau Nama Item).
- User klik tombol Tambah Item.

**Harapan**:
- Sistem menolak submit dan menampilkan pesan validasi pada field yang kosong (mis. tooltip browser: “Please fill out this field.”).
- Item tidak tersimpan.
- Modal tetap terbuka.

**Hasil**:
- Pesan validasi tampil pada field yang kosong, item tidak tersimpan, dan modal tetap terbuka sampai user melengkapi field wajib.

## Skenario 3: Klik “Batal” pada form tambah item (tidak menyimpan)

**Skenario**:
- User membuka form Tambah Item Baru.
- User mengisi sebagian field.
- User klik tombol Batal.

**Harapan**:
- Modal tertutup tanpa menyimpan item.
- Tidak ada item baru pada daftar Item Saya.
- Jika form dibuka lagi, field kembali kosong (reset) sesuai desain.

**Hasil**:
- Modal tertutup, tidak ada item baru yang tersimpan, dan form kembali ke kondisi awal saat dibuka ulang.