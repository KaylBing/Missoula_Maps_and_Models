import rasterio
from rasterio.merge import merge
from rasterio.plot import show
import matplotlib.pyplot as plt
import os
import numpy as np

# Directory containing your TIFF files
data_dir = "/home/mikhailu/Projects/Missoula_Maps_and_Models/data"

# Get a list of all TIFF files in the directory
tif_files = [os.path.join(data_dir, f) for f in os.listdir(data_dir) if f.endswith('.tif')]

# Open all TIFF files
src_files_to_mosaic = []
for file in tif_files:
    src = rasterio.open(file)
    src_files_to_mosaic.append(src)

# Merge the TIFF files in a memory-efficient way
mosaic, out_trans = merge(src_files_to_mosaic)

# Plot the merged raster in a memory-efficient way
plt.figure(figsize=(10, 10))
ax = plt.gca()

# Downsample the mosaic for visualization (reduce memory usage)
downsample_factor = 4  # Increase this to further reduce memory usage
mosaic_downsampled = mosaic[0, ::downsample_factor, ::downsample_factor]

# Calculate the extent of the downsampled raster
height, width = mosaic_downsampled.shape
extent = (
    out_trans[2],  # left
    out_trans[2] + out_trans[0] * width * downsample_factor,  # right
    out_trans[5] + out_trans[4] * height * downsample_factor,  # bottom
    out_trans[5],  # top
)

# Use imshow to display the downsampled raster
merged_plot = ax.imshow(mosaic_downsampled, cmap='terrain', extent=extent)

# Add a colorbar
plt.colorbar(merged_plot, ax=ax, label="Elevation (meters)")

# Add titles and labels
plt.title("Merged Raster for Missoula, Montana (Downsampled)")
plt.xlabel("Longitude")
plt.ylabel("Latitude")

# Show the map
plt.show()

# Close all source files to free up memory
for src in src_files_to_mosaic:
    src.close()