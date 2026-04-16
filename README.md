# Surface-Roughness-Analysis
# Surface Roughness Analysis — Roughness Profile Toolkit

A Python toolkit for loading, analysing, and visualising surface 
roughness measurement data. Achieved a grade of 78% on this coursework.

## Overview

Processes multi-sample roughness profile data (X/Y measurements) to 
compute surface roughness metrics and compare samples visually.

## Features

**Data Inspection**
- Loads roughness profile CSV data and reports structure
- Interactive row-level inspection of raw measurements

**Sample Management**
- Extracts sample ID range from dataset
- Loads individual sample profiles by ID

**Ra Calculation**
- Computes arithmetic mean roughness (Ra) — the mean absolute deviation 
  of surface height from the profile mean
- Exports per-sample results to CSV

**Visualisation**
- Line plots of individual roughness profiles with mean line overlay
- Bar chart comparison of Ra values across all samples

**Object-Oriented Implementation**
- `RoughnessProfile` class encapsulating sample data, Ra computation, 
  plotting, and property accessors/mutators

## Dependencies

```bash
pip install numpy matplotlib
```

## Files

| File | Description |
|------|-------------|
| `Template.py` | Full implementation — all questions |
| `Data.csv` | Raw roughness profile measurements |
