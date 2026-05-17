# aspect_flow_visualization.py

import numpy as np
import pyvista as pv
import matplotlib.pyplot as plt
from scipy.interpolate import griddata
from scipy.spatial import cKDTree
import os


# =========================
# USER SETTINGS
# =========================

VTU_FILE = "solution-00010.vtu"   # change this
OUTPUT_DIR = "flow_figures"

# model dimensions in metres
X_MIN, X_MAX = 0, 2.5e6
Y_MIN, Y_MAX = 0, 9.0e5
Z_MIN, Z_MAX = 0, 6.6e5

# back-arc analysis region
X_RANGE = (1.0e6, 1.8e6)
Y_RANGE = (0.0, 5.0e5)

# fixed depth slices, in km
DEPTH_SLICES_KM = [100, 150, 200, 250, 300]

# temperature mask
# exclude cold slab/slab-adjacent material
T_CUTOFF = 1300 + 273.15   # Kelvin

# LAB isotherm
LAB_ISOTHERM = 1300 + 273.15   # Kelvin

# slab edge position in y direction
SLAB_EDGE_Y = 0.0

# bin width for distance-from-slab-edge plot
Y_BIN_WIDTH = 100e3

EPS = 1e-30

os.makedirs(OUTPUT_DIR, exist_ok=True)


# =========================
# READ VTU FILE
# =========================

mesh = pv.read(VTU_FILE)

points = mesh.points
x = points[:, 0]
y = points[:, 1]
z = points[:, 2]

print("Available point arrays:")
print(mesh.point_data.keys())

# You may need to rename these depending on your ASPECT output
velocity = mesh.point_data["velocity"]
temperature = mesh.point_data["T"]

vx = velocity[:, 0]
vy = velocity[:, 1]
vz = velocity[:, 2]


# =========================
# HELPER FUNCTION
# nearest-neighbour derivative
# =========================

def estimate_gradient(points, values, k=20):
    """
    Estimate spatial gradient of a scalar field using local least squares.
    Returns dvalue/dx, dvalue/dy, dvalue/dz.
    """

    tree = cKDTree(points)
    gradients = np.zeros((len(points), 3))

    for i, p in enumerate(points):
        _, idx = tree.query(p, k=k)

        P = points[idx] - p
        V = values[idx] - values[i]

        grad, _, _, _ = np.linalg.lstsq(P, V, rcond=None)
        gradients[i, :] = grad

    return gradients


print("Calculating velocity gradients...")

grad_vx = estimate_gradient(points, vx)
grad_vy = estimate_gradient(points, vy)
grad_vz = estimate_gradient(points, vz)

dvx_dx, dvx_dy, dvx_dz = grad_vx[:, 0], grad_vx[:, 1], grad_vx[:, 2]
dvy_dx, dvy_dy, dvy_dz = grad_vy[:, 0], grad_vy[:, 1], grad_vy[:, 2]
dvz_dx, dvz_dy, dvz_dz = grad_vz[:, 0], grad_vz[:, 1], grad_vz[:, 2]


# =========================
# VORTICITY
# =========================

omega_x = dvz_dy - dvy_dz
omega_y = dvx_dz - dvz_dx
omega_z = dvy_dx - dvx_dy

# Common proxy:
# toroidal = vertical-axis rotation
# poloidal = rotation in vertical planes
omega_toroidal_sq = omega_z**2
omega_poloidal_sq = omega_x**2 + omega_y**2

R = omega_toroidal_sq / (omega_poloidal_sq + EPS)

print("Finished vorticity calculation.")


# =========================
# BASIC MASKS
# =========================

region_mask = (
    (x >= X_RANGE[0]) & (x <= X_RANGE[1]) &
    (y >= Y_RANGE[0]) & (y <= Y_RANGE[1])
)

temperature_mask = temperature > T_CUTOFF

mantle_mask = region_mask & temperature_mask


# =========================
# 1. DEPTH-SLICE MAPS
# =========================

def plot_depth_slice(depth_km):
    depth_m = depth_km * 1e3

    slice_thickness = 10e3

    mask = (
        mantle_mask &
        (np.abs(z - depth_m) <= slice_thickness)
    )

    xi = np.linspace(X_RANGE[0], X_RANGE[1], 250)
    yi = np.linspace(Y_RANGE[0], Y_RANGE[1], 250)
    XI, YI = np.meshgrid(xi, yi)

    RI = griddata(
        (x[mask], y[mask]),
        np.log10(R[mask] + EPS),
        (XI, YI),
        method="linear"
    )

    plt.figure(figsize=(8, 5))
    plt.pcolormesh(XI / 1e3, YI / 1e3, RI, shading="auto")
    plt.colorbar(label=r"$\log_{10}(\Omega_T^2 / \Omega_P^2)$")
    plt.xlabel("X distance (km)")
    plt.ylabel("Y distance from slab edge (km)")
    plt.title(f"Toroidal/Poloidal Ratio at {depth_km} km Depth")
    plt.tight_layout()

    outfile = f"{OUTPUT_DIR}/R_depth_{depth_km}km.png"
    plt.savefig(outfile, dpi=300)
    plt.close()

    print(f"Saved {outfile}")


for d in DEPTH_SLICES_KM:
    plot_depth_slice(d)


# =========================
# 2. DISTANCE FROM SLAB EDGE PROFILE
# =========================

def plot_y_binned_profile(depth_range_km=(100, 300)):
    zmin = depth_range_km[0] * 1e3
    zmax = depth_range_km[1] * 1e3

    mask = mantle_mask & (z >= zmin) & (z <= zmax)

    distance_from_edge = np.abs(y - SLAB_EDGE_Y)

    bins = np.arange(Y_RANGE[0], Y_RANGE[1] + Y_BIN_WIDTH, Y_BIN_WIDTH)

    bin_centres = []
    mean_R = []
    rms_toroidal = []
    rms_poloidal = []

    for i in range(len(bins) - 1):
        b0, b1 = bins[i], bins[i + 1]

        bmask = mask & (distance_from_edge >= b0) & (distance_from_edge < b1)

        if np.sum(bmask) < 10:
            continue

        bin_centres.append((b0 + b1) / 2 / 1e3)

        mean_R.append(np.nanmean(R[bmask]))

        rms_toroidal.append(np.sqrt(np.nanmean(omega_toroidal_sq[bmask])))
        rms_poloidal.append(np.sqrt(np.nanmean(omega_poloidal_sq[bmask])))

    plt.figure(figsize=(7, 5))
    plt.plot(bin_centres, mean_R, marker="o")
    plt.axhline(1, linestyle="--")
    plt.yscale("log")
    plt.xlabel("Distance from slab edge, Y (km)")
    plt.ylabel(r"Mean $\Omega_T^2 / \Omega_P^2$")
    plt.title(f"Toroidal/Poloidal Ratio, {depth_range_km[0]}-{depth_range_km[1]} km")
    plt.tight_layout()

    outfile = f"{OUTPUT_DIR}/R_vs_distance_from_slab_edge.png"
    plt.savefig(outfile, dpi=300)
    plt.close()

    print(f"Saved {outfile}")


plot_y_binned_profile(depth_range_km=(100, 300))


# =========================
# 3. TEMPERATURE SLICE WITH VELOCITY ARROWS
# =========================

def plot_temperature_velocity_slice(depth_km):
    depth_m = depth_km * 1e3
    slice_thickness = 10e3

    mask = (
        region_mask &
        (np.abs(z - depth_m) <= slice_thickness)
    )

    xi = np.linspace(X_RANGE[0], X_RANGE[1], 200)
    yi = np.linspace(Y_RANGE[0], Y_RANGE[1], 200)
    XI, YI = np.meshgrid(xi, yi)

    TI = griddata(
        (x[mask], y[mask]),
        temperature[mask] - 273.15,
        (XI, YI),
        method="linear"
    )

    VXI = griddata(
        (x[mask], y[mask]),
        vx[mask],
        (XI, YI),
        method="linear"
    )

    VYI = griddata(
        (x[mask], y[mask]),
        vy[mask],
        (XI, YI),
        method="linear"
    )

    plt.figure(figsize=(8, 5))
    plt.pcolormesh(XI / 1e3, YI / 1e3, TI, shading="auto")
    plt.colorbar(label="Temperature (°C)")

    step = 15
    plt.quiver(
        XI[::step, ::step] / 1e3,
        YI[::step, ::step] / 1e3,
        VXI[::step, ::step],
        VYI[::step, ::step],
        scale=1e-8
    )

    plt.xlabel("X distance (km)")
    plt.ylabel("Y distance from slab edge (km)")
    plt.title(f"Temperature + Horizontal Velocity at {depth_km} km")
    plt.tight_layout()

    outfile = f"{OUTPUT_DIR}/temperature_velocity_{depth_km}km.png"
    plt.savefig(outfile, dpi=300)
    plt.close()

    print(f"Saved {outfile}")


plot_temperature_velocity_slice(150)


# =========================
# 4. LAB DEPTH MAP
# =========================

def plot_lab_depth_map():
    mask = region_mask

    xi = np.linspace(X_RANGE[0], X_RANGE[1], 200)
    yi = np.linspace(Y_RANGE[0], Y_RANGE[1], 200)

    LAB = np.full((len(yi), len(xi)), np.nan)

    for i, xx in enumerate(xi):
        for j, yy in enumerate(yi):

            local_mask = (
                mask &
                (np.abs(x - xx) < 10e3) &
                (np.abs(y - yy) < 10e3)
            )

            if np.sum(local_mask) < 5:
                continue

            zz = z[local_mask]
            TT = temperature[local_mask]

            order = np.argsort(zz)
            zz = zz[order]
            TT = TT[order]

            # find first depth where T exceeds LAB isotherm
            above = np.where(TT >= LAB_ISOTHERM)[0]

            if len(above) > 0:
                LAB[j, i] = zz[above[0]] / 1e3

    XI, YI = np.meshgrid(xi, yi)

    plt.figure(figsize=(8, 5))
    plt.pcolormesh(XI / 1e3, YI / 1e3, LAB, shading="auto")
    plt.colorbar(label="LAB depth from 1300°C isotherm (km)")
    plt.xlabel("X distance (km)")
    plt.ylabel("Y distance from slab edge (km)")
    plt.title("Thermal LAB Depth Map")
    plt.tight_layout()

    outfile = f"{OUTPUT_DIR}/LAB_depth_map.png"
    plt.savefig(outfile, dpi=300)
    plt.close()

    print(f"Saved {outfile}")


plot_lab_depth_map()

print("All figures created.")
