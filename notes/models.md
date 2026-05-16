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

---

## 3D_simple_subduction_isoviscous_1e20PaS.prm

Reference 3D subduction model without a slab edge. The model represents a simple subduction setup with an isoviscous mantle viscosity of 1e20 Pa·s.

**Objective:**
Provide a baseline model for comparison with slab-edge and toroidal-flow simulations.

---

## 3D_simple_subduction_isoviscous_1e20PaS_drip_zone_1e18PaS.prm

This model extends the baseline 3D subduction setup by introducing a localized low-viscosity region (1e18 Pa·s) beneath the lithosphere within an otherwise isoviscous mantle (1e20 Pa·s).

The weak zone is designed to promote the development of small-scale convection (SSC) while maintaining a simple subduction geometry without slab edges.

**Objective:**
To investigate the onset and evolution of small-scale convection (SSC) in the mantle and to quantify its interaction with large-scale subduction-driven flow.

**Key Processes Studied:**
- Geometry: 3D Cartesian domain
- Rheology: Isoviscous mantle
- Viscosity: 1e20 Pa·s
- Boundary conditions: Free-slip / prescribed velocity (depending on model)
- Small-scale convection (SSC) initiation beneath the lithosphere
- Interaction between SSC and background poloidal subduction flow
- Influence of localized viscosity reduction on mantle instability growth
- Comparison with slab-edge models to distinguish SSC from toroidal and edge-driven flow

**Notes:**
- No slab-edge geometry is included in this model
- Any lateral flow is driven by internal instabilities rather than slab-edge effects
- Serves as a controlled setup to isolate SSC dynamics from toroidal flow
- All models are implemented using ASPECT.
- Parameter files are located in `input-files/`.
- Visualization can be performed using ParaView.
