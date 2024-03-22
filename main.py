import picamera
import requests
from io import BytesIO
import time

# Define the URL of the server where images will be sent
SERVER_URL = "http://your_server_ip:port/receive_image"

# Initialize the camera
camera = picamera.PiCamera()
camera.resolution = (640, 480)  # Set the camera resolution

try:
    while True:
        # Capture an image
        stream = BytesIO()
        camera.capture(stream, format='jpeg')
        stream.seek(0)

        # Send the image to the server
        files = {'image': ('image.jpg', stream, 'image/jpeg')}
        response = requests.post(SERVER_URL, files=files)

        # Print the server's response (for testing purposes)
        print(response.text)

        # Wait for a few seconds before capturing the next image
        time.sleep(5)

finally:
    camera.close()  # Close the camera when done


from flask import Flask, request
import os
from datetime import datetime
from PIL import Image
from io import BytesIO

app = Flask(__name__)

# Directory to save uploaded images
UPLOAD_FOLDER = 'uploaded_images'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/receive_image', methods=['POST'])
def receive_image():
    if 'image' not in request.files:
        return "No image uploaded", 400
    
    image_file = request.files['image']
    if image_file.filename == '':
        return "Empty filename", 400

    if image_file:
        try:
            # Save the uploaded image to disk
            filename = datetime.now().strftime("%Y%m%d_%H%M%S") + '.jpg'
            filepath = os.path.join(UPLOAD_FOLDER, filename)
            image = Image.open(BytesIO(image_file.read()))
            image.save(filepath)
            return f"Image saved: {filename}", 200
        except Exception as e:
            return f"Error saving image: {str(e)}", 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
