# Post-processing Workflows

This folder contains representative scripts used to analyze outputs from ASPECT geodynamic simulations and extract physically meaningful quantities related to mantle flow and thermal structure.

---

## Python Script

### aspect.py

This script processes ASPECT `.vtu` output files to analyze mantle flow patterns in 3D subduction models.

### Capabilities

- Reads ASPECT model output using Python-based tools
- Extracts velocity and temperature fields
- Computes velocity gradients and vorticity
- Estimates toroidal and poloidal flow contributions
- Generates depth-dependent flow maps
- Produces visualization figures for interpretation

### Purpose

This script demonstrates how numerical model outputs are transformed into physically meaningful quantities such as mantle circulation patterns, flow partitioning (toroidal vs poloidal), and convection structure.

---

## MATLAB Script

### temperaturegradient.m

This script reconstructs and visualizes temperature profiles from the ASPECT model setup.

### Capabilities

- Uses thermal parameters consistent with ASPECT model configuration
- Computes temperature variation with depth
- Compares temperature profiles across different lithospheric domains
  - oceanic region
  - continental region
  - cratonic region
- Plots temperature vs depth for each domain
- Highlights key thermal gradients and lithospheric structure

### Purpose

This script is used to verify and interpret the initial thermal structure of the model, and to compare geotherms across different tectonic settings prior to or alongside full simulation analysis.

---

## Overall Purpose

Together, these scripts demonstrate a complete post-processing workflow for:

- Extracting physical insight from numerical models
- Quantifying mantle flow behavior
- Analyzing thermal structure and lithosphere-asthenosphere interactions

---

## Note

These scripts are representative examples of post-processing workflows. Full analysis pipelines and model-specific configurations are part of ongoing research work.
