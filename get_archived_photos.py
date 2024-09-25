import os, sys
import requests

# Create the directory if it doesn't exist
if not os.path.exists('archived_live_photos'):
    os.makedirs('archived_live_photos')

count_404 = 0

# Loop over the range of image numbers
for i in range(1, 2030):
    # Format the number with leading zeros (6 digits)
    image_number = f"{i:06d}"
    
    # Path to save the image locally
    save_path = f"archived_live_photos/{image_number}.jpg"
    
    # Check if the image already exists
    if os.path.exists(save_path):
        print(f"Image {image_number}.jpg already exists, skipping download.")
        continue

    # Construct the URL
    url = f"https://projectskydrop.com/cameras/archiveA/{image_number}.jpg"

    try:
        # Download the image
        response = requests.get(url)
        # Check if the request was successful
        if response.status_code == 200:
            # Save the image to the folder
            with open(save_path, 'wb') as f:
                f.write(response.content)
            print(f"Downloaded {image_number}.jpg")
        else:
            if count_404 >= 2:
                print(f"Too many 404 responses in the loop, quitting entirely...")
                sys.exit()
            print(f"Failed to download {image_number}.jpg (Status code: {response.status_code})")
            count_404 += 1
    except Exception as e:
        print(f"An error occurred: {e}")
