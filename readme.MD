

# Image Processing Application

## Overview
This Flask application is designed to process images uploaded by users and generate new images based on text prompts. The application leverages the `PIL` library for image manipulation and the `diffusers` library to utilize pre-trained models from Stable Diffusion for image generation.

## Features
- **Image Upload**: Users can upload images in JPEG, PNG, or GIF formats. Uploaded images are verified and processed to fit into a predefined frame.
- **Image Generation**: Users can input text prompts to generate images. These images are then processed similarly to uploaded images.
- **Dynamic Hue Adjustment**: Both uploaded and generated images can have their hues adjusted randomly to enhance visual variety.

## Installation

### Prerequisites
- Python 3.8+
- pip
- Flask
- PIL
- diffusers
- torch

### Setup
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/image-processing-app.git
   cd image-processing-app
   ```

2. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the Flask application:
   ```bash
   python app.py
   ```

## Usage

### Starting the Server
Run the Flask application using the command:
```bash
python app.py
```
The server will start, and you can access the application on `localhost:5000` or the configured port.

### Endpoints
- **POST `/upload`**: Upload an image to be processed. The request should include a multipart/form-data field with the key `file`.
- **POST `/generate_image`**: Generate an image based on a text prompt. Send a JSON payload with the key `prompt`.

### Testing with Postman
#### Uploading an Image
- **Method**: POST
- **URL**: `http://localhost:5000/upload`
- **Body Type**: form-data
- **Key**: `file` (type: File)
- **Action**: Upload an image file.
- **Response**: Expect a JSON with a success message and the path to the processed image.

#### Generating an Image
- **Method**: POST
- **URL**: `http://localhost:5000/generate_image`
- **Body Type**: raw (JSON)
- **Content**: `{"prompt":"an owl"}`
- **Action**: Send the request to generate an image based on the prompt.
- **Response**: Expect a JSON with a success message and the path to the generated image.

## Troubleshooting

### Common Issues
- **Upload Fails**: Ensure the file size does not exceed 16 MB and the file format is among the supported types (JPEG, PNG, GIF).
- **Model Loading Errors**: Check if the `diffusers` and `torch` libraries are installed correctly and the model `runwayml/stable-diffusion-v1-5` is accessible.

### Logs
Check the Flask server logs for errors. These logs provide insights into the operations and errors encountered by the server.

---
