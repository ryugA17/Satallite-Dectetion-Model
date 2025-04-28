import cv2
import numpy as np
from PIL import Image
import os

def remove_noise(image_path):
    """
    Remove noise from satellite imagery using various filtering techniques
    """
    # Read the image
    img = cv2.imread(image_path)
    if img is None:
        raise ValueError(f"Failed to load image: {image_path}")
    
    # Convert BGR to RGB (OpenCV loads as BGR)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    
    # Convert to grayscale for certain operations if needed
    if len(img.shape) > 2:
        gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    else:
        gray = img.copy()
    
    # Store original for comparison
    original = img.copy()
    
    # Apply multiple noise reduction techniques
    # 1. Median filtering - good for salt and pepper noise
    median_filtered = cv2.medianBlur(img, 5)
    
    # 2. Bilateral filtering - edge-preserving smoothing
    if len(img.shape) > 2:
        bilateral_filtered = cv2.bilateralFilter(img, 9, 75, 75)
    else:
        bilateral_filtered = cv2.bilateralFilter(gray, 9, 75, 75)
        bilateral_filtered = cv2.cvtColor(bilateral_filtered, cv2.COLOR_GRAY2RGB)
    
    # 3. Non-local means denoising - good for Gaussian noise
    nlm_filtered = cv2.fastNlMeansDenoisingColored(img, None, 10, 10, 7, 21) if len(img.shape) > 2 else cv2.fastNlMeansDenoising(gray, None, 10, 7, 21)
    
    # Create visualization
    # Stack original and filtered images side by side
    h, w = img.shape[:2]
    
    # Ensure all images are RGB for stacking
    if len(original.shape) == 2:
        original = cv2.cvtColor(original, cv2.COLOR_GRAY2RGB)
    if len(median_filtered.shape) == 2:
        median_filtered = cv2.cvtColor(median_filtered, cv2.COLOR_GRAY2RGB)
    if len(nlm_filtered.shape) == 2:
        nlm_filtered = cv2.cvtColor(nlm_filtered, cv2.COLOR_GRAY2RGB)
    
    # Create comparison visualization
    top_row = np.hstack((original, median_filtered))
    bottom_row = np.hstack((bilateral_filtered, nlm_filtered))
    visualization = np.vstack((top_row, bottom_row))
    
    # Add labels
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(visualization, "Original", (10, 30), font, 1, (255, 255, 255), 2, cv2.LINE_AA)
    cv2.putText(visualization, "Median Filter", (w + 10, 30), font, 1, (255, 255, 255), 2, cv2.LINE_AA)
    cv2.putText(visualization, "Bilateral Filter", (10, h + 30), font, 1, (255, 255, 255), 2, cv2.LINE_AA)
    cv2.putText(visualization, "NLM Denoising", (w + 10, h + 30), font, 1, (255, 255, 255), 2, cv2.LINE_AA)
    
    # Generate filenames based on original image
    base_name = os.path.basename(image_path)
    filename, ext = os.path.splitext(base_name)
    processed_filename = f"{filename}_processed{ext}"
    comparison_filename = f"{filename}_comparison{ext}"
    
    # Generate paths
    processed_path = os.path.join(os.path.dirname(image_path), processed_filename)
    viz_path = os.path.join(os.path.dirname(image_path), comparison_filename)
    
    # Save processed image (use NLM as default output)
    cv2.imwrite(processed_path, cv2.cvtColor(nlm_filtered, cv2.COLOR_RGB2BGR))
    
    # Save visualization
    cv2.imwrite(viz_path, cv2.cvtColor(visualization, cv2.COLOR_RGB2BGR))
    
    return {
        'processed_image': processed_path,
        'comparison_image': viz_path,
        'techniques': ['median_filter', 'bilateral_filter', 'non_local_means']
    } 