import cv2
import os

# Specify the folder containing the images
image_folder = 'archived_live_photos'
video_name = 'output_video.mp4'

# Get a list of images in the folder, sorted in the correct order
images = [img for img in os.listdir(image_folder) if img.endswith(".jpg")]
images.sort()

# Read the first image to get the size (assuming all images have the same size)
frame = cv2.imread(os.path.join(image_folder, images[0]))
height, width, layers = frame.shape

# Define the codec and create a VideoWriter object to write the video
fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # You can choose other codecs like 'mp4v' for mp4 files
video = cv2.VideoWriter(video_name, fourcc, 30, (width, height))

# Loop through the images and add them to the video
for image in images:
    img_path = os.path.join(image_folder, image)
    frame = cv2.imread(img_path)
    video.write(frame)

# Release the video writer object
video.release()

print("Video created successfully!")
