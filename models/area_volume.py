import cv2
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import os

def calculate_area_volume(image_path):
    """
    Calculate the area and estimate volume of waterbodies from satellite imagery
    """
    # Read the image
    img = cv2.imread(image_path)
    if img is None:
        raise ValueError(f"Failed to load image: {image_path}")
    
    # Convert BGR to RGB (OpenCV loads as BGR)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    
    # Convert to RGB if necessary
    if len(img.shape) == 2:
        img = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)
    
    # Extract water regions using a more robust method for RGB images
    blue_band = img[:, :, 2].astype(float)
    green_band = img[:, :, 1].astype(float)
    red_band = img[:, :, 0].astype(float)
    
    # Modified normalized difference water index (for RGB images)
    ndwi = (green_band - red_band) / (green_band + red_band + 1e-10)
    
    # Use blue/red ratio to enhance water detection (water reflects more blue light)
    blue_red_ratio = blue_band / (red_band + 1e-10)
    
    # Adjust for HSV color space which can better isolate water in certain conditions
    hsv = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)
    h, s, v = cv2.split(hsv)
    
    # Create masks for different types of water bodies (light/dark/mid-blue)
    # Lower NDWI threshold to catch more water bodies
    water_mask1 = (ndwi > 0.05) & (blue_red_ratio > 1.3) & (blue_band > 80)
    
    # Additional mask for darker water (like some of the Great Lakes)
    # These often have lower brightness but still high blue content proportionally
    water_mask2 = (blue_band > red_band + 15) & (blue_band > green_band) & (v < 150) & (s > 30)
    
    # Combine masks
    water_mask = water_mask1 | water_mask2
    
    # Apply morphological operations to clean up the mask
    kernel = np.ones((5, 5), np.uint8)
    water_mask = cv2.morphologyEx(water_mask.astype(np.uint8), cv2.MORPH_OPEN, kernel)
    water_mask = cv2.morphologyEx(water_mask, cv2.MORPH_CLOSE, kernel)
    
    # Additional closing with larger kernel to connect nearby water bodies
    kernel_large = np.ones((9, 9), np.uint8)
    water_mask = cv2.morphologyEx(water_mask, cv2.MORPH_CLOSE, kernel_large)
    
    # Remove small noise regions
    contours, _ = cv2.findContours(water_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for cnt in contours:
        if cv2.contourArea(cnt) < 100:  # Adjust threshold as needed
            cv2.drawContours(water_mask, [cnt], 0, 0, -1)
    
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
    
    # Create a colored overlay for water bodies
    overlay = np.zeros_like(img)
    overlay[water_mask == 1] = [0, 0, 255]  # Blue for water
    
    # Blend original and overlay
    alpha = 0.5
    visualization = cv2.addWeighted(img, 1, overlay, alpha, 0)
    
    # Outline water bodies
    contours, _ = cv2.findContours(water_mask.astype(np.uint8), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cv2.drawContours(visualization, contours, -1, (0, 255, 255), 2)  # Yellow outline
    
    # Save processed image with a unique name based on the original filename
    base_name = os.path.basename(image_path)
    filename, ext = os.path.splitext(base_name)
    processed_filename = f"{filename}_processed{ext}"
    processed_path = os.path.join(os.path.dirname(image_path), processed_filename)
    
    # Convert RGB to BGR for saving with OpenCV
    cv2.imwrite(processed_path, cv2.cvtColor(visualization, cv2.COLOR_RGB2BGR))
    
    return {
        'water_area_sq_meters': float(area_sq_meters),
        'water_area_sq_km': float(area_sq_km),
        'estimated_volume_cubic_meters': float(volume_cubic_meters),
        'pixel_count': int(pixel_count),
        'processed_image': processed_path
    } 