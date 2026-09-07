# German Course AI

German Course AI, Almanca öğrenimi için yerel veriyi önceleyen bağımsız bir Windows masaüstü uygulamasıdır. Türkçe, English ve Deutsch arayüzleri; hedef dile özgü kelime, yazım, ses ve dilbilgisi içeriğiyle aynı özellik kapsamını sunar.

> Temel çalışma özellikleri ve öğrenci verileri yereldir. Kaynak bağlantılarını açmak ve isteğe bağlı uzak servisleri kullanmak internet gerektirir; uygulama bu nedenle yanıltıcı bir “%100 çevrimdışı” iddiasında bulunmaz.

Kullanım kılavuzu: [docs/KULLANIM_KILAVUZU.md](docs/KULLANIM_KILAVUZU.md) — kurulum, 18 ekran, sözlük, yapay zekâ ve sorun giderme.

## Öne çıkan özellikler

- SM-2 ve Leitner tabanlı aralıklı tekrar; günlük hedef ve seri
- 160 yerleşik A1 kelime; isimlerde artikel, cinsiyet ve çoğul
- Almanca-Türkçe-İngilizce sözlük, favoriler, yanlış kelimeler
- Üç dilli **Almanca ↔ İngilizce ↔ Türkçe sözlük** sekmesi: 1.260+ gömülü madde (artikel + çoğul), yön seçici (`Otomatik`, `DE → EN`, `EN → DE`, `DE → TR`, `TR → DE`; sabit yönde yalnızca kaynak dil aranır, seçim kaydedilir), Türkçe sütunu ve ayrıntı satırı, çoğul/umlaut/ß toleranslı arama, seslendirme, kelime bankasına ekleme (Türkçe karşılık varsa `tr` alanına), CSV/TSV içe/dışa aktarma (`tr` sütunu; başlık satırı tanınır, eski düzen kabul edilir; gömülü bir kelime için kullanıcı satırı Türkçe karşılığın yerine geçer)
- **AI destekli sözlük**: sözlükte bulunmayan kelimeler LM Studio'ya ya da alternatif bir OpenAI uyumlu uç noktaya (NVIDIA NIM veya herhangi bir URL + API anahtarı) yapılandırılmış JSON olarak sorulur; sonuçlar (artikel/çoğul, İngilizce ve Türkçe çeviri, örnek cümle, not) yerel sözlüğe önbelleklenir ve sonraki aramalar çevrimdışı çalışır; `DE → TR` yönünde Türkçe karşılığı eksik bir madde bulunursa AI arka planda sorulur ve gelen Türkçe karşılık aynı maddeye eklenir (kopya oluşmaz)
- Kart, çoktan seçmeli, yazma, dinleme ve eşleştirme çalışma seçenekleri
- CEFR A1-C1 profili ve puanlanan sınav motoru
- Ä, Ö, Ü, ß, isimlerin büyük yazımı, `ch`, `sch`, `sp`, `st`, `z`, `w`, `v`, `j`, bileşik kelime ve vurgu laboratuvarı
- Nominativ, Akkusativ, Dativ, Genitiv; artikel, sıfat, zamir, fiil, söz dizimi, zaman, edat ve sayı konuları
- Telaffuz, konuşma, serbest yazma ve el yazısı alanı
- Yerel PDF metin okuma ve sayfa notları
- Lisans ve atıf bilgili açık Kaynak Merkezi
- LM Studio ile yerel AI öğretmen; açıklama, çeviri, düzeltme, konuşma ve görsel/OCR görevleri
- Göreve göre model profilleri ve metin içermeyen token defteri
- Haftalık ilerleme raporu, açık/koyu tema ve öğrenci profilleri
- Unicode CSV ve `.gcapack` paket içe/dışa aktarımı

## Kurulum ve kaynaktan çalıştırma

Gereksinim: Python 3.11 veya üzeri.

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python .\German_Course_AI.pyw
```

Öğrenci verileri varsayılan olarak `%APPDATA%\GermanCourseAI` altında tutulur. Test veya taşınabilir deneme için `GCA_HOME` ortam değişkeniyle farklı bir klasör seçilebilir.

## Windows EXE üretimi

```powershell
python -m pip install -r requirements-dev.txt
.\build.bat
```

Çıktı: `dist\GermanCourseAI.exe`. `build`, `dist` ve kullanıcı verileri Git deposuna alınmaz.

## Yerel AI kurulumu

1. LM Studio'yu kurun ve bir sohbet modeli indirin.
2. Local Server bölümünde OpenAI uyumlu sunucuyu başlatın.
3. Varsayılan adres `http://127.0.0.1:1234` olarak ayarlıdır.
4. Uygulama içindeki Ayarlar sayfasından modeli veya adresi değiştirebilirsiniz.

LM Studio kapalıysa uygulama çalışmaya devam eder; yalnız AI düğmeleri erişilemez yanıtı gösterir. Prompt ve AI yanıt metinleri veritabanına yazılmaz. Token defteri yalnız model, görev, token sayıları, süre ve başarı durumunu saklar.

### Sözlük için AI sağlayıcısı

Sözlük sekmesi iki sağlayıcı kullanabilir:

- **LM Studio** (yerel, anahtar gerekmez) — `app.ai`, yukarıdaki adres.
- **Alternatif uç nokta** — herhangi bir OpenAI uyumlu API: varsayılan `https://integrate.api.nvidia.com/v1` (NVIDIA NIM, model `meta/llama-3.1-8b-instruct`); OpenRouter, Groq veya Ollama gibi başka bir temel URL, model adı ve API anahtarı da girilebilir. Ayarlar sayfasında etkinleştirilir, "Bağlantıyı test et" ile denenir. Yerel ağdaki bir sunucu (ör. `http://192.168.1.10:11434`, `.local` adları) için API anahtarı gerekmez; genel adreslerde anahtar zorunludur.

Ayarlardaki (ve sözlük araç çubuğundaki) **Sözlük AI kaynağı** politikası: `Otomatik` (LM Studio erişilebilirse o, değilse etkinse alternatif), `LM Studio`, `Alternatif` veya `Kapalı`. Sözlükte sonuç çıkmazsa AI arka planda sorulur; bulunan maddeler `AI` kaynağıyla listelenir ve (varsayılan olarak) `dict_entries` tablosuna kaydedilir; sözlüğün zaten bildiği bir madde başlığını yineleyen yanıtlar kaydedilmez, istenirse "Sözlüğe kaydet" ile saklanır. "AI'a sor" düğmesi yerel sonuç olsa bile AI maddelerini listenin üstüne ekler; bu maddeler otomatik kaydedilmez. AI'dan hem `translation_en` hem `translation_tr` istenir; `DE → TR` yönünde bulunan maddenin Türkçe karşılığı yoksa AI kendiliğinden sorulur ve yanıttaki Türkçe karşılık var olan maddeye yazılır (gömülü maddeler için `dict_entries` tablosuna `ai` kaynaklı bir eş satır düşer; yeni bir madde üretilmez). Karşılığı zaten olan bir madde için AI'ın verdiği ek Türkçe anlam mevcut karşılığa eklenir, üzerine yazılmaz; "Rastgele kelime" ve arama geçmişi seçili yön ne olursa olsun kelimeyi madde başı tarafında bulur.

API anahtarı Windows Kimlik Bilgisi Yöneticisi'nde (`GermanCourseAI/alt_api_key`) saklanır; Windows dışında veya API başarısız olursa `settings/secrets.json` dosyasına düşer. Anahtar hiçbir zaman `settings.json` içine yazılmaz. `GERMANCOURSEAI_API_KEY` ortam değişkeni kayıtlı anahtarı geçersiz kılar.

## Gizlilik ve internet

- Profil, kelime ilerlemesi, sınavlar, PDF notları ve token sayaçları ayrı SQLite veritabanında yerel saklanır.
- SRS, sınav, sözlük, dilbilgisi ve paket özellikleri internet olmadan çalışır.
- Kaynak Merkezi bağlantılarını açmak internet kullanır ve kullanıcı eylemi gerektirir.
- Uzak AI servisleri isteğe bağlıdır ve varsayılan olarak kapalıdır; API anahtarı Kimlik Bilgisi Yöneticisi'nde tutulur, ayar dosyasına yazılmaz.

## Testler

```powershell
python -m pytest -q
```

Testler pencere/18 sayfa kurulumu, anlık ve kalıcı dil değişimi, i18n bütünlüğü, SQLite geçişi, 150+ kelime, 1.260+ maddelik sözlük motoru (sabit ve otomatik yönler, Türkçe alanı, içe/dışa aktarma, SQLite kullanıcı maddeleri), yerel sahte OpenAI sunucusuyla AI sözlük araması (JSON ayrıştırma, Bearer başlığı, sağlayıcı seçimi, sözlük sekmesi akışı), gizli anahtar deposu (dosya arka ucu), `dict_entries` şema geçişi, SRS, kart/sınav akışı, `ä/ae` ve `ß/ss` araması, doğru yazım kontrolü, Unicode CSV, AI çevrimdışı davranışı, token gizliliği ve paket turunu kapsar. Testler gerçek ağa ya da Kimlik Bilgisi Yöneticisi'ne asla dokunmaz.

## Proje yapısı

```text
German_Course_AI.pyw    Uygulama girişi
gca/                    Bağımsız Python paketi
  app.py                Tkinter kabuğu ve dil seçici
  tabs/                 Modüler öğrenme, laboratuvar, okuma ve sistem sayfaları
  db.py                 SQLite şema, geçiş ve depolar
  srs.py                SM-2 / Leitner hesapları
  content.py            Almancaya özgü laboratuvar içeriği
  seed_words.py         Özgün A1 başlangıç sözlüğü
  dictionary.py         Sözlük motoru ve yapılandırılmış AI araması
  dict_data.py          Gömülü DE-EN-TR sözlük verisi
  ai_client.py          OpenAI uyumlu istemci (LM Studio, NIM, ...) ve sağlayıcı seçimi
  secrets.py            API anahtarı deposu (Kimlik Bilgisi Yöneticisi / dosya)
tests/                  Otomatik testler
grammar/                Çevrimdışı dilbilgisi notları
Resources/              Kullanıcının ders dosyaları
docs/presentation/      Düzenlenebilir PPTX, PDF ve ekran görüntüleri
```

## Açık kaynak kataloğu

Uygulama, içerikleri pakete kopyalamaz; yalnız lisans ve atıf bilgili bağlantılar sunar. Katalog Wikibooks (CC BY-SA), Tatoeba (CC BY 2.0 FR / seçili CC0), LibriVox ve Project Gutenberg kamu malı koleksiyonlarını içerir. Kamu malı durumu ülkeye göre değişebileceğinden her kayıt bu uyarıyı görünür tutar.
