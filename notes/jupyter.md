# Introduction to Jupyter

## Table of Contents

1. [What is Jupyter?](#what-is-jupyter)
2. [Installation and Setup](#installation-and-setup)
3. [Notebook Basics](#notebook-basics)
4. [Keyboard Shortcuts](#keyboard-shortcuts)
5. [Markdown in Notebooks](#markdown-in-notebooks)
6. [Magic Commands](#magic-commands)
7. [Rich Output](#rich-output)
8. [Working with Data](#working-with-data)
9. [Notebook Best Practices](#notebook-best-practices)
10. [Extensions and Widgets](#extensions-and-widgets)
11. [Converting and Sharing](#converting-and-sharing)
12. [JupyterLab Features](#jupyterlab-features)
13. [Practice Exercises](#practice-exercises)
14. [Summary](#summary)

---

## What is Jupyter?

Jupyter is an open-source platform for interactive computing. It provides:
- **Jupyter Notebook**: A web-based document combining live code, equations, visualizations, and narrative text
- **JupyterLab**: A next-generation IDE-like interface with tabs, terminals, and a file browser
- **IPython kernel**: The default Python execution backend powering notebooks
- **Multi-language support**: The name stands for **Ju**lia, **Py**thon, **R** (and 40+ other kernels)
- **Ecosystem**: nbconvert, nbviewer, JupyterHub (multi-user), Binder (shareable environments)

```python
# Jupyter notebooks use the .ipynb format (JSON under the hood)
# Each notebook consists of cells: code, markdown, or raw text
# Code cells execute via a "kernel" (a persistent process)

# A typical data science workflow in Jupyter:
# 1. Load and explore data interactively
# 2. Visualize patterns inline
# 3. Iterate on models with immediate feedback
# 4. Document findings alongside code
```

---

## Installation and Setup

```bash
# Install Jupyter Notebook (classic interface)
pip install notebook

# Install JupyterLab (recommended modern interface)
pip install jupyterlab

# Install both together with common data science tools
pip install jupyterlab notebook ipywidgets pandas matplotlib
```

```bash
# Launch JupyterLab (opens browser at http://localhost:8888)
jupyter lab

# Launch classic Notebook interface
jupyter notebook

# Launch on a specific port
jupyter lab --port 9999

# Launch without opening a browser (useful for remote servers)
jupyter lab --no-browser

# List running notebook servers
jupyter server list
```

```python
# Check Jupyter version from inside a notebook
import IPython
print(IPython.__version__)
# 8.x.x

# Check kernel info
!jupyter kernelspec list
# Available kernels:
#   python3    /usr/local/share/jupyter/kernels/python3
```

---

## Notebook Basics

### Cell Types

```python
# CODE CELL: executes Python (or whatever kernel language)
# This is a code cell - press Shift+Enter to run it
x = 42
print(f"The answer is {x}")
# The answer is 42

# The last expression in a cell is displayed automatically (no print needed)
x * 2
# Out[1]: 84
```

```markdown
<!-- MARKDOWN CELL: for documentation and narrative text -->
<!-- Switch a cell to markdown with Esc then m -->
<!-- Rendered when you run the cell (Shift+Enter) -->

# This is a heading
Some explanatory text about the analysis.
```

```python
# RAW CELL: plain text, not executed or rendered
# Useful for nbconvert directives or preserving unformatted text
# Switch a cell to raw with Esc then r
```

### Kernel Operations

```python
# The kernel is a persistent process that runs your code
# All variables persist across cells until you restart

# Common kernel operations (from the Kernel menu):
# - Restart: clears all variables, re-imports needed
# - Restart & Run All: fresh execution of the entire notebook
# - Interrupt: stops a long-running cell (like Ctrl+C)

# Check if running inside Jupyter
import sys
"ipykernel" in sys.modules
# True (inside Jupyter), False (in a script)
```

### Cell Output

```python
# Suppress output with a semicolon
import matplotlib.pyplot as plt
plt.plot([1, 2, 3]);  # Semicolon suppresses the [<matplotlib.lines.Line2D>] text

# Display multiple outputs from one cell (not just the last expression)
from IPython.display import display
display("first output")
display("second output")
# 'first output'
# 'second output'

# Clear output programmatically
from IPython.display import clear_output
clear_output(wait=True)  # wait=True prevents flicker
```

---

## Keyboard Shortcuts

### Command Mode (press Esc first)

```
a           Insert cell above
b           Insert cell below
dd          Delete selected cell (press d twice)
z           Undo cell deletion
m           Change cell to Markdown
y           Change cell to Code
r           Change cell to Raw
c           Copy cell
v           Paste cell below
x           Cut cell
Shift+M     Merge selected cells
l           Toggle line numbers
o           Toggle cell output
Shift+Up/Down  Select multiple cells
```

### Edit Mode (press Enter to enter)

```
Shift+Enter     Run cell, move to next
Ctrl+Enter      Run cell, stay in place
Alt+Enter       Run cell, insert new cell below
Ctrl+Shift+-    Split cell at cursor
Tab             Code completion / indent
Shift+Tab       Show function signature/docstring
Ctrl+/          Toggle comment on selected lines
Ctrl+D          Delete whole line
Ctrl+Z          Undo
Ctrl+Shift+Z    Redo
```

```python
# View all shortcuts: press h in command mode
# Or go to Help > Keyboard Shortcuts in the menu

# Tip: the most important shortcut to memorize first
# Shift+Enter - run and advance (you will use this hundreds of times)
```

---

## Markdown in Notebooks

```markdown
<!-- Headers -->
# H1 Title
## H2 Section
### H3 Subsection

<!-- Emphasis -->
**bold text** and *italic text* and ***bold italic***
~~strikethrough~~

<!-- Lists -->
- Unordered item
  - Nested item
1. Ordered item
2. Second item

<!-- Links and Images -->
[Link text](https://example.com)
![Alt text](path/to/image.png)

<!-- Code -->
Inline `code` with backticks
```python
# Fenced code block with syntax highlighting
print("hello")
```

<!-- Tables -->
| Column 1 | Column 2 | Column 3 |
|----------|----------|----------|
| Row 1    | Data     | Data     |
| Row 2    | Data     | Data     |

<!-- LaTeX Math (powered by MathJax) -->
Inline math: $E = mc^2$

Display math:
$$\frac{\partial f}{\partial x} = \lim_{h \to 0} \frac{f(x+h) - f(x)}{h}$$

<!-- Block quotes -->
> This is a quote
> spanning multiple lines

<!-- Horizontal rule -->
---
```

---

## Magic Commands

```python
# Line magics start with % and apply to a single line
# Cell magics start with %% and apply to the entire cell

# TIMING
%timeit sum(range(1000))       # Run many times, report average
# 12.3 us +/- 145 ns per loop (mean +/- std. dev. of 7 runs, 100000 loops each)

%time sum(range(1000000))      # Run once, report wall time
# CPU times: user 28.3 ms, sys: 0 ns, total: 28.3 ms
# Wall time: 28.5 ms
```

```python
%%time
# Cell magic version - times the entire cell
total = 0
for i in range(1000000):
    total += i
print(total)
# 499999500000
# CPU times: user 82.1 ms, sys: 0 ns, total: 82.1 ms
# Wall time: 82.5 ms
```

```python
# MATPLOTLIB INTEGRATION
%matplotlib inline              # Render plots inline (default in modern Jupyter)
%config InlineBackend.figure_format = "retina"  # High-DPI plots

# VARIABLE INSPECTION
x = 10
name = "jupyter"
data = [1, 2, 3]

%who                            # List all variables
# data    name    x

%who str                        # List only string variables
# name

%whos                           # Detailed variable info (type, size, value)
# Variable   Type    Data/Info
# --------------------------------
# data       list    n=3
# name       str     jupyter
# x          int     10
```

```python
# SHELL COMMANDS
!pwd                            # Run shell commands with !
# /home/john/projects

!pip install requests           # Install packages without leaving the notebook

# Capture shell output in a Python variable
files = !ls *.csv
print(files)
# ['data.csv', 'results.csv']
```

```python
# RUNNING EXTERNAL FILES
%run my_script.py               # Execute a Python script (variables become available)
%load my_script.py              # Load file contents into the cell (for editing)

# LOADING EXTENSIONS
%load_ext autoreload            # Load the autoreload extension
%autoreload 2                   # Auto-reload all modules before executing code
# Extremely useful: edit .py files and they reload automatically

# ENVIRONMENT INFO
%env                            # Show all environment variables
%env MY_VAR=hello               # Set an environment variable

# HISTORY
%history -n 1-5                 # Show input history for cells 1-5

# RESET
%reset -f                       # Clear all variables (careful!)

# LIST ALL MAGICS
%lsmagic                        # Show all available magic commands
```

---

## Rich Output

```python
# Jupyter renders rich output for many object types automatically

# DATAFRAMES: rendered as formatted HTML tables
import pandas as pd
df = pd.DataFrame({
    "name": ["Alice", "Bob", "Charlie"],
    "score": [92, 85, 78],
    "grade": ["A", "B+", "C+"]
})
df  # Just place at end of cell - renders as a styled table
#       name  score grade
# 0    Alice     92     A
# 1      Bob     85    B+
# 2  Charlie     78    C+
```

```python
# PLOTS: displayed inline with %matplotlib inline
import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(0, 10, 100)
fig, ax = plt.subplots(figsize=(8, 4))
ax.plot(x, np.sin(x), label="sin(x)")
ax.plot(x, np.cos(x), label="cos(x)")
ax.set_title("Trigonometric Functions")
ax.legend()
plt.show()  # Renders inline in the notebook
```

```python
# HTML OUTPUT
from IPython.display import HTML, display

display(HTML("<h3 style='color: blue;'>Styled heading</h3>"))
display(HTML("<table><tr><td>Custom</td><td>HTML</td></tr></table>"))

# IMAGES
from IPython.display import Image
display(Image(filename="chart.png", width=400))  # Local file
display(Image(url="https://example.com/image.png"))  # From URL

# JSON (collapsible tree view in JupyterLab)
from IPython.display import JSON
display(JSON({"key": "value", "nested": {"a": 1, "b": 2}}))

# AUDIO AND VIDEO
from IPython.display import Audio, Video
display(Audio(filename="sound.wav"))
display(Video("clip.mp4", width=600))
```

```python
# STYLED DATAFRAMES (Pandas Styler)
import pandas as pd
import numpy as np

df = pd.DataFrame(np.random.randn(5, 3), columns=["A", "B", "C"])

# Highlight max values, apply gradient, format numbers
(df.style
    .highlight_max(axis=0, color="lightgreen")
    .background_gradient(cmap="RdYlGn", axis=None)
    .format("{:.2f}")
    .set_caption("Styled DataFrame"))
```

---

## Working with Data

```python
# LOADING DATA
import pandas as pd
import matplotlib.pyplot as plt

# Read CSV (the most common operation)
df = pd.read_csv("sales_data.csv")

# Quick exploration pattern (run these in separate cells for clarity)
df.shape               # (1000, 8) - rows and columns
# (1000, 8)

df.head()              # First 5 rows as a table
df.dtypes              # Column types
df.describe()          # Statistical summary
df.info()              # Non-null counts and memory usage
df.isnull().sum()      # Missing values per column
```

```python
# INLINE PLOTTING WORKFLOW
# Explore distributions
fig, axes = plt.subplots(1, 3, figsize=(15, 4))

df["revenue"].hist(bins=30, ax=axes[0], color="steelblue")
axes[0].set_title("Revenue Distribution")

df["category"].value_counts().plot(kind="bar", ax=axes[1], color="coral")
axes[1].set_title("Category Counts")

df.plot(kind="scatter", x="quantity", y="revenue", ax=axes[2], alpha=0.5)
axes[2].set_title("Quantity vs Revenue")

plt.tight_layout()
plt.show()
```

```python
# INTERACTIVE EXPLORATION PATTERNS

# Pattern 1: filter-then-examine
subset = df[df["revenue"] > 1000]
print(f"High revenue rows: {len(subset)} ({len(subset)/len(df)*100:.1f}%)")
subset.head(10)

# Pattern 2: group-then-summarize
summary = (df
    .groupby("category")
    .agg(count=("revenue", "size"),
         mean_revenue=("revenue", "mean"),
         total_revenue=("revenue", "sum"))
    .sort_values("total_revenue", ascending=False))
summary

# Pattern 3: iterate with value_counts
for col in df.select_dtypes(include="object").columns:
    print(f"\n--- {col} ---")
    print(df[col].value_counts().head())
```

```python
# CORRELATION ANALYSIS
import numpy as np

# Compute and display correlation matrix
corr = df.select_dtypes(include=np.number).corr()

plt.figure(figsize=(8, 6))
plt.imshow(corr, cmap="coolwarm", aspect="auto", vmin=-1, vmax=1)
plt.colorbar(label="Correlation")
plt.xticks(range(len(corr.columns)), corr.columns, rotation=45)
plt.yticks(range(len(corr.columns)), corr.columns)
plt.title("Correlation Matrix")
plt.tight_layout()
plt.show()
```

---

## Notebook Best Practices

```python
# 1. RESTART & RUN ALL before sharing
# Ensures cells run in order and nothing depends on deleted/moved cells
# Kernel > Restart & Run All (or use the toolbar button)

# 2. KEEP IMPORTS AT THE TOP
# First cell should contain all imports
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

# 3. USE MEANINGFUL CELL STRUCTURE
# - One logical step per cell
# - Add markdown cells to explain "why", not "what"
# - Keep cells short (roughly 1-20 lines)
```

```python
# 4. CLEAR OUTPUTS BEFORE COMMITTING TO GIT
# Notebook files contain output (images, HTML tables) which bloat diffs
# From menu: Cell > All Output > Clear (classic) or Edit > Clear All Outputs (Lab)

# Or from command line:
# jupyter nbconvert --clear-output --inplace notebook.ipynb

# 5. USE .gitignore FOR NOTEBOOK CHECKPOINTS
# .ipynb_checkpoints/   <-- add this to .gitignore
```

```python
# 6. EXTRACT REUSABLE CODE INTO .py MODULES
# Instead of copy-pasting between notebooks:

# utils.py
def load_and_clean(filepath):
    """Load CSV and apply standard cleaning."""
    df = pd.read_csv(filepath)
    df.columns = df.columns.str.lower().str.replace(" ", "_")
    df = df.dropna(subset=["id"])
    return df

# Then in the notebook:
# %load_ext autoreload
# %autoreload 2
# from utils import load_and_clean
# df = load_and_clean("data.csv")
```

```python
# 7. DOCUMENT ASSUMPTIONS AND DECISIONS
# Use markdown cells before analysis steps:
# "We exclude rows before 2024 because the data format changed"
# "Using median imputation for missing values (< 5% missing)"

# 8. PARAMETERIZE NOTEBOOKS
# Define key parameters in one cell at the top
DATA_PATH = Path("data/raw/sales_2024.csv")
START_DATE = "2024-01-01"
TARGET_COL = "revenue"
RANDOM_SEED = 42

# 9. USE ASSERTIONS AS SANITY CHECKS
df = pd.read_csv(DATA_PATH)
assert len(df) > 0, "DataFrame is empty"
assert df[TARGET_COL].notnull().all(), f"Nulls found in {TARGET_COL}"
assert df[TARGET_COL].dtype in [np.float64, np.int64], "Target must be numeric"
```

---

## Extensions and Widgets

```python
# IPYWIDGETS: interactive UI controls in notebooks
# pip install ipywidgets
import ipywidgets as widgets
from IPython.display import display

# Simple slider
slider = widgets.IntSlider(value=50, min=0, max=100, description="Threshold:")
display(slider)

# Access the value
print(slider.value)
# 50
```

```python
# INTERACTIVE FUNCTION with interact
from ipywidgets import interact

@interact(x=(0, 100, 5), color=["red", "blue", "green"])
def plot_threshold(x=50, color="red"):
    """Automatically creates sliders/dropdowns from the parameters."""
    data = np.random.randn(200)
    plt.figure(figsize=(8, 3))
    plt.hist(data, bins=30, color=color, alpha=0.7)
    plt.axvline(x / 50 - 1, color="black", linestyle="--", label=f"Threshold: {x}")
    plt.legend()
    plt.show()
```

```python
# COMMON WIDGET TYPES
widgets.Text(description="Name:")                         # Text input
widgets.Dropdown(options=["A", "B", "C"], description="Choice:")  # Dropdown
widgets.Checkbox(value=True, description="Enable:")       # Checkbox
widgets.FloatRangeSlider(value=[2, 8], min=0, max=10)     # Range slider
widgets.DatePicker(description="Start date:")             # Date picker
widgets.Button(description="Run Analysis")                # Button
```

```python
# TQDM: progress bars for loops
# pip install tqdm
from tqdm.notebook import tqdm
import time

# Wrap any iterable with tqdm for a progress bar
results = []
for i in tqdm(range(100), desc="Processing"):
    time.sleep(0.01)  # Simulate work
    results.append(i ** 2)

# Works with pandas apply too
from tqdm.notebook import tqdm
tqdm.pandas(desc="Applying transform")
df["new_col"] = df["revenue"].progress_apply(lambda x: x * 1.1)
```

---

## Converting and Sharing

```bash
# NBCONVERT: convert notebooks to other formats

# Convert to HTML (self-contained, great for sharing)
jupyter nbconvert --to html notebook.ipynb

# Convert to PDF (requires LaTeX: sudo apt install texlive-xetex)
jupyter nbconvert --to pdf notebook.ipynb

# Convert to Python script (strips markdown, keeps code)
jupyter nbconvert --to script notebook.ipynb

# Convert to slides (reveal.js presentation)
jupyter nbconvert --to slides notebook.ipynb --post serve

# Convert to Markdown
jupyter nbconvert --to markdown notebook.ipynb

# Execute notebook from command line (useful for automation / CI)
jupyter nbconvert --to notebook --execute notebook.ipynb --output executed.ipynb
```

```python
# NBVIEWER
# Upload notebook to GitHub, then view rendered at:
# https://nbviewer.org/github/username/repo/blob/main/notebook.ipynb
# Free, no setup needed, renders static notebooks beautifully

# GOOGLE COLAB
# Open any GitHub notebook in Colab by changing the URL:
# github.com/user/repo/blob/main/notebook.ipynb
#   becomes
# colab.research.google.com/github/user/repo/blob/main/notebook.ipynb
# Provides free GPU/TPU, no local setup required

# BINDER
# Create shareable, executable notebook environments from a GitHub repo
# Add a requirements.txt, then launch via https://mybinder.org
# Anyone can run your notebooks without installing anything
```

---

## JupyterLab Features

```python
# JupyterLab is the next-generation Jupyter interface (recommended over classic)

# TABS AND SPLIT VIEWS
# - Open multiple notebooks, terminals, and files as tabs
# - Drag tabs to create side-by-side split views
# - View a notebook and its output/data file simultaneously

# FILE BROWSER (left sidebar)
# - Navigate directories, create files/folders
# - Drag and drop files to upload
# - Right-click for rename, delete, download, copy path

# BUILT-IN TERMINAL
# - File > New > Terminal
# - Full shell access without leaving JupyterLab
# - Run git commands, install packages, manage files

# CSV VIEWER
# - Double-click any .csv file to view as a formatted table
# - Sortable columns, scrollable view
```

```python
# JUPYTERLAB EXTENSIONS
# Extensions add functionality to the JupyterLab interface

# Install extensions via pip (JupyterLab 3+)
# pip install jupyterlab-git         # Git integration (diff, commit, push)
# pip install jupyterlab-lsp         # Language Server Protocol (autocomplete, linting)
# pip install jupyterlab_code_formatter  # Auto-format code with black/isort

# List installed extensions
# jupyter labextension list

# TABLE OF CONTENTS (built-in since JupyterLab 3)
# - Auto-generated from markdown headings
# - Click to navigate sections
# - Toggle from the left sidebar

# DEBUGGER (built-in since JupyterLab 3)
# - Set breakpoints by clicking next to line numbers
# - Step through code, inspect variables
# - Enable with the bug icon in the toolbar
```

---

## Practice Exercises

### Exercise 1: Exploration Notebook

```python
# Create a notebook that loads and explores a dataset
# Use markdown cells to document your findings

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Generate sample data
rng = np.random.default_rng(42)
n = 500
df = pd.DataFrame({
    "date": pd.date_range("2024-01-01", periods=n, freq="D"),
    "category": rng.choice(["Electronics", "Clothing", "Food", "Books"], n),
    "units_sold": rng.integers(1, 100, n),
    "unit_price": rng.uniform(5, 200, n).round(2),
    "region": rng.choice(["North", "South", "East", "West"], n),
})
df["revenue"] = df["units_sold"] * df["unit_price"]

# Tasks:
# 1. Use df.describe(), df.info() to understand the data
# 2. Find the top category by total revenue
# 3. Plot monthly revenue trend
# 4. Create a 2x2 subplot grid with distribution, bar, scatter, and box plots
# 5. Add markdown cells explaining each finding
```

### Exercise 2: Magic Commands and Timing

```python
# Compare performance of different approaches

import numpy as np

data = list(range(100000))

# Time each approach with %timeit
%timeit sum(data)                           # Built-in sum
%timeit np.sum(data)                        # NumPy on a list
%timeit np.sum(np.array(data))              # NumPy on an array

# Create the array once, then time
arr = np.array(data)
%timeit np.sum(arr)                         # NumPy on a pre-made array

# Tasks:
# 1. Which approach is fastest? Why?
# 2. Use %%time to measure a multi-line data processing pipeline
# 3. Use %who and %whos to inspect your variables
# 4. Use !ls to check what files are in your directory
```

### Exercise 3: Interactive Widget Dashboard

```python
# Build an interactive data explorer
import ipywidgets as widgets
from ipywidgets import interact
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

rng = np.random.default_rng(42)
df = pd.DataFrame({
    "x": rng.normal(0, 1, 1000),
    "y": rng.normal(0, 1, 1000),
    "group": rng.choice(["A", "B", "C"], 1000),
})

@interact(
    group=["All", "A", "B", "C"],
    bins=(5, 50, 5),
    plot_type=["histogram", "scatter"]
)
def explore(group="All", bins=20, plot_type="histogram"):
    subset = df if group == "All" else df[df["group"] == group]
    plt.figure(figsize=(8, 4))
    if plot_type == "histogram":
        plt.hist(subset["x"], bins=bins, color="steelblue", edgecolor="white")
        plt.title(f"Distribution of x (group={group}, n={len(subset)})")
    else:
        plt.scatter(subset["x"], subset["y"], alpha=0.4, s=10)
        plt.title(f"x vs y (group={group}, n={len(subset)})")
    plt.tight_layout()
    plt.show()

# Tasks:
# 1. Add a color dropdown that changes the plot color
# 2. Add a checkbox to toggle grid lines
# 3. Export the notebook to HTML with nbconvert
```

---

## Summary

These notes cover the essential features of the Jupyter ecosystem:

1. **Environment**: Jupyter Notebook for simple workflows, JupyterLab for full IDE experience
2. **Cells**: Code (execute), Markdown (document), Raw (plain text)
3. **Shortcuts**: Shift+Enter to run, Esc/Enter for mode switching, a/b/dd for cell management
4. **Markdown**: Headers, lists, links, tables, and LaTeX math for documentation
5. **Magic Commands**: `%timeit` for benchmarking, `%matplotlib inline` for plots, `!` for shell
6. **Rich Output**: DataFrames as HTML tables, inline plots, styled output, multimedia
7. **Data Workflows**: Load, explore, visualize, and iterate interactively
8. **Best Practices**: Restart & Run All, clear outputs for git, extract code to modules
9. **Widgets**: Interactive controls with ipywidgets, progress bars with tqdm
10. **Sharing**: nbconvert for HTML/PDF/slides, nbviewer and Colab for cloud viewing
11. **JupyterLab**: Tabs, terminals, file browser, extensions, debugger

### Next Steps

1. Set up JupyterLab as your default data science environment
2. Learn ipywidgets to build interactive dashboards for stakeholders
3. Explore Papermill for parameterized notebook execution in pipelines
4. Try JupyterHub for team-based multi-user deployments
5. Investigate Jupyter Book for publishing notebook collections as documentation

### Additional Resources

- **Jupyter Documentation**: https://jupyter.org/documentation
- **JupyterLab Docs**: https://jupyterlab.readthedocs.io/
- **IPython Magic Commands**: https://ipython.readthedocs.io/en/stable/interactive/magics.html
- **ipywidgets Guide**: https://ipywidgets.readthedocs.io/en/stable/
- **nbconvert Docs**: https://nbconvert.readthedocs.io/
- **Real Python - Jupyter Tutorial**: https://realpython.com/jupyter-notebook-introduction/
