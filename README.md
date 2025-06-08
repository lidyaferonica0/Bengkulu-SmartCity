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

| Jenis Data            | Sumber              | Format              | Fungsi                                           |
| --------------------- | ------------------- | ------------------- | ------------------------------------------------ |
| Jaringan Jalan        | OpenStreetMap (OSM) | GraphML             | Membangun peta, pencarian rute, dan pelatihan AI |
| Koordinat Lokasi      | Nominatim (OSM)     | Tuple (lat, long)   | Menentukan node terdekat dari input lokasi       |
| Label Kemacetan       | Simulasi (dari OSM) | Integer (0/1)       | Melatih model Random Forest                      |
| Prediksi Kemacetan    | Model AI (RF)       | List of tuples      | Penalti rute, visualisasi                        |
| Rute & Estimasi Waktu | Hasil perhitungan   | List, float, string | Menampilkan rute dan informasi waktu tempuh      |

### 🔹 Praproses Data:

* Unduh data jalan via `osmnx`
* Bangun graf menggunakan `networkx`
* Hitung panjang ruas jalan
* Label kemacetan: jika panjang > 200 m → **macet** (1)

---

## ⚙️ 4. Alur Kerja Sistem

```plaintext
Input Lokasi Awal & Tujuan
         ↓
    Geocoding Lokasi
         ↓
     Cari Node Terdekat
         ↓
   Prediksi Kemacetan (RF)
         ↓
     Beri Penalti ke Jalan Macet
         ↓
     Algoritma Dijkstra untuk Rute
         ↓
      Tampilkan di Peta Interaktif
```

---

## 📁 5. Struktur Proyek

```plaintext
smartcity-bengkulu/
│
├── app/                         # FastAPI backend
│   ├── main.py                  # Endpoint utama
│   ├── model.py                 # Model Random Forest
│   └── utils.py                 # Fungsi bantu (routing, penalti)
│
├── data/
│   ├── jalan_kota_bengkulu.graphml  # Data graf OSM
│   └── label_kemacetan.csv          # Data simulasi label kemacetan
│
├── static/
│   └── map.html                # Visualisasi peta Folium
│
├── templates/
│   └── index.html              # Tampilan web utama
│
├── requirements.txt
└── README.md
```

---

## 📈 6. Evaluasi Model

### Evaluasi Model AI

Jika tersedia data nyata:

* 🔹 **Akurasi**
* 🔹 **Precision & Recall**
* 🔹 **F1 Score**

### Evaluasi Sistem Keseluruhan

* 🔹 **Waktu respon**
* 🔹 **Feedback pengguna**
* 🔹 **Uji lapangan (bandingkan prediksi vs realita)**

---

## 🚀 7. Rencana Pengembangan

✅ Integrasi data lalu lintas waktu nyata (API / sensor)
✅ Prediksi berbasis waktu, cuaca, atau event kota
✅ Push notification ke ponsel
✅ Model AI lanjutan:

* GNN (Graph Neural Network)
* LSTM (Time-based prediksi)
* Reinforcement Learning (optimasi jangka panjang)

✅ Pembuatan Aplikasi Mobile (Flutter / React Native)
✅ Dashboard untuk pemantauan lalu lintas kota
✅ Dukungan voice navigation & live rerouting

---

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

Jika kamu ingin, saya juga bisa bantu buatkan file `README.md` versi Markdown siap pakai atau konversi ke format PDF.
