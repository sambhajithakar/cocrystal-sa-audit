"""Harmonization test: can published cross-medium SA values be reconciled using the
field's own published relation?

Relation (Kuminek G, Cao F, Bahia de Oliveira da Rocha A, Goncalves Cardoso S,
Rodriguez-Hornedo N. Adv Drug Deliv Rev 2016;101:143-166, DOI 10.1016/j.addr.2016.04.022):

  SR_cocrystal = SR_drug^(1/2)              for 1:1 cocrystals
  SR_cocrystal = SR_drug^(2/3)              for 2:1 cocrystals
  log(SA) vs log(SR_drug) has slope -1/2    for 1:1 cocrystals

Hence, for a 1:1 cocrystal moving from a reference medium to a solubilizing medium:

  SA_reference / SA_solubilizing  =  SR_drug / SR_cocrystal  =  SR_drug^(1/2)

This script compares that PREDICTED reduction factor with the reduction factor
OBSERVED in the published SA pairs. Every input is a printed value from the audit
table; the only derived quantity is SR_drug where it is not printed, and that
derivation is labelled.
"""
import csv, json

import os

def _data_dir():
    """Locate sa_keu_audit.csv.

    The working tree keeps it beside these scripts; the public deposit keeps it in data/
    while the scripts sit in code/. Both layouts, and a plain current directory, are
    accepted so that the script runs unmodified wherever it is unpacked.
    """
    here = os.path.dirname(os.path.abspath(__file__))
    for cand in (os.getcwd(), here,
                 os.path.join(here, "..", "data"),
                 os.path.join(here, "data")):
        if os.path.isfile(os.path.join(cand, "sa_keu_audit.csv")):
            return cand
    raise SystemExit("sa_keu_audit.csv not found next to this script, in ./ or in ../data")

DATA = _data_dir()

rows = list(csv.DictReader(open(os.path.join(DATA, "sa_keu_audit.csv"))))

def val(s):
    return float(s.split("+/-")[0].replace(" times", "").strip())

# A solubilization ratio is specific to the solubilizing medium it was measured in, so
# both lookups are keyed by that medium class. Keying by drug alone would let a FeSSIF
# SR_drug be applied to a Tween 80 SA pair, which is not the same quantity.
SR_drug_printed = {(r["drug"], r["medium_class"]): val(r["value_as_printed"])
                   for r in rows if r["quantity"] == "SR_drug"}
SR_cc_printed = {(r["drug"], r["coformer"], r["medium_class"]): val(r["value_as_printed"])
                 for r in rows if r["quantity"] == "SR_cocrystal_NOT_SA"}

REFERENCE = ("neat-aqueous", "neat-aqueous-buffer")
SOLUBILIZING = ("surfactant-micellar", "biorelevant-micellar")

# published SA pairs: a reference medium and a solubilizing medium for the same pair,
# same stoichiometry (1:1) and same definition class
pairs = {}
for r in rows:
    if r["quantity"] != "SA" or r["stoichiometry"] != "1:1":
        continue
    if r["medium_class"] not in REFERENCE + SOLUBILIZING:
        continue
    # A row printed as a range cannot enter a single-value comparison, and §2.3
    # forbids collapsing it to a midpoint, so ranges are skipped rather than averaged.
    if r["is_range"].strip().lower() in ("yes", "true"):
        continue
    k = (r["drug"], r["coformer"], r["definition_class"])
    pairs.setdefault(k, {})[r["medium_class"]] = (val(r["value_as_printed"]), r["source_short"])

out = []
for (drug, cf, dc), v in sorted(pairs.items()):
    ref = [m for m in REFERENCE if m in v]
    sol = [m for m in SOLUBILIZING if m in v]
    if not ref or not sol:
        continue
    ref_m, sol_m = ref[0], sol[0]
    sa_ref = v[ref_m][0]
    sa_sol = v[sol_m][0]
    observed = sa_ref / sa_sol

    rec = {"drug": drug, "coformer": cf, "definition_class": dc,
           "reference_medium_class": ref_m, "solubilizing_medium_class": sol_m,
           "SA_reference": sa_ref, "SA_solubilizing": sa_sol,
           "observed_reduction": round(observed, 2),
           "SA_source": v[ref_m][1]}

    if (drug, sol_m) in SR_drug_printed:
        sr_drug, sr_src = SR_drug_printed[(drug, sol_m)], "printed"
    elif (drug, cf, sol_m) in SR_cc_printed:
        # derive SR_drug from the printed SR_cocrystal via SR_cc = SR_drug^(1/2)
        sr_drug = SR_cc_printed[(drug, cf, sol_m)] ** 2
        sr_src = "DERIVED from printed SR_cocrystal"
    else:
        rec.update({"SR_drug": None, "SR_drug_provenance": "NOT AVAILABLE",
                    "predicted_reduction": None, "relative_discrepancy_pct": None,
                    "verdict": "CANNOT BE HARMONIZED - no solubilization ratio is "
                               "published for this drug in this medium"})
        out.append(rec)
        continue

    predicted = sr_drug ** 0.5
    disc = abs(predicted - observed) / observed * 100.0
    rec.update({"SR_drug": round(sr_drug, 2), "SR_drug_provenance": sr_src,
                "predicted_reduction": round(predicted, 2),
                "relative_discrepancy_pct": round(disc, 1),
                "verdict": "harmonizable"})
    out.append(rec)

json.dump(out, open(os.path.join(DATA, "harmonization_results.json"), "w"), indent=2)

SHORT = {"neat-aqueous": "aq", "neat-aqueous-buffer": "buf",
         "surfactant-micellar": "surf", "biorelevant-micellar": "FeSSIF"}

print("=" * 100)
print("HARMONIZATION TEST  (1:1 cocrystals, a reference medium against a solubilizing medium)")
print("predicted reduction = SR_drug^(1/2)   [Kuminek 2016, Adv Drug Deliv Rev 101:143-166]")
print("=" * 100)
hdr = (f"{'pair':34s} {'media':>11s} {'SA_ref':>7s} {'SA_sol':>7s} {'obs':>7s} "
       f"{'SR_drug':>8s} {'pred':>6s} {'disc%':>6s}")
print(hdr); print("-" * 100)
for o in out:
    pair = f"{o['drug']} + {o['coformer']}"
    media = f"{SHORT[o['reference_medium_class']]}/{SHORT[o['solubilizing_medium_class']]}"
    head = (f"{pair:34s} {media:>11s} {o['SA_reference']:7g} {o['SA_solubilizing']:7g} "
            f"{o['observed_reduction']:7g} ")
    if o["predicted_reduction"] is None:
        print(head + f"{'n/a':>8s} {'n/a':>6s} {'n/a':>6s}   <- NOT HARMONIZABLE")
    else:
        print(head + f"{o['SR_drug']:8g} {o['predicted_reduction']:6g} "
              f"{o['relative_discrepancy_pct']:6g}   ({o['SR_drug_provenance']})")
print("-" * 100)
ok = [o for o in out if o["relative_discrepancy_pct"] is not None]
printed = [o for o in ok if o["SR_drug_provenance"] == "printed"]
derived = [o for o in ok if o["SR_drug_provenance"].startswith("DERIVED")]
print(f"pairs with a published cross-medium SA pair        : {len(out)}")
print(f"  harmonizable with a PRINTED SR_drug            : {len(printed)}"
      + (f"  -> discrepancy {min(o['relative_discrepancy_pct'] for o in printed)}"
         f"-{max(o['relative_discrepancy_pct'] for o in printed)}%" if printed else ""))
print(f"  harmonizable only with a DERIVED SR_drug       : {len(derived)}"
      + (f"  -> discrepancy {min(o['relative_discrepancy_pct'] for o in derived)}"
         f"-{max(o['relative_discrepancy_pct'] for o in derived)}%" if derived else ""))
print(f"  NOT harmonizable (no SR_drug for that medium)  : {len(out) - len(ok)}")
for o in out:
    if o["relative_discrepancy_pct"] is None:
        print(f"      {o['drug']} + {o['coformer']}  "
              f"({SHORT[o['reference_medium_class']]} vs {SHORT[o['solubilizing_medium_class']]})")
print("=" * 100)
