## Skenario 1: Generate resep dengan input bahan valid (sukses)

**Skenario**:
- User membuka halaman Recipe (/recipe).
- User mengisi textarea dengan bahan valid (mis. telur, bayam, kedelai).
- User menekan tombol Generate Recipe.

**Harapan**:
- Sistem menampilkan indikator proses (loading) saat request berjalan.
- Setelah selesai, resep muncul di UI lengkap: judul resep, cooking time, servings, difficulty, daftar ingredients, dan instructions.
- Konten resep sesuai dengan bahan yang dimasukkan (ingredients mencantumkan bahan input atau turunannya).

**Hasil**:
- Loading tampil saat proses generate, lalu resep berhasil muncul lengkap (judul, meta, ingredients, instructions) dan memuat bahan yang diinput.

## Skenario 2: Generate resep dengan input kosong (validasi gagal)

**Skenario**:
- User membuka halaman /recipe.
- User tidak mengisi textarea (kosong).
- User menekan Generate Recipe.

**Harapan**:
- Sistem menolak proses generate dan menampilkan pesan validasi.
- Tidak ada request ke API (atau API tidak dipanggil).
- Tidak ada resep baru yang ditampilkan.

**Hasil**:
- Pesan validasi muncul, tombol tidak memproses generate, dan tidak ada hasil resep yang ditampilkan.

## Skenario 3: Generate resep dengan input sangat panjang / banyak bahan (tetap sukses & UI stabil)

**Skenario**:
- User mengisi textarea dengan banyak bahan (mis. 30+ item atau paragraf panjang).
- User menekan Generate Recipe.

**Harapan**:
- Sistem tetap memproses (loading muncul), tidak crash/hang.
- Resep berhasil muncul, layout tetap rapi (scroll bekerja, tidak overflow parah).

**Hasil**:
- Aplikasi tetap stabil; resep berhasil tampil

## Skenario 4: API gagal (timeout/500) saat generate

**Skenario**:
- User mengisi bahan valid lalu klik Generate Recipe, tetapi API error (500/timeout).

**Harapan**:
- Sistem menampilkan pesan error yang jelas.
- Tombol Generate Recipe aktif kembali setelah error.
- Tidak menampilkan hasil resep parsial/korup.

**Hasil**:
- Pesan error tampil, user bisa menekan Generate lagi, dan tidak ada resep “setengah jadi” yang muncul.