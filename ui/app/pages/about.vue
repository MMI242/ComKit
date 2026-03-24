<template>
  <div class="min-h-screen bg-gray-50 pt-16">
    <div class="max-w-4xl mx-auto px-4 py-8">
      <div class="bg-white rounded-lg shadow-sm p-6 md:p-8">
        <h1 class="text-3xl font-bold text-gray-900 mb-6">Tentang ComKit</h1>
        
        <!-- Hero Image -->
        <div class="mb-8 mt-8 pt-8">
          <img 
            src="/images/img.png"
            alt="ComKit - Berbagi Peralatan Dapur" 
            class="w-full object-cover"
          />
        </div>
        
        <div class="prose max-w-none">
          <section class="mb-8">
            <h2 class="text-xl font-semibold text-gray-800 mb-4">Apa itu ComKit?</h2>
            <p class="text-gray-600 leading-relaxed">
              ComKit adalah aplikasi berbagi peralatan dapur yang inovatif yang dirancang untuk menghubungkan 
              komunitas lokal melalui praktik berbagi yang berkelanjutan. Kami percaya bahwa banyak peralatan 
              dapur yang sering digunakan hanya sesekali dapat dibagikan kepada tetangga dan teman-teman, 
              mengurangi pembelian yang tidak perlu dan membangun hubungan yang lebih kuat dalam komunitas.
            </p>
          </section>

          <section class="mb-8">
            <h2 class="text-xl font-semibold text-gray-800 mb-4">Visi Kami</h2>
            <p class="text-gray-600 leading-relaxed">
              Visi kami adalah menciptakan ekosistem berbagi yang inklusif di mana setiap rumah tangga dapat 
              mengakses peralatan dapur yang mereka butuhkan tanpa harus membeli semuanya. Kami ingin mengurangi 
              limbah konsumsi dan mendorong gaya hidup berkelanjutan melalui teknologi yang memudahkan 
              interaksi komunitas.
            </p>
          </section>

          <section class="mb-8">
            <h2 class="text-xl font-semibold text-gray-800 mb-4">Misi Kami</h2>
            <div class="space-y-3">
              <div class="flex items-start">
                <div class="flex-shrink-0">
                  <div class="flex items-center justify-center h-8 w-8 rounded-full bg-primary-100 text-primary-600 font-semibold text-sm">
                    1
                  </div>
                </div>
                <div class="ml-4">
                  <h3 class="text-lg font-medium text-gray-800">Menghubungkan Komunitas</h3>
                  <p class="text-gray-600">Memfasilitasi koneksi antar tetangga untuk berbagi peralatan dapur dengan aman dan mudah.</p>
                </div>
              </div>
              
              <div class="flex items-start">
                <div class="flex-shrink-0">
                  <div class="flex items-center justify-center h-8 w-8 rounded-full bg-primary-100 text-primary-600 font-semibold text-sm">
                    2
                  </div>
                </div>
                <div class="ml-4">
                  <h3 class="text-lg font-medium text-gray-800">Mengurangi Limbah</h3>
                  <p class="text-gray-600">Menurunkan jumlah peralatan dapur yang tidak terpakai dan mengurangi pembelian yang tidak perlu.</p>
                </div>
              </div>
              
              <div class="flex items-start">
                <div class="flex-shrink-0">
                  <div class="flex items-center justify-center h-8 w-8 rounded-full bg-primary-100 text-primary-600 font-semibold text-sm">
                    3
                  </div>
                </div>
                <div class="ml-4">
                  <h3 class="text-lg font-medium text-gray-800">Mendorong Keberlanjutan</h3>
                  <p class="text-gray-600">Mendorong gaya hidup berkelanjutan dan konsumsi yang bertanggung jawab dalam kehidupan sehari-hari.</p>
                </div>
              </div>
            </div>
          </section>

          <section class="mb-8">
            <h2 class="text-xl font-semibold text-gray-800 mb-4">Fitur Utama</h2>
            <div class="grid md:grid-cols-2 gap-6">
              <div class="bg-gray-50 p-4 rounded-lg">
                <h3 class="font-semibold text-gray-800 mb-2">🔍 Pencarian Mudah</h3>
                <p class="text-gray-600 text-sm">Temukan peralatan dapur yang Anda butuhkan dengan sistem pencarian yang intuitif.</p>
              </div>
              
              <div class="bg-gray-50 p-4 rounded-lg">
                <h3 class="font-semibold text-gray-800 mb-2">📅 Sistem Booking</h3>
                <p class="text-gray-600 text-sm">Jadwalkan peminjaman peralatan dengan sistem reservasi yang terintegrasi.</p>
              </div>
              
              <div class="bg-gray-50 p-4 rounded-lg">
                <h3 class="font-semibold text-gray-800 mb-2">📍 Lokasi Terdekat</h3>
                <p class="text-gray-600 text-sm">Temukan peralatan dapur dari tetangga terdekat. Hemat waktu dan tenaga dengan akses mudah ke barang yang Anda butuhkan tanpa harus pergi jauh.</p>
              </div>
              
              <div class="bg-gray-50 p-4 rounded-lg">
                <h3 class="font-semibold text-gray-800 mb-2">💬 Pesan Langsung</h3>
                <p class="text-gray-600 text-sm">Komunikasi langsung dengan pemilik peralatan untuk koordinasi yang mudah.</p>
              </div>
              
              <div class="bg-gray-50 p-4 rounded-lg">
                <h3 class="font-semibold text-gray-800 mb-2">🤖 AI Resep</h3>
                <p class="text-gray-600 text-sm">Buat resep makanan dari bahan terbatas yang tersedia dengan bantuan AI yang cerdas. Hemat waktu dan dapatkan inspirasi masakan baru.</p>
              </div>
              
              <div class="bg-gray-50 p-4 rounded-lg">
                <h3 class="font-semibold text-gray-800 mb-2">📱 Notifikasi</h3>
                <p class="text-gray-600 text-sm">Dapatkan pemberitahuan tentang ketersediaan peralatan dan status peminjaman secara real-time.</p>
              </div>
            </div>
          </section>

          <section class="mb-8">
            <h2 class="text-xl font-semibold text-gray-800 mb-4">Cara Kerja ComKit</h2>
            <div class="space-y-4">
              <div class="flex items-center space-x-3">
                <div class="flex-shrink-0 w-8 h-8 bg-primary-500 text-white rounded-full flex items-center justify-center font-semibold">
                  1
                </div>
                <p class="text-gray-600"><strong>Daftar</strong> - Buat akun Anda secara gratis dan lengkapi profil Anda.</p>
              </div>
              
              <div class="flex items-center space-x-3">
                <div class="flex-shrink-0 w-8 h-8 bg-primary-500 text-white rounded-full flex items-center justify-center font-semibold">
                  2
                </div>
                <p class="text-gray-600"><strong>Bagikan</strong> - Daftarkan peralatan dapur yang ingin Anda bagikan dengan komunitas.</p>
              </div>
              
              <div class="flex items-center space-x-3">
                <div class="flex-shrink-0 w-8 h-8 bg-primary-500 text-white rounded-full flex items-center justify-center font-semibold">
                  3
                </div>
                <p class="text-gray-600"><strong>Pinjam</strong> - Cari dan pinjam peralatan yang Anda butuhkan dari tetangga terdekat.</p>
              </div>
              
              <div class="flex items-center space-x-3">
                <div class="flex-shrink-0 w-8 h-8 bg-primary-500 text-white rounded-full flex items-center justify-center font-semibold">
                  4
                </div>
                <p class="text-gray-600"><strong>Nikmati</strong> - Gunakan peralatan dan kembalikan tepat waktu sambil membangun hubungan komunitas.</p>
              </div>
            </div>
          </section>

          <section class="mb-8">
            <h2 class="text-xl font-semibold text-gray-800 mb-4">Tim Kami</h2>
            <p class="text-gray-600 leading-relaxed">
              ComKit dikembangkan oleh tim yang berdedikasi untuk menciptakan solusi teknologi yang berdampak positif 
              bagi masyarakat. Kami terinspirasi dari pengalaman pribadi dalam melihat banyak peralatan dapur yang 
              tidak terpakai di rumah-rumah, sementara tetangga di sekitarnya membutuhkan peralatan yang sama untuk 
              penggunaan jangka pendek.
            </p>
          </section>

          <section class="mb-8">
            <h2 class="text-xl font-semibold text-gray-800 mb-4">Hubungi Kami</h2>
            <p class="text-gray-600 leading-relaxed">
              Kami selalu terbuka untuk masukan, saran, dan kerjasama. Jika Anda memiliki pertanyaan atau ingin 
              berkolaborasi dengan kami, jangan ragu untuk menghubungi:
            </p>
            <div class="mt-4 space-y-2">
              <p class="text-gray-600">
                <strong>Email:</strong> <a href="mailto:info@comkit.com" class="text-primary-600 hover:text-primary-800 underline">info@comkit.com</a>
              </p>
              <p class="text-gray-600">
                <strong>WhatsApp:</strong> +62 812-3456-7890
              </p>
              <p class="text-gray-600">
                <strong>Alamat:</strong> Jl. Bulaksumur, Caturtunggal, Kapanewon Depok, Kabupaten Sleman, Daerah Istimewa Yogyakarta 55281, Indonesia
              </p>
            </div>
          </section>

          <div class="mt-8 pt-6 border-t border-gray-200">
            <p class="text-sm text-gray-500 text-center">
              © 2024 ComKit. Membangun komunitas yang berkelanjutan melalui berbagi peralatan dapur.
            </p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
// About page
useHead({
  title: 'Tentang Kami - ComKit'
})
</script>
