from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
import os
from PIL import Image
from image_processing.badge import verify_image_and_process_image,generate_image,generate_image_fast,load_mini_model 

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'
app.config['MAX_CONTENT_LENGTH'] = 16*1024*1024


@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': ' No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    if file and allowed_files(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        try:
            image = Image.open(file_path).convert('RGBA')
            processed_image, _ = verify_image_and_process_image(image)
            if processed_image.mode =='RGBA':
                processed_image = processed_image.convert('RGB')

            output_path = os.path.join(
            app.config['UPLOAD_FOLDER'], "processed_"+filename)
            processed_image.save(output_path,'JPEG')
            os.remove(file_path)
            return jsonify({'message': 'File uploaded successfully', 'path': output_path}), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    else:
        return jsonify({'error': 'Invalid files or file types'}), 400
    
@app.route('/generate_image', methods=['POST'])
def generate_images():
    prompt = request.json.get('prompt')
    if not prompt:
        return jsonify({'error': 'No prompt provided'}),400
    try:
        model =load_mini_model()
        generated_image=generate_image_fast(model,prompt)
        processed_image, _ = generate_image(generated_image)
        output_format = 'JPEG'
        file_extension = 'jpg' if output_format == 'JPEG' else 'png'
        if processed_image.mode =='RGBA' and output_format == 'JPEG':
            processed_image = processed_image.convert('RGB')

            output_path = os.path.join(
            app.config['UPLOAD_FOLDER'], f"processed_generated.{file_extension}")
            processed_image.save(output_path,output_format)
            return jsonify({'message': 'File uploaded successfully', 'path': output_path}), 200
    except Exception as e:
        app.logger.error(f"Server Error: {str(e)}")
        return jsonify({'error': str(e)}), 500
    else:
        return jsonify({'error': 'Invalid files or file types'}), 400



def allowed_files(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg', 'gif'}


if __name__ == '__main__':
    app.run(debug=True)
