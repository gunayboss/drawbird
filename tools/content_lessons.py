"""Drawing lessons (/dersler/<slug>). Canvas is 240x180; the dashed wing line is at y=80.

Shapes: ('e', cx, cy, rx, ry, fill) ellipse · ('c', cx, cy, r, fill) circle · ('p', d, fill) path · ('l', d) outline only.
"""
INK = '#1b2740'

LESSONS = [
    {
        'slug': 'serce', 'title': 'Serçe nasıl çizilir?', 'bird': 'Serçe', 'acc': 'serçeni', 'level': 'Kolay',
        'intro': 'Serçe, DrawBird gökyüzüne ilk kuşunu salmak için en iyi başlangıç: yuvarlak bir gövde, küçük bir baş, kısa bir gaga. Beş adımda, kanat çırpan bir serçe çizeceğiz.',
        'steps': [
            ('Gövde', 'Çizim alanının ortasındaki kesik çizginin hemen altına, yatay bir yumurta çiz. Gövde çizginin altında kalırsa uçarken sabit durur.', [('e', 105, 112, 50, 30, '#b07a4f')]),
            ('Baş', 'Gövdenin sağ üst köşesine, gövdeye biraz giren bir daire ekle. Serçenin boynu yok gibidir; baş doğrudan gövdeye oturur.', [('c', 155, 92, 22, '#b07a4f')]),
            ('Gaga ve göz', 'Başın sağına küçük, kalın bir üçgen gaga koy. Serçenin gagası tohum kırmak için kısa ve kalındır. Gözü gagaya yakın, dolu bir nokta olarak çiz.', [('p', 'M174 88 L194 94 L174 101 Z', '#f2b705'), ('c', 162, 87, 4, INK)]),
            ('Kanat ve kuyruk', 'Kesik çizginin ÜSTÜNE, gövdenin ortasından yukarı doğru bir yaprak gibi kanat çiz. Gökyüzünde bu kısım açılıp kapanır. Gövdenin soluna kısa, kare uçlu bir kuyruk ekle.', [('p', 'M80 100 Q95 40 135 48 Q120 78 118 100 Z', '#8a5a36'), ('p', 'M57 104 L22 92 L28 124 L60 118 Z', '#8a5a36')]),
            ('Renk ve ayrıntı', 'Erkek serçenin gerdanı siyah, yanakları gri olur. Gerdanına küçük siyah bir leke, kanadına iki açık çizgi ekle. Kalın kalemle (6 ve üstü) çizersen gökyüzünde daha net görünür.', [('p', 'M150 106 Q160 114 170 104 Q162 100 150 106 Z', INK), ('l', 'M98 66 L124 60'), ('l', 'M92 80 L122 74')]),
        ],
        'mistakes': ['Kanadı gövdenin içine çizmek: kanat kesik çizginin altında kalırsa çırpmaz.', 'Başı çok büyük çizmek: serçenin başı gövdesinin yarısından küçüktür.', 'İnce kalem kullanmak: gökyüzünde kuşlar küçülür, ince çizgiler kaybolur.'],
        'facts': [
            'Ev serçesi (Passer domesticus) 14–16 cm boyundadır ve insanların yaşadığı hemen her yerde görülür.',
            'Erkeğin tepesi gri, gerdanı siyahtır; dişi ise baştan aşağı kahverengi tonlardadır.',
            'Serçeler toz banyosu yapar: tüylerindeki parazitlerden kurtulmak için kuru toprağa yatıp kanat çırparlar.',
            'Çoğunlukla tohum yerler, ama yavrularını protein açısından zengin böceklerle beslerler.',
        ],
    },
    {
        'slug': 'marti', 'title': 'Martı nasıl çizilir?', 'bird': 'Martı', 'acc': 'martını', 'level': 'Kolay',
        'intro': 'Martının sırrı uzun ve ince kanatlarıdır. DrawBird gökyüzünde martılar, kanatlarını yukarı kaldırınca en güzel görünür. Kıyı şehirlerinin bu tanıdık kuşunu beş adımda çizelim.',
        'steps': [
            ('Gövde', 'Kesik çizginin altına, serçeninkinden daha uzun ve ince bir gövde çiz. Martı gövdesi bir mermi gibi öne doğru incelir.', [('e', 112, 112, 62, 22, '#ffffff')]),
            ('Baş', 'Gövdenin sağ ucuna, yuvarlak ama gövdeye göre küçük bir baş ekle.', [('c', 174, 100, 17, '#ffffff')]),
            ('Gaga', 'Uzun, sarı bir gaga çiz; ucunu hafif aşağı kıvır. Alt gagaya kırmızı bir nokta koy: yavrular bu noktayı gagalayınca anne yiyecek verir.', [('p', 'M189 98 L217 102 L211 108 L189 106 Z', '#f2b705'), ('c', 209, 106, 2.5, '#e03131'), ('c', 179, 95, 3, INK)]),
            ('Kanatlar', 'Asıl iş burada: kesik çizginin ÜSTÜNE, gövdenin ortasından yukarı doğru uzun, ince, açık gri bir kanat çiz. Kanadın ucunu siyaha boya. Kanat ne kadar uzunsa, çırpınca o kadar martıya benzer.', [('p', 'M90 100 L120 30 L150 22 L128 60 L130 100 Z', '#c9d3e0'), ('p', 'M120 30 L150 22 L140 40 Z', INK)]),
            ('Kuyruk ve ayaklar', 'Gövdenin soluna kısa, beyaz bir yelpaze kuyruk ekle. Ayakları istersen sarı çizebilirsin; uçarken genelde gövdenin altına toplanırlar.', [('p', 'M52 108 L24 100 L26 122 L54 118 Z', '#ffffff'), ('l', 'M110 132 L104 146 M120 132 L118 146')]),
        ],
        'mistakes': ['Beyaz kuşu beyaz kalemle çizip kenar çizgisini unutmak: önce koyu bir kenar çiz, sonra içini beyaz bırak.', 'Kanadı kısa çizmek: martının kanadı gövdesinden uzundur.', 'Gagayı serçe gibi küçük çizmek: martı gagası uzun ve kalındır.'],
        'facts': [
            'İstanbul\'da en sık görülen martı, sarı bacaklı martıdır (Larus michahellis). Boyu 52–68 cm, kanat açıklığı 1,2–1,5 metreyi bulur.',
            'Martılar hem tatlı hem tuzlu su içebilir; gözlerinin üstündeki bezler fazla tuzu dışarı atar.',
            'Yavru martılar ilk yıllarında kahverengi beneklidir; yetişkin tüylerine kavuşmaları dört yıl sürebilir.',
            'Gagadaki kırmızı nokta bir "düğme" gibidir: yavru onu gagalayınca ebeveyn yiyeceği geri çıkarır.',
        ],
    },
    {
        'slug': 'baykus', 'title': 'Baykuş nasıl çizilir?', 'bird': 'Baykuş', 'acc': 'baykuşunu', 'level': 'Orta',
        'intro': 'Baykuşlar diğer kuşlardan farklıdır: kocaman başları ve öne bakan iri gözleri vardır. DrawBird\'de sevimli bir kukumav çizmek için yarı yandan bakan, kanatlarını açmış bir baykuş çizeceğiz.',
        'steps': [
            ('Gövde', 'Kesik çizginin altına, tombul ve hafif dik duran bir yumurta çiz. Baykuşun gövdesi serçeninkinden daha yuvarlaktır.', [('e', 110, 120, 44, 32, '#9c7b5b')]),
            ('Baş', 'Gövdenin sağ üstüne büyük bir daire ekle. Baykuşun başı gövdesine göre iridir; bu ona sevimli görüntüsünü verir.', [('c', 148, 94, 28, '#9c7b5b')]),
            ('Gözler ve gaga', 'İki büyük sarı daire içine siyah göz bebekleri çiz. Baykuşun gözleri yüzünün önündedir, bu yüzden ikisi de görünür. Aralarına aşağı bakan küçük bir gaga koy.', [('c', 138, 90, 10, '#f2b705'), ('c', 162, 90, 10, '#f2b705'), ('c', 139, 90, 4, INK), ('c', 163, 90, 4, INK), ('p', 'M148 98 L154 108 L158 98 Z', '#5c4632')]),
            ('Kanat', 'Kesik çizginin ÜSTÜNE, gövdenin solundan yukarı doğru geniş, yuvarlak uçlu bir kanat çiz. Baykuş kanatları geniştir ve uçları yumuşak tüylüdür, bu sayede neredeyse sessiz uçarlar.', [('p', 'M70 106 Q60 46 104 40 Q112 70 104 102 Z', '#7a5c42')]),
            ('Benekler ve pençeler', 'Gövdeye ve başa küçük beyaz benekler serpiştir; kukumavın tüyleri böyle beneklidir. Altına iki küçük pençe ekle.', [('c', 98, 122, 3, '#ffffff'), ('c', 116, 132, 3, '#ffffff'), ('c', 106, 110, 3, '#ffffff'), ('c', 134, 74, 2.5, '#ffffff'), ('l', 'M102 152 L98 162 M118 152 L120 162')]),
        ],
        'mistakes': ['Gözleri küçük çizmek: baykuşun gözleri yüzünün büyük kısmını kaplar.', 'Başı çizginin tamamen üstüne çizmek: başın çoğu çizginin altında olsun, yoksa uçarken baş da sallanır.', 'Gagayı öne uzatmak: baykuş gagası kısa ve aşağı kıvrıktır.'],
        'facts': [
            'Türkiye\'de en sık görülen baykuş kukumavdır (Athene noctua); boyu yalnız 21–23 cm\'dir.',
            'Baykuşlar gözlerini yuvalarında oynatamaz; bunun yerine başlarını yaklaşık 270 derece çevirebilirler.',
            'Kanat tüylerinin tarak gibi kenarları havayı böler, bu yüzden uçarken neredeyse ses çıkarmazlar.',
            'Kukumav, diğer baykuşların aksine gündüz de görülebilir; duvarlarda ve çatılarda tünediğini görebilirsin.',
        ],
    },
    {
        'slug': 'flamingo', 'title': 'Flamingo nasıl çizilir?', 'bird': 'Flamingo', 'acc': 'flamingonu', 'level': 'Orta',
        'intro': 'Flamingo çizmek eğlencelidir çünkü her şeyi uzun: boyun, bacaklar, kanatlar. Uçan bir flamingo boynunu ve bacaklarını dümdüz uzatır; biz de öyle çizeceğiz.',
        'steps': [
            ('Gövde', 'Kesik çizginin altına, ortada küçük ve yatay bir yumurta çiz. Flamingonun gövdesi, boynuna ve bacaklarına göre küçüktür.', [('e', 112, 108, 40, 18, '#ff8fab')]),
            ('Boyun ve baş', 'Gövdenin sağından ileriye doğru uzun, ince bir boyun çiz; ucuna küçük bir baş ekle. Uçan flamingonun boynu S değil düz uzanır.', [('p', 'M148 104 L196 98 L196 106 L148 112 Z', '#ff8fab'), ('c', 200, 101, 8, '#ff8fab')]),
            ('Gaga', 'Başın önüne aşağı doğru kıvrık bir gaga çiz. Gaganın ucunu siyaha boya; flamingonun gagası ortasından kırılmış gibi aşağı bükülür.', [('p', 'M206 98 L222 104 L216 114 L208 106 Z', '#ffe3ea'), ('p', 'M216 108 L222 104 L216 114 Z', INK), ('c', 201, 99, 2, INK)]),
            ('Kanatlar', 'Kesik çizginin ÜSTÜNE geniş, pembe bir kanat çiz ve uç kısmını siyah yap. Flamingoların uçarken görünen siyah kanat uçları en tanıdık işaretleridir.', [('p', 'M92 100 L104 36 L140 30 L128 70 L130 100 Z', '#ff6b8f'), ('p', 'M104 36 L140 30 L134 48 L108 50 Z', INK)]),
            ('Bacaklar', 'Gövdenin arkasından sola doğru iki uzun, ince, pembe bacak uzat. Uçan flamingo bacaklarını kuyruğunun arkasına doğru dümdüz uzatır.', [('l', 'M74 110 L16 118 M74 114 L18 124')]),
        ],
        'mistakes': ['Bacakları aşağı sarkıtmak: uçan flamingo bacaklarını arkaya uzatır.', 'Gagayı düz çizmek: flamingo gagası ortadan aşağı bükülür.', 'Pembeyi tek ton bırakmak: kanatlar gövdeden daha koyu pembe olunca kuş canlanır.'],
        'facts': [
            'Flamingolar gri-beyaz doğar; pembe renk yedikleri karides ve alglerdeki karotenoid boyalarından gelir.',
            'Tuz Gölü, dünyanın en büyük flamingo üreme alanlarından biridir.',
            'Başlarını ters çevirip gagalarıyla suyu süzerek beslenirler.',
            'Büyük flamingonun kanat açıklığı 1,4–1,7 metreyi bulur.',
        ],
    },
    {
        'slug': 'papagan', 'title': 'Papağan nasıl çizilir?', 'bird': 'Papağan', 'acc': 'papağanını', 'level': 'Kolay',
        'intro': 'Papağanlar gökyüzündeki en renkli kuşlar olur. Bu derste kırmızı, sarı ve mavi bir ara papağanı çizeceğiz; renkleri cesurca kullanmaktan çekinme.',
        'steps': [
            ('Gövde', 'Kesik çizginin altına, hafif eğik ve uzun bir yumurta çiz. Papağanın gövdesi kuyruğa doğru incelir.', [('e', 112, 112, 48, 24, '#e03131')]),
            ('Baş', 'Gövdenin sağ ucuna yuvarlak bir baş ekle. Ara papağanlarının yüzünde beyaz, tüysüz bir alan vardır; gözün çevresini beyaz bırak.', [('c', 160, 98, 20, '#e03131'), ('e', 162, 96, 9, 7, '#ffffff'), ('c', 163, 95, 3, INK)]),
            ('Gaga', 'Papağanın en tanıdık parçası: büyük, aşağı kıvrılan, kanca gibi bir gaga. Üst gaga alttakinin üstüne kapanır.', [('p', 'M176 92 Q198 92 194 112 Q186 104 178 108 Z', '#f1f3f5'), ('p', 'M178 108 Q186 104 190 112 Q182 116 178 112 Z', INK)]),
            ('Kanat', 'Kesik çizginin ÜSTÜNE geniş bir kanat çiz. Kanadın omzunu sarı, uç kısmını mavi yap; renk bantları papağanı papağan yapar.', [('p', 'M86 100 Q90 40 132 36 Q126 70 126 100 Z', '#f2b705'), ('p', 'M98 56 Q110 38 132 36 Q128 52 120 60 Z', '#1c7ed6')]),
            ('Uzun kuyruk', 'Gövdenin soluna, gövde kadar uzun, ince ve sivri bir kuyruk çiz. Kuyruğun ucunu maviye boya.', [('p', 'M66 108 L6 124 L10 132 L68 118 Z', '#e03131'), ('p', 'M20 120 L6 124 L10 132 L24 128 Z', '#1c7ed6')]),
        ],
        'mistakes': ['Gagayı küçük ve düz çizmek: papağan gagası büyük ve kanca gibidir.', 'Tek renk kullanmak: kanat bantları papağanı tanınır yapar.', 'Kuyruğu kısa çizmek: ara papağanının kuyruğu gövdesi kadar uzundur.'],
        'facts': [
            'Dünyada yaklaşık 400 papağan türü vardır; çoğu tropik ormanlarda yaşar.',
            'Papağanların ayağında iki parmak öne, iki parmak arkaya bakar; dalları ve yiyecekleri el gibi tutabilirler.',
            'Büyük papağan türleri 50 yıldan uzun yaşayabilir.',
            'Bazı papağanlar yüzlerce kelimeyi ve sesi taklit edebilir.',
        ],
    },
    {
        'slug': 'ordek', 'title': 'Ördek nasıl çizilir?', 'bird': 'Ördek', 'acc': 'ördeğini', 'level': 'Kolay',
        'intro': 'Göllerin tanıdık kuşu yeşilbaş ördeği, yassı gagası ve yeşil başıyla çizmesi en keyifli kuşlardan biridir. Uçan bir ördek boynunu öne uzatır ve hızlı hızlı kanat çırpar.',
        'steps': [
            ('Gövde', 'Kesik çizginin altına tombul, yatay bir gövde çiz. Ördeğin gövdesi ağırdır; serçeninkinden daha dolgun olsun.', [('e', 110, 114, 52, 26, '#adb5bd')]),
            ('Boyun ve baş', 'Gövdenin sağından kısa ve kalın bir boyun, ucuna yuvarlak bir baş ekle. Erkek yeşilbaşın başı parlak yeşildir.', [('p', 'M150 104 L172 98 L172 112 L152 120 Z', '#2f9e44'), ('c', 178, 100, 15, '#2f9e44'), ('c', 182, 96, 2.5, INK)]),
            ('Yassı gaga', 'Başın önüne uzun, yassı ve ucu yuvarlak sarı bir gaga çiz. Ördek gagası sivri değil, kaşık gibidir.', [('p', 'M191 98 L214 102 Q218 108 212 110 L191 106 Z', '#f2b705')]),
            ('Kanat', 'Kesik çizginin ÜSTÜNE geniş bir kanat çiz. Kanadın ortasına, ördeklerin "ayna" denen parlak mavi lekesini ekle.', [('p', 'M86 102 Q88 44 132 40 Q126 74 128 102 Z', '#868e96'), ('p', 'M100 70 L126 64 L124 76 L100 82 Z', '#1c7ed6')]),
            ('Ayrıntılar', 'Boyna ince beyaz bir halka, göğse kahverengi ekle. Kuyruğu kısa ve sivri çiz; erkek yeşilbaşın kuyruğunda yukarı kıvrık küçük siyah tüyler vardır.', [('l', 'M156 112 L168 106'), ('e', 150, 120, 12, 9, '#8d5524'), ('p', 'M60 112 L36 106 L38 120 L60 120 Z', '#f8f9fa')]),
        ],
        'mistakes': ['Gagayı sivri çizmek: ördek gagası yassı ve yuvarlak uçludur.', 'Boynu uzun çizmek: ördeğin boynu kısadır, kuğu gibi değildir.', 'Mavi aynayı unutmak: kanattaki mavi leke ördeği hemen tanıtır.'],
        'facts': [
            'Evcil ördeklerin neredeyse hepsinin atası yeşilbaştır (Anas platyrhynchos).',
            'Erkeğin başı yeşil, dişinin tüyleri ise benekli kahverengidir.',
            'Yeşilbaşlar kuyruklarını havaya dikip başlarını suya daldırarak beslenir.',
            'Ekmek ördekler için iyi değildir; mısır, bezelye ya da ördek yemi daha sağlıklıdır.',
        ],
    },
    {
        'slug': 'penguen', 'title': 'Penguen nasıl çizilir?', 'bird': 'Penguen', 'acc': 'pengueni', 'level': 'Kolay',
        'intro': 'Penguenler uçamaz ama DrawBird gökyüzünde her kuş uçar! Bu derste kanatlarını çırparak uçmaya çalışan komik bir penguen çizeceğiz.',
        'steps': [
            ('Gövde', 'Kesik çizginin altına yatay, damla biçimli büyük bir gövde çiz. Gövdenin üstünü siyah, karnını beyaz boyayacağız.', [('e', 112, 116, 54, 28, INK)]),
            ('Beyaz karın', 'Gövdenin alt yarısına beyaz, yumurta biçimli bir karın ekle. Penguenin smokinli görünüşü bu beyaz karından gelir.', [('e', 118, 124, 42, 16, '#ffffff')]),
            ('Baş ve gaga', 'Gövdenin sağına yuvarlak siyah bir baş, önüne kısa turuncu bir gaga ekle. Gözün çevresine küçük beyaz bir leke koy.', [('c', 166, 104, 18, INK), ('p', 'M182 102 L198 106 L182 112 Z', '#f08c00'), ('c', 172, 99, 4, '#ffffff'), ('c', 173, 99, 2, INK)]),
            ('Kısa kanatlar', 'Kesik çizginin ÜSTÜNE kısa, kürek gibi bir kanat çiz. Penguen kanatları suda yüzmek için kısa ve serttir; gökyüzünde çırpınca çok komik görünür.', [('p', 'M98 102 Q96 58 126 54 Q124 80 124 102 Z', INK)]),
            ('Ayaklar', 'Gövdenin arkasına iki turuncu, perdeli ayak ekle. Uçmaya çalışan bir penguen ayaklarını arkaya uzatır.', [('p', 'M60 120 L40 114 L42 126 Z', '#f08c00'), ('p', 'M62 128 L42 126 L46 136 Z', '#f08c00')]),
        ],
        'mistakes': ['Kanadı uzun çizmek: penguen kanatları kısadır, bu yüzden komik görünür.', 'Karnı siyah bırakmak: beyaz karın penguenin en tanıdık parçasıdır.', 'Gagayı unutmak: küçük turuncu gaga yüze hayat verir.'],
        'facts': [
            'Yaklaşık 18 penguen türü vardır ve neredeyse hepsi Güney Yarımküre\'de yaşar.',
            'İmparator penguen 1,1–1,3 metre boyuyla en büyük penguendir ve 500 metreden derine dalabilir.',
            'Penguenlerin kanatları suda uçarcasına yüzmek için kürek gibi sertleşmiştir.',
            'Siyah sırt ve beyaz karın, denizde yukarıdan ve aşağıdan bakan avcılardan gizlenmelerini sağlar.',
        ],
    },
    {
        'slug': 'kartal', 'title': 'Kartal nasıl çizilir?', 'bird': 'Kartal', 'acc': 'kartalını', 'level': 'Zor',
        'intro': 'Kartal geniş kanatları ve kanca gagasıyla gökyüzünün kralıdır. Bu derste kanatlarını açmış bir kaya kartalı çizeceğiz; kanat uçlarındaki parmak gibi tüyler en önemli ayrıntı.',
        'steps': [
            ('Gövde', 'Kesik çizginin altına güçlü, uzun bir gövde çiz. Kartalın gövdesi kalın ve kaslıdır.', [('e', 108, 114, 54, 22, '#6b4423')]),
            ('Baş', 'Gövdenin sağına gövdeye göre küçük bir baş ekle. Kaya kartalının ensesi altın sarısıdır; başın üst kısmını açık kahve yap.', [('c', 164, 104, 15, '#b08850'), ('c', 168, 100, 2.5, INK)]),
            ('Kanca gaga', 'Başın önüne kısa ama güçlü, ucu aşağı kıvrık bir kanca gaga çiz. Gaganın dibi sarı, ucu koyudur.', [('p', 'M176 100 Q190 98 188 112 Q184 106 176 108 Z', '#495057'), ('p', 'M176 100 L180 100 L180 107 L176 108 Z', '#f2b705')]),
            ('Geniş kanatlar', 'Kesik çizginin ÜSTÜNE geniş ve uzun bir kanat çiz. Kanadın ucunu düz bitirme; parmak gibi ayrılmış 4–5 tüyle bitir. Kartalı uzaktan tanıtan şey budur.', [('p', 'M78 100 L86 40 L104 28 L112 34 L120 24 L128 32 L136 26 L140 40 L132 100 Z', '#5c3a1e')]),
            ('Kuyruk ve pençeler', 'Gövdenin soluna yelpaze gibi geniş bir kuyruk, altına sarı, kıvrık tırnaklı pençeler ekle.', [('p', 'M56 108 L22 98 L20 128 L56 122 Z', '#6b4423'), ('l', 'M112 136 L106 148 M122 136 L120 148')]),
        ],
        'mistakes': ['Kanat ucunu sivri bitirmek: kartal kanadı parmak gibi ayrılmış tüylerle biter.', 'Gagayı uzun çizmek: kartal gagası kısa ama çok kıvrık ve güçlüdür.', 'Başı büyük çizmek: kartalın başı gövdesine göre küçüktür.'],
        'facts': [
            'Kaya kartalının (Aquila chrysaetos) kanat açıklığı 1,8–2,3 metreyi bulur ve Türkiye dağlarında yaşar.',
            'Kartalların görme keskinliği insanınkinin birkaç katıdır; çok yüksekten tavşan gibi avları seçebilirler.',
            'Sıcak hava akımlarında kanat çırpmadan saatlerce süzülebilirler.',
            'Kartal çiftleri ömür boyu birlikte kalır ve aynı yuvayı yıllarca büyüterek kullanır.',
        ],
    },
    {
        'slug': 'tavuskusu', 'title': 'Tavus kuşu nasıl çizilir?', 'bird': 'Tavus kuşu', 'acc': 'tavus kuşunu', 'level': 'Zor',
        'intro': 'Tavus kuşunun uzun kuyruğu gökyüzünde muhteşem görünür. Bu derste uçan bir tavus kuşu çizeceğiz; kuyruktaki "gözler" en eğlenceli kısım.',
        'steps': [
            ('Gövde', 'Kesik çizginin altına, ortadan biraz sağa, orta boy bir gövde çiz ve parlak mavi boya.', [('e', 136, 112, 38, 20, '#1864ab')]),
            ('Boyun ve baş', 'Gövdenin sağından ince bir boyun ve küçük bir baş çiz. Başın üstüne, ucu top gibi olan üç ince tüyden bir taç ekle.', [('p', 'M166 106 L184 96 L186 106 L170 116 Z', '#1864ab'), ('c', 190, 96, 9, '#1864ab'), ('l', 'M188 88 L184 76 M191 87 L192 75 M194 88 L200 77'), ('c', 184, 76, 2, '#1864ab'), ('c', 192, 75, 2, '#1864ab'), ('c', 200, 77, 2, '#1864ab'), ('c', 193, 94, 2, INK)]),
            ('Gaga', 'Başın önüne küçük, sivri, açık renkli bir gaga ekle.', [('p', 'M198 94 L210 98 L198 101 Z', '#e9ecef')]),
            ('Kanat', 'Kesik çizginin ÜSTÜNE kahverengi, geniş bir kanat çiz. Tavus kuşunun kanatları kuyruğuna göre sadedir.', [('p', 'M118 102 Q118 52 152 46 Q148 78 150 102 Z', '#a0522d')]),
            ('Gözlü kuyruk', 'Gövdenin soluna, gövdeden çok daha uzun, geniş yeşil bir kuyruk çiz. İçine mavi ortalı, yeşil kenarlı "göz" desenleri koy. Bu desenler aslında kuyruk değil, kuyruğun üstündeki uzun örtü tüyleridir.', [('p', 'M100 106 L8 92 L8 136 L100 122 Z', '#2f9e44'), ('e', 30, 106, 6, 5, '#f2b705'), ('c', 30, 106, 3, '#1864ab'), ('e', 58, 116, 6, 5, '#f2b705'), ('c', 58, 116, 3, '#1864ab'), ('e', 30, 124, 6, 5, '#f2b705'), ('c', 30, 124, 3, '#1864ab')]),
        ],
        'mistakes': ['Kuyruğu kesik çizginin üstüne taşırmak: kuyruk üstte kalırsa kanatla birlikte sallanır.', 'Gözleri tek renk yapmak: mavi orta ve sarı-yeşil halka desenin canını verir.', 'Tacı unutmak: baştaki üç tüy tavus kuşunu hemen tanıtır.'],
        'facts': [
            'Göz desenli uzun tüyler kuyruk değil, kuyruğun üstündeki örtü tüyleridir ve 1,5 metreyi geçebilir.',
            'Yalnız erkek tavus kuşlarında bu gösterişli tüyler bulunur; dişiler sade kahverengidir.',
            'Mavi tavus kuşu Hindistan\'ın ulusal kuşudur.',
            'Tavus kuşları ağır görünse de uçabilir; geceyi güvenli olsun diye ağaçların yüksek dallarında geçirirler.',
        ],
    },
    {
        'slug': 'kolibri', 'title': 'Kolibri nasıl çizilir?', 'bird': 'Kolibri', 'acc': 'kolibrini', 'level': 'Orta',
        'intro': 'Kolibri (sinekkuşu) dünyanın en hızlı kanat çırpan kuşudur. DrawBird gökyüzünde de minicik gövdesi ve hızla çırpan kanatlarıyla çok sevimli görünür.',
        'steps': [
            ('Küçük gövde', 'Kesik çizginin altına küçük, ince ve parlak yeşil bir gövde çiz. Kolibri kuşların en küçüklerindendir.', [('e', 116, 112, 34, 15, '#2b8a3e')]),
            ('Baş', 'Gövdenin sağına küçük yuvarlak bir baş ekle. Boğazına parlak kırmızı bir leke koy; erkek kolibrilerin boğazı ışıkta parlar.', [('c', 152, 104, 12, '#2b8a3e'), ('p', 'M146 112 Q154 120 162 110 Q154 108 146 112 Z', '#e03131'), ('c', 156, 100, 2, INK)]),
            ('Uzun ince gaga', 'Başın önüne çok uzun ve ince, iğne gibi bir gaga çiz. Kolibri bu gagayla çiçeklerin içindeki nektara ulaşır.', [('p', 'M163 101 L212 100 L212 103 L163 105 Z', INK)]),
            ('Hızlı kanatlar', 'Kesik çizginin ÜSTÜNE ince ve sivri bir kanat çiz. Gökyüzünde çırparken çok hızlı görünsün diye kanadı ince tut.', [('p', 'M110 100 L104 34 L128 46 L124 100 Z', '#a5d8ff')]),
            ('Kuyruk', 'Gövdenin soluna kısa, yelpaze gibi açılan bir kuyruk ekle. İstersen yanına küçük bir çiçek çizebilirsin, ama çiçek kuşla birlikte uçar!', [('p', 'M84 110 L62 100 L64 124 L84 118 Z', '#2b8a3e')]),
        ],
        'mistakes': ['Gagayı kısa çizmek: kolibrinin gagası neredeyse gövdesi kadar uzundur.', 'Kuşu büyük çizmek: kolibri minik bir kuştur; küçük çizdiğinde daha sevimli olur.', 'Kanadı kalın çizmek: ince kanat hızlı çırpıyormuş hissi verir.'],
        'facts': [
            'Kolibriler saniyede 50–80 kez kanat çırpabilir ve havada asılı kalabilir.',
            'Geri geri uçabilen tek kuş grubu kolibrilerdir.',
            'En küçük kuş Küba\'daki arı sinekkuşudur; boyu yalnız 5–6 cm\'dir.',
            'Kolibriler yalnız Amerika kıtasında yaşar; Türkiye\'de bulunmazlar.',
        ],
    },
]
