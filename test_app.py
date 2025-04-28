"""
Test script for the Satellite Image Analysis application
This script checks if the application components are working as expected
"""

import os
import cv2
import numpy as np
from PIL import Image
from models.water_quality import estimate_water_quality
from models.area_volume import calculate_area_volume
from models.noise_removal import remove_noise

def create_test_image():
    """Create a simple test image with water-like features"""
    # Create a 300x300 RGB image
    img = np.zeros((300, 300, 3), dtype=np.uint8)
    
    # Draw a blue "water body"
    cv2.circle(img, (150, 150), 100, (180, 180, 255), -1)
    
    # Add some green "land"
    cv2.rectangle(img, (0, 0), (300, 300), (20, 180, 20), -1)
    
    # Make the water body visible on top of the land
    cv2.circle(img, (150, 150), 100, (180, 180, 255), -1)
    
    # Add some noise
    noise = np.random.randint(0, 50, img.shape, dtype=np.uint8)
    img = cv2.add(img, noise)
    
    # Save the test image
    os.makedirs('static/uploads', exist_ok=True)
    test_image_path = 'static/uploads/test_image.jpg'
    Image.fromarray(img).save(test_image_path)
    
    return test_image_path

def test_water_quality():
    """Test water quality estimation"""
    try:
        image_path = create_test_image()
        result = estimate_water_quality(image_path)
        print("Water Quality Test: PASSED")
        print(f"  - Turbidity: {result['turbidity']:.2f}")
        print(f"  - Chlorophyll: {result['chlorophyll']:.2f}")
        print(f"  - Water Coverage: {result['water_coverage']:.2f}%")
        return True
    except Exception as e:
        print(f"Water Quality Test: FAILED - {str(e)}")
        return False

def test_area_volume():
    """Test area/volume estimation"""
    try:
        image_path = create_test_image()
        result = calculate_area_volume(image_path)
        print("Area/Volume Test: PASSED")
        print(f"  - Area: {result['water_area_sq_meters']:.2f} m²")
        print(f"  - Volume: {result['estimated_volume_cubic_meters']:.2f} m³")
        return True
    except Exception as e:
        print(f"Area/Volume Test: FAILED - {str(e)}")
        return False

def test_noise_removal():
    """Test noise removal"""
    try:
        image_path = create_test_image()
        result = remove_noise(image_path)
        print("Noise Removal Test: PASSED")
        print(f"  - Techniques applied: {', '.join(result['techniques'])}")
        return True
    except Exception as e:
        print(f"Noise Removal Test: FAILED - {str(e)}")
        return False

if __name__ == "__main__":
    print("Running tests for Satellite Image Analysis application...")
    
    results = []
    results.append(test_water_quality())
    results.append(test_area_volume())
    results.append(test_noise_removal())
    
    if all(results):
        print("\nAll tests PASSED! The application is working correctly.")
        print("You can now run the web application with: python app.py")
    else:
        print("\nSome tests FAILED. Please check the errors above.") 