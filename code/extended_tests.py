"""Three further tests on the audited values, all from data/sa_keu_audit.csv.

Relation (Kuminek G, Cao F, Bahia de Oliveira da Rocha A, Goncalves Cardoso S,
Rodriguez-Hornedo N. Adv Drug Deliv Rev 2016;101:143-166, DOI 10.1016/j.addr.2016.04.022):

  SR_cocrystal = SR_drug^(1/2)   for 1:1 cocrystals

A. DIRECT TEST on printed solubilization ratios only. Lipert MP, Roy L, Childs SL,
   Rodriguez-Hornedo N. J Pharm Sci 2015;104(12):4153-4163 prints, for danazol moving
   from pH 5.00 acetate buffer to FeSSIF, SR_drug = 766 +/- 80 together with
   SR_cocrystal = 23 +/- 3 (4-hydroxybenzoic acid) and 24 +/- 4 (vanillin). The first
   equality can therefore be tested without involving any solubility-advantage
   definition. All five numbers are read from the audit table (rows R050, R051, R062).

B. INVERSE INFERENCE. Where a cross-medium pair cannot be tested forward because no
   SR_drug is published for the solubilizing medium, invert the relation:

     SR_drug = (SA_reference / SA_solubilizing)^2

   Inverting one pair assumes the relation and so proves nothing. Inverting TWO
   independent cocrystals of the same drug in the same pair of media is a test, because
   both must return the same SR_drug. Intervals are propagated from the precision of the
   printed figures under two stated readings, because the sources do not state their
   precision. Inferred values are kept in their own field and are never pooled with
   printed or derived SR_drug values.

C. REPORTING COMPLETENESS. Each value is scored against those items of the proposed
   reporting standard that can be scored mechanically from the audit table. A field
   counts as reported only where the source printed it. Items turning on second-hand
   provenance and on eutectic composition are not scored mechanically; surfactant
   identity and concentration are conditional on the medium and are reported separately
   over micellar rows only.

No value in this script is entered by hand except the five printed solubilization ratios
and uncertainties of test A and the four printed advantages of test B, each of which is
also present in the audit table at the row ids named above.
"""
import csv, json, math, pathlib, statistics

ROOT = pathlib.Path(__file__).resolve().parent.parent
rows = list(csv.DictReader(open(ROOT / "data" / "sa_keu_audit.csv")))
out = {}

# --------------------------------------------------------------------------- A
SRd, SRd_u = 766.0, 80.0
pred = math.sqrt(SRd)
pred_lo, pred_hi = math.sqrt(SRd - SRd_u), math.sqrt(SRd + SRd_u)
A = {"test": "SR_cocrystal = SR_drug^(1/2) on printed solubilization ratios only",
     "source": "Lipert 2015 J Pharm Sci 104(12):4153-4163",
     "audit_rows_used": ["R062", "R050", "R051"],
     "SR_drug_printed": SRd, "SR_drug_uncertainty": SRd_u,
     "predicted_SR_cocrystal": round(pred, 2),
     "predicted_interval": [round(pred_lo, 2), round(pred_hi, 2)],
     "pairs": []}
for cof, val, unc in (("4-hydroxybenzoic acid", 23.0, 3.0), ("Vanillin", 24.0, 4.0)):
    lo, hi = val - unc, val + unc
    A["pairs"].append({"coformer": cof, "SR_cocrystal_printed": val, "uncertainty": unc,
                       "printed_interval": [lo, hi],
                       "relative_discrepancy_pct": round(100 * (pred - val) / val, 1),
                       "intervals_overlap": not (hi < pred_lo or lo > pred_hi)})
A["sign_of_discrepancy"] = ("prediction exceeds measurement for both pairs; this is the sign "
                            "expected when coformer solubilization (the epsilon correction of "
                            "the source relation) is not applied, as here")
out["A_direct_SR_test"] = A

# --------------------------------------------------------------------------- B
PAIRS = (("4-hydroxybenzoic acid", 770.0, 10.0, "R063", "R065"),
         ("Vanillin", 370.0, 6.0, "R064", "R066"))

def case(step_ref, step_sol, label):
    infs = []
    for cof, ref, sol, rid_ref, rid_sol in PAIRS:
        red = ref / sol
        lo = ((ref - step_ref / 2) / (sol + step_sol / 2)) ** 2
        hi = ((ref + step_ref / 2) / (sol - step_sol / 2)) ** 2
        infs.append({"coformer": cof, "audit_rows_used": [rid_ref, rid_sol],
                     "SA_reference": ref, "SA_solubilizing": sol,
                     "observed_reduction": round(red, 2),
                     "inferred_SR_drug": round(red ** 2),
                     "interval": [round(lo), round(hi)]})
    a, b = infs
    ov = not (a["interval"][1] < b["interval"][0] or b["interval"][1] < a["interval"][0])
    return {"precision_assumption": label, "inferences": infs, "intervals_overlap": ov,
            "gap_ratio": None if ov else round(max(a["interval"][0], b["interval"][0])
                                               / min(a["interval"][1], b["interval"][1]), 2)}

c_unit = case(1, 1, "every printed figure read to the nearest unit")
c_ten = case(10, 1, "figures carrying a trailing zero read to the nearest ten")
pts = [i["inferred_SR_drug"] for i in c_unit["inferences"]]
B = {"test": "inverse inference of an unreported SR_drug, cross-checked between two cocrystals",
     "drug": "Danazol",
     "reference_medium": "aqueous media (not further specified in the source)",
     "solubilizing_medium": "Tween 80 solution (concentration not printed in the source)",
     "source": "Kuminek 2016 Adv Drug Deliv Rev 101:143-166",
     "inferences": c_unit["inferences"],
     "precision_cases": [c_unit, c_ten],
     "cross_pair_consistency": {
         "point_inferences": pts,
         "ratio_of_point_inferences": round(max(pts) / min(pts), 2),
         "geometric_mean": round(math.sqrt(pts[0] * pts[1])),
         "nearest_unit_intervals_overlap": c_unit["intervals_overlap"],
         "nearest_unit_gap_ratio": c_unit["gap_ratio"],
         "nearest_ten_intervals_overlap": c_ten["intervals_overlap"],
         "nearest_ten_gap_ratio": c_ten["gap_ratio"]},
     "falsifiable_prediction": {
         "quantity": "SR_drug for danazol, Tween 80 solution relative to aqueous medium",
         "range": [min(i["interval"][0] for i in c_ten["inferences"]),
                   max(i["interval"][1] for i in c_ten["inferences"])],
         "central_value": round(math.sqrt(pts[0] * pts[1])),
         "condition": ("the Tween 80 concentration is not printed in the source, so the medium "
                       "must be specified before the prediction can be tested"),
         "comparison_to_printed_biorelevant_value": {
             "printed_SR_drug_FeSSIF": SRd,
             "ratio_range": [round(min(pts) / SRd, 1), round(max(pts) / SRd, 1)],
             "note": "arithmetic ratio only; no claim is made about physical plausibility"}}}
out["B_inverse_inference"] = B

# --------------------------------------------------------------------------- C
ABSENT = {"", "not printed", "not stated", "n/a", "not applicable", "none stated"}
def present(v):
    s = (v or "").strip().lower()
    return s not in ABSENT and not s.startswith("not printed")

FIELDS = {"1_definition": "definition_as_stated", "2_denominator": "denominator",
          "3_stoichiometry": "stoichiometry", "4_medium": "medium",
          "6_pH": "pH_as_printed", "7_temperature": "temperature_as_printed",
          "8_measured_or_derived": "measured_or_derived"}

src = {}
for r in rows:
    s = src.setdefault(r["source_short"], {"rows": 0, "hit": {k: 0 for k in FIELDS},
                                           "mic": 0, "mic_conc": 0, "SR_drug": False})
    s["rows"] += 1
    for k, col in FIELDS.items():
        if present(r[col]):
            s["hit"][k] += 1
    if r["medium_class"] in ("surfactant-micellar", "biorelevant-micellar"):
        s["mic"] += 1
        if present(r["surfactant_conc"]):
            s["mic_conc"] += 1
    if r["quantity"].strip() == "SR_drug":
        s["SR_drug"] = True

C = {"machine_scoreable_items": list(FIELDS),
     "items_not_machine_scoreable": ["5 (conditional on medium; reported separately)",
                                     "9 (second-hand provenance)",
                                     "10 (eutectic composition)"],
     "per_source": []}
for name, s in sorted(src.items(), key=lambda kv: -kv[1]["rows"]):
    frac = {k: round(v / s["rows"], 2) for k, v in s["hit"].items()}
    C["per_source"].append({"source": name, "rows": s["rows"], "item_fractions": frac,
                            "mean_completeness": round(statistics.mean(frac.values()), 2),
                            "micellar_rows": s["mic"],
                            "surfactant_concentration_reported": s["mic_conc"],
                            "prints_SR_drug": s["SR_drug"]})
C["n_sources"] = len(C["per_source"])
C["corpus_mean_completeness"] = round(
    statistics.mean(d["mean_completeness"] for d in C["per_source"]), 2)
C["micellar_rows_total"] = sum(d["micellar_rows"] for d in C["per_source"])
C["micellar_rows_with_concentration"] = sum(
    d["surfactant_concentration_reported"] for d in C["per_source"])
C["sources_printing_SR_drug"] = sum(1 for d in C["per_source"] if d["prints_SR_drug"])
out["C_reporting_completeness"] = C

(ROOT / "data" / "extended_results.json").write_text(json.dumps(out, indent=2))
print(json.dumps(out, indent=2))
