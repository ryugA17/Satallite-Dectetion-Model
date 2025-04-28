import cv2
import numpy as np
from skimage import io, color
import rasterio
import matplotlib.pyplot as plt
from PIL import Image

def calculate_area_volume(image_path):
    """
    Calculate the area and estimate volume of waterbodies from satellite imagery
    """
    # Read the image
    img = io.imread(image_path)
    
    # Convert to RGB if necessary
    if len(img.shape) == 2:
        img = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)
    
    # Extract water regions using NDWI (Normalized Difference Water Index)
    # For actual satellite imagery, you would use specific bands (green and NIR)
    green = img[:, :, 1].astype(float)
    nir = img[:, :, 0].astype(float)  # Using red as proxy for NIR in RGB images
    ndwi = (green - nir) / (green + nir + 1e-10)
    
    # Create water mask using threshold
    water_mask = ndwi > 0.1
    
    # Calculate area (in pixels)
    pixel_count = np.sum(water_mask)
    
    # For actual applications, you would convert pixel area to real-world units
    # using the image's spatial resolution (e.g., 10m/pixel for Sentinel-2)
    # This is a simplified example assuming 30m/pixel (Landsat-like)
    pixel_size = 30 * 30  # square meters per pixel
    area_sq_meters = pixel_count * pixel_size
    area_sq_km = area_sq_meters / 1000000
    
    # Simple volume estimation based on area and assumed average depth
    # In real applications, you would use DEM/bathymetry data
    # This is a very simplified model
    avg_depth = 3  # meters (arbitrary example value)
    volume_cubic_meters = area_sq_meters * avg_depth
    
    # Create visualization
    visualization = img.copy()
    # Create a semi-transparent overlay
    overlay = np.zeros_like(img)
    overlay[water_mask] = [0, 0, 255]  # Blue for water
    
    # Blend original and overlay
    alpha = 0.5
    visualization = cv2.addWeighted(img, 1, overlay, alpha, 0)
    
    # Outline water bodies
    contours, _ = cv2.findContours(water_mask.astype(np.uint8), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cv2.drawContours(visualization, contours, -1, (255, 255, 0), 2)
    
    # Save processed image
    processed_path = image_path.replace('.', '_processed.')
    Image.fromarray(visualization).save(processed_path)
    
    return {
        'water_area_sq_meters': float(area_sq_meters),
        'water_area_sq_km': float(area_sq_km),
        'estimated_volume_cubic_meters': float(volume_cubic_meters),
        'pixel_count': int(pixel_count),
        'processed_image': processed_path
    } 