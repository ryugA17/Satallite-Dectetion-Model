import cv2
import numpy as np
from PIL import Image
import os

def estimate_water_quality(image_path):
    """
    Estimate water quality parameters from satellite imagery
    Returns water quality metrics and processed image
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
    
    # Extract water regions using NDWI (Normalized Difference Water Index)
    # This is a simplified version - in practice, you'd use specific band combinations
    green = img[:, :, 1].astype(float)
    nir = img[:, :, 0].astype(float)
    ndwi = (green - nir) / (green + nir + 1e-10)
    
    # Create water mask
    water_mask = ndwi > 0.1
    
    # Calculate water quality parameters
    # 1. Turbidity estimation (using red band)
    red_band = img[:, :, 0].astype(float)
    turbidity = np.mean(red_band[water_mask]) if np.any(water_mask) else 0
    
    # 2. Chlorophyll estimation (using green/blue ratio)
    green_band = img[:, :, 1].astype(float)
    blue_band = img[:, :, 2].astype(float)
    chlorophyll = np.mean(green_band[water_mask] / (blue_band[water_mask] + 1e-10)) if np.any(water_mask) else 0
    
    # Create visualization
    visualization = img.copy()
    visualization[water_mask] = [0, 255, 0]  # Highlight water in green
    
    # Save processed image with a unique name based on the original filename
    base_name = os.path.basename(image_path)
    filename, ext = os.path.splitext(base_name)
    processed_filename = f"{filename}_processed{ext}"
    processed_path = os.path.join(os.path.dirname(image_path), processed_filename)
    
    # Convert RGB to BGR for saving with OpenCV
    cv2.imwrite(processed_path, cv2.cvtColor(visualization, cv2.COLOR_RGB2BGR))
    
    return {
        'turbidity': float(turbidity),
        'chlorophyll': float(chlorophyll),
        'water_coverage': float(np.mean(water_mask) * 100),
        'processed_image': processed_path
    } 