"""Teacher page, FAQ, About and blog posts, in the DrawBird voice (see YAZIM_TARZI.md). Body text is trusted HTML written here."""

TEACHERS = {
    'slug': 'ogretmenler', 'title': 'Sınıfça DrawBird',
    'desc': 'Öğretmenler için 40 dakikalık DrawBird ders planı: kuşları tanı, çiz, ortak gökyüzüne sal. Çocuk güvenliği nasıl sağlanıyor?',
    'html': '''
<p>DrawBird'ü sınıfta kullanmak çok kolay. Üyelik yok, e-posta yok, kurulum yok. Tahtaya yansıtılan bir tarayıcı ve öğrencilerin tableti ya da bilgisayarı yeter. Her öğrenci bir kuş çiziyor, hepsi aynı gökyüzünde uçuyor. Çocuklar kendi kuşunu bulunca sınıfın havası değişiyor.</p>

<h2>Hangi yaşlar için?</h2>
<p>Çizim kısmı okul öncesinden itibaren herkese uygun. Kuş bilgisi olan sayfalar ilkokul 2. sınıf ve üstü için. Ortaokulda "canlıların sınıflandırılması", "göç" ve "yaşam alanı" konularına bağlayabilirsin.</p>

<h2>40 dakikalık ders planı</h2>
<ol class="steps">
  <li><b>Isınma (5 dk):</b> Okul bahçesinde ya da pencereden hangi kuşları gördüklerini sor, tahtaya yaz. Sonra <a href="/kuslar/">Türkiye'nin kuşları</a> sayfasından birini birlikte okuyun.</li>
  <li><b>Gözlem (5 dk):</b> Seçtiğiniz kuşun gagasına, kanadına, kuyruğuna bakın. "Bu gaga ne yemeye yarıyor?" diye sor. Genelde güzel bir sohbet çıkıyor.</li>
  <li><b>Çizim dersi (10 dk):</b> <a href="/dersler/">Çizim derslerinden</a> birini yansıt, adımları beraber izleyin. Kesik çizgiyi anlat: üstü kanat gibi çırpıyor, altı gövde olarak kalıyor.</li>
  <li><b>Herkes çizsin (10 dk):</b> Her öğrenci kendi kuşunu çizsin, bir isim versin ve "uçur!"a bassın.</li>
  <li><b>Ortak gökyüzü (7 dk):</b> Tahtada Gökyüzü sekmesini aç. Kuşlar geldikçe sınıf birbirinin kuşunu tanıyor. Yem modunu açıp yem atarsan kahkaha garanti.</li>
  <li><b>Kapanış (3 dk):</b> "Senin kuşunun gagası neden öyle?" diye sorup günü bağla. İstersen ödev olarak evden bir kuş gözlemi iste.</li>
</ol>

<h2>Önemli: ilk kuşlar onay bekliyor</h2>
<p>DrawBird'ü her yaştan çocuk kullanabilsin diye <b>yeni kuşçuların ilk iki kuşu bir yönetici bakana kadar sadece çizen kişiye görünüyor</b>. Yani sınıfta ilk kez çizilen kuşlar ortak gökyüzüne hemen düşmeyebilir. Öğrenciler kendi ekranında yine kendi kuşunu görür. Ortak ekranın boş kalmaması için dersten bir gün önce kendi tarayıcında iki kuş çizip onaylatman yeterli.</p>

<h2>Çocuk güvenliği</h2>
<ul>
  <li>Ad, e-posta, telefon ya da şifre istenmiyor. Öğrencilere kuşçu adına gerçek adlarını yazmamalarını hatırlat.</li>
  <li>Kuş, kuşçu ve sürü adlarındaki uygunsuz kelimeler otomatik engelleniyor.</li>
  <li>Her kuş "Bildir" ile işaretlenebiliyor. Uygunsuz çizimler gökyüzünden iniyor ve yöneticiye gidiyor.</li>
  <li>Reklam yok, sohbet yok, özel mesaj yok.</li>
  <li>Ayrıntılar: <a href="/kosullar">kullanım koşulları</a>, <a href="/gizlilik">gizlilik</a>, <a href="/kvkk">KVKK aydınlatma metni</a>.</li>
</ul>

<h2>Birkaç ipucu</h2>
<ul>
  <li>Tablette parmakla çizmek kolay. Kalınlığı 8–10 yap.</li>
  <li>Bir şekli tek seferde boyamak için kova aracını kullanın. Çocuklar çok seviyor.</li>
  <li>Bütün sınıf aynı ağdan bağlandığı için çok hızlı art arda gönderince "Biraz yavaş!" uyarısı çıkabilir. Bir dakika beklemek yetiyor.</li>
  <li>Bir sürü kur, sınıfın kuşlarını içine ekle ve linki velilerle paylaş. "5-B sınıfının gökyüzü" gibi.</li>
  <li>Kalabalık sınıfta Gökyüzü'ndeki "Kuş sayısı"nı 40'a çıkar.</li>
</ul>
''',
}

FAQ = {
    'slug': 'sss', 'title': 'Sık sorulan sorular',
    'desc': 'DrawBird hakkında sık sorulan sorular: üyelik, kuşum neden görünmüyor, başka cihaz, silme, güvenlik.',
    'items': [
        ('DrawBird ücretli mi?', 'Hayır, tamamen ücretsiz. Ödeme yok, abonelik yok, uygulama içi satın alma yok.'),
        ('Üye olmam gerekiyor mu?', 'Hayır. Sayfayı açtığın an çizebilirsin. Tarayıcın senin için rastgele bir kod üretiyor. E-posta ya da şifre istemiyoruz.'),
        ('Kuşum neden gökyüzünde görünmüyor?', 'Yeni kuşçuların ilk iki kuşu bir yönetici bakana kadar sadece çizene görünüyor. Siteyi her yaştan kullanıcı için güvenli tutmak için böyle. İki kuşun onaylanınca sonrakiler direkt uçuyor.'),
        ('Kuşum neden kanat çırpmıyor?', 'Çizim alanındaki kesik çizginin üstü kanat gibi çırpıyor, altı gövde olarak duruyor. Kanatları çizginin üstüne çizmeyi dene. <a href="/dersler/">Çizim dersleri</a> bunu adım adım gösteriyor.'),
        ('Bir şeklin içini nasıl boyarım?', 'Araçlardan kovayı seç, rengini seç ve şeklin içine dokun. Kapalı şeklin içi tek seferde dolar. Kenarda boşluk varsa boya dışarı taşar, o yüzden şekli kapat.'),
        ('Kaç kuş çizebilirim?', 'Aynı anda en fazla 8 kuşun olabilir. Yeni kuş için Profil\'den eskilerden birini silebilirsin.'),
        ('Kuşlarımı telefonumda da görebilir miyim?', 'Evet. Profil\'deki kurtarma kodunu kopyala, telefonda DrawBird\'ü açıp Profil → Kodla giriş\'e yapıştır. Kodu kimseyle paylaşma.'),
        ('Tarayıcımın verilerini silersem ne olur?', 'Cihaz kodun silinir ve kuşlarına o cihazdan ulaşamazsın. Kurtarma kodunu önceden kaydettiysen tekrar girersin.'),
        ('Uygunsuz bir çizim gördüm, ne yapayım?', 'Kuşa dokun ve "Bildir"e bas. Üç bildirim alan kuş (ilk gününde iki) gökyüzünden hemen iniyor ve yöneticiye gidiyor.'),
        ('Verilerimi nasıl silerim?', 'Profil\'deki "Tüm verilerimi sil" düğmesi kuşlarını, oylarını, bildirimlerini, sürülerini ve kuşçu adını kalıcı olarak siliyor.'),
        ('Çizimlerimin hakları kime ait?', 'Sana. DrawBird sadece sitede gösterme ve paylaşım linkinde önizleme izni alıyor. Çizimini satmıyoruz, ürüne basmıyoruz. Ayrıntılar <a href="/kosullar">kullanım koşullarında</a>.'),
        ('Hangi dilleri destekliyor?', 'Oyun 11 dilde: Türkçe, İngilizce, İspanyolca, Portekizce, Fransızca, Almanca, Rusça, Arapça, Çince, Japonca ve Endonezce. Dil tarayıcına göre seçiliyor, menüden değiştirebilirsin.'),
        ('Telefona uygulama gibi ekleyebilir miyim?', 'Evet. Tarayıcının menüsünden "Ana ekrana ekle"yi seç. DrawBird uygulama gibi açılıyor.'),
        ('Kaynak kodu açık mı?', 'Evet. AGPL-3.0 lisansıyla <a href="https://github.com/gunayboss/drawbird">GitHub\'da</a>.'),
    ],
}

ABOUT = {
    'slug': 'hakkinda', 'title': 'DrawBird hakkında',
    'desc': 'DrawBird nedir, neden var? Herkesin çizdiği kuşların aynı gökyüzünde uçtuğu ücretsiz, açık kaynak bir çizim oyunu.',
    'html': '''
<p>DrawBird küçük bir çizim oyunu. Bir kuş çiziyorsun, adını koyuyorsun, "uçur!" diyorsun. Birkaç saniye sonra kuşun dünyanın dört bir yanından gelen kuşlarla aynı gökyüzünde kanat çırpıyor.</p>

<h2>Neden?</h2>
<p>İyi çizmek zorunda olmadığın, kimsenin puan peşinde koşmadığı bir yer istedim. Sadece bir şey yap, paylaş, keyfini çıkar.</p>
<p>Kuş seçmemin sebebi basit. Herkes bir kuş çizebilir, her çocuk bir kuş görmüştür ve kuşlar uçar. Kendi çizdiğin bir şeyin canlanıp gitmesi küçük ama gerçek bir mutluluk.</p>
<p>Oyunun yanında kuşları tanımayı da önemsiyorum. <a href="/kuslar/">Türkiye'nin kuşları</a> sayfalarında balkonundan görebileceğin kuşları anlatıyorum, <a href="/dersler/">çizim derslerinde</a> de onları adım adım nasıl çizeceğini gösteriyorum.</p>

<h2>Kurallarım</h2>
<ul>
  <li><b>Ücretsiz ve üyeliksiz.</b> E-posta, şifre ya da gerçek ad istemiyorum.</li>
  <li><b>Her yaşa güvenli.</b> Yeni kuşçuların ilk kuşları onaydan geçiyor, uygunsuz adlar engelleniyor, her kuş bildirilebiliyor.</li>
  <li><b>Az veri.</b> Sadece oyunun çalışması için gereken veriyi tutuyorum. Çerez ve takip aracı yok.</li>
  <li><b>Açık kaynak.</b> Kodun tamamı <a href="https://github.com/gunayboss/drawbird">GitHub'da</a>, AGPL-3.0 lisansıyla.</li>
</ul>

<h2>İlham</h2>
<p>Fikir Alden Hallak'ın balık çizme oyunu DrawAFish'ten geldi. DrawBird'ün kodu sıfırdan yazıldı. DrawAFish'in kodu, görselleri ya da modeli kullanılmadı.</p>

<h2>Kim yapıyor?</h2>
<p>DrawBird'ü Türkiye'den bağımsız bir geliştirici olarak ben yapıyorum. Öneri, hata ya da iş birliği için <a href="https://github.com/gunayboss/drawbird/issues">GitHub üzerinden</a> yazabilirsin.</p>
''',
}

POSTS = [
    {
        'slug': '2026-11-drawbird-yayinda', 'date': '2026-11-02', 'title': 'DrawBird yayında: ilk ayın notları',
        'desc': 'DrawBird yayına çıktı. Neler yaptık, gökyüzünde neler oluyor, sırada ne var?',
        'html': '''
<p>DrawBird yayında! İlk haftalarda neler yaptığımı, gökyüzünü güvenli tutmak için neye dikkat ettiğimi ve sırada ne olduğunu yazmak istedim.</p>

<h2>Gökyüzündeki ilk kuşlar</h2>
<p>İlk kuşlar daha ilk saatlerde uçmaya başladı. Kırmızı bir kumru, sarı gagalı serçeler, birkaç cesur martı denemesi. En çok hoşuma giden şey kuşların birbirine hiç benzememesi. Kimi gerçekçi, kimi tek çizgiyle çizilmiş bir "V". Ama hepsi aynı hevesle kanat çırpıyor.</p>

<h2>Neler ekledim?</h2>
<ul>
  <li><b>11 dil.</b> Oyunu artık Türkçe, İngilizce, İspanyolca, Portekizce, Fransızca, Almanca, Rusça, Arapça, Çince, Japonca ve Endonezce oynayabiliyorsun.</li>
  <li><b>Sürüler.</b> Sevdiğin kuşları bir sürüde topla, gökyüzünde sadece onları izle, linkini paylaş.</li>
  <li><b>Yem atma.</b> Gökyüzünde bir yere yem bırak, yakındaki kuşlar gelip gagalasın.</li>
  <li><b>Kova aracı.</b> Bir şekil çiz, kovayla içine dokun, tek seferde dolsun.</li>
  <li><b>Çizim dersleri ve kuş sayfaları.</b> <a href="/dersler/">10 çizim dersi</a> ve <a href="/kuslar/">Türkiye'den 20 kuş</a> hazır.</li>
</ul>

<h2>Güvenli bir gökyüzü</h2>
<p>DrawBird'ü çocuklar da kullanıyor. O yüzden yeni kuşçuların ilk iki kuşu bir insan bakana kadar sadece çizene görünüyor. Kuş, kuşçu ve sürü adlarındaki uygunsuz kelimeler otomatik engelleniyor. Her kuş bildirilebiliyor. Bunların işleri biraz yavaşlattığını biliyorum. Ama gökyüzünün herkes için keyifli kalması daha önemli.</p>

<h2>Bu ayın meydan okuması: en komik baykuş</h2>
<p>Bu ay herkesi bir baykuş çizmeye çağırıyorum. <a href="/dersler/baykus">Baykuş dersini</a> izleyebilirsin ya da tamamen kendi tarzında çizebilirsin. Kuşunun adına "baykuş" yaz. Ay sonunda en çok beğeni alan baykuşları <a href="/haftanin-kuslari">Haftanın kuşları</a> sayfasında öne çıkaracağım.</p>

<h2>Sırada ne var?</h2>
<p>Yeni kuş sayfaları, yeni dersler ve derslerin öteki dillere çevrilmesi. Bir önerin varsa <a href="https://github.com/gunayboss/drawbird/issues">GitHub'dan</a> yaz. Hepsini okuyorum.</p>
''',
    },
]
