# Post-processing Workflows

This folder contains example scripts used to analyze outputs from ASPECT geodynamic models.

## aspect.py

This script processes ASPECT `.vtu` output files to analyze mantle flow patterns.

### Capabilities

- Reads ASPECT model output
- Extracts velocity and temperature fields
- Computes velocity gradients and vorticity
- Estimates toroidal and poloidal flow components
- Generates depth-dependent flow maps
- Produces visualization figures for interpretation

### Purpose

This script demonstrates how numerical model outputs are transformed into physically meaningful quantities such as flow structure, convection patterns, and lithosphere-asthenosphere boundary characteristics.

### Note

This is a representative post-processing workflow. Full analysis pipelines are part of ongoing research work. 
