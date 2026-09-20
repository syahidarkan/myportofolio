Nama : Syahid Arkan Fashihurrohman

NPM : 2506632936

Kelas : PBP C

## Tentang Proyek

Website portofolio pribadi yang dibangun dengan Django (pola MVT), HTML5, CSS3, dan sedikit JavaScript untuk interaktivitas. Data Experience dan Projects disimpan di database lewat model Django dan ditampilkan lewat halaman experience dan projects masing-masing, sementara halaman utama tetap berisi section Hero, About, Skills, Education, dan preview Experience/Projects, lengkap dengan layout responsif untuk desktop, tablet, dan mobile, plus beberapa elemen interaktif seperti ID card bertali yang mengikuti gerakan mouse, carousel Projects, dan efek reveal saat scroll.

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
7. Data Experience dan Project bisa ditambah, diedit, dan dihapus langsung dari web lewat `/experience/add/` dan `/projects/add/`, atau dilihat dalam bentuk JSON di `/api/experience/` dan `/api/projects/` (versi XML ada di `/api/experience/xml/` dan `/api/projects/xml/`).

### Tugas 1

1. Iya betul, saya menggunakan elemen semantik HTML5 secara konsisten di seluruh halaman seperti header membungkus navigasi atas, nav untuk tautan navigasinya, main sebagai pembungkus konten utama, section untuk memisahkan tiap kelompok konten (About, Skills, Experience, Education, Projects), article untuk setiap kartu skill, pengalaman, entri pendidikan, dan proyek yang berdiri sendiri, footer untuk bagian bawah halaman, serta dl dt dan dd untuk pasangan label nilai seperti NPM dan Program studi. Elemen elemen ini membantu saya memberi struktur yang baik tanpa harus menambahkan atribut atau kelas tambahan hanya untuk menandai fungsi suatu blok. Screen reader dan search engine dapat langsung memahami hierarki dan fungsi setiap bagian halaman yang jauh lebih informatif dibanding menumpuk div di mana mana.

2. Tantangan terbesar adalah pas membuat beberapa elemen yang di desktop bentuknya cukup kompleks tapi tetap harus enak dipakai di layar sempit, misalnya kartu ID card bertali (lanyard) di section Hero dan About, carousel Projects dengan tombol panah, dan kartu Skills yang lebarnya bisa berubah pas di-hover. Saya mengevaluasinya dengan memperkecil lebar browser secara bertahap dan mengamati elemen mana yang terlalu rapat, kepotong, atau kehilangan hierarki visual. Keputusan yang saya ambil antara lain: ID card di Hero saya sembunyikan total di layar mobile (≤768px) karena talinya butuh ruang vertikal yang cukup besar dan malah menutupi teks nama kalau dipaksa muat di layar sempit, sementara ID card di section About tetap ditampilkan tapi ukurannya disesuaikan lagi lewat variabel CSS supaya talinya konsisten nyambung ke tepi atas section di semua ukuran; pada Projects, tombol panah kiri-kanan saya sembunyikan di layar HP karena memakan jatah lebar carousel sehingga kartunya jadi kecil, padahal di HP orang sudah biasa swipe langsung; pada Experience, foto asli tiap pengalaman saya render pakai object-fit: contain (bukan cover) karena rasio tiap foto beda-beda jauh dan cover justru bikin fotonya terlalu di-zoom sampai tidak jelas isinya; dan navbar link saya sembunyikan bertahap lewat nth-child supaya pill navigasi tidak meluber di layar sempit. Prioritas ukuran saya tentukan dari peran tiap elemen: teks konten dan foto asli (Experience, Projects) tetap diusahakan terlihat penuh, sedangkan elemen dekoratif seperti ID card di Hero yang justru saya hilangkan dulu di mobile kalau ruangnya tidak cukup.

3. Batasan paling terasa dari static web murni ini adalah semua konten harus ditulis hardcoded langsung di HTML. Setiap kali ada proyek baru, pengalaman baru, atau perubahan data, saya harus membuka file HTML, mengedit markup, dan deploy ulang. Tidak ada cara untuk memfilter atau mengurutkan konten secara dinamis, misalnya menampilkan hanya proyek dengan kategori tertentu atau menyorot yang terbaru secara otomatis. Fungsionalitas dinamis yang paling ingin saya tambahkan pada iterasi berikutnya adalah manajemen konten berbasis database untuk section Projects dan Experience, sehingga data bisa dikelola dari satu tempat dan ditampilkan secara dinamis lewat Django template tanpa menyentuh HTML setiap kali ada pembaruan.

### Tugas 2

1. Pas user membuka projects, browser mengirim HTTP request ke server Django. Proyek menerima request lewat portofolio/urls.py, yang meneruskannya ke main/urls.py lewat include("main.urls"). Di sana pola URL projects/ dicocokkan dengan view show_projects. View memanggil Project.objects.all() buat ambil semua data dari tabel main_project di database lewat ORM Django. Hasilnya dimasukkan ke context dengan key project_list, lalu diteruskan ke render() bareng nama template projects.html. Django memproses template itu tiap {{ variable }} diganti nilai dari context dan blok {% for %}` diulang buat tiap objek Project. Hasil akhirnya dokumen HTML yang dikirim balik sebagai response dan ditampilkan browser.

2. Data proyek disimpan di model karena beberapa alasan: Pemeliharaan jadi lebih gampang, nambah atau ubah satu proyek cukup lewat shell atau admin panel tanpa nyentuh HTML sama sekali. Data yang sama juga bisa dipakai di beberapa halaman (daftar dan detail) tanpa duplikasi karena keduanya ambil dari sumber yang sama. Pas jumlah proyek nambah, template gak perlu diubah karena {% for %} udah nanganin berapapun datanya. Tanggung jawabnya: template ngurus tampilan, view ngurus logika, model ngurus data.

3. makemigrations bikin berkas migrasi berdasarkan perubahan yang kedeteksi di model Python, tapi belum ngubah database. migrate yang ngejalanin berkas itu buat ubah skema database contohnya pas nambah model Project baru, makemigrations dulu bikin 0002_project.py yang isinya instruksi bikin tabel, baru migrate yang bikin tabel main_project di database. Dua-duanya wajib dijalanin urut tiap kali ada perubahan struktur model, kayak nambah field baru atau ganti tipe data field.

### Tugas 3

1. ModelForm dipakai karena Django langsung bikin field form dari definisi model: tipe data, panjang maksimal, pilihan (choices), dan validasinya ikut ke-generate otomatis. Kalau nulis form HTML manual, semua itu harus ditulis dua kali, sekali di model dan sekali di form, jadi gampang gak sinkron pas model berubah. Di project ini ProjectForm dan ExperienceForm dipakai buat form tambah dan form edit sekaligus, bedanya cuma instance= yang diisi pas edit sehingga field-nya otomatis ke-prefill. {% csrf_token %} wajib ada karena Django nyimpen token rahasia per sesi dan ngecek token itu di tiap request POST. Tujuannya biar request yang masuk beneran berasal dari form di situs kita sendiri, bukan dari situs lain yang diam-diam nyuruh browser pengguna ngirim POST (serangan CSRF). Tanpa token, CsrfViewMiddleware nolak request dengan error 403 Forbidden.

2. JSON lebih disukai karena lebih ringkas: XML wajib nulis tag pembuka dan penutup buat tiap field, sedangkan JSON cukup pasangan key-value. Ukuran datanya lebih kecil dan lebih cepat di-parse. JSON juga langsung kebaca di JavaScript lewat JSON.parse() atau response.json() tanpa parser tambahan, dan strukturnya (objek, array, string, angka, boolean, null) nyambung langsung ke tipe data di hampir semua bahasa pemrograman, jadi gampang dipakai antar layanan. XML masih dipakai di sistem lama dan enterprise, tapi buat API web modern JSON udah jadi standarnya. Contohnya bisa dilihat sendiri dengan bandingin /api/experience/ (JSON) sama /api/experience/xml/: isinya sama tapi versi XML jauh lebih panjang.

3. Pas /experience/ dibuka, show_experience manggil get_experience_json dulu. Fungsi itu ngambil semua objek lewat Experience.objects.all(), terus di-serialize pakai serializers.serialize("json", ...) dan dikembalikan sebagai HttpResponse dengan content_type="application/json". Selanjutnya show_experience ngebaca isi response itu dan di-deserialize pakai serializers.deserialize("json", ...) jadi objek model lagi, baru dikirim ke template lewat context. Serialization perlu karena objek model Django itu instance Python yang hidup di memori server dan gak bisa langsung dikirim lewat HTTP, sedangkan HTTP cuma bisa bawa teks atau bytes. Serializer ngubah objek itu jadi teks JSON yang formatnya baku dan bisa dibaca client apapun (Postman, JavaScript, aplikasi lain), sementara content_type ngasih tau client cara bacanya.

### AI Disclosure

Dalam mengerjakan tugas ini saya menggunakan bantuan AI, yaitu Claude (lewat Claude Code), pada bagian berikut:

- Menyiapkan struktur awal proyek Django: mengganti nama folder konfigurasi menjadi portofolio, wiring views/urls/templates/static, serta konfigurasi WhiteNoise agar static file dilayani di produksi.
- Membantu membuatkan struktur HTML5 dan CSS3 untuk tiap section (layout Grid dan Flexbox, timeline Experience, kartu Skills, carousel Projects).
- Setelah dosen mengizinkan pemakaian JavaScript dan CSS framework di Tugas 1, saya minta dibantu menambahkan interaktivitas yang tadinya tidak mungkin murni pakai CSS: efek scroll-parallax di tiap section, carousel Projects dengan tombol panah dan dot indicator, efek tilt 3D pada ID card yang mengikuti gerakan mouse, dan efek hover di kartu Skills yang saling melebar-mengecil. Saya sempat mempertimbangkan Tailwind CSS juga, tapi saya putuskan tidak dipakai karena desain custom yang sudah ada sudah cukup rapi dan mengganti semuanya ke utility class berisiko merusak hasil yang sudah pas tanpa manfaat fungsional tambahan.
- Membantu proses responsivitas untuk breakpoint tablet dan mobile, kompresi aset video hero, dan kompresi foto Experience serta Projects supaya ukurannya wajar untuk web.

Seluruh isi konten (bio, daftar skill, riwayat pengalaman, riwayat pendidikan, daftar proyek, dan jawaban pertanyaan reflektif di atas) saya tulis dan verifikasi sendiri. Pemilihan skema warna, tipografi, tata letak akhir, aset ID card/lanyard, dan foto-foto asli yang dipakai (Experience, Projects, gedung Fasilkom) saya siapkan sendiri. Proses prompting dilakukan secara iteratif: saya kasih arahan desain lewat kata-kata dan kadang screenshot hasil yang salah, AI mencoba, saya tinjau langsung di browser saya sendiri, lalu minta perbaikan spesifik sampai sesuai yang saya mau.

Untuk Tugas 2, saya pakai Claude buat bantu bikin struktur basic model Project, view show_projects dan show_project_detail, routing URL-nya, template projects.html dan project_detail.html, CSS tambahan, serta unit test ProjectTest.

Untuk Tugas 3, saya pakai Claude Code (di terminal/VS Code) buat ngerjain refactor template ke base.html, ProjectForm dan ExperienceForm, view create/update/delete plus endpoint JSON dan XML buat Experience dan Project, template form, tombol edit dan hapus dengan modal konfirmasi, CSS-nya, dan unit test. Cara promptnya: saya kasih teks tutorial dan spek tugas lengkap, minta AI ngerjain per bagian, lalu tiap hasilnya saya jalanin dan cek sendiri di browser sebelum lanjut. Command git buat tiap commit juga saya jalanin manual sendiri.

### Keterbatasan AI yang saya temui dan perbaikan manual yang saya lakukan

- Desain awal dari AI kelihatan generik: kartu Skills versi pertama cuma kotak putih dengan angka kecil, terasa seperti template SaaS biasa. Saya minta rombak berkali-kali sampai jadi kartu gelap asimetris dengan efek saling melebar pas di-hover, yang jauh lebih terasa personal.
- AI tidak bisa melihat hasil render sebenarnya tanpa dites: waktu saya minta foto Experience dan Projects dipasang, AI sempat memaksa semua foto ke rasio kotak yang sama padahal rasio asli tiap foto beda jauh, hasilnya foto jadi ter-zoom parah dan tidak jelas isinya sampai saya screenshot dan tunjukkan langsung baru diperbaiki jadi object-fit: contain.
- Sempat ada "bug" yang ternyata bukan bug: pas saya buka hero section, ID card-nya tampil raksasa dan pecah. Setelah ditelusuri ternyata itu cache browser yang belum ke-refresh, bukan kesalahan kode. Saya baru yakin setelah minta AI menguji ulang dengan ukuran layar persis yang sama dan hasilnya normal.
- Ukuran elemen hasil AI sering perlu dikoreksi manual di perangkat nyata: ID card di Hero versi mobile sempat kepanjangan sampai menutupi teks, lalu setelah dikecilkan malah kelihatan kekecilan dengan jarak kosong yang aneh. Saya minta disesuaikan sampai pas, dan akhirnya saya putuskan sendiri untuk mode mobile ID card di Hero dihilangkan saja karena tidak menambah nilai dan malah bikin ramai.
- Form edit Experience awalnya pasti gagal validasi: field thumbnail bertipe URLField, padahal data aslinya berupa path static (/static/img/exp-photos/...), jadi Django selalu bilang "Enter a valid URL" bahkan pas cuma ganti judul. Ini ketemu pas dites, lalu field-nya saya ubah jadi CharField lewat migrasi baru.
- Widget datetime-local butuh format YYYY-MM-DDTHH:MM, sedangkan default Django nge-render spasi, jadi kolom "Tanggal Selesai" kosong tiap kali form edit dibuka. Saya benerin dengan nentuin format di widget dan nulis test khusus buat ngecek prefill-nya.
- Tombol edit dan hapus di card Experience awalnya sempat gak bisa diklik: pointer-events: none yang saya pasang biar tombol gak ke-klik pas card masih transparan ikut ke-inherit ke modal konfirmasi. Ketahuan dari test browser otomatis yang nunjukin request POST-nya gak pernah kekirim, lalu aturannya dipersempit ke tombol pemicunya aja.

Kesimpulan yg saya dapat: AI cukup berguna untuk mempercepat penulisan kode dan eksplorasi ide desain, tapi tidak bisa dipercaya begitu saja soal selera desain, hasil visual sebenarnya di berbagai ukuran layar/browser, dan menjaga dokumentasi tetap sinkron dengan kode. Bagian-bagian itu tetap saya yang mengevaluasi, menguji di perangkat/browser saya sendiri, dan memutuskan versi akhirnya.
