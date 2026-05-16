# Model Descriptions

This document provides a brief overview of the numerical models included in this repository.

---

## 1. Slab-Edge Toroidal Flow Model (Isoviscous, 1e20 Pa·s)

This model simulates a 3D subduction system with a finite slab geometry to investigate toroidal mantle flow around slab edges. The mantle is treated as isoviscous with a viscosity of 1e20 Pa·s.

**Objective:**
To analyze how slab edges generate lateral (toroidal) flow patterns in the mantle.

---

## 2. Double Toroidal Flow Model (Isoviscous, 1e20 Pa·s)

This model extends the slab geometry to generate symmetric toroidal flow on both sides of the slab.

**Objective:**
To study interaction between dual slab edges and resulting mantle circulation patterns.

---

## Key Parameters Across Models

- Geometry: 3D Cartesian domain
- Rheology: Isoviscous mantle
- Viscosity: 1e20 Pa·s
- Boundary conditions: Free-slip / prescribed velocity (depending on model)

---

## Notes

- All models are implemented using ASPECT.
- Parameter files are located in `input-files/`.
- Visualization can be performed using ParaView.
