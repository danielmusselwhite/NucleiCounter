import cv2
import numpy as np
import os

#region Variables to change scripts functionality

# Define image path and extract image name and file type
image_path = "sample2.jpg"  # Change to your image path
imageName, fileType = os.path.splitext(os.path.basename(image_path))

printAllCircledNuclei = True # do you want to print all highlighted nuclei or filter out small ones?
cleanMask = True # do you want to clean the mask (eg auto filter out small areas from being included in the count)?

#endregion

#region Functions

# Function to update the mask with trackbar values
def update_mask(x):
    try:
        # Get trackbar positions only if the window is still open
        if cv2.getWindowProperty("Mask", cv2.WND_PROP_VISIBLE) >= 1:
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

            # Create a blank image to draw color squares
            color_square = np.zeros((100, 300, 3), dtype=np.uint8)

            # Draw minimum value square (using the actual min HSV values)
            color_square[:, :100] = cv2.cvtColor(np.uint8([[lower_purple]]), cv2.COLOR_HSV2BGR)[0][0]  # Min HSV color
            cv2.putText(color_square, f"Min HSV", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

            # Draw maximum value square (using the actual max HSV values)
            color_square[:, 200:] = cv2.cvtColor(np.uint8([[upper_purple]]), cv2.COLOR_HSV2BGR)[0][0]  # Max HSV color
            cv2.putText(color_square, f"Max HSV", (210, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

            # Show the color squares
            cv2.imshow("Value Indicators", color_square)

    except Exception as e:
        print(f"Error updating mask: {e}")

def done_callback():
    """Function to handle cleanup and show final values when done."""
    # Check if the windows are still open before accessing trackbars
    if cv2.getWindowProperty("Mask", cv2.WND_PROP_VISIBLE) >= 1:
        # Read final HSV values from trackbars
        h_min = cv2.getTrackbarPos("Hue Min", "Mask")
        h_max = cv2.getTrackbarPos("Hue Max", "Mask")
        s_min = cv2.getTrackbarPos("Sat Min", "Mask")
        s_max = cv2.getTrackbarPos("Sat Max", "Mask")
        v_min = cv2.getTrackbarPos("Val Min", "Mask")
        v_max = cv2.getTrackbarPos("Val Max", "Mask")

        # Set the lower and upper bounds for masking using trackbar values
        lower_purple = np.array([h_min, s_min, v_min])
        upper_purple = np.array([h_max, s_max, v_max])
        
        print(f"Final HSV Min: [{h_min}, {s_min}, {v_min}]")
        print(f"Final HSV Max: [{h_max}, {s_max}, {v_max}]")

    # Close all windows
    cv2.destroyAllWindows()

#endregion

#region Main script

# Load the image
image = cv2.imread(image_path)

# Check if the image was loaded successfully
if image is None:
    print(f"Error: Could not load image at {image_path}")
    exit()

# Display the input image
cv2.imshow("Input Image", image)
cv2.waitKey(0)

# Convert to HSV color space
hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

# Display the HSV image for debugging
cv2.imshow("HSV Image", hsv_image)
cv2.waitKey(0)

# Create a resizable window and trackbars for adjusting HSV ranges
cv2.namedWindow("Mask", cv2.WINDOW_NORMAL)  # Make window resizable
cv2.createTrackbar("Hue Min", "Mask", 0, 179, update_mask)
cv2.createTrackbar("Hue Max", "Mask", 179, 179, update_mask)
cv2.createTrackbar("Sat Min", "Mask", 0, 255, update_mask)
cv2.createTrackbar("Sat Max", "Mask", 255, 255, update_mask)
cv2.createTrackbar("Val Min", "Mask", 0, 255, update_mask)
cv2.createTrackbar("Val Max", "Mask", 255, 255, update_mask)

# Create a resizable window for the value indicators
cv2.namedWindow("Value Indicators", cv2.WINDOW_NORMAL)  # Make window resizable

# Initial mask display
update_mask(0)

# Main loop to wait for user input
while True:
    key = cv2.waitKey(1)  # Wait for key press, 1 ms delay
    if key == ord('d'):  # If 'd' key is pressed, finalize and exit
        # getting the thresholds before closing the window
        lower_purple = np.array([cv2.getTrackbarPos("Hue Min", "Mask"),
            cv2.getTrackbarPos("Sat Min", "Mask"),
            cv2.getTrackbarPos("Val Min", "Mask")])
        upper_purple = np.array([cv2.getTrackbarPos("Hue Max", "Mask"),
            cv2.getTrackbarPos("Sat Max", "Mask"),
            cv2.getTrackbarPos("Val Max", "Mask")])
        done_callback()
        break
    elif key == 27:  # ESC key to exit
        cv2.destroyAllWindows()
        exit()

# Get the lower_purple and upper_purple hsv values from the trackbars
# Moved this part into done_callback to ensure window is open
# Removed the redundant code since it's handled in done_callback

# Threshold the image to create a binary mask for purple regions
mask = cv2.inRange(hsv_image, lower_purple, upper_purple)





# Optional: Morphological opening to reduce small noise in mask
# MODIFY THIS EG IF YOU WANT SMALL ONES, AS NUCLEI MAY BE VERY SMALL SO WE MAY NOT WANT TO REMOVE THEM
if(cleanMask):
    kernel = np.ones((0, 0), np.uint8)
    cleaned_mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel, iterations=1)
else:
    cleaned_mask = mask # quick and dirty if you just want to keep it the same






# Display the mask for debugging
cv2.imshow("Cleaned Mask", cleaned_mask)
cv2.waitKey(0)

# Use connected components to label each detected nucleus in the mask
num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(cleaned_mask, connectivity=8)

# Draw bounding boxes around detected nuclei and label each one
for i in range(1, num_labels):  # Skip the background label (label 0)
    x, y, w, h, area = stats[i]
    if printAllCircledNuclei or 50 < area < 1000:  # Filter nuclei based on area
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 1)
        cv2.putText(image, str(i), (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.1, (0, 0, 255), 2)

# Construct the output filename using imageName and fileType
output_filename = f"{imageName}_labeled{fileType}"
cv2.imwrite(output_filename, image)

print(f"Number of nuclei detected: {num_labels - 1}")
print(f"Labeled image saved as '{output_filename}'")

# Display final labeled image
cv2.imshow("Labeled Nuclei", image)
cv2.waitKey(0)
cv2.destroyAllWindows()

