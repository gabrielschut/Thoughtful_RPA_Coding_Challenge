from pathlib import Path
import os
import urllib.request

def download_image(image_url, file_name):
    # Ensure the output directory exists
    output_directory = 'output/pictures'
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    # Construct the full path for the file
    file_path = os.path.join(output_directory, file_name)

    # Download the image and save it to the specified path
    urllib.request.urlretrieve(image_url, file_path)