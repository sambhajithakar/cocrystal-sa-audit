"""Generate the manuscript figures from the audit outputs.

Figure 1: the medium- and pH-resolved data model (schema).
Figure 2: observed vs predicted cross-medium reduction factor (the harmonization result).

Both are vector (PDF) plus a 600 dpi PNG for convenience. Print-targeted: no dark mode,
colour-blind-safe two-colour scheme, greyscale-distinguishable by marker fill as well as hue,
no rainbow, no dual axis.
"""
import json, os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

HERE = os.path.dirname(os.path.abspath(__file__))
# Figures are written to the repository's figures/ directory, where the deposit keeps them.
FIGDIR = os.path.join(HERE, "..", "figures")
os.makedirs(FIGDIR, exist_ok=True)

def _find_inputs():
    """Locate the analysis outputs.

    The working tree keeps them in ../audit; the public deposit keeps them in ../data.
    Both layouts, and a plain current directory, are accepted so that the script runs
    unmodified wherever it is unpacked.
    """
    for cand in (os.path.join(HERE, "..", "audit"),
                 os.path.join(HERE, "..", "data"),
                 os.path.join(HERE, "data"),
                 os.getcwd()):
        if os.path.isfile(os.path.join(cand, "harmonization_results.json")):
            return cand
    raise SystemExit(
        "harmonization_results.json not found. Run analyze_audit.py and "
        "harmonization_test.py first, then run this script from the directory holding "
        "them or from its sibling figures/ directory.")

AUDIT = _find_inputs()

# Lettering follows the journal's graphics appendix: a sans-serif face, type
# that is still legible when the figure is reduced to its column width, and no
# line thinner than 0.5 point.
plt.rcParams.update({
    "font.family": "sans-serif",
    "font.sans-serif": ["DejaVu Sans"],
    "font.size": 9,
    "axes.labelsize": 9,
    "axes.titlesize": 9,
    "xtick.labelsize": 8.5,
    "ytick.labelsize": 8.5,
    "legend.fontsize": 8.5,
    "axes.linewidth": 0.9,
    "xtick.major.width": 0.9,
    "ytick.major.width": 0.9,
    "savefig.bbox": "tight",
    "savefig.pad_inches": 0.02,
    "pdf.fonttype": 42,
})

INK      = "#1a1a1a"
MUTED    = "#555555"
BLUE     = "#1f5c8b"   # printed SR_drug
AMBER    = "#a66212"   # derived SR_drug
PANEL    = "#f2f2f2"

# ----------------------------------------------------------------- Figure 2
res = json.load(open(os.path.join(AUDIT, "harmonization_results.json")))
pts = [r for r in res if r["predicted_reduction"] is not None]
# Pairs with a published cross-medium SA pair but no published solubilization ratio for the
# drug in that medium have an observed reduction and no predicted one. They cannot be given a
# position on these axes, so they are stated in the corner rather than placed at a made-up y.
nopred = [r for r in res if r["predicted_reduction"] is None]

fig, ax = plt.subplots(figsize=(5.0, 4.3))

lo, hi = 1.15, 45.0
ax.plot([lo, hi], [lo, hi], ls="--", lw=0.8, color=MUTED, zorder=1)
ax.text(6.2, 7.6, "identity", fontsize=6.5, color=MUTED,
        ha="center", va="bottom", rotation=41, rotation_mode="anchor")

for r in pts:
    printed = r["SR_drug_provenance"] == "printed"
    col = BLUE if printed else AMBER
    ax.plot(r["observed_reduction"], r["predicted_reduction"],
            marker="o", ms=5.5, mew=1.1,
            mfc=col if printed else "white", mec=col,
            ls="none", zorder=3)

lab = {
    ("Carbamazepine", "Salicylic acid"): ("CBZ–SLC", 15, 18, "left"),
    ("Danazol", "Vanillin"):             ("DNZ–VAN", -10, 4, "right"),
    ("Piroxicam", "Saccharin"):          ("PXC–SAC", 17, 2, "left"),
    ("Indomethacin", "Saccharin"):       ("IND–SAC", -11, -8, "right"),
}
for r in pts:
    t, dx, dy, ha = lab[(r["drug"], r["coformer"])]
    ax.annotate(f"{t}\n{r['relative_discrepancy_pct']}%",
                (r["observed_reduction"], r["predicted_reduction"]),
                textcoords="offset points", xytext=(dx, dy),
                fontsize=6.5, color=INK, ha=ha, va="center", linespacing=1.25)

ax.set_xscale("log"); ax.set_yscale("log")
ax.set_xlim(lo, hi); ax.set_ylim(lo, hi)
from matplotlib.ticker import FixedLocator, FixedFormatter, NullLocator, NullFormatter
TICKS = [1.5, 2, 3, 5, 10, 20, 40]
TLAB = ["1.5", "2", "3", "5", "10", "20", "40"]
for axis in (ax.xaxis, ax.yaxis):
    axis.set_major_locator(FixedLocator(TICKS))
    axis.set_major_formatter(FixedFormatter(TLAB))
    axis.set_minor_locator(NullLocator())
    axis.set_minor_formatter(NullFormatter())
ax.set_xlabel("observed reduction, SA$_{\\mathrm{reference}}$ / SA$_{\\mathrm{solubilizing}}$")
ax.set_ylabel("predicted reduction, SR$_{\\mathrm{drug}}^{1/2}$")
ax.set_aspect("equal")
for sp in ("top", "right"):
    ax.spines[sp].set_visible(False)
ax.grid(True, which="major", lw=0.35, color="#dddddd", zorder=0)
ax.set_axisbelow(True)

h = [plt.Line2D([], [], marker="o", ls="none", ms=5.5, mew=1.1, mfc=BLUE, mec=BLUE,
                label="SR$_{\\mathrm{drug}}$ printed"),
     plt.Line2D([], [], marker="o", ls="none", ms=5.5, mew=1.1, mfc="white", mec=AMBER,
                label="SR$_{\\mathrm{drug}}$ derived")]
ax.legend(handles=h, loc="upper left", frameon=False, handletextpad=0.4,
          borderaxespad=0.2, labelspacing=0.35)

# the pairs that cannot be plotted, named in the empty lower-right corner
if nopred:
    names = {("Danazol", "4-hydroxybenzoic acid"): "DNZ\u2013HBA",
             ("Danazol", "Vanillin"): "DNZ\u2013VAN"}
    items = ", ".join(f"{names.get((r['drug'], r['coformer']), r['drug'])} {round(r['observed_reduction']):g}\u00d7"
                      for r in nopred)
    # These pairs have an observed value and no predicted one, so there is no honest position
    # for them on these axes. They are named in the caption rather than drawn on the artwork.
    print("  caption must state: not plottable (no SR_drug for that medium):", items)

fig.savefig(os.path.join(FIGDIR, "figure2_harmonization.pdf"))
fig.savefig(os.path.join(FIGDIR, "figure2_harmonization.png"), dpi=600)
plt.close(fig)

# ----------------------------------------------------------------- Figure 1
fig, ax = plt.subplots(figsize=(6.9, 3.4))
ax.set_xlim(0, 100); ax.set_ylim(0, 46); ax.axis("off")

def box(x, y, w, h, title, lines, edge=INK, face="white", lw=0.8, ls="-"):
    ax.add_patch(FancyBboxPatch((x, y), w, h,
        boxstyle="round,pad=0.6,rounding_size=1.2",
        linewidth=lw, edgecolor=edge, facecolor=face, linestyle=ls, zorder=2))
    ax.text(x + w / 2, y + h - 2.6, title, ha="center", va="top",
            fontsize=8, fontweight="bold", color=INK, zorder=3)
    for i, t in enumerate(lines):
        ax.text(x + 2.2, y + h - 6.6 - i * 3.1, t, ha="left", va="top",
                fontsize=7, color=INK, zorder=3)

box(1, 14, 26, 30, "VALUE",
    ["value, as printed", "quantity (SA / K$_{eu}$ / $\\Phi$ / S$_{CC,T}$)",
     "definition class", "denominator  ← often implicit",
     "measured or model-derived", "range endpoints, if a range",
     "location in source", "source + version"],
    face=PANEL)

box(37, 24, 27, 20, "SYSTEM",
    ["drug", "coformer", "stoichiometry  ← K$_{eu}$ scale"])

box(37, 1, 27, 20, "CONDITIONS",
    ["medium + medium class", "surfactant + concentration",
     "pH, equilibrium  ← often absent", "temperature"])

box(73, 14, 26, 20, "COMPARABILITY",
    ["SR$_{\\mathrm{drug}}$ in this medium", "reference medium for SR",
     "ε, if coformer solubilized"],
    edge=AMBER, ls=(0, (4, 2)), lw=1.0)

for y0, y1 in ((29, 34), (29, 11)):
    ax.add_patch(FancyArrowPatch((27.8, y0), (36.2, y1),
        arrowstyle="-", linewidth=0.7, color=MUTED, zorder=1,
        connectionstyle="arc3,rad=0"))
ax.add_patch(FancyArrowPatch((64.8, 29), (72.2, 26),
    arrowstyle="-|>", mutation_scale=8, linewidth=0.9, color=AMBER, zorder=1))
ax.add_patch(FancyArrowPatch((64.8, 11), (72.2, 22),
    arrowstyle="-|>", mutation_scale=8, linewidth=0.9, color=AMBER, zorder=1))

ax.text(86, 10.4,
        "without this block, two correct\nmeasurements in different media\nare indistinguishable "
        "from a\ndisagreement (§3.6)",
        ha="center", va="top", fontsize=6.5, color=AMBER, linespacing=1.4, style="italic")
ax.text(14, 11.6,
        "one row per (system × conditions),\nnot one row per pair",
        ha="center", va="top", fontsize=6.5, color=MUTED, linespacing=1.4, style="italic")

fig.savefig(os.path.join(FIGDIR, "figure1_data_model.pdf"))
fig.savefig(os.path.join(FIGDIR, "figure1_data_model.png"), dpi=600)
plt.close(fig)

print("figure1_data_model.pdf/.png and figure2_harmonization.pdf/.png written to", os.path.normpath(FIGDIR))
