# Dokumentasi Tools Data Pipeline ERGM

Repositori ini berisi kumpulan skrip Python (`tools`) untuk memproses, membersihkan, dan mengekstraksi fitur (salah satunya *network backbone*) dari berbagai dataset jaringan (seperti data perdagangan, pertukaran diplomatik, jarak spasial, dan log koloni) agar siap digunakan dalam pemodelan ERGM (*Exponential Random Graph Model*).

## 📊 Ringkasan Fungsi Kode

| Nama Modul / Skrip | Deskripsi Singkat Fungsi |
| :--- | :--- |
| **`backbone.py`** | Modul pustaka (library) inti untuk mengekstraksi *multiscale backbone* dari jaringan berbobot kompleks dengan menetapkan *disparity filter*. |
| **`backbone_runner.py`** | Skrip *runner* utama yang membaca *nodelist* & *edgelist*, memanggil fungsi di `backbone.py`, membuat plot distribusi *degree*, lalu menyimpan representasi *backbone* hasil filter. |
| **`colony_modifier.py`** | Membuat matriks relasi jajahan (Adjacency Matrix). Mengonversi daftar sepasang negara dan riwayat penjajahannya menjadi format jaringan *edgelist*. |
| **`diplomatic_exchange_modifier.py`** | Membersihkan data jaringan diplomasi dengan menyelaraskan nama-nama negara (*Country* dan *Destination*) menjadi kode negara `ISO3`. |
| **`dist_modifier.py`** | Menyaring *dataset* matriks jarak agar hanya mempertimbangkan interaksi jarak fisik pada negara-negara yang valid dan tercatat dalam *nodelist*. |
| **`feature_merger.py`** | Utilitas untuk menggabungkan dua berkas fitur node (*Left Join*) berbasis identitas kode `country_iso3`. |
| **`missing_handler.py`** | Skrip penyeimbang yang melakukan validasi keutuhan *edges* dan *nodes*. Skrip menghapus *edge* asing maupun *node* yatim piatu yang tidak sinkron di antara kedua data. |
| **`trade_cleaner.py`** | Skrip pembersih dan agregator data *TradeValue* dari *United Nations*. Mengagregasi volume nilai tukar ke sebuah matriks format *edgelist* dasar. |

---

## 📖 Penjelasan Detail & Cara Menjalankan (*How to Run*)

Berikut adalah penjelasan mendalam mengenai peran fungsional setiap skrip beserta dokumentasi urutan argumen parameter untuk menjalankannya melalui terminal.

### 1. `backbone.py`
**Penjelasan:** 
Ini bukanlah skrip eksekusi langsung, melainkan **Modul Inti**. Skrip ini memiliki implementasi algoritma *Disparity Filter* pada struktur graf kompleks beserta perhitungan metrik *alpha significance*, *centrality*, dan penentuan batas *quantile/percentile*. 
**Cara Menjalankan:**
Di-import ke dalam skrip Python lain (contoh: `from backbone import *`). Fungsi internal testing (*Dummy Random Graph*) dapat dijalankan melalui:
```bash
python backbone.py
```

### 2. `backbone_runner.py`
**Penjelasan:** 
Bertindak sebagai eksekutor fungsional *backbone extraction*. Skrip membaca data dari `.csv`, mereplika matriks menjadi `nx.DiGraph`, lalu mengurasi *cutoff constraint* *degree* maupun *alpha_percentile*. Hasil olahan jaringan disimpan di path target sekaligus menghasilkan *visual reports* berupa grafik derajat.
**Cara Menjalankan:**
```bash
python backbone_runner.py <nodelist_path> <edgelist_path> <min_alpha_ptile> <min_degree> <out_nodelist_path> <out_edgelist_path_disparity> <out_edgelist_path_threshold> <reports_path>
```

### 3. `colony_modifier.py`
**Penjelasan:** 
Mapping matriks relasional Kolonialisme. Skrip membangun Array N-x-N bersimbol biner '1' jika negara relasi bertindak sebagai kolonial atas negara matriks pasangannya. Mengubah representasinya kembali menjadi format edge source dan target lalu menyimpannya dalam suatu CSV keluaran.
**Cara Menjalankan:**
```bash
python colony_modifier.py <nodelist_path> <colonies_base_path> <output_path>
```

### 4. `diplomatic_exchange_modifier.py`
**Penjelasan:** 
Membersihkan kerancuan dalam entitas data *Diplomatic Exchange* atau pertukaran duta besar. Skrip memperbaiki referensi teks nama "negara asli" yang bisa ambigu menjadi referensi ID Universal (`ISO3`) lewat mekanisme pemetaan.
**Cara Menjalankan:**
```bash
python diplomatic_exchange_modifier.py <initial_dip_exchange_path> <country_names_path> <nodelist_path> <output_path>
```

### 5. `dist_modifier.py`
**Penjelasan:** 
Memangkas data tabel spasial / Jarak Euclidean Negara sehingga data entri yang dibaca benar-benar hanya berisikan nama-nama entri valid (`iso_o` dan `iso_d`) yang memang telah terdaftar pada daftar Node model dasar kita. Mengonversi alias dari referensi kolom tersebut menjadi `source` dan `target`.
**Cara Menjalankan:**
```bash
python dist_modifier.py <nl_path> <dist_path> <cleaned_output_path>
```

### 6. `feature_merger.py`
**Penjelasan:** 
Menyatukan (*merge*) dua tabel atribut secara berdampingan asalkan keduanya memiliki kolom ID utama `country_iso3`. Fitur skrip menggunakan fungsi dasar Left Join dari fitur `pandas`.
**Cara Menjalankan:**
```bash
python feature_merger.py <input1_path> <input2_path> <merged_path>
```

### 7. `missing_handler.py`
**Penjelasan:** 
Modul *Sanitizer/Garbage Collector*. Jika dalam daftar koneksi Network terdapat negara hantu yang ternyata tak ada di Metadata Nodelist (ataupun sebaliknya, ada Meta Node tetapi tak pernah muncul dalam satupun *edges* transaksi), skrip inilah yang akan menyesuaikan (*drop*) baris-baris kotor tersebut sembari membersihkan Data Duplikat.
**Cara Menjalankan:**
```bash
python missing_handler.py <nodelist_path> <edgelist_path> <out_nodelist_path> <out_edgelist_path>
```

### 8. `trade_cleaner.py`
**Penjelasan:** 
Pembersih khusus skema tabel *Trade Value* internasional. Ekstraksi spesifik ini merekonstruksi rincian tabel *flow* perdagangan dengan menyingkirkan atribut kolom pengganggu, lantas memadatkannya (*aggregate sum*) menjadi bobot graf (`weight`) ke dalam arsitektur Edge (Reporter x Partner).
**Cara Menjalankan:**
```bash
python trade_cleaner.py <uncleaned_file_path> <cleaned_file_path>
```
