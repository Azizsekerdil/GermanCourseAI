# German Course AI - Kullanım Kılavuzu

## İçindekiler

- [1. Bu kılavuz hakkında](#1-bu-kılavuz-hakkında)
- [2. Kurulum](#2-kurulum)
- [3. Programın ilk açılışı](#3-programın-ilk-açılışı)
- [4. Ekranlar](#4-ekranlar)
- [5. Sözlük (ayrıntılı)](#5-sözlük-ayrıntılı)
- [6. Yapay zeka](#6-yapay-zeka)
- [7. Veri yönetimi](#7-veri-yönetimi)
- [8. Kısayollar ve ipuçları](#8-kısayollar-ve-ipuçları)
- [9. Sorun giderme](#9-sorun-giderme)
- [10. Sürüm notları özeti](#10-sürüm-notları-özeti)
- [11. Sık sorulan sorular](#11-sık-sorulan-sorular)
- [12. Lisans](#12-lisans)

---

## 1. Bu kılavuz hakkında

Bu belge **German Course AI** sürüm **1.3.0** için yazılmıştır. Uygulama, Almanca öğrenmek için tasarlanmış bağımsız bir masaüstü programıdır: Windows ve macOS üzerinde çalışır, verilerinizi kendi bilgisayarınızda tutar ve yapay zeka dışındaki her özelliği internet olmadan yerine getirir.

Kılavuzu baştan sona okumanız gerekmez: ilk kurulum için [2](#2-kurulum) ve [3](#3-programın-ilk-açılışı), bir ekranın ne yaptığı için [4](#4-ekranlar), sözlüğün ayrıntıları için [5](#5-sözlük-ayrıntılı) bölümüne bakın.

Bütün düğme ve alan adları, arayüz dili **Türkçe** seçiliyken göründüğü gibi yazılmıştır; İngilizce karşılıkları gerektiğinde parantez içinde verilmiştir. Arayüz dili olarak **Türkçe**, **English** ve **Deutsch** seçilebilir.

---

## 2. Kurulum

### Windows (zip arşivi)

1. `GermanCourseAI-Windows.zip` dosyasını indirin.
2. Arşivi sağ tıklayıp **Tümünü ayıkla** ile bir klasöre açın.
3. Klasördeki **`GermanCourseAI.exe`** dosyasına çift tıklayın.

Kurulum sihirbazı yoktur, yönetici hakkı gerekmez, kayıt defterine bir şey yazılmaz. Kaldırmak için klasörü silin; verileriniz ayrı klasörde durduğu için silinmez.

Arşivde çalıştırılabilir dosyanın yanında `LICENSE` (MIT) ve `THIRD_PARTY_NOTICES.md` (üçüncü taraf bileşen bildirimleri) dosyaları da bulunur.

### macOS (zip arşivi)

macOS paketi Apple Silicon Mac'ler için `GermanCourseAI-macOS.zip` olarak dağıtılır.

1. Arşivi açın; `GermanCourseAI.app` çıkar. Uygulamayı **Uygulamalar** klasörüne taşıyın.
2. Uygulama Apple tarafından **notarize edilmemiştir**. İlk açılışta çift tıklamak yerine simgeye **sağ tıklayın → Aç** deyin ve uyarıda yine **Aç**'a basın. Bu onay yalnızca bir kez gerekir.

### Kaynaktan çalıştırma

Python 3.11 veya üzeri gerekir. Tek çalışma zamanı bağımlılığı, PDF metni okuyan `pypdf` paketidir.

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python .\German_Course_AI.pyw
```

Kendi çalıştırılabilir dosyanızı üretmek için `python -m pip install -r requirements-dev.txt` ardından `.\build.bat` çalıştırın; çıktı `dist\GermanCourseAI.exe` olur. macOS paketi bir Mac üzerinde `./build_macos.sh` ile üretilir ve `dist/GermanCourseAI.app` ile `dist/GermanCourseAI-macOS.zip` dosyalarını oluşturur.

### Veriler nerede tutulur

Öğrenci verisi program klasöründe değil, ayrı bir kullanıcı klasöründe saklanır.

| Sistem | Varsayılan veri klasörü |
| --- | --- |
| Windows | `%APPDATA%\GermanCourseAI` |
| macOS | `~/Library/Application Support/GermanCourseAI` |
| Linux | `~/.germancourseai` |

Altında `data\` (SQLite veritabanı `GermanCourseAI.db`), `settings\`, `exports\` ve `downloads\` klasörleri bulunur. Taşınabilir kullanım için **`GCA_HOME`** ortam değişkenini tanımlayın; program bütün verisini o klasöre yazar:

```powershell
$env:GCA_HOME = "E:\GermanCourseAI-Veri"
.\GermanCourseAI.exe
```

---

## 3. Programın ilk açılışı

Pencere 1360 × 860 boyutunda açılır (en küçük 1080 × 700): solda gruplanmış gezinme çubuğu, üstte araç şeridi, altta durum satırı.

İlk çalıştırmada veri klasörü ile SQLite veritabanı oluşturulur, **Alex** adlı varsayılan profil açılır, gömülü **161 A1 kelimesi** kelime bankasına yazılır ve gömülü **1267 maddelik Almanca-İngilizce-Türkçe sözlük** yüklenir; sözlük programın içinde gelir, indirme gerektirmez.

Ardından şunları ayarlamanız önerilir:

- **Arayüz dili:** Üst şeritteki 🌐 simgesinin yanındaki listeden **Türkçe**, **English** veya **Deutsch** seçin. Değişiklik anında uygulanır ve kaydedilir.
- **Profil:** Dil listesinin sağındaki liste etkin öğrenciyi gösterir; aradaki **+** düğmesi yeni profil açar. Her profilin ilerlemesi, sınavları ve PDF notları ayrıdır; kelime bankası ile sözlük ortaktır.
- **Tema:** **Ayarlar → Tema** listesinden `dark` (varsayılan) ya da `light` seçip **Kaydet** deyin.
- **Günlük hedef:** **Ayarlar → Günlük hedef** varsayılan olarak 20'dir; 5-200 arası bir değer seçebilirsiniz.

Üst şeridin sağındaki **AI:** etiketi yerel yapay zeka sunucusunun durumunu (**Kullanılabilir** / **Kullanılamıyor**) gösterir. Bu bir hata değildir; yapay zeka olmadan da programın tamamı çalışır.

---

## 4. Ekranlar

Sol gezinme çubuğu 18 sayfayı beş gruba ayırır.

| Grup | Simge | Sayfa | Kısaca |
| --- | --- | --- | --- |
| ÖĞREN | ↻ | Aralıklı Tekrar | SM-2 / Leitner kart çalışması |
| ÖĞREN | Aa | Kelime Bankası | Kelime listesi ve CSV |
| ÖĞREN | 📖 | Sözlük DE-EN-TR | Üç dilli sözlük, AI araması |
| ÖĞREN | ✓ | Sınav | Puanlanan çoktan seçmeli sınav |
| LABORATUVARLAR | Äß | Yazım ve Ses | Alfabe, umlaut, ß, dikte |
| LABORATUVARLAR | ◖ | Telaffuz | Seslendirme ve ses kuralları |
| LABORATUVARLAR | § | Dilbilgisi | 24 konu ve alıştırma |
| OKU & KEŞFET | ◇ | Kaynak Merkezi | Açık lisanslı dış kaynaklar |
| OKU & KEŞFET | ▤ | PDF Okuyucu | PDF metni ve sayfa notları |
| OKU & KEŞFET | ▣ | Ders Kitaplığı | Kendi ders dosyalarınız |
| PRATİK | ✦ | AI Öğretmen | Açıkla, çevir, düzelt, OCR |
| PRATİK | ◌ | Konuşma | Senaryo tabanlı diyalog |
| PRATİK | ✎ | Yazma & El Yazısı | Yazma, AI düzeltmesi, çizim |
| İLERLEME & SİSTEM | ↗ | İlerleme | Hedef, seri, haftalık grafik |
| İLERLEME & SİSTEM | ⬡ | Paketler | `.gcapack` aktarımı |
| İLERLEME & SİSTEM | # | Token Defteri | AI kullanım özeti |
| İLERLEME & SİSTEM | ? | Çevrimdışı Kılavuz | Program içi kılavuz |
| İLERLEME & SİSTEM | ⚙ | Ayarlar | Tema, hedef, ses, AI |

**ÖĞREN grubu**

### Aralıklı Tekrar (Spaced Review)

**Ne işe yarar.** SM-2 algoritması ve Leitner kutularıyla hangi kelimeyi ne zaman tekrar edeceğinizi hesaplar. Üstteki dört kutu **Bugün**, **Yeni**, **Yanlışlar** ve **Favoriler** sayılarını gösterir.

**Nasıl kullanılır.** Kuyruğu (`new`, `due`, `wrong`, `favorites`) ve modu (**Kart**, **Çoktan seçmeli**, **Yazma**, **Dinleme**, **Eşleştirme**) seçin, kart sayısını belirleyin (5-50, varsayılan 10) ve **Başlat**'a basın. **Cevabı göster** düğmesi Türkçe ile İngilizce karşılığı ve örnek cümleyi açar; sonra kendinizi **Tekrar**, **Zor**, **İyi** veya **Kolay** ile değerlendirin. Sonraki tarih buna göre hesaplanır; oturum bitince **Oturum tamamlandı** yazar.

**İpucu.** Bu sürümde beş modun tamamı aynı kart akışını kullanır; yalnız **Dinleme** modunda kart açılırken kelime ayrıca sesli okunur.

### Kelime Bankası (Word Bank)

**Ne işe yarar.** Almanca-Türkçe-İngilizce kelime listenizi artikel ve çoğul bilgisiyle tutar; Aralıklı Tekrar ve Sınav kartlarını buradan alır.

**Nasıl kullanılır.** Arama kutusuna yazıp **Ara** düğmesine (ya da `Enter`) basın; arama üç dilde birden çalışır. Sütunlar **Almanca**, **Türkçe**, **İngilizce**, **Artikel**, **Çoğul**, **Deste**'dir; satır seçince altta örnek cümleler görünür. **★ Favori** favori durumunu değiştirir; **↑ Dışa aktar** ve **↓ İçe aktar** UTF-8 CSV ile çalışır.

**İpucu.** Destesi belirtilmemiş içe aktarılan kelimeler `İçe Aktarılan` destesine düşer; bu ad sabittir, arayüz diline göre değişmez.

### Sözlük DE-EN-TR (Dictionary DE-EN-TR)

**Ne işe yarar.** Gömülü 1267 madde, kendi maddeleriniz ve yapay zekanın önbelleğe aldığı maddelerden oluşan üç dilli sözlük. Ayrıntı için [5. Sözlük](#5-sözlük-ayrıntılı) bölümüne bakın.

**Nasıl kullanılır.** Kelimeyi yazın; iki harften sonra liste kendiliğinden süzülür, `Enter` ya da **Ara** tam aramayı çalıştırır. Sağdaki panel madde başını, türü, artikel/çoğulu, İngilizce ve Türkçe karşılığı, örnek cümleyi ve notu gösterir.

**İpucu.** **🎲 Rastgele kelime** gömülü sözlükten rastgele bir madde açar; günlük ısınma için idealdir.

### Sınav (Exam)

**Ne işe yarar.** Kelime bankasından çoktan seçmeli sorular üretir, cevapları kaydeder ve yüzde olarak puanlar.

**Nasıl kullanılır.** **Soru sayısı** ile 5-50 arası bir değer seçip **Başlat**'a basın. Her soruda Almanca kelime gösterilir; dört şıktan doğru Türkçe karşılığı seçip **Kontrol et** deyin. Sonunda **Sınav bitti** ekranı ve **Puan** yüzdesi gelir; sonuç haftalık rapora katılır.

**İpucu.** Her sınav kaydı ayarlardaki CEFR düzeyiyle (varsayılan `A1`) saklanır.

**LABORATUVARLAR grubu**

### Yazım ve Ses (Spelling & Sound)

**Ne işe yarar.** Alman alfabesi, `Ä/Ö/Ü`, `ß` ve isimlerin büyük yazımı gibi 15 yazım kuralını örnekleriyle listeler; kısa bir dikte alıştırması içerir.

**Nasıl kullanılır.** Soldaki tablodan bir sembol seçin; sağda kuralın açıklaması görünür. **Dikte alıştırması** bölümünde **▶ Seslendir**'e basıp duyduğunuz kelimeyi yazın ve **Kontrol et** deyin; doğruysa `✓`, yanlışsa doğru yazım gösterilir.

**İpucu.** Karşılaştırma büyük/küçük harfe ve umlautlara duyarlıdır: `Strasse` yazarsanız `Straße` düzeltmesi gelir.

### Telaffuz (Pronunciation)

**Ne işe yarar.** Almancaya özgü dokuz ses kuralını (`ch` iki kez - `i/e` sonrası ve `a/o/u` sonrası - ayrıca `r`, `z`, `sch`, `sp/st`, `ei/ie`, `eu/äu`, `w/j`) IPA gösterimi ve örneklerle verir.

**Nasıl kullanılır.** Üstteki kutuya kelimeyi yazın ve **▶ Seslendir** düğmesine basın. **◉ Mikrofonla karşılaştır** düğmesi bu sürümde etkin değildir; **Kullanılamıyor** yanıtı verir.

**İpucu.** Sayfa açıldığında kutuda `Mädchen` yazar; umlaut ve `ch` sesini duymak için iyi bir örnektir.

### Dilbilgisi (Grammar)

**Ne işe yarar.** Nominativ'den bileşik kelimelere 24 Almanca konuyu kural, örnek ve alıştırma biçiminde sunar.

**Nasıl kullanılır.** Soldaki listeden konuyu seçin; sağda başlık, kural ve örnek cümle görünür. Altta bir alıştırma yer alır: şıkkı işaretleyip **Kontrol et** deyin, doğru cevap ve açıklama gösterilsin. **Sonraki** yeni alıştırma getirir; sonuçlar konu bazında kaydedilir.

**İpucu.** Alıştırmalar 18 sorudan oluşan ortak havuzdan gelir; konu değiştirmeden **Sonraki**'ye basmayı sürdürebilirsiniz.

**OKU & KEŞFET grubu**

### Kaynak Merkezi (Resource Center)

**Ne işe yarar.** Yalnızca kamu malı ya da Creative Commons lisanslı dört dış kaynağı (Wikibooks, Tatoeba, LibriVox, Project Gutenberg) düzey, lisans ve atıf bilgisiyle listeler.

**Nasıl kullanılır.** Karttaki **Aç ↗** düğmesi bağlantıyı varsayılan tarayıcınızda açar. Üstteki uyarı, bağlantı açmanın internet kullandığını hatırlatır.

**İpucu.** İçerikler programa kopyalanmaz; kamu malı durumu ülkeye göre değişebildiği için lisans satırını okuyun.

### PDF Okuyucu (PDF Reader)

**Ne işe yarar.** Bilgisayarınızdaki bir PDF'in metnini sayfa sayfa gösterir ve her sayfaya ayrı not tutmanızı sağlar.

**Nasıl kullanılır.** **PDF seç** ile dosyayı açın, **Sayfa** sayacıyla gezinin; sol bölmede metin görünür. Sağdaki **Sayfa notu** alanına yazıp **Kaydet** deyin. Son açtığınız PDF kaydedilir ve sayfayı yeniden açınca kendiliğinden yüklenir.

**İpucu.** Notlar profil, dosya yolu ve sayfa üçlüsüne bağlıdır.

### Ders Kitaplığı (Course Library)

**Ne işe yarar.** Programın yanındaki `Resources` klasörüne koyduğunuz ders dosyalarını (PDF, ses, metin) tek listede toplar.

**Nasıl kullanılır.** **Ders klasörünü aç** klasörü Gezgin'de açar (yalnız Windows); dosyalarınızı oraya kopyalayın, **Yenile** listeyi tazeler. Tabloda ad, tür ve MB boyut görünür; satıra **çift tıklamak** dosyayı varsayılan programda açar (yine yalnız Windows).

**İpucu.** Klasördeki `BURAYA_DERS_KOYUN.txt` yer tutucusu listede gösterilmez.

**PRATİK grubu**

### AI Öğretmen (AI Tutor)

**Ne işe yarar.** Yerel yapay zekayla dilbilgisi açıklaması, çeviri, düzeltme ve görselden metin okuma (OCR) yapar.

**Nasıl kullanılır.** **Görev** listesinden **Açıkla**, **Çevir**, **Düzelt** ya da **Görsel / OCR** seçin, metninizi yazın ve **Gönder**'e basın; yanıt alttaki kutuda görünür. Görsel için **Görsel / OCR** düğmesiyle bir PNG/JPG/WEBP dosyası seçin; metin kutusu boşsa program hazır bir yönerge kullanır.

**İpucu.** Alttaki 🔒 satırı gizlilik sözünü hatırlatır: prompt ve yanıt metni kaydedilmez, yalnız token sayıları tutulur.

### Konuşma (Speaking)

**Ne işe yarar.** Beş günlük senaryoda (`Im Café`, `Am Bahnhof`, `Im Hotel`, `Beim Einkaufen`, `Beim Arzt`) Almanca rol yapma pratiği sağlar.

**Nasıl kullanılır.** **Senaryo** seçip **Konuşmayı başlat** deyin; yapay zeka karşı rolü üstlenip kısa bir soru sorar. Almanca yanıtınızı yazıp **Gönder**'e basın; gerekirse nazikçe düzeltilir ve yeni soruyla devam edilir.

**İpucu.** Diyalog A1 seviyesinde kısa tutulur; tur sayısını artırmak uzun cümleden çok fayda sağlar.

### Yazma & El Yazısı (Writing & Handwriting)

**Ne işe yarar.** Serbest yazma alıştırması, yapay zeka ile düzeltme ve fareyle yazı çalışabileceğiniz bir alan sunar.

**Nasıl kullanılır.** Sol kutuya Almanca metninizi yazın (varsayılan yönerge: bugün ne yaptığınızı yazın) ve **AI ile düzelt**'e basın; düzeltilmiş metin, kuralın adı ve kısa açıklama altta görünür. Sağdaki **El yazısı alanı**'na fareyle yazın, **Temizle** siler.

**İpucu.** El yazısı alanı kaydedilmez; metniniz ise yalnız **AI ile düzelt** dediğinizde gönderilir.

**İLERLEME & SİSTEM grubu**

### İlerleme (Progress)

**Ne işe yarar.** **Günlük hedef**, **Günlük seri**, **Çalışılan** ve **Öğrenilen** kelime sayısı ile **Son 7 gün** çubuk grafiğini gösterir.

**Nasıl kullanılır.** Sayfa açıldığında ölçümler ve grafik kendiliğinden hesaplanır. Grafiğin altındaki **Haftalık rapor** satırı son yedi günün doğru, yanlış ve yüzde puanını verir.

**İpucu.** "Öğrenilen", Leitner kutusu 4 ve üzerine çıkmış kelimeleri sayar.

### Paketler (Packs)

**Ne işe yarar.** Kelime listenizi, isteğe bağlı olarak ilerlemenizle birlikte, `.gcapack` uzantılı taşınabilir bir dosyaya yazar ve geri okur.

**Nasıl kullanılır.** **İlerlemeyi ekle** kutusunu isteğinize göre işaretleyip **↑ Dışa aktar** ile kaydedin; başka bilgisayarda **↓ İçe aktar** ile okuyun. Kaç kelimenin alındığı ekranda yazar.

**İpucu.** Paket hedef dili kontrol eder; başka bir dil için üretilmiş paket içe aktarılmaz.

### Token Defteri (Token Ledger)

**Ne işe yarar.** Yapay zeka çağrılarının yerel özetini tutar: çağrı sayısı, toplam token ve son 500 çağrının dökümü.

**Nasıl kullanılır.** Sayfayı açmanız yeterlidir. Sütunlar tarih/saat, model, görev, prompt tokenları, tamamlama tokenları, toplam token, süre (ms) ve başarı durumudur.

**İpucu.** Defterde hiçbir istek ya da yanıt metni yoktur; alttaki 🔒 uyarısı bunu belirtir.

### Çevrimdışı Kılavuz (Offline Guide)

**Ne işe yarar.** İnternetsiz hangi özelliklerin çalıştığını, sözlüğün yön mantığını, yapay zeka seçeneklerini ve verilerin yerini program içinde özetler.

**Nasıl kullanılır.** Sayfayı açıp metni okuyun. En altta veri klasörünüzün tam yolu yazılıdır.

**İpucu.** Metin arayüz diline göre değişir.

### Ayarlar (Settings)

**Ne işe yarar.** Tema, günlük hedef, seslendirme, yerel yapay zeka ve alternatif uç nokta ayarlarını toplar.

**Nasıl kullanılır.** Alanları doldurup **Kaydet** düğmesine basın. Sayfa her açılışında ayarları yeniden okur, bu yüzden sözlük araç çubuğundan değiştirdiğiniz AI politikası burada da güncel görünür.

| Alan | Anlamı | Varsayılan |
| --- | --- | --- |
| Tema | `dark` / `light` | `dark` |
| Günlük hedef | 5-200 arası kart hedefi | `20` |
| Seslendirme | Metin okuma açık/kapalı | Açık |
| Yerel AI | LM Studio kullanımı açık/kapalı | Açık |
| LM Studio adresi | Yerel sunucu adresi | `http://127.0.0.1:1234` |
| Varsayılan model | Yerel model adı | `qwen2.5-7b-instruct` |
| Sözlük AI kaynağı | Otomatik / LM Studio / Alternatif / Kapalı | Otomatik |
| AI sözlük sonuçlarını sözlüğe kaydet | Bulunan maddeleri önbelleğe al ve eksik Türkçe karşılıkları tamamla | Açık |
| Alternatif uç noktayı kullan | İkinci sağlayıcı açık/kapalı | Kapalı |
| Temel URL | OpenAI uyumlu adres | `https://integrate.api.nvidia.com/v1` |
| Model | Alternatif uç nokta modeli | `meta/llama-3.1-8b-instruct` |
| API anahtarı | Gizli anahtar (maskeli) | boş |

**İpucu.** **Varsayılan model** listesi kurulu modelleri değil, uygulamanın bildiği profilleri gösterir: `gemma-2-9b-it`, `llama-3.1-8b-instruct`, `llava-v1.6-mistral-7b`, `qwen2-vl-7b-instruct`, `qwen2.5-14b-instruct`, `qwen2.5-7b-instruct`. Kutuya elle başka bir ad da yazabilirsiniz.

---

## 5. Sözlük (ayrıntılı)

Sözlük üç dili yan yana tutar: madde başı **Almanca**, karşılıklar **İngilizce** ve **Türkçe**. Üç kaynak birleşir: gömülü çekirdek sözlük, sizin maddeleriniz ve yapay zekanın önbelleğe aldığı maddeler.

### Yön seçici

Araç çubuğunun ikinci satırındaki **Yön:** listesi beş seçenek sunar.

| Kod | Etiket | Ne yapar | Ne zaman seçilir |
| --- | --- | --- | --- |
| `auto` | Otomatik | Üç tarafta birden arar, en iyi eşleşen taraf kazanır | Hangi dilde yazdığınızı düşünmek istemediğinizde |
| `de2en` | DE → EN | Yalnızca Almanca madde başlarında arar | Almanca bir kelimenin İngilizcesi için |
| `en2de` | EN → DE | Yalnızca İngilizce karşılıklarda arar | İngilizceden Almancaya geçerken |
| `de2tr` | DE → TR | Almanca madde başlarında arar, Türkçe sütununu öne alır | Almanca bir kelimenin Türkçesi için |
| `tr2de` | TR → DE | Yalnızca Türkçe karşılıklarda arar | Türkçeden Almancaya geçerken |

Sabit yönde yalnız kaynak dil taranır: `de2tr` yönünde `ev` yazarsanız sonuç çıkmaz, çünkü Almanca madde başlarında `ev` yoktur. Seçiminiz kaydedilir ve program yeniden açıldığında geçerli kalır; yönü değiştirince kutudaki sorgu varsa arama yenilenir. Arama kutusunun sağındaki etiket sonucun hangi yönde bulunduğunu (`DE → TR` gibi) yazar - **Otomatik** modda programın algıladığı gerçek yönü gösterir.

### Türkçe sütunu ve ayrıntı paneli

Sonuç tablosunda **Almanca**, **İngilizce**, **Türkçe**, **Tür**, **Artikel / Çoğul** ve **Kaynak** sütunları vardır. `*2tr` yönlerinde Türkçe sütunu madde başının hemen sağına taşınır; Türkçe karşılığı bilinmeyen maddelerde hücrede `—` görünür.

Sağdaki panel seçili maddeyi büyük puntoyla gösterir: artikelli madde başı (`das Haus`), tür ve cinsiyet, çoğul, **İngilizce:** ve **Türkçe:** satırları, örnek cümle ve not. Kelime, Kelime Bankası'nda kayıtlıysa `★ Kelime Bankası: …` satırı görünür.

### Arama kuralları

Sıralama katıdır: **tam eşleşme > önek > kelime başı > içerme**. Ek olarak:

- `to`, `the`, `a`, `an`, `sich` gibi baştaki sözcükler yok sayılır; `to learn` ile `learn` aynı maddeyi bulur.
- Umlautlar ve `ß` esnektir (`ae = ä`, `oe = ö`, `ue = ü`, `ss = ß`): `Strasse` yazarak `Straße` maddesine ulaşırsınız.
- Türkçe karşılıklarda Türkçe harfler ASCII karşılıklarına da katlanır (`ı/İ → i`, `ş → s`, `ğ → g`, `ç → c`, `ö → o`, `ü → u`) ve düzeltme işareti (`kâğıt`) yok sayılır: `çok` için `cok`, `öğrenmek` için `ogrenmek`, `ışık` için `isik` ya da `ISIK` yazmanız yeterlidir. Doğrudan eşleşme, katlanmış eşleşmenin üstünde sıralanır.
- Çoğul biçimler de aranır: `Häuser` yazarsanız `Haus` bulunur.
- Karşılıklar `;` ya da `/` ile anlamlara bölünür; parantez içi açıklama (`ona (erkek/nesne)`) bölünmez.
- Sonuç yoksa İngilizce not/tanım alanı son çare olarak taranır (yalnız **Otomatik** ve `EN → DE` yönlerinde).
- İki harften itibaren liste yazdıkça süzülür; bu "sessiz" arama yapay zekaya soru göndermez. Yapay zeka yalnız `Enter` ya da **Ara** ile çalışan tam aramada devreye girer.

### Kaynak etiketleri

| Etiket | Anlamı |
| --- | --- |
| gömülü | Programla birlikte gelen çekirdek sözlük |
| kullanıcı | CSV ile aktardığınız ya da elle eklediğiniz madde |
| AI | Yapay zekanın bulduğu ve önbelleğe alınan madde |

Sayfanın altındaki sayaç bu üçünü ayrı ayrı toplar: `1267 madde  ·  gömülü 1267  ·  kullanıcı 0  ·  AI 0` gibi.

### Eksik Türkçe karşılığın AI ile doldurulması

`DE → TR` yönünde bulunan maddenin Türkçe karşılığı yoksa ve AI politikası **Kapalı** değilse, program arka planda yapay zekaya sorar; durum satırında **Türkçe karşılık eksik, AI'a soruluyor…** yazar. **Ayarlar → AI sözlük sonuçlarını sözlüğe kaydet** açıkken gelen karşılık **aynı maddeye** yazılır, kopya madde oluşturulmaz; işlem bitince **Türkçe karşılık AI ile eklendi** iletisi görünür. Bu kutu kapalıysa soru yine sorulur, ama yanıt kaydedilmez ve bu ileti çıkmaz.

Karşılığı zaten olan bir maddeye yapay zeka ek bir Türkçe anlam verirse, bu anlam mevcut karşılığın sonuna eklenir, üzerine yazılmaz. Buna karşılık CSV ile aktardığınız ya da **Madde ekle** ile girdiğiniz bir kullanıcı satırı, gömülü maddenin Türkçe karşılığının **yerine geçer**.

**✦ AI'a sor** düğmesi açık bir istektir: yerel sonuç bulunsa bile yapay zeka maddelerini listenin üstüne ekler. Bu maddeler kendiliğinden kaydedilmez; beğendiğinizi seçip **💾 Sözlüğe kaydet** ile saklarsınız. Yanıtın altındaki **Yanıtlayan:** satırı hangi sağlayıcı ve modelin cevap verdiğini yazar.

### Kelime bankasına ekleme

**★ Kelime bankasına ekle** seçili maddeyi Kelime Bankası'na yazar. Türkçe alanına ilk Türkçe anlam, yoksa ilk İngilizce anlam konur; isimlerde artikel, cinsiyet ve çoğul da aktarılır. Deste adı **Sözlük DE-EN-TR** olur, böylece bu kelimeleri sonradan süzebilirsiniz.

### CSV içe/dışa aktarma

**↑ CSV dışa aktar** o an listede duran sonuçları, liste boşsa sözlüğün tamamını yazar. Dosya varsayılan olarak veri klasörünüzün `exports` alt klasörüne `dictionary_de.csv` adıyla önerilir. Sütun sırası sabittir:

| Sütun | İçerik |
| --- | --- |
| `headword` | Almanca madde başı (artikelsiz) |
| `translation` | İngilizce karşılık(lar), `;` ile ayrılır |
| `pos` | Tür kodu: `n`, `v`, `adj`, `adv`, `pron`, `prep`, `conj`, `num`, `art`, `int`, `part`, `phr` |
| `extra` | İsimlerde artikel + çoğul (`das Häuser`), diğerlerinde boş |
| `note` | Not / tanım / kullanım açıklaması |
| `source` | `builtin`, `user` ya da `ai` |
| `example` | Almanca örnek cümle |
| `tr` | Türkçe karşılık(lar), `;` ile ayrılır |

```csv
headword,translation,pos,extra,note,source,example,tr
Haus,house,n,das Häuser,,builtin,,ev
Buch,book,n,das Bücher,,builtin,,kitap
lernen,to learn; to study,v,,,builtin,,öğrenmek; ders çalışmak
schnell,fast,adj,,,builtin,,hızlı
Fenster,window,n,das Fenster,,user,Das Fenster ist offen.,pencere
```

Gömülü maddeler örnek cümle taşımaz; bu yüzden `builtin` satırlarında `example` sütunu her zaman boştur. Örnek cümle yalnız kendi eklediğiniz (`user`) ve yapay zekanın bulduğu (`ai`) maddelerde bulunur.

**↓ CSV/TSV içe aktar** `.csv`, `.tsv` ve `.txt` dosyalarını okur; ayraç dosya türüne ve içeriğe göre seçilir. Başlık satırı varsa sütunlar herhangi bir sırada olabilir (`headword`, `word`, `de`, `Deutsch`, `translation`, `meaning`, `en`, `english`, `tr`, `turkish`, `türkçe` adları tanınır); yoksa yukarıdaki sıra beklenir. `tr` sütunu olmayan eski dosyalar da okunur, boş satırlar atlanır, aktarılanlar `kullanıcı` kaynağıyla işaretlenir.

### Madde ekleme

**+ Madde ekle** bir pencere açar. Alanlar: **Almanca**, **İngilizce**, **Türkçe**, **Tür (n/v/adj/…)**, **Artikel / Çoğul**, **Not / tanım**, **Örnek cümle**. Arama kutusunda metin varsa program onu, **Otomatik** yöndeyken algıladığı dilin alanına, sabit bir yön seçiliyken o yönün kaynak dili alanına yerleştirir; kaydetmeden önce alanları denetleyin. **Almanca** ve **İngilizce** zorunludur; boşsa **Almanca ve İngilizce alanları zorunlu.** uyarısı gelir. `Enter` kaydeder, `Esc` kapatır.

---

## 6. Yapay zeka

Yapay zeka isteğe bağlıdır. Kapalıyken sözlük, tekrar, sınav, dilbilgisi, PDF ve ilerleme özellikleri eksiksiz çalışır.

### LM Studio kurulumu ve yerel sunucu

1. LM Studio uygulamasını kurun.
2. Bir sohbet modeli indirin (öneri: `qwen2.5-7b-instruct`).
3. **Local Server** bölümünde OpenAI uyumlu sunucuyu başlatın.
4. Program varsayılan olarak `http://127.0.0.1:1234` adresini kullanır; farklıysa **Ayarlar → LM Studio adresi** alanını düzeltip **Kaydet** deyin.

Bağlantı kurulunca üst şeritteki **AI:** etiketi **Kullanılabilir** olur.

### Model seçimi

Program görev başına model profilleri tutar:

| Görev | Tercih edilen modeller |
| --- | --- |
| `chat` | `qwen2.5-7b-instruct`, `llama-3.1-8b-instruct` |
| `grammar` | `qwen2.5-7b-instruct`, `qwen2.5-14b-instruct` |
| `translate` | `qwen2.5-7b-instruct`, `gemma-2-9b-it` |
| `correct` | `qwen2.5-7b-instruct`, `qwen2.5-14b-instruct` |
| `dialogue` | `qwen2.5-7b-instruct`, `llama-3.1-8b-instruct` |
| `dictionary` | `qwen2.5-7b-instruct`, `llama-3.1-8b-instruct` |
| `vision` | `qwen2-vl-7b-instruct`, `llava-v1.6-mistral-7b` |

Seçim sırası: ayarlarda yazan model kuruluysa o; değilse görev profilindeki adlar; o da yoksa kurulu modeller sıralanır. Sıralamada **uzman modeller atlanır** - adında `embed`, `rerank`, `math`, `coder`, `code-`, `moondream`, `llava`, `-vl`, `vision`, `bio`, `medic`, `whisper`, `tts`, `audio`, `clip`, `sd-` veya `stable-diffusion` geçenler gömme, matematik, kod, görüntü ya da ses içindir ve sözlük görevlerinde kötü yanıt verir; başka seçenek kalmazsa yine de kullanılırlar. Eşitlikte 4-16 milyar parametreli ve adında `instruct`, `-it`, `chat` ya da `assistant` geçen modeller öne alınır.

Sözlük çağrılarında yerel sunuculara `reasoning_effort: none` gönderilir; "düşünen" modellerin bütçeyi akıl yürütmeye harcayıp boş yanıt döndürmesini engeller. Sunucu bu alanı reddederse istek alansız yinelenir; yanıt bütçe dolduğu için kesildiyse üç katı bütçeyle bir kez daha denenir.

### Alternatif uç nokta

İkinci sağlayıcı herhangi bir **OpenAI uyumlu** hizmet olabilir: varsayılan NVIDIA NIM (`https://integrate.api.nvidia.com/v1`, model `meta/llama-3.1-8b-instruct`), ya da OpenRouter, Groq, Ollama veya yerel ağınızdaki başka bir sunucu.

1. **Ayarlar → Alternatif uç nokta** altında **Alternatif uç noktayı kullan** kutusunu işaretleyin.
2. **Temel URL** ve **Model** alanlarını doldurun, **API anahtarı** alanına anahtarınızı yapıştırın (yazarken maskelenir).
3. **Bağlantıyı test et** düğmesine basın: **Bağlantı başarılı · N model** görünür. Model listede yoksa **seçili model listede yok**, genel bir adres için anahtar girilmemişse **genel adres: sözlüğün kullanması için API anahtarı gerekli** uyarısı eklenir.
4. **Kaydet** deyin.

Yerel ağdaki bir sunucu için (`http://192.168.1.10:11434` ya da `.local` ile biten adlar) API anahtarı gerekmez; program adresin bu makinede mi, yerel ağda mı yoksa internette mi olduğunu ayırt eder ve yalnız genel adreslerde anahtar arar.

### Anahtarın saklanması

API anahtarı **hiçbir zaman** `settings.json` içine yazılmaz. Windows'ta **Kimlik Bilgisi Yöneticisi**'nde `GermanCourseAI/alt_api_key` adlı genel kimlik bilgisi olarak saklanır; Windows dışında ya da bu API başarısız olursa `settings\secrets.json` kullanılır. **Anahtarı sil** düğmesi kaydı kaldırır ve **Anahtar silindi** yazar. `GERMANCOURSEAI_API_KEY` ortam değişkeni tanımlıysa kayıtlı anahtarın yerine o kullanılır.

### AI politikası

Sözlük hangi sağlayıcıyı kullanacağını **Sözlük AI kaynağı** ayarından öğrenir. Aynı liste sözlük sayfasının araç çubuğunda **AI:** etiketiyle de bulunur; seçim ortaktır.

| Politika | Davranış |
| --- | --- |
| Otomatik | LM Studio erişilebiliyorsa o; değilse etkinse alternatif uç nokta; ikisi de yoksa kapalı |
| LM Studio | Yalnız yerel sunucu (Yerel AI açık ve erişilebilir olmalı) |
| Alternatif | Yalnız alternatif uç nokta (etkin ve anahtar koşulu sağlanmış olmalı) |
| Kapalı | Sözlük hiçbir yapay zeka isteği göndermez (AI Öğretmen, Konuşma ve Yazma sayfaları **Yerel AI** ayarına bağlıdır) |

Durum etiketi seçime göre **LM Studio: bağlı**, **Alternatif: hazır**, **AI erişilemiyor** ya da **AI kapalı** yazar. Erişilebilirlik yanıtı 30 saniye önbelleklenir.

### Token defteri

Her çağrı **Token Defteri** sayfasına bir satır düşer: tarih/saat, model, görev, prompt tokenları, tamamlama tokenları, toplam, süre (ms) ve başarı durumu. Üstteki iki kutu toplam çağrı ve toplam token sayısını verir; defter son 500 çağrıyı gösterir.

### Gizlilik

- İstek ve yanıt metni **hiçbir yere kaydedilmez**; yalnız sayısal token bilgisi tutulur.
- Alternatif uç nokta varsayılan olarak kapalıdır; açıkça açmadan internete istek gitmez.
- Yerel model kullandığınızda metniniz bilgisayarınızdan çıkmaz.
- Yapay zekanın bulduğu maddeler yerel sözlüğe yazılır; aynı kelimeyi bir daha aradığınızda sonuç çevrimdışı gelir.

---

## 7. Veri yönetimi

### Profil

Üst şeritteki profil listesi etkin öğrenciyi belirler; **+** düğmesi ad sorup yeni profil açar. Kelime ilerlemesi, çalışma günlüğü, sınavlar, PDF notları ve dilbilgisi istatistikleri profile özeldir; kelime bankası, sözlük ve token defteri paylaşılır.

### Yedekleme

| Yöntem | Ne kapsar | Nerede |
| --- | --- | --- |
| Kelime CSV'si | Kelime bankasının tamamı (13 sütun, UTF-8) | Kelime Bankası → **↑ Dışa aktar** |
| Sözlük CSV'si | Sözlük maddeleri (8 sütun) | Sözlük → **↑ CSV dışa aktar** |
| `.gcapack` paketi | Kelimeler + isteğe bağlı ilerleme | Paketler → **↑ Dışa aktar** |

En eksiksiz yedek veri klasörünün kendisini kopyalamaktır: program kapalıyken `%APPDATA%\GermanCourseAI` klasörünü, özellikle `data\GermanCourseAI.db` dosyasını kopyalayın.

### Veri klasörü

```text
%APPDATA%\GermanCourseAI\
  data\GermanCourseAI.db      SQLite veritabanı (profiller, kelimeler, ilerleme, sözlük, notlar, token kaydı)
  settings\settings.json      Gizli olmayan ayarlar
  settings\secrets.json       Yalnız Kimlik Bilgisi Yöneticisi kullanılamadığında oluşur
  exports\                    Dışa aktarımlar için önerilen klasör
  downloads\                  İndirilenler için ayrılmış klasör
```

Ders dosyalarınızın durduğu `Resources` klasörü buraya değil, programın yanına gelir.

### Sıfırlama

Program içinde "her şeyi sil" düğmesi yoktur; sıfırlama dosya düzeyinde yapılır.

- **Yalnız ilerlemeyi sıfırlamak:** yeni bir profil açıp onu kullanın; eski profil dokunulmadan kalır.
- **Her şeyi sıfırlamak:** program kapalıyken `data\GermanCourseAI.db` dosyasını silin. Program bir dahaki açılışta veritabanını, varsayılan profili ve gömülü kelime destesini yeniden kurar.
- **Ayarları sıfırlamak:** `settings\settings.json` dosyasını silin.
- **API anahtarını kaldırmak:** **Ayarlar → Anahtarı sil** düğmesini kullanın.

---

## 8. Kısayollar ve ipuçları

Program genel kısayol tuşu tanımlamaz; aşağıdakiler ilgili alan seçiliyken çalışır.

| Kısayol | Nerede | Ne yapar |
| --- | --- | --- |
| `Enter` | Sözlük arama kutusu | Tam aramayı çalıştırır (gerekirse yapay zekaya sorar) |
| `Enter` | Kelime Bankası arama kutusu | Listeyi süzer |
| `Enter` | Madde ekle penceresi | Maddeyi kaydeder |
| `Esc` | Madde ekle penceresi | Pencereyi kapatır |
| Çift tıklama | Sözlük sonuç satırı | Madde başını sesli okur |
| Çift tıklama | Ders Kitaplığı satırı | Dosyayı varsayılan programda açar (Windows) |

Pratik ipuçları:

- Sözlükte iki harf yazdığınızda liste kendiliğinden süzülür; yapay zekaya soru gitmesini istemiyorsanız `Enter`'a basmayın.
- **Son aramalar** listesi son 12 sorguyu **yönüyle birlikte** saklar; bir kaydı tıkladığınızda arama o yönle yinelenir, o yönde artık sonuç yoksa **Otomatik** moda düşer.
- **🎲 Rastgele kelime**, seçili yön ne olursa olsun kelimeyi madde başı tarafında arar; böylece `TR → DE` seçiliyken bilinen bir Almanca kelime boşuna yapay zekaya sorulmaz.
- **Kopyala** düğmesi maddeyi `das Haus — house — ev` biçiminde panoya alır.
- Arayüz dilini değiştirmek sayfaları yeniden kurar ve açık kart oturumunu sıfırlar; dili oturum başında seçin.
- Tema değişikliği **Kaydet**'e basınca uygulanır.

---

## 9. Sorun giderme

### LM Studio bağlanmıyor

**Belirti.** Üst şeritte **AI: Kullanılamıyor**, sözlükte **AI erişilemiyor** yazıyor.
**Neden ve çözüm.** Program `GET /v1/models` isteğiyle sunucuyu yoklar. LM Studio açık ve **Local Server** başlatılmış olmalı, **Ayarlar → LM Studio adresi** LM Studio'nun gösterdiği adresle aynı olmalı (varsayılan `http://127.0.0.1:1234`), **Ayarlar → Yerel AI** kutusu işaretli olmalı; güvenlik duvarı da engelliyor olabilir. Erişilebilirlik yanıtı 30 saniye önbelleklenir, bu yüzden sonuç yarım dakika gecikebilir; **Ayarlar → Kaydet** önbelleği hemen temizler. Üst şeritteki **AI:** etiketi yalnız açılışta ölçülür - güncel durumu görmek için sözlük sayfasındaki durum etiketine bakın, o sayfa her açıldığında yeniden ölçer.

### AI boş yanıt veriyor

**Belirti.** Sözlükte **AI bu sorgu için madde döndürmedi.** yazıyor.
**Neden ve çözüm.** En sık neden modelin uygunsuz olmasıdır: gömme, kod, matematik ya da görüntü modelleri yapılandırılmış JSON üretemez. **Ayarlar → Varsayılan model** alanına `qwen2.5-7b-instruct` gibi genel bir sohbet modeli yazın. İkinci neden "düşünen" modellerin bütçeyi tüketmesidir; program bunu `reasoning_effort: none` ve üç kat bütçeyle yeniden deneme ile karşılar, ama çok küçük bir model yine geçersiz JSON üretebilir. Var olmayan bir kelime aradıysanız boş yanıt doğru davranıştır.

### Türkçe karşılık yok

**Belirti.** Türkçe sütununda `—` görünüyor.
**Neden ve çözüm.** O madde henüz Türkçe karşılık taşımıyor. **Yön** listesinden **DE → TR** seçip aramayı yineleyin; program eksik karşılığı arka planda yapay zekaya sorar ve aynı maddeye yazar. Yapay zeka kullanmak istemiyorsanız **+ Madde ekle** ile alanı kendiniz doldurun ya da `tr` sütunlu bir CSV içe aktarın. **AI:** politikası **Kapalı** ise istek gönderilmez.

### macOS "açılamıyor" uyarısı

**Belirti.** "Tanımlanamayan bir geliştiriciden" benzeri bir uyarı çıkıyor.
**Neden ve çözüm.** Uygulama notarize edilmemiştir. Çift tıklamak yerine simgeye **sağ tıklayın → Aç** deyin ve açılan pencerede yine **Aç**'a basın. Bu onay yalnız ilk açılışta gerekir.

### Ses çıkmıyor

**Belirti.** **▶ Seslendir** düğmesi hiçbir şey yapmıyor.
**Neden ve çözüm.** Seslendirme Windows'un `System.Speech` sentezleyicisini PowerShell üzerinden çağırır. **Ayarlar → Seslendirme** kutusunun işaretli olduğunu doğrulayın, Windows ayarlarından bir **Almanca (de-DE) ses paketi** kurun (yoksa sistemin varsayılan sesi kullanılır) ve ses düzeyini denetleyin. macOS ile Linux'ta bu yol kullanılamaz, seslendirme sessiz kalır.

### exe açılmıyor

**Belirti.** `GermanCourseAI.exe` çift tıklanınca pencere açılmıyor.
**Neden ve çözüm.** Zip arşivini **açtığınızdan** emin olun; arşiv içinden çalıştırmak başarısız olur. SmartScreen uyarısında **Ek bilgi → Yine de çalıştır** deyin. Antivirüs, PyInstaller ile paketlenmiş dosyaları karantinaya alabilir; klasörü izin listesine ekleyin. `%APPDATA%` klasörüne yazma izniniz yoksa `GCA_HOME` ile başka bir klasör gösterin. Sorun sürerse hatayı görmek için kaynaktan çalıştırın: `python German_Course_AI.pyw`.

### Veriler nerede

**Belirti.** Yedek almak ya da veriyi başka bilgisayara taşımak istiyorsunuz.
**Neden ve çözüm.** Tam yol **Çevrimdışı Kılavuz** sayfasının altında yazılıdır: Windows'ta `%APPDATA%\GermanCourseAI`, macOS'ta `~/Library/Application Support/GermanCourseAI`, diğer sistemlerde `~/.germancourseai`. `GCA_HOME` tanımlıysa program o klasörü kullanır.

---

## 10. Sürüm notları özeti

| Sürüm | Öne çıkanlar |
| --- | --- |
| **v1.0.0** | 18 sayfalık kabuk; SM-2 / Leitner tekrar; 161 gömülü A1 kelimesi; sınav motoru; yazım, telaffuz ve 24 konuluk dilbilgisi laboratuvarları; PDF okuyucu; Ders Kitaplığı; Kaynak Merkezi; LM Studio ile AI Öğretmen, Konuşma ve Yazma; ilerleme grafiği; `.gcapack` paketleri; token defteri; koyu/açık tema; tr/en/de arayüz. |
| **v1.1.0** | Ayrı **Sözlük** sekmesi: gömülü sözlük, kaynak etiketleri, arama sıralaması, umlaut/ß toleransı, CSV/TSV içe-dışa aktarma, madde ekleme, kelime bankasına aktarma, arama geçmişi, seslendirme. Sözlükte bulunmayan kelimeler için **yapay zeka bağlantısı**: yapılandırılmış JSON madde üretimi, sonuçların önbelleklenmesi, alternatif OpenAI uyumlu uç nokta, anahtarın Kimlik Bilgisi Yöneticisi'nde saklanması, sözlük AI politikası. |
| **v1.2.0** | **Yön seçici** (`Otomatik`, `DE → EN`, `EN → DE`, `DE → TR`, `TR → DE`); sabit yönde yalnız kaynak dil aranır ve seçim kaydedilir. **Türkçe sütunu** ve ayrıntı panelinde Türkçe satırı; `*2tr` yönlerinde Türkçe sütunu öne alınır. Eksik Türkçe karşılığın yapay zeka ile **kopya oluşturmadan** tamamlanması; ek anlamların mevcut karşılığa eklenmesi, kullanıcı satırlarının karşılığın yerine geçmesi. `tr` sütunlu CSV düzeni (eski düzen de okunur). Gömülü sözlük 1267 maddeye çıktı ve her maddeye Türkçe karşılık eklendi. |
| **v1.2.1** | **Türkçe aramada ASCII ve büyük harf desteği**: "sinav" = "SINAV" = "sınav", "cok" = "çok", "ogrenci" = "öğrenci". Türkçe katlama, Almanca ö→oe katlamasından önce uygulanır; katlanarak bulunan eşleşme doğrudan eşleşmenin altına oranlanır, böylece "ask" yazan kullanıcı İngilizce karşılığı alır. Gösterilen yazım değişmez. **Kullanım kılavuzu**: depoya `docs/KULLANIM_KILAVUZU.md` (Türkçe) ve `docs/USER_GUIDE.md` (İngilizce) eklendi; kurulum, 18 ekran, sözlük ve yön seçimi, yapay zekâ kurulumu, veri yönetimi, sorun giderme ve SSS bölümlerini kapsar; PDF sürümü sürüm dosyalarına eklidir. |
| **v1.3.0** | **MIT lisansı**: proje MIT Lisansı altında yayımlandı; depoya `LICENSE` ve `THIRD_PARTY_NOTICES.md` eklendi ve her iki dosya dağıtım arşivlerinin içinde çalıştırılabilir dosyanın yanında yer alır. **Temiz sanal ortamda derleme**: Windows paketi artık yalnızca `requirements.txt` bağımlılıklarını içeren ayrı bir sanal ortamda üretilir; uygulamanın kullanmadığı kütüphaneler (pandas, SQLAlchemy, lxml, NumPy ve benzerleri) pakete girmez, dosya boyutu belirgin biçimde küçülür ve üçüncü taraf bildirimi paketle birlikte gelir. |

---

## 11. Sık sorulan sorular

**Program internetsiz çalışır mı?**
Evet. Kelime bankası, tekrar, sınav, sözlük, dilbilgisi, yazım, PDF notları, ilerleme ve paketler yereldir. İnternet yalnız Kaynak Merkezi bağlantılarında ve alternatif uç noktada gerekir.

**Yapay zeka zorunlu mu?**
Hayır. LM Studio kurulmasa da program çalışır; yapay zeka düğmeleri "AI kapalı veya LM Studio erişilemiyor." yanıtı verir. **Sözlük AI kaynağı** ayarını **Kapalı** yapmak yalnızca sözlüğün isteklerini durdurur; bütün sayfaları (AI Öğretmen, Konuşma ve Yazma dahil) susturmak için **Ayarlar → Yerel AI** kutusunun işaretini kaldırın ve **Alternatif uç noktayı kullan**'ı kapalı bırakın.

**Verilerim buluta gider mi?**
Hayır. Bütün veri bilgisayarınızdaki SQLite dosyasındadır. Yalnız alternatif uç noktayı etkinleştirirseniz sorgu metni seçtiğiniz sağlayıcıya gider; hiçbir metin kaydedilmez.

**API anahtarım nerede duruyor?**
Windows'ta Kimlik Bilgisi Yöneticisi'nde `GermanCourseAI/alt_api_key` adıyla, diğer sistemlerde `settings\secrets.json` içinde. `settings.json` dosyasına asla yazılmaz.

**Aynı bilgisayarda iki kişi çalışabilir mi?**
Evet. **+** düğmesiyle ikinci profil açın; ilerleme, sınav ve PDF notları ayrıdır.

**Kendi kelime listemi nasıl aktarırım?**
Kelime Bankası'nda **↓ İçe aktar** ile UTF-8 CSV dosyanızı seçin. Sözlük maddeleri için Sözlük sayfasındaki **↓ CSV/TSV içe aktar** düğmesini kullanın; başlık satırı varsa sütun sırası önemsizdir.

**Sözlükte kaç kelime var?**
Gömülü sözlük 1267 madde içerir ve hepsinin Türkçe karşılığı vardır; kendi maddeleriniz ile önbelleğe alınan AI maddeleri buna eklenir. Toplam sayfanın altında yazar.

**Yapay zekanın bulduğu madde kalıcı mı?**
Sözlükte sonuç çıkmadığı için sorulan aramaların sonuçları, **AI sözlük sonuçlarını sözlüğe kaydet** açıksa kendiliğinden kaydedilir. **✦ AI'a sor** ile istedikleriniz kaydedilmez; saklamak için **💾 Sözlüğe kaydet** düğmesine basın.

**"Otomatik" yön ne zaman yanılır?**
Aynı biçim hem İngilizce hem Türkçe anlam olduğunda - ve Almanca bir madde başı değilse - İngilizce taraf öne çıkar. Almanca bir madde başı her zaman diğer taraflara üstün gelir: `park` gibi aynı zamanda Almanca madde başı olan sorgular bu yüzden `DE → EN` sonucunu verir. Beklediğiniz sonucu almazsanız yönü elle seçin.

**Güncelleme verilerimi siler mi?**
Hayır. Program klasörünü yenisiyle değiştirin; veriler ayrı klasörde durur ve veritabanı şeması eklemeli güncellenir.

---

## 12. Lisans

German Course AI **MIT Lisansı** ile yayımlanır. Tam metin, program kaynağındaki `LICENSE`
dosyasındadır: programı kullanabilir, kopyalayabilir, değiştirebilir ve dağıtabilirsiniz; tek
koşul telif ve lisans bildiriminin kopyalarla birlikte kalmasıdır. Program hiçbir garanti
vermez.

Programın içinde taşıdığı üçüncü taraf bileşenler - PDF Okuyucu'nun kullandığı pypdf, PyInstaller'ın
donmuş uygulamaya eklediği Python, Tcl/Tk, SQLite ve OpenSSL gibi parçalar ve derleme araçları -
kendi lisanslarıyla gelir. Hepsinin gerçek lisansı ve ne için kullanıldığı `THIRD_PARTY_NOTICES.md`
dosyasında listelenir; bu dosya hem kaynak deposunda bulunur hem de indirdiğiniz arşivde
`GermanCourseAI.exe` (macOS'ta `GermanCourseAI.app`) ile birlikte gelir.

Sürüm 1.3.0'dan itibaren hem Windows hem macOS paketi, yalnızca `requirements.txt` içindeki
bağımlılıkları taşıyan ayrı bir sanal ortamda derlenir; bu yüzden paketlerde standart kütüphane
dışındaki tek Python paketi pypdf'tir. Dağıtılan ikili dosyalarda **GPL, LGPL veya AGPL lisanslı
hiçbir kütüphane kodu bulunmaz**. (1.2.1 ve öncesindeki Windows sürümü, NumPy'nin OpenBLAS
kütüphanesine statik bağlanmış libgfortran çalışma zamanını da taşıyordu; taşıdığı **GCC Runtime
Library Exception 3.1** istisnası nedeniyle o da hiçbir kaynak açma yükümlülüğü doğurmuyordu.)

**Kaynak Merkezi**'nde listelenen dış kaynaklar (Wikibooks, Tatoeba, LibriVox, Project Gutenberg)
programa kopyalanmaz; her biri kendi lisansını korur ve bu lisanslar sayfada görünür durumdadır.
Sizin `Resources/` klasörüne koyduğunuz ders dosyaları yerelinizde kalır ve hiçbir zaman
dağıtılmaz.
