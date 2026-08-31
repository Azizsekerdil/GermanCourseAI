"""German-specific orthography, pronunciation, grammar and open resources."""
from __future__ import annotations

import random

ORTHOGRAPHY = [
    ("A–Z", "Deutsches Alphabet", "Buchstaben werden in Eigennamen und beim Buchstabieren einzeln gesprochen.", "Anna buchstabiert A-N-N-A."),
    ("Ä ä", "Umlaut A", "Ä ist ein eigener Laut; in Ersatzschreibungen ist ae möglich.", "Mädchen · Bär · Käse"),
    ("Ö ö", "Umlaut O", "Die Lippen sind gerundet, die Zunge bleibt vorn.", "Öl · schön · zwölf"),
    ("Ü ü", "Umlaut U", "Wie i sprechen, dabei die Lippen runden.", "Tür · fünf · müde"),
    ("ß", "Eszett", "Nach langem Vokal oder Diphthong steht oft ß; nach kurzem Vokal ss.", "Straße · Fuß / Kasse · müssen"),
    ("Nomen", "Großschreibung", "Alle Nomen beginnen mit einem Großbuchstaben.", "das Haus · die Sprache · der Zug"),
    ("Vokal", "Lang oder kurz", "Ein Doppelkonsonant signalisiert meist einen kurzen Vokal; h kann Länge zeigen.", "Ofen / offen · wohnen"),
    ("ch", "Ich- und Ach-Laut", "Nach e, i, ä, ö, ü ist ch weich; nach a, o, u rauer.", "ich · Bücher / Bach · Buch"),
    ("sch", "Sch-Laut", "sch entspricht meist [ʃ].", "Schule · schreiben"),
    ("sp/st", "Silbenanfang", "Am Wort- oder Silbenanfang klingen sp und st oft wie schp und scht.", "Spiel · Straße"),
    ("z", "Ts-Laut", "z wird [ts] gesprochen.", "Zeit · zehn"),
    ("w/v", "W und V", "w klingt [v]; v klingt je nach Wort [f] oder [v].", "Wasser · Vater · Vase"),
    ("j", "J-Laut", "j klingt wie türkisches y oder englisches y in yes.", "ja · Jahr"),
    ("Komposita", "Zusammengesetzte Nomen", "Das letzte Nomen bestimmt Artikel und Kernbedeutung.", "die Haustür · der Bahnhof"),
    ("Betonung", "Silben und Akzent", "Deutsche Stammwörter tragen den Akzent oft auf der ersten Silbe.", "ARbeiten · LEHrerin"),
]

PRONUNCIATION = [
    ("ch nach i/e", "[ç]", "ich, nicht, Bücher"),
    ("ch nach a/o/u", "[x]", "Bach, doch, Buch"),
    ("r", "[ʁ] / [ɐ]", "rot, Lehrer"),
    ("z", "[ts]", "Zeit, Zug"),
    ("sch", "[ʃ]", "Schule, Fisch"),
    ("sp/st am Anfang", "[ʃp] / [ʃt]", "Sport, Straße"),
    ("ei / ie", "[aɪ] / [iː]", "mein, sieben"),
    ("eu / äu", "[ɔʏ]", "heute, Häuser"),
    ("w / j", "[v] / [j]", "Wasser, Jahr"),
]

_TOPIC_ROWS = [
    ("case.nom", "Nominativ", "Nominative", "Nominativ", "Özne ve sözlük biçimi.", "Subject and dictionary form.", "Subjekt und Wörterbuchform.", "Der Mann lernt Deutsch."),
    ("case.acc", "Akkusativ", "Accusative", "Akkusativ", "Doğrudan nesne; eril artikel der → den.", "Direct object; masculine der becomes den.", "Direktes Objekt; der wird zu den.", "Ich sehe den Mann."),
    ("case.dat", "Dativ", "Dative", "Dativ", "Dolaylı nesne ve belirli edatlar.", "Indirect object and selected prepositions.", "Indirektes Objekt und bestimmte Präpositionen.", "Ich helfe dem Kind."),
    ("case.gen", "Genitiv", "Genitive", "Genitiv", "Aidiyet ve resmî yazı dili.", "Possession and formal written usage.", "Besitz und formelle Schriftsprache.", "Das Auto des Lehrers ist neu."),
    ("article.def", "Belirli artikeller", "Definite articles", "Bestimmte Artikel", "der, die, das ve çoğul die.", "der, die, das and plural die.", "der, die, das und Plural die.", "Das Buch liegt auf dem Tisch."),
    ("article.indef", "Belirsiz artikeller", "Indefinite articles", "Unbestimmte Artikel", "ein/eine; çoğul belirsiz artikel yoktur.", "ein/eine; there is no indefinite plural article.", "ein/eine; im Plural gibt es keinen unbestimmten Artikel.", "Sie hat eine Katze."),
    ("noun.gender", "İsim cinsiyetleri", "Noun gender", "Genus der Nomen", "İsimleri artikel ve çoğullarıyla öğren.", "Learn nouns with article and plural.", "Nomen immer mit Artikel und Plural lernen.", "der Tisch · die Tür · das Fenster"),
    ("adjective.endings", "Sıfat çekimleri", "Adjective endings", "Adjektivdeklination", "Sıfat sonu artikelin taşıdığı bilgiye göre değişir.", "The ending depends on information carried by the article.", "Die Endung hängt vom Artikel ab.", "ein guter Kaffee · der gute Kaffee"),
    ("pron.personal", "Kişi zamirleri", "Personal pronouns", "Personalpronomen", "ich, du, er/sie/es, wir, ihr, sie/Sie.", "ich, du, er/sie/es, wir, ihr, sie/Sie.", "ich, du, er/sie/es, wir, ihr, sie/Sie.", "Wir wohnen in Berlin."),
    ("pron.possessive", "İyelik zamirleri", "Possessives", "Possessivartikel", "mein, dein, sein, ihr, unser, euer.", "mein, dein, sein, ihr, unser, euer.", "mein, dein, sein, ihr, unser, euer.", "Das ist meine Schwester."),
    ("verb.present", "Fiil çekimleri", "Verb conjugation", "Verbkonjugation", "Fiil kökü kişi ekleriyle çekimlenir.", "The verb stem takes personal endings.", "Der Verbstamm bekommt Personalendungen.", "ich lerne · du lernst · er lernt"),
    ("verb.irregular", "Düzensiz fiiller", "Irregular verbs", "Unregelmäßige Verben", "Bazı fiiller du ve er/sie/es biçiminde kök değiştirir.", "Some verbs change their stem for du and er/sie/es.", "Manche Verben ändern den Stamm bei du und er/sie/es.", "du fährst · er liest"),
    ("verb.separable", "Ayrılabilen fiiller", "Separable verbs", "Trennbare Verben", "Ana cümlede ön ek sona gider.", "In a main clause the prefix moves to the end.", "Im Hauptsatz steht das Präfix am Ende.", "Der Zug kommt um acht Uhr an."),
    ("verb.modal", "Modal fiiller", "Modal verbs", "Modalverben", "Modal fiil çekilir, asıl fiil sonda mastar olur.", "The modal is conjugated; the main verb is final infinitive.", "Das Modalverb wird konjugiert; der Infinitiv steht am Ende.", "Ich kann heute kommen."),
    ("syntax.v2", "Fiil ikinci sırada", "Verb-second order", "Verbzweitstellung", "Ana cümlede çekimli fiil ikinci ögedir.", "The finite verb is the second constituent in a main clause.", "Im Hauptsatz steht das finite Verb an zweiter Stelle.", "Heute lerne ich Deutsch."),
    ("syntax.subordinate", "Yan cümlede fiil sonda", "Subordinate clauses", "Nebensätze", "weil, dass gibi bağlaçlardan sonra çekimli fiil sona gider.", "After weil or dass, the finite verb moves to the end.", "Nach weil oder dass steht das finite Verb am Ende.", "Ich bleibe zu Hause, weil es regnet."),
    ("tense.perfect", "Perfekt", "Present perfect", "Perfekt", "haben/sein + Partizip II; konuşmada yaygındır.", "haben/sein + past participle; common in speech.", "haben/sein + Partizip II; häufig in der gesprochenen Sprache.", "Wir sind nach Hause gegangen."),
    ("tense.preterite", "Präteritum", "Simple past", "Präteritum", "Yazıda ve sein/haben/modal fiillerde sık görülür.", "Common in writing and with sein/haben/modals.", "Häufig in Texten und bei sein/haben/Modalverben.", "Früher wohnte ich in Bonn."),
    ("prep.case", "Edat-hal eşleşmeleri", "Preposition-case pairs", "Präpositionen und Kasus", "mit daima Dativ; für daima Akkusativ alır.", "mit always takes dative; für always takes accusative.", "mit steht mit Dativ; für steht mit Akkusativ.", "mit dem Bus · für meinen Freund"),
    ("comparison", "Karşılaştırma ve üstünlük", "Comparison", "Komparation", "schnell – schneller – am schnellsten.", "schnell – schneller – am schnellsten.", "schnell – schneller – am schnellsten.", "Der Zug ist schneller als der Bus."),
    ("numbers", "Sayılar", "Numbers", "Zahlen", "Birleşik sayılar bir kelime olarak yazılır.", "Compound numbers are written as one word.", "Zusammengesetzte Zahlen schreibt man zusammen.", "einundzwanzig"),
    ("time", "Saat", "Telling time", "Uhrzeit", "Resmî: vierzehn Uhr dreißig; günlük: halb drei.", "Formal: vierzehn Uhr dreißig; colloquial: halb drei.", "Formell: vierzehn Uhr dreißig; umgangssprachlich: halb drei.", "Der Kurs beginnt um neun Uhr."),
    ("date", "Tarih", "Dates", "Datum", "Sıra sayısı nokta ile yazılır; edatla Dativ kullanılır.", "Ordinal numbers use a full stop; dates with am take dative.", "Ordnungszahlen haben einen Punkt; nach am steht Dativ.", "Heute ist der 3. Mai."),
    ("compounds", "Bileşik kelimeler", "Compound nouns", "Komposita", "Son isim cinsiyeti ve çoğulu belirler.", "The final noun determines gender and plural.", "Das letzte Nomen bestimmt Genus und Plural.", "die Haus+tür = die Haustür"),
]

GRAMMAR_TOPICS = [
    {"code": code, "title": {"tr": tr, "en": en, "de": de},
     "rule": {"tr": rtr, "en": ren, "de": rde}, "example": example}
    for code, tr, en, de, rtr, ren, rde, example in _TOPIC_ROWS
]

EXERCISES = [
    {"topic": "case.nom", "prompt": "___ Mann lernt Deutsch.", "answer": "Der", "options": ["Der", "Den", "Dem", "Des"], "explain": "Mann ist das Subjekt: Nominativ."},
    {"topic": "case.acc", "prompt": "Ich sehe ___ Mann.", "answer": "den", "options": ["der", "den", "dem", "des"], "explain": "Direktes Objekt: Akkusativ maskulin."},
    {"topic": "case.dat", "prompt": "Ich helfe ___ Kind.", "answer": "dem", "options": ["das", "den", "dem", "des"], "explain": "helfen verlangt den Dativ."},
    {"topic": "case.gen", "prompt": "Das ist das Auto ___ Lehrers.", "answer": "des", "options": ["der", "den", "dem", "des"], "explain": "Besitz: Genitiv maskulin."},
    {"topic": "article.def", "prompt": "___ Tür ist offen.", "answer": "Die", "options": ["Der", "Die", "Das", "Den"], "explain": "Tür ist feminin."},
    {"topic": "article.indef", "prompt": "Sie hat ___ Katze.", "answer": "eine", "options": ["ein", "eine", "einen", "einem"], "explain": "Katze ist feminin und Akkusativ."},
    {"topic": "adjective.endings", "prompt": "Das ist ein gut___ Kaffee.", "answer": "guter", "options": ["gute", "guter", "gutes", "guten"], "explain": "ein + Nominativ maskulin: -er."},
    {"topic": "verb.present", "prompt": "Du ___ Deutsch. (lernen)", "answer": "lernst", "options": ["lerne", "lernst", "lernt", "lernen"], "explain": "du-Endung: -st."},
    {"topic": "verb.irregular", "prompt": "Er ___ ein Buch. (lesen)", "answer": "liest", "options": ["lest", "liest", "lesen", "leset"], "explain": "lesen hat e→ie bei er/sie/es."},
    {"topic": "verb.separable", "prompt": "Der Zug ___ um acht Uhr ___. (ankommen)", "answer": "kommt … an", "options": ["ankommt", "kommt … an", "kommen … an", "an … kommt"], "explain": "Im Hauptsatz wird das Präfix getrennt."},
    {"topic": "verb.modal", "prompt": "Ich ___ heute arbeiten. (müssen)", "answer": "muss", "options": ["muss", "musst", "müssen", "müsst"], "explain": "ich muss; der Infinitiv steht am Ende."},
    {"topic": "syntax.v2", "prompt": "Heute ___ ich zu Hause.", "answer": "arbeite", "options": ["ich arbeite", "arbeite", "arbeiten", "gearbeitet"], "explain": "Das finite Verb steht an Position zwei."},
    {"topic": "syntax.subordinate", "prompt": "..., weil ich heute ___.", "answer": "arbeite", "options": ["arbeite", "ich arbeite", "arbeiten", "gearbeitet"], "explain": "Im Nebensatz steht das finite Verb am Ende."},
    {"topic": "tense.perfect", "prompt": "Wir ___ nach Hause gegangen.", "answer": "sind", "options": ["haben", "sind", "werden", "sein"], "explain": "gehen bildet das Perfekt mit sein."},
    {"topic": "prep.case", "prompt": "Ich fahre mit ___ Bus.", "answer": "dem", "options": ["der", "den", "dem", "des"], "explain": "mit verlangt den Dativ."},
    {"topic": "comparison", "prompt": "Der Zug ist ___ als der Bus.", "answer": "schneller", "options": ["schnell", "schneller", "am schnellsten", "schnelle"], "explain": "Vergleich mit als: Komparativ."},
    {"topic": "numbers", "prompt": "21 = ___", "answer": "einundzwanzig", "options": ["zwanzigeins", "einundzwanzig", "einszwanzig", "zwanzigundeins"], "explain": "Einer + und + Zehner, zusammengeschrieben."},
    {"topic": "time", "prompt": "08:30 = Es ist ___.", "answer": "halb neun", "options": ["halb acht", "halb neun", "acht halb", "neun halb"], "explain": "halb neun bedeutet 30 Minuten vor neun."},
]


def build(lab: str = "grammar", n: int = 10, rng: random.Random | None = None):
    if lab not in {"grammar", "cases", "verbs", "syntax", "numbers", "orthography"}:
        return []
    rng = rng or random.Random()
    source = list(EXERCISES)
    if lab == "cases":
        source = [e for e in source if e["topic"].startswith(("case.", "article."))]
    elif lab == "verbs":
        source = [e for e in source if e["topic"].startswith(("verb.", "tense."))]
    elif lab == "syntax":
        source = [e for e in source if e["topic"].startswith("syntax.")]
    elif lab == "numbers":
        source = [e for e in source if e["topic"] in {"numbers", "time", "date"}]
    elif lab == "orthography":
        source = [{"topic": "orthography", "prompt": f"Welche Schreibweise ist korrekt? {ex}",
                   "answer": token.split(" · ")[0], "options": [token.split(" · ")[0], token.split(" · ")[0].replace("ß", "ss"), token.split(" · ")[0].lower()],
                   "explain": rule} for token, _name, rule, ex in ORTHOGRAPHY if " · " in ex]
    if not source:
        return []
    return [dict(rng.choice(source)) for _ in range(n)]


RESOURCES = [
    {"id": "wikibooks-de", "title": "German - Wikibooks", "kind": "book", "level": "A1-C1",
     "url": "https://en.wikibooks.org/wiki/German", "license": "CC BY-SA 4.0",
     "attribution": "Wikibooks contributors", "online": True},
    {"id": "tatoeba-de", "title": "Tatoeba German sentences", "kind": "data", "level": "A1-C1",
     "url": "https://tatoeba.org/en/downloads", "license": "CC BY 2.0 FR / selected CC0",
     "attribution": "Tatoeba contributors; preserve sentence-level attribution", "online": True},
    {"id": "librivox-de", "title": "LibriVox German audiobooks", "kind": "audio", "level": "B1-C1",
     "url": "https://librivox.org/search?primary_key=4&search_category=language&search_page=1&search_form=get_results",
     "license": "Public domain in the USA; check local status", "attribution": "LibriVox volunteers", "online": True},
    {"id": "gutenberg-de", "title": "Project Gutenberg German shelf", "kind": "book", "level": "B1-C1",
     "url": "https://www.gutenberg.org/browse/languages/de", "license": "Project Gutenberg public-domain terms; check local status",
     "attribution": "Project Gutenberg and named authors/editors", "online": True},
]
