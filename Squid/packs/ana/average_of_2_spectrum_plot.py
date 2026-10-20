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

# Make a function that will read each file and plot it, then average with all other data to then plot the average spectrum. 
# Initially the function will take a list of file paths, but then later modify to scrape the directory for all files with a 
# certain name pattern (e.g. spectrum*.txt) and then plot all of them and average them.
# Will either use .glob or will see what .pathlib can do.

# Will need some test data...

# Main

# First , will just hardcode a list of the file paths for now, then later will modify to scrape the directory 
# for all files with a certain name pattern (e.g. spectrum*.txt) and then plot all of them and average them.

save_fig = False
counter = 0
total_sum_photocurrent = []

# Need to define the prefix and suffix before use, used to strip file name to only the identifiable component
path_prefix = "C:\\Users\\laugh\\Documents\\MPhys_Projects_Code\\D2lamp_128nm_stability_(08-10-2026)\\"
path_suffix = ".txt"

path_file1 = "C:\\Users\\laugh\\Documents\\MPhys_Projects_Code\\D2lamp_128nm_stability_(08-10-2026)\\spectrum53V_081026.txt"
path_file2 = "C:\\Users\\laugh\\Documents\\MPhys_Projects_Code\\D2lamp_128nm_stability_(08-10-2026)\\spectrum53Va_081026.txt"

path_files = [path_file1, path_file2]

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

# Assume file format as follows: angle_deg,epos,current_mean_A,current_std_A,n_samples
for path_file in path_files:
    try:
        trimmed_path_file = path_file.lstrip(path_prefix).rstrip(path_suffix)

        df = pd.read_csv(path_file)

        angle = df["angle_deg"]
        photocurrent = df["current_mean_A"]
        photocurrent_std = df["current_std_A"] / np.sqrt(df["n_samples"]) # errors are negligible

        wavelength_calibrated = actuator_angle_to_wavelength(angle)

        # Plot 1 : Raw Data (angles)
        ax1.errorbar(angle, photocurrent, yerr=photocurrent_std, fmt='.',label=f"{trimmed_path_file}", zorder=1)

        # Plot 2 : Calibrated Spectrum
        # Will the error be affected by the calibration? I think not, as the calibration is a function of angle, which is a constant for each data point. 
        # So the error should remain the same.

        ax2.errorbar(wavelength_calibrated, photocurrent, yerr=photocurrent_std, fmt='.',label=f"{trimmed_path_file}", zorder=1)

        if counter == 0:
            total_sum_photocurrent = photocurrent
            counter += 1
        else:
            total_sum_photocurrent += photocurrent

    except:
        print(f"File {path_file} failed to load.")
    #else:
        #print(df.head()) # Checks the file has loaded properly (needs a try, except)

photocurrent_avg = total_sum_photocurrent / (len(path_files))

ax1.plot(angle, photocurrent_avg, 'r-', linewidth=1, label="Average", zorder=2)
ax2.plot(wavelength_calibrated, photocurrent_avg, 'r-', linewidth=1, label="Average")

ax1.set_xlabel('Actuator Angle (degrees)', fontsize=12)
ax1.set_ylabel('Photocurrent (A)', fontsize=12)
ax1.set_title('Raw Data: Photocurrent vs Angle', fontsize=14)
ax1.set_yscale('log')
ax1.grid(True, alpha=0.3)

ax1.legend()

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