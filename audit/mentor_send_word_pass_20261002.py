"""Third mentor-send pass: word-by-word reading of the sealed QA02 manuscript.

Every sentence, caption, table cell and reference of the QA02 source was read
against the released aggregate report. One statement did not match Table 3 as a
reader would check it; nine wordings were ambiguous or used a term with another
meaning in calorimetry. Counted byte replacements only; no numbered equation,
table body, figure or number is changed.
"""
import hashlib
import json
import platform
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
QA02_MAIN = '52a7b267299a3999e1831a99aad3c95a101a0fab9f4761cbeef6f58dfbd3cc92'


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def replace(path, old, new, count=1):
    raw = path.read_bytes()
    found = raw.count(old.encode('utf-8'))
    assert found == count, (path.name, old[:70], found)
    path.write_bytes(raw.replace(old.encode('utf-8'), new.encode('utf-8')))


tex = ROOT / 'main.tex'
assert sha(tex) == QA02_MAIN, 'Run once, on the QA02 source'
EDITS = [
    ('deposited energy',
     'Table 3 lists +7.74% at 125-150 GeV, larger in magnitude than the quoted -7.65%; the quoted bin is largest only in standard-error units. Signs are -,+,-,+,-,+,+,+, which is mixed rather than alternating.',
     r"the largest binwise mean difference ($-7.65\%$ at 150--175\,GeV) is 2.0 standard errors; the alternating signs in",
     r"the two largest binwise mean differences ($+7.74\%$ at 125--150\,GeV and $-7.65\%$ at 150--175\,GeV) are 1.8 and 2.0 standard errors; the mixed signs in"),
    ('hit pattern',
     'The parenthesis followed the Geant4 value and could be read as Geant4 being narrower.',
     r"87.1\,mm for Geant4 (2.8\% narrower);",
     r"87.1\,mm for Geant4 (the generator is 2.8\% narrower);"),
    ('longitudinal figure caption',
     'Compensation has a specific meaning in hadron calorimetry (e/h response); the text elsewhere calls this effect cancellation.',
     r"deposits expose section-level compensation.",
     r"deposits expose section-level cancellation."),
    ('evaluation',
     'The run tag appeared here for the first time, before Appendix A identifies it as the analyzed checkpoint.',
     r"A separate pair-grouped monitor for \texttt{dicos-f-02}, epoch 90, records",
     r"A separate pair-grouped monitor of the same checkpoint (\texttt{dicos-f-02}, epoch 90) records"),
    ('evaluation',
     'The pronoun followed a sentence whose subject is the event masks.',
     r"but were not retained. It discounts empty-layer separations",
     r"but were not retained. The bound discounts empty-layer separations"),
    ('introduction',
     'Later can be read as a time; the observable is a layer depth and no timing is used.',
     r"the last deposit occurs later, more layers are skipped",
     r"the last deposit lies deeper, more layers are skipped"),
    ('limitations',
     'E denotes the incident energy in Eq. 1; the deposit symbol is Y. The established term is zero-threshold.',
     r"The strict $E>0$ hit pattern describes",
     r"The zero-threshold hit pattern describes"),
    ('hit pattern',
     'Summaries from the same summary.',
     r"Energy-weighted transverse summaries from the same evaluation summary differ",
     r"Energy-weighted transverse observables from the same evaluation summary differ"),
    ('evaluation',
     'Splits rows did not say what a row is or how it is split.',
     r"The three-seed classifier battery splits rows. Members",
     r"The three-seed classifier battery splits individual showers at random, not matched pairs. Members"),
    ('evaluation',
     'Edges join channels, not layers.',
     r"Graph edges join only the same or adjacent layers.",
     r"Graph edges join channels only within a layer or between adjacent layers."),
]
for _, _, old, new in EDITS:
    replace(tex, old, new)

checks = ROOT / 'scripts/mentor_send_checks.py'
replace(checks,
        "    assert round(largest['mean_difference_percent'], 2) == -7.65\n",
        "    assert round(largest['mean_difference_percent'], 2) == -7.65\n"
        "    # Both of the largest percentage differences are quoted with their error scales.\n"
        "    by_percent = sorted(rows, key=lambda row: abs(row['mean_difference_percent']), reverse=True)[:2]\n"
        "    assert [row['low'] for row in by_percent] == [125.0, 150.0]\n"
        "    assert round(by_percent[0]['mean_difference_percent'], 2) == 7.74\n"
        "    assert round(by_percent[0]['difference_over_independent_se'], 1) == 1.8\n"
        "    assert sorted(row['mean_difference_percent'] > 0 for row in rows) == [False] * 3 + [True] * 5\n")
replace(checks,
        "        'is 2.0 standard errors', 'do not establish an energy-dependent bias',\n",
        "        'are 1.8 and 2.0 standard errors', 'the mixed signs in', 'do not establish an energy-dependent bias',\n"
        r"        '(the generator is 2.8\\% narrower)', 'section-level cancellation'," + "\n"
        r"        'of the same checkpoint (\\texttt{dicos-f-02}, epoch 90)', 'The bound discounts empty-layer separations'," + "\n"
        "        'the last deposit lies deeper', 'The zero-threshold hit pattern describes',\n"
        "        'splits individual showers at random, not matched pairs',\n")
replace(checks,
        "    figures = (ROOT / 'scripts/reader_figures.py')",
        "    for superseded in ['the largest binwise mean difference', 'alternating signs', 'section-level compensation',\n"
        "                       'strict $E>0$', 'the last deposit occurs later', 'classifier battery splits rows']:\n"
        "        assert superseded not in tex, superseded\n"
        "    figures = (ROOT / 'scripts/reader_figures.py')")

NOTE = (" A word-by-word pre-send pass then corrected the binwise statement to quote both of the largest differences "
        "(1.8 and 2.0 standard errors) and made nine wording clarifications without changing any number.")
ANCHOR = "No event-level data, checkpoint, threshold scan or new evaluation was used."
for name in ['README.md', 'STATUS.md']:
    replace(ROOT / name, ANCHOR + " See `audit/mentor_send_response_20261002.md`.",
            ANCHOR + NOTE + " See `audit/mentor_send_response_20261002.md`.")

path = ROOT / 'audit/finalization_20260930.json'
data = json.loads(path.read_text(encoding='utf-8'))
data['current_main_tex_sha256'] = sha(tex)
path.write_text(json.dumps(data, indent=2) + '\n', encoding='utf-8')

response = ROOT / 'audit/mentor_send_response_20261002.json'
payload = json.loads(response.read_text(encoding='utf-8'))
payload['current_main_sha256'] = sha(tex)
payload['third_pass'] = {
    'created_utc': datetime.now(timezone.utc).isoformat(), 'qa02_main_sha256': QA02_MAIN,
    'method': 'All 14 pages of the QA02 PDF were read, then the full source was read word by word: every sentence, caption, table cell and bibliography entry. Each quoted number was recomputed from data/reports/dicos-f-02_epoch90.json by a separate script; the component bound, the three-layer independence example, the Table 1 and Table 3 differences, the Table 2 normalization and the Table 4 means were rechecked by hand.',
    'finding': 'All numbers, equations and tables agree with the released report. One sentence in Sec. 5.1 named -7.65% as the largest binwise mean difference while Table 3 lists +7.74%; it is largest only in standard-error units (2.0 against 1.8). Nine further wordings were ambiguous for a detector-physics reader.',
    'verified_without_change': [
        'Component bound: Q_gen >= 52.3407, Q_ref <= 21.8949, difference 30.4458 to 37.1372, 84.64% of 35.9703.',
        'Binwise independent-sample scale: -1.6, 0.1, -0.1, 1.8, -2.0, 1.5, 0.4, 1.0 standard errors; reference relative standard errors 2.7-3.4%.',
        'Section sums, layer-9 ratio (-8.64%), layers 57-64 energy (17.85 and 17.19 MeV), timing remainder (2,433 s), calibration weights (sum 9, bound ratio 16).',
        'Figure 4 illustrations: 9 active/span 10/G=1/R=2 and 8 active/span 12/G=4/R=4; panel (b) has three groups in four consecutive active layers.',
        'References: arXiv 2608.12795, 2512.20346, 2507.18811 and 2406.12877 resolve to the cited titles and authors; Crossref confirms 10.1016/j.nima.2025.170613, 10.1016/j.cpc.2025.109936 and 10.1007/s41781-025-00130-x.',
        'Cited design cuts: arXiv 2406.12877 states E > 0.5 MIP with 1 MIP = 0.5 MeV and t < 275 ns, and an iron/scintillator structure, as quoted in Sec. 6.2.',
    ],
    'layout_probe': 'Scratch-copy pdfLaTeX/Biber builds before and after: 14 pages, identical page breaks, no log warning. Page 7 gains one line inside its existing white space; no other page changes its line count.',
    'replacements': [{'section': section, 'reason': reason, 'old_sha256': hashlib.sha256(old.encode()).hexdigest(), 'new': new}
                     for section, reason, old, new in EDITS],
    'not_changed': [
        'Abstract and page-1 flow, every numbered equation, every table body and all four figures.',
        'Geant4 is cited where the transport is described (Sec. 2.1), not at its first mention; moving the citation would renumber every reference.',
        'No chi-square or other new statistic is added. The eight binwise values give 13.0 for 8 bins on the same independent-sample scale; it is recorded here only as a possible addition for the author to decide.',
    ],
    'environment': {'python': sys.version, 'platform': platform.platform()},
    'new_event_or_test_data_access': False, 'new_model_evaluation': False,
}
response.write_text(json.dumps(payload, indent=2) + '\n', encoding='utf-8')
with response.with_suffix('.md').open('a', encoding='utf-8', newline='\n') as handle:
    handle.write('\n## Third pass: word-by-word reading of QA02\n\n'
                 'The sealed QA02 manuscript was read in full, page by page and then word by word in source, and every quoted number was recomputed from the released report. '
                 'All numbers, equations and tables hold. Section 5.1 called -7.65% the largest binwise mean difference although Table 3 lists +7.74%; the sentence now quotes both with their error scales (1.8 and 2.0 standard errors) and says mixed rather than alternating signs. '
                 'Nine wordings were clarified: which sample has the narrower radial RMS, cancellation in place of compensation in the Figure 3 caption, the run tag introduced as the same checkpoint, an unclear pronoun, deeper in place of later, zero-threshold in place of a reused energy symbol, a repeated word, how the classifier battery splits showers, and what graph edges join. '
                 'No number, numbered equation, table body or figure changed, and the page breaks are identical. Reasons, hashes and the items verified without change are in the JSON twin.\n')
print(json.dumps({'source_sha256': sha(tex), 'replacements': len(EDITS)}, indent=2))
