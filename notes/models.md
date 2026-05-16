# Model Descriptions

This document provides a brief overview of the numerical models included in this repository.

---

## Slab-Edge Toroidal Flow Model (Isoviscous, 1e20 Pa·s)

This model simulates a 3D subduction system with a finite slab geometry to investigate toroidal mantle flow around slab edges. The mantle is treated as isoviscous with a viscosity of 1e20 Pa·s.

**Objective:**
To analyze how slab edges generate lateral (toroidal) flow patterns in the mantle.

---

## Double Toroidal Flow Model (Isoviscous, 1e20 Pa·s)

This model extends the slab geometry to generate symmetric toroidal flow on both sides of the slab.

**Objective:**
To study interaction between dual slab edges and resulting mantle circulation patterns.

---

## Slab-Edge Toroidal Flow Model with Weak Dip Zone

This model builds on the 3D slab-edge toroidal flow setup by adding a lower-viscosity dip zone with viscosity of 1e18 Pa·s, while the background isoviscous mantle viscosity is 1e20 Pa·s.

**Objective:**
To test how localized weakening along the dipping slab/interface region affects slab-edge flow, coupling, and mantle circulation.

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
