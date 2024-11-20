from flask import Flask, request, jsonify, render_template_string
from rembg import remove
from PIL import Image
import io
import os
import base64

app = Flask(__name__)

@app.route('/')
def home():
    html_content = '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Background Remover</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                max-width: 800px;
                margin: 0 auto;
                padding: 20px;
                background-color: #f5f5f5;
            }

            .container {
                background-color: white;
                padding: 20px;
                border-radius: 8px;
                box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
            }

            h1 {
                text-align: center;
                color: #333;
            }

            .upload-section {
                text-align: center;
                margin: 20px 0;
            }

            #uploadBtn {
                background-color: #4CAF50;
                color: white;
                padding: 10px 20px;
                border: none;
                border-radius: 4px;
                cursor: pointer;
                font-size: 16px;
            }

            #uploadBtn:hover {
                background-color: #45a049;
            }

            .image-preview {
                display: flex;
                justify-content: space-around;
                margin-top: 20px;
                flex-wrap: wrap;
            }

            .preview-container {
                margin: 10px;
                text-align: center;
            }

            .preview-container img {
                max-width: 300px;
                max-height: 300px;
                margin-top: 10px;
            }

            #loading {
                display: none;
                text-align: center;
                margin: 20px 0;
            }

            .error {
                color: red;
                text-align: center;
                margin: 10px 0;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Background Remover</h1>
            
            <div class="upload-section">
                <input type="file" id="fileInput" accept="image/*" style="display: none;">
                <button id="uploadBtn">Upload Image</button>
            </div>

            <div id="loading">Processing...</div>
            
            <div class="image-preview">
                <div class="preview-container">
                    <h3>Original Image</h3>
                    <img id="originalImage">
                </div>
                <div class="preview-container">
                    <h3>Processed Image</h3>
                    <img id="processedImage">
                </div>
            </div>
        </div>

        <script>
            document.getElementById('uploadBtn').addEventListener('click', () => {
                document.getElementById('fileInput').click();
            });

            document.getElementById('fileInput').addEventListener('change', async (e) => {
                const file = e.target.files[0];
                if (!file) return;

                // Display original image
                const originalImage = document.getElementById('originalImage');
                originalImage.src = URL.createObjectURL(file);

                // Show loading
                document.getElementById('loading').style.display = 'block';

                // Prepare form data
                const formData = new FormData();
                formData.append('image', file);

                try {
                    // Send request to server
                    const response = await fetch('/remove-bg', {
                        method: 'POST',
                        body: formData
                    });

                    const data = await response.json();

                    if (response.ok) {
                        // Display processed image
                        const processedImage = document.getElementById('processedImage');
                        processedImage.src = `data:image/png;base64,${data.image}`;
                    } else {
                        alert('Error: ' + data.error);
                    }
                } catch (error) {
                    alert('Error processing image: ' + error.message);
                } finally {
                    document.getElementById('loading').style.display = 'none';
                }
            });
        </script>
    </body>
    </html>
    '''
    return render_template_string(html_content)

@app.route('/remove-bg', methods=['POST'])
def remove_background():
    try:
        # Get the image from the request
        file = request.files['image']
        if not file:
            return jsonify({'error': 'No image uploaded'}), 400

        # Read and process the image
        input_image = Image.open(file.stream)
        
        # Remove background
        output_image = remove(input_image)
        
        # Convert to base64 for sending back to frontend
        buffered = io.BytesIO()
        output_image.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode()
        
        return jsonify({'image': img_str})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
