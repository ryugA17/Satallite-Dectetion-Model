from flask import Flask, render_template, request, jsonify
import os
from werkzeug.utils import secure_filename
from models.water_quality import estimate_water_quality
from models.area_volume import calculate_area_volume
from models.noise_removal import remove_noise

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    if file:
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Get the selected processing type
        processing_type = request.form.get('processing_type')
        
        try:
            if processing_type == 'water_quality':
                result = estimate_water_quality(filepath)
            elif processing_type == 'area_volume':
                result = calculate_area_volume(filepath)
            elif processing_type == 'noise_removal':
                result = remove_noise(filepath)
            else:
                return jsonify({'error': 'Invalid processing type'}), 400
            
            return jsonify({
                'success': True,
                'result': result,
                'processed_image': f'/static/uploads/processed_{filename}'
            })
            
        except Exception as e:
            return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True) 