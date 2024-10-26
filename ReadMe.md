# Interactive Nucleus Counter Project

## Technical Description

This Python script utilizes OpenCV to detect and label nuclei in an image based on user-defined HSV (Hue, Saturation, Value) color ranges. It allows for real-time adjustments of these ranges through trackbars and can filter out small detected nuclei based on area.

### Features

- **Dynamic HSV Thresholding**: Users can adjust the HSV thresholds interactively using trackbars to fine-tune the detection of purple nuclei in the image.
- **Mask Cleaning Option**: The script can clean the mask using morphological operations to reduce noise, with a toggle to include or exclude small areas from the analysis.
- **Nuclei Detection**: It employs connected components analysis to identify and label each detected nucleus in the binary mask.
- **Output**: The script generates an output image with bounding boxes around detected nuclei and saves it to disk.

### Requirements

- Python 3.x
- OpenCV (`cv2`)
- NumPy

## User Guide

To run the script, ensure you have your environment set up with the required packages, and execute:

```bash
python nuclei_detection.py
```
![InitialInputs](./docs/images/1_initialInputs.png)

1. You will be prompted to enter the:
   1. Image Path
   2. If you want to circle all found nuclei or only the large ones (recommend all)
   3. If you want to clean the mask (recommended to clean)

2. You can either use the default values by just pressing `Enter` or input your own values.

![MaskSelector](./docs/images/2_MaskSelector.png)

3. A window will pop up with the original image and a mask of the detected nuclei. You can adjust the HSV values using the trackbars to fine-tune the detection. Use the Value Indicators to help you find the right values. 
   
4. Then when the mask looks good, press `d` (for done) to continue.
   
![Output](./docs/images/3_Output.png)

5. You will now see the cleaned mask that was used (if you chose to clean it), the original image with bounding boxes around the detected nuclei, and the number of nuclei found outputted in the console.
6. The output image will be saved in the same directory as the script with the same name as the input image but with `_labeled` appended to the name.
