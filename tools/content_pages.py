"""Teacher page, FAQ, About and blog posts. Body text is simple HTML (trusted, written here)."""

TEACHERS = {
    'slug': 'ogretmenler', 'title': 'Sınıfça DrawBird',
    'desc': 'Öğretmenler için 40 dakikalık DrawBird ders planı: kuşları tanı, çiz, ortak gökyüzüne sal. Çocuk güvenliği nasıl sağlanıyor?',
    'html': '''
<p>DrawBird, bir sınıfın birlikte çizip aynı gökyüzünde uçurduğu kuşlarla <b>gözlem, çizim ve doğa bilgisini</b> birleştiren ücretsiz bir etkinliktir. Üyelik, e-posta ya da kurulum gerektirmez; tahtaya yansıtılan bir tarayıcı ve öğrencilerin tablet ya da bilgisayarları yeterlidir.</p>

<h2>Hangi yaşlar için?</h2>
<p>Çizim kısmı okul öncesinden itibaren herkese uygundur. Kuş bilgisi bölümleri ilkokul 2. sınıf ve üstü için hazırlandı. Ortaokulda "canlıların sınıflandırılması", "göç" ve "habitat" konularına bağlanabilir.</p>

<h2>40 dakikalık ders planı</h2>
<ol class="steps">
  <li><b>Isınma (5 dk):</b> Okul bahçesinde ya da pencereden görülen kuşları sorun. Tahtaya listeleyin. Ardından <a href="/kuslar/">Türkiye'nin kuşları</a> sayfasından birini birlikte okuyun.</li>
  <li><b>Gözlem (5 dk):</b> Seçilen kuşun gaga biçimini, kanat uzunluğunu, kuyruğunu konuşun. "Bu gaga ne yemeye yarar?" sorusu iyi bir başlangıçtır.</li>
  <li><b>Çizim dersi (10 dk):</b> <a href="/dersler/">Çizim derslerinden</a> birini yansıtın ve adımları birlikte izleyin. Kesik çizginin anlamını açıklayın: üstü kanat olarak çırpar, altı gövde olarak kalır.</li>
  <li><b>Herkes çizer (10 dk):</b> Her öğrenci kendi kuşunu çizer, ona bir ad verir ve "uçur!" düğmesine basar.</li>
  <li><b>Ortak gökyüzü (7 dk):</b> Tahtadaki ekranda Gökyüzü sekmesini açın. Kuşlar geldikçe sınıf birbirinin kuşunu tanır. "Yem modu" ile yem atmak her zaman kahkaha getirir.</li>
  <li><b>Kapanış (3 dk):</b> "Kuşun neden böyle bir gagası var?" sorusuyla günü bağlayın. Ödev olarak evden bir kuş gözlemi isteyebilirsiniz.</li>
</ol>

<h2>Önemli: ilk kuşlar onay bekler</h2>
<p>DrawBird'ü her yaştan çocuk kullanabilsin diye <b>yeni kuşçuların ilk iki kuşu bir yönetici bakana kadar yalnız çizen kişiye görünür</b>. Bu yüzden sınıfta ilk kez çizilen kuşlar ortak gökyüzünde hemen görünmeyebilir; öğrenciler kendi ekranlarında yine kendi kuşlarını görür. Dersten bir gün önce kendi tarayıcınızda iki kuş çizip onaylatmak, ortak ekranı canlı tutmanın en kolay yoludur.</p>

<h2>Çocuk güvenliği</h2>
<ul>
  <li>Ad, e-posta, telefon ya da şifre istenmez. Öğrencilerin kuşçu adına gerçek adlarını yazmamasını hatırlatın.</li>
  <li>Kuş, kuşçu ve sürü adlarında uygunsuz kelimeler otomatik engellenir.</li>
  <li>Her kuş "Bildir" ile işaretlenebilir; uygunsuz çizimler gökyüzünden iner ve yöneticiye gider.</li>
  <li>Reklam, sohbet ya da özel mesajlaşma yoktur.</li>
  <li>Ayrıntılar: <a href="/kosullar">kullanım koşulları</a>, <a href="/gizlilik">gizlilik</a> ve <a href="/kvkk">KVKK aydınlatma metni</a>.</li>
</ul>

<h2>Pratik ipuçları</h2>
<ul>
  <li>Tabletlerde parmakla çizmek kolaydır; kalınlığı 8–10 yapın.</li>
  <li>Bütün sınıf aynı ağdan bağlandığı için çok hızlı ardışık gönderimlerde "Biraz yavaş!" uyarısı çıkabilir; bir dakika beklemek yeterlidir.</li>
  <li>Bir sürü kurup sınıfın kuşlarını içine ekleyin, linkini velilerle paylaşın: "5-B sınıfının gökyüzü".</li>
  <li>Kalabalık bir sınıfta Gökyüzü sekmesindeki "Kuş sayısı"nı 40'a çıkarın.</li>
</ul>
''',
}

FAQ = {
    'slug': 'sss', 'title': 'Sık sorulan sorular',
    'desc': 'DrawBird hakkında sık sorulan sorular: üyelik, kuşum neden görünmüyor, başka cihaz, silme, güvenlik.',
    'items': [
        ('DrawBird ücretli mi?', 'Hayır, tamamen ücretsiz. Ödeme, abonelik ya da uygulama içi satın alma yok.'),
        ('Üye olmam gerekiyor mu?', 'Hayır. Sayfayı açtığın an çizebilirsin. Tarayıcın senin için rastgele bir cihaz kodu üretir; e-posta ya da şifre istemeyiz.'),
        ('Kuşum neden gökyüzünde görünmüyor?', 'Yeni kuşçuların ilk iki kuşu, bir yönetici bakana kadar yalnız çizene görünür. Bu, siteyi her yaştan kullanıcı için güvenli tutmak içindir. İki kuşun onaylandıktan sonra sonraki kuşların hemen uçar.'),
        ('Kuşum neden kanat çırpmıyor?', 'Çizim alanındaki kesik çizginin üstü kanat olarak çırpar, altı gövde olarak sabit kalır. Kanatları çizginin üstüne çizmeyi dene. <a href="/dersler/">Çizim dersleri</a> bunu adım adım gösteriyor.'),
        ('Kaç kuş çizebilirim?', 'Aynı anda en fazla 8 kuşun olabilir. Yeni bir kuş için Profil sayfasından eskilerden birini silebilirsin.'),
        ('Kuşlarımı telefonumda da görebilir miyim?', 'Evet. Profil sayfasındaki kurtarma kodunu kopyala, telefonunda DrawBird\'ü açıp Profil → Kodla giriş alanına yapıştır. Kodu kimseyle paylaşma.'),
        ('Tarayıcımın verilerini silersem ne olur?', 'Cihaz kodun silinir ve kuşlarına bu cihazdan ulaşamazsın. Kurtarma kodunu önceden kaydettiysen yeniden girebilirsin.'),
        ('Uygunsuz bir çizim gördüm, ne yapmalıyım?', 'Kuşa dokun ve "Bildir"e bas. Üç bildirim alan kuş (ilk gününde iki) gökyüzünden hemen iner ve yöneticiye gider.'),
        ('Verilerimi nasıl silerim?', 'Profil sayfasındaki "Tüm verilerimi sil" düğmesi kuşlarını, oylarını, bildirimlerini, sürülerini ve kuşçu adını kalıcı olarak siler.'),
        ('Çizimlerimin hakları kime ait?', 'Sana. DrawBird yalnız sitede gösterme ve paylaşım linklerinde önizleme izni alır; çizimini satmaz, ürüne basmaz. Ayrıntılar <a href="/kosullar">kullanım koşullarında</a>.'),
        ('Hangi dilleri destekliyor?', 'Oyun 11 dilde: Türkçe, İngilizce, İspanyolca, Portekizce, Fransızca, Almanca, Rusça, Arapça, Çince, Japonca ve Endonezce. Dil tarayıcına göre seçilir, menüden değiştirebilirsin.'),
        ('DrawBird\'ü telefona uygulama gibi ekleyebilir miyim?', 'Evet. Tarayıcının menüsünden "Ana ekrana ekle"yi seç; DrawBird bir uygulama gibi açılır.'),
        ('Kaynak kodu açık mı?', 'Evet, AGPL-3.0 lisansıyla <a href="https://github.com/gunayboss/drawbird">GitHub\'da</a>.'),
    ],
}

ABOUT = {
    'slug': 'hakkinda', 'title': 'DrawBird hakkında',
    'desc': 'DrawBird nedir, kim yaptı, neden var? Herkesin çizdiği kuşların aynı gökyüzünde uçtuğu ücretsiz, açık kaynak bir çizim oyunu.',
    'html': '''
<p>DrawBird, herkesin çizdiği kuşların aynı gökyüzünde kanat çırparak uçtuğu küçük bir çizim oyunudur. Bir kuş çizersin, adını koyarsın, "uçur!" dersin; birkaç saniye sonra kuşun dünyanın dört bir yanından gelen kuşlarla birlikte uçar.</p>

<h2>Neden?</h2>
<p>Çizmenin iyi olmak zorunda olmadığı, kimsenin puan peşinde koşmadığı, sadece bir şey yapıp paylaşmanın keyfini yaşatan bir yer istedik. Kuşları seçtik çünkü herkes bir kuş çizebilir, her çocuk bir kuş görmüştür ve kuşlar uçar: insanın çizdiği bir şeyin canlanıp gitmesi küçük ama gerçek bir sevinçtir.</p>
<p>Oyunun yanında kuşları tanımayı da önemsiyoruz. <a href="/kuslar/">Türkiye'nin kuşları</a> sayfalarında balkonundan görebileceğin kuşları, <a href="/dersler/">çizim derslerinde</a> onları adım adım nasıl çizeceğini anlatıyoruz.</p>

<h2>İlkelerimiz</h2>
<ul>
  <li><b>Ücretsiz ve üyeliksiz.</b> E-posta, şifre ya da gerçek ad istemeyiz.</li>
  <li><b>Her yaşa güvenli.</b> Yeni kuşçuların ilk kuşları onaydan geçer, uygunsuz adlar engellenir, her kuş bildirilebilir.</li>
  <li><b>Az veri.</b> Yalnız oyunun çalışması için gereken veriyi tutarız; çerez ve takip aracı kullanmayız.</li>
  <li><b>Açık kaynak.</b> Kodun tamamı <a href="https://github.com/gunayboss/drawbird">GitHub'da</a>, AGPL-3.0 lisansıyla.</li>
</ul>

<h2>İlham</h2>
<p>Fikir, Alden Hallak'ın balık çizme oyunu DrawAFish'ten esinlendi. DrawBird'ün kodu sıfırdan yazıldı; DrawAFish'in kodu, görselleri ya da modeli kullanılmadı.</p>

<h2>Kim yaptı?</h2>
<p>DrawBird Türkiye'de, bağımsız bir geliştirici tarafından yapılıyor. Öneri, hata bildirimi ve iş birliği için <a href="https://github.com/gunayboss/drawbird/issues">GitHub üzerinden</a> yazabilirsin.</p>
''',
}

POSTS = [
    {
        'slug': '2026-11-drawbird-yayinda', 'date': '2026-11-02', 'title': 'DrawBird yayında: ilk ayın notları',
        'desc': 'DrawBird yayına çıktı. Neler yaptık, gökyüzünde neler oluyor, sırada ne var?',
        'html': '''
<p>DrawBird yayında! Bu yazıda ilk haftalarda neler yaptığımızı, gökyüzünü güvenli tutmak için nelere dikkat ettiğimizi ve sırada ne olduğunu anlatıyoruz.</p>

<h2>Gökyüzünde ilk kuşlar</h2>
<p>İlk kuşlar yayının ilk saatlerinde uçmaya başladı: kırmızı bir kumru, sarı gagalı serçeler, birkaç cesur martı denemesi. En çok sevdiğimiz şey, kuşların ne kadar farklı olduğu. Kimisi gerçekçi, kimisi tek çizgiyle çizilmiş bir "V". Hepsi aynı gökyüzünde aynı hevesle kanat çırpıyor.</p>

<h2>Neleri ekledik?</h2>
<ul>
  <li><b>11 dil.</b> Oyun artık Türkçe, İngilizce, İspanyolca, Portekizce, Fransızca, Almanca, Rusça, Arapça, Çince, Japonca ve Endonezce oynanabiliyor.</li>
  <li><b>Sürüler.</b> Sevdiğin kuşları bir sürüde toplayıp gökyüzünde yalnız onları izleyebilir, linkini paylaşabilirsin.</li>
  <li><b>Yem atma.</b> Gökyüzünde bir yere yem bırak, yakındaki kuşlar gelip gagalasın.</li>
  <li><b>Çizim dersleri ve kuş sayfaları.</b> <a href="/dersler/">10 çizim dersi</a> ve <a href="/kuslar/">Türkiye'den 20 kuş</a> hazır.</li>
</ul>

<h2>Güvenli bir gökyüzü</h2>
<p>DrawBird'ü çocuklar da kullanıyor. Bu yüzden yeni kuşçuların ilk iki kuşu bir insan bakana kadar yalnız çizene görünüyor; kuş, kuşçu ve sürü adlarında uygunsuz kelimeler otomatik engelleniyor; her kuş bildirilebiliyor. Bu kuralların biraz yavaşlattığını biliyoruz, ama gökyüzünün herkes için keyifli kalması daha önemli.</p>

<h2>Bu ayın çizim meydan okuması: en komik baykuş</h2>
<p>Bu ay herkesi bir baykuş çizmeye davet ediyoruz. <a href="/dersler/baykus">Baykuş dersini</a> izleyebilir ya da tamamen kendi tarzında çizebilirsin. Kuşunun adına "baykuş" yaz; ay sonunda en çok beğeni alan baykuşları <a href="/haftanin-kuslari">Haftanın kuşları</a> sayfasında öne çıkaracağız.</p>

<h2>Sırada ne var?</h2>
<p>Yeni kuş sayfaları, yeni dersler ve çizim derslerinin diğer dillere çevrilmesi. Bir önerin varsa <a href="https://github.com/gunayboss/drawbird/issues">GitHub'dan</a> yaz; her öneriyi okuyoruz.</p>
''',
    },
]
