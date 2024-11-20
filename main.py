from flask import Flask, render_template, request, send_file
from rembg import remove
from PIL import Image
import io

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'image' not in request.files:
        return 'No image uploaded!', 400
    
    image_file = request.files['image']
    
    if image_file.filename == '':
        return 'No image selected!', 400
    
    # Read image and remove background
    img = Image.open(image_file)
    img = remove(img)  # Removing background

    # Save the processed image in-memory
    img_io = io.BytesIO()
    img.save(img_io, 'PNG')
    img_io.seek(0)
    
    # Return processed image
    return send_file(img_io, mimetype='image/png')

if __name__ == '__main__':
    app.run(debug=True)
