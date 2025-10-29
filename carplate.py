# import streamlit as st
# import cv2
# import numpy as np
# import pytesseract
# from imutils import contours
# from tika import parser
# import matplotlib.pyplot as plt

# # Configure the path to the Tesseract-OCR executable
# pytesseract.pytesseract.tesseract_cmd = r"D:\Google Play Store\tesseract.exe"

# def detect_license_plate(image):
#     # Convert the image to grayscale
#     gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

#     # Apply a bilateral filter to reduce noise while keeping edges sharp
#     gray = cv2.bilateralFilter(gray, 11, 17, 17)

#     # Perform edge detection
#     edged = cv2.Canny(gray, 170, 200)

#     # Find contours based on edges detected
#     cnts, _ = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
#     cnts = sorted(cnts, key=cv2.contourArea, reverse=True)[:30]  # Keep top 30 contours

#     # Initialize license plate contour and coordinates
#     plate_contour = None
#     plate_coords = None

#     # Loop over contours to find the license plate contour
#     for c in cnts:
#         # Approximate the contour
#         peri = cv2.arcLength(c, True)
#         approx = cv2.approxPolyDP(c, 0.018 * peri, True)
        
#         # If the contour has 4 vertices, it's likely to be the license plate
#         if len(approx) == 4:
#             plate_contour = approx
#             x, y, w, h = cv2.boundingRect(c)
#             plate_coords = (x, y, w, h)
#             break

#     return plate_contour, plate_coords

# def main():
#     st.title("License Plate Detection")

#     # File uploader to upload an image
#     uploaded_file = st.file_uploader("Upload an image of a car", type=["jpg", "jpeg", "png"])

#     if uploaded_file is not None:
#         # Read the image file
#         file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
#         image = cv2.imdecode(file_bytes, 1)
        
#         # Detect license plate
#         plate_contour, plate_coords = detect_license_plate(image)
        
#         # Draw the contour if detected
#         if plate_contour is not None:
#             cv2.drawContours(image, [plate_contour], -1, (0, 255, 0), 3)
#             st.write("License plate detected.")
#         else:
#             st.write("No license plate detected.")
        
#         # Convert BGR to RGB for displaying with Matplotlib
#         image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

#         # Display the image with the detected license plate
#         plt.figure(figsize=(10, 6))
#         plt.imshow(image_rgb)
#         plt.axis('off')
#         st.pyplot(plt)

# if __name__ == "__main__":
#     main()

import cv2
import imutils
import numpy as np
import pytesseract
import streamlit as st

# Path to the Tesseract executable
pytesseract.pytesseract.tesseract_cmd = r"D:\Google Play Store\tesseract.exe"

def process_image(image_path):
    # Read and resize the image
    img = cv2.imread(image_path, cv2.IMREAD_COLOR)
    img = cv2.resize(img, (600, 400))

    # Convert to grayscale and apply bilateral filter
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.bilateralFilter(gray, 13, 15, 15)

    # Edge detection
    edged = cv2.Canny(gray, 30, 200)
    contours = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours = imutils.grab_contours(contours)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)[:10]
    
    screenCnt = None

    # Find the contour with four sides
    for c in contours:
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.018 * peri, True)

        if len(approx) == 4:
            screenCnt = approx
            break

    # If no contour is detected
    if screenCnt is None:
        return img, None, None
    
    # Draw the contour on the original image
    cv2.drawContours(img, [screenCnt], -1, (0, 0, 255), 3)

    # Create a mask and extract the plate area
    mask = np.zeros(gray.shape, np.uint8)
    new_image = cv2.drawContours(mask, [screenCnt], 0, 255, -1)
    new_image = cv2.bitwise_and(img, img, mask=mask)

    (x, y) = np.where(mask == 255)
    (topx, topy) = (np.min(x), np.min(y))
    (bottomx, bottomy) = (np.max(x), np.max(y))
    cropped = gray[topx:bottomx+1, topy:bottomy+1]

    # Use Tesseract to extract text
    text = pytesseract.image_to_string(cropped, config='--psm 11')

    return img, cropped, text

def main():
    # Upload image file
    uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])
    
    if uploaded_file is not None:
        # Save the uploaded image file temporarily
        with open("temp_image.jpg", "wb") as f:
            f.write(uploaded_file.getbuffer())

        # Process the image
        img, cropped, text = process_image("temp_image.jpg")

        # Display the original image
        st.image(cv2.cvtColor(img, cv2.COLOR_BGR2RGB), caption='Original Image', use_column_width=True)
        
        if text:
            # Display the cropped plate area
            st.image(cv2.cvtColor(cropped, cv2.COLOR_BGR2RGB), caption='Cropped Plate', use_column_width=True)

            # Display the extracted text
            st.write(f"Detected License Plate Number: {text}")
        else:
            st.write("No license plate detected.")

