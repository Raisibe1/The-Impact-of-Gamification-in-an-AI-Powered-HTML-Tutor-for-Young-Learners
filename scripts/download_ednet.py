import requests
import zipfile
import os
import pandas as pd

os.makedirs('data/raw', exist_ok=True)

print("=" * 60)
print(" DOWNLOADING EDNET DATASET")
print("  This is a LARGE dataset (~4.3GB)")
print(" Will take 1-2 hours depending on internet speed")
print("=" * 60)

# URL for EdNet KT3
url = "https://zenodo.org/record/5525437/files/ednet_kt3.zip?download=1"
output_path = "data/raw/ednet_kt3.zip"

print(f"\n Downloading from: {url}")
print(f" Saving to: {output_path}")

try:
    response = requests.get(url, stream=True)
    total_size = int(response.headers.get('content-length', 0))
    
    print(f" Total size: {total_size / (1024**3):.2f} GB")
    
    with open(output_path, 'wb') as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)
    
    print(" Download complete!")
    
    print("\n Extracting zip file...")
    with zipfile.ZipFile(output_path, 'r') as zip_ref:
        zip_ref.extractall("data/raw/")
    
    print(" Extraction complete!")
    print(f" Files extracted to: data/raw/")
    
    # List extracted files
    print("\n Extracted files:")
    for file in os.listdir('data/raw/'):
        if file.startswith('ednet'):
            file_size = os.path.getsize(f'data/raw/{file}') / (1024**3)
            print(f"   - {file} ({file_size:.2f} GB)")
    
    # Clean up zip file
    os.remove(output_path)
    print(f"\n Removed zip file: {output_path}")
    
except Exception as e:
    print(f" Error: {e}")
    print("\n Alternative download methods:")
    print("1. Download manually from: https://zenodo.org/record/5525437")
    print("2. Use the EduData package if available")