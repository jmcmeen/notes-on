# Introduction to Matplotlib

## Table of Contents

1. [What is Matplotlib?](#what-is-matplotlib)
2. [Installation and Setup](#installation-and-setup)
3. [Basic Plotting](#basic-plotting)
4. [Plot Types](#plot-types)
5. [Customizing Plots](#customizing-plots)
6. [Subplots and Layouts](#subplots-and-layouts)
7. [Working with Axes](#working-with-axes)
8. [Annotations and Text](#annotations-and-text)
9. [Colormaps and Styling](#colormaps-and-styling)
10. [3D Plots](#3d-plots)
11. [Saving Figures](#saving-figures)
12. [Practice Exercises](#practice-exercises)
13. [Summary](#summary)

---

## What is Matplotlib?

Matplotlib is the foundational plotting library for Python. It provides:
- **Publication-quality figures**: Static, animated, and interactive visualizations
- **Extensive plot types**: Line, bar, scatter, histogram, heatmap, 3D, and more
- **Full control**: Every element of a figure can be customized
- **Backend support**: Works in scripts, Jupyter notebooks, GUIs, and web apps
- **Integration**: Works seamlessly with NumPy, Pandas, and SciPy

---

## Installation and Setup

```bash
pip install matplotlib
```

```python
import matplotlib.pyplot as plt
import numpy as np

# For Jupyter notebooks
# %matplotlib inline

# For higher resolution in notebooks
# %config InlineBackend.figure_format = 'retina'
```

---

## Basic Plotting

### Line Plot

```python
import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(0, 2 * np.pi, 100)
y = np.sin(x)

plt.plot(x, y)
plt.title("Sine Wave")
plt.xlabel("x (radians)")
plt.ylabel("sin(x)")
plt.grid(True)
plt.show()
```

### Multiple Lines

```python
x = np.linspace(0, 2 * np.pi, 100)

plt.plot(x, np.sin(x), label="sin(x)")
plt.plot(x, np.cos(x), label="cos(x)")
plt.plot(x, np.sin(x) + np.cos(x), label="sin(x) + cos(x)", linestyle="--")

plt.title("Trigonometric Functions")
plt.xlabel("x")
plt.ylabel("y")
plt.legend()
plt.grid(True, alpha=0.3)
plt.show()
```

### Quick Plotting with Pandas

```python
import pandas as pd

df = pd.DataFrame({
    "x": range(10),
    "y1": np.random.randn(10).cumsum(),
    "y2": np.random.randn(10).cumsum()
})

df.plot(x="x", y=["y1", "y2"], title="Random Walks")
plt.show()
```

---

## Plot Types

### Scatter Plot

```python
rng = np.random.default_rng(42)
x = rng.normal(0, 1, 100)
y = 2 * x + rng.normal(0, 0.5, 100)
colors = rng.random(100)
sizes = rng.integers(20, 200, 100)

plt.scatter(x, y, c=colors, s=sizes, alpha=0.6, cmap="viridis")
plt.colorbar(label="Color Value")
plt.title("Scatter Plot")
plt.xlabel("x")
plt.ylabel("y")
plt.show()
```

### Bar Chart

```python
categories = ["Python", "JavaScript", "Java", "C++", "Ruby"]
values = [85, 78, 72, 65, 45]

# Vertical bars
plt.bar(categories, values, color=["#3776ab", "#f7df1e", "#b07219", "#00599c", "#cc342d"])
plt.title("Language Popularity")
plt.ylabel("Score")
plt.show()

# Horizontal bars
plt.barh(categories, values)
plt.title("Language Popularity")
plt.xlabel("Score")
plt.show()

# Grouped bars
x = np.arange(len(categories))
width = 0.35
scores_2023 = [80, 75, 70, 63, 42]
scores_2024 = values

fig, ax = plt.subplots()
ax.bar(x - width/2, scores_2023, width, label="2023")
ax.bar(x + width/2, scores_2024, width, label="2024")
ax.set_xticks(x)
ax.set_xticklabels(categories)
ax.legend()
ax.set_title("Year-over-Year Comparison")
plt.show()
```

### Histogram

```python
data = np.random.default_rng(42).normal(50, 10, 1000)

plt.hist(data, bins=30, edgecolor="black", alpha=0.7, color="steelblue")
plt.axvline(np.mean(data), color="red", linestyle="--", label=f"Mean: {np.mean(data):.1f}")
plt.title("Distribution")
plt.xlabel("Value")
plt.ylabel("Frequency")
plt.legend()
plt.show()

# Multiple histograms
data2 = np.random.default_rng(99).normal(55, 8, 1000)
plt.hist(data, bins=30, alpha=0.5, label="Group A")
plt.hist(data2, bins=30, alpha=0.5, label="Group B")
plt.legend()
plt.title("Overlapping Distributions")
plt.show()
```

### Box Plot and Violin Plot

```python
rng = np.random.default_rng(42)
data = [rng.normal(50, 10, 100), rng.normal(60, 8, 100), rng.normal(45, 12, 100)]

# Box plot
fig, axes = plt.subplots(1, 2, figsize=(12, 5))

axes[0].boxplot(data, labels=["A", "B", "C"])
axes[0].set_title("Box Plot")
axes[0].set_ylabel("Value")

# Violin plot
axes[1].violinplot(data, showmeans=True, showmedians=True)
axes[1].set_xticks([1, 2, 3])
axes[1].set_xticklabels(["A", "B", "C"])
axes[1].set_title("Violin Plot")

plt.tight_layout()
plt.show()
```

### Pie Chart

```python
labels = ["Python", "JavaScript", "Java", "C++", "Other"]
sizes = [35, 25, 20, 12, 8]
explode = (0.05, 0, 0, 0, 0)  # Explode first slice

plt.pie(sizes, explode=explode, labels=labels, autopct="%1.1f%%",
        startangle=90, shadow=False)
plt.title("Language Usage")
plt.axis("equal")
plt.show()
```

### Heatmap

```python
data = np.random.default_rng(42).random((8, 8))

plt.imshow(data, cmap="YlOrRd", aspect="auto")
plt.colorbar(label="Value")
plt.title("Heatmap")
plt.xlabel("Column")
plt.ylabel("Row")
plt.show()

# Correlation matrix heatmap
import pandas as pd
df = pd.DataFrame(np.random.default_rng(42).random((100, 5)), columns=list("ABCDE"))
corr = df.corr()

fig, ax = plt.subplots(figsize=(6, 5))
im = ax.imshow(corr, cmap="RdBu_r", vmin=-1, vmax=1)
ax.set_xticks(range(len(corr.columns)))
ax.set_yticks(range(len(corr.columns)))
ax.set_xticklabels(corr.columns)
ax.set_yticklabels(corr.columns)
plt.colorbar(im, label="Correlation")

# Add text annotations
for i in range(len(corr)):
    for j in range(len(corr)):
        ax.text(j, i, f"{corr.iloc[i, j]:.2f}", ha="center", va="center", fontsize=8)

plt.title("Correlation Matrix")
plt.tight_layout()
plt.show()
```

### Error Bars and Fill Between

```python
x = np.linspace(0, 10, 20)
y = np.sin(x)
yerr = np.random.default_rng(42).uniform(0.1, 0.3, len(x))

# Error bars
plt.errorbar(x, y, yerr=yerr, fmt="o-", capsize=3, label="Data ± error")
plt.legend()
plt.title("Error Bars")
plt.show()

# Fill between (confidence band)
x = np.linspace(0, 10, 100)
y = np.sin(x)
plt.plot(x, y, label="Mean")
plt.fill_between(x, y - 0.2, y + 0.2, alpha=0.3, label="±0.2")
plt.legend()
plt.title("Confidence Band")
plt.show()
```

---

## Customizing Plots

### Line Styles and Markers

```python
x = np.linspace(0, 5, 20)

plt.plot(x, x, "r-", label="solid red")          # Color-linestyle shorthand
plt.plot(x, x**1.5, "g--", label="dashed green")
plt.plot(x, x**2, "b:", label="dotted blue")
plt.plot(x, x**0.5, "ko-", label="black circles") # k=black, o=circle

# Full control
plt.plot(x, x**0.8, color="#FF6B6B", linewidth=2.5, linestyle="-.",
         marker="s", markersize=5, markerfacecolor="white",
         markeredgecolor="#FF6B6B", label="custom")

plt.legend()
plt.title("Line Styles and Markers")
plt.show()

# Common markers: o . , v ^ < > s p * h + x D d
# Common colors: b g r c m y k w, or hex "#FF0000", or named "steelblue"
# Common linestyles: - -- -. :
```

### Figure and Font Control

```python
# Figure size and DPI
fig, ax = plt.subplots(figsize=(10, 6), dpi=100)

x = np.linspace(0, 2 * np.pi, 100)
ax.plot(x, np.sin(x))

# Font sizes
ax.set_title("Custom Fonts", fontsize=16, fontweight="bold")
ax.set_xlabel("x", fontsize=12)
ax.set_ylabel("sin(x)", fontsize=12)
ax.tick_params(axis="both", labelsize=10)

# Axis limits
ax.set_xlim(0, 2 * np.pi)
ax.set_ylim(-1.5, 1.5)

# Grid
ax.grid(True, alpha=0.3, linestyle="--")

# Spine customization
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)

plt.tight_layout()
plt.show()
```

### Axis Formatting

```python
import matplotlib.ticker as ticker

fig, ax = plt.subplots()
x = np.linspace(0, 100, 50)
y = x ** 2

ax.plot(x, y)

# Custom tick formatting
ax.xaxis.set_major_locator(ticker.MultipleLocator(20))
ax.xaxis.set_minor_locator(ticker.MultipleLocator(5))
ax.yaxis.set_major_formatter(ticker.StrMethodFormatter("{x:,.0f}"))

# Log scale
fig, axes = plt.subplots(1, 2, figsize=(12, 4))
axes[0].plot(x, y)
axes[0].set_title("Linear Scale")
axes[1].plot(x, y)
axes[1].set_yscale("log")
axes[1].set_title("Log Scale")

plt.tight_layout()
plt.show()
```

---

## Subplots and Layouts

### Basic Subplots

```python
fig, axes = plt.subplots(2, 2, figsize=(10, 8))

x = np.linspace(0, 2 * np.pi, 100)

axes[0, 0].plot(x, np.sin(x))
axes[0, 0].set_title("sin(x)")

axes[0, 1].plot(x, np.cos(x), "r")
axes[0, 1].set_title("cos(x)")

axes[1, 0].plot(x, np.tan(x), "g")
axes[1, 0].set_ylim(-5, 5)
axes[1, 0].set_title("tan(x)")

axes[1, 1].plot(x, np.sin(x) ** 2, "m")
axes[1, 1].set_title("sin²(x)")

plt.suptitle("Trigonometric Functions", fontsize=14, fontweight="bold")
plt.tight_layout()
plt.show()
```

### Unequal Subplot Sizes

```python
fig = plt.figure(figsize=(12, 6))

# GridSpec for flexible layouts
gs = fig.add_gridspec(2, 3, hspace=0.3, wspace=0.3)

ax1 = fig.add_subplot(gs[0, :2])   # Top left, spans 2 columns
ax2 = fig.add_subplot(gs[0, 2])    # Top right
ax3 = fig.add_subplot(gs[1, 0])    # Bottom left
ax4 = fig.add_subplot(gs[1, 1:])   # Bottom right, spans 2 columns

ax1.set_title("Wide Top")
ax2.set_title("Small Top")
ax3.set_title("Small Bottom")
ax4.set_title("Wide Bottom")

plt.show()
```

### Shared Axes

```python
fig, axes = plt.subplots(2, 1, figsize=(10, 6), sharex=True)

x = np.linspace(0, 10, 100)
axes[0].plot(x, np.sin(x))
axes[0].set_ylabel("sin(x)")

axes[1].plot(x, np.cos(x), "r")
axes[1].set_ylabel("cos(x)")
axes[1].set_xlabel("x")

plt.tight_layout()
plt.show()
```

---

## Working with Axes

### Twin Axes (Two Y-Axes)

```python
fig, ax1 = plt.subplots()

x = np.arange(1, 13)
temp = [5, 7, 12, 18, 23, 27, 29, 28, 23, 17, 10, 6]
rain = [80, 65, 70, 55, 45, 30, 25, 35, 50, 70, 85, 90]

color1 = "tab:red"
ax1.set_xlabel("Month")
ax1.set_ylabel("Temperature (°C)", color=color1)
ax1.plot(x, temp, color=color1, marker="o")
ax1.tick_params(axis="y", labelcolor=color1)

ax2 = ax1.twinx()  # Second y-axis sharing x-axis
color2 = "tab:blue"
ax2.set_ylabel("Rainfall (mm)", color=color2)
ax2.bar(x, rain, alpha=0.3, color=color2)
ax2.tick_params(axis="y", labelcolor=color2)

plt.title("Temperature and Rainfall")
fig.tight_layout()
plt.show()
```

### Inset Axes

```python
fig, ax = plt.subplots()

x = np.linspace(0, 10, 1000)
y = np.sin(x) * np.exp(-0.1 * x)

ax.plot(x, y)
ax.set_title("Damped Oscillation")

# Create inset
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
axins = inset_axes(ax, width="40%", height="40%", loc="upper right")
axins.plot(x[:200], y[:200], "r")
axins.set_title("Zoomed", fontsize=8)

plt.show()
```

---

## Annotations and Text

```python
fig, ax = plt.subplots(figsize=(10, 6))

x = np.linspace(0, 2 * np.pi, 100)
y = np.sin(x)
ax.plot(x, y)

# Text at specific location
ax.text(np.pi, 0, "π", fontsize=14, ha="center", va="bottom",
        bbox=dict(boxstyle="round", facecolor="wheat", alpha=0.5))

# Annotation with arrow
ax.annotate("Maximum", xy=(np.pi/2, 1), xytext=(np.pi/2 + 1, 0.8),
            fontsize=12, arrowprops=dict(arrowstyle="->", color="red"),
            color="red")

ax.annotate("Minimum", xy=(3*np.pi/2, -1), xytext=(3*np.pi/2 + 1, -0.8),
            fontsize=12, arrowprops=dict(arrowstyle="->", color="blue"),
            color="blue")

# Horizontal/vertical lines
ax.axhline(y=0, color="gray", linestyle="--", alpha=0.5)
ax.axvline(x=np.pi, color="gray", linestyle=":", alpha=0.5)

# Shaded region
ax.axvspan(np.pi/4, 3*np.pi/4, alpha=0.1, color="green")

ax.set_title("Annotated Sine Wave")
plt.show()
```

---

## Colormaps and Styling

### Colormaps

```python
# Available colormaps
# Sequential: viridis, plasma, inferno, magma, cividis
# Diverging: RdBu, coolwarm, seismic, PiYG
# Qualitative: Set1, Set2, tab10, tab20
# Cyclic: twilight, hsv

data = np.random.default_rng(42).random((10, 10))

fig, axes = plt.subplots(1, 3, figsize=(15, 4))

for ax, cmap in zip(axes, ["viridis", "RdBu_r", "plasma"]):
    im = ax.imshow(data, cmap=cmap)
    ax.set_title(cmap)
    plt.colorbar(im, ax=ax, shrink=0.8)

plt.tight_layout()
plt.show()
```

### Built-in Styles

```python
# List available styles
print(plt.style.available)

# Use a style
plt.style.use("seaborn-v0_8-whitegrid")

# Temporary style
with plt.style.context("ggplot"):
    plt.plot([1, 2, 3], [1, 4, 9])
    plt.title("ggplot style")
    plt.show()

# Common styles: default, seaborn-v0_8, ggplot, bmh, dark_background, fivethirtyeight
```

### Custom Style with rcParams

```python
# Global settings
plt.rcParams.update({
    "figure.figsize": (10, 6),
    "figure.dpi": 100,
    "font.size": 12,
    "font.family": "sans-serif",
    "axes.grid": True,
    "grid.alpha": 0.3,
    "lines.linewidth": 2,
})

# Reset to defaults
# plt.rcdefaults()
```

---

## 3D Plots

```python
from mpl_toolkits.mplot3d import Axes3D

# Surface plot
fig = plt.figure(figsize=(10, 7))
ax = fig.add_subplot(111, projection="3d")

x = np.linspace(-5, 5, 50)
y = np.linspace(-5, 5, 50)
X, Y = np.meshgrid(x, y)
Z = np.sin(np.sqrt(X**2 + Y**2))

surf = ax.plot_surface(X, Y, Z, cmap="viridis", alpha=0.8)
fig.colorbar(surf, shrink=0.5)
ax.set_xlabel("X")
ax.set_ylabel("Y")
ax.set_zlabel("Z")
ax.set_title("3D Surface")
plt.show()

# 3D scatter plot
fig = plt.figure()
ax = fig.add_subplot(111, projection="3d")

rng = np.random.default_rng(42)
x = rng.normal(0, 1, 200)
y = rng.normal(0, 1, 200)
z = rng.normal(0, 1, 200)
colors = np.sqrt(x**2 + y**2 + z**2)

ax.scatter(x, y, z, c=colors, cmap="plasma", alpha=0.6)
ax.set_title("3D Scatter")
plt.show()
```

---

## Saving Figures

```python
fig, ax = plt.subplots()
ax.plot([1, 2, 3], [1, 4, 9])
ax.set_title("Save Example")

# Save as PNG (raster)
fig.savefig("plot.png", dpi=150, bbox_inches="tight")

# Save as SVG (vector)
fig.savefig("plot.svg", bbox_inches="tight")

# Save as PDF (vector)
fig.savefig("plot.pdf", bbox_inches="tight")

# Options
fig.savefig("plot.png",
    dpi=300,                    # Resolution
    bbox_inches="tight",        # Crop whitespace
    facecolor="white",          # Background color
    transparent=False,          # Transparent background
    pad_inches=0.1              # Padding
)

plt.close(fig)  # Close to free memory

# Cleanup
import os
for f in ["plot.png", "plot.svg", "plot.pdf"]:
    if os.path.exists(f):
        os.remove(f)
```

---

## Practice Exercises

### Exercise 1: Multi-Panel Dashboard

```python
rng = np.random.default_rng(42)
months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
          "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
sales = rng.integers(50, 200, 12)
temps = [5, 7, 12, 18, 23, 27, 29, 28, 23, 17, 10, 6]
categories = rng.choice(["A", "B", "C"], 100)

fig, axes = plt.subplots(2, 2, figsize=(12, 8))

# Line chart
axes[0, 0].plot(months, sales, "o-", color="steelblue")
axes[0, 0].set_title("Monthly Sales")
axes[0, 0].tick_params(axis="x", rotation=45)

# Bar chart
axes[0, 1].bar(months, temps, color="coral")
axes[0, 1].set_title("Monthly Temperature")
axes[0, 1].tick_params(axis="x", rotation=45)

# Histogram
axes[1, 0].hist(rng.normal(50, 10, 500), bins=25, edgecolor="black")
axes[1, 0].set_title("Score Distribution")

# Pie chart
unique, counts = np.unique(categories, return_counts=True)
axes[1, 1].pie(counts, labels=unique, autopct="%1.0f%%")
axes[1, 1].set_title("Category Split")

plt.suptitle("Dashboard", fontsize=14, fontweight="bold")
plt.tight_layout()
plt.show()
```

### Exercise 2: Publication-Quality Figure

```python
x = np.linspace(0, 10, 100)
y1 = np.exp(-0.3 * x) * np.sin(2 * x)
y2 = np.exp(-0.3 * x) * np.cos(2 * x)
envelope = np.exp(-0.3 * x)

fig, ax = plt.subplots(figsize=(8, 5))

ax.plot(x, y1, "b-", linewidth=1.5, label=r"$e^{-0.3x}\sin(2x)$")
ax.plot(x, y2, "r--", linewidth=1.5, label=r"$e^{-0.3x}\cos(2x)$")
ax.plot(x, envelope, "k:", linewidth=1, alpha=0.5, label=r"$e^{-0.3x}$ envelope")
ax.plot(x, -envelope, "k:", linewidth=1, alpha=0.5)
ax.fill_between(x, -envelope, envelope, alpha=0.05, color="gray")

ax.set_xlabel("Time (s)", fontsize=12)
ax.set_ylabel("Amplitude", fontsize=12)
ax.set_title("Damped Oscillations", fontsize=14)
ax.legend(fontsize=10, framealpha=0.9)
ax.set_xlim(0, 10)
ax.grid(True, alpha=0.2)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)

plt.tight_layout()
plt.show()
```

---

## Summary

These notes cover the fundamental concepts of Matplotlib:

1. **Basic Plotting**: `plt.plot()`, labels, titles, legends, grids
2. **Plot Types**: Line, scatter, bar, histogram, box, violin, pie, heatmap, error bars
3. **Customization**: Colors, line styles, markers, fonts, axis limits, spines
4. **Subplots**: `plt.subplots()`, GridSpec, shared axes
5. **Axes Control**: Twin axes, inset axes, log scale, tick formatting
6. **Annotations**: Text, arrows, lines, shaded regions
7. **Styling**: Colormaps (viridis, RdBu, etc.), built-in styles, rcParams
8. **3D Plots**: Surface plots, 3D scatter via `mpl_toolkits.mplot3d`
9. **Saving**: PNG, SVG, PDF with DPI and layout control

### Next Steps

1. Explore Seaborn for statistical visualization built on Matplotlib
2. Learn Plotly or Bokeh for interactive web-based plots
3. Study animation with `matplotlib.animation`
4. Practice creating publication-quality figures with LaTeX labels
5. Explore Matplotlib widgets for interactive exploration

### Additional Resources

- **Matplotlib Documentation**: https://matplotlib.org/stable/
- **Gallery**: https://matplotlib.org/stable/gallery/
- **Cheat Sheets**: https://matplotlib.org/cheatsheets/
- **Tutorials**: https://matplotlib.org/stable/tutorials/
