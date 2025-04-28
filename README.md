# Satellite Image Analysis Platform

A web application for analyzing satellite imagery, featuring water quality estimation, waterbody area/volume calculation, and noise removal.

## Features

1. **Water Quality Estimation**
   - Turbidity measurement
   - Chlorophyll concentration estimation
   - Water coverage percentage calculation

2. **Waterbody Area/Volume Estimation**
   - Surface area calculation (m² and km²)
   - Volume estimation based on area and average depth
   - Waterbody outline detection

3. **Noise Removal**
   - Median filtering for salt-and-pepper noise
   - Bilateral filtering for edge-preserving smoothing
   - Non-local means denoising for Gaussian noise

## Installation

### Prerequisites
- Python 3.7 or higher
- GDAL library

### Setup

1. Clone the repository:
```
git clone <repository-url>
cd satellite-analysis-platform
```

2. Create a virtual environment (recommended):
```
python -m venv venv
```

3. Activate the virtual environment:
   - Windows:
   ```
   venv\Scripts\activate
   ```
   - macOS/Linux:
   ```
   source venv/bin/activate
   ```

4. Install requirements:
```
pip install -r requirements.txt
```

5. Run the application:
```
python app.py
```

6. Open a web browser and navigate to:
```
http://localhost:5000
```

## Usage

1. Select the analysis type from the dropdown menu
2. Upload a satellite image using drag & drop or the browse button
3. Click "Process Image" and wait for the results
4. View the processed image and results
5. Download the processed image if needed

## Technical Notes

This application is designed to work with common satellite imagery formats. For best results:

- Use multispectral imagery if available, especially for water quality analysis
- Ensure the image contains water bodies for area/volume and water quality estimations
- For actual applications, you would need to calibrate the models with ground truth data

## Dependencies

- Flask - Web framework
- OpenCV - Image processing
- NumPy - Numerical operations
- rasterio - Geospatial raster data processing
- scikit-image - Image processing algorithms
- GDAL - Geospatial data abstraction library
- Pillow - Image manipulation
- Matplotlib - Visualization 