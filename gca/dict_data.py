"""Built-in German <-> English core dictionary (A1-B1, ~900 entries).

Line format:  headword|pos [article] [plural]|english; english 2[|note]
Nouns carry their article and plural in the second field (``n das Häuser``).
Irregular verb forms go into the optional note field (``ging, ist gegangen``).
"""

DATA = r"""
# ---- greetings / politeness ----
Hallo|int|hello; hi
Guten Morgen|phr|good morning
Guten Tag|phr|good day; hello
Guten Abend|phr|good evening
Gute Nacht|phr|good night
Auf Wiedersehen|phr|goodbye
Tschüss|int|bye
bis bald|phr|see you soon
bis später|phr|see you later
danke|int|thank you; thanks
vielen Dank|phr|thank you very much
bitte|part|please; you are welcome
Entschuldigung|n die Entschuldigungen|excuse me; apology
es tut mir leid|phr|I am sorry
ja|part|yes
nein|part|no
doch|part|yes (contradicting a negative); but; after all
gern|adv|gladly; with pleasure
gerne|adv|gladly; with pleasure
Willkommen|n das|welcome
Herzlichen Glückwunsch|phr|congratulations
Alles Gute|phr|all the best
Viel Glück|phr|good luck
Guten Appetit|phr|enjoy your meal
Gesundheit|n die|health; bless you
Prost|int|cheers
Wie geht es dir|phr|how are you (informal)
Wie geht es Ihnen|phr|how are you (formal)
Mir geht es gut|phr|I am fine
Wie heißt du|phr|what is your name (informal)
Ich heiße|phr|my name is
Ich komme aus|phr|I come from
Ich verstehe nicht|phr|I do not understand
Ich weiß nicht|phr|I do not know
Wie bitte|phr|pardon; sorry, what?
Sprechen Sie Englisch|phr|do you speak English
Können Sie das wiederholen|phr|can you repeat that
Wie viel kostet das|phr|how much does it cost
Wo ist|phr|where is
Ich hätte gern|phr|I would like
Ich möchte|phr|I would like
# ---- question words ----
wer|pron|who
was|pron|what
wo|adv|where
wohin|adv|where to
woher|adv|where from
wann|adv|when
warum|adv|why
wieso|adv|why; how come
wie|adv|how
welcher|pron|which
wessen|pron|whose
wie viel|phr|how much
wie viele|phr|how many
# ---- pronouns / articles ----
ich|pron|I
du|pron|you (singular, informal)
er|pron|he
sie|pron|she; they; you (formal, capitalised)
es|pron|it
wir|pron|we
ihr|pron|you (plural, informal); her; their
Sie|pron|you (formal)
mich|pron|me (accusative)
mir|pron|me (dative)
dich|pron|you (accusative)
dir|pron|you (dative)
ihn|pron|him
ihm|pron|him; it (dative)
uns|pron|us
euch|pron|you (plural, object)
ihnen|pron|them (dative)
mein|pron|my
dein|pron|your (informal)
sein|pron|his; its
unser|pron|our
euer|pron|your (plural)
Ihr|pron|your (formal)
der|art|the (masculine)
die|art|the (feminine; plural)
das|art|the (neuter)
ein|art|a; an (masculine, neuter)
eine|art|a; an (feminine)
kein|pron|no; not a; none
dieser|pron|this
jener|pron|that
jeder|pron|each; every
alle|pron|all; everyone
alles|pron|everything
etwas|pron|something; some
nichts|pron|nothing
jemand|pron|someone
niemand|pron|nobody
man|pron|one; you; people (impersonal)
sich|pron|oneself; himself; herself; themselves
selbst|pron|self; myself; even
einander|pron|each other
# ---- numbers ----
null|num|zero
eins|num|one
zwei|num|two
drei|num|three
vier|num|four
fünf|num|five
sechs|num|six
sieben|num|seven
acht|num|eight
neun|num|nine
zehn|num|ten
elf|num|eleven
zwölf|num|twelve
dreizehn|num|thirteen
vierzehn|num|fourteen
fünfzehn|num|fifteen
sechzehn|num|sixteen
siebzehn|num|seventeen
achtzehn|num|eighteen
neunzehn|num|nineteen
zwanzig|num|twenty
einundzwanzig|num|twenty-one
dreißig|num|thirty
vierzig|num|forty
fünfzig|num|fifty
sechzig|num|sixty
siebzig|num|seventy
achtzig|num|eighty
neunzig|num|ninety
hundert|num|hundred
tausend|num|thousand
Million|n die Millionen|million
erste|num|first
zweite|num|second
dritte|num|third
letzte|adj|last
Hälfte|n die Hälften|half
halb|adj|half
Mal|n das Male|time (occasion)
einmal|adv|once
zweimal|adv|twice
viel|adv|much; a lot
viele|pron|many
wenig|adv|little; few
einige|pron|some; several
ein paar|phr|a few; a couple of
ein bisschen|phr|a little; a bit
# ---- time ----
Zeit|n die Zeiten|time
Uhr|n die Uhren|clock; watch; o'clock
Stunde|n die Stunden|hour; lesson
Minute|n die Minuten|minute
Sekunde|n die Sekunden|second
Tag|n der Tage|day
Nacht|n die Nächte|night
Morgen|n der Morgen|morning
Vormittag|n der Vormittage|late morning
Mittag|n der Mittage|noon; midday
Nachmittag|n der Nachmittage|afternoon
Abend|n der Abende|evening
Woche|n die Wochen|week
Wochenende|n das Wochenenden|weekend
Monat|n der Monate|month
Jahr|n das Jahre|year
Jahrhundert|n das Jahrhunderte|century
heute|adv|today
morgen|adv|tomorrow
gestern|adv|yesterday
übermorgen|adv|the day after tomorrow
vorgestern|adv|the day before yesterday
jetzt|adv|now
gleich|adv|right away; in a moment; same
sofort|adv|immediately
bald|adv|soon
später|adv|later
früher|adv|earlier; formerly
früh|adv|early
spät|adv|late
immer|adv|always
nie|adv|never
niemals|adv|never
manchmal|adv|sometimes
oft|adv|often
selten|adv|rarely
meistens|adv|mostly; usually
schon|adv|already
noch|adv|still; yet
noch nicht|phr|not yet
wieder|adv|again
zuerst|adv|first; at first
dann|adv|then
danach|adv|after that
zuletzt|adv|last; finally
endlich|adv|finally; at last
plötzlich|adv|suddenly
lange|adv|for a long time
kurz|adv|briefly; short
Montag|n der Montage|Monday
Dienstag|n der Dienstage|Tuesday
Mittwoch|n der Mittwoche|Wednesday
Donnerstag|n der Donnerstage|Thursday
Freitag|n der Freitage|Friday
Samstag|n der Samstage|Saturday
Sonntag|n der Sonntage|Sunday
Januar|n der Januare|January
Februar|n der Februare|February
März|n der Märze|March
April|n der Aprile|April
Mai|n der Maie|May
Juni|n der Junis|June
Juli|n der Julis|July
August|n der Auguste|August
September|n der September|September
Oktober|n der Oktober|October
November|n der November|November
Dezember|n der Dezember|December
Frühling|n der Frühlinge|spring
Sommer|n der Sommer|summer
Herbst|n der Herbste|autumn; fall
Winter|n der Winter|winter
Feiertag|n der Feiertage|public holiday
Urlaub|n der Urlaube|vacation; holiday
Ferien|n die|school holidays
Geburtstag|n der Geburtstage|birthday
Termin|n der Termine|appointment; date; deadline
Kalender|n der Kalender|calendar
Datum|n das Daten|date
# ---- family / people ----
Mensch|n der Menschen|human; person
Leute|n die|people
Mann|n der Männer|man; husband
Frau|n die Frauen|woman; wife; Mrs
Kind|n das Kinder|child
Junge|n der Jungen|boy
Mädchen|n das Mädchen|girl
Baby|n das Babys|baby
Familie|n die Familien|family
Eltern|n die|parents
Mutter|n die Mütter|mother
Vater|n der Väter|father
Mama|n die Mamas|mom
Papa|n der Papas|dad
Sohn|n der Söhne|son
Tochter|n die Töchter|daughter
Bruder|n der Brüder|brother
Schwester|n die Schwestern|sister
Geschwister|n die|siblings
Großmutter|n die Großmütter|grandmother
Großvater|n der Großväter|grandfather
Oma|n die Omas|grandma
Opa|n der Opas|grandpa
Enkel|n der Enkel|grandson; grandchild
Onkel|n der Onkel|uncle
Tante|n die Tanten|aunt
Cousin|n der Cousins|cousin (male)
Cousine|n die Cousinen|cousin (female)
Ehemann|n der Ehemänner|husband
Ehefrau|n die Ehefrauen|wife
Freund|n der Freunde|friend; boyfriend
Freundin|n die Freundinnen|friend (female); girlfriend
Nachbar|n der Nachbarn|neighbour
Gast|n der Gäste|guest
Kollege|n der Kollegen|colleague
Chef|n der Chefs|boss
Herr|n der Herren|Mr; gentleman; lord
Name|n der Namen|name
Vorname|n der Vornamen|first name
Nachname|n der Nachnamen|surname
Alter|n das|age
Erwachsene|n der Erwachsenen|adult
Jugendliche|n der Jugendlichen|teenager; young person
Person|n die Personen|person
Bevölkerung|n die|population
# ---- jobs ----
Arbeit|n die Arbeiten|work; job
Beruf|n der Berufe|profession; occupation
Arzt|n der Ärzte|doctor (male)
Ärztin|n die Ärztinnen|doctor (female)
Lehrer|n der Lehrer|teacher
Lehrerin|n die Lehrerinnen|teacher (female)
Schüler|n der Schüler|pupil; student (school)
Student|n der Studenten|student (university)
Ingenieur|n der Ingenieure|engineer
Programmierer|n der Programmierer|programmer
Verkäufer|n der Verkäufer|shop assistant; salesman
Koch|n der Köche|cook; chef
Kellner|n der Kellner|waiter
Fahrer|n der Fahrer|driver
Polizist|n der Polizisten|police officer
Journalist|n der Journalisten|journalist
Künstler|n der Künstler|artist
Musiker|n der Musiker|musician
Schauspieler|n der Schauspieler|actor
Schriftsteller|n der Schriftsteller|writer
Anwalt|n der Anwälte|lawyer
Bäcker|n der Bäcker|baker
Friseur|n der Friseure|hairdresser
Krankenschwester|n die Krankenschwestern|nurse
Krankenpfleger|n der Krankenpfleger|nurse (male)
Handwerker|n der Handwerker|craftsman
Mechaniker|n der Mechaniker|mechanic
Sekretärin|n die Sekretärinnen|secretary
Beamte|n der Beamten|civil servant
Unternehmer|n der Unternehmer|entrepreneur
Wissenschaftler|n der Wissenschaftler|scientist
Übersetzer|n der Übersetzer|translator
Firma|n die Firmen|company; firm
Unternehmen|n das Unternehmen|company; enterprise
Büro|n das Büros|office
Fabrik|n die Fabriken|factory
Gehalt|n das Gehälter|salary
Lohn|n der Löhne|wage
Kunde|n der Kunden|customer
Besprechung|n die Besprechungen|meeting
Vertrag|n der Verträge|contract
Bewerbung|n die Bewerbungen|application (job)
Lebenslauf|n der Lebensläufe|CV; résumé
Stelle|n die Stellen|position; job; place
arbeitslos|adj|unemployed
Karriere|n die Karrieren|career
# ---- home ----
Haus|n das Häuser|house
Wohnung|n die Wohnungen|flat; apartment
Zimmer|n das Zimmer|room
Küche|n die Küchen|kitchen
Schlafzimmer|n das Schlafzimmer|bedroom
Wohnzimmer|n das Wohnzimmer|living room
Badezimmer|n das Badezimmer|bathroom
Bad|n das Bäder|bath; bathroom
Toilette|n die Toiletten|toilet
Flur|n der Flure|hallway; corridor
Balkon|n der Balkone|balcony
Garten|n der Gärten|garden
Keller|n der Keller|cellar; basement
Dach|n das Dächer|roof
Stock|n der Stockwerke|floor; storey
Treppe|n die Treppen|stairs
Aufzug|n der Aufzüge|lift; elevator
Tür|n die Türen|door
Fenster|n das Fenster|window
Wand|n die Wände|wall (interior)
Boden|n der Böden|floor; ground; soil
Decke|n die Decken|ceiling; blanket
Möbel|n die|furniture
Tisch|n der Tische|table
Stuhl|n der Stühle|chair
Sessel|n der Sessel|armchair
Sofa|n das Sofas|sofa
Bett|n das Betten|bed
Schrank|n der Schränke|cupboard; wardrobe
Regal|n das Regale|shelf
Spiegel|n der Spiegel|mirror
Lampe|n die Lampen|lamp
Licht|n das Lichter|light
Teppich|n der Teppiche|carpet
Bild|n das Bilder|picture; image
Kühlschrank|n der Kühlschränke|fridge
Herd|n der Herde|stove; cooker
Ofen|n der Öfen|oven
Waschmaschine|n die Waschmaschinen|washing machine
Fernseher|n der Fernseher|television set
Schlüssel|n der Schlüssel|key
Müll|n der|rubbish; garbage
Miete|n die Mieten|rent
Nachbarschaft|n die Nachbarschaften|neighbourhood
aufräumen|v|to tidy up
putzen|v|to clean
waschen|v|to wash|wusch, gewaschen
kochen|v|to cook; to boil
wohnen|v|to live; to reside
umziehen|v|to move (house)|zog um, ist umgezogen
mieten|v|to rent
# ---- everyday objects ----
Ding|n das Dinge|thing
Sache|n die Sachen|thing; matter
Tasche|n die Taschen|bag; pocket
Rucksack|n der Rucksäcke|backpack
Koffer|n der Koffer|suitcase
Geldbörse|n die Geldbörsen|wallet; purse
Geld|n das|money
Handy|n das Handys|mobile phone
Telefon|n das Telefone|telephone
Computer|n der Computer|computer
Laptop|n der Laptops|laptop
Brille|n die Brillen|glasses
Regenschirm|n der Regenschirme|umbrella
Buch|n das Bücher|book
Heft|n das Hefte|exercise book; notebook
Stift|n der Stifte|pen; pencil
Kugelschreiber|n der Kugelschreiber|ballpoint pen
Bleistift|n der Bleistifte|pencil
Papier|n das Papiere|paper
Brief|n der Briefe|letter (mail)
Zeitung|n die Zeitungen|newspaper
Zeitschrift|n die Zeitschriften|magazine
Foto|n das Fotos|photo
Geschenk|n das Geschenke|present; gift
Spielzeug|n das Spielzeuge|toy
Ball|n der Bälle|ball
Karte|n die Karten|card; map; ticket
Schachtel|n die Schachteln|box (small)
Kiste|n die Kisten|crate; box
Flasche|n die Flaschen|bottle
# ---- clothing ----
Kleidung|n die|clothing
Kleid|n das Kleider|dress
Hemd|n das Hemden|shirt
T-Shirt|n das T-Shirts|T-shirt
Hose|n die Hosen|trousers; pants
Jeans|n die Jeans|jeans
Rock|n der Röcke|skirt
Mantel|n der Mäntel|coat
Jacke|n die Jacken|jacket
Anzug|n der Anzüge|suit
Pullover|n der Pullover|sweater
Mütze|n die Mützen|cap; beanie
Hut|n der Hüte|hat
Schal|n der Schals|scarf
Handschuh|n der Handschuhe|glove
Socke|n die Socken|sock
Schuh|n der Schuhe|shoe
Stiefel|n der Stiefel|boot
Turnschuh|n der Turnschuhe|sneaker
Größe|n die Größen|size
anziehen|v|to put on (clothes); to attract|zog an, angezogen
ausziehen|v|to take off (clothes); to move out|zog aus, ausgezogen
tragen|v|to wear; to carry|trug, getragen
anprobieren|v|to try on
# ---- body / health ----
Körper|n der Körper|body
Kopf|n der Köpfe|head
Gesicht|n das Gesichter|face
Auge|n das Augen|eye
Ohr|n das Ohren|ear
Nase|n die Nasen|nose
Mund|n der Münder|mouth
Zahn|n der Zähne|tooth
Haar|n das Haare|hair
Hals|n der Hälse|neck; throat
Schulter|n die Schultern|shoulder
Arm|n der Arme|arm
Hand|n die Hände|hand
Finger|n der Finger|finger
Bein|n das Beine|leg
Fuß|n der Füße|foot
Knie|n das Knie|knee
Rücken|n der Rücken|back
Bauch|n der Bäuche|belly; stomach
Herz|n das Herzen|heart
Blut|n das|blood
Haut|n die Häute|skin
gesund|adj|healthy
krank|adj|ill; sick
Krankheit|n die Krankheiten|illness; disease
Schmerz|n der Schmerzen|pain
Kopfschmerzen|n die|headache
Fieber|n das|fever
Erkältung|n die Erkältungen|cold (illness)
Husten|n der|cough
Medikament|n das Medikamente|medicine; drug
Tablette|n die Tabletten|tablet; pill
Apotheke|n die Apotheken|pharmacy
Krankenhaus|n das Krankenhäuser|hospital
Praxis|n die Praxen|doctor's office; practice
Notarzt|n der Notärzte|emergency doctor
Unfall|n der Unfälle|accident
müde|adj|tired
schlafen|v|to sleep|schlief, geschlafen
einschlafen|v|to fall asleep|schlief ein, ist eingeschlafen
aufwachen|v|to wake up|wachte auf, ist aufgewacht
aufstehen|v|to get up|stand auf, ist aufgestanden
sich ausruhen|v|to rest
sich erholen|v|to recover; to relax
wehtun|v|to hurt|tat weh, wehgetan
# ---- food / drink ----
Essen|n das|food; meal
Frühstück|n das Frühstücke|breakfast
Mittagessen|n das Mittagessen|lunch
Abendessen|n das Abendessen|dinner; supper
Brot|n das Brote|bread
Brötchen|n das Brötchen|bread roll
Butter|n die|butter
Käse|n der|cheese
Milch|n die|milk
Ei|n das Eier|egg
Fleisch|n das|meat
Hähnchen|n das Hähnchen|chicken (food)
Fisch|n der Fische|fish
Wurst|n die Würste|sausage
Suppe|n die Suppen|soup
Reis|n der|rice
Nudel|n die Nudeln|noodle; pasta
Kartoffel|n die Kartoffeln|potato
Gemüse|n das|vegetables
Obst|n das|fruit
Apfel|n der Äpfel|apple
Birne|n die Birnen|pear; light bulb
Banane|n die Bananen|banana
Orange|n die Orangen|orange
Zitrone|n die Zitronen|lemon
Traube|n die Trauben|grape
Erdbeere|n die Erdbeeren|strawberry
Tomate|n die Tomaten|tomato
Gurke|n die Gurken|cucumber
Zwiebel|n die Zwiebeln|onion
Knoblauch|n der|garlic
Salat|n der Salate|salad; lettuce
Karotte|n die Karotten|carrot
Pilz|n der Pilze|mushroom
Salz|n das|salt
Zucker|n der|sugar
Pfeffer|n der|pepper
Öl|n das Öle|oil
Honig|n der|honey
Kuchen|n der Kuchen|cake
Keks|n der Kekse|biscuit; cookie
Schokolade|n die Schokoladen|chocolate
Eis|n das|ice cream; ice
Süßigkeit|n die Süßigkeiten|sweet; candy
Wasser|n das|water
Tee|n der Tees|tea
Kaffee|n der|coffee
Saft|n der Säfte|juice
Bier|n das Biere|beer
Wein|n der Weine|wine
Glas|n das Gläser|glass
Tasse|n die Tassen|cup
Teller|n der Teller|plate
Löffel|n der Löffel|spoon
Gabel|n die Gabeln|fork
Messer|n das Messer|knife
Topf|n der Töpfe|pot; saucepan
Pfanne|n die Pfannen|pan
Restaurant|n das Restaurants|restaurant
Café|n das Cafés|cafe
Bäckerei|n die Bäckereien|bakery
Speisekarte|n die Speisekarten|menu
Rechnung|n die Rechnungen|bill; invoice
Trinkgeld|n das Trinkgelder|tip (money)
lecker|adj|tasty; delicious
süß|adj|sweet; cute
sauer|adj|sour; annoyed
scharf|adj|spicy; sharp
frisch|adj|fresh
hungrig|adj|hungry
durstig|adj|thirsty
satt|adj|full (after eating)
Hunger|n der|hunger
Durst|n der|thirst
essen|v|to eat|aß, gegessen
trinken|v|to drink|trank, getrunken
frühstücken|v|to have breakfast
bestellen|v|to order
bezahlen|v|to pay
schmecken|v|to taste (good)
# ---- city / transport ----
Stadt|n die Städte|city; town
Dorf|n das Dörfer|village
Land|n das Länder|country; land; state
Hauptstadt|n die Hauptstädte|capital city
Straße|n die Straßen|street; road
Platz|n der Plätze|square; place; seat; space
Weg|n der Wege|way; path
Brücke|n die Brücken|bridge
Park|n der Parks|park
Zentrum|n das Zentren|centre
Innenstadt|n die Innenstädte|city centre
Gebäude|n das Gebäude|building
Kirche|n die Kirchen|church
Museum|n das Museen|museum
Theater|n das Theater|theatre
Kino|n das Kinos|cinema
Bibliothek|n die Bibliotheken|library
Schule|n die Schulen|school
Universität|n die Universitäten|university
Bank|n die Banken|bank
Post|n die|post office; mail
Hotel|n das Hotels|hotel
Bahnhof|n der Bahnhöfe|railway station
Haltestelle|n die Haltestellen|stop (bus, tram)
Flughafen|n der Flughäfen|airport
U-Bahn|n die U-Bahnen|underground; subway
S-Bahn|n die S-Bahnen|suburban train
Bus|n der Busse|bus
Straßenbahn|n die Straßenbahnen|tram
Auto|n das Autos|car
Taxi|n das Taxis|taxi
Zug|n der Züge|train
Flugzeug|n das Flugzeuge|aeroplane
Schiff|n das Schiffe|ship
Fahrrad|n das Fahrräder|bicycle
Fahrkarte|n die Fahrkarten|ticket (transport)
Ticket|n das Tickets|ticket
Reisepass|n der Reisepässe|passport
Ausweis|n der Ausweise|ID card
Grenze|n die Grenzen|border
Reise|n die Reisen|journey; trip
Ausflug|n der Ausflüge|excursion; outing
Tourist|n der Touristen|tourist
Stadtplan|n der Stadtpläne|city map
Adresse|n die Adressen|address
Ampel|n die Ampeln|traffic light
Kreuzung|n die Kreuzungen|crossroads
Ecke|n die Ecken|corner
Parkplatz|n der Parkplätze|parking space; car park
Tankstelle|n die Tankstellen|petrol station
Stau|n der Staus|traffic jam
Fahrplan|n der Fahrpläne|timetable
Abfahrt|n die Abfahrten|departure
Ankunft|n die Ankünfte|arrival
Gleis|n das Gleise|platform; track
Eingang|n der Eingänge|entrance
Ausgang|n der Ausgänge|exit
rechts|adv|right; on the right
links|adv|left; on the left
geradeaus|adv|straight ahead
weit|adj|far; wide
nah|adj|near
hier|adv|here
dort|adv|there
da|adv|there; then
dorthin|adv|to there
hierher|adv|to here
zu Hause|phr|at home
nach Hause|phr|(to) home
oben|adv|above; upstairs
unten|adv|below; downstairs
drinnen|adv|inside
draußen|adv|outside
überall|adv|everywhere
nirgends|adv|nowhere
# ---- movement verbs ----
gehen|v|to go; to walk|ging, ist gegangen
kommen|v|to come|kam, ist gekommen
fahren|v|to drive; to go (by vehicle)|fuhr, ist gefahren
laufen|v|to run; to walk|lief, ist gelaufen
rennen|v|to run|rannte, ist gerannt
fliegen|v|to fly|flog, ist geflogen
schwimmen|v|to swim|schwamm, ist geschwommen
reisen|v|to travel
ankommen|v|to arrive|kam an, ist angekommen
abfahren|v|to depart|fuhr ab, ist abgefahren
abfliegen|v|to take off (plane)|flog ab, ist abgeflogen
einsteigen|v|to get in; to board|stieg ein, ist eingestiegen
aussteigen|v|to get off; to get out|stieg aus, ist ausgestiegen
umsteigen|v|to change (trains)|stieg um, ist umgestiegen
zurückkommen|v|to come back|kam zurück, ist zurückgekommen
weggehen|v|to go away|ging weg, ist weggegangen
hereinkommen|v|to come in|kam herein, ist hereingekommen
hinausgehen|v|to go out|ging hinaus, ist hinausgegangen
bringen|v|to bring|brachte, gebracht
holen|v|to fetch; to get
abholen|v|to pick up
mitnehmen|v|to take along|nahm mit, mitgenommen
folgen|v|to follow
springen|v|to jump|sprang, ist gesprungen
fallen|v|to fall|fiel, ist gefallen
steigen|v|to climb; to rise|stieg, ist gestiegen
# ---- core verbs ----
sein|v|to be|war, ist gewesen
haben|v|to have|hatte, gehabt
werden|v|to become; will|wurde, ist geworden
machen|v|to do; to make
tun|v|to do|tat, getan
sagen|v|to say
sprechen|v|to speak|sprach, gesprochen
reden|v|to talk
erzählen|v|to tell; to narrate
fragen|v|to ask
antworten|v|to answer
bitten|v|to ask for; to request|bat, gebeten
wissen|v|to know (facts)|wusste, gewusst
kennen|v|to know (be familiar with)|kannte, gekannt
kennenlernen|v|to get to know; to meet
denken|v|to think|dachte, gedacht
glauben|v|to believe; to think
meinen|v|to mean; to think (opinion)
verstehen|v|to understand|verstand, verstanden
wollen|v|to want|wollte, gewollt
möchten|v|would like
können|v|can; to be able|konnte, gekonnt
müssen|v|must; to have to|musste, gemusst
sollen|v|should; to be supposed to
dürfen|v|may; to be allowed|durfte, gedurft
mögen|v|to like|mochte, gemocht
lieben|v|to love
gefallen|v|to please; to be liked|gefiel, gefallen
hassen|v|to hate
sehen|v|to see|sah, gesehen
schauen|v|to look
ansehen|v|to look at; to watch|sah an, angesehen
hören|v|to hear; to listen
zuhören|v|to listen (to)
lesen|v|to read|las, gelesen
schreiben|v|to write|schrieb, geschrieben
lernen|v|to learn; to study
studieren|v|to study (at university)
lehren|v|to teach
unterrichten|v|to teach; to instruct
üben|v|to practise
arbeiten|v|to work
leben|v|to live
spielen|v|to play
geben|v|to give|gab, gegeben
nehmen|v|to take|nahm, genommen
bekommen|v|to get; to receive|bekam, bekommen
kaufen|v|to buy
verkaufen|v|to sell
einkaufen|v|to shop; to go shopping
kosten|v|to cost
zahlen|v|to pay
öffnen|v|to open
aufmachen|v|to open (colloquial)
schließen|v|to close|schloss, geschlossen
zumachen|v|to close (colloquial)
anfangen|v|to begin|fing an, angefangen
beginnen|v|to begin|begann, begonnen
aufhören|v|to stop; to cease
beenden|v|to finish; to end
weitermachen|v|to continue
warten|v|to wait
suchen|v|to look for
finden|v|to find|fand, gefunden
verlieren|v|to lose|verlor, verloren
sich erinnern|v|to remember
vergessen|v|to forget|vergaß, vergessen
helfen|v|to help|half, geholfen
anrufen|v|to call (phone)|rief an, angerufen
treffen|v|to meet|traf, getroffen
sich treffen|v|to meet (each other)
zeigen|v|to show
erklären|v|to explain
übersetzen|v|to translate
wiederholen|v|to repeat
schicken|v|to send
senden|v|to send|sandte, gesandt
legen|v|to lay; to put (flat)
stellen|v|to put (upright); to place
setzen|v|to set; to put
sich setzen|v|to sit down
sitzen|v|to sit|saß, gesessen
stehen|v|to stand|stand, gestanden
liegen|v|to lie (be lying)|lag, gelegen
hängen|v|to hang|hing, gehangen
halten|v|to hold; to stop|hielt, gehalten
sich fühlen|v|to feel
fühlen|v|to feel
fürchten|v|to fear
hoffen|v|to hope
entscheiden|v|to decide|entschied, entschieden
sich entscheiden|v|to decide; to make up one's mind
lösen|v|to solve
probieren|v|to try; to taste
versuchen|v|to try; to attempt
träumen|v|to dream
lachen|v|to laugh
lächeln|v|to smile
weinen|v|to cry
schreien|v|to shout; to scream|schrie, geschrien
singen|v|to sing|sang, gesungen
tanzen|v|to dance
malen|v|to paint
zeichnen|v|to draw
spazieren gehen|phr|to go for a walk
wandern|v|to hike
sich interessieren|v|to be interested (in)
heißen|v|to be called|hieß, geheißen
nennen|v|to call; to name|nannte, genannt
heiraten|v|to marry
geboren werden|phr|to be born
sterben|v|to die|starb, ist gestorben
wachsen|v|to grow|wuchs, ist gewachsen
ändern|v|to change; to alter
sich ändern|v|to change (oneself)
wechseln|v|to change; to exchange
bauen|v|to build
kaputtgehen|v|to break (down)|ging kaputt, ist kaputtgegangen
reparieren|v|to repair
werfen|v|to throw|warf, geworfen
heben|v|to lift|hob, gehoben
bewegen|v|to move (something)
aufhalten|v|to stop; to hold up|hielt auf, aufgehalten
sich verspäten|v|to be late
sich beeilen|v|to hurry
schaffen|v|to manage; to create|schuf, geschaffen
einladen|v|to invite|lud ein, eingeladen
vorschlagen|v|to suggest|schlug vor, vorgeschlagen
empfehlen|v|to recommend|empfahl, empfohlen
raten|v|to advise; to guess|riet, geraten
versprechen|v|to promise|versprach, versprochen
erlauben|v|to allow
verbieten|v|to forbid|verbot, verboten
prüfen|v|to check; to test
überprüfen|v|to verify; to check
wählen|v|to choose; to elect; to dial
vergleichen|v|to compare|verglich, verglichen
zählen|v|to count
rechnen|v|to calculate
benutzen|v|to use
verwenden|v|to use; to apply
brauchen|v|to need
planen|v|to plan
organisieren|v|to organise
teilnehmen|v|to take part|nahm teil, teilgenommen
gewinnen|v|to win|gewann, gewonnen
passieren|v|to happen|passierte, ist passiert
geschehen|v|to happen|geschah, ist geschehen
scheinen|v|to seem; to shine|schien, geschienen
bedeuten|v|to mean
existieren|v|to exist
reichen|v|to be enough; to pass
genügen|v|to suffice
gehören|v|to belong
bleiben|v|to stay; to remain|blieb, ist geblieben
lassen|v|to let; to leave|ließ, gelassen
verlassen|v|to leave (a place)|verließ, verlassen
besuchen|v|to visit
begrüßen|v|to greet
sich verabschieden|v|to say goodbye
danken|v|to thank
sich entschuldigen|v|to apologise
sich freuen|v|to be glad; to look forward
sich ärgern|v|to be annoyed
sich sorgen|v|to worry
sich beschweren|v|to complain
streiten|v|to argue|stritt, gestritten
diskutieren|v|to discuss
zustimmen|v|to agree
ablehnen|v|to refuse; to reject
aufpassen|v|to pay attention; to watch out
merken|v|to notice; to remember
bemerken|v|to notice
beschreiben|v|to describe|beschrieb, beschrieben
sich vorstellen|v|to introduce oneself; to imagine
abhängen|v|to depend|hing ab, abgehangen
beeinflussen|v|to influence
sich unterscheiden|v|to differ|unterschied, unterschieden
entwickeln|v|to develop
schützen|v|to protect
zerstören|v|to destroy
sparen|v|to save (money)
ausgeben|v|to spend (money)|gab aus, ausgegeben
verdienen|v|to earn; to deserve
kündigen|v|to quit; to give notice
leiten|v|to lead; to manage
rauchen|v|to smoke
abnehmen|v|to lose weight; to decrease|nahm ab, abgenommen
zunehmen|v|to gain weight; to increase|nahm zu, zugenommen
heilen|v|to heal; to cure
behandeln|v|to treat
# ---- adjectives ----
groß|adj|big; tall
klein|adj|small; little
gut|adj|good
schlecht|adj|bad
neu|adj|new
alt|adj|old
jung|adj|young
schön|adj|beautiful; nice
hässlich|adj|ugly
klug|adj|clever
dumm|adj|stupid
nett|adj|nice; kind
freundlich|adj|friendly
böse|adj|angry; evil
lustig|adj|funny
traurig|adj|sad
glücklich|adj|happy; lucky
zufrieden|adj|satisfied; content
interessant|adj|interesting
langweilig|adj|boring
wichtig|adj|important
schwierig|adj|difficult
schwer|adj|heavy; difficult
leicht|adj|light; easy
einfach|adj|simple; easy
kompliziert|adj|complicated
teuer|adj|expensive
billig|adj|cheap
günstig|adj|inexpensive; favourable
reich|adj|rich
arm|adj|poor
stark|adj|strong
schwach|adj|weak
hoch|adj|high; tall
niedrig|adj|low
lang|adj|long
kurz|adj|short
breit|adj|wide
schmal|adj|narrow
eng|adj|tight; narrow
dick|adj|thick; fat
dünn|adj|thin
heiß|adj|hot
warm|adj|warm
kalt|adj|cold
kühl|adj|cool
schnell|adj|fast
langsam|adj|slow
laut|adj|loud
leise|adj|quiet
sauber|adj|clean
schmutzig|adj|dirty
hell|adj|bright; light
dunkel|adj|dark
voll|adj|full
leer|adj|empty
offen|adj|open
geschlossen|adj|closed
frei|adj|free; vacant
beschäftigt|adj|busy
fertig|adj|ready; finished
richtig|adj|correct; right
falsch|adj|wrong; false
echt|adj|real; genuine
möglich|adj|possible
unmöglich|adj|impossible
nötig|adj|necessary
gleich|adj|same; equal
anders|adj|different
ähnlich|adj|similar
verschieden|adj|different; various
nächste|adj|next
vorige|adj|previous
eigen|adj|own
persönlich|adj|personal
bequem|adj|comfortable
gefährlich|adj|dangerous
sicher|adj|safe; sure; certain
ehrlich|adj|honest
höflich|adj|polite
ernst|adj|serious
nass|adj|wet
trocken|adj|dry
weich|adj|soft
hart|adj|hard
rund|adj|round
lebendig|adj|alive; lively
tot|adj|dead
berühmt|adj|famous
beliebt|adj|popular
modern|adj|modern
bekannt|adj|known; well-known
fremd|adj|foreign; strange
deutsch|adj|German
englisch|adj|English
türkisch|adj|Turkish
französisch|adj|French
russisch|adj|Russian
fleißig|adj|hard-working
faul|adj|lazy
ruhig|adj|calm; quiet
nervös|adj|nervous
verrückt|adj|crazy
allein|adj|alone
zusammen|adv|together
ganz|adj|whole; entire; quite
# ---- colours ----
Farbe|n die Farben|colour
weiß|adj|white
schwarz|adj|black
rot|adj|red
blau|adj|blue
grün|adj|green
gelb|adj|yellow
orange|adj|orange
braun|adj|brown
grau|adj|grey
rosa|adj|pink
lila|adj|purple
bunt|adj|colourful
# ---- adverbs / particles / prepositions / conjunctions ----
sehr|adv|very
zu|adv|too (excessively)
fast|adv|almost
nur|adv|only
auch|adv|also; too
ebenfalls|adv|likewise; also
sogar|adv|even
etwa|adv|approximately; perhaps
ungefähr|adv|approximately
genau|adv|exactly
wirklich|adv|really
natürlich|adv|of course; naturally
vielleicht|adv|maybe; perhaps
wahrscheinlich|adv|probably
bestimmt|adv|certainly
leider|adv|unfortunately
hoffentlich|adv|hopefully
besonders|adv|especially
ziemlich|adv|rather; quite
gar nicht|phr|not at all
überhaupt|adv|at all; generally
eigentlich|adv|actually
übrigens|adv|by the way
also|adv|so; therefore
deshalb|adv|therefore
trotzdem|adv|nevertheless
sonst|adv|otherwise
außerdem|adv|besides; moreover
jedoch|adv|however
nämlich|adv|namely; you see
mal|part|once; just (softening particle)
nicht|part|not
und|conj|and
oder|conj|or
aber|conj|but
sondern|conj|but rather
denn|conj|because; for
weil|conj|because
dass|conj|that
ob|conj|whether; if
wenn|conj|if; when
als|conj|when (past); than; as
obwohl|conj|although
damit|conj|so that
bevor|conj|before
nachdem|conj|after
während|conj|while; during
seit|prep|since; for (time)
bis|prep|until
in|prep|in; into
an|prep|at; on
auf|prep|on; onto
unter|prep|under; among
über|prep|over; above; about
vor|prep|in front of; before; ago
hinter|prep|behind
neben|prep|next to
zwischen|prep|between
mit|prep|with
ohne|prep|without
für|prep|for
gegen|prep|against; around (time)
um|prep|around; at (time)
durch|prep|through
nach|prep|after; to (a place)
aus|prep|out of; from
bei|prep|at; near; with
von|prep|from; of
zu|prep|to; at
außer|prep|except
wegen|prep|because of
trotz|prep|despite
statt|prep|instead of
entlang|prep|along
gegenüber|prep|opposite
# ---- education / language ----
Sprache|n die Sprachen|language
Wort|n das Wörter|word
Satz|n der Sätze|sentence
Buchstabe|n der Buchstaben|letter (alphabet)
Alphabet|n das Alphabete|alphabet
Grammatik|n die Grammatiken|grammar
Wörterbuch|n das Wörterbücher|dictionary
Wortschatz|n der|vocabulary
Unterricht|n der|lessons; teaching
Klasse|n die Klassen|class
Kurs|n der Kurse|course
Prüfung|n die Prüfungen|exam
Test|n der Tests|test
Note|n die Noten|grade; mark; note (music)
Fehler|n der Fehler|mistake
Frage|n die Fragen|question
Antwort|n die Antworten|answer
Regel|n die Regeln|rule
Beispiel|n das Beispiele|example
Aufgabe|n die Aufgaben|task; exercise
Hausaufgabe|n die Hausaufgaben|homework
Übung|n die Übungen|exercise; practice
Text|n der Texte|text
Geschichte|n die Geschichten|story; history
Literatur|n die|literature
Mathematik|n die|mathematics
Physik|n die|physics
Chemie|n die|chemistry
Biologie|n die|biology
Erdkunde|n die|geography
Wissenschaft|n die Wissenschaften|science
Bedeutung|n die Bedeutungen|meaning; importance
Übersetzung|n die Übersetzungen|translation
Aussprache|n die|pronunciation
Erinnerung|n die Erinnerungen|memory; reminder
Aufmerksamkeit|n die|attention
Kenntnis|n die Kenntnisse|knowledge
Erfahrung|n die Erfahrungen|experience
Tafel|n die Tafeln|blackboard; bar (of chocolate)
Pause|n die Pausen|break
Zeugnis|n das Zeugnisse|school report; certificate
Ausbildung|n die Ausbildungen|training; education
# ---- money / shopping ----
Preis|n der Preise|price; prize
Euro|n der Euro|euro
Cent|n der Cent|cent
Kasse|n die Kassen|cash desk; checkout
Kleingeld|n das|small change
Wechselgeld|n das|change (money)
Rabatt|n der Rabatte|discount
Angebot|n das Angebote|offer
kostenlos|adj|free of charge
Geschäft|n das Geschäfte|shop; business
Laden|n der Läden|shop
Supermarkt|n der Supermärkte|supermarket
Markt|n der Märkte|market
Einkaufszentrum|n das Einkaufszentren|shopping centre
Kaufhaus|n das Kaufhäuser|department store
Ware|n die Waren|goods
Produkt|n das Produkte|product
Qualität|n die Qualitäten|quality
Kreditkarte|n die Kreditkarten|credit card
Konto|n das Konten|account
Schulden|n die|debts
Steuer|n die Steuern|tax
Versicherung|n die Versicherungen|insurance
# ---- communication / technology ----
Internet|n das|internet
Webseite|n die Webseiten|website
E-Mail|n die E-Mails|e-mail
Nachricht|n die Nachrichten|message; news item
Nachrichten|n die|the news
Nummer|n die Nummern|number
Anruf|n der Anrufe|phone call
Verbindung|n die Verbindungen|connection
Information|n die Informationen|information
Programm|n das Programme|programme; program
App|n die Apps|app
Bildschirm|n der Bildschirme|screen
Taste|n die Tasten|key (keyboard)
Tastatur|n die Tastaturen|keyboard
Maus|n die Mäuse|mouse
Datei|n die Dateien|file
Ordner|n der Ordner|folder
Passwort|n das Passwörter|password
Drucker|n der Drucker|printer
Radio|n das Radios|radio
Musik|n die|music
Lied|n das Lieder|song
Film|n der Filme|film; movie
Serie|n die Serien|TV series
Spiel|n das Spiele|game; match
Kamera|n die Kameras|camera
Akku|n der Akkus|rechargeable battery
Batterie|n die Batterien|battery
aufladen|v|to charge|lud auf, aufgeladen
einschalten|v|to switch on
ausschalten|v|to switch off
herunterladen|v|to download|lud herunter, heruntergeladen
drucken|v|to print
speichern|v|to save (file)
löschen|v|to delete
# ---- nature / weather ----
Natur|n die|nature
Wetter|n das|weather
Sonne|n die Sonnen|sun
Mond|n der Monde|moon
Stern|n der Sterne|star
Himmel|n der Himmel|sky; heaven
Wolke|n die Wolken|cloud
Regen|n der|rain
Schnee|n der|snow
Wind|n der Winde|wind
Gewitter|n das Gewitter|thunderstorm
Nebel|n der|fog
Frost|n der|frost
Hitze|n die|heat
Grad|n der Grade|degree
Erde|n die|earth; soil
Welt|n die Welten|world
Luft|n die|air
Feuer|n das Feuer|fire
Meer|n das Meere|sea
See|n der Seen|lake
Fluss|n der Flüsse|river
Ufer|n das Ufer|shore; bank
Insel|n die Inseln|island
Berg|n der Berge|mountain
Wald|n der Wälder|forest
Feld|n das Felder|field
Baum|n der Bäume|tree
Blume|n die Blumen|flower
Gras|n das|grass
Blatt|n das Blätter|leaf; sheet
Stein|n der Steine|stone
Sand|n der|sand
Tier|n das Tiere|animal
Hund|n der Hunde|dog
Katze|n die Katzen|cat
Pferd|n das Pferde|horse
Kuh|n die Kühe|cow
Schwein|n das Schweine|pig
Vogel|n der Vögel|bird
Bär|n der Bären|bear
Wolf|n der Wölfe|wolf
Fuchs|n der Füchse|fox
Hase|n der Hasen|hare
Schlange|n die Schlangen|snake; queue
Insekt|n das Insekten|insect
Es regnet|phr|it is raining
Es schneit|phr|it is snowing
Es ist kalt|phr|it is cold
Es ist heiß|phr|it is hot
sonnig|adj|sunny
bewölkt|adj|cloudy
windig|adj|windy
# ---- sport / leisure ----
Sport|n der|sport
Fußball|n der|football; soccer
Handball|n der|handball
Tennis|n das|tennis
Schach|n das|chess
Schwimmbad|n das Schwimmbäder|swimming pool
Stadion|n das Stadien|stadium
Mannschaft|n die Mannschaften|team
Training|n das|training
Sieg|n der Siege|victory
Hobby|n das Hobbys|hobby
Freizeit|n die|free time; leisure
Konzert|n das Konzerte|concert
Ausstellung|n die Ausstellungen|exhibition
Party|n die Partys|party
Fest|n das Feste|celebration; festival
feiern|v|to celebrate
Verein|n der Vereine|club; association
# ---- feelings / abstract ----
Leben|n das Leben|life
Tod|n der|death
Liebe|n die|love
Freundschaft|n die Freundschaften|friendship
Glück|n das|happiness; luck
Freude|n die|joy
Angst|n die Ängste|fear; anxiety
Hoffnung|n die Hoffnungen|hope
Traum|n der Träume|dream
Wahrheit|n die Wahrheiten|truth
Lüge|n die Lügen|lie
Gedanke|n der Gedanken|thought
Idee|n die Ideen|idea
Meinung|n die Meinungen|opinion
Gefühl|n das Gefühle|feeling
Laune|n die Launen|mood
Wunsch|n der Wünsche|wish
Interesse|n das Interessen|interest
Freiheit|n die|freedom
Recht|n das Rechte|right; law
Gesetz|n das Gesetze|law
Ordnung|n die|order
Wahl|n die Wahlen|choice; election
Möglichkeit|n die Möglichkeiten|possibility; opportunity
Grund|n der Gründe|reason; ground
Folge|n die Folgen|consequence; episode
Fall|n der Fälle|case; fall
Art|n die Arten|kind; type; way
Weise|n die Weisen|manner; way
Bedingung|n die Bedingungen|condition
Unterschied|n der Unterschiede|difference
Teil|n der Teile|part
Ende|n das Enden|end
Anfang|n der Anfänge|beginning
Mitte|n die|middle
Ort|n der Orte|place; location
Seite|n die Seiten|side; page
Form|n die Formen|form; shape
Zahl|n die Zahlen|number
Menge|n die Mengen|amount; quantity; crowd
Gewicht|n das Gewichte|weight
Gesellschaft|n die Gesellschaften|society; company
Staat|n der Staaten|state (country)
Regierung|n die Regierungen|government
Volk|n das Völker|people; nation
Krieg|n der Kriege|war
Frieden|n der|peace
Polizei|n die|police
Kultur|n die Kulturen|culture
Kunst|n die Künste|art
Religion|n die Religionen|religion
Problem|n das Probleme|problem
Lösung|n die Lösungen|solution
Erfolg|n der Erfolge|success
Ziel|n das Ziele|goal; destination
Plan|n der Pläne|plan
Ergebnis|n das Ergebnisse|result
Projekt|n das Projekte|project
Umwelt|n die|environment
Zukunft|n die|future
Vergangenheit|n die|past
Gegenwart|n die|present
Ereignis|n das Ereignisse|event
Situation|n die Situationen|situation
Beziehung|n die Beziehungen|relationship
Verantwortung|n die|responsibility
Sicherheit|n die|safety; security
"""
