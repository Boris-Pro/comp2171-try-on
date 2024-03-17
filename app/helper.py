import os
from app import app

def get_uploaded_images():
    rootdir = os.getcwd()
    upload_folder = os.path.join(rootdir, app.config['UPLOAD_FOLDER'])
    images = []
    for subdir, dirs, files in os.walk(upload_folder):
        for file in files:
            images.append(file)
    return images