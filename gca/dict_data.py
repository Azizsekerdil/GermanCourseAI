"""Built-in German <-> English <-> Turkish core dictionary (A1-B1, ~900 entries).

Line format:  headword|pos [article] [plural]|english; english 2[|note[|türkçe; türkçe 2]]
Nouns carry their article and plural in the second field (``n das Häuser``).
Irregular verb forms go into the optional note field (``ging, ist gegangen``).
The optional fifth field is the Turkish gloss (senses separated by ``; ``); leave the note field empty
to add one without a note (``Haus|n das Häuser|house||ev``). Entries without it show "—" in the
Turkish column until the AI fills the gloss in.
"""

DATA = r"""
# ---- greetings / politeness ----
Hallo|int|hello; hi||merhaba; selam
Guten Morgen|phr|good morning||günaydın
Guten Tag|phr|good day; hello||iyi günler; merhaba
Guten Abend|phr|good evening||iyi akşamlar
Gute Nacht|phr|good night||iyi geceler
Auf Wiedersehen|phr|goodbye||hoşça kalın; güle güle
Tschüss|int|bye||hoşça kal; bay bay
bis bald|phr|see you soon||yakında görüşürüz
bis später|phr|see you later||sonra görüşürüz
danke|int|thank you; thanks||teşekkürler; sağ ol
vielen Dank|phr|thank you very much||çok teşekkür ederim
bitte|part|please; you are welcome||lütfen; rica ederim
Entschuldigung|n die Entschuldigungen|excuse me; apology||affedersiniz; özür
es tut mir leid|phr|I am sorry||üzgünüm; özür dilerim
ja|part|yes||evet
nein|part|no||hayır
doch|part|yes (contradicting a negative); but; after all||evet (olumsuz soruya yanıt); yine de; ama
gern|adv|gladly; with pleasure||seve seve; memnuniyetle
gerne|adv|gladly; with pleasure||seve seve; memnuniyetle
Willkommen|n das|welcome||hoş geldiniz
Herzlichen Glückwunsch|phr|congratulations||tebrikler
Alles Gute|phr|all the best||her şey gönlünce olsun; iyi dileklerimle
Viel Glück|phr|good luck||bol şans; iyi şanslar
Guten Appetit|phr|enjoy your meal||afiyet olsun
Gesundheit|n die|health; bless you||sağlık; çok yaşa
Prost|int|cheers||şerefe
Wie geht es dir|phr|how are you (informal)||nasılsın
Wie geht es Ihnen|phr|how are you (formal)||nasılsınız
Mir geht es gut|phr|I am fine||iyiyim
Wie heißt du|phr|what is your name (informal)||adın ne
Ich heiße|phr|my name is||benim adım
Ich komme aus|phr|I come from||ben ...'dan geliyorum; ...'lıyım
Ich verstehe nicht|phr|I do not understand||anlamıyorum
Ich weiß nicht|phr|I do not know||bilmiyorum
Wie bitte|phr|pardon; sorry, what?||efendim; pardon
Sprechen Sie Englisch|phr|do you speak English||İngilizce biliyor musunuz
Können Sie das wiederholen|phr|can you repeat that||tekrar edebilir misiniz
Wie viel kostet das|phr|how much does it cost||bu ne kadar; bunun fiyatı ne
Wo ist|phr|where is||nerede
Ich hätte gern|phr|I would like||... istiyorum; ... rica ediyorum
Ich möchte|phr|I would like||istiyorum; isterim
# ---- question words ----
wer|pron|who||kim
was|pron|what||ne
wo|adv|where||nerede
wohin|adv|where to||nereye
woher|adv|where from||nereden
wann|adv|when||ne zaman
warum|adv|why||neden; niçin
wieso|adv|why; how come||neden; nasıl olur
wie|adv|how||nasıl
welcher|pron|which||hangi
wessen|pron|whose||kimin
wie viel|phr|how much||ne kadar
wie viele|phr|how many||kaç tane; kaç
# ---- pronouns / articles ----
ich|pron|I||ben
du|pron|you (singular, informal)||sen
er|pron|he||o (erkek)
sie|pron|she; they; you (formal, capitalised)||o (kadın); onlar; siz
es|pron|it||o (nesne)
wir|pron|we||biz
ihr|pron|you (plural, informal); her; their||siz; onun (kadın); onların
Sie|pron|you (formal)||siz (resmî)
mich|pron|me (accusative)||beni
mir|pron|me (dative)||bana
dich|pron|you (accusative)||seni
dir|pron|you (dative)||sana
ihn|pron|him||onu (erkek)
ihm|pron|him; it (dative)||ona (erkek, nesne)
uns|pron|us||bizi; bize
euch|pron|you (plural, object)||sizi; size
ihnen|pron|them (dative)||onlara
mein|pron|my||benim
dein|pron|your (informal)||senin
sein|pron|his; its||onun (erkek, nesne)
unser|pron|our||bizim
euer|pron|your (plural)||sizin
Ihr|pron|your (formal)||sizin (resmî)
der|art|the (masculine)||belirli tanımlık (eril)
die|art|the (feminine; plural)||belirli tanımlık (dişil; çoğul)
das|art|the (neuter)||belirli tanımlık (nötr)
ein|art|a; an (masculine, neuter)||bir (eril, nötr)
eine|art|a; an (feminine)||bir (dişil)
kein|pron|no; not a; none||hiç; hiçbir
dieser|pron|this||bu
jener|pron|that||şu; o
jeder|pron|each; every||her; her biri
alle|pron|all; everyone||hepsi; herkes
alles|pron|everything||her şey
etwas|pron|something; some||bir şey; biraz
nichts|pron|nothing||hiçbir şey
jemand|pron|someone||birisi; biri
niemand|pron|nobody||hiç kimse
man|pron|one; you; people (impersonal)||insan; kişi (genel özne)
sich|pron|oneself; himself; herself; themselves||kendini; kendisi
selbst|pron|self; myself; even||kendi; bizzat; hatta
einander|pron|each other||birbirini; birbirine
# ---- numbers ----
null|num|zero||sıfır
eins|num|one||bir
zwei|num|two||iki
drei|num|three||üç
vier|num|four||dört
fünf|num|five||beş
sechs|num|six||altı
sieben|num|seven||yedi
acht|num|eight||sekiz
neun|num|nine||dokuz
zehn|num|ten||on
elf|num|eleven||on bir
zwölf|num|twelve||on iki
dreizehn|num|thirteen||on üç
vierzehn|num|fourteen||on dört
fünfzehn|num|fifteen||on beş
sechzehn|num|sixteen||on altı
siebzehn|num|seventeen||on yedi
achtzehn|num|eighteen||on sekiz
neunzehn|num|nineteen||on dokuz
zwanzig|num|twenty||yirmi
einundzwanzig|num|twenty-one||yirmi bir
dreißig|num|thirty||otuz
vierzig|num|forty||kırk
fünfzig|num|fifty||elli
sechzig|num|sixty||altmış
siebzig|num|seventy||yetmiş
achtzig|num|eighty||seksen
neunzig|num|ninety||doksan
hundert|num|hundred||yüz
tausend|num|thousand||bin
Million|n die Millionen|million||milyon
erste|num|first||birinci; ilk
zweite|num|second||ikinci
dritte|num|third||üçüncü
letzte|adj|last||son; sonuncu
Hälfte|n die Hälften|half||yarı; yarım
halb|adj|half||yarım; yarı
Mal|n das Male|time (occasion)||kez; defa
einmal|adv|once||bir kez; bir zamanlar
zweimal|adv|twice||iki kez
viel|adv|much; a lot||çok
viele|pron|many||birçok; çok
wenig|adv|little; few||az
einige|pron|some; several||bazı; birkaç
ein paar|phr|a few; a couple of||birkaç
ein bisschen|phr|a little; a bit||biraz; azıcık
# ---- time ----
Zeit|n die Zeiten|time||zaman; vakit
Uhr|n die Uhren|clock; watch; o'clock||saat
Stunde|n die Stunden|hour; lesson||saat; ders
Minute|n die Minuten|minute||dakika
Sekunde|n die Sekunden|second||saniye
Tag|n der Tage|day||gün
Nacht|n die Nächte|night||gece
Morgen|n der Morgen|morning||sabah
Vormittag|n der Vormittage|late morning||öğleden önce; kuşluk vakti
Mittag|n der Mittage|noon; midday||öğle
Nachmittag|n der Nachmittage|afternoon||öğleden sonra
Abend|n der Abende|evening||akşam
Woche|n die Wochen|week||hafta
Wochenende|n das Wochenenden|weekend||hafta sonu
Monat|n der Monate|month||ay
Jahr|n das Jahre|year||yıl; sene
Jahrhundert|n das Jahrhunderte|century||yüzyıl
heute|adv|today||bugün
morgen|adv|tomorrow||yarın
gestern|adv|yesterday||dün
übermorgen|adv|the day after tomorrow||öbür gün
vorgestern|adv|the day before yesterday||evvelsi gün
jetzt|adv|now||şimdi
gleich|adv|right away; in a moment; same||hemen; birazdan; aynı
sofort|adv|immediately||derhal; hemen
bald|adv|soon||yakında
später|adv|later||sonra; daha sonra
früher|adv|earlier; formerly||daha önce; eskiden
früh|adv|early||erken
spät|adv|late||geç
immer|adv|always||her zaman; daima
nie|adv|never||asla; hiç
niemals|adv|never||asla; hiçbir zaman
manchmal|adv|sometimes||bazen
oft|adv|often||sık sık; çoğu zaman
selten|adv|rarely||nadiren; seyrek
meistens|adv|mostly; usually||çoğunlukla; genellikle
schon|adv|already||zaten; çoktan
noch|adv|still; yet||hâlâ; henüz; daha
noch nicht|phr|not yet||henüz değil
wieder|adv|again||yine; tekrar
zuerst|adv|first; at first||önce; ilk önce
dann|adv|then||sonra; o zaman
danach|adv|after that||ondan sonra; ardından
zuletzt|adv|last; finally||en son; sonunda
endlich|adv|finally; at last||nihayet; sonunda
plötzlich|adv|suddenly||aniden; birdenbire
lange|adv|for a long time||uzun süre
kurz|adv|briefly; short||kısaca; kısa
Montag|n der Montage|Monday||pazartesi
Dienstag|n der Dienstage|Tuesday||salı
Mittwoch|n der Mittwoche|Wednesday||çarşamba
Donnerstag|n der Donnerstage|Thursday||perşembe
Freitag|n der Freitage|Friday||cuma
Samstag|n der Samstage|Saturday||cumartesi
Sonntag|n der Sonntage|Sunday||pazar
Januar|n der Januare|January||ocak
Februar|n der Februare|February||şubat
März|n der Märze|March||mart
April|n der Aprile|April||nisan
Mai|n der Maie|May||mayıs
Juni|n der Junis|June||haziran
Juli|n der Julis|July||temmuz
August|n der Auguste|August||ağustos
September|n der September|September||eylül
Oktober|n der Oktober|October||ekim
November|n der November|November||kasım
Dezember|n der Dezember|December||aralık
Frühling|n der Frühlinge|spring||ilkbahar; bahar
Sommer|n der Sommer|summer||yaz
Herbst|n der Herbste|autumn; fall||sonbahar; güz
Winter|n der Winter|winter||kış
Feiertag|n der Feiertage|public holiday||resmî tatil; bayram günü
Urlaub|n der Urlaube|vacation; holiday||tatil; izin
Ferien|n die|school holidays||okul tatili; tatil
Geburtstag|n der Geburtstage|birthday||doğum günü
Termin|n der Termine|appointment; date; deadline||randevu; son tarih
Kalender|n der Kalender|calendar||takvim
Datum|n das Daten|date||tarih
# ---- family / people ----
Mensch|n der Menschen|human; person||insan; kişi
Leute|n die|people||insanlar; halk
Mann|n der Männer|man; husband||adam; erkek; koca
Frau|n die Frauen|woman; wife; Mrs||kadın; eş (karı); hanım
Kind|n das Kinder|child||çocuk
Junge|n der Jungen|boy||oğlan; erkek çocuk
Mädchen|n das Mädchen|girl||kız
Baby|n das Babys|baby||bebek
Familie|n die Familien|family||aile
Eltern|n die|parents||anne baba; ebeveynler
Mutter|n die Mütter|mother||anne
Vater|n der Väter|father||baba
Mama|n die Mamas|mom||anne; anneciğim
Papa|n der Papas|dad||baba; babacığım
Sohn|n der Söhne|son||oğul
Tochter|n die Töchter|daughter||kız (evlat)
Bruder|n der Brüder|brother||erkek kardeş; ağabey
Schwester|n die Schwestern|sister||kız kardeş; abla
Geschwister|n die|siblings||kardeşler
Großmutter|n die Großmütter|grandmother||büyükanne; nine
Großvater|n der Großväter|grandfather||büyükbaba; dede
Oma|n die Omas|grandma||nine; babaanne; anneanne
Opa|n der Opas|grandpa||dede
Enkel|n der Enkel|grandson; grandchild||torun
Onkel|n der Onkel|uncle||amca; dayı; enişte
Tante|n die Tanten|aunt||teyze; hala; yenge
Cousin|n der Cousins|cousin (male)||kuzen (erkek)
Cousine|n die Cousinen|cousin (female)||kuzen (kız)
Ehemann|n der Ehemänner|husband||koca; eş
Ehefrau|n die Ehefrauen|wife||karı; eş
Freund|n der Freunde|friend; boyfriend||arkadaş; erkek arkadaş
Freundin|n die Freundinnen|friend (female); girlfriend||arkadaş (kadın); kız arkadaş
Nachbar|n der Nachbarn|neighbour||komşu
Gast|n der Gäste|guest||misafir; konuk
Kollege|n der Kollegen|colleague||meslektaş; iş arkadaşı
Chef|n der Chefs|boss||patron; şef
Herr|n der Herren|Mr; gentleman; lord||bay; beyefendi; efendi
Name|n der Namen|name||ad; isim
Vorname|n der Vornamen|first name||ad; ön ad
Nachname|n der Nachnamen|surname||soyadı
Alter|n das|age||yaş
Erwachsene|n der Erwachsenen|adult||yetişkin
Jugendliche|n der Jugendlichen|teenager; young person||genç; ergen
Person|n die Personen|person||kişi; şahıs
Bevölkerung|n die|population||nüfus
# ---- jobs ----
Arbeit|n die Arbeiten|work; job||iş; çalışma
Beruf|n der Berufe|profession; occupation||meslek
Arzt|n der Ärzte|doctor (male)||doktor (erkek); hekim
Ärztin|n die Ärztinnen|doctor (female)||doktor (kadın); hekim
Lehrer|n der Lehrer|teacher||öğretmen
Lehrerin|n die Lehrerinnen|teacher (female)||öğretmen (kadın)
Schüler|n der Schüler|pupil; student (school)||öğrenci (okul)
Student|n der Studenten|student (university)||öğrenci (üniversite)
Ingenieur|n der Ingenieure|engineer||mühendis
Programmierer|n der Programmierer|programmer||programcı
Verkäufer|n der Verkäufer|shop assistant; salesman||satıcı; tezgâhtar
Koch|n der Köche|cook; chef||aşçı
Kellner|n der Kellner|waiter||garson
Fahrer|n der Fahrer|driver||sürücü; şoför
Polizist|n der Polizisten|police officer||polis; polis memuru
Journalist|n der Journalisten|journalist||gazeteci
Künstler|n der Künstler|artist||sanatçı
Musiker|n der Musiker|musician||müzisyen
Schauspieler|n der Schauspieler|actor||oyuncu; aktör
Schriftsteller|n der Schriftsteller|writer||yazar
Anwalt|n der Anwälte|lawyer||avukat
Bäcker|n der Bäcker|baker||fırıncı
Friseur|n der Friseure|hairdresser||kuaför; berber
Krankenschwester|n die Krankenschwestern|nurse||hemşire
Krankenpfleger|n der Krankenpfleger|nurse (male)||hemşire (erkek); hastabakıcı
Handwerker|n der Handwerker|craftsman||zanaatkâr; usta
Mechaniker|n der Mechaniker|mechanic||tamirci; mekanisyen
Sekretärin|n die Sekretärinnen|secretary||sekreter (kadın)
Beamte|n der Beamten|civil servant||memur; devlet memuru
Unternehmer|n der Unternehmer|entrepreneur||girişimci; iş insanı
Wissenschaftler|n der Wissenschaftler|scientist||bilim insanı
Übersetzer|n der Übersetzer|translator||çevirmen; tercüman
Firma|n die Firmen|company; firm||firma; şirket
Unternehmen|n das Unternehmen|company; enterprise||şirket; işletme
Büro|n das Büros|office||ofis; büro
Fabrik|n die Fabriken|factory||fabrika
Gehalt|n das Gehälter|salary||maaş
Lohn|n der Löhne|wage||ücret; yevmiye
Kunde|n der Kunden|customer||müşteri
Besprechung|n die Besprechungen|meeting||toplantı; görüşme
Vertrag|n der Verträge|contract||sözleşme; kontrat
Bewerbung|n die Bewerbungen|application (job)||iş başvurusu; başvuru
Lebenslauf|n der Lebensläufe|CV; résumé||özgeçmiş
Stelle|n die Stellen|position; job; place||iş; kadro; yer
arbeitslos|adj|unemployed||işsiz
Karriere|n die Karrieren|career||kariyer
# ---- home ----
Haus|n das Häuser|house||ev
Wohnung|n die Wohnungen|flat; apartment||daire; apartman dairesi
Zimmer|n das Zimmer|room||oda
Küche|n die Küchen|kitchen||mutfak
Schlafzimmer|n das Schlafzimmer|bedroom||yatak odası
Wohnzimmer|n das Wohnzimmer|living room||oturma odası; salon
Badezimmer|n das Badezimmer|bathroom||banyo
Bad|n das Bäder|bath; bathroom||banyo
Toilette|n die Toiletten|toilet||tuvalet
Flur|n der Flure|hallway; corridor||koridor; hol
Balkon|n der Balkone|balcony||balkon
Garten|n der Gärten|garden||bahçe
Keller|n der Keller|cellar; basement||bodrum; kiler
Dach|n das Dächer|roof||çatı
Stock|n der Stockwerke|floor; storey||kat
Treppe|n die Treppen|stairs||merdiven
Aufzug|n der Aufzüge|lift; elevator||asansör
Tür|n die Türen|door||kapı
Fenster|n das Fenster|window||pencere
Wand|n die Wände|wall (interior)||duvar
Boden|n der Böden|floor; ground; soil||zemin; yer; toprak
Decke|n die Decken|ceiling; blanket||tavan; battaniye
Möbel|n die|furniture||mobilya
Tisch|n der Tische|table||masa
Stuhl|n der Stühle|chair||sandalye
Sessel|n der Sessel|armchair||koltuk
Sofa|n das Sofas|sofa||kanepe
Bett|n das Betten|bed||yatak
Schrank|n der Schränke|cupboard; wardrobe||dolap; gardırop
Regal|n das Regale|shelf||raf
Spiegel|n der Spiegel|mirror||ayna
Lampe|n die Lampen|lamp||lamba
Licht|n das Lichter|light||ışık
Teppich|n der Teppiche|carpet||halı
Bild|n das Bilder|picture; image||resim; görüntü
Kühlschrank|n der Kühlschränke|fridge||buzdolabı
Herd|n der Herde|stove; cooker||ocak
Ofen|n der Öfen|oven||fırın; soba
Waschmaschine|n die Waschmaschinen|washing machine||çamaşır makinesi
Fernseher|n der Fernseher|television set||televizyon
Schlüssel|n der Schlüssel|key||anahtar
Müll|n der|rubbish; garbage||çöp
Miete|n die Mieten|rent||kira
Nachbarschaft|n die Nachbarschaften|neighbourhood||mahalle; komşuluk
aufräumen|v|to tidy up||toplamak; düzenlemek
putzen|v|to clean||temizlemek
waschen|v|to wash|wusch, gewaschen|yıkamak
kochen|v|to cook; to boil||yemek pişirmek; kaynatmak
wohnen|v|to live; to reside||oturmak; ikamet etmek
umziehen|v|to move (house)|zog um, ist umgezogen|taşınmak
mieten|v|to rent||kiralamak
# ---- everyday objects ----
Ding|n das Dinge|thing||şey; nesne
Sache|n die Sachen|thing; matter||şey; mesele
Tasche|n die Taschen|bag; pocket||çanta; cep
Rucksack|n der Rucksäcke|backpack||sırt çantası
Koffer|n der Koffer|suitcase||bavul; valiz
Geldbörse|n die Geldbörsen|wallet; purse||cüzdan
Geld|n das|money||para
Handy|n das Handys|mobile phone||cep telefonu
Telefon|n das Telefone|telephone||telefon
Computer|n der Computer|computer||bilgisayar
Laptop|n der Laptops|laptop||dizüstü bilgisayar; laptop
Brille|n die Brillen|glasses||gözlük
Regenschirm|n der Regenschirme|umbrella||şemsiye
Buch|n das Bücher|book||kitap
Heft|n das Hefte|exercise book; notebook||defter
Stift|n der Stifte|pen; pencil||kalem
Kugelschreiber|n der Kugelschreiber|ballpoint pen||tükenmez kalem
Bleistift|n der Bleistifte|pencil||kurşun kalem
Papier|n das Papiere|paper||kâğıt
Brief|n der Briefe|letter (mail)||mektup
Zeitung|n die Zeitungen|newspaper||gazete
Zeitschrift|n die Zeitschriften|magazine||dergi
Foto|n das Fotos|photo||fotoğraf
Geschenk|n das Geschenke|present; gift||hediye; armağan
Spielzeug|n das Spielzeuge|toy||oyuncak
Ball|n der Bälle|ball||top
Karte|n die Karten|card; map; ticket||kart; harita; bilet
Schachtel|n die Schachteln|box (small)||kutu (küçük)
Kiste|n die Kisten|crate; box||sandık; kasa
Flasche|n die Flaschen|bottle||şişe
# ---- clothing ----
Kleidung|n die|clothing||giysi; kıyafet
Kleid|n das Kleider|dress||elbise
Hemd|n das Hemden|shirt||gömlek
T-Shirt|n das T-Shirts|T-shirt||tişört
Hose|n die Hosen|trousers; pants||pantolon
Jeans|n die Jeans|jeans||kot pantolon; jean
Rock|n der Röcke|skirt||etek
Mantel|n der Mäntel|coat||palto; manto
Jacke|n die Jacken|jacket||ceket; mont
Anzug|n der Anzüge|suit||takım elbise
Pullover|n der Pullover|sweater||kazak
Mütze|n die Mützen|cap; beanie||bere; kasket
Hut|n der Hüte|hat||şapka
Schal|n der Schals|scarf||atkı; şal
Handschuh|n der Handschuhe|glove||eldiven
Socke|n die Socken|sock||çorap
Schuh|n der Schuhe|shoe||ayakkabı
Stiefel|n der Stiefel|boot||çizme; bot
Turnschuh|n der Turnschuhe|sneaker||spor ayakkabı
Größe|n die Größen|size||beden; boyut; büyüklük
anziehen|v|to put on (clothes); to attract|zog an, angezogen|giymek; çekmek (cezbetmek)
ausziehen|v|to take off (clothes); to move out|zog aus, ausgezogen|çıkarmak (giysi); taşınmak (evden)
tragen|v|to wear; to carry|trug, getragen|giymek; taşımak
anprobieren|v|to try on||denemek (giysi); prova etmek
# ---- body / health ----
Körper|n der Körper|body||vücut; beden
Kopf|n der Köpfe|head||baş; kafa
Gesicht|n das Gesichter|face||yüz
Auge|n das Augen|eye||göz
Ohr|n das Ohren|ear||kulak
Nase|n die Nasen|nose||burun
Mund|n der Münder|mouth||ağız
Zahn|n der Zähne|tooth||diş
Haar|n das Haare|hair||saç; kıl
Hals|n der Hälse|neck; throat||boyun; boğaz
Schulter|n die Schultern|shoulder||omuz
Arm|n der Arme|arm||kol
Hand|n die Hände|hand||el
Finger|n der Finger|finger||parmak
Bein|n das Beine|leg||bacak
Fuß|n der Füße|foot||ayak
Knie|n das Knie|knee||diz
Rücken|n der Rücken|back||sırt
Bauch|n der Bäuche|belly; stomach||karın; göbek; mide
Herz|n das Herzen|heart||kalp; yürek
Blut|n das|blood||kan
Haut|n die Häute|skin||deri; cilt
gesund|adj|healthy||sağlıklı
krank|adj|ill; sick||hasta
Krankheit|n die Krankheiten|illness; disease||hastalık
Schmerz|n der Schmerzen|pain||ağrı; acı
Kopfschmerzen|n die|headache||baş ağrısı
Fieber|n das|fever||ateş (hastalık)
Erkältung|n die Erkältungen|cold (illness)||soğuk algınlığı; nezle
Husten|n der|cough||öksürük
Medikament|n das Medikamente|medicine; drug||ilaç
Tablette|n die Tabletten|tablet; pill||tablet; hap
Apotheke|n die Apotheken|pharmacy||eczane
Krankenhaus|n das Krankenhäuser|hospital||hastane
Praxis|n die Praxen|doctor's office; practice||muayenehane; doktor muayenehanesi
Notarzt|n der Notärzte|emergency doctor||acil doktoru
Unfall|n der Unfälle|accident||kaza
müde|adj|tired||yorgun
schlafen|v|to sleep|schlief, geschlafen|uyumak
einschlafen|v|to fall asleep|schlief ein, ist eingeschlafen|uykuya dalmak
aufwachen|v|to wake up|wachte auf, ist aufgewacht|uyanmak
aufstehen|v|to get up|stand auf, ist aufgestanden|kalkmak; ayağa kalkmak
sich ausruhen|v|to rest||dinlenmek
sich erholen|v|to recover; to relax||iyileşmek; dinlenmek
wehtun|v|to hurt|tat weh, wehgetan|ağrımak; acıtmak
# ---- food / drink ----
Essen|n das|food; meal||yemek; yiyecek
Frühstück|n das Frühstücke|breakfast||kahvaltı
Mittagessen|n das Mittagessen|lunch||öğle yemeği
Abendessen|n das Abendessen|dinner; supper||akşam yemeği
Brot|n das Brote|bread||ekmek
Brötchen|n das Brötchen|bread roll||küçük ekmek; sandviç ekmeği
Butter|n die|butter||tereyağı
Käse|n der|cheese||peynir
Milch|n die|milk||süt
Ei|n das Eier|egg||yumurta
Fleisch|n das|meat||et
Hähnchen|n das Hähnchen|chicken (food)||tavuk (yemek); piliç
Fisch|n der Fische|fish||balık
Wurst|n die Würste|sausage||sosis; sucuk
Suppe|n die Suppen|soup||çorba
Reis|n der|rice||pirinç; pilav
Nudel|n die Nudeln|noodle; pasta||makarna; erişte
Kartoffel|n die Kartoffeln|potato||patates
Gemüse|n das|vegetables||sebze
Obst|n das|fruit||meyve
Apfel|n der Äpfel|apple||elma
Birne|n die Birnen|pear; light bulb||armut; ampul
Banane|n die Bananen|banana||muz
Orange|n die Orangen|orange||portakal
Zitrone|n die Zitronen|lemon||limon
Traube|n die Trauben|grape||üzüm
Erdbeere|n die Erdbeeren|strawberry||çilek
Tomate|n die Tomaten|tomato||domates
Gurke|n die Gurken|cucumber||salatalık
Zwiebel|n die Zwiebeln|onion||soğan
Knoblauch|n der|garlic||sarımsak
Salat|n der Salate|salad; lettuce||salata; marul
Karotte|n die Karotten|carrot||havuç
Pilz|n der Pilze|mushroom||mantar
Salz|n das|salt||tuz
Zucker|n der|sugar||şeker
Pfeffer|n der|pepper||karabiber; biber
Öl|n das Öle|oil||yağ
Honig|n der|honey||bal
Kuchen|n der Kuchen|cake||kek; pasta
Keks|n der Kekse|biscuit; cookie||bisküvi; kurabiye
Schokolade|n die Schokoladen|chocolate||çikolata
Eis|n das|ice cream; ice||dondurma; buz
Süßigkeit|n die Süßigkeiten|sweet; candy||şekerleme; tatlı
Wasser|n das|water||su
Tee|n der Tees|tea||çay
Kaffee|n der|coffee||kahve
Saft|n der Säfte|juice||meyve suyu
Bier|n das Biere|beer||bira
Wein|n der Weine|wine||şarap
Glas|n das Gläser|glass||bardak; cam
Tasse|n die Tassen|cup||fincan
Teller|n der Teller|plate||tabak
Löffel|n der Löffel|spoon||kaşık
Gabel|n die Gabeln|fork||çatal
Messer|n das Messer|knife||bıçak
Topf|n der Töpfe|pot; saucepan||tencere
Pfanne|n die Pfannen|pan||tava
Restaurant|n das Restaurants|restaurant||restoran; lokanta
Café|n das Cafés|cafe||kafe
Bäckerei|n die Bäckereien|bakery||fırın; pastane
Speisekarte|n die Speisekarten|menu||yemek listesi; menü
Rechnung|n die Rechnungen|bill; invoice||hesap; fatura
Trinkgeld|n das Trinkgelder|tip (money)||bahşiş
lecker|adj|tasty; delicious||lezzetli
süß|adj|sweet; cute||tatlı; şirin
sauer|adj|sour; annoyed||ekşi; kızgın
scharf|adj|spicy; sharp||acı (baharatlı); keskin
frisch|adj|fresh||taze
hungrig|adj|hungry||aç
durstig|adj|thirsty||susamış
satt|adj|full (after eating)||tok
Hunger|n der|hunger||açlık
Durst|n der|thirst||susuzluk
essen|v|to eat|aß, gegessen|yemek
trinken|v|to drink|trank, getrunken|içmek
frühstücken|v|to have breakfast||kahvaltı yapmak
bestellen|v|to order||sipariş etmek; ısmarlamak
bezahlen|v|to pay||ödemek
schmecken|v|to taste (good)||tadı olmak; lezzetli gelmek
# ---- city / transport ----
Stadt|n die Städte|city; town||şehir; kent
Dorf|n das Dörfer|village||köy
Land|n das Länder|country; land; state||ülke; kara; eyalet
Hauptstadt|n die Hauptstädte|capital city||başkent
Straße|n die Straßen|street; road||cadde; sokak; yol
Platz|n der Plätze|square; place; seat; space||meydan; yer; koltuk
Weg|n der Wege|way; path||yol; patika
Brücke|n die Brücken|bridge||köprü
Park|n der Parks|park||park
Zentrum|n das Zentren|centre||merkez
Innenstadt|n die Innenstädte|city centre||şehir merkezi
Gebäude|n das Gebäude|building||bina; yapı
Kirche|n die Kirchen|church||kilise
Museum|n das Museen|museum||müze
Theater|n das Theater|theatre||tiyatro
Kino|n das Kinos|cinema||sinema
Bibliothek|n die Bibliotheken|library||kütüphane
Schule|n die Schulen|school||okul
Universität|n die Universitäten|university||üniversite
Bank|n die Banken|bank||banka
Post|n die|post office; mail||postane; posta
Hotel|n das Hotels|hotel||otel
Bahnhof|n der Bahnhöfe|railway station||tren istasyonu; gar
Haltestelle|n die Haltestellen|stop (bus, tram)||durak
Flughafen|n der Flughäfen|airport||havalimanı; havaalanı
U-Bahn|n die U-Bahnen|underground; subway||metro
S-Bahn|n die S-Bahnen|suburban train||banliyö treni
Bus|n der Busse|bus||otobüs
Straßenbahn|n die Straßenbahnen|tram||tramvay
Auto|n das Autos|car||araba; otomobil
Taxi|n das Taxis|taxi||taksi
Zug|n der Züge|train||tren
Flugzeug|n das Flugzeuge|aeroplane||uçak
Schiff|n das Schiffe|ship||gemi
Fahrrad|n das Fahrräder|bicycle||bisiklet
Fahrkarte|n die Fahrkarten|ticket (transport)||bilet (ulaşım)
Ticket|n das Tickets|ticket||bilet
Reisepass|n der Reisepässe|passport||pasaport
Ausweis|n der Ausweise|ID card||kimlik kartı; kimlik
Grenze|n die Grenzen|border||sınır
Reise|n die Reisen|journey; trip||seyahat; yolculuk
Ausflug|n der Ausflüge|excursion; outing||gezi; gezinti
Tourist|n der Touristen|tourist||turist
Stadtplan|n der Stadtpläne|city map||şehir planı; şehir haritası
Adresse|n die Adressen|address||adres
Ampel|n die Ampeln|traffic light||trafik ışığı
Kreuzung|n die Kreuzungen|crossroads||kavşak
Ecke|n die Ecken|corner||köşe
Parkplatz|n der Parkplätze|parking space; car park||park yeri; otopark
Tankstelle|n die Tankstellen|petrol station||benzin istasyonu
Stau|n der Staus|traffic jam||trafik sıkışıklığı
Fahrplan|n der Fahrpläne|timetable||tarife; sefer çizelgesi
Abfahrt|n die Abfahrten|departure||kalkış; hareket
Ankunft|n die Ankünfte|arrival||varış
Gleis|n das Gleise|platform; track||peron; ray
Eingang|n der Eingänge|entrance||giriş
Ausgang|n der Ausgänge|exit||çıkış
rechts|adv|right; on the right||sağ; sağda
links|adv|left; on the left||sol; solda
geradeaus|adv|straight ahead||dosdoğru; düz ileri
weit|adj|far; wide||uzak; geniş
nah|adj|near||yakın
hier|adv|here||burada
dort|adv|there||orada
da|adv|there; then||orada; o zaman
dorthin|adv|to there||oraya
hierher|adv|to here||buraya
zu Hause|phr|at home||evde
nach Hause|phr|(to) home||eve
oben|adv|above; upstairs||yukarıda; üst katta
unten|adv|below; downstairs||aşağıda; alt katta
drinnen|adv|inside||içeride
draußen|adv|outside||dışarıda
überall|adv|everywhere||her yerde
nirgends|adv|nowhere||hiçbir yerde
# ---- movement verbs ----
gehen|v|to go; to walk|ging, ist gegangen|gitmek; yürümek
kommen|v|to come|kam, ist gekommen|gelmek
fahren|v|to drive; to go (by vehicle)|fuhr, ist gefahren|araba sürmek; araçla gitmek
laufen|v|to run; to walk|lief, ist gelaufen|koşmak; yürümek
rennen|v|to run|rannte, ist gerannt|koşmak
fliegen|v|to fly|flog, ist geflogen|uçmak
schwimmen|v|to swim|schwamm, ist geschwommen|yüzmek
reisen|v|to travel||seyahat etmek
ankommen|v|to arrive|kam an, ist angekommen|varmak; gelmek
abfahren|v|to depart|fuhr ab, ist abgefahren|hareket etmek; yola çıkmak
abfliegen|v|to take off (plane)|flog ab, ist abgeflogen|havalanmak; kalkmak (uçak)
einsteigen|v|to get in; to board|stieg ein, ist eingestiegen|binmek
aussteigen|v|to get off; to get out|stieg aus, ist ausgestiegen|inmek
umsteigen|v|to change (trains)|stieg um, ist umgestiegen|aktarma yapmak
zurückkommen|v|to come back|kam zurück, ist zurückgekommen|geri gelmek
weggehen|v|to go away|ging weg, ist weggegangen|gitmek; uzaklaşmak
hereinkommen|v|to come in|kam herein, ist hereingekommen|içeri gelmek
hinausgehen|v|to go out|ging hinaus, ist hinausgegangen|dışarı çıkmak
bringen|v|to bring|brachte, gebracht|getirmek
holen|v|to fetch; to get||getirmek; alıp gelmek
abholen|v|to pick up||almaya gitmek; karşılamak
mitnehmen|v|to take along|nahm mit, mitgenommen|yanına almak; beraberinde götürmek
folgen|v|to follow||takip etmek; izlemek
springen|v|to jump|sprang, ist gesprungen|atlamak; zıplamak
fallen|v|to fall|fiel, ist gefallen|düşmek
steigen|v|to climb; to rise|stieg, ist gestiegen|tırmanmak; yükselmek
# ---- core verbs ----
sein|v|to be|war, ist gewesen|olmak
haben|v|to have|hatte, gehabt|sahip olmak
werden|v|to become; will|wurde, ist geworden|olmak; -ecek (gelecek zaman)
machen|v|to do; to make||yapmak
tun|v|to do|tat, getan|yapmak; etmek
sagen|v|to say||söylemek; demek
sprechen|v|to speak|sprach, gesprochen|konuşmak
reden|v|to talk||konuşmak; sohbet etmek
erzählen|v|to tell; to narrate||anlatmak
fragen|v|to ask||sormak
antworten|v|to answer||cevap vermek; yanıtlamak
bitten|v|to ask for; to request|bat, gebeten|rica etmek; istemek
wissen|v|to know (facts)|wusste, gewusst|bilmek
kennen|v|to know (be familiar with)|kannte, gekannt|tanımak; bilmek
kennenlernen|v|to get to know; to meet||tanışmak; tanımak
denken|v|to think|dachte, gedacht|düşünmek
glauben|v|to believe; to think||inanmak; sanmak
meinen|v|to mean; to think (opinion)||demek istemek; düşünmek (görüş)
verstehen|v|to understand|verstand, verstanden|anlamak
wollen|v|to want|wollte, gewollt|istemek
möchten|v|would like||istemek (kibarca)
können|v|can; to be able|konnte, gekonnt|-ebilmek; yapabilmek
müssen|v|must; to have to|musste, gemusst|zorunda olmak; -meli
sollen|v|should; to be supposed to||-meli; gerekmek
dürfen|v|may; to be allowed|durfte, gedurft|izinli olmak; -ebilmek (izin)
mögen|v|to like|mochte, gemocht|sevmek; hoşlanmak
lieben|v|to love||sevmek; âşık olmak
gefallen|v|to please; to be liked|gefiel, gefallen|hoşuna gitmek; beğenilmek
hassen|v|to hate||nefret etmek
sehen|v|to see|sah, gesehen|görmek
schauen|v|to look||bakmak
ansehen|v|to look at; to watch|sah an, angesehen|bakmak; seyretmek
hören|v|to hear; to listen||duymak; dinlemek
zuhören|v|to listen (to)||dinlemek
lesen|v|to read|las, gelesen|okumak
schreiben|v|to write|schrieb, geschrieben|yazmak
lernen|v|to learn; to study||öğrenmek; ders çalışmak
studieren|v|to study (at university)||üniversitede okumak
lehren|v|to teach||öğretmek
unterrichten|v|to teach; to instruct||ders vermek; öğretmek
üben|v|to practise||alıştırma yapmak; pratik yapmak
arbeiten|v|to work||çalışmak
leben|v|to live||yaşamak
spielen|v|to play||oynamak; çalmak (müzik)
geben|v|to give|gab, gegeben|vermek
nehmen|v|to take|nahm, genommen|almak
bekommen|v|to get; to receive|bekam, bekommen|almak; edinmek
kaufen|v|to buy||satın almak
verkaufen|v|to sell||satmak
einkaufen|v|to shop; to go shopping||alışveriş yapmak
kosten|v|to cost||mal olmak; fiyatı olmak
zahlen|v|to pay||ödemek
öffnen|v|to open||açmak
aufmachen|v|to open (colloquial)||açmak
schließen|v|to close|schloss, geschlossen|kapatmak
zumachen|v|to close (colloquial)||kapatmak
anfangen|v|to begin|fing an, angefangen|başlamak
beginnen|v|to begin|begann, begonnen|başlamak
aufhören|v|to stop; to cease||durmak; bırakmak
beenden|v|to finish; to end||bitirmek; sona erdirmek
weitermachen|v|to continue||devam etmek
warten|v|to wait||beklemek
suchen|v|to look for||aramak
finden|v|to find|fand, gefunden|bulmak
verlieren|v|to lose|verlor, verloren|kaybetmek
sich erinnern|v|to remember||hatırlamak
vergessen|v|to forget|vergaß, vergessen|unutmak
helfen|v|to help|half, geholfen|yardım etmek
anrufen|v|to call (phone)|rief an, angerufen|telefon etmek; aramak
treffen|v|to meet|traf, getroffen|buluşmak; karşılaşmak
sich treffen|v|to meet (each other)||buluşmak
zeigen|v|to show||göstermek
erklären|v|to explain||açıklamak
übersetzen|v|to translate||çevirmek; tercüme etmek
wiederholen|v|to repeat||tekrarlamak
schicken|v|to send||göndermek
senden|v|to send|sandte, gesandt|göndermek; yollamak
legen|v|to lay; to put (flat)||koymak (yatay); yatırmak
stellen|v|to put (upright); to place||koymak (dik); yerleştirmek
setzen|v|to set; to put||oturtmak; koymak
sich setzen|v|to sit down||oturmak
sitzen|v|to sit|saß, gesessen|oturmak
stehen|v|to stand|stand, gestanden|ayakta durmak; durmak
liegen|v|to lie (be lying)|lag, gelegen|yatmak; bulunmak
hängen|v|to hang|hing, gehangen|asmak; asılı olmak
halten|v|to hold; to stop|hielt, gehalten|tutmak; durmak
sich fühlen|v|to feel||hissetmek (kendini)
fühlen|v|to feel||hissetmek
fürchten|v|to fear||korkmak
hoffen|v|to hope||ummak; umut etmek
entscheiden|v|to decide|entschied, entschieden|karar vermek
sich entscheiden|v|to decide; to make up one's mind||karar vermek
lösen|v|to solve||çözmek
probieren|v|to try; to taste||denemek; tatmak
versuchen|v|to try; to attempt||denemek; çalışmak
träumen|v|to dream||rüya görmek; hayal kurmak
lachen|v|to laugh||gülmek
lächeln|v|to smile||gülümsemek
weinen|v|to cry||ağlamak
schreien|v|to shout; to scream|schrie, geschrien|bağırmak; çığlık atmak
singen|v|to sing|sang, gesungen|şarkı söylemek
tanzen|v|to dance||dans etmek
malen|v|to paint||resim yapmak; boyamak
zeichnen|v|to draw||çizmek
spazieren gehen|phr|to go for a walk||yürüyüşe çıkmak
wandern|v|to hike||doğa yürüyüşü yapmak
sich interessieren|v|to be interested (in)||ilgilenmek; ilgi duymak
heißen|v|to be called|hieß, geheißen|adı olmak; denmek
nennen|v|to call; to name|nannte, genannt|adlandırmak; demek
heiraten|v|to marry||evlenmek
geboren werden|phr|to be born||doğmak
sterben|v|to die|starb, ist gestorben|ölmek
wachsen|v|to grow|wuchs, ist gewachsen|büyümek
ändern|v|to change; to alter||değiştirmek
sich ändern|v|to change (oneself)||değişmek
wechseln|v|to change; to exchange||değiştirmek; bozdurmak
bauen|v|to build||inşa etmek; yapmak
kaputtgehen|v|to break (down)|ging kaputt, ist kaputtgegangen|bozulmak; kırılmak
reparieren|v|to repair||tamir etmek; onarmak
werfen|v|to throw|warf, geworfen|atmak; fırlatmak
heben|v|to lift|hob, gehoben|kaldırmak
bewegen|v|to move (something)||hareket ettirmek; kımıldatmak
aufhalten|v|to stop; to hold up|hielt auf, aufgehalten|durdurmak; alıkoymak
sich verspäten|v|to be late||gecikmek; geç kalmak
sich beeilen|v|to hurry||acele etmek
schaffen|v|to manage; to create|schuf, geschaffen|başarmak; yaratmak
einladen|v|to invite|lud ein, eingeladen|davet etmek
vorschlagen|v|to suggest|schlug vor, vorgeschlagen|önermek; teklif etmek
empfehlen|v|to recommend|empfahl, empfohlen|tavsiye etmek; önermek
raten|v|to advise; to guess|riet, geraten|tavsiye etmek; tahmin etmek
versprechen|v|to promise|versprach, versprochen|söz vermek
erlauben|v|to allow||izin vermek
verbieten|v|to forbid|verbot, verboten|yasaklamak
prüfen|v|to check; to test||kontrol etmek; sınamak
überprüfen|v|to verify; to check||doğrulamak; gözden geçirmek
wählen|v|to choose; to elect; to dial||seçmek; oy vermek; (numara) çevirmek
vergleichen|v|to compare|verglich, verglichen|karşılaştırmak
zählen|v|to count||saymak
rechnen|v|to calculate||hesaplamak
benutzen|v|to use||kullanmak
verwenden|v|to use; to apply||kullanmak; uygulamak
brauchen|v|to need||ihtiyaç duymak; gerekmek
planen|v|to plan||planlamak
organisieren|v|to organise||düzenlemek; organize etmek
teilnehmen|v|to take part|nahm teil, teilgenommen|katılmak
gewinnen|v|to win|gewann, gewonnen|kazanmak
passieren|v|to happen|passierte, ist passiert|olmak; meydana gelmek
geschehen|v|to happen|geschah, ist geschehen|olmak; gerçekleşmek
scheinen|v|to seem; to shine|schien, geschienen|görünmek; parlamak
bedeuten|v|to mean||anlamına gelmek
existieren|v|to exist||var olmak
reichen|v|to be enough; to pass||yetmek; uzatmak
genügen|v|to suffice||yetmek; yeterli olmak
gehören|v|to belong||ait olmak
bleiben|v|to stay; to remain|blieb, ist geblieben|kalmak
lassen|v|to let; to leave|ließ, gelassen|bırakmak; izin vermek
verlassen|v|to leave (a place)|verließ, verlassen|terk etmek; ayrılmak
besuchen|v|to visit||ziyaret etmek
begrüßen|v|to greet||selamlamak; karşılamak
sich verabschieden|v|to say goodbye||vedalaşmak
danken|v|to thank||teşekkür etmek
sich entschuldigen|v|to apologise||özür dilemek
sich freuen|v|to be glad; to look forward||sevinmek; dört gözle beklemek
sich ärgern|v|to be annoyed||kızmak; sinirlenmek
sich sorgen|v|to worry||endişelenmek
sich beschweren|v|to complain||şikâyet etmek
streiten|v|to argue|stritt, gestritten|tartışmak; kavga etmek
diskutieren|v|to discuss||tartışmak
zustimmen|v|to agree||kabul etmek; onaylamak
ablehnen|v|to refuse; to reject||reddetmek
aufpassen|v|to pay attention; to watch out||dikkat etmek
merken|v|to notice; to remember||fark etmek; aklında tutmak
bemerken|v|to notice||fark etmek
beschreiben|v|to describe|beschrieb, beschrieben|tarif etmek; betimlemek
sich vorstellen|v|to introduce oneself; to imagine||kendini tanıtmak; hayal etmek
abhängen|v|to depend|hing ab, abgehangen|bağlı olmak
beeinflussen|v|to influence||etkilemek
sich unterscheiden|v|to differ|unterschied, unterschieden|farklı olmak; ayrılmak
entwickeln|v|to develop||geliştirmek
schützen|v|to protect||korumak
zerstören|v|to destroy||yok etmek; tahrip etmek
sparen|v|to save (money)||biriktirmek; tasarruf etmek
ausgeben|v|to spend (money)|gab aus, ausgegeben|harcamak
verdienen|v|to earn; to deserve||kazanmak; hak etmek
kündigen|v|to quit; to give notice||istifa etmek; feshetmek
leiten|v|to lead; to manage||yönetmek
rauchen|v|to smoke||sigara içmek
abnehmen|v|to lose weight; to decrease|nahm ab, abgenommen|zayıflamak; azalmak
zunehmen|v|to gain weight; to increase|nahm zu, zugenommen|kilo almak; artmak
heilen|v|to heal; to cure||iyileştirmek; iyileşmek
behandeln|v|to treat||tedavi etmek; muamele etmek
# ---- adjectives ----
groß|adj|big; tall||büyük; uzun boylu
klein|adj|small; little||küçük
gut|adj|good||iyi
schlecht|adj|bad||kötü
neu|adj|new||yeni
alt|adj|old||eski; yaşlı
jung|adj|young||genç
schön|adj|beautiful; nice||güzel
hässlich|adj|ugly||çirkin
klug|adj|clever||akıllı; zeki
dumm|adj|stupid||aptal
nett|adj|nice; kind||nazik; hoş
freundlich|adj|friendly||güler yüzlü; dostça
böse|adj|angry; evil||kızgın; kötü
lustig|adj|funny||komik; eğlenceli
traurig|adj|sad||üzgün
glücklich|adj|happy; lucky||mutlu; şanslı
zufrieden|adj|satisfied; content||memnun
interessant|adj|interesting||ilginç
langweilig|adj|boring||sıkıcı
wichtig|adj|important||önemli
schwierig|adj|difficult||zor
schwer|adj|heavy; difficult||ağır; zor
leicht|adj|light; easy||hafif; kolay
einfach|adj|simple; easy||basit; kolay
kompliziert|adj|complicated||karmaşık
teuer|adj|expensive||pahalı
billig|adj|cheap||ucuz
günstig|adj|inexpensive; favourable||uygun fiyatlı; elverişli
reich|adj|rich||zengin
arm|adj|poor||fakir; yoksul
stark|adj|strong||güçlü
schwach|adj|weak||zayıf; güçsüz
hoch|adj|high; tall||yüksek
niedrig|adj|low||alçak; düşük
lang|adj|long||uzun
kurz|adj|short||kısa
breit|adj|wide||geniş
schmal|adj|narrow||dar
eng|adj|tight; narrow||dar; sıkı
dick|adj|thick; fat||kalın; şişman
dünn|adj|thin||ince; zayıf
heiß|adj|hot||sıcak
warm|adj|warm||ılık; sıcak
kalt|adj|cold||soğuk
kühl|adj|cool||serin
schnell|adj|fast||hızlı
langsam|adj|slow||yavaş
laut|adj|loud||gürültülü; yüksek sesli
leise|adj|quiet||sessiz; alçak sesli
sauber|adj|clean||temiz
schmutzig|adj|dirty||kirli
hell|adj|bright; light||aydınlık; açık (renk)
dunkel|adj|dark||karanlık; koyu
voll|adj|full||dolu
leer|adj|empty||boş
offen|adj|open||açık
geschlossen|adj|closed||kapalı
frei|adj|free; vacant||özgür; boş
beschäftigt|adj|busy||meşgul
fertig|adj|ready; finished||hazır; bitmiş
richtig|adj|correct; right||doğru
falsch|adj|wrong; false||yanlış; sahte
echt|adj|real; genuine||gerçek; hakiki
möglich|adj|possible||mümkün
unmöglich|adj|impossible||imkânsız
nötig|adj|necessary||gerekli
gleich|adj|same; equal||aynı; eşit
anders|adj|different||farklı; başka türlü
ähnlich|adj|similar||benzer
verschieden|adj|different; various||farklı; çeşitli
nächste|adj|next||gelecek; sonraki
vorige|adj|previous||önceki; geçen
eigen|adj|own||kendi; öz
persönlich|adj|personal||kişisel
bequem|adj|comfortable||rahat
gefährlich|adj|dangerous||tehlikeli
sicher|adj|safe; sure; certain||güvenli; emin; kesin
ehrlich|adj|honest||dürüst
höflich|adj|polite||kibar; nazik
ernst|adj|serious||ciddi
nass|adj|wet||ıslak
trocken|adj|dry||kuru
weich|adj|soft||yumuşak
hart|adj|hard||sert
rund|adj|round||yuvarlak
lebendig|adj|alive; lively||canlı
tot|adj|dead||ölü
berühmt|adj|famous||ünlü
beliebt|adj|popular||popüler; sevilen
modern|adj|modern||modern
bekannt|adj|known; well-known||tanınmış; bilinen
fremd|adj|foreign; strange||yabancı
deutsch|adj|German||Almanca; Alman
englisch|adj|English||İngilizce; İngiliz
türkisch|adj|Turkish||Türkçe; Türk
französisch|adj|French||Fransızca; Fransız
russisch|adj|Russian||Rusça; Rus
fleißig|adj|hard-working||çalışkan
faul|adj|lazy||tembel
ruhig|adj|calm; quiet||sakin; sessiz
nervös|adj|nervous||gergin; sinirli
verrückt|adj|crazy||deli; çılgın
allein|adj|alone||yalnız
zusammen|adv|together||birlikte; beraber
ganz|adj|whole; entire; quite||bütün; tamamen; oldukça
# ---- colours ----
Farbe|n die Farben|colour||renk
weiß|adj|white||beyaz
schwarz|adj|black||siyah
rot|adj|red||kırmızı
blau|adj|blue||mavi
grün|adj|green||yeşil
gelb|adj|yellow||sarı
orange|adj|orange||turuncu
braun|adj|brown||kahverengi
grau|adj|grey||gri
rosa|adj|pink||pembe
lila|adj|purple||mor
bunt|adj|colourful||rengarenk
# ---- adverbs / particles / prepositions / conjunctions ----
sehr|adv|very||çok
zu|adv|too (excessively)||fazla; aşırı
fast|adv|almost||neredeyse
nur|adv|only||sadece; yalnızca
auch|adv|also; too||de/da; ayrıca
ebenfalls|adv|likewise; also||aynı şekilde; de/da
sogar|adv|even||hatta; bile
etwa|adv|approximately; perhaps||yaklaşık; belki
ungefähr|adv|approximately||yaklaşık; aşağı yukarı
genau|adv|exactly||tam olarak; tam
wirklich|adv|really||gerçekten
natürlich|adv|of course; naturally||tabii; elbette
vielleicht|adv|maybe; perhaps||belki
wahrscheinlich|adv|probably||muhtemelen
bestimmt|adv|certainly||kesinlikle; mutlaka
leider|adv|unfortunately||maalesef; ne yazık ki
hoffentlich|adv|hopefully||umarım; inşallah
besonders|adv|especially||özellikle
ziemlich|adv|rather; quite||oldukça; epey
gar nicht|phr|not at all||hiç; asla
überhaupt|adv|at all; generally||hiç; genel olarak
eigentlich|adv|actually||aslında
übrigens|adv|by the way||bu arada; aklıma gelmişken
also|adv|so; therefore||yani; o halde; demek ki
deshalb|adv|therefore||bu yüzden; bundan dolayı
trotzdem|adv|nevertheless||yine de; buna rağmen
sonst|adv|otherwise||yoksa; aksi halde
außerdem|adv|besides; moreover||ayrıca; üstelik
jedoch|adv|however||ancak; fakat
nämlich|adv|namely; you see||yani; çünkü
mal|part|once; just (softening particle)||bir (kere); hele
nicht|part|not||değil; -me/-ma
und|conj|and||ve
oder|conj|or||veya; ya da
aber|conj|but||ama; fakat
sondern|conj|but rather||aksine; bilakis
denn|conj|because; for||çünkü; zira
weil|conj|because||çünkü
dass|conj|that||-diği; ki
ob|conj|whether; if||-ip -mediği; acaba
wenn|conj|if; when||eğer; -ince; -diğinde
als|conj|when (past); than; as||-diğinde; -den daha; olarak
obwohl|conj|although||-e rağmen; her ne kadar
damit|conj|so that||-mesi için; diye
bevor|conj|before||-meden önce
nachdem|conj|after||-dikten sonra
während|conj|while; during||-iken; sırasında
seit|prep|since; for (time)||-den beri
bis|prep|until||-e kadar
in|prep|in; into||-de/-da; içinde
an|prep|at; on||-de/-da; yanında
auf|prep|on; onto||üstünde; üzerine
unter|prep|under; among||altında; arasında
über|prep|over; above; about||üzerinde; hakkında
vor|prep|in front of; before; ago||önünde; önce
hinter|prep|behind||arkasında
neben|prep|next to||yanında
zwischen|prep|between||arasında
mit|prep|with||ile
ohne|prep|without||-sız/-siz; olmadan
für|prep|for||için
gegen|prep|against; around (time)||karşı; -e doğru (saat)
um|prep|around; at (time)||etrafında; -de (saat)
durch|prep|through||-den geçerek; aracılığıyla
nach|prep|after; to (a place)||sonra; -e (yer)
aus|prep|out of; from||-den; dışarı
bei|prep|at; near; with||-de/-da; yanında
von|prep|from; of||-den; -in
zu|prep|to; at||-e/-a
außer|prep|except||hariç; dışında
wegen|prep|because of||yüzünden; nedeniyle
trotz|prep|despite||-e rağmen
statt|prep|instead of||yerine
entlang|prep|along||boyunca
gegenüber|prep|opposite||karşısında
# ---- education / language ----
Sprache|n die Sprachen|language||dil
Wort|n das Wörter|word||kelime; sözcük
Satz|n der Sätze|sentence||cümle
Buchstabe|n der Buchstaben|letter (alphabet)||harf
Alphabet|n das Alphabete|alphabet||alfabe
Grammatik|n die Grammatiken|grammar||dil bilgisi; gramer
Wörterbuch|n das Wörterbücher|dictionary||sözlük
Wortschatz|n der|vocabulary||kelime hazinesi; söz varlığı
Unterricht|n der|lessons; teaching||ders; öğretim
Klasse|n die Klassen|class||sınıf
Kurs|n der Kurse|course||kurs
Prüfung|n die Prüfungen|exam||sınav
Test|n der Tests|test||test
Note|n die Noten|grade; mark; note (music)||not (okul); nota (müzik)
Fehler|n der Fehler|mistake||hata
Frage|n die Fragen|question||soru
Antwort|n die Antworten|answer||cevap; yanıt
Regel|n die Regeln|rule||kural
Beispiel|n das Beispiele|example||örnek
Aufgabe|n die Aufgaben|task; exercise||görev; alıştırma
Hausaufgabe|n die Hausaufgaben|homework||ev ödevi
Übung|n die Übungen|exercise; practice||alıştırma; egzersiz
Text|n der Texte|text||metin
Geschichte|n die Geschichten|story; history||hikâye; tarih
Literatur|n die|literature||edebiyat
Mathematik|n die|mathematics||matematik
Physik|n die|physics||fizik
Chemie|n die|chemistry||kimya
Biologie|n die|biology||biyoloji
Erdkunde|n die|geography||coğrafya
Wissenschaft|n die Wissenschaften|science||bilim
Bedeutung|n die Bedeutungen|meaning; importance||anlam; önem
Übersetzung|n die Übersetzungen|translation||çeviri
Aussprache|n die|pronunciation||telaffuz
Erinnerung|n die Erinnerungen|memory; reminder||anı; hatırlatma
Aufmerksamkeit|n die|attention||dikkat
Kenntnis|n die Kenntnisse|knowledge||bilgi
Erfahrung|n die Erfahrungen|experience||deneyim; tecrübe
Tafel|n die Tafeln|blackboard; bar (of chocolate)||yazı tahtası; tablet (çikolata)
Pause|n die Pausen|break||ara; teneffüs
Zeugnis|n das Zeugnisse|school report; certificate||karne; belge
Ausbildung|n die Ausbildungen|training; education||eğitim; meslek eğitimi
# ---- money / shopping ----
Preis|n der Preise|price; prize||fiyat; ödül
Euro|n der Euro|euro||avro
Cent|n der Cent|cent||sent
Kasse|n die Kassen|cash desk; checkout||kasa
Kleingeld|n das|small change||bozuk para
Wechselgeld|n das|change (money)||para üstü
Rabatt|n der Rabatte|discount||indirim
Angebot|n das Angebote|offer||teklif; kampanya
kostenlos|adj|free of charge||ücretsiz
Geschäft|n das Geschäfte|shop; business||dükkân; iş
Laden|n der Läden|shop||dükkân
Supermarkt|n der Supermärkte|supermarket||süpermarket
Markt|n der Märkte|market||pazar; market
Einkaufszentrum|n das Einkaufszentren|shopping centre||alışveriş merkezi
Kaufhaus|n das Kaufhäuser|department store||büyük mağaza
Ware|n die Waren|goods||mal; ürün
Produkt|n das Produkte|product||ürün
Qualität|n die Qualitäten|quality||kalite
Kreditkarte|n die Kreditkarten|credit card||kredi kartı
Konto|n das Konten|account||hesap
Schulden|n die|debts||borçlar
Steuer|n die Steuern|tax||vergi
Versicherung|n die Versicherungen|insurance||sigorta
# ---- communication / technology ----
Internet|n das|internet||internet
Webseite|n die Webseiten|website||web sitesi
E-Mail|n die E-Mails|e-mail||e-posta
Nachricht|n die Nachrichten|message; news item||mesaj; haber
Nachrichten|n die|the news||haberler
Nummer|n die Nummern|number||numara
Anruf|n der Anrufe|phone call||telefon araması
Verbindung|n die Verbindungen|connection||bağlantı
Information|n die Informationen|information||bilgi
Programm|n das Programme|programme; program||program
App|n die Apps|app||uygulama
Bildschirm|n der Bildschirme|screen||ekran
Taste|n die Tasten|key (keyboard)||tuş
Tastatur|n die Tastaturen|keyboard||klavye
Maus|n die Mäuse|mouse||fare
Datei|n die Dateien|file||dosya
Ordner|n der Ordner|folder||klasör
Passwort|n das Passwörter|password||şifre; parola
Drucker|n der Drucker|printer||yazıcı
Radio|n das Radios|radio||radyo
Musik|n die|music||müzik
Lied|n das Lieder|song||şarkı
Film|n der Filme|film; movie||film
Serie|n die Serien|TV series||dizi
Spiel|n das Spiele|game; match||oyun; maç
Kamera|n die Kameras|camera||kamera
Akku|n der Akkus|rechargeable battery||şarj edilebilir pil; batarya
Batterie|n die Batterien|battery||pil
aufladen|v|to charge|lud auf, aufgeladen|şarj etmek
einschalten|v|to switch on||açmak (cihaz)
ausschalten|v|to switch off||kapatmak (cihaz)
herunterladen|v|to download|lud herunter, heruntergeladen|indirmek
drucken|v|to print||yazdırmak
speichern|v|to save (file)||kaydetmek
löschen|v|to delete||silmek
# ---- nature / weather ----
Natur|n die|nature||doğa
Wetter|n das|weather||hava (durumu)
Sonne|n die Sonnen|sun||güneş
Mond|n der Monde|moon||ay
Stern|n der Sterne|star||yıldız
Himmel|n der Himmel|sky; heaven||gökyüzü; cennet
Wolke|n die Wolken|cloud||bulut
Regen|n der|rain||yağmur
Schnee|n der|snow||kar
Wind|n der Winde|wind||rüzgâr
Gewitter|n das Gewitter|thunderstorm||fırtına; gök gürültülü fırtına
Nebel|n der|fog||sis
Frost|n der|frost||don
Hitze|n die|heat||sıcaklık; sıcak
Grad|n der Grade|degree||derece
Erde|n die|earth; soil||dünya; toprak
Welt|n die Welten|world||dünya
Luft|n die|air||hava
Feuer|n das Feuer|fire||ateş
Meer|n das Meere|sea||deniz
See|n der Seen|lake||göl
Fluss|n der Flüsse|river||nehir; ırmak
Ufer|n das Ufer|shore; bank||kıyı; sahil
Insel|n die Inseln|island||ada
Berg|n der Berge|mountain||dağ
Wald|n der Wälder|forest||orman
Feld|n das Felder|field||tarla; alan
Baum|n der Bäume|tree||ağaç
Blume|n die Blumen|flower||çiçek
Gras|n das|grass||çim; ot
Blatt|n das Blätter|leaf; sheet||yaprak; sayfa
Stein|n der Steine|stone||taş
Sand|n der|sand||kum
Tier|n das Tiere|animal||hayvan
Hund|n der Hunde|dog||köpek
Katze|n die Katzen|cat||kedi
Pferd|n das Pferde|horse||at
Kuh|n die Kühe|cow||inek
Schwein|n das Schweine|pig||domuz
Vogel|n der Vögel|bird||kuş
Bär|n der Bären|bear||ayı
Wolf|n der Wölfe|wolf||kurt
Fuchs|n der Füchse|fox||tilki
Hase|n der Hasen|hare||tavşan
Schlange|n die Schlangen|snake; queue||yılan; kuyruk (sıra)
Insekt|n das Insekten|insect||böcek
Es regnet|phr|it is raining||yağmur yağıyor
Es schneit|phr|it is snowing||kar yağıyor
Es ist kalt|phr|it is cold||hava soğuk
Es ist heiß|phr|it is hot||hava sıcak
sonnig|adj|sunny||güneşli
bewölkt|adj|cloudy||bulutlu
windig|adj|windy||rüzgârlı
# ---- sport / leisure ----
Sport|n der|sport||spor
Fußball|n der|football; soccer||futbol
Handball|n der|handball||hentbol
Tennis|n das|tennis||tenis
Schach|n das|chess||satranç
Schwimmbad|n das Schwimmbäder|swimming pool||yüzme havuzu
Stadion|n das Stadien|stadium||stadyum
Mannschaft|n die Mannschaften|team||takım
Training|n das|training||antrenman
Sieg|n der Siege|victory||zafer; galibiyet
Hobby|n das Hobbys|hobby||hobi
Freizeit|n die|free time; leisure||boş zaman
Konzert|n das Konzerte|concert||konser
Ausstellung|n die Ausstellungen|exhibition||sergi
Party|n die Partys|party||parti
Fest|n das Feste|celebration; festival||kutlama; bayram
feiern|v|to celebrate||kutlamak
Verein|n der Vereine|club; association||dernek; kulüp
# ---- feelings / abstract ----
Leben|n das Leben|life||hayat; yaşam
Tod|n der|death||ölüm
Liebe|n die|love||aşk; sevgi
Freundschaft|n die Freundschaften|friendship||arkadaşlık; dostluk
Glück|n das|happiness; luck||mutluluk; şans
Freude|n die|joy||sevinç; neşe
Angst|n die Ängste|fear; anxiety||korku; kaygı
Hoffnung|n die Hoffnungen|hope||umut
Traum|n der Träume|dream||rüya; hayal
Wahrheit|n die Wahrheiten|truth||gerçek; hakikat
Lüge|n die Lügen|lie||yalan
Gedanke|n der Gedanken|thought||düşünce
Idee|n die Ideen|idea||fikir
Meinung|n die Meinungen|opinion||görüş; kanaat
Gefühl|n das Gefühle|feeling||duygu; his
Laune|n die Launen|mood||ruh hali; keyif
Wunsch|n der Wünsche|wish||dilek; istek
Interesse|n das Interessen|interest||ilgi; çıkar
Freiheit|n die|freedom||özgürlük
Recht|n das Rechte|right; law||hak; hukuk
Gesetz|n das Gesetze|law||kanun; yasa
Ordnung|n die|order||düzen
Wahl|n die Wahlen|choice; election||seçim
Möglichkeit|n die Möglichkeiten|possibility; opportunity||olanak; imkân; fırsat
Grund|n der Gründe|reason; ground||sebep; neden; zemin
Folge|n die Folgen|consequence; episode||sonuç; bölüm (dizi)
Fall|n der Fälle|case; fall||durum; olay; düşüş
Art|n die Arten|kind; type; way||tür; çeşit; tarz
Weise|n die Weisen|manner; way||biçim; tarz; şekil
Bedingung|n die Bedingungen|condition||koşul; şart
Unterschied|n der Unterschiede|difference||fark
Teil|n der Teile|part||parça; bölüm
Ende|n das Enden|end||son
Anfang|n der Anfänge|beginning||başlangıç
Mitte|n die|middle||orta
Ort|n der Orte|place; location||yer; mekân
Seite|n die Seiten|side; page||taraf; sayfa
Form|n die Formen|form; shape||biçim; şekil; form
Zahl|n die Zahlen|number||sayı
Menge|n die Mengen|amount; quantity; crowd||miktar; kalabalık
Gewicht|n das Gewichte|weight||ağırlık
Gesellschaft|n die Gesellschaften|society; company||toplum; şirket
Staat|n der Staaten|state (country)||devlet
Regierung|n die Regierungen|government||hükümet
Volk|n das Völker|people; nation||halk; millet
Krieg|n der Kriege|war||savaş
Frieden|n der|peace||barış
Polizei|n die|police||polis
Kultur|n die Kulturen|culture||kültür
Kunst|n die Künste|art||sanat
Religion|n die Religionen|religion||din
Problem|n das Probleme|problem||sorun; problem
Lösung|n die Lösungen|solution||çözüm
Erfolg|n der Erfolge|success||başarı
Ziel|n das Ziele|goal; destination||hedef; amaç; varış yeri
Plan|n der Pläne|plan||plan
Ergebnis|n das Ergebnisse|result||sonuç
Projekt|n das Projekte|project||proje
Umwelt|n die|environment||çevre
Zukunft|n die|future||gelecek
Vergangenheit|n die|past||geçmiş
Gegenwart|n die|present||şimdiki zaman; bugün
Ereignis|n das Ereignisse|event||olay
Situation|n die Situationen|situation||durum
Beziehung|n die Beziehungen|relationship||ilişki
Verantwortung|n die|responsibility||sorumluluk
Sicherheit|n die|safety; security||güvenlik; emniyet
"""
