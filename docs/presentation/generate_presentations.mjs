import fs from "node:fs/promises";
import path from "node:path";
// The deck renderer is an internal tool; point ARTIFACT_TOOL at its module (file:// URL or package name).
const { Presentation } = await import(process.env.ARTIFACT_TOOL ?? "@oai/artifact-tool");

// Repo kokleri: betik <root>/tmp icinde durur; GEFR_ROOT ile disaridan da verilebilir.
const ROOT = process.env.GEFR_ROOT ?? path.resolve(path.dirname(new URL(import.meta.url).pathname.replace(/^\/([A-Za-z]:)/, "$1")), "..");

const W = 1280;
const H = 720;
const INK = "#111111";
const MUTED = "#5D6470";
const PANEL = "#EDEDED";
const RULE = "#B8BCC4";
const FONT = "Arial";
let shapeSerial = 0;

async function bytes(file) {
  const b = await fs.readFile(file);
  return b.buffer.slice(b.byteOffset, b.byteOffset + b.byteLength);
}

async function writeBlob(file, blob) {
  await fs.mkdir(path.dirname(file), { recursive: true });
  await fs.writeFile(file, new Uint8Array(await blob.arrayBuffer()));
}

function box(slide, x, y, w, h, fill, line = fill, lineWidth = 0) {
  return slide.shapes.add({
    name: `box-${++shapeSerial}`,
    geometry: "rect",
    position: { left: x, top: y, width: w, height: h },
    fill,
    line: { style: "solid", fill: line, width: lineWidth },
  });
}

function txt(slide, text, x, y, w, h, size, opts = {}) {
  const shape = slide.shapes.add({
    name: `text-${++shapeSerial}`,
    geometry: "textbox",
    position: { left: x, top: y, width: w, height: h },
    fill: "none",
    line: { style: "solid", fill: "none", width: 0 },
  });
  shape.text = text;
  shape.text.style = {
    fontSize: size,
    bold: Boolean(opts.bold),
    color: opts.color || INK,
    typeface: FONT,
    alignment: opts.align || "left",
    verticalAlignment: opts.valign || "top",
  };
  return shape;
}

function baseSlide(pres, cfg, index, withMeta = true) {
  const slide = pres.slides.add();
  slide.background.fill = "#FFFFFF";
  box(slide, 0, 0, 14, H, cfg.accent);
  if (withMeta) {
    txt(slide, cfg.shortName.toUpperCase(), 42, 30, 470, 28, 16, { bold: true, color: cfg.accentDark });
    txt(slide, `${String(index).padStart(2, "0")} / 06`, 1160, 30, 78, 24, 14, { color: MUTED, align: "right" });
  }
  return slide;
}

function setNotes(slide, text) {
  slide.speakerNotes.textFrame.setText(text);
}

async function buildDeck(cfg) {
  const pres = Presentation.create({ slideSize: { width: W, height: H } });
  const iconBytes = await bytes(cfg.icon);
  const screenshotBytes = await bytes(cfg.screenshot);

  // 01 — Codex Grid slide 01: sparse stacked title flow.
  {
    const s = baseSlide(pres, cfg, 1);
    txt(s, cfg.kicker, 42, 76, 760, 32, 18, { bold: true, color: cfg.accentDark });
    txt(s, cfg.name, 42, 170, 860, 94, 68, { bold: true });
    txt(s, cfg.titleLine, 42, 288, 740, 48, 25, { color: MUTED });
    txt(s, cfg.taglineTr, 42, 440, 700, 34, 21, { bold: true });
    txt(s, cfg.taglineEn, 42, 482, 700, 30, 19, { color: MUTED });
    txt(s, cfg.taglineTarget, 42, 520, 700, 30, 19, { color: MUTED });
    box(s, 916, 138, 250, 250, cfg.pale, cfg.accent, 2);
    s.images.add({ blob: iconBytes, contentType: "image/png", alt: `${cfg.name} application icon`, fit: "contain", position: { left: 941, top: 163, width: 200, height: 200 } });
    txt(s, cfg.platformCaption || "Windows · Python · SQLite", 916, 420, 250, 30, 17, { align: "center", color: MUTED });
    setNotes(s, `${cfg.name} overview.\n\n[Sources]\n- Original icon generated for this project: ${cfg.icon}\n[/Sources]`);
  }

  // 02 — Codex Grid slide 08: text + dominant real product evidence.
  {
    const s = baseSlide(pres, cfg, 2);
    txt(s, cfg.uiTitleTarget, 42, 82, 430, 105, 40, { bold: true });
    txt(s, cfg.uiTitleTr, 42, 198, 430, 28, 19, { bold: true, color: cfg.accentDark });
    txt(s, cfg.uiTitleEn, 42, 232, 430, 28, 19, { color: MUTED });
    box(s, 42, 274, 378, 2, cfg.accent);
    txt(s, cfg.uiBodyTarget, 42, 306, 400, 134, 21);
    txt(s, cfg.uiBodyTr, 42, 452, 400, 70, 18, { color: MUTED });
    txt(s, cfg.uiBodyEn, 42, 548, 400, 70, 18, { color: MUTED });
    box(s, 474, 92, 764, 520, cfg.pale, RULE, 1);
    s.images.add({ blob: screenshotBytes, contentType: "image/jpeg", alt: `Real ${cfg.name} Windows application screenshot`, fit: "contain", position: { left: 492, top: 110, width: 728, height: 476 } });
    txt(s, cfg.realCaption, 492, 622, 728, 26, 15, { align: "right", color: MUTED });
    setNotes(s, `This is a real screenshot captured from the packaged Windows executable.\n\n[Sources]\n- Product screenshot: ${cfg.screenshot}\n[/Sources]`);
  }

  // 03 — Codex Grid slide 06: three parallel language columns.
  {
    const s = baseSlide(pres, cfg, 3);
    txt(s, cfg.engineTitle, 42, 82, 1100, 62, 48, { bold: true });
    txt(s, cfg.engineSub, 42, 150, 1100, 34, 19, { color: MUTED });
    const cols = [42, 452, 862];
    const labels = [cfg.langs[0], cfg.langs[1], cfg.langs[2]];
    const heads = cfg.engineHeads;
    const bodies = cfg.engineBodies;
    for (let i = 0; i < 3; i++) {
      txt(s, labels[i].toUpperCase(), cols[i], 258, 330, 28, 15, { bold: true, color: cfg.accentDark });
      box(s, cols[i], 304, 330, 3, i === 1 ? cfg.accent : INK);
      txt(s, heads[i], cols[i], 334, 330, 62, 25, { bold: true });
      txt(s, bodies[i], cols[i], 416, 330, 148, 20, { color: MUTED });
    }
    txt(s, cfg.catalogLine, 42, 616, 1100, 34, 16, { color: MUTED });
    setNotes(s, `Learning engine and openly licensed resource catalog.\n\n[Sources]\n- ${cfg.wikibooks}\n- https://tatoeba.org/en/downloads\n- https://librivox.org/pages/about-librivox/\n- https://www.gutenberg.org/policy/permission.html\n[/Sources]`);
  }

  // 04 — Codex Grid slide 13: four language-specific evidence regions.
  {
    const s = baseSlide(pres, cfg, 4);
    txt(s, cfg.labTitleTarget, 42, 82, 1040, 62, 48, { bold: true });
    txt(s, `${cfg.labTitleTr}  ·  ${cfg.labTitleEn}`, 42, 150, 1060, 32, 19, { color: MUTED });
    const cells = [
      [42, 234], [656, 234], [42, 430], [656, 430],
    ];
    for (let i = 0; i < 4; i++) {
      const [x, y] = cells[i];
      box(s, x, y, 540, 1, RULE);
      txt(s, cfg.labExamples[i], x, y + 22, 540, 54, 32, { bold: true, color: i === 0 ? cfg.accentDark : INK });
      txt(s, cfg.labDescriptions[i], x, y + 90, 520, 66, 18, { color: MUTED });
    }
    setNotes(s, `${cfg.name} language-specific lab examples.\n\n[Sources]\n- Product seed data and tests in the local ${cfg.pkg} source tree.\n[/Sources]`);
  }

  // 05 — Codex Grid slide 17: privacy flow over three milestones.
  {
    const s = baseSlide(pres, cfg, 5);
    txt(s, cfg.privacyTitleTr, 42, 82, 1160, 60, 44, { bold: true });
    txt(s, `${cfg.privacyTitleEn}  ·  ${cfg.privacyTitleTarget}`, 42, 150, 1120, 34, 19, { color: MUTED });
    box(s, 70, 348, 1050, 2, INK);
    const xs = [92, 492, 892];
    for (let i = 0; i < 3; i++) {
      s.shapes.add({ name: `dot-${++shapeSerial}`, geometry: "ellipse", position: { left: xs[i], top: 337, width: 24, height: 24 }, fill: i === 1 ? cfg.accent : INK, line: { style: "solid", fill: "none", width: 0 } });
      txt(s, cfg.flowLabels[i], xs[i], 292, 260, 30, 16, { bold: true, color: cfg.accentDark });
      txt(s, cfg.flowHeads[i], xs[i], 388, 270, 58, 28, { bold: true });
      txt(s, cfg.flowBodies[i], xs[i], 460, 280, 92, 19, { color: MUTED });
    }
    box(s, 42, 606, 1120, 50, cfg.pale);
    txt(s, cfg.offlineLine, 62, 617, 1080, 28, 17, { bold: true, color: cfg.accentDark, align: "center" });
    setNotes(s, `The optional AI path uses a local LM Studio endpoint. The token ledger stores usage metadata, not prompt or response text.\n\n[Sources]\n- Local application source: ${cfg.pkg}/ai.py and ${cfg.pkg}/db.py\n[/Sources]`);
  }

  // 06 — Codex Grid slide 26: resolved close and delivery proof.
  {
    const s = baseSlide(pres, cfg, 6, false);
    txt(s, cfg.closeKicker, 42, 48, 900, 30, 18, { bold: true, color: cfg.accentDark });
    txt(s, cfg.closeWords[0], 42, 176, 260, 88, 64, { bold: true });
    txt(s, cfg.closeWords[1], 326, 176, 260, 88, 64, { bold: true });
    txt(s, cfg.closeWords[2], 610, 176, 300, 88, 64, { bold: true });
    txt(s, cfg.closeSub, 42, 286, 930, 40, 22, { color: MUTED });
    txt(s, cfg.metricWords, 42, 418, 260, 60, 42, { bold: true, color: cfg.accentDark });
    txt(s, cfg.metricTests, 368, 418, 260, 60, 42, { bold: true });
    txt(s, "18", 694, 418, 160, 60, 42, { bold: true });
    txt(s, cfg.metricWordsLabel, 42, 490, 260, 88, 17, { color: MUTED });
    txt(s, cfg.metricTestsLabel, 368, 490, 260, 88, 17, { color: MUTED });
    txt(s, cfg.metricTabsLabel, 694, 490, 220, 88, 17, { color: MUTED });
    box(s, 42, 590, 1120, 2, cfg.accent);
    if (cfg.platformLineTr) {
      txt(s, cfg.deliveryLine, 42, 600, 1120, 22, 14, { bold: true });
      txt(s, cfg.platformLineTr, 42, 626, 1120, 22, 14, { bold: true, color: cfg.accentDark });
      txt(s, cfg.platformLineEn, 42, 650, 1120, 20, 13, { color: MUTED });
      if (cfg.macNote) txt(s, cfg.macNote, 42, 672, 1120, 20, 12, { color: MUTED });
    } else {
      txt(s, cfg.deliveryLine, 42, 610, 1120, 54, 16, { bold: true });
    }
    setNotes(s, `Delivery summary based on the packaged executable and automated test suite.\n\n[Sources]\n- ${cfg.name} local build output\n- ${cfg.name} pytest results${cfg.releaseUrl ? `\n- ${cfg.releaseUrl}` : ""}\n[/Sources]`);
  }

  const outDir = path.dirname(cfg.output);
  const renderDir = path.join(outDir, "render-artifact-tool");
  await fs.mkdir(renderDir, { recursive: true });
  for (const [i, slide] of pres.slides.items.entries()) {
    const stem = `slide-${String(i + 1).padStart(2, "0")}`;
    await writeBlob(path.join(renderDir, `${stem}.png`), await pres.export({ slide, format: "png", scale: 1 }));
    const layout = await slide.export({ format: "layout" });
    await fs.writeFile(path.join(renderDir, `${stem}.layout.json`), await layout.text());
  }
  await writeBlob(path.join(renderDir, "montage.webp"), await pres.export({ format: "webp", montage: true, scale: 1 }));
  await writeBlob(cfg.output, await pres.export({ format: "pptx" }));
  return cfg.output;
}

const configs = [
  {
    name: "German Course AI", shortName: "German Course AI", pkg: "gca",
    output: path.join(ROOT, "GermanCourseAI/docs/presentation/German-Course-AI-Trilingual.pptx"),
    icon: path.join(ROOT, "GermanCourseAI/assets/app-final.png"),
    screenshot: path.join(ROOT, "GermanCourseAI/docs/presentation/assets/german-course-ai-screenshot.jpg"),
    accent: "#E8AE2E", accentDark: "#9A6500", pale: "#FFF3CF",
    kicker: "OFFLINE-FIRST WINDOWS LANGUAGE LEARNING",
    titleLine: "Türkçe · English · Deutsch",
    taglineTr: "Yerel, ölçülebilir Almanca öğrenimi",
    taglineEn: "Local, measurable German learning",
    taglineTarget: "Lokales, messbares Deutschlernen",
    uiTitleTarget: "Lernen ohne Reibung",
    uiTitleTr: "Tek uygulama, üç arayüz",
    uiTitleEn: "One app, three interfaces",
    uiBodyTarget: "18 Bereiche verbinden Wiederholung, Wortschatz, ein dreisprachiges Wörterbuch DE-EN-TR, Prüfung, Grammatik und Praxis in einem ruhigen Windows-Arbeitsraum.",
    uiBodyTr: "Dil seçimi anında kaydedilir; uygulama çevrimdışı çalışmaya devam eder.",
    uiBodyEn: "The language choice persists instantly, and core learning stays available offline.",
    realCaption: "Gerçek EXE ekranı · Real executable · Echte Anwendung",
    engineTitle: "A learning engine that remembers",
    engineSub: "Öğrenme motoru hatırlar · Die Lernmaschine merkt sich den Fortschritt",
    langs: ["Türkçe", "English", "Deutsch"],
    engineHeads: ["Her gün doğru sıra", "Practice with evidence", "Fortschritt bleibt lokal"],
    engineBodies: ["SM-2 ve Leitner, yeni ve gecikmiş kartları günlük bir sıraya dönüştürür.", "160 A1 entries, a 1,260-entry DE-EN-TR dictionary with selectable direction, strict spelling, exams, favorites and mistakes share one SQLite record.", "Wiederholung, Fehler, Favoriten und Prüfungen werden lokal und nachvollziehbar gespeichert."],
    catalogLine: "Kaynak kataloğu / resource catalog / Quellenkatalog: Wikibooks · Tatoeba · LibriVox · Project Gutenberg",
    wikibooks: "https://en.wikibooks.org/wiki/German",
    labTitleTarget: "Deutsch verdient präzise Werkzeuge",
    labTitleTr: "Almancaya özgü laboratuvar", labTitleEn: "A German-specific language lab",
    labExamples: ["der Tisch · die Tische", "ä · ö · ü", "Straße · Grüße", "Häuser → das Haus"],
    labDescriptions: ["Artikel + çoğul birlikte · article and plural together · Artikel und Plural zusammen", "Umlaut araması kontrollü · controlled umlaut search · kontrollierte Umlautsuche", "ß aramada esnek, yanıtta kesin · flexible search, strict answer · flexible Suche, genaue Antwort", "Sözlük DE↔EN↔TR yön seçimli · dictionary DE/EN/TR with direction switch · Wörterbuch DE/EN/TR mit Richtungswahl"],
    privacyTitleTr: "AI isteğe bağlı; mahremiyet varsayılan",
    privacyTitleEn: "AI is optional; privacy is the default", privacyTitleTarget: "KI ist optional; Datenschutz ist Standard",
    flowLabels: ["01 · CONTEXT", "02 · LOCAL MODEL", "03 · RECORD"],
    flowHeads: ["Öğrenci bağlamı", "LM Studio / alt. uç", "Güvenli kayıt"],
    flowBodies: ["Seviye, hedef ve etkin çalışma uygulama içinde derlenir.", "Önce yerel LM Studio; isteğe bağlı NVIDIA NIM veya özel OpenAI uyumlu uç. API anahtarı diske yazılmaz.", "Yalnızca süre, token sayısı ve durum tutulur; konuşma metni tutulmaz."],
    offlineLine: "Çevrimdışı çekirdek / Offline core / Offline-Kern — AI kapalıyken de tüm temel çalışma akışları kullanılabilir.",
    closeKicker: "TESLİME HAZIR · READY TO DELIVER · BEREIT ZUR AUSLIEFERUNG",
    closeTitle: "Hazır. Ready. Bereit.", closeWords: ["Hazır.", "Ready.", "Bereit."],
    closeSub: "Bağımsız Windows uygulaması, belgeler, testler ve sunum tek pakette.",
    metricWords: "160", metricTests: "88 / 88",
    metricWordsLabel: "benzersiz A1 kelime\nunique A1 words\neindeutige A1-Wörter",
    metricTestsLabel: "otomatik test geçti\nautomated tests passed\nautomatische Tests bestanden",
    metricTabsLabel: "öğrenme alanı\nlearning areas\nLernbereiche",
    deliveryLine: "EXE + source + docs + GitHub Releases + trilingual deck · EXE + kaynak + belgeler + GitHub Releases + üç dilli sunum",
    platformCaption: "Windows x64 · macOS arm64",
    platformLineTr: "Windows 10/11 (x64) + macOS (Apple Silicon) — İndirme: github.com/Azizsekerdil/GermanCourseAI/releases (v1.3.0) · MIT lisanslı",
    platformLineEn: "Windows 10/11 (x64) & macOS (Apple Silicon) — Download: GitHub Releases (v1.3.0)",
    macNote: "macOS paketi Apple Silicon (arm64) içindir ve notarize edilmemiştir; ilk açılışta sağ tık → Aç. / Not notarized; first launch: right-click → Open.",
    releaseUrl: "https://github.com/Azizsekerdil/GermanCourseAI/releases/tag/v1.3.0",
  },
  {
    name: "French Course AI", shortName: "French Course AI", pkg: "fca",
    output: path.join(ROOT, "FrenchCourseAI/docs/presentation/French-Course-AI-Trilingual.pptx"),
    icon: path.join(ROOT, "FrenchCourseAI/assets/app-final.png"),
    screenshot: path.join(ROOT, "FrenchCourseAI/docs/presentation/assets/french-course-ai-screenshot.jpg"),
    accent: "#FF6668", accentDark: "#B8323A", pale: "#FFE5E5",
    kicker: "OFFLINE-FIRST WINDOWS LANGUAGE LEARNING",
    titleLine: "Türkçe · English · Français",
    taglineTr: "Yerel, ölçülebilir Fransızca öğrenimi",
    taglineEn: "Local, measurable French learning",
    taglineTarget: "Un apprentissage local et mesurable du français",
    uiTitleTarget: "Apprendre sans friction",
    uiTitleTr: "Tek uygulama, üç arayüz",
    uiTitleEn: "One app, three interfaces",
    uiBodyTarget: "18 espaces relient révision, vocabulaire, dictionnaire trilingue FR-EN-TR, examen, grammaire et pratique dans un atelier Windows cohérent.",
    uiBodyTr: "Dil seçimi anında kaydedilir; uygulama çevrimdışı çalışmaya devam eder.",
    uiBodyEn: "The language choice persists instantly, and core learning stays available offline.",
    realCaption: "Gerçek EXE ekranı · Real executable · Application réelle",
    engineTitle: "A learning engine that remembers",
    engineSub: "Öğrenme motoru hatırlar · Le moteur d’apprentissage retient vos progrès",
    langs: ["Türkçe", "English", "Français"],
    engineHeads: ["Her gün doğru sıra", "Practice with evidence", "Les progrès restent locaux"],
    engineBodies: ["SM-2 ve Leitner, yeni ve gecikmiş kartları günlük bir sıraya dönüştürür.", "162 A1 entries, a 1,210-entry FR-EN-TR dictionary with selectable direction, strict accented answers, exams, favorites and mistakes share one SQLite record.", "Révisions, erreurs, favoris et examens sont enregistrés localement et restent explicables."],
    catalogLine: "Kaynak kataloğu / resource catalog / catalogue de ressources: Wikibooks · Tatoeba · LibriVox · Project Gutenberg",
    wikibooks: "https://en.wikibooks.org/wiki/French",
    labTitleTarget: "Le français mérite des outils précis",
    labTitleTr: "Fransızcaya özgü laboratuvar", labTitleEn: "A French-specific language lab",
    labExamples: ["l’école · les écoles", "é · è · ê · ç", "cœur · sœur · œuvre", "yeux → l’œil (m)"],
    labDescriptions: ["Artikel ve elision · articles and elision · articles et élision", "Aksan araması kontrollü · controlled accent search · recherche d’accents contrôlée", "œ aramada esnek, yanıtta kesin · flexible search, strict answer · recherche souple, réponse exacte", "Sözlük FR↔EN↔TR yön seçimli · dictionary FR/EN/TR with direction switch · dictionnaire FR/EN/TR à sens réglable"],
    privacyTitleTr: "AI isteğe bağlı; mahremiyet varsayılan",
    privacyTitleEn: "AI is optional; privacy is the default", privacyTitleTarget: "L’IA est facultative; la confidentialité est la règle",
    flowLabels: ["01 · CONTEXT", "02 · LOCAL MODEL", "03 · RECORD"],
    flowHeads: ["Öğrenci bağlamı", "LM Studio / alt. uç", "Güvenli kayıt"],
    flowBodies: ["Seviye, hedef ve etkin çalışma uygulama içinde derlenir.", "Önce yerel LM Studio; isteğe bağlı NVIDIA NIM veya özel OpenAI uyumlu uç. API anahtarı diske yazılmaz.", "Yalnızca süre, token sayısı ve durum tutulur; konuşma metni tutulmaz."],
    offlineLine: "Çevrimdışı çekirdek / Offline core / cœur hors ligne — AI kapalıyken de tüm temel çalışma akışları kullanılabilir.",
    closeKicker: "TESLİME HAZIR · READY TO DELIVER · PRÊT À LIVRER",
    closeTitle: "Hazır. Ready. Prêt.", closeWords: ["Hazır.", "Ready.", "Prêt."],
    closeSub: "Bağımsız Windows uygulaması, belgeler, testler ve sunum tek pakette.",
    metricWords: "162", metricTests: "90 / 90",
    metricWordsLabel: "benzersiz A1 kelime\nunique A1 words\nmots A1 uniques",
    metricTestsLabel: "otomatik test geçti\nautomated tests passed\ntests automatisés réussis",
    metricTabsLabel: "öğrenme alanı\nlearning areas\nespaces d’apprentissage",
    deliveryLine: "EXE + source + docs + private GitHub + trilingual deck · EXE + kaynak + belgeler + GitHub privé + sunum trilingue",
    platformCaption: "Windows x64 · macOS arm64",
    platformLineTr: "Windows 10/11 (x64) + macOS (Apple Silicon) — İndirme: github.com/Azizsekerdil/FrenchCourseAI/releases (v1.2.1) · (özel repo)",
    platformLineEn: "Windows 10/11 (x64) & macOS (Apple Silicon) — Download: GitHub Releases (v1.2.1)",
    macNote: "macOS paketi Apple Silicon (arm64) içindir ve notarize edilmemiştir; ilk açılışta sağ tık → Aç. / Not notarized; first launch: right-click → Open.",
    releaseUrl: "https://github.com/Azizsekerdil/FrenchCourseAI/releases/tag/v1.2.1",
  },
];

const only = process.env.ONLY_DECK;
for (const cfg of configs) {
  if (only && cfg.pkg !== only) continue;
  console.log(await buildDeck(cfg));
}
