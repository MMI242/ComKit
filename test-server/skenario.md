# Skenario Testing 
---

# Unit Test Server 

## Test Register

1. Test register sukses
    - form benar:
        - username
        - password
        - name
        - address
        - community_id
    - cek struktur response (user langsung login)
        - response["access_token"]
        - response["refresh_token"]
        - response["token_type"]
        - response["expires_in"]
        - response["user"]
    - cek token_type == "Bearer"
    - cek user:
        - response["user"]["id"]
        - response["user"]["username"]
        - response["user"]["name"]
        - response["user"]["address"]
    - cek response["user"] == isi form di awal

2. Test register duplicate username (ditolak) status_code: 409

3. test username
    - test valid username pakai alphanumeric dan underscore 
    - ditolak username kosong
    - ditolak username kurang dari 3 karakter
    - ditolak username mengandung huruf besar
    - ditolak username mengandung karakter selain alphanumeric & underscore

4. test register password invalid:
    - ditolak password kosong
    - ditolak password kurang dari 6 karakter

5. test register "name" field kosong (ditolak)

6. test register missing address field
7. test register missing semua fields

## test login
1. test login sukses
    - chek struktur response komplit
    - cek struktur response["user"] komplit

2. test login invalid username (ditolak)
3. test login invalid password (ditolak)
4. test login missing username field (ditolak)
5. test login missing password field (ditolak)
5. test login missing semua field (ditolak)

6. test refresh token yang valid
7. test refresh token yang invalid
8. test refresh token tanpa mengirimkan token

## Test user item
1. get user item, user belum punya item (assert length==0)
2. test buat item sukses
3. test buat item missing field
4. test buat item salah qty=0
5. test buat item salah type (hanya ada 2 tipe yang benar "borrow"/"share") (ditolak)
6. test buat beberapa item sukses, kemudian get user item, semua item yang dibuat harus ada
7. test mengubah user item milik sendiri 
8. test mengubah user item yang bukan miliknya (ditolak)
9. test user item tanpa Authorization token (ditolak)

## test homepage
1. test user buka homepage (get items). ada pagination (response["pagination"]["items_per_page"] == 25)
2. get items dengan pagination /items?page=1, ?page=2
3. get items dengan search items?search=q
4. get items dengan filter /items?type=borrow
5. get items dengan filter /items?type=share
6. get items dengan semua parameter /items?type=all&page=n&search=query
7. get items unauthorized
8. get items invalid token
8. get items page diluar range pagination

## test user request-item
1. test lihat incoming requests
2. test lihat outgoing requests
3. test lihat requests invalid token (ditolak)
4. test lihat incoming requests ada datanya
    - user1 membuat item
    - user2 request item
    - user1 lihat incoming request muncul permintaan user2
    - user2 check outgoing requests ada datanya (status "pending")
5. test approve request
6. test reject request
7. test cancel request dari peminta
8. test item dipinjam, kemudian approve, cek status sudah menjadi "approved" kemudian (ceritanya dikembalikan) ubah status menjadi "returned" oleh item owner
9. test ubah status request tanpa token yang valid
10. test ubah status request dengan urutan status yang tidak benar (harusnya pending -> approved -> returned)
    - test setelah pending, langsung ubah returned


## Test alur pengguna

1. user1 register
2. user1 logout (lupakan token)
3. user1 login ulang (dapatkan token)
4. user1 lihat item user (cek harus kosong)
5. user1 membuat 30 items
6. user1 logout (lupakan token)
7. user2 register
8. user2 membuka homepage /items tanpa filter, cek banyak item dan total pagination (ada lebih dari 1 pagination, dan ada 30 item dari user1 tadi)
9. user2 buka pagination ke2 (masih ada item)
10. user2 request-item ke item pertama dari user1
11. user1 login ulang
12. user1 check incoming item-requests
13. user1 approve request

