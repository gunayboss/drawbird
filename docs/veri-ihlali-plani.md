# Veri ihlali müdahale planı

KVKK m.12/5: Veri sorumlusu, ihlali öğrendiği andan itibaren **en geç 72 saat içinde** Kişisel Verileri Koruma Kurulu'na bildirir; etkilenen kişilere de makul en kısa sürede haber verir.

## Ne tutuyoruz (etki değerlendirmesi için)

| Veri | Nerede | Hassasiyet |
| --- | --- | --- |
| Cihaz kodu özeti (SHA-256) | D1 `users.token_hash` | Düşük: geri çevrilemez |
| Kuşçu adı | D1 `users.name` | Düşük: takma ad, gerçek ad istenmiyor |
| Çizimler ve adları | D1 `birds` | Düşük, ama çocuk içeriği olabilir |
| IP özeti (anahtarlı) | D1 `new_ids`, `limits`, `users.ip_hash`, `ip_bans` | Düşük: `ADMIN_KEY` sızmadıkça geri çevrilemez |
| Oylar, bildirimler, sürüler | D1 | Düşük |

E-posta, telefon, şifre, ödeme veya özel nitelikli veri **yok**.

## Erken uyarılar (Telegram)

- 🚨 Yönetici anahtarı bir saatte 20 kez yanlış girildi
- ⚠️ Bir ağdan günlük yeni hesap sınırı aşıldı
- ❗ Sunucu hatası (10 dakikada en fazla bir uyarı)

Ayrıntılı kayıtlar: Cloudflare paneli → Workers & Pages → `drawbird` → Logs.

## Adımlar

**0–1 saat: durdur**
1. Yönetim → **Bakım modu → Aç** (site yalnız okunur olur).
2. Yönetici anahtarını yenile:
   ```bash
   python -c "import secrets;print(secrets.token_hex(32))" > admin-key.txt
   npx wrangler secret put ADMIN_KEY
   ```
3. Telegram bot anahtarını @BotFather'da `/revoke` ile iptal et, yenisini `npx wrangler secret put TELEGRAM_TOKEN` ile koy.
4. Cloudflare ve GitHub şifrelerini değiştir, iki aşamalı doğrulamayı kontrol et; Cloudflare panelinde API token'larını gözden geçir. Gerekirse `npx wrangler logout` sonra `npx wrangler login`.

**1–24 saat: anla**
5. Cloudflare Logs ve D1 üzerinden neyin, ne zaman, kaç kişiyi etkilediğini çıkar:
   ```bash
   npx wrangler d1 execute drawbird --remote --command "SELECT COUNT(*) FROM users"
   ```
6. Gerekirse veritabanını ihlal öncesine döndür (D1 Time Travel, son 7 gün ücretsiz planda):
   ```bash
   npx wrangler d1 time-travel info drawbird
   npx wrangler d1 time-travel restore drawbird --timestamp=<ISO-zaman>
   ```
7. Aşağıdaki kayıt şablonunu doldur.

**24–72 saat: bildir**
8. Kurul'a bildir: kvkk.gov.tr üzerindeki **Veri İhlali Bildirim Formu**. Tüm bilgiler henüz yoksa eldekileri bildir, kalanını sonra tamamla.
9. Etkilenen kullanıcılara haber ver: sitenin üstünde bir duyuru (Bakım modu bandı) ve README.
10. Bakım modunu kapat, kayıt şablonunu sakla.

## Kayıt şablonu

```
Tespit zamanı:
Nasıl fark edildi:
Ne oldu (kısa):
Etkilenen veri türleri:
Etkilenen kişi sayısı (tahmini):
Alınan önlemler ve saatleri:
Kurul bildirimi (tarih, referans no):
Kullanıcı bildirimi (tarih, kanal):
Bir daha olmaması için:
```
