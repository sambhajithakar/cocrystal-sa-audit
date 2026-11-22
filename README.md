# Cocrystal solubility-advantage provenance audit

A provenance-level audit of published cocrystal solubility-advantage, eutectic-constant,
solubilization-ratio and related values for drugs whose development is solubility-limited,
together with the code that reproduces every reported result.

**Every value in `data/sa_keu_audit.csv` is copied verbatim from a published source.** Nothing is
rounded, converted, averaged, recomputed, or read off a plotted curve. Each row carries its own
definition, denominator, medium, surfactant, pH, temperature, a measured-or-model-derived flag,
and the location in the source at which it can be re-checked.

## Contents

```
data/
  sa_keu_audit.csv          66 rows, 25 provenance columns
  audit_results.json        output of code/analyze_audit.py
  harmonization_results.json output of code/harmonization_test.py
  smiles.csv                structures of all 12 compounds, from two independent sources
code/
  analyze_audit.py          composition, within-pair spread, K_eu position
  harmonization_test.py     cross-medium harmonization using SR_drug
  make_figures.py           both figures, from the outputs above
figures/
  figure1_data_model.pdf    the medium- and pH-resolved data model
  figure2_harmonization.pdf observed vs predicted cross-medium reduction
sources/
  kuminek2016_verbatim_quotes.md  verbatim definitions and relations relied on
  extraction-log.md               the full extraction record, including sources not obtained
```

## Reproducing

```
python3 code/analyze_audit.py          # run from data/'s parent, or adjust paths
python3 code/harmonization_test.py
python3 code/make_figures.py
```

Requires Python 3 and, for the figures, matplotlib. No other dependency.

## The definition classes

Values are grouped only where the source's own definition, denominator and measured-or-derived
status all agree. Twelve classes emerged for cocrystal quantities, plus one supporting class for
the drug-only solubilization ratio. **Classes are never pooled.** Classes suffixed `x` hold values
a source quotes from another study and carry secondary provenance. `D6` (cocrystal solubilization
ratio) and `D9` (peak supersaturation) are *not* solubility advantages and are recorded only
because they appear beside solubility advantages in the same tables.

## Known discrepancies

Recorded, not reconciled. See the `notes` column of each affected row and `sources/extraction-log.md`:
one source prints SA = 25 and K_eu = 642 for the same 1:1 cocrystal where K_eu = SA² gives 625;
one prints two different surfactant concentrations for the same table row; one reports the same
pair in neat water as both 319 and 130 depending on the eutectic composition chosen.

## Sources not obtained

Three publisher-paywalled papers and one repository-hosted thesis could not be read. They are
listed with the outcome of each retrieval attempt in `sources/extraction-log.md`, so that the
negative result is reproducible.

## Licence

Released under the MIT licence; see `LICENSE`.

## Citation

Thakar, S. B.; Ghorpade, P. N. *Cocrystal solubility-advantage provenance audit.*
GitHub repository, 2026. https://github.com/sambhajithakar/cocrystal-sa-audit

The article reporting this audit is under consideration; its citation will be added here
on acceptance. This deposit is journal-neutral by design and names no journal.
