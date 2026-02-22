```mermaid
usecaseDiagram

    actor U as "Warga (User)"
    actor AI as "AI Service"

    package "Aplikasi ComKit" {
        usecase "Register & Auto Login" as UC1
        usecase "Lihat Feed Komunitas" as UC2
        usecase "Post Item (Share/Borrow)" as UC3
        usecase "Request Item" as UC4
        usecase "Kelola Request (Approve/Reject)" as UC5
        usecase "Generate Resep Masakan" as UC6
    }

    U --> UC1
    U --> UC2
    U --> UC3
    U --> UC4
    U --> UC5
    U --> UC6
    UC6 .> AI : <<include>>
```
