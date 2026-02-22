# Architectural Styles - Community Kitchen

Dokumen ini menjelaskan gaya arsitektur yang diterapkan dalam pengembangan sistem Community Kitchen.

## 1. Pembagian Subsistem (Subsystems)

Sistem dibagi menjadi tiga subsistem utama yang saling berinteraksi:

1.  **Subsistem Client (Frontend)**
    *   Bertanggung jawab atas antarmuka pengguna (UI) dan pengalaman pengguna (UX).
    *   Teknologi: Vue.js / Mobile WebView.
2.  **Subsistem Core Server (Backend Utama)**
    *   Menangani logika bisnis utama: Autentikasi, Manajemen Barang, Peminjaman/Request.
    *   Teknologi: Laravel/Django.
3.  **Subsistem AI Service (Intelligence)**
    *   Layanan khusus untuk pemrosesan kecerdasan buatan (Generate Resep).
    *   Teknologi: FastAPI + Ollama.

### Diagram Interaksi Antar Subsistem

```mermaid
graph TD
    Client[Client / Frontend]
    Core[Core Backend]
    AI[AI Service]
    DB[(Database System)]

    Client -- HTTP Request (Auth, Items) --> Core
    Client -- HTTP Request (Generate Recipe) --> Core
    Core -- Query/Transact --> DB
    Core -- Internal API Call (AI Recipe) --> AI
    AI -- Response (Recipe JSON) --> Core
    Core -- Response --> Client
```

---

## 2. Gaya Arsitektural (Architectural Styles)

### A. Client-Server Architecture
Sistem memisahkan tanggung jawab antara penyedia sumber daya (Server) dan peminta layanan (Client).

*   **Penerapan:**
    *   **Client:** Aplikasi Frontend (Mobile/Web) tidak menyimpan logika bisnis yang berat, hanya bertugas menampilkan data dan mengirim input pengguna.
    *   **Server:** Backend menyediakan API (RESTful) yang merespon request dari Client dengan format JSON, termasuk sebagai gateway untuk fitur AI.
*   **Alasan:** Memungkinkan pengembangan frontend dan backend dilakukan secara independen. Backend yang sama dapat melayani platform berbeda (Web, Android, iOS).

**Visualisasi Client-Server**

```mermaid
graph LR
    Client[Client / Frontend]

    subgraph Server[Server]
        Core[Core Backend]
        AI[AI Service]
        DB[(Database System)]
        Core -- Query/Transact --> DB
        Core -- Internal API Call --> AI
        AI -- Response --> Core
    end

    Client -- HTTP Request --> Core
    Core -- HTTP Response --> Client
```

### B. Microservices (Service-Oriented) Architecture
Fungsionalitas sistem dipecah menjadi layanan-layanan kecil yang independen dan berjalan sebagai proses terpisah.

*   **Penerapan:**
    *   **Core Service:** Fokus pada manajemen user, transaksi barang, dan notifikasi.
    *   **AI Service:** Fokus pada komputasi berat (LLM Inference) untuk resep, diakses melalui backend utama.
*   **Alasan:**
    *   **Skalabilitas:** Server AI yang butuh resource besar (GPU/RAM) bisa di-scale terpisah dari server utama.
    *   **Isolasi Kegagalan:** Jika layanan AI sedang down (maintenance/error), fitur utama (login, pinjam barang) tidak terganggu.
    *   **Fleksibilitas Teknologi:** Menggunakan Python untuk AI (karena ekosistem AI kuat) dan kerangka kerja web yang matang untuk fitur sosial.

### C. Layered Architecture
Di dalam internal setiap subsistem backend, kode diorganisir ke dalam lapisan-lapisan logis (Layers) dengan tanggung jawab spesifik.

**Catatan:** Jumlah dan nama layer tidak harus sama di setiap subsistem. Prinsip utamanya adalah pemisahan tanggung jawab; layer bisa berbeda sesuai kebutuhan masing-masing komponen.

*   **Penerapan (Contoh pada Core Backend):**
    Visualisasi menunjukkan 5 komponen dalam alur data, di mana **3 di tengah** adalah layer aplikasi backend:
    1.  **Client / Frontend (External):** Mengirim request ke server.
    2.  **Presentation Layer (Routes & Controllers):** Menerima HTTP request, validasi input, dan memanggil business logic.
    3.  **Business Logic Layer (Services/Serializers):** Menjalankan aturan bisnis (misal: cek stok, hitung denda).
    4.  **Data Access Layer (Models/ORM):** Berinteraksi/query ke database.
    5.  **Database System (Infrastructure):** Sistem penyimpanan data fisik.
*   **Alasan:** Memudahkan maintenance dan testing (Testability). Jika kita ingin mengubah database, kita hanya perlu mengubah Data Layer tanpa mengganggu Presentation Layer.

**Visualisasi Layered Architecture (Core Backend)**

```mermaid
flowchart TB
    Client[Client / Frontend]
    PL[Presentation Layer\nRoutes & Controllers]
    BL[Business Logic Layer\nServices & Serializers]
    DAL[Data Access Layer\nModels / ORM]
    DB[(Database System)]

    Client --> PL
    PL --> BL
    BL --> DAL
    DAL --> DB
```

**Penerapan Layered Architecture Lainnya**

- **Frontend (Client):**
    - Presentation/UI Layer: komponen tampilan, halaman, layout.
    - State/Interaction Layer: manajemen state, validasi form, debouncing.
    - Service/API Layer: wrapper HTTP untuk komunikasi ke backend.
    - Utility Layer: helper, formatter, konfigurasi.
- **AI Service (FastAPI):**
    - API Layer: endpoint generate resep.
    - Service/Use-Case Layer: orkestrasi prompt, preprocessing input, postprocessing output.
    - Integration Layer: adapter ke Ollama/LLM.
    - Data/Cache Layer (opsional): cache hasil resep.
- **Database/Storage:**
    - Schema/Model Layer: struktur tabel dan relasi.
    - Repository/Query Layer: query/ORM yang dipakai backend.
- **Testing:**
    - Unit Test Layer: menguji fungsi tiap layer.
    - Integration Test Layer: menguji alur antar layer (API → service → DB).



```mermaid
---
config:
  layout: elk
---
graph TD
  subgraph microservice[Microservice]
    Client[Client / Frontend]
    Core[Core Backend]
    AI[AI Service]
    DB[(Database System)]

    Client -- HTTP Request (Auth, Items) --> Core
    Client -- HTTP Request (Generate Recipe) --> Core
    Core -- Query/Transact --> DB
    Core -- Internal API Call (AI Recipe) --> AI
    AI -- Response (Recipe JSON) --> Core
    Core -- Response --> Client

    
  end
  subgraph clientserver[Client-Server]
    Client2[Client / Frontend]
    subgraph Server2[Server]
        Core2[Core Backend]
        AI2[AI Service]
        DB2[(Database System)]
        Core2 -- Query/Transact --> DB2
        Core2 -- Internal API Call --> AI2
        AI2 -- Response --> Core2
    end

    Client2 -- HTTP Request --> Core2
    Core2 -- HTTP Response --> Client2
  end


  subgraph layered[Layered Architecture]
    direction TB
      LayeredClient[Client / Frontend]
      LayeredPL[Presentation Layer Routes & Controllers]
      LayeredBL[Business Logic Layer Services & Serializers]
      LayeredDAL[Data Access Layer Models / ORM]
      LayeredDB[(Database System)]

      LayeredClient --> LayeredPL
      LayeredPL --> LayeredBL
      LayeredBL --> LayeredDAL
      LayeredDAL --> LayeredDB
  end

  subgraph LyrFE_[Layered Architecture Frontend]
    direction TB
      LyrFE_Client[Presentation Layer]
      LyrFE_State[State manajemen state, validasi form, debouncing]
      LyrFE_Service[Service Layer]
      LyrFE_Utility[Utility Layer]

      LyrFE_Client --> LyrFE_State
      LyrFE_State --> LyrFE_Service
      LyrFE_Service --> LyrFE_Utility
  end

  subgraph LyrAI[Layered Architecture AI service]
    direction TB
        LAI_API[Endpoint generate resep]
        LAI_Service[Prompting, preprocessing input]
        LAI_Integration[adapter ke LLM - ollama]

        LAI_API --> LAI_Service
        LAI_Service --> LAI_Integration
  end
```