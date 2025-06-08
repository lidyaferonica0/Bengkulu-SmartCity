# 🚦 SmartCity Bengkulu – Sistem Prediksi Kemacetan & Rekomendasi Rute Berbasis AI

 Sistem ini merupakan solusi awal Smart City untuk memprediksi kemacetan dan memberikan rute alternatif berbasis AI sederhana (Random Forest). Dengan memanfaatkan data OpenStreetMap, FastAPI, dan visualisasi Folium, sistem mampu memberikan peringatan kemacetan dan rute terbaik secara real-time. Pengembangan lebih lanjut dapat menjadikan sistem ini lebih adaptif dan bermanfaat secara luas bagi masyarakat kota Bengkulu.

---

## 💡 1. Alasan Memilih Model AI: Random Forest Classifier

Model **Random Forest Classifier (Scikit-learn)** dipilih karena:

* ✅ Model Random Forest Classifier dari pustaka scikit-learn dipilih sebagai komponen utama dalam sistem prediksi kemacetan karena berbagai keunggulannya dalam akurasi, kestabilan, dan efisiensi implementasi terutama untuk data berskala kecil hingga menengah seperti jaringan jalan Kota Bengkulu.
* ✅ Akurasi Tinggi dan Stabil = Menggabungkan banyak pohon keputusan (ensemble) untuk meningkatkan akurasi. Lebih tahan terhadap overfitting dibandingkan Decision Tree tunggal.
* ✅ Tahan terhadap Noise dan Outlier = Tidak mudah terpengaruh oleh data ekstrim seperti ruas jalan yang sangat panjang atau pendek.
* ✅ Tidak Membutuhkan Normalisasi atau Pra pemrosesan Rumit = Bisa langsung digunakan dengan data numerik seperti panjang jalan dalam meter.
* ✅ Cepat dan Efisien untuk Skala Kota = Dapat dilatih dan dijalankan dengan cepat pada dataset graf jalan ukuran kecil hingga menengah. Cocok untuk sistem Smart City berbasis FastAPI dan OSMnx seperti di Bengkulu.
* ✅ Output Klasifikasi yang Sederhana = Menghasilkan hasil biner: 1 = macet, 0 = tidak macet, sesuai dengan ambang panjang jalan dan mudah digunakan untuk menentukan penalti pada rute di algoritma navigasi seperti Dijkstra.
* ✅ Lebih Unggul daripada Decision Tree = Lebih stabil dan akurat karena tidak bergantung pada satu struktur pohon. Cocok untuk aplikasi nyata, bukan hanya uji coba awal.
* ✅ Lebih Ringan daripada LSTM/Neural Network = Tidak memerlukan tuning parameter rumit atau infrastruktur berat seperti GPU. Lebih cepat diimplementasikan dan diproses di sisi server
* ✅ Lebih Efisien daripada Model Lain (SVM, Naive Bayes, KNN)
* ✅ SVM: Kurang cocok untuk data besar dan tidak tahan noise.
* ✅ Naive Bayes: Asumsinya terlalu sederhana untuk data jalanan yang kompleks.
* ✅ KNN: Prediksi lambat karena perlu menghitung jarak ke seluruh data.

---

## ✨ 2. Fitur Utama

### 🧠 Prediksi Kemacetan AI

Menggunakan Random Forest Classifier untuk memprediksi kemacetan pada ruas jalan berdasarkan fitur panjang jalan. Sistem ini mampu mendeteksi potensi kemacetan secara cepat dan ringan tanpa memerlukan data historis.

### 🗺 Peta Interaktif & Visualisasi
Menampilkan jaringan jalan Kota Bengkulu secara real-time dengan warna berbeda:
* 🔴 **Jalur macet**
* 🔵 **Rute utama**
* 🟢 **Rute alternatif**
* Ikon titik awal & tujuan, lengkap dengan legenda interaktif.

### 🛣 Rekomendasi Rute Cerdas

Sistem menyarankan rute tercepat dan teraman berdasarkan hasil prediksi kemacetan. Rute utama akan dihindari jika terdapat ruas yang rawan macet, dan rute alternatif akan disorot sebagai solusi.

### 🚨 Notifikasi Kemacetan Otomatis

Jika jalur utama terdeteksi macet, pengguna mendapatkan peringatan langsung di peta berupa kotak peringatan berwarna merah dengan saran untuk menggunakan rute alternatif.

### 📏 Estimasi Waktu & Jarak

Menampilkan estimasi waktu tempuh berdasarkan moda transportasi:

* 🚶 Jalan kaki
* 🛵 Motor
* 🚗 Mobil
Disertai juga jarak tempuh untuk rute utama dan alternatif

### 🖥 Antarmuka Modern & Responsif

Tampilan aplikasi ringan dan profesional dengan desain biru-putih. Form input rute dilengkapi ikon dan tombol aksi yang bersih serta mudah digunakan di desktop maupun perangkat mobile

### 📡 Data Jalan dari OpenStreetMap

* Diambil dan diproses dengan **osmnx**
* Divisualisasikan melalui **folium**

### 🪶 Model AI Tambahan

Random Forest Regressor digunakan untuk memprediksi tingkat kemacetan berdasarkan data seperti:

  * Hari
  * Jam
  * Titik lokasi

---

## 📊 3. Jenis & Sumber Data

| Jenis Data                      | Sumber                            |  Fungsi                                                        |
| ---------------------           | -------------------               | ------------------------------------------------               |
| Jaringan Jalan                  | OpenStreetMap (OSM)               | Representasi graf kota: node (persimpangan), edge (ruas jalan) |
| Fitur jalan(panjang)            | OSM data / hasil perhitungan)     | Input untuk prediksi kemacetan                                 |
| Lokasi awal dan tujuan pengguna | Input pengguna                    | Menentukan rute pencarian                      |
| waktu saat ini                  | datetime Python                   | Penalti rute, visualisasi                        |
| dara historis kemacetan         | Sensor jalan / API lalu lintas    | Untuk model lanjutan      |

📊 Jenis Data
1.	Data Jaringan Jalan (Graph Jalan)
   * Isi: Node (titik persimpangan) dan edge (ruas jalan) dengan atribut seperti panjang ruas (length).
   * Format: GraphML (jalan_kota_bengkulu.graphml).
     Digunakan untuk: Membangun peta, mencari rute, dan melatih model AI.
2.	Data Lokasi Awal & Tujuan
  * Isi: Nama lokasi yang diinput user (misal: "Universitas Bengkulu", "Pantai Panjang").
  * Format: String (teks).
    Digunakan untuk: Dicari koordinatnya melalui proses geocoding.
3.	Data Koordinat Geografis
  * Isi: Latitude dan longitude hasil geocoding dari nama lokasi.
  * Format: Tuple float (latitude, longitude).
   Digunakan untuk: Menentukan node terdekat pada graph.
4.	Data Label Kemacetan
  * Isi: Label macet/tidak macet pada setiap ruas jalan, berdasarkan panjang ruas.
  * Format: Integer (1 = macet, 0 = tidak macet).
   Digunakan untuk: Melatih model Random Forest.
5.	Data Prediksi Kemacetan
  * Isi: Daftar ruas jalan yang diprediksi macet oleh model AI
  * 	Format: List of tuples (node1, node2).
    Digunakan untuk: Memberi penalti pada rute alternatif, visualisasi di peta.
6.	Data Rute & Estimasi Waktu
  * Isi: Urutan node rute utama dan alternatif, jarak tempuh, estimasi waktu tempuh (jalan kaki, motor, mobil).
  * Format: List, float, string.
    Digunakan untuk: Menampilkan rute dan informasi di peta.

🌐 Sumber Data
1.	OpenStreetMap (OSM)
  * Diperoleh dengan: Library osmnx.
  * Data yang diambil: Jaringan jalan kota Bengkulu (node, edge, panjang ruas).
  * Keterangan: Data diunduh satu kali dan disimpan ke file lokal (jalan_kota_bengkulu.graphml).
2.	Nominatim (OpenStreetMap Geocoding Service)
  * Diperoleh dengan: Library geopy.
  * Data yang diambil: Koordinat geografis (latitude, longitude) dari nama lokasi input user.
3.	Data Label Kemacetan (Simulasi)
  * Dibuat dari: Data panjang ruas jalan pada graph OSM.
  * Metode: Ruas jalan dengan panjang > 200 meter diberi label macet, sisanya tidak macet.
  * Keterangan: Bukan data kemacetan real-time, hanya simulasi untuk pelatihan model AI.

📝 Ringkasan

| Jenis Data                      | Sumber                           | Cara diperoleh     |  Keterangan                                                      |
| ---------------------           | -------------------              | -------------------  | ------------------------------------------------               |
| Jaringan Jalan                  | OpenStreetMap (OSM)              | osmnx | Graph jalan kota Bengkulu |
| Koordinat lokasi           | Nominatim (OSM)    | geopy | Hasil geocoding nama tempat                                 |
| Label kemacetan | Simulasi (dari OSM)                    | Berdasarkan panjang ruas| Untuk pelatihan Random Forest                      |
| Prediksi kemacetan                  | Model AI (RF)                   | Output prediksi| Untuk penalti rute & visual                        |
| Rute & estimasi         | Hasil perhitungan   | Algoritma rute & waktu | Untuk info ke user      |

### 🔹 Praproses Data:

* Metode Pengumpulan & Praproses:Unduh data jalan dari OpenStreetMap menggunakan OSMnx.
* Bangun graph jalan menggunakan NetworkX.
* Hitung panjang tiap ruas jalan (fitur utama).
* Label kemacetan disimulasikan berdasarkan panjang > 200 meter (sederhana untuk tahap awal).
* Untuk sistem nyata, gunakan API lalu lintas (Google, TomTom, atau sensor kota).


---

## ⚙️ 4. Alur Kerja Proses Sistem Navigasi SmartCity Bengkulu

1. 🧾 Masukan Pengguna
Input Lokasi: Pengguna mengisi lokasi awal dan tujuan melalui form HTML.
Validasi Form: Sistem memeriksa apakah kedua lokasi terisi dan berbeda, serta menghindari input kosong.
Pemrosesan: Permintaan dikirim ke backend (/generate-route) menggunakan metode POST.
2. 🗺 Pemetaan dan Praproses
Geokode Lokasi: Sistem menggunakan Nominatim untuk mencari koordinat lokasi di Bengkulu.
Pemetaan ke Jaringan Jalan: Lokasi dikonversi ke node terdekat pada graf jalan dari OpenStreetMap (OSM), dimuat dari file .graphml.

3. 🚦 Analisis Kemacetan
Prediksi Model ML: Model Random Forest (rf_model.pkl) menilai kemacetan tiap ruas berdasarkan panjang jalan (length).

   Klasifikasi Ruas: Ruas yang diprediksi padat ditandai sebagai “macet” dan dikenakan penalti untuk rute alternatif.

4. 🚗 Penentuan Rute
Algoritma Rute:
Rute utama dihitung dengan A* menggunakan bobot panjang jalan.
Rute alternatif dihitung dengan Dijkstra sambil menerapkan penalti pada ruas macet.

   Estimasi Waktu: Waktu tempuh dihitung berdasarkan kecepatan rata-rata per moda (jalan kaki, motor, mobil).

5. 🗂 Visualisasi dan Antarmuka
Peta Interaktif: Folium menghasilkan HTML dengan rute utama, rute alternatif, dan titik kemacetan.

  Warna Jalur:
   * 🟥 Merah: ruas macet
   * 🔵 Biru: rute utama lancar
   * 🟢 Hijau strip: rute alternatif
  Panel Informasi:
 * Menampilkan nama lokasi, waktu, jarak, dan estimasi waktu perjalanan.
 * Peringatan kemacetan muncul jika rute utama melewati ruas padat.

6. 🖥 Antarmuka Web Responsif
Form Input (HTML): Diatur dengan PyQt/HTML, menggunakan ikon dan gaya UI modern.
Map Output: iframe diperbarui secara dinamis untuk menampilkan rute terbaru (smartcity_rute_kemacetan.html).
Feedback Pengguna: Status pemrosesan dan hasil ditampilkan secara interaktif.



---

## 📁 5. Struktur Proyek

```plaintext
smartcity-bengkulu/
│                     
│── main.py                               # File utama phyton
|
├── data/
    ├──generate_navigation_map.py         #script pembuatan peta demo
│   ├── jalan_kota_bengkulu.graphml       # file graf dari OSM
│
│── smartcity_rute_kemacetan.html         # output peta yang ditampilkan
│
│── index.html                            # Tampilan web utama
│
└── README.md
```

## 📁 6. Diagram Alur
![image](https://github.com/user-attachments/assets/42513924-1e39-4548-bcd4-9ee7e5d8a57b)


## 📈 7. Contoh Kasus Uji 

 * 🧪 Uji 1:
      ![image](https://github.com/user-attachments/assets/7447c282-fce8-4b72-b708-95f3a9daaa98)

        * Lokasi Awal: Terminal Panorama
        * Lokasi Tujuan: RS M. Yunus
   * ✅ Hasil:
   * Jarak utama: 2.498 m
   * Jarak alternatif: 2.601 m
   * Prediksi kemacetan terdeteksi pada rute utama (ditandai garis merah)
   * Rute alternatif disarankan (garis hijau putus-putus)

 * 🧪 Uji 2:
      ![image](https://github.com/user-attachments/assets/cbeca7e0-5ba9-4715-8e49-4a9b16d25dbf)

         * Lokasi Awal: Simpang Skip
         * Lokasi Tujuan: Universitas Bengkulu
    * ✅ Hasil:
    * Jarak utama utama 2.025 m
    * Jarak alternatif 2.165 m
    * Kemacetan terdeteksi di rute utama (tengah)
    * Rute alternatif disarankan
    * Estimasi waktu:
    * Jalan kaki: 25 menit
    * Motor: 8 menit
    * Mobil: 10 menit

 * 🧪 Uji 3:
      ![image](https://github.com/user-attachments/assets/3a1ce74a-64bd-45fa-ac03-6feec6ea7cd2)
 
         * Lokasi Awal: Taman Smart City
         * Lokasi Tujuan: Masjid Al-Taqwa
    * ✅ Hasil:
    * Jarak utama: 2.383 m
    * Jarak alternatif: 3.422 m
    * Terjadi kemacetan di ruas tengah rute utama (garis merah)
    * Rute alternatif (hijau putus-putus) lebih panjang, namun disarankan
    * Estimasi waktu:
    * Jalan kaki: 29 menit
    * Motor: 9 menit
    * Mobil: 11 menit
    * Panel kemacetan otomatis muncul
      
 * 🧪 Uji 4:
      ![image](https://github.com/user-attachments/assets/e47a0aab-3cb6-42f3-966b-ba89ade463e0)

           * Lokasi Awal: Pasar Minggu
           * Lokasi Tujuan: Simpang Padang Harapan
   * ✅ Hasil:
   * Jarak utama: 2.129 m
   * Jarak alternatif: 2.346 m
   * Terjadi kemacetan di ruas tengah rute utama (garis merah)
   * Rute alternatif (hijau putus-putus) lebih panjang, namun disarankan
   * Estimasi waktu:
   * Jalan kaki: 26 menit
   * Motor: 8 menit
   * Mobil: 10 menit
   * Panel kemacetan otomatis muncul

 * 🧪 Uji 5:
      ![image](https://github.com/user-attachments/assets/904ab799-ebf5-42ee-943d-b2acc52c6023)

         * Lokasi Awal: Stadion Semarak
         * Lokasi Tujuan: Rumah Dinas Gubernur
* ✅ Hasil:
* Jarak utama: 1.384 m
* Jarak alternatif: 1.592 m
* Terjadi kemacetan di ruas tengah rute utama (garis merah)
* Rute alternatif (hijau putus-putus) lebih panjang, namun disarankan
* Estimasi waktu:
* Jalan kaki: 17 menit
* Motor: 5 menit
* Mobil: 6 menit
* Panel kemacetan otomatis muncul

Skema Pengujian Fitur
* 	Pencarian Rute: Penguji memasukkan lokasi awal dan tujuan, lalu menekan tombol “Temukan Rute”. Sistem harus   menampilkan rute utama, rute alternatif, serta estimasi waktu tempuh untuk berjalan kaki, motor, dan mobil.
* Deteksi Kemacetan: Sistem harus dapat mendeteksi kemacetan pada rute utama (ditandai warna merah pada peta) dan secara otomatis merekomendasikan rute alternatif (warna biru/hijau).
*	Visualisasi Peta: Penguji memastikan peta interaktif berjalan lancar, marker lokasi awal/tujuan tampil jelas, dan legenda warna rute mudah dipahami.
*	Estimasi Jarak dan Waktu: Sistem harus menampilkan jarak tempuh (meter) dan estimasi waktu perjalanan (menit) untuk setiap moda transportasi.
Hasil Pengujian
*	Semua fitur utama, seperti pencarian rute, deteksi kemacetan, dan visualisasi peta, berjalan sesuai fungsinya.
*	Sistem berhasil menampilkan peringatan jika rute utama mengalami kemacetan dan merekomendasikan rute alternatif.
*	Estimasi waktu dan jarak tampil akurat dan responsif terhadap perubahan input pengguna.
*	Aplikasi mudah digunakan, dengan tampilan antarmuka yang informatif dan intuitif bagi pengguna umum.



📈 4. Strategi Evaluasi Model
* 🔹 Evaluasi Model AI (Random Forest):
  * 	Jika memakai data real (label kemacetan aktual), evaluasi dengan:
     * 	Akurasi
     * 	Precision & Recall (untuk lihat trade-off salah prediksi)
     * 	F1 Score (gabungan presisi dan recall)
* 🔹 Evaluasi Sistem Keseluruhan:
  * Waktu respon sistem (real-time atau tidak)
  * Feedback pengguna terhadap akurasi rute & prediksi macet
  * Uji lapangan: Bandingkan rute vs kondisi nyata

## 🏛️ 7. 🚀 Pengembangan Lanjutan
Untuk meningkatkan manfaat bagi masyarakat, fitur tambahan bisa ditambahkan:
* ✅Integrasi data waktu nyata dari API atau sensor lalu lintas.
* ✅Prediksi waktu tempuh berdasarkan waktu, cuaca, atau event kota.
* ✅Peringatan notifikasi real-time ke ponsel pengguna.
* ✅Model AI lebih kompleks:
     * Graph Neural Network (GNN): lebih cocok untuk graf jalan.
     * LSTM: prediksi berdasarkan waktu (jam sibuk).
     * Reinforcement Learning: untuk optimasi rute jangka panjang.

Dashboard SmartCity: untuk pemantauan lalu lintas oleh dinas kota
 * 🔄 Integrasi data real-time dari CCTV / Google Maps
 * 📲 Pembuatan aplikasi mobile dengan Flutter / React Native
 * 🔔 Push notifikasi untuk rute padat
 * 🧭 Dukungan voice navigation dan live rerouting


## 🏛️ 8. Kontributor

| Nama Lengkap     | NPM       |
| ---------------- | --------- |
| Linia Nur Aini   | G1A023007 |
| Lidya Feronica   | G1A023009 |
| Ayu Dewanti Suci | G1A023057 |

**Proyek**: Tugas UAS Kecerdasan Buatan
**Institusi**: Universitas Bengkulu
**Dosen Pembimbing**: *Ir. Arie Vatresia, S.T., M.T.I., Ph.D*
**Tahun**: 2025

---
