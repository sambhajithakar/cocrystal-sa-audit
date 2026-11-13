# Eutectic constant (K_eu) literature extraction — working log

Started 10 November 2026. Purpose: build a curated, fully cited dataset of
published cocrystal eutectic constants and solubility advantages, because no
public compilation exists.

**Rule for this file: every number is copied exactly as printed in its source.
Nothing is rounded, converted, averaged, recomputed or read off a plotted curve.
Values that could not be verified verbatim are kept in a separate section and are
NOT dataset candidates until checked.**

---

## Definitions encountered (these differ, and must not be mixed)

- **Standard ratio**: K_eu = [coformer]_eu / [drug]_eu, analytical (total) molar
  concentrations at the eutectic point.
- **1:1 cocrystals**: K_eu = (S_cocrystal/S_drug)^2 = SA^2, so log K_eu = 2 log SA.
- **2:1 cocrystals**: K_eu = 0.5 (S_c/S_d)^3. **Not** SA^2 — 1:1 and 2:1 K_eu
  values therefore do not lie on one scale and must carry a stoichiometry flag.
- Transition thresholds: pH_max occurs at K_eu = 1 for 1:1, K_eu = 0.5 for 2:1.
  These are thresholds, not measurements, and are excluded from the dataset.

---

## Verified measured K_eu values

| Drug | Coformer | Stoich | K_eu | Medium | T | pH | Location | Source |
|---|---|---|---|---|---|---|---|---|
| Indomethacin | Saccharin | 1:1 | 642 | measured in Brij 99 / Myrj 52 / SLS solutions; text ties it to SA_aq = 25 at pH 2.1 with no drug solubilization | 25.0 ± 0.2 °C | 2.1 (0.2 M phosphate buffer) | Results, "Quantitative predictive model" subsection | Huang 2019 |
| Nevirapine | Saccharin | 2:1 | 0.4 | aqueous | 25 °C | not printed in that sentence | Results, pH_max paragraph | Kuminek 2016 |

**Open discrepancy, recorded not resolved:** Huang 2019 prints SA = 25 and
K_eu = 642, but SA^2 = 625. Both are recorded as printed. Do not recompute or
silently reconcile; this needs the publisher version to settle.

## Verified solubility advantage (SA) values

| Drug | Coformer | Stoich | SA | Definition | Medium | T | pH | Location | Source |
|---|---|---|---|---|---|---|---|---|---|
| Indomethacin | Saccharin | 1:1 | 25 | S_cocrystal/S_drug, molar | pH 2.1 buffer | — | 2.1 | Introduction ¶2; Results | Huang 2019 |
| Nevirapine | Maleic acid | 1:1 | 3 (pH 1), 20 (pH 2), 900 (pH 5) | S_cc/S_drug, eutectic-based equilibrium | aqueous | 25 °C | 1, 2, 5 | Results, after Table 2 | Kuminek 2016 |
| Nevirapine | Maleic acid | 1:1 | range 3.4–906 over pH 1–5 | S_cc/S_drug equilibrium calc | aqueous | 25 °C | 1–5 | Table 2 footnote d | Kuminek 2016 |
| Nevirapine | Saccharin | 2:1 | range 0.9–47 over pH 1–5 | S_cc/S_drug equilibrium calc | aqueous | 25 °C | 1–5 | Table 2 | Kuminek 2016 |
| Nevirapine | Salicylic acid | 2:1 | range 0.6–11 over pH 1–5 | S_cc/S_drug equilibrium calc | aqueous | 25 °C | 1–5 | Table 2 | Kuminek 2016 |

### Third-party values quoted inside Kuminek 2016 (originally Caira et al.)
Kept separate: these are not this paper's measurements, pH is unstated, and the
drug solubility used was at 37 °C.

| Drug | Coformer | Stoich | SA | Note |
|---|---|---|---|---|
| Nevirapine | Maleic acid | 1:1 | 5.3 | Table 2 col "pH ?", footnote e |
| Nevirapine | Saccharin | 2:1 | 1.4 | Table 2 footnote e |
| Nevirapine | Salicylic acid | 2:1 | 1.1 | Table 2 footnote e |

---

## NOT verified — must be checked against the source before any use

From Huang 2019, taken from a model summary of the latter half of the article
rather than from the text itself. **Do not treat as data.**
SA = 12 (Fig 9 section); SA = 10 (0.30 mM Brij 99); SA = 4; SA = 2 (7.78 mM
Brij 99); SA = 1 (transition point).

---

## Sources read

1. Huang Y, Kuminek G, Roy L, Cavanagh KL, Yin Q, Rodríguez-Hornedo N.
   "Cocrystal solubility advantage diagrams as a means to control dissolution,
   supersaturation and precipitation." *Mol Pharm* 2019, 16(9), 3887–3895.
   DOI 10.1021/acs.molpharmaceut.9b00501. PMID 31318567.
   *PMC copy is the NIHMS author manuscript — verify against publisher version.*
2. Kuminek G, Rodríguez-Hornedo N, Siedler S, Rocha HVA, Cuffini SL, Cardoso SG.
   "How cocrystals of weakly basic drugs and acidic coformers might modulate
   solubility and stability." *Chem Commun* 2016, 52(34), 5832–5835.
   DOI 10.1039/c6cc00898d. PMID 27042997. *Author manuscript copy.*

## Sources attempted and not obtained

- Good DJ, PhD thesis 2010, University of Michigan, "Pharmaceutical Cocrystal
  Eutectic Analysis". Handle https://deepblue.lib.umich.edu/handle/2027.42/76018
  Abstract states **"More than forty eutectic constants are presented"** —
  by far the largest known single source. The landing page exposed no PDF link
  to the fetcher. **Highest-value outstanding target.**
- Good DJ & Rodríguez-Hornedo N, "Cocrystal Eutectic Constants and Prediction of
  Solubility Behavior", *Cryst Growth Des* 2010, 10, 1028–1032,
  DOI 10.1021/cg901232h — ACS paywall.
- Good DJ & Rodríguez-Hornedo N, "Solubility Advantage of Pharmaceutical
  Cocrystals", *Cryst Growth Des* 2009, 9, 2252–2264 — ACS paywall.
- PMC6261521 (Cocrystals Mitigate Negative Effects of High pH) — reCAPTCHA block.

## Known hazards for merging
1. 1:1 and 2:1 K_eu are on different scales — always carry stoichiometry.
2. Surfactant/micellar and biorelevant media are not comparable to plain aqueous.
3. Author manuscripts may differ from publisher versions.
4. Salt vs cocrystal and hydrate vs anhydrate confusion appears in this literature.
5. Literature-quoted values inside a paper must stay separate from its own measurements.

---

## Round 2 — four further PMC papers (added 2026-11-10)

Three of four read verbatim. **Printed numeric K_eu values found: ZERO.**

| Paper | Citation | K_eu printed | SA / solubility-ratio printed |
|---|---|---|---|
| PMC5732061 | Cao F, Amidon GL, Rodriguez-Hornedo N, Amidon GE. Mechanistic basis of cocrystal dissolution advantage. J Pharm Sci 2018;107(1):380-389. DOI 10.1016/j.xphs.2017.09.014 | 0 (plotted only, Fig 1b/2b — NOT digitized) | 11 (Tables 1-2), all **theoretical predictions**, all < 1 |
| PMC4706795 | Lipert MP, Roy L, Childs SL, Rodriguez-Hornedo N. Cocrystal solubilization in biorelevant media and its prediction from drug solubilization. J Pharm Sci 2015;104(12):4153-4163. DOI 10.1002/jps.24640 | 0 (K_eu never used) | 4 (text): CBZ-SLC 12x buffer / 9x FeSSIF; DNZ-VAN 393x buffer / 13x FeSSIF |
| PMC8876770 | NOT READ — host returned reCAPTCHA challenge page. Values unknown. | — | — |
| PMC3873677 | Li M, Qiao N, Wang K. Pharmaceutics 2013;5(4):508-524. DOI 10.3390/pharmaceutics5040508 | 0 (K_eu never used) | 17 distinct Scc/S_CBZ,aq values (Table 2 + Sec 3.3): water 319; SLS series 302/319/332/340/333/348/319; Tween 80 series 315/319/335/334/306/296/294; text 130; literature 152 |

### Merge hazards recorded (do NOT merge these three ratio types)
1. **PMC5732061** SA = Scc/S_R where S_R is the drug solubility in the *same surfactant medium*, computed from its Eq. 3. These are **predictions, not measurements**, and all are < 1 ("no solubility advantage").
2. **PMC4706795** ratio = cocrystal/drug solubility *in the same medium* (buffer or FeSSIF). No formula printed; source data in unread Supporting Information. The "393 times DNZ-VAN in buffer" comparator is not spelled out in the sentence — flagged, not used.
3. **PMC3873677** ratio = Scc/S_CBZ,aq — denominator is the **aqueous** drug solubility, not the drug solubility in the surfactant medium. Therefore **not comparable** to 1 or 2.
4. PMC4706795 Table 2 additionally prints SR_cocrystal,exp (CBZ-SAC 1.03; CBZ-SLC 1.33; CBZ-4ABA(H) 1.49 (2:1); PXC-SAC 1.40; IND-SAC 4.5; DNZ-HBA 23; DNZ-VAN 24). These are **solubilization ratios, not SA** — must not enter an SA column.
5. PMC3873677 Sec 3.1: solid residue "totally converted to CBZ DH"; the eutectic point "was not a single point". The 319/130/152 values depend on which eutectic point is chosen.
6. PMC3873677 internal discrepancy: Table 2 prints SLS 6.7 mM, Sec 2.2.1 says 6.9 mM. Table value used; discrepancy flagged.
7. pH coverage is uneven: PMC5732061 gives bulk and interfacial pH per row; PMC4706795 gives equilibrium pH 4.29-5.00; PMC3873677 states no pH at all.

### Running tally after round 2
- Papers surveyed: 14. **Verified printed numeric K_eu values: 2** (IND-SAC 1:1 = 642; NVP-SAC 2:1 = 0.4).
- Verified printed SA / solubility-ratio values: 36+, but spread over **at least four mutually incompatible definitions** and three medium classes (neat aqueous, ionic surfactant micellar, biorelevant FeSSIF).
- **Conclusion for study design: a K_eu regression dataset cannot be assembled from open literature. The definitional heterogeneity of published SA values is itself the finding.**

---

## Round 3 — the Good 2010 thesis (2026-11-10)

**Still not obtained.** Full citation now confirmed from the Deep Blue landing page:

> Good, David John (2010). *Pharmaceutical Cocrystal Eutectic Analysis: Study of Thermodynamic
> Stability, Solubility, and Phase Behavior.* PhD thesis, University of Michigan.
> Handle https://deepblue.lib.umich.edu/handle/2027.42/76018

Routes tried and their outcomes:
- `deepblue.lib.umich.edu` via the container's HTTPS proxy: **CONNECT tunnel failed, 403** — the
  environment's network policy does not allow this host.
- Landing page via WebFetch: HTTP 200, 4,024 characters, **exposes no bitstream or PDF link**.
- DSpace REST / discover API paths, and the bitstream path: client errors (permanent).
- core.ac.uk search: robots-disallowed.

### A definitional find that matters more than the missing values

The landing page states verbatim that the thesis concerns

> "Cocrystal eutectic constants (Keu), the ratio of solution **activities** of cocrystal
> components at the eutectic"

and that **"More than forty eutectic constants are presented."**

**This is a fifth, previously unrecorded incompatibility.** The thesis defines K_eu as a ratio of
solution *activities*; Kuminek 2016 and Huang 2019 define and use it as a ratio of *total
analytical molar concentrations*. Those two coincide only in the ideal-dilute limit with no
ionisation and no micellar partitioning — i.e. almost never for a BCS II/IV weak base or weak acid
in a surfactant or biorelevant medium, which is exactly the regime of interest. So even if the
forty-plus thesis values were obtained, they could **not** be pooled with the concentration-ratio
K_eu values without an activity-coefficient correction that none of these papers reports.

**Consequence for study design:** the audit paper's thesis strengthens rather than weakens. The
K_eu literature is not merely sparse; its two largest sources are on different physical scales.

---

## Round 4 — a re-read of Kuminek 2016 §4.2 (2026-11-10)

Triggered by a structure-sourcing question, not by a new search: while confirming which isomer
"HBA" denotes, the §4.2 paragraph was re-read in full. It prints **four solubility advantages that
earlier rounds did not extract**, although the carbamazepine value in the same paragraph was taken.
This is recorded as an extraction miss, not as a new source.

| Drug | Coformer | Stoich | SA | Medium | Row |
|---|---|---|---|---|---|
| Danazol | 4-hydroxybenzoic acid | 1:1 | 770 | aqueous media (not further specified) | R063 |
| Danazol | Vanillin | 1:1 | 370 | aqueous media (not further specified) | R064 |
| Danazol | 4-hydroxybenzoic acid | 1:1 | 10 | Tween 80 solution (concentration not printed) | R065 |
| Danazol | Vanillin | 1:1 | 6 | Tween 80 solution (concentration not printed) | R066 |

Source sentence, verbatim: "Danazol cocrystals, danazol-4-hydroxybenzoic acid (DNZ-HBA) and
danazol-vanillin (DNZ-VAN) are much more soluble than danazol (DNZ) in aqueous media with SA of
770 and 370 for 4-hydroxybenzoic acid (HBA) and vanillin (VAN) cocrystals, but this SA is
decreased to 10 and 6 in solution of Tween 80."

Three consequences:

1. **The isomer is now sourced.** This sentence is the only place in the material read that names
   HBA as 4-hydroxybenzoic acid; the measurement source (Lipert 2015) writes only HBA. The audit
   keeps the measurement source's label and records the assignment with its source.
2. **A cross-source discrepancy.** Kuminek 2016 prints SA = 370 for DNZ-VAN in aqueous media;
   Lipert 2015 prints 393 in pH 5.00 acetate buffer. Possibly the same measurement; neither source
   says so, and the stated media differ. Both recorded as printed, not reconciled.
3. **Two cross-medium pairs that cannot be harmonized.** Both Tween 80 values pair with an aqueous
   value for the same 1:1 cocrystal, so both are genuine cross-medium comparisons — and neither can
   be tested against SR_drug^(1/2), because no solubilization ratio for danazol in Tween 80 is
   printed anywhere in the material read. The harmonization test therefore stands at six published
   cross-medium pairs: two harmonizable from a printed SR_drug, two from a derived one, two not at
   all. The two that fail do so for want of a reported number, not for want of a relation.

Values present in the same paragraph and deliberately **not** extracted: SA = 26 and 6 for
pterostilbene–caffeine and pterostilbene–piperazine, falling to 0.3 and 0.2 in lipids.
Pterostilbene has no BCS classification and is outside the scope; no class is assigned to it here.

### Structure sourcing (same date)

Every drug and coformer structure was obtained twice and required to agree on the standard
InChIKey: ChEMBL release 34 and OPSIN 2.9.0 run offline. All seven coformers agree across both.
OPSIN cannot parse the five invented drug names, so for those ChEMBL is the sole source and the
table says so. Maleic acid and 4-hydroxybenzoic acid are not retrievable from ChEMBL by name and
were located by exact-structure search on the OPSIN output (CHEMBL539648 and CHEMBL441343, the
latter carrying the ChEMBL preferred name PARABEN). Network routes to PubChem, the NCI resolver
and UniChem were all refused by the environment's proxy; this is why a local parser was used
rather than a web lookup. No structure was written from memory.
