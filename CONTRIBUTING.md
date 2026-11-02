# Katkı rehberi

DrawBird'e katkı vermek istediğin için sağ ol! Hata düzeltmesi, çeviri, yeni fikir, hepsi güzel.
Başlamadan [Davranış Kuralları](CODE_OF_CONDUCT.md) dosyasına göz at.

## Yerelde çalıştırma

```sh
npm install
npx wrangler d1 migrations apply drawbird --local
```

Proje kökünde `.dev.vars` adlı bir dosya aç ve içine yönetim anahtarı yaz:

```
ADMIN_KEY=istedigin-bir-test-degeri
```

Sonra başlat:

```sh
npx wrangler dev
```

**`.dev.vars` ve `admin-key.txt` dosyalarını asla commit'leme.** İçlerinde sır var. Gerçek anahtarlarını kimseyle paylaşma.

## İçerik ve çeviriler nasıl işliyor?

Türkçe metin kaynağı `tools/content_*.py` dosyalarında. Akış şöyle:

1. `tools/content_*.py` dosyasını düzenle.
2. `python tools/export_tr.py` çalıştır. Türkçe kaynak `tools/i18n_content/tr.py` olarak çıkar.
3. Çevirileri `tools/i18n_content/<dil>.py` dosyalarında güncelle. Kurallar: `tools/i18n_content/CEVIRI.md`.
4. `python tools/check_i18n.py` ile biçimi doğrula.
5. `python tools/build_pages.py` ile 11 dildeki HTML sayfalarını üret.

Oyun içi kısa metinler `tools/i18n_table.py` içinde.

## Yazım tarzı

Sitedeki bütün yazılar arkadaşça, kısa cümlelerle, günlük dille yazılır. Ayrıntılar `tools/YAZIM_TARZI.md` dosyasında. Yeni bir şey eklerken ona bak.

## Test

```sh
node tests/smoke.mjs
```

Bu test yalnız **yerel** geliştirme sunucusuna karşı çalıştırılır (`npx wrangler dev`). Canlı siteye karşı çalıştırma.

## Pull request

- Küçük ve tek konuya odaklı olsun.
- Ne değiştiğini ve nasıl denediğini yaz (şablon seni yönlendirir).
- Büyük bir değişiklik düşünüyorsan önce bir issue aç, birlikte bakalım.

## Lisans

Katkı vererek çalışmanın [AGPL-3.0](LICENSE) lisansıyla yayımlanmasını kabul etmiş olursun.
