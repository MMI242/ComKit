<template>
  <div class="min-h-screen bg-gray-50 pt-16">
    <div class="max-w-4xl mx-auto px-4 py-8">
      <div class="bg-white rounded-lg shadow-sm p-6 md:p-8">
        <h1 class="text-3xl font-bold text-gray-900 mb-6">Terms and Conditions</h1>

        <div class="prose max-w-none">

          <section class="mb-8">
            <h2 class="text-xl font-semibold text-gray-800 mb-4">Privacy Policy</h2>
            <div class="text-gray-600 leading-relaxed space-y-4">
              <p>
                Kami mengumpulkan data anda untuk menunjang penyediaan layanan. Dengan menggunakan layanan ini, berarti anda telah membaca, memahami, dan setuju dengan pengumpulan dan penggunaan informasi yang sesuai dengan dokumen kebijakan privasi ini.
              </p>
              <p>
                Bila anda menyediakan data pribadi yang berkaitan dengan individu lain (seperti data pribadi yang berkaitan dengan pasangan anda, anggota keluarga, atau pihak lain) kepada kami, maka anda menyatakan dan menjamin bahwa anda telah memperoleh persetujuan dari individu yang bersangkutan serta (atas nama individu tersebut) menyetujui pemrosesan data pribadi oleh kami.
              </p>
              
              <h3 class="text-lg font-medium text-gray-800 mt-6 mb-3">BAGAIMANA KAMI MENGGUNAKAN DATA ANDA</h3>
              <p>
                Kami menggunakan data pribadi anda untuk mengatur dan mengelola akun anda, berkomunikasi dengan anda, serta untuk menyediakan berbagai fitur, layanan dan fungsi bagi anda pada aplikasi kami.
              </p>
              
              <h3 class="text-lg font-medium text-gray-800 mt-6 mb-3">KEAMANAN DATA</h3>
              <p>
                Kami akan memberlakukan upaya terbaik untuk melindungi dan mengamankan Data Pribadi anda dari akses, pengumpulan, penggunaan atau pengungkapan oleh orang-orang yang tidak berwenang dan dari pengolahan yang bertentangan dengan hukum, kehilangan yang tidak disengaja, pemusnahan dan kerusakan atau risiko serupa. Namun, dikarenakan pengiriman data melalui internet tidak sepenuhnya aman, Kami tidak dapat sepenuhnya menjamin bahwa Data Pribadi tersebut tidak akan dicegat, diakses, diungkapkan, diubah atau dihancurkan oleh pihak ketiga yang tidak berwenang, karena faktor-faktor di luar kendali kami. Anda bertanggung jawab untuk menjaga kerahasiaan detail akun anda dan anda wajib untuk tidak membagikan detail akun anda, termasuk kata sandi anda dengan siapapun, dan anda harus selalu menjaga dan bertanggung jawab atas keamanan perangkat yang Anda gunakan.
              </p>
              
              <h3 class="text-lg font-medium text-gray-800 mt-6 mb-3">DATA PRIBADI APA YANG DIKUMPULKAN DAN DIPROSES</h3>
              <ul class="list-disc list-inside space-y-1">
                <li>nama lengkap</li>
                <li>alamat surel (e-mail) pribadi</li>
                <li>Jenis kelamin</li>
                <li>Lokasi</li>
              </ul>
              
              <p class="mt-3">
                <strong>ComKit AKAN MENGGUNAKAN INFORMASI INI UNTUK TUJUAN:</strong>
              </p>
              <ul class="list-disc list-inside space-y-1">
                <li>mengautentikasi pengguna</li>
                <li>memberikan hak akses terhadap pengguna untuk menggunakan fitur yang kami sediakan</li>
              </ul>
              
              <h3 class="text-lg font-medium text-gray-800 mt-6 mb-3">PENGUNGKAPAN DATA PRIBADI</h3>
              <p>
                ComKit tidak akan mengalihkan, menjual, mendistribusikan, mengungkapkan atau meminjamkan informasi dan juga Data Pribadi Anda kepada pihak ketiga lain kecuali Apabila diharuskan oleh hukum atau kepatuhan terhadap hukum (legal compliance) berdasarkan peraturan perundang-undangan yang berlaku.
              </p>
              
              <h3 class="text-lg font-medium text-gray-800 mt-6 mb-3">AKSES DAN KOREKSI INFORMASI PRIBADI</h3>
              <p>
                Tunduk pada peraturan perundang-undangan yang berlaku, anda dapat meminta kepada kami untuk mengakses dan/atau mengoreksi Informasi Pribadi anda yang berada dalam kepemilikan dan penguasaan kami.
              </p>
              <p>
                Kami berhak menolak permintaan anda untuk mengakses, atau untuk memperbaiki, sebagian atau semua Informasi Pribadi anda yang kami miliki atau kuasai jika diizinkan atau diperlukan berdasarkan perundang-undangan yang berlaku. Hal ini termasuk dalam keadaan di mana Informasi Pribadi tersebut dapat berisi referensi kepada orang lain atau di mana permintaan untuk akses atau permintaan untuk mengoreksi adalah untuk alasan yang kami anggap tidak relevan.
              </p>
              
              <h3 class="text-lg font-medium text-gray-800 mt-6 mb-3">HUBUNGI KAMI</h3>
              <p>
                Apabila Anda memiliki pertanyaan atau masalah tentang praktik privasi kami mohon hubungi kami melalui e-mail di <a href="mailto:support@comkit.com" class="text-primary-600 hover:text-primary-800 underline">support@comkit.com</a>
              </p>
            </div>
          </section>

          <div class="mt-8 pt-6 border-t border-gray-200">
            <p class="text-sm text-gray-500 text-center">
              Last updated: {{ new Date().toLocaleDateString() }}
            </p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
// Terms and Conditions page
useHead({
  title: 'Terms and Conditions - ComKit'
})
</script>
