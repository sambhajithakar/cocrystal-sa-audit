"""Quantitative analysis of the SA/K_eu provenance audit.

Every number this script prints is computed from sa_keu_audit.csv, whose every
row is a value copied verbatim from a published source. No value is imputed,
averaged across definition classes, or converted between definitions.
"""
import csv, json
from collections import defaultdict

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
out = {}

# --- 1. How much of the apparent "SA data" is actually usable ---
usable = [r for r in rows
          if r["quantity"] in ("SA", "solubility_ratio")
          and r["measured_or_derived"] == "measured"]
out["total_rows"] = len(rows)
out["rows_a_naive_scraper_would_take_as_SA"] = len(
    [r for r in rows if r["quantity"] in ("SA", "solubility_ratio", "SR_cocrystal_NOT_SA")])
out["rows_actually_measured_SA_or_ratio"] = len(usable)
out["rows_model_derived"] = len([r for r in rows if r["measured_or_derived"].startswith("MODEL")])
out["rows_third_party_provenance"] = len([r for r in rows if r["measured_or_derived"].startswith("third-party")])
out["rows_that_are_not_SA_at_all"] = len([r for r in rows if r["quantity"] == "SR_cocrystal_NOT_SA"])
all_classes = sorted({r["definition_class"] for r in rows})
# S1 (SR_drug) is a drug-only supporting quantity, not a cocrystal-vs-drug definition,
# and is counted separately so the headline count means one thing.
out["distinct_definition_classes"] = [c for c in all_classes if c != "S1"]
out["supporting_classes"] = [c for c in all_classes if c == "S1"]
out["distinct_medium_classes"] = sorted({r["medium_class"] for r in rows})
out["rows_with_no_stated_pH"] = len([r for r in rows
                                     if r["pH_as_printed"] in ("", "not stated",
                                                               "not printed in that sentence")])
out["rows_with_no_stated_temperature"] = len([r for r in rows
                                              if r["temperature_as_printed"] in ("", "not stated")])

# --- 2. Within-pair spread, computed ONLY inside one definition class ---
def numeric(r):
    """Return (lo, hi) for a row, or None. Ranges keep both ends."""
    if r["is_range"] == "TRUE":
        return float(r["value_min"]), float(r["value_max"])
    t = r["value_as_printed"].replace(" times", "").split("+/-")[0].strip()
    try:
        v = float(t)
    except ValueError:
        return None
    return v, v

spreads = []
groups = defaultdict(list)
for r in usable:
    g = (r["drug"], r["coformer"], r["stoichiometry"], r["definition_class"])
    n = numeric(r)
    if n:
        groups[g].append((n, r))
for g, vals in sorted(groups.items()):
    lo = min(v[0][0] for v in vals)
    hi = max(v[0][1] for v in vals)
    if lo > 0 and hi / lo > 1.0:
        spreads.append({
            "drug": g[0], "coformer": g[1], "stoich": g[2], "definition_class": g[3],
            "n_values": len(vals), "min": lo, "max": hi, "fold_spread": round(hi / lo, 1),
            "what_varies": sorted({v[1]["pH_as_printed"] for v in vals}) if len(
                {v[1]["pH_as_printed"] for v in vals}) > 1 else sorted(
                {v[1]["surfactant_conc"] or v[1]["medium"] for v in vals}),
            "source": vals[0][1]["source_short"],
        })
spreads.sort(key=lambda d: -d["fold_spread"])
out["within_pair_within_definition_spreads"] = spreads

# --- 3. Same pair, same paper, different reporting choice ---
cbz_nic = [r for r in usable if r["coformer"] == "Nicotinamide" and r["definition_class"] == "D5"]
water_row = [numeric(r)[0] for r in cbz_nic if r["medium_class"] == "neat-aqueous"]
out["CBZ_NIC_same_paper_eutectic_choice"] = {
    "values_in_neat_water": sorted(water_row),
    "fold_spread_from_reporting_choice_alone": round(max(water_row) / min(water_row), 2),
    "note": "Li 2013 prints both; the paper itself says the eutectic point 'was not a single point'.",
}

# --- 4. Same pair, same paper, buffer vs biorelevant medium ---
pairs = defaultdict(dict)
for r in usable:
    if r["definition_class"] == "D4":
        pairs[(r["drug"], r["coformer"])][r["medium_class"]] = numeric(r)[0]
out["buffer_vs_biorelevant_same_pair"] = [
    {"drug": k[0], "coformer": k[1], "buffer": v.get("neat-aqueous-buffer"),
     "FeSSIF": v.get("biorelevant-micellar"),
     "fold_difference": round(max(v.values()) / min(v.values()), 1)}
    for k, v in sorted(pairs.items()) if len(v) == 2]

# --- 5. The K_eu position ---
keu = [r for r in rows if r["quantity"] == "K_eu"]
out["K_eu_situation"] = {
    "verified_printed_numeric_K_eu_values_in_14_papers": len(keu),
    "values": [{"drug": r["drug"], "coformer": r["coformer"], "stoich": r["stoichiometry"],
                "K_eu": r["value_as_printed"], "definition_class": r["definition_class"]} for r in keu],
    "note": "1:1 and 2:1 K_eu are on different scales (SA^2 vs 0.5*(S_c/S_d)^3), so even these two "
            "cannot be placed on one axis. A regression target cannot be built from n=2 on two scales.",
}

json.dump(out, open(os.path.join(DATA, "audit_results.json"), "w"), indent=2)

# -------- report --------
print("=" * 72)
print("PROVENANCE AUDIT RESULTS")
print("=" * 72)
print(f"Rows in audit                                    : {out['total_rows']}")
print(f"Rows a naive scraper would read as 'SA'          : {out['rows_a_naive_scraper_would_take_as_SA']}")
print(f"  of which actually measured SA / ratio          : {out['rows_actually_measured_SA_or_ratio']}")
print(f"  of which MODEL-DERIVED, not measured           : {out['rows_model_derived']}")
print(f"  of which third-party (secondary provenance)    : {out['rows_third_party_provenance']}")
print(f"  of which not a drug-referenced ratio at all    : {out['rows_that_are_not_SA_at_all']}")
print(f"Cocrystal-quantity definition classes            : {len(out['distinct_definition_classes'])} {out['distinct_definition_classes']}")
print(f"Supporting classes (drug-only quantities)        : {len(out['supporting_classes'])} {out['supporting_classes']}")
print(f"Distinct medium classes                          : {len(out['distinct_medium_classes'])} {out['distinct_medium_classes']}")
print(f"Rows with no stated pH                           : {out['rows_with_no_stated_pH']}")
print(f"Rows with no stated temperature                  : {out['rows_with_no_stated_temperature']}")
print()
print("WITHIN-PAIR SPREAD (same pair, same definition class):")
for s in spreads:
    print(f"  {s['drug']:14s} + {s['coformer']:22s} {s['stoich']:4s} [{s['definition_class']}] "
          f"n={s['n_values']}  {s['min']:g} -> {s['max']:g}  = {s['fold_spread']}x")
print()
print("SAME PAIR, SAME PAPER, DIFFERENT EUTECTIC-POINT CHOICE:")
c = out["CBZ_NIC_same_paper_eutectic_choice"]
print(f"  Carbamazepine + Nicotinamide, neat water: {c['values_in_neat_water']} "
      f"= {c['fold_spread_from_reporting_choice_alone']}x from reporting choice alone")
print()
print("SAME PAIR, SAME PAPER, BUFFER vs BIORELEVANT MEDIUM:")
for b in out["buffer_vs_biorelevant_same_pair"]:
    print(f"  {b['drug']:14s} + {b['coformer']:16s} buffer {b['buffer']:g} vs FeSSIF {b['FeSSIF']:g} "
          f"= {b['fold_difference']}x")
print()
print("K_eu:")
print(f"  verified printed numeric values across 14 papers: "
      f"{out['K_eu_situation']['verified_printed_numeric_K_eu_values_in_14_papers']}")
for v in out["K_eu_situation"]["values"]:
    print(f"    {v['drug']} + {v['coformer']} {v['stoich']}: K_eu = {v['K_eu']} [{v['definition_class']}]")
print("=" * 72)
