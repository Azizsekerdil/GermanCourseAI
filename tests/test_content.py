from gca import content
from gca.seed_words import WORDS


def test_has_at_least_150_original_a1_words():
    assert len(WORDS) >= 150
    assert len({w["de"] for w in WORDS}) >= 150
    required = {"de", "tr", "en", "article", "plural", "part_of_speech", "example_de", "example_tr", "example_en", "frequency_rank", "deck", "audio"}
    assert all(required <= set(word) for word in WORDS)


def test_nouns_have_article_plural_and_natural_example():
    nouns = [w for w in WORDS if w["part_of_speech"] == "noun"]
    assert len(nouns) >= 90
    assert all(w["article"] in {"der", "die", "das"} and w["plural"] for w in nouns)
    assert all(w["de"] in w["example_de"] for w in nouns)


def test_orthography_covers_required_german_features():
    text = " ".join(" ".join(row) for row in content.ORTHOGRAPHY)
    for token in ("Ä", "Ö", "Ü", "ß", "Großschreibung", "ch", "sch", "sp/st", "Komposita", "Betonung"):
        assert token in text


def test_grammar_topics_cover_requirements():
    codes = {t["code"] for t in content.GRAMMAR_TOPICS}
    required = {"case.nom", "case.acc", "case.dat", "case.gen", "article.def", "article.indef", "noun.gender",
                "adjective.endings", "pron.personal", "pron.possessive", "verb.present", "verb.irregular",
                "verb.separable", "verb.modal", "syntax.v2", "syntax.subordinate", "tense.perfect",
                "tense.preterite", "prep.case", "comparison", "numbers", "time", "date"}
    assert required <= codes


def test_all_labs_generate_valid_exercises():
    for lab in ("grammar", "cases", "verbs", "syntax", "numbers", "orthography"):
        items = content.build(lab, 8)
        assert len(items) == 8
        assert all(item["answer"] in item["options"] and item["prompt"] for item in items)
    assert content.build("unknown", 3) == []


def test_resource_catalog_is_open_and_attributed():
    assert len(content.RESOURCES) >= 4
    assert all(r["license"] and r["attribution"] and r["url"].startswith("https://") for r in content.RESOURCES)
    assert all("CC" in r["license"] or "Public" in r["license"] or "public" in r["license"] for r in content.RESOURCES)
