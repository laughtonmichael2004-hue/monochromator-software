# Plotting of two sets of spectrum data, spectrum53V_081026.txt and spectrum53Va_081026.txt
# Plots the individual spectrum but also averages them
# Converts the photocurrent-angle plots to a photocurrent-wavelength plot
# Modified from code working on the same project available at 
# https://github.com/leagagneux11/Summer_2026_Internship/blob/main/2.%20Deuterium%20Lamp/Deuterium%20Lamp%20Analysis%20Code.ipynb


# Note: current reposoitory does not have data used on it

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

def actuator_angle_to_wavelength(theta_deg):
    # Equation 20 of Max's report: m * lambda = 2 * d * cos(phi) * sin(gamma * (theta - theta0))

    d = 835.5           # nm (1 / 1200 lines/mm)
    phi = 35            # degrees (half deviation angle)
    gamma = 1.00694     # NEW actuator scaling factor, Max's : 1.0028
    theta0 = -1.02898   # NEW degrees (angular offset), max's : 1.502
    m = 1               # first diffraction order

    theta_rad = np.radians(theta_deg)
    theta0_rad = np.radians(theta0)
    phi_rad = np.radians(phi)

    C = 2 * d * np.cos(phi_rad)  # ≈ 1365 nm

    wavelength = (C * np.sin(gamma * (theta_rad - theta0_rad))) / m

    return wavelength

# Main

save_fig = False

path_file1 = "spectrum53V_081026.txt"
path_file2 = "spectrum53Va_081026.txt"

try: 
    df1 = pd.read_csv(path_file1)
    df2 = pd.read_csv(path_file2)
except:
    print("One of the files failed to load.")
else:
    print(df1.head()) # Checks the file has loaded properly (needs a try, except)
    print(df2.head())

angle1 = df1["angle_deg"]
photocurrent1 = df1["current_mean_A"]
# photocurrent_std1 = df1["current_std_A"] / np.sqrt(df1["n_samples"]) # errors are negligible

wavelength_calibrated1 = actuator_angle_to_wavelength(angle1)

angle2 = df2["angle_deg"]
photocurrent2 = df2["current_mean_A"]
# photocurrent_std2 = df2["current_std_A"] / np.sqrt(df2["n_samples"]) # errors are negligible

wavelength_calibrated2 = actuator_angle_to_wavelength(angle2)

photocurrent_avg = (photocurrent1 + photocurrent2) / 2 # Averaging the photocurrents, assuming they have the same range of angles (I checked they do)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

# Plot 1 : Raw Data (angles)
ax1.plot(angle1, photocurrent1, 'b-', linewidth=1, label=f"{path_file1.rsplit('.', 1)[0]}")

ax1.plot(angle2, photocurrent2, 'm-', linewidth=1, label=f"{path_file2.rsplit('.', 1)[0]}")

ax1.plot(angle2, photocurrent_avg, 'g--', linewidth=1, label="Average")

ax1.set_xlabel('Actuator Angle (degrees)', fontsize=12)
ax1.set_ylabel('Photocurrent (A)', fontsize=12)
ax1.set_title('Raw Data: Photocurrent vs Angle', fontsize=14)
ax1.set_yscale('log')
ax1.grid(True, alpha=0.3)

ax1.legend()

# Plot 2 : Calibrated Spectrum
ax2.plot(wavelength_calibrated1, photocurrent1, 'r-', linewidth=1, label=f"{path_file1.rsplit('.', 1)[0]}")

ax2.plot(wavelength_calibrated2, photocurrent2, 'y-', linewidth=1, label=f"{path_file2.rsplit('.', 1)[0]}")

ax2.plot(wavelength_calibrated2, photocurrent_avg, 'g--', linewidth=1, label="Average")

ax2.set_xlabel('Wavelength (nm)', fontsize=12)
ax2.set_ylabel('Photocurrent (A)', fontsize=12)
ax2.set_title('Spectrum: Eq 20 Calibration', fontsize=14)
ax2.set_yscale('log')
ax2.grid(True, alpha=0.3)

ax2.legend()

plt.tight_layout()

# calibrated_spectrum_data = np.column_stack((wavelength_calibrated, photocurrent))

if save_fig:
    plt.savefig(f"{path_file1.rsplit('.', 1)[0]}_{path_file2.rsplit('.', 1)[0]}.png", dpi=600, bbox_inches='tight')
plt.show()