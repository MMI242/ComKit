# Edit Item
## Skenario 1: Edit item dengan input valid (sukses)

**Skenario**:
- User sudah login dan berada di halaman Item Saya.
- User klik tombol Edit pada salah satu item.
- Form edit terbuka dengan data item terisi (prefilled).
- User mengubah beberapa field (mis. Nama, Deskripsi, Qty, Status) lalu klik Simpan/Update.

**Harapan**:
- Sistem menyimpan perubahan item.
- Muncul notifikasi sukses.
- Daftar Item Saya menampilkan data terbaru (updated).

**Hasil**:
- Perubahan tersimpan, notifikasi sukses tampil, dan data item di list ter-update sesuai input terbaru.

## Skenario 2: Edit item tetapi field wajib dikosongkan (validasi gagal)

**Skenario**:
- User klik Edit pada item.
- User mengosongkan field wajib (mis. Nama Item atau Deskripsi).
- User klik Simpan/Update.

**Harapan**:
- Sistem menolak update dan menampilkan pesan validasi (mis. “Please fill out this field”).
- Perubahan tidak tersimpan.
- Form tetap terbuka.

**Hasil**:
- Validasi muncul, update tidak terjadi, dan user tetap di form edit sampai field wajib dilengkapi.
  
## Skenario 3: Klik “Batal” pada form Edit item (tidak menyimpan)

**Skenario**:
- User membuka form Edit.
- User mengisi sebagian field.
- User klik tombol Batal.

**Harapan**:
- Modal tertutup tanpa menyimpan item.
- Tidak ada item baru pada daftar Item Saya.
- Jika form dibuka lagi, field kembali kosong (reset) sesuai desain.

**Hasil**:
- Modal tertutup, tidak ada item baru yang tersimpan, dan form kembali ke kondisi awal saat dibuka ulang.

# Hapus Item
## Skenario 4: Hapus item (sukses)

**Skenario**:
- User sudah login dan berada di halaman Item Saya.
- User klik tombol Hapus pada item.
- Sistem menampilkan dialog konfirmasi, lalu user memilih Ya/Hapus.

**Harapan**:
- Item terhapus dari sistem.
- Muncul notifikasi sukses.
- Item hilang dari daftar Item Saya (dan tidak muncul lagi setelah refresh).

**Hasil**:
- Item berhasil dihapus, notifikasi sukses tampil, item hilang dari list dan tetap hilang setelah halaman di-refresh.

## Skenario 5: Hapus item dibatalkan (tidak jadi hapus)

**Skenario**:
- User klik tombol Hapus pada item.
- Muncul dialog konfirmasi.
- User memilih Batal/Cancel.

**Harapan**:
- Item tidak terhapus.
- Daftar Item Saya tidak berubah.

**Hasil**:
- Proses hapus dibatalkan, item tetap ada di daftar, dan tidak ada perubahan data.