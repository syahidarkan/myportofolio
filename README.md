Nama : Syahid Arkan Fashihurrohman

NPM : 2506632936

Kelas : PBP C

## Tentang Proyek

Website portofolio pribadi yang dibangun dengan Django, HTML5, dan CSS3 murni (belum memakai database/MVT). Halaman utama berisi section About, Skills, Experience, Education, dan Projects, lengkap dengan layout responsif untuk desktop, tablet, dan mobile.

Tautan deployment PWS: https://syahid-arkan-myportofolio.pws.cs.ui.ac.id

## Cara Menjalankan Proyek Secara Lokal

1. Clone repositori ini lalu masuk ke foldernya.
2. Buat dan aktifkan virtual environment:
   ```
   python -m venv env
   source env/bin/activate      # Untuk macOS / Linux
   env\Scripts\activate         # Untuk Windows
   ```
3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
4. Buat file .env di root proyek (sejajar dengan manage.py):
   ```
   PRODUCTION=False
   ```
5. Jalankan migrasi lalu server pengembangan:
   ```
   python manage.py migrate
   python manage.py runserver
   ```
6. Buka http://localhost:8000/ di browser.


### Tugas 1

1. Iya betul, saya menggunakan elemen semantik HTML5 secara konsisten di seluruh halaman seperti header membungkus navigasi atas, nav untuk tautan navigasinya, main sebagai pembungkus konten utama, section untuk memisahkan tiap kelompok konten (About, Skills, Experience, Education, Projects), article untuk setiap kartu skill, pengalaman, entri pendidikan, dan proyek yang berdiri sendiri, footer untuk bagian bawah halaman, serta dl dt dan dd untuk pasangan label nilai seperti NPM dan Program studi. Elemen elemen ini membantu saya memberi struktur yang baik tanpa harus menambahkan atribut atau kelas tambahan hanya untuk menandai fungsi suatu blok. Screen reader dan search engine dapat langsung memahami hierarki dan fungsi setiap bagian halaman yang jauh lebih informatif dibanding menumpuk div di mana mana.

2. Tantangan terbesar adalah pas membuat beberapa layout dua kolom yang harus runtuh dengan rapi menjadi satu kolom di layar sempit tanpa merusak urutan baca konten, yaitu grid teks dan foto pada section About, timeline foto dan detail pada section Experience, dan baris nomor dan kartu pada section Projects. Saya mengevaluasinya dengan memperkecil lebar browser secara bertahap dan mengamati elemen mana yang terlalu rapat, terlalu besar, atau kehilangan hierarki visual. Keputusan yang saya ambil antara lain: pada Projects, nomor urut proyek yang di desktop memakai position sticky di kolom kiri saya ubah jadi position static dan ditata horizontal di atas kartu ketika layar sempit, karena efek sticky tidak berguna di satu kolom; pada Experience, kolom foto placeholder saya perkecil lebarnya lalu jadikan satu kolom penuh di breakpoint terkecil sambil menggeser titik timeline mengikuti; pada navbar, link navigasi saya sembunyikan bertahap lewat nth-child (tiga link disembunyikan di ukuran tablet, dan di layar HP seluruh link disembunyikan sehingga hanya menyisakan tombol Home dan Contact) supaya pill navigasi tidak meluber; dan teks paragraf saya biarkan rata kiri di semua ukuran agar tetap nyaman dibaca. Prioritas ukuran saya tentukan dari peran tiap elemen: teks konten mendapat ruang paling besar, sedangkan gambar dan elemen dekoratif seperti nomor urut, foto placeholder, dan video hero adalah yang saya biarkan menyusut lebih dulu.

3. Batasan paling terasa dari static web murni ini adalah semua konten harus ditulis hardcoded langsung di HTML. Setiap kali ada proyek baru, pengalaman baru, atau perubahan data, saya harus membuka file HTML, mengedit markup, dan deploy ulang. Tidak ada cara untuk memfilter atau mengurutkan konten secara dinamis, misalnya menampilkan hanya proyek dengan kategori tertentu atau menyorot yang terbaru secara otomatis. Fungsionalitas dinamis yang paling ingin saya tambahkan pada iterasi berikutnya adalah manajemen konten berbasis database untuk section Projects dan Experience, sehingga data bisa dikelola dari satu tempat dan ditampilkan secara dinamis lewat Django template tanpa menyentuh HTML setiap kali ada pembaruan.


### AI Disclosure

Dalam mengerjakan tugas ini saya menggunakan bantuan AI, yaitu Claude (lewat Claude Code), pada bagian berikut:

- Menyiapkan struktur awal proyek Django: mengganti nama folder konfigurasi menjadi portofolio, wiring views/urls/templates/static, serta konfigurasi WhiteNoise agar static file dilayani di produksi.
- Membantu membuatkan struktur awal HTML5 semantik dan CSS3 untuk section seperti layout Grid dan Flexbox, timeline Experience, kartu Skills dan Projects, serta efek reveal saat scroll.
- Membantu mengoreksi pengerjaan terkait responsivitas untuk breakpoint tablet dan mobile, serta mengompres aset video hero.

Seluruh isi konten (bio, daftar skill, riwayat pengalaman, riwayat pendidikan, daftar proyek, dan jawaban pertanyaan reflektif di atas) saya tulis dan verifikasi sendiri. Pemilihan skema warna, tipografi, tata letak akhir, dan penyesuaian detail dilakukan manual oleh saya. Proses prompting dilakukan secara iteratif yakni saya memberi arahan desain, meninjau hasilnya langsung di browser, lalu meminta perbaikan spesifik sampai sesuai ide saya.
