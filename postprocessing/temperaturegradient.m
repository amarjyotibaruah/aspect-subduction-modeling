%% ASPECT Initial Temperature Profile Plotter
%  Model: 3D subduction model  1800 x 900 x 660 km
%  Plots Depth (660-z) vs Temperature (K) at:
%    x = 200  km  -> Oceanic
%    x = 1400 km  -> Continental
%    x = 1700 km  -> Cratonic
%  Fixed:  y = 200 km  (< ytf = 500 km, so "front" half-space branch)
%
%  All spatial constants from the .prm file are in metres.
%  The depth axis is defined as  depth = 660 km - z  (surface = 0 km).

clear; clc; close all;

%% ── Constants from .prm ──────────────────────────────────────────────────
Ax   = 800e3;      % x boundary oceanic/continental  [m]
Az   = 660e3;      % model height                    [m]
sd   = 360e3;      % slab depth threshold            [m]
r    = 600e3;      % slab radius                     [m]
ccb  = 1600e3;     % continental-craton boundary     [m]

ocd  = 652.5e3;    % oceanic crust base              [m]
omd  = 590e3;      % oceanic mantle lithosphere base [m]

ud   = 650e3;      % upper crust base                [m]
ld   = 625e3;      % lower crust base                [m]
cmd  = 600e3;      % CMLU base                       [m]

T0   = 273;        % surface temperature             [K]
Ts1  = 537;        % temperature step 1              [K]
Ts2  = 1108;       % temperature step 2              [K]
Ts3  = 416;        % temperature step 3              [K]
Ts4  = 557;        % temperature step 4              [K]
Ts5  = 354;        % temperature step 5              [K]

A1   = 1.10e-6;    % heat production 1  [W/m^3 / (W/m/K)] -> K/m^2
A2   = 0.4e-6;
k1   = 2.5;        % thermal conductivity [W/m/K]
k2   = 2.5;

qs1    = 0.0715;   % surface heat flow values [W/m^2]
qscr1  = 0.0258;
qs2    = 0.0621;
qs3    = 0.0489;
qs4    = 0.0253;
qs5    = 0.04767;
qs_cmlc= 0.017;

ytf  = 500e3;      % transform fault y-position [m]

%% ── Sampling grid ────────────────────────────────────────────────────────
% z runs from 0 (bottom) to 660 km (surface) in the ASPECT convention.
% We sample densely near the lithosphere (high z) where gradients are steep.
z_vec  = linspace(0, 660e3, 5000);   % z in metres
y      = 200e3;                        % fixed y = 200 km  (<  ytf)

x_vals = [200e3, 1400e3, 1700e3];
labels = {'Oceanic  (x = 200 km)', ...
          'Continental  (x = 1400 km)', ...
          'Cratonic  (x = 1700 km)'};
colors = {'#1f77b4', '#d62728', '#2ca02c'};   % blue, red, green

%% ── Temperature function (y ≤ ytf branch) ───────────────────────────────
function T = aspect_T(x, y, z, ...
        Ax, Az, sd, r, ccb, ocd, omd, ud, ld, cmd, ...
        T0, Ts1, Ts2, Ts3, Ts4, Ts5, ...
        A1, A2, k1, k2, ...
        qs1, qscr1, qs2, qs3, qs4, qs5, qs_cmlc, ytf)

    % Mantle adiabat (fallback everywhere)
    T_adiabat = 1325 + 273 + 0.4*(660 - z/1000);

    % Distance from slab axis (used for slab geometry)
    dist = sqrt((x - Ax)^2 + (Az - r - z)^2);

    if y > ytf
        % ── Back half-space (not used here, included for completeness) ──
        T = T_adiabat;   % simplified – user's y=200 never enters this branch

    else
        % ── Front half-space (y ≤ ytf) ──────────────────────────────────

        % 1. Oceanic crust/lithosphere  (x ≤ Ax, front half)
        if x <= Ax
            if z >= ocd
                T = qs5*(660e3 - z)/k1 + T0;
            elseif z >= omd
                T = qs5*(ocd - z)/k2 + Ts3;
            else
                T = T_adiabat;
            end

        % 2. Slab geometry (x ≥ Ax, inside slab radius, front half)
        elseif x >= Ax && z >= sd && dist <= r && dist >= (r - (Az - ocd))
            % Oceanic crust part of slab
            T = qs5*(r - dist)/k1 + T0;

        elseif x >= Ax && z >= sd && dist < (r - (Az - ocd)) && dist >= (r - (Az - omd))
            % Oceanic mantle part of slab
            T = qs5*((r - (Az - ocd)) - dist)/k2 + Ts3;

        % 3. Continental lithosphere between Ax and ccb (outside slab)
        elseif x > Ax && x < ccb && (dist > r || y > ytf)
            if z >= ud
                T = -A1*(660e3 - z)^2/(2*k1) + qs1*(660e3 - z)/k1 + T0;
            elseif z >= ld
                T = -A2*(ud - z)^2/(2*k1) + qs2*(ud - z)/k1 + Ts1;
            elseif z >= cmd
                T = qs3*(ld - z)/k1 + Ts2;
            else
                T = T_adiabat;
            end

        % 4. Cratonic lithosphere (x ≥ ccb, outside slab)
        elseif x >= ccb && x <= 1800e3 && (dist > r || y > ytf)
            if z >= ud
                T = -A1*(660e3 - z)^2/(2*k1) + qscr1*(660e3 - z)/k1 + T0;
            elseif z >= ld
                T = -A2*(ud - z)^2/(2*k1) + qs4*(ud - z)/k1 + Ts5;
            elseif z >= 460e3 && z < 625e3
                T = qs_cmlc*(625e3 - z)/k1 + Ts4;
            else
                T = T_adiabat;
            end

        else
            T = T_adiabat;
        end
    end
end

%% ── Evaluate temperature along each profile ──────────────────────────────
T_profiles = zeros(length(x_vals), length(z_vec));

for ix = 1:length(x_vals)
    x = x_vals(ix);
    for iz = 1:length(z_vec)
        z = z_vec(iz);
        T_profiles(ix, iz) = aspect_T(x, y, z, ...
            Ax, Az, sd, r, ccb, ocd, omd, ud, ld, cmd, ...
            T0, Ts1, Ts2, Ts3, Ts4, Ts5, ...
            A1, A2, k1, k2, ...
            qs1, qscr1, qs2, qs3, qs4, qs5, qs_cmlc, ytf);
    end
end

%% ── Convert z to depth (km) ──────────────────────────────────────────────
depth_km = (660e3 - z_vec) / 1e3;   % depth = 660 - z, in km

%% ── Plot ─────────────────────────────────────────────────────────────────
fig = figure('Color','w','Position',[100 100 700 820]);

hold on; box on; grid on;

for ix = 1:length(x_vals)
    plot(T_profiles(ix,:), depth_km, ...
        'Color', colors{ix}, ...
        'LineWidth', 2.2, ...
        'DisplayName', labels{ix});
end

% Reference lines for key layer boundaries (depth = 660 - z)
layer_z   = [ocd, omd, ud, ld, cmd, 460e3] / 1e3;      % z in km
layer_d   = 660 - layer_z;                               % depth in km
layer_lbl = {'OC base (7.5 km)', 'OML base (70 km)', ...
             'UC base (10 km)',   'LC base (35 km)', ...
             'CMLU base (60 km)','CMLC base (200 km)'};
lcolors   = {[.5 .5 .5],[.5 .5 .5],[.8 .6 0],[.8 .6 0],[0 .6 .6],[0 .6 .6]};
lstyles   = {'--',':','--',':','--',':'};

for ii = 1:length(layer_d)
    xline(NaN);   % dummy for legend spacing (optional)
    yline(layer_d(ii), lstyles{ii}, 'Color', lcolors{ii}, ...
          'LineWidth', 0.8, 'Alpha', 0.6, ...
          'HandleVisibility','off');
end

% Axes formatting
set(gca, 'YDir','reverse', 'FontSize', 13, 'TickDir','out', ...
    'XAxisLocation','bottom');
ylim([0 660]);
xlim([200 2000]);

xlabel('Temperature  (K)', 'FontSize', 14, 'FontWeight', 'bold');
ylabel('Depth  (km)', 'FontSize', 14, 'FontWeight', 'bold');
title({'ASPECT Initial Temperature Profiles', ...
       sprintf('y = 200 km  (y \\leq y_{tf} = 500 km)')}, ...
      'FontSize', 14);

legend('Location','southeast','FontSize',11,'Box','on');

% Annotate layer boundaries on right margin
ax = gca;
for ii = 1:length(layer_d)
    text(ax.XLim(2)*0.99, layer_d(ii), ...
         sprintf('  %s', layer_lbl{ii}), ...
         'FontSize', 7, 'Color', lcolors{ii}, ...
         'HorizontalAlignment','right','VerticalAlignment','bottom', ...
         'Clipping','on');
end

%% ── Save figure ──────────────────────────────────────────────────────────
exportgraphics(fig, 'temperature_profiles.png', 'Resolution', 200);
fprintf('Figure saved to temperature_profiles.png\n');
