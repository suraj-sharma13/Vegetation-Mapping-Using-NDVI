import numpy as np
import rasterio
import matplotlib.pyplot as plt
import os

# Function to generate visualizations and save them
def generate_visualizations(ndvi, average_ndvi, output_dir):
    # Create a histogram of NDVI values
    plt.figure(figsize=(8, 6))
    plt.hist(ndvi.flatten(), bins=50, color='green', alpha=0.7)
    plt.xlabel("NDVI Value")
    plt.ylabel("Frequency")
    plt.title("Histogram of NDVI Values")
    plt.grid(True)
    hist_path = os.path.join(output_dir, "ndvi_histogram.png")
    plt.savefig(hist_path)
    plt.close()

    # Create a bar chart for average NDVI value
    categories = ["Category 1", "Category 2", "Category 3", "Category 4", "Category 5"]
    avg_ndvi_values = [average_ndvi, 0.25, 0.35, 0.6, 0.8]  # Placeholder values
    plt.figure(figsize=(8, 6))
    plt.bar(categories, avg_ndvi_values, color='blue', alpha=0.7)
    plt.xlabel("NDVI Category")
    plt.ylabel("Average NDVI Value")
    plt.title("Average NDVI Value by Category")
    plt.grid(True)
    avg_ndvi_path = os.path.join(output_dir, "average_ndvi_bar_chart.png")
    plt.savefig(avg_ndvi_path)
    plt.close()

    # Return paths of the created visualizations
    return hist_path, avg_ndvi_path

# Function to categorize average NDVI values into specific ranges
def categorize_ndvi(avg_ndvi):
    if avg_ndvi < 0:
        return "NDVI Range: -1 to 0\nWater Bodies or Barren Surfaces"
    elif avg_ndvi < 0.2:
        return "NDVI Range: 0 to 0.2\nNon-Vegetated or Sparse Vegetation (e.g., bare soil, urban areas)"
    elif avg_ndvi < 0.5:
        return "NDVI Range: 0.2 to 0.5\nShrublands, Grasslands, and Croplands (moderate vegetation cover)"
    elif avg_ndvi < 0.8:
        return "NDVI Range: 0.5 to 0.8\nDense and Healthy Vegetation (e.g., forests, rainforests)"
    else:
        return "NDVI Range: 0.8 to 1\nSaturated and Dense Vegetation (Rare)"

# Function to calculate NDVI statistics
def calculate_ndvi(red_path, nir_path):
    try:
        # Open the red band TIFF file
        with rasterio.open(red_path) as band4:
            # Read the red band data and convert it to float64 data type
            red = band4.read(1).astype('float64')
    except Exception as e:
        print(f"Error opening {red_path}: {e}")
        return None

    try:
        # Open the near-infrared (NIR) band TIFF file
        with rasterio.open(nir_path) as band5:
            # Read the NIR band data and convert it to float64 data type
            nir = band5.read(1).astype('float64')
    except Exception as e:
        print(f"Error opening {nir_path}: {e}")
        return None

    # Calculate NDVI using the formula: (NIR - Red) / (NIR + Red)
    ndvi = np.where(
        (nir + red) == 0.0,  # Handle cases where denominator is zero
        0.0,
        (nir - red) / (nir + red)
    )

    # Calculate average, minimum, and maximum NDVI values
    average_ndvi = np.mean(ndvi)
    min_ndvi = np.min(ndvi)
    max_ndvi = np.max(ndvi)

    # Categorize the average NDVI value
    ndvi_category = categorize_ndvi(average_ndvi)

    # Specify the output directory for saving visualizations
    output_directory = "C:/Users/Shavit/Desktop/Projects/Vegetation Mapping Using NDVI/Project Code/Visualizations"
    os.makedirs(output_directory, exist_ok=True)

    # Generate visualizations and save them
    hist_path, average_ndvi_path = generate_visualizations(ndvi, average_ndvi, output_directory)

    # Return values including category
    return str(average_ndvi), str(min_ndvi), str(max_ndvi), ndvi_category, hist_path, average_ndvi_path


