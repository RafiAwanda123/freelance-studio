<div align="center">
  <img src="https://odoocdn.com/openerp_website/static/src/img/assets/png/odoo_logo.png" alt="Odoo Logo" width="250"/>

  # Self Management Freelance - Odoo 18 Module

  **Sistem ERP Mini untuk Manajemen Klien, Proyek, dan Tagihan Freelancer**

  ### Tech Stack / Skills
  ![Odoo 18](https://img.shields.io/badge/Odoo_18-714B67?style=for-the-badge&logo=odoo&logoColor=white)
  ![Python](https://img.shields.io/badge/Python_3-3776AB?style=for-the-badge&logo=python&logoColor=white)
  ![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)
  ![XML](https://img.shields.io/badge/XML-006600?style=for-the-badge&logo=xml&logoColor=white)
</div>

<br>

## Deskripsi Singkat
**Self Management Freelance** adalah modul kustom Odoo 18 yang dirancang khusus untuk mempermudah operasional seorang freelancer. Modul ini mengotomatiskan alur kerja mulai dari masuknya klien di CRM, manajemen tugas di Project, hingga pembuatan tagihan dan kustomisasi cetak PDF Invoice yang terintegrasi penuh.

Dibuat untuk memastikan tidak ada pekerjaan yang terlewat, tidak ada jadwal yang bentrok, dan tidak ada tagihan ganda, dengan alur kerja yang rapi dan profesional.

---

## Fitur Utama

### 1. Otomatisasi CRM ke Manajemen Proyek
Setiap kali klien sepakat dan status penawaran di CRM diubah menjadi "Won", sistem akan secara otomatis membuatkan Proyek baru beserta Tugas (Task) di papan Kanban, sekaligus menyiapkan draf penawaran (Draft Quotation) di latar belakang.
*Screenshot: Menampilkan status Lead di CRM yang sudah Won dan transisinya ke Project.*
![Otomatisasi CRM](tautan_screenshot_crm_won_disini.png)

### 2. Papan Kanban Kustom & Validasi Jadwal
Papan proyek telah disesuaikan dengan alur kerja freelancer: *Tugas Baru, Sedang Dikerjakan, Selesai, Revisi, Selesai Revisi*. Modul ini juga dilengkapi fitur validasi jadwal yang membatasi maksimal 4 proyek per minggu untuk menjaga beban kerja tetap ideal.
*Screenshot: Menampilkan papan Kanban tugas dan peringatan validasi maksimal 4 proyek.*
![Manajemen Proyek](tautan_screenshot_kanban_project_disini.png)

### 3. Penyesuaian Harga Dinamis (Fitur Revisi)
Terkadang harga awal dapat berubah setelah proses revisi. Modul ini memungkinkan freelancer untuk memasukkan "Harga Akhir" dan "Keterangan Tambahan" langsung di dalam kartu Tugas sebelum diselesaikan. Sistem akan otomatis memperbarui harga pada tagihan akhir beserta keterangan revisinya.
*Screenshot: Menampilkan form dalam Task yang berisi kolom Harga Akhir dan Keterangan Revisi.*
![Penyesuaian Harga](tautan_screenshot_form_task_harga_disini.png)

### 4. Otomatisasi Tagihan & Anti-Duplikasi
Mencegah terjadinya pembuatan tagihan ganda. Saat tugas di papan Kanban digeser ke kolom "Selesai", sistem secara presisi akan mencari draf Quotation milik klien tersebut, mengonfirmasinya menjadi Sales Order, dan mencetak draf Invoice secara otomatis.
*Screenshot: Menampilkan daftar Sales Order yang sudah otomatis terkonfirmasi dari Project.*
![Otomatisasi Sales Order](tautan_screenshot_sales_order_otomatis_disini.png)

### 5. Kustomisasi Desain PDF Invoice Elegan
Mengganti desain standar bawaan Odoo dengan desain PDF Invoice yang lebih premium. Menampilkan logo perusahaan freelancer secara otomatis, tata letak yang bersih, stempel lunas otomatis, dan identitas "Kinetic's ERP" di bagian catatan kaki.
*Screenshot: Menampilkan hasil cetak PDF Invoice kustom yang elegan.*
![Kustomisasi Invoice PDF](tautan_screenshot_pdf_invoice_disini.png)

### 6. Pemantauan Pembayaran Langsung
Menambahkan kolom khusus "Sudah Dibayar" dan label "Status Lunas" (Lunas, Sebagian, Belum Bayar) langsung di halaman daftar Sales Order. Mempermudah pemantauan klien mana yang belum melunasi tagihannya tanpa harus membuka menu akuntansi.
*Screenshot: Menampilkan List View Sales Order dengan kolom tambahan status pembayaran.*
![Status Pembayaran](tautan_screenshot_status_pembayaran_so_disini.png)

---

## Panduan Instalasi

1. Unduh (Download ZIP) atau lakukan *clone* pada repositori ini ke komputer Anda.
2. Ekstrak file ZIP yang telah diunduh. Di dalamnya, Anda akan menemukan folder bernama `self_management_freelance`.
3. Salin (Copy) folder `self_management_freelance` tersebut.
4. Tempel (Paste) folder tersebut ke dalam direktori `addons` pada instalasi Odoo 18 Anda (contoh letak folder bawaan Windows: `C:\Program Files\Odoo 18.0\server\odoo\addons`).
5. Buka program **Services** pada OS Anda, cari servis Odoo (misal: `odoo-server`), lalu lakukan **Restart**. Langkah ini wajib dilakukan untuk memuat file Python ke dalam sistem.
6. Buka aplikasi Odoo melalui peramban (browser) dan aktifkan **Developer Mode**.
7. Masuk ke menu **Apps** (Aplikasi), lalu klik **Update Apps List** (Perbarui Daftar Aplikasi) di bilah atas.
8. Cari modul **Self Management Freelance** di kolom pencarian (hapus filter 'Apps' pada bar pencarian jika perlu).
9. Klik **Install**.

---

## Prasyarat Modul
Pastikan modul bawaan Odoo berikut ini sudah terinstal di basis data Anda sebelum memasang modul ini:
* CRM (`crm`)
* Project (`project`)
* Sales (`sale_management`)
* Invoicing/Accounting (`account`)

---

## Dibuat Oleh
**Kinetic's ERP**
Modern Business & Management Solutions
