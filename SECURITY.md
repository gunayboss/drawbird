# Güvenlik

## Açık bulursan

Lütfen herkese açık issue açma. Önce özel olarak bildir:

1. Depo sayfasında **Security** sekmesine gir.
2. **Report a vulnerability** düğmesine bas (GitHub özel güvenlik bildirimi).
3. Ne bulduğunu, nasıl tekrar edildiğini ve etkisini yaz.

Bildirimi en kısa sürede okuruz ve düzelene kadar seninle konuşuruz. Düzeltme yayımlanmadan ayrıntıyı herkese açık paylaşma.

## Kapsam

Bakmak istediklerimiz:

- DrawBird kodu (`src/`, `public/`, `migrations/`)
- Yönetim paneli, kimlik ve yetki atlatma
- Başkasının verisine erişme, veri silme ya da değiştirme
- XSS, enjeksiyon, hız sınırı ve engel atlatma
- Gizli anahtarların sızması

Kapsam dışı:

- Cloudflare'in kendi altyapısındaki sorunlar
- Yoğun otomatik tarama, yük testi, hizmeti aksatan denemeler
- Sosyal mühendislik ya da fiziksel saldırılar
- Etkisi olmayan eksik başlık gibi teorik bulgular

Test ederken başka kullanıcıların verisine dokunma. Yerelde kendi kopyanda dene.

## Uygunsuz içerik ve veri talepleri

Bunlar güvenlik açığı değil. Sitedeki iletişim formunu kullan: https://drawbird.the-pit.workers.dev/#iletisim
