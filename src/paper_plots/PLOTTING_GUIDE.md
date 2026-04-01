# Plotting Guide: parallel-algorithms-liva

How the plot code is organized, how to run it, and where to change visual properties.

---

## Table of Contents

1. [Code Organization](#1-code-organization)
2. [Running the Plots](#2-running-the-plots)
3. [Global Visual Settings — header.py](#3-global-visual-settings--headerpy)
4. [Data Objects](#4-data-objects)
5. [Paper Plots — File by File](#5-paper-plots--file-by-file)
6. [Thesis Plots Referenced by the Paper](#6-thesis-plots-referenced-by-the-paper)
7. [Common Adjustments Quick Reference](#7-common-adjustments-quick-reference)

---

## 1. Code Organization

```
parallel-algorithms-liva/
├── header.py                  # Global imports, colors, SAVE_LOC — loaded by every plot file
├── main.py                    # Entry point: calls all plot functions in sequence
├── converter.py               # Converts Google Sheets CSV → JSON data files
├── sync_from_sheets.py        # Downloads latest CSVs from Google Sheets
├── data/
│   ├── par_algos_original_MAR21.json   # Raw parallel algorithm records
│   ├── par_algos_simulated_MAR21.json  # Same + model 700 (distributed) simulations
│   ├── seq_data_MAR21.json             # Sequential algorithm records
│   ├── par_models_FEB18.json           # Year/model pairings for model-over-time plots
│   └── old/                            # Archived older data versions
├── src/
│   ├── processed_data.py      # Loads JSON files and exposes named data objects
│   ├── helper_functions.py    # Runtime formula (Brent's theorem), get_runtime, get_pareto_points
│   ├── complexity_functions.py # Evaluates asymptotic complexity codes → numeric values
│   ├── standard_codes.py      # Maps complexity code integers → LaTeX strings and model IDs
│   ├── huge_num.py            # Handles very large/very small asymptotic values
│   ├── paper_plots/           # Plot generators for the journal paper (this directory)
│   └── thesis_plots/          # Plot generators for the thesis
└── output-plots/
    └── MAR21 data/            # Where plots are currently saved (see SAVE_LOC in header.py)
```

### Data flow

```
Google Sheets
    ↓ sync_from_sheets.py  (downloads CSVs)
    ↓ converter.py         (parses CSVs → JSON)
data/*.json
    ↓ src/processed_data.py (loads JSON → Python dicts)
Named data objects (full_data, simulated_par_data, etc.)
    ↓ imported by header.py via `from src.processed_data import *`
    ↓ available to every plot file via `from header import *`
src/paper_plots/*.py  →  output-plots/MAR21 data/*.png
```

Every plot file starts with `from header import *`, which gives it access to all data,
all color constants, matplotlib, numpy, etc. in one import.

### Paper plots directory (this directory)

| File | What it generates |
|---|---|
| `average_imprvmnt_rates.py` | Improvement rate histograms; Sankey-style bar chart |
| `problem_speedup_vs_proc.py` | Speedup vs processor count curves |
| `num_overhead_vs_span.py` | Work overhead vs speedup scatter/pareto |
| `span_work_more_probs.py` | Work-span pareto frontier |
| `aggregate_switch_to_work_ineff.py` | Work efficiency vs processor count; overhead histograms |
| `models_contour.py` | (Stub, not yet implemented) |
| `problem_overhead_vs_proc.py` | Work overhead vs processor count |

### Thesis plots directory

| File | What it generates |
|---|---|
| `relative_speedup.py` | `speedup_for_available_processors`, `available_processors` |
| `aggregated_relative_speedup.py` | Aggregated speedup across all problems |
| `span_work_imprvmnt.py` | Span and work improvement over time |
| `work_eff_vs_overall_span.py` | Work efficiency vs best-span tradeoff |
| `decade_progress.py` | Improvement breakdown by decade |
| `pareto_frontier.py` | Per-problem pareto frontier plots |
| `share_of_progress.py` | Share of algorithmic progress pie/bar |
| `compound_growth_rate.py` | Compound growth rate of improvements |
| `models.py` | Model distribution over time |
| `strong_scaling.py`, `weak_scaling.py`, `varying_scaling.py` | Scaling behavior plots |
| `span_overhead.py`, `span_perf_imprvmnt.py` | Span-specific analysis |
| `improved_families.py`, `new_parallelism.py` | Problem family analysis |
| `histograms.py`, `incremental_benefit_table.py` | Supplementary analysis |
| `helper_improvements.py` | Shared helpers for improvement calculations |

---

## 2. Running the Plots

All commands should be run from the `parallel-algorithms-liva/` directory.

**Run all paper figures:**
```bash
python3 main.py
```

**Run a single figure in a script:**
```python
from header import *
from src.paper_plots.problem_speedup_vs_proc import problem_speedup_vs_proc_three_curves

problem_speedup_vs_proc_three_curves(full_data, 'Topological Sorting',
                                     n_values=[10**3, 10**6, 10**9], max_p=10**10)
```

**Run without a display (e.g., on a server):**
```bash
MPLBACKEND=Agg python3 main.py
```

**Update data before regenerating plots (full pipeline):**
```bash
python3 sync_from_sheets.py     # Download latest CSVs
python3 converter.py            # Convert CSVs → JSON
python3 main.py                 # Regenerate all plots
```

**When updating to a new data version** (e.g., a new month's data), there are three
places to update — see section 3.

---

## 3. Global Visual Settings — `header.py`

`header.py` is the single place that controls global appearance. Every plot file
imports it with `from header import *`.

### Output location and data version

```python
SAVE_LOC = "output-plots/MAR21 data/"
```
Change this to redirect where all plots are saved. Create the directory first.

The data version is controlled in `src/processed_data.py`:
```python
VERSION = "_MAR21"
```
Change this to switch which `data/par_algos_original_{VERSION}.json` etc. are loaded.

Also update the version string in `converter.py` if re-running the data pipeline:
```python
VERSION = "_MAR21"   # in converter.py, near the top
```

### Color palettes

```python
# Processor lines (Top Supercomputers, Personal Computers, Sequential)
PROCESSOR_COLORS = ['#3cb44b', '#ffe119', '#a9a9a9']  # green, yellow, grey

# Sequential vs parallel highlighting
SEQ_PAR_COLORS = ['#F5C8AF', '#58D68D']  # warm tan, green

# Algorithm segment backgrounds (speedup_vs_proc plot)
ALGO_COLORS = ["#AEDBFF", "#369BFF", "#6FBFFF"]   # light → dark blue
ALGO_LINE_COLOR = "#0A2A4F"                          # very dark blue for the speedup line

# Blue gradient (work efficiency stacked bars)
COLORS_GRADIENT = ['#88CCEE', '#6BAEDC', '#4E94C6', '#3970A5', '#2B5580']

# Work efficiency spectrum (no parallel, seq fastest, work-efficient, work-inefficient)
WORK_EFF_COLORS = ["#4477AA", "#88CCEE", "#FDB863", "#D55E00"]

# Per-problem colors (used in overhead_vs_span, span_work_more_probs)
COLORS = list(mcolors.TABLEAU_COLORS.values())   # 10 standard tableau colors

# Model-specific colors (used in model distribution plots)
MODEL_COLORS = {100: '#0000ff', 200: '#ffff00', 300: '#ff00ff', ...}
```

### Current year

```python
CUR_YEAR = 2024
```
Used for x-axis limits (plots extend to `CUR_YEAR+1`) and for "as of today" calculations.
Update this when a new year's data is incorporated.

---

## 4. Data Objects

These are loaded by `src/processed_data.py` and available everywhere via `from header import *`.

| Variable | Description |
|---|---|
| `full_data` | All algorithms (parallel + sequential), keyed by algorithm name string |
| `simulated_par_data` | Parallel algorithms only (parallel field == "1"), with model 700 simulations added |
| `full_seq_data` | Sequential algorithms only |
| `full_problem_data` | Per-problem summary: best span algo, best work algo, work-efficient algo, etc. |
| `top_processor_data` | Dict: year → (processor_count, supercomputer_name). Supercomputer evolution. |
| `pc_processor_data` | Dict: year → (processor_count, ''). Personal computer core evolution. |
| `problem_dict` | Dict: problem_id_string → human-readable problem name |
| `model_dict` | Dict: model_int → human-readable model name |
| `DECADES` | List of decade boundary years used in decade-progress plots |

**Algorithm record structure** (values of `full_data`):
```python
{
    "year":     int,       # publication year
    "problem":  str,       # problem name string (exact match for filtering)
    "span":     code,      # span complexity code (int or Huge)
    "work":     code,      # work complexity code
    "model":    int,       # computational model ID (see MODEL_COLORS/model_dict)
    "parallel": "1"/"0",  # "1" = parallel algorithm
    "author":   str,       # author string (may include problem prefix + ID digits)
    ...
}
```

**Algorithm name format:** Keys in `full_data` have the form `"{family_id}{AuthorName (Year)}"`.
The family ID is either a pure number prefix (parallel, e.g. `"56Chaudhuri (1992)"`)
or a problem-name + number prefix (sequential, e.g. `"Topological Sorting453Kahn's algorithm (1962)"`).
Strip the prefix with `re.sub(r'^[^\d]*\d+', '', key)` to get the display name.

---

## 5. Paper Plots — File by File

### 5.1 `average_imprvmnt_rates.py`

**`sankey_style_graph(all_data, par_data, n=1000000, p=1000)`**

Three-bar "sankey" chart showing: all problems → problems with parallel → speedup distribution.

Key visual parameters inside the function:

```python
fig, ax = plt.subplots(figsize=(8, 6))   # figure size
bar_width = 0.7                           # width of each bar (0–1 scale)

# Bar colors (uses seaborn colorblind palette)
bar1_color_top    = cb_colors[0]   # blue  — "Parallel Algorithm Exists"
bar1_color_bottom = cb_colors[1]   # orange — "No Parallel Algorithm Exists"
bar2_color_top    = cb_colors[2]   # green  — "Parallel Algorithm Faster"
bar2_color_bottom = cb_colors[3]   # red    — "Parallel Algorithm Not Faster"
# Bar 3 uses a Greens colormap gradient (matplotlib cm.Greens)

# Top-of-bar percentage labels (100%, 40%, 25%)
ax.text(1, 1.02, ...)     # y=1.02 places them just above the bars
                           # increase to push them further above

# Title padding (prevents percentage labels overlapping title)
ax.set_title(..., pad=28)  # increase pad= to push title higher

# Top margin
fig.subplots_adjust(top=0.82)  # lower value = more space above axes for title+labels

# Label x-positions of the three bars
# Bar 1 at x=1, Bar 2 at x=2, Bar 3 at x=3  (hardcoded)
# The line between bar endpoints (for the dashed Sankey connectors):
ax.plot([1 + bar_width/2, 2 - bar_width/2], [1, 1], ...)

# Speedup bin right-side labels
label_base_x   = 3 + bar_width/2 + 0.03   # x where the tick line starts
label_gap       = 0.03                      # gap between tick line and text
stagger_x_offset = 0.07                    # extra x offset for odd-indexed labels
```

Saved to: `SAVE_LOC + 'sankey_style_graph_n_{n}_p_{p}.png'`

---

**`EVERYTHING_yearly_impr_rate_histo_grid(full_data, raw_buckets, n_values, p_values, variation, ...)`**

3×3 grid of improvement rate histograms. One column per n value, one row per p value.

```python
figsize = (7, 7)           # overall figure size — increase for larger subplots
dpi = 200

# Bucket boundaries are passed in from main.py as `histo_buckets`:
histo_buckets = [
    {"max": 0.001, "label": "~0%"},
    {"max": 0.03,  "label": "0.1-3%"},
    {"max": 0.1,   "label": "3-10%"},
    {"max": 0.3,   "label": "10-30%"},
    {"max": 1,     "label": "30-100%"},
]
# Add more dicts to add more columns, or change "max" to shift bucket boundaries.

# variation parameter selects the data subset:
#   "just_par_impr"  — parallel improvements only (measured from best sequential)
#   "seq_plus_all"   — sequential + parallel combined
#   (default)        — all algorithms
```

Saved to: `SAVE_LOC + '{variation}_EVERYTHING_average_improvement_rate.png'`

---

### 5.2 `problem_speedup_vs_proc.py`

**`problem_speedup_vs_proc_three_curves(all_data, problem, n_values, max_p, point_number=1000)`**

Speedup envelope curves for one problem across multiple n values.

```python
figsize = (10, 5 * len(n_values))  # grows vertically with number of n values
# constrained_layout=True handles spacing between subplots automatically

# Algorithm segment background shading
background_colors = ALGO_COLORS          # from header.py — 3 shades of blue
# If more than 3 algorithm segments appear, it will cycle/wrap

# Speedup line
color = ALGO_LINE_COLOR                  # single dark blue line for the envelope

# Segment boundary markers
ax.axvline(x=p1, color='gray', linestyle='--', linewidth=0.8)

# Segment labels (author name + overhead)
# x position: log-midpoint of the segment
mid_x = 10 ** ((math.log10(p1) + math.log10(p2)) / 2)
# y position: 2× the speedup at max_p (top of visible range)
top_y = serial_runtime / processor_data[max_p]["runtime"] * 2
# Text content: display name (prefix-stripped) + overhead range
# Font size:
fontsize=8      # change this to make segment labels larger/smaller
# clip_on=True prevents text from rendering outside the axes frame

# The "1×" reference line
ax.axhline(y=1, color='gray', linestyle=':', linewidth=1)

# Y-axis limits
ax.set_ylim(0.9, top_y * 1.5)   # bottom is just below 1; top is 1.5× the label height
```

Saved to: `SAVE_LOC + 'speedup_separated_{problem}_curves.png'`

---

### 5.3 `num_overhead_vs_span.py`

**`numerical_overhead_vs_span(par_data, seq_data, problems, n=10**6, allowed_models=...)`**

Work overhead vs speedup scatter with pareto frontier for 3 problems.

```python
figsize = (6.55, 3)      # matches paper column width
dpi = 200

# Colors: one per problem, drawn from COLORS (tableau palette)
# Pareto frontier points: hardcoded lists of algorithm name strings at the top of the file
# If data changes and pareto points shift, these lists must be updated manually.

# Axis limits
ax.set_ylim(0.5, 0.9e6)     # y: overhead range
# x-axis limits are computed automatically from the data

# X-tick labels: only even powers of 10 are shown
# controlled by even_powers_list() helper inside the file

# Y-tick labels formatted as "1,234×" (comma-formatted integer with ×)
```

Saved to: `SAVE_LOC + 'numerical_overhead_vs_span.png'`

---

### 5.4 `span_work_more_probs.py`

**`span_vs_work_multiple_probs_pareto_frontier(par_data, seq_data, problems, allowed_models=...)`**

Work-span pareto frontier for 3 problems on the same axes.

```python
figsize = (6.55, 3)      # matches paper column width
dpi = 200

# Axis tick labels: asymptotic complexity strings derived from complexity codes
# They are placed every-other (even index) to prevent overlap
# To control which labels show: edit the slice/modulo in the tick-placement loop

# Per-problem algorithm label positions are manually tweaked with hardcoded (x, y) offsets
# inside the function — search for `ax.text(` calls to find them
```

Saved to: `SAVE_LOC + 'span_vs_work_pareto_multiple_problems.png'`

---

### 5.5 `aggregate_switch_to_work_ineff.py`

**`NEW_work_overhead_histogram_graph_multiple_p(par_data, seq_data, problems, p_values, n_values, upper_bounds, ...)`**

Stacked percentage bar chart: fraction of problems in each overhead bucket, at various (n, p).

```python
figsize = (6.5, 2.5)      # wide and short
dpi = 200

# Overhead bins are passed as upper_bounds from main.py:
upper_bounds = [0, 100, 1000, 10000, math.inf]
# Each pair of consecutive values defines one bar segment.
# Change these to adjust the bin boundaries.

# Colors per bin: drawn from COLORS_GRADIENT (5-step blue gradient from header.py)

# Legend placement: only shown on the n=10^9 subplot, bottom-right
# change loc= and bbox_to_anchor= inside the function to move it
```

Saved to: `SAVE_LOC + 'NEW_work_overhead_histo_different_ps.png'`

---

## 6. Thesis Plots Referenced by the Paper

### `src/thesis_plots/relative_speedup.py`

Two functions from this file are called from `main.py` for the paper.

---

**`available_processors(top_proc_data, pc_proc_data)`**

Raw processor count over time. Two step-function lines.

```python
figsize = (6.55, 3.25)
dpi = 200
layout = 'tight'

# Line colors (from header.py PROCESSOR_COLORS):
PROCESSOR_COLORS[0]  # green — Top Supercomputers
PROCESSOR_COLORS[1]  # yellow — Personal Computers

# Horizontal "current value" extension
ax.hlines(y=top_points[-1], xmin=top_years[-1], xmax=CUR_YEAR+1, ...)
# xmax=CUR_YEAR+1 — where the flat end line terminates.
# Increase this value to extend the line further right.

# Right-side labels
ax.text(CUR_YEAR+1.5, final_y_vals[0], "Top Supercomputers", fontsize=8, ...)
ax.text(CUR_YEAR+1.5, final_y_vals[1], "Personal Computers", fontsize=8, ...)
# CUR_YEAR+1.5: x position of labels. Increase to push labels further right.
# fontsize=8: label size. Change this if labels are too small or overlap.
# final_y_vals[0/1]: y position matches the end-of-line value (automatic).

# X-axis range
ax.set_xlim(1962-1, CUR_YEAR+1)
# Keep CUR_YEAR+1 tight — labels extend past this via bbox_inches='tight' in savefig.

plt.savefig(..., bbox_inches='tight')
# bbox_inches='tight' is required to capture labels placed outside the axes frame.
# Without it, the labels get cropped at the figure boundary.
```

---

**`speedup_for_available_processors(parallel_data, sequential_data, problem, top_proc_data, pc_proc_data, n, seq)`**

Historical speedup for a problem as processor counts grew.

```python
figsize = (6.55, 3.25)
dpi = 200
layout = 'tight'

# Right-side label placement (controls all three labels together)
LABEL_X = CUR_YEAR + 1.5       # x position for all labels
                                 # increase to push labels further right
MIN_LOG_GAP = 1.2               # minimum vertical separation in log10 decades
                                 # increase if labels still overlap (e.g. try 1.5 or 2.0)
                                 # decrease to allow labels closer together

# How label spreading works:
# Labels are sorted highest-y first. If two consecutive labels are less than
# MIN_LOG_GAP decades apart, the lower one is pushed down to maintain the gap.
# The top label always stays at its true y value; only lower ones get shifted.

# Horizontal line endpoint (where flat lines end before labels start)
ax.hlines(y=values[-1], xmin=years[-1], xmax=CUR_YEAR+1, ...)
# CUR_YEAR+1: end of line. Keep 0.5 less than LABEL_X for a visual gap.

# Arrow annotations (show speedup ratio between curves)
offset_arrow(arrow_y=2018)                              # Top Supercomputers vs Sequential at 2018
offset_arrow(arrow_y=2022, curve=pc_adjusted_curve,
             size="normal", text_left=True)             # Personal Computers vs Sequential at 2022
# arrow_y: the year where the arrow is drawn
# size: "normal" for readable font, "small" for smaller
# text_left=True: puts the annotation text to the LEFT of the arrow
#   (use this when the arrow is near the right edge to avoid label overlap)
# text_left=False (default): puts text to the RIGHT (offset +2 years)

# X-axis range
ax.set_xlim(first_year-1, CUR_YEAR+1)   # tight; labels sit outside via bbox_inches='tight'

plt.savefig(..., bbox_inches='tight')    # required to capture outside-axes labels
```

---

## 7. Common Adjustments Quick Reference

### Change where plots are saved
In `header.py`:
```python
SAVE_LOC = "output-plots/MAR21 data/"   # change to new directory (must exist first)
```
Also update the same version string in `src/processed_data.py` (`VERSION`) and
`converter.py` (`VERSION`) if switching data versions.

### Change figure DPI or size
Each function has its own `figsize` and `dpi` arguments in the `plt.subplots()` call.
All paper plots use `dpi=200`. Change locally in the function; there is no global DPI setting.

### Change font sizes
Each `ax.text(...)`, `ax.set_title(...)`, `ax.set_xlabel(...)` call has its own `fontsize`.
There is no global font size override. Search for `fontsize=` within the relevant file.
Common values: axis labels = 12–14, tick labels = 8–10, in-plot annotations = 6–8.

### Add or change colors
Edit the relevant palette in `header.py`. Most plot files read colors by index
(e.g. `PROCESSOR_COLORS[0]`), so changing the palette there affects all plots using it.

### Move right-side line labels (`available_processors`, `speedup_for_available_processors`)
- **Label x position:** change `CUR_YEAR+1.5` in `ax.text(CUR_YEAR+1.5, ...)`.
  More than ~3 years past `CUR_YEAR` is usually sufficient; `bbox_inches='tight'` in
  `savefig` ensures the figure expands to include the text.
- **Label separation (speedup plot only):** change `MIN_LOG_GAP` from its current value of
  `1.2` to a larger number (e.g. `2.0`) if labels still crowd each other.
- **Line endpoint:** `xmax=CUR_YEAR+1` in `ax.hlines(...)` — keep this ~0.5 less than
  the label x position to leave a visual gap between line and text.

### Change axis limits
- **X-axis (year plots):** `ax.set_xlim(first_year-1, CUR_YEAR+1)`. The right limit
  should be `CUR_YEAR+1` regardless of label positions (labels live outside via
  `bbox_inches='tight'`).
- **Y-axis (speedup plot segment labels):** `top_y = serial_runtime / processor_data[max_p]["runtime"] * 2`
  and `ax.set_ylim(0.9, top_y * 1.5)`. The `*2` and `*1.5` multipliers control headroom.
- **Y-axis (overhead vs span):** `ax.set_ylim(0.5, 0.9e6)` in `num_overhead_vs_span.py` — hardcoded.

### Change improvement histogram bins
In `main.py`, the `histo_buckets` list controls both boundaries and labels:
```python
histo_buckets = [
    {"max": 0.001, "label": "~0%"},
    {"max": 0.03,  "label": "0.1-3%"},
    ...
]
```
Add, remove, or shift entries here. The histogram generator reads this list directly.

### Change speedup bins (Sankey plot)
In `average_imprvmnt_rates.py`, `sankey_style_graph()`, around line 1393:
```python
speedup_bins = ["1-2x", "2x-4x", "4x-8x", ...]
speedup_values = [0, 0, 0, ...]  # must have same length as speedup_bins
```
The `if/elif` block below assigns each speedup to a bin — update that logic to match
any new bin boundaries.

### Change which problem the APSP speedup plot uses
In `main.py`:
```python
speedup_for_available_processors(..., 'APSP', ..., n=10**6, seq=True)
```
Replace `'APSP'` with any string from `problem_dict.keys()`, and adjust `n` as needed.

### Change the processor arrow years
In `speedup_for_available_processors`, near the bottom of the function:
```python
offset_arrow()                                           # arrow at 2018, Top Supercomputers
offset_arrow(arrow_y=2022, curve=pc_adjusted_curve,
             text_left=True)                             # arrow at 2022, Personal Computers
```
Change `arrow_y` to any year in the dataset range. If the arrow text overlaps the
right-edge labels, add `text_left=True` to place the text on the left side of the arrow.

### Add a new paper figure
1. Create a new `.py` file in `src/paper_plots/` starting with `from header import *`.
2. Write a function that accepts data objects from section 4 and calls `plt.savefig(SAVE_LOC + 'yourfile.png', bbox_inches='tight')`.
3. Add the call to `main.py` in the appropriate figure block.
4. Add the `from src.paper_plots.yourfile import *` line to `main.py`'s import block at the top.
