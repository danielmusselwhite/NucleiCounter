import cv2
import numpy as np
import os

#region Functions

# Function to update the mask with trackbar values
def update_mask(x):
    try:
        # Get trackbar positions
        h_min = cv2.getTrackbarPos("Hue Min", "Mask")
        h_max = cv2.getTrackbarPos("Hue Max", "Mask")
        s_min = cv2.getTrackbarPos("Sat Min", "Mask")
        s_max = cv2.getTrackbarPos("Sat Max", "Mask")
        v_min = cv2.getTrackbarPos("Val Min", "Mask")
        v_max = cv2.getTrackbarPos("Val Max", "Mask")
        
        # Apply threshold based on current trackbar positions
        lower_purple = np.array([h_min, s_min, v_min])
        upper_purple = np.array([h_max, s_max, v_max])
        mask = cv2.inRange(hsv_image, lower_purple, upper_purple)
        
        # Display the mask
        cv2.imshow("Mask", mask)
    except Exception as e:
        print(f"Error updating mask: {e}")

#endregion

#region Main script

# Define image path and extract image name and file type
image_path = "sample2.jpg"  # Change to your image path
imageName, fileType = os.path.splitext(os.path.basename(image_path))

# Load the image
image = cv2.imread(image_path)

# Check if the image was loaded successfully
if image is None:
    print(f"Error: Could not load image at {image_path}")
    exit()

# Convert to HSV color space
hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

# Create a resizable window and trackbars for adjusting HSV ranges
cv2.namedWindow("Mask", cv2.WINDOW_NORMAL)  # Make window resizable
cv2.createTrackbar("Hue Min", "Mask", 120, 180, update_mask)
cv2.createTrackbar("Hue Max", "Mask", 160, 180, update_mask)
cv2.createTrackbar("Sat Min", "Mask", 50, 255, update_mask)
cv2.createTrackbar("Sat Max", "Mask", 255, 255, update_mask)
cv2.createTrackbar("Val Min", "Mask", 20, 255, update_mask)
cv2.createTrackbar("Val Max", "Mask", 100, 255, update_mask)

# Initial mask display
update_mask(0)

# Wait for user to adjust trackbars before proceeding
cv2.waitKey(0)

# Once the appropriate HSV values are determined, generate the mask
lower_purple = np.array([120, 50, 20])  # Use values from trackbars for fine-tuning
upper_purple = np.array([160, 255, 100])

# Threshold the image to create a binary mask for dark purple regions
mask = cv2.inRange(hsv_image, lower_purple, upper_purple)

# Optional: Morphological opening to reduce small noise in mask
kernel = np.ones((3, 3), np.uint8)
cleaned_mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel, iterations=1)

# Display the mask for debugging
cv2.imshow("Nuclei Mask", cleaned_mask)
cv2.waitKey(0)

# Use connected components to label each detected nucleus in the mask
num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(cleaned_mask, connectivity=8)

# Draw bounding boxes around detected nuclei and label each one
for i in range(1, num_labels):  # Skip the background label (label 0)
    x, y, w, h, area = stats[i]
    if 50 < area < 1000:  # Filter nuclei based on area
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.putText(image, str(i), (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

# Construct the output filename using imageName and fileType
output_filename = f"{imageName}_labeled{fileType}"
cv2.imwrite(output_filename, image)

print(f"Number of nuclei detected: {num_labels - 1}")
print(f"Labeled image saved as '{output_filename}'")

# Display final labeled image
cv2.imshow("Labeled Nuclei", image)
cv2.waitKey(0)
cv2.destroyAllWindows()

#endregion
