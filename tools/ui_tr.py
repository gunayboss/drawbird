"""Turkish template strings for the generated pages and the Worker's week pages.

{placeholders} must stay as they are in every translation.
"""
UI = {
    # navigation and footer
    'nav_draw': 'Çiz', 'nav_lessons': 'Dersler', 'nav_birds': 'Kuşlar', 'nav_week': 'Haftanın kuşları', 'nav_blog': 'Blog', 'nav_faq': 'SSS',
    'foot_about': 'Hakkında', 'foot_teachers': 'Öğretmenler', 'foot_howto': 'Nasıl oynanır', 'foot_terms': 'Koşullar',
    'foot_privacy': 'Gizlilik', 'foot_kvkk': 'KVKK', 'foot_source': 'Kaynak kod', 'foot_contact': 'Bize yaz', 'language': 'Dil',
    # lessons
    'wing_note': 'Kesik çizgi, DrawBird çizim alanındaki kanat hattı: üstündekiler çırpıyor, altındakiler gövde olarak kalıyor.',
    'step_by_step': 'Adım adım', 'step_n': 'Adım {n}', 'finished_label': 'Bitmiş hâli', 'done': 'Bitti!',
    'done_text': '{bird} hazır. Şimdi DrawBird’de çiz, adını koy ve gökyüzüne sal.',
    'mistakes': 'Sık yapılan hatalar', 'about_bird': '{bird} hakkında bilmen gerekenler', 'related_birds': 'Bu dersle çizebileceğin kuşlar',
    'level_easy': 'Kolay', 'level_medium': 'Orta', 'level_hard': 'Zor',
    'lessons_title': 'Kuş çizim dersleri',
    'lessons_desc': '{n} adım adım kuş çizim dersi: serçe, martı, baykuş, flamingo, papağan ve daha fazlası. DrawBird gökyüzünde kanat çırpan kuşlar çiz.',
    'lessons_intro': '{n} ders, her biri beş adım. Hepsi DrawBird\'ün kanat hattına göre hazırlandı, yani çizdiğin kuş gökyüzünde gerçekten kanat çırpıyor. Kolaydan zora sıralı. İlk kez çiziyorsan serçeyle başla.',
    'start_drawing': 'Çizmeye başla',
    # birds
    'tbl': ['Boy', 'Kanat açıklığı', 'Ağırlık', 'Beslenme', 'Yumurta', 'Görüldüğü yer'],
    'bird_title': '{name}: tanı ve çiz', 'my_note': 'Benim notum', 'draw_it': 'DrawBird\'de çizmek için',
    'lesson_link': 'Çizim dersi: {title} →', 'other_birds': 'Diğer kuşlar',
    'birds_title': 'Türkiye\'nin kuşları',
    'birds_desc': 'Türkiye\'de görebileceğin {n} kuşu tanı, sonra DrawBird\'de çiz: kumru, leylek, flamingo, kelaynak ve daha fazlası.',
    'birds_intro': 'Balkonundan, parktan, kıyıdan ve göllerden tanıyabileceğin {n} kuş. Her sayfada kuşun boyu, ne yediği, nerede yaşadığı ve onu DrawBird\'de nasıl çizeceğin var.',
    # pages
    'open_drawbird': 'DrawBird\'ü aç',
    'faq_more': 'Cevabını bulamadın mı? <a href="https://github.com/gunayboss/drawbird/issues">GitHub üzerinden</a> sor.',
    'blog_title': 'DrawBird blog', 'blog_heading': 'Blog',
    'blog_desc': 'DrawBird\'den haberler, yeni özellikler, topluluğun öne çıkan kuşları ve aylık çizim meydan okumaları.',
    'blog_intro': 'Yeni özellikler, topluluğun öne çıkan kuşları ve her ay bir çizim meydan okuması.',
    'all_posts': '← Tüm yazılar',
    'months': ['Ocak', 'Şubat', 'Mart', 'Nisan', 'Mayıs', 'Haziran', 'Temmuz', 'Ağustos', 'Eylül', 'Ekim', 'Kasım', 'Aralık'],
    'date_format': '{d} {month} {y}',
    # Worker week pages
    'week_title': 'Haftanın kuşları', 'week_desc': 'DrawBird\'de son yedi günde en çok beğenilen kuş çizimleri.',
    'week_alltime': 'Bu hafta henüz yeterince kuş uçmadı. Şimdilik tüm zamanların en sevilen kuşları burada.',
    'week_intro': '{from} ile bugün arasında gökyüzüne {birds} kuş katıldı, {artists} kuşçu çizdi. İşte en çok beğenilenler.',
    'week_tap': 'Bir kuşa dokunursan gökyüzünde onu bulur, oy verebilirsin.',
    'week_empty': 'Gökyüzü henüz boş. İlk kuşu sen çiz!',
    'week_cta': 'Sen de bir kuş çiz',
    'week_note': 'Liste beş dakikada bir yenileniyor. Sıralama kuşların aldığı ▲ ve ▼ oyların farkına göre. Geçmiş haftalar için <a href="{archive}">hafta arşivine</a> bak.',
    'card_line': '#{rank} · {author} · {up} beğeni', 'an_artist': 'Bir kuşçu',
    'archive_title': 'Hafta arşivi', 'archive_desc': 'DrawBird\'ün geçmiş haftaları: her hafta gökyüzüne katılan kuşlar ve en çok beğenilenler.',
    'archive_intro': 'Her hafta gökyüzüne katılan kuşlar burada saklanıyor. Bir haftaya girince o hafta en çok beğenilen kuşları görürsün.',
    'archive_empty': 'Arşivde henüz hafta yok.', 'archive_row': '{y}, {w}. hafta', 'archive_count': '{n} kuş',
    'weekpage_title': '{y}, {w}. haftanın kuşları', 'weekpage_desc': 'DrawBird {y} yılı {w}. hafta: {birds} kuş, {artists} kuşçu.',
    'weekpage_summary': '{from} – {to} arasında gökyüzüne {birds} kuş katıldı ve {artists} kuşçu çizdi.',
    'weekpage_best': 'Haftanın en sevilen kuşu “{name}” oldu (çizen: {author}). {up} beğeni aldı.',
    'weekpage_none': '{from} – {to} arasında gökyüzüne kuş katılmadı.',
    'prev_week': '← Önceki hafta', 'next_week': 'Sonraki hafta →', 'archive_link': 'Arşiv', 'week_not_found': 'Bu hafta bulunamadı',
    # share preview (/k/<bird>)
    'share_desc': '{author} bu kuşu çizdi. Sen de bir kuş çiz, ortak gökyüzünde uçsun.',
}
