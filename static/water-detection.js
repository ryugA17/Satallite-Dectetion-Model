/**
 * Water Detection Visualization Enhancement
 * This script adds interactive features to the water detection results
 */

document.addEventListener('DOMContentLoaded', function() {
    // Elements
    const imageContainer = document.querySelector('.image-container');
    const resultImage = document.getElementById('result-image');
    const originalImage = document.getElementById('original-image');
    const toggleOriginal = document.getElementById('toggle-original');
    
    // Add image slider functionality (if both images are available)
    if (resultImage && originalImage) {
        let sliderActive = false;
        let sliderPosition = 50;
        
        // Create slider elements
        const sliderContainer = document.createElement('div');
        sliderContainer.className = 'slider-container';
        sliderContainer.style.cssText = `
            position: absolute;
            top: 10px;
            right: 10px;
            display: none;
            z-index: 1000;
        `;
        
        const slider = document.createElement('input');
        slider.type = 'range';
        slider.min = '0';
        slider.max = '100';
        slider.value = '50';
        slider.className = 'form-range';
        
        const sliderLabel = document.createElement('div');
        sliderLabel.className = 'slider-label text-white bg-dark bg-opacity-75 px-2 py-1 rounded-pill';
        sliderLabel.textContent = 'Comparison Slider';
        sliderLabel.style.marginBottom = '5px';
        
        sliderContainer.appendChild(sliderLabel);
        sliderContainer.appendChild(slider);
        
        // Add slider to DOM
        imageContainer?.appendChild(sliderContainer);
        
        // Add slider button
        const sliderButton = document.createElement('button');
        sliderButton.className = 'btn btn-sm btn-outline-light ms-2';
        sliderButton.innerHTML = '<i class="fas fa-sliders-h me-1"></i> Compare';
        sliderButton.id = 'slider-button';
        toggleOriginal.parentNode.appendChild(sliderButton);
        
        // Split view overlay
        const splitOverlay = document.createElement('div');
        splitOverlay.className = 'split-overlay';
        splitOverlay.style.cssText = `
            position: absolute;
            top: 0;
            left: 0;
            height: 100%;
            width: 50%;
            overflow: hidden;
            z-index: 5;
            pointer-events: none;
            border-right: 2px solid white;
            display: none;
        `;
        
        // Clone original image for split view
        const clonedOriginal = originalImage.cloneNode(true);
        clonedOriginal.style.cssText = `
            position: absolute;
            top: 0;
            left: 0;
            opacity: 1;
            display: block;
            max-width: initial;
            width: ${resultImage.offsetWidth}px;
        `;
        
        splitOverlay.appendChild(clonedOriginal);
        imageContainer?.appendChild(splitOverlay);
        
        // Add event for slider button
        sliderButton.addEventListener('click', function() {
            if (!sliderActive) {
                // Activate slider view
                sliderActive = true;
                sliderContainer.style.display = 'block';
                splitOverlay.style.display = 'block';
                originalImage.style.opacity = '0';
                originalImage.style.display = 'none';
                sliderButton.classList.remove('btn-outline-light');
                sliderButton.classList.add('btn-light');
                toggleOriginal.disabled = true;
                
                // Update split position
                updateSplitPosition(sliderPosition);
            } else {
                // Deactivate slider view
                sliderActive = false;
                sliderContainer.style.display = 'none';
                splitOverlay.style.display = 'none';
                toggleOriginal.disabled = false;
                sliderButton.classList.remove('btn-light');
                sliderButton.classList.add('btn-outline-light');
            }
        });
        
        // Update split position when slider is moved
        slider.addEventListener('input', function() {
            sliderPosition = this.value;
            updateSplitPosition(sliderPosition);
        });
        
        // Update split position and original image view
        function updateSplitPosition(position) {
            const width = position + '%';
            splitOverlay.style.width = width;
        }
        
        // Handle window resize
        window.addEventListener('resize', function() {
            if (sliderActive && resultImage) {
                clonedOriginal.style.width = resultImage.offsetWidth + 'px';
            }
        });
    }
    
    // Add water coverage percentage visualization
    const coverageValue = document.getElementById('coverage-value');
    const coverageBar = document.getElementById('coverage-bar');
    
    if (coverageValue && coverageBar) {
        const observer = new MutationObserver(function(mutations) {
            mutations.forEach(function(mutation) {
                if (mutation.type === 'characterData' || mutation.type === 'childList') {
                    const valueText = coverageValue.textContent;
                    const percentage = parseFloat(valueText);
                    
                    if (!isNaN(percentage)) {
                        // Update progress bar color based on value
                        if (percentage > 50) {
                            coverageBar.classList.add('bg-success');
                            coverageBar.classList.remove('bg-warning', 'bg-danger', 'bg-info');
                        } else if (percentage > 25) {
                            coverageBar.classList.add('bg-info');
                            coverageBar.classList.remove('bg-warning', 'bg-danger', 'bg-success');
                        } else if (percentage > 10) {
                            coverageBar.classList.add('bg-warning');
                            coverageBar.classList.remove('bg-info', 'bg-danger', 'bg-success');
                        } else {
                            coverageBar.classList.add('bg-danger');
                            coverageBar.classList.remove('bg-warning', 'bg-info', 'bg-success');
                        }
                    }
                }
            });
        });
        
        observer.observe(coverageValue, { characterData: true, childList: true, subtree: true });
    }
    
    // Add zoom functionality to images
    const zoomContainer = document.createElement('div');
    zoomContainer.className = 'zoom-container';
    zoomContainer.style.cssText = `
        position: absolute;
        bottom: 10px;
        right: 10px;
        z-index: 1000;
    `;
    
    const zoomInButton = document.createElement('button');
    zoomInButton.className = 'btn btn-sm btn-dark me-1';
    zoomInButton.innerHTML = '<i class="fas fa-search-plus"></i>';
    
    const zoomOutButton = document.createElement('button');
    zoomOutButton.className = 'btn btn-sm btn-dark';
    zoomOutButton.innerHTML = '<i class="fas fa-search-minus"></i>';
    
    zoomContainer.appendChild(zoomInButton);
    zoomContainer.appendChild(zoomOutButton);
    
    imageContainer?.appendChild(zoomContainer);
    
    let currentZoom = 1;
    
    zoomInButton.addEventListener('click', function() {
        if (currentZoom < 3) {
            currentZoom += 0.25;
            applyZoom();
        }
    });
    
    zoomOutButton.addEventListener('click', function() {
        if (currentZoom > 1) {
            currentZoom -= 0.25;
            applyZoom();
        }
    });
    
    function applyZoom() {
        if (resultImage) {
            resultImage.style.transform = `scale(${currentZoom})`;
            resultImage.style.transformOrigin = 'center center';
            resultImage.style.transition = 'transform 0.3s ease';
        }
        
        if (originalImage) {
            originalImage.style.transform = `scale(${currentZoom})`;
            originalImage.style.transformOrigin = 'center center';
            originalImage.style.transition = 'transform 0.3s ease';
        }
        
        if (clonedOriginal) {
            clonedOriginal.style.transform = `scale(${currentZoom})`;
            clonedOriginal.style.transformOrigin = 'center center';
            clonedOriginal.style.transition = 'transform 0.3s ease';
        }
    }
}); 