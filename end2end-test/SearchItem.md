## Skenario 1: Cari item dengan keyword yang ada (hasil ditemukan)

**Skenario**:
- User berada di halaman homepage.
- User mengetik keyword yang sesuai dengan nama item (mis. “cooking pan”) pada field Cari item….
- User menekan Enter / berhenti mengetik (trigger search).

**Harapan**:
- Daftar item terfilter menampilkan item yang relevan dengan keyword.
- Jumlah item yang tampil berkurang sesuai hasil pencarian.
- Pagination menyesuaikan jumlah hasil.

**Hasil**:
- Item relevan muncul sesuai keyword, list dan pagination terupdate sesuai hasil pencarian.

## Skenario 2: Cari item dengan keyword yang tidak ada (tidak ditemukan)

**Skenario**:
- User berada di halaman homepage.
- User mengetik keyword yang tidak cocok dengan item manapun (mis. “xyzabc”) pada field Cari item….

**Harapan**:
- Sistem menampilkan kondisi kosong (empty state) seperti “No item founds”.
- Tidak ada item yang ditampilkan.

**Hasil**:
- Empty state tampil (“Item tidak ditemukan”), dan list item kosong.

## Skenario 3: Clear pencarian (kembali ke semua item)

**Skenario**:
- User sudah melakukan pencarian dan hasil terfilter.
- User menghapus isi field pencarian (backspace sampai kosong). 

**Harapan**:
- Daftar item kembali menampilkan semua item (default state).
- Filter search reset dan pagination kembali normal.

**Hasil**:
- List kembali ke semua item dan pagination kembali ke kondisi awal.

## Skenario 4: Cari item + filter tipe (All / Borrow / Share)

**Skenario**:
- User berada di halaman homepage.
- User mengetik keyword (mis. “cooking pan”).
- User memilih filter: Borrow atau Share.

**Harapan**:
- Sistem menampilkan item yang match keyword dan sesuai tipe filter (Borrow/Share).
- Jika tidak ada yang cocok, tampil empty state.

**Hasil**:
- Hasil pencarian terfilter ganda (keyword + tipe), dan empty state muncul jika tidak ada hasil.