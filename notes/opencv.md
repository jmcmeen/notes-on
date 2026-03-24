# Introduction to OpenCV

## Table of Contents

1. [What is OpenCV?](#what-is-opencv)
2. [Installation](#installation)
3. [Reading and Writing Images](#reading-and-writing-images)
4. [Color Spaces](#color-spaces)
5. [Drawing on Images](#drawing-on-images)
6. [Image Transformations](#image-transformations)
7. [Filtering and Edge Detection](#filtering-and-edge-detection)
8. [Thresholding](#thresholding)
9. [Contour Detection](#contour-detection)
10. [Feature Detection](#feature-detection)
11. [Template Matching](#template-matching)
12. [Video Processing](#video-processing)
13. [Object Detection with Cascades](#object-detection-with-cascades)
14. [Practice Exercises](#practice-exercises)
15. [Summary](#summary)

---

## What is OpenCV?

OpenCV (Open Source Computer Vision Library) is the most widely used library for computer vision and image processing. It provides:

- **Image Processing**: Reading, writing, transforming, and filtering images
- **Video Analysis**: Capturing and processing video streams frame by frame
- **Object Detection**: Haar cascades, template matching, feature matching
- **Feature Detection**: Corner detection, SIFT, ORB, and other keypoint detectors
- **Drawing Utilities**: Lines, shapes, and text annotation on images
- **Color Space Conversion**: BGR, RGB, HSV, grayscale, and more

---

## Installation

```bash
# Install the main OpenCV package
pip install opencv-python

# Install with extra modules (SIFT, SURF, etc.)
pip install opencv-contrib-python
```

```python
import cv2
import numpy as np

# Verify installation
print(cv2.__version__)  # e.g., 4.9.0
```

---

## Reading and Writing Images

```python
import cv2

# Read an image from disk
# cv2.IMREAD_COLOR       - loads color image (default)
# cv2.IMREAD_GRAYSCALE   - loads image as grayscale
# cv2.IMREAD_UNCHANGED   - loads image including alpha channel
img = cv2.imread("photo.jpg", cv2.IMREAD_COLOR)

# Check if the image was loaded successfully
if img is None:
    print("Error: Could not load image")
else:
    print(img.shape)    # (height, width, channels), e.g., (480, 640, 3)
    print(img.dtype)    # uint8 (values 0-255)

# Display in a window
cv2.imshow("My Image", img)  # window name, image array
cv2.waitKey(0)               # wait for a key press (0 = indefinitely)
cv2.destroyAllWindows()

# Save the image to a new file (format inferred from extension)
cv2.imwrite("output.png", img)

# Save with compression parameters
cv2.imwrite("output.jpg", img, [cv2.IMWRITE_JPEG_QUALITY, 90])  # JPEG quality 0-100
```

### Accessing Pixel Values

```python
import cv2

img = cv2.imread("photo.jpg")

# Access a single pixel (row, col) - returns BGR tuple
pixel = img[100, 200]       # e.g., [255, 128, 64] -> (B, G, R)
blue  = img[100, 200, 0]    # Blue channel value
green = img[100, 200, 1]    # Green channel value
red   = img[100, 200, 2]    # Red channel value

# Modify a pixel
img[100, 200] = [0, 255, 0]  # Set pixel to green

# Extract a region of interest (ROI) via slicing
roi = img[50:200, 100:300]   # rows 50-199, cols 100-299
```

---

## Color Spaces

```python
import cv2
import numpy as np

img = cv2.imread("photo.jpg")

# OpenCV loads images in BGR order by default (not RGB)
rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)    # convert to RGB
gray    = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)   # convert to grayscale
hsv     = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)    # convert to HSV

# HSV ranges in OpenCV: Hue 0-179, Saturation 0-255, Value 0-255

# Color-based filtering with HSV
lower_blue = np.array([100, 50, 50])    # lower bound of blue hue
upper_blue = np.array([130, 255, 255])  # upper bound of blue hue
mask = cv2.inRange(hsv, lower_blue, upper_blue)   # binary mask
result = cv2.bitwise_and(img, img, mask=mask)      # apply mask to image
```

---

## Drawing on Images

```python
import cv2
import numpy as np

# Create a blank black image (height=400, width=600, 3 channels)
canvas = np.zeros((400, 600, 3), dtype=np.uint8)

# Draw a line: image, start_point, end_point, color_BGR, thickness
cv2.line(canvas, (50, 50), (550, 50), (255, 0, 0), 2)

# Draw a rectangle: image, top_left, bottom_right, color_BGR, thickness
cv2.rectangle(canvas, (50, 80), (250, 200), (0, 255, 0), 3)

# Filled rectangle (thickness = -1)
cv2.rectangle(canvas, (300, 80), (500, 200), (0, 0, 255), -1)

# Draw a circle: image, center, radius, color_BGR, thickness
cv2.circle(canvas, (150, 300), 50, (255, 255, 0), 2)
cv2.circle(canvas, (400, 300), 50, (0, 255, 255), -1)  # filled

# Draw an ellipse: image, center, axes, angle, startAngle, endAngle, color, thickness
cv2.ellipse(canvas, (300, 300), (80, 40), 0, 0, 360, (255, 0, 255), 2)

# Draw a polyline
pts = np.array([[50, 350], [150, 380], [250, 350], [200, 370]], np.int32)
pts = pts.reshape((-1, 1, 2))
cv2.polylines(canvas, [pts], True, (255, 255, 255), 2)  # closed polyline

# Add text: image, text, origin, font, scale, color, thickness
cv2.putText(canvas, "OpenCV Drawing", (150, 30),
            cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
```

---

## Image Transformations

### Resizing

```python
import cv2

img = cv2.imread("photo.jpg")

# Resize to specific dimensions (width, height)
resized = cv2.resize(img, (320, 240))

# Resize by scale factor
scaled = cv2.resize(img, None, fx=0.5, fy=0.5)  # half size

# Interpolation methods:
# cv2.INTER_NEAREST  - fastest, blocky
# cv2.INTER_LINEAR   - default, good for enlarging
# cv2.INTER_AREA     - best for shrinking
# cv2.INTER_CUBIC    - smoother enlarging
upscaled = cv2.resize(img, None, fx=2.0, fy=2.0, interpolation=cv2.INTER_CUBIC)
```

### Cropping, Rotation, and Flipping

```python
import cv2

img = cv2.imread("photo.jpg")
h, w = img.shape[:2]

# Cropping is just NumPy slicing
cropped = img[50:300, 100:400]  # rows 50-299, cols 100-399

# Rotation using getRotationMatrix2D: center, angle, scale
center = (w // 2, h // 2)
matrix = cv2.getRotationMatrix2D(center, 45, 1.0)  # rotate 45 degrees
rotated = cv2.warpAffine(img, matrix, (w, h))

# Simple 90-degree rotations
rot_90  = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)
rot_180 = cv2.rotate(img, cv2.ROTATE_180)

# Flipping: 0=vertical, 1=horizontal, -1=both
flipped_h = cv2.flip(img, 1)  # horizontal mirror
flipped_v = cv2.flip(img, 0)  # vertical flip
```

### Affine and Perspective Transforms

```python
import cv2
import numpy as np

img = cv2.imread("photo.jpg")
h, w = img.shape[:2]

# Affine transform: 3 pairs of corresponding points
src_pts = np.float32([[50, 50], [200, 50], [50, 200]])
dst_pts = np.float32([[10, 100], [200, 50], [100, 250]])
affine_matrix = cv2.getAffineTransform(src_pts, dst_pts)
affine_result = cv2.warpAffine(img, affine_matrix, (w, h))

# Perspective transform: 4 pairs of corresponding points
src_pts = np.float32([[56, 65], [368, 52], [28, 387], [389, 390]])
dst_pts = np.float32([[0, 0], [300, 0], [0, 300], [300, 300]])
persp_matrix = cv2.getPerspectiveTransform(src_pts, dst_pts)
persp_result = cv2.warpPerspective(img, persp_matrix, (300, 300))
```

---

## Filtering and Edge Detection

```python
import cv2
import numpy as np

img = cv2.imread("photo.jpg")

# Average blur - simple mean filter (kernel must be odd)
avg_blur = cv2.blur(img, (5, 5))

# Gaussian blur - weighted average, better noise reduction
gauss_blur = cv2.GaussianBlur(img, (5, 5), sigmaX=0)

# Median blur - excellent for salt-and-pepper noise
median_blur = cv2.medianBlur(img, 5)

# Bilateral filter - smooths while keeping edges sharp
bilateral = cv2.bilateralFilter(img, d=9, sigmaColor=75, sigmaSpace=75)
```

### Edge Detection

```python
import cv2
import numpy as np

img = cv2.imread("photo.jpg")
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Canny edge detection: image, lower_threshold, upper_threshold
edges_canny = cv2.Canny(gray, 100, 200)

# Sobel operator: computes gradient in x or y direction
sobel_x = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3)  # horizontal gradient
sobel_y = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=3)  # vertical gradient
sobel_combined = cv2.magnitude(sobel_x, sobel_y)

# Laplacian - second derivative, detects edges in all directions
laplacian = cv2.Laplacian(gray, cv2.CV_64F)
```

### Morphological Operations

```python
import cv2
import numpy as np

img = cv2.imread("photo.jpg", cv2.IMREAD_GRAYSCALE)
kernel = np.ones((5, 5), np.uint8)  # structuring element

eroded  = cv2.erode(img, kernel, iterations=1)   # shrinks bright regions
dilated = cv2.dilate(img, kernel, iterations=1)   # expands bright regions
opened  = cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel)    # erosion then dilation
closed  = cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel)   # dilation then erosion
gradient = cv2.morphologyEx(img, cv2.MORPH_GRADIENT, kernel)  # outlines
```

---

## Thresholding

```python
import cv2

img = cv2.imread("photo.jpg", cv2.IMREAD_GRAYSCALE)

# Binary threshold: pixels > 127 become 255, rest become 0
ret, thresh_binary = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)

# Inverse binary threshold
ret, thresh_inv = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY_INV)

# Truncate: pixels > 127 are set to 127
ret, thresh_trunc = cv2.threshold(img, 127, 255, cv2.THRESH_TRUNC)
```

### Adaptive and Otsu's Thresholding

```python
import cv2

img = cv2.imread("document.jpg", cv2.IMREAD_GRAYSCALE)

# Adaptive mean: threshold is the mean of a local neighborhood minus C
adaptive_mean = cv2.adaptiveThreshold(
    img, 255, cv2.ADAPTIVE_THRESH_MEAN_C,
    cv2.THRESH_BINARY, 11, 2  # blockSize=11, C=2
)

# Adaptive Gaussian: weighted sum of neighborhood minus C
adaptive_gauss = cv2.adaptiveThreshold(
    img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
    cv2.THRESH_BINARY, 11, 2
)

# Otsu's method: automatically finds the optimal threshold
blurred = cv2.GaussianBlur(img, (5, 5), 0)
ret, otsu = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
print(f"Otsu threshold: {ret}")
```

---

## Contour Detection

```python
import cv2

img = cv2.imread("shapes.jpg")
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
ret, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)

# Find contours
# mode: RETR_EXTERNAL (outer only), RETR_TREE (full hierarchy)
# method: CHAIN_APPROX_SIMPLE (compress), CHAIN_APPROX_NONE (all points)
contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
print(f"Found {len(contours)} contours")

# Draw all contours
output = img.copy()
cv2.drawContours(output, contours, -1, (0, 255, 0), 2)  # -1 = draw all
```

### Contour Properties

```python
import cv2

img = cv2.imread("shapes.jpg")
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
ret, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

for i, cnt in enumerate(contours):
    area = cv2.contourArea(cnt)                # area of the contour
    perimeter = cv2.arcLength(cnt, True)       # perimeter (True = closed)
    x, y, w, h = cv2.boundingRect(cnt)         # bounding rectangle

    # Centroid using moments
    M = cv2.moments(cnt)
    if M["m00"] != 0:
        cx = int(M["m10"] / M["m00"])
        cy = int(M["m01"] / M["m00"])

    # Contour approximation (simplify shape)
    epsilon = 0.02 * perimeter
    approx = cv2.approxPolyDP(cnt, epsilon, True)
    print(f"Contour {i}: area={area:.0f}, vertices={len(approx)}")
```

---

## Feature Detection

### Harris Corners and SIFT

```python
import cv2
import numpy as np

img = cv2.imread("chessboard.jpg")
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Harris corner detection
gray32 = np.float32(gray)
corners = cv2.cornerHarris(gray32, blockSize=2, ksize=3, k=0.04)
corners = cv2.dilate(corners, None)
img[corners > 0.01 * corners.max()] = [0, 0, 255]  # mark corners in red
```

```python
import cv2

img = cv2.imread("photo.jpg")
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# SIFT: Scale-Invariant Feature Transform
sift = cv2.SIFT_create()
keypoints, descriptors = sift.detectAndCompute(gray, None)
print(f"SIFT: {len(keypoints)} keypoints, descriptor shape: {descriptors.shape}")

# ORB: Oriented FAST and Rotated BRIEF (faster, patent-free)
orb = cv2.ORB_create(nfeatures=500)
kp_orb, des_orb = orb.detectAndCompute(gray, None)
print(f"ORB: {len(kp_orb)} keypoints, descriptor shape: {des_orb.shape}")

# Draw keypoints
output = cv2.drawKeypoints(img, keypoints, None,
                           flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
```

### Feature Matching

```python
import cv2

img1 = cv2.imread("object.jpg", cv2.IMREAD_GRAYSCALE)
img2 = cv2.imread("scene.jpg", cv2.IMREAD_GRAYSCALE)

# Detect features with ORB
orb = cv2.ORB_create(nfeatures=1000)
kp1, des1 = orb.detectAndCompute(img1, None)
kp2, des2 = orb.detectAndCompute(img2, None)

# Match with Brute-Force (Hamming distance for binary descriptors)
bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
matches = bf.match(des1, des2)
matches = sorted(matches, key=lambda m: m.distance)  # sort by quality

# Draw the top 20 matches
result = cv2.drawMatches(img1, kp1, img2, kp2, matches[:20], None,
                         flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)
```

---

## Template Matching

```python
import cv2
import numpy as np

img = cv2.imread("scene.jpg")
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
template = cv2.imread("template.jpg", cv2.IMREAD_GRAYSCALE)
th, tw = template.shape[:2]

# Perform template matching
result = cv2.matchTemplate(gray, template, cv2.TM_CCOEFF_NORMED)

# Find the best match location
min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
top_left = max_loc  # for TM_CCOEFF_NORMED, best match is maximum
bottom_right = (top_left[0] + tw, top_left[1] + th)
cv2.rectangle(img, top_left, bottom_right, (0, 255, 0), 2)

# Multiple matches: find all locations above a threshold
threshold = 0.8
locations = np.where(result >= threshold)
for pt in zip(*locations[::-1]):
    cv2.rectangle(img, pt, (pt[0] + tw, pt[1] + th), (0, 0, 255), 2)
print(f"Found {len(locations[0])} matches above {threshold}")
```

---

## Video Processing

### Reading and Displaying Video

```python
import cv2

# Open a video file (or webcam with index 0)
cap = cv2.VideoCapture("video.mp4")

if not cap.isOpened():
    print("Error: Cannot open video")
    exit()

# Get video properties
fps    = cap.get(cv2.CAP_PROP_FPS)
width  = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
total  = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
print(f"Video: {width}x{height} @ {fps} FPS, {total} frames")

# Read and process frames
while True:
    ret, frame = cap.read()  # ret=True if frame was read successfully
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # process each frame
    cv2.imshow("Video", gray)

    if cv2.waitKey(1) & 0xFF == ord('q'):  # press 'q' to quit
        break

cap.release()
cv2.destroyAllWindows()
```

### Writing Video

```python
import cv2

cap = cv2.VideoCapture("input.mp4")
fps    = cap.get(cv2.CAP_PROP_FPS)
width  = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

# Define codec and create VideoWriter
fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # also: 'XVID', 'MJPG', 'H264'
out = cv2.VideoWriter("output.mp4", fourcc, fps, (width, height))

while True:
    ret, frame = cap.read()
    if not ret:
        break
    # Add frame number overlay
    frame_num = int(cap.get(cv2.CAP_PROP_POS_FRAMES))
    cv2.putText(frame, f"Frame: {frame_num}", (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    out.write(frame)

cap.release()
out.release()
```

---

## Object Detection with Cascades

```python
import cv2

img = cv2.imread("people.jpg")
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Load the pre-trained Haar cascade for face detection
face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)

# Detect faces
faces = face_cascade.detectMultiScale(
    gray,
    scaleFactor=1.1,    # image size reduction at each scale
    minNeighbors=5,     # higher = fewer detections, fewer false positives
    minSize=(30, 30)
)

print(f"Detected {len(faces)} face(s)")
for (x, y, w, h) in faces:
    cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
```

### Face and Eye Detection

```python
import cv2

img = cv2.imread("portrait.jpg")
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)
eye_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_eye.xml"
)

faces = face_cascade.detectMultiScale(gray, 1.1, 5)
for (x, y, w, h) in faces:
    cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)

    # Search for eyes only within the face ROI
    roi_gray = gray[y:y+h, x:x+w]
    roi_color = img[y:y+h, x:x+w]
    eyes = eye_cascade.detectMultiScale(roi_gray, 1.1, 3)
    for (ex, ey, ew, eh) in eyes:
        cv2.rectangle(roi_color, (ex, ey), (ex + ew, ey + eh), (0, 255, 0), 2)
```

---

## Practice Exercises

### Exercise 1: Image Editor

```python
# Build a simple image editor with filters and brightness/contrast

import cv2
import numpy as np

def adjust_brightness_contrast(img, brightness=0, contrast=0):
    alpha = 1 + contrast / 100  # contrast multiplier
    beta = brightness            # brightness offset
    return cv2.convertScaleAbs(img, alpha=alpha, beta=beta)

def apply_filter(img, filter_name):
    if filter_name == "blur":
        return cv2.GaussianBlur(img, (15, 15), 0)
    elif filter_name == "sharpen":
        kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])
        return cv2.filter2D(img, -1, kernel)
    elif filter_name == "edges":
        return cv2.Canny(cv2.cvtColor(img, cv2.COLOR_BGR2GRAY), 100, 200)
    return img

img = cv2.imread("photo.jpg")
result = adjust_brightness_contrast(img, brightness=30, contrast=20)
result = apply_filter(result, "sharpen")
cv2.imwrite("edited_photo.jpg", result)
```

### Exercise 2: Motion Detection

```python
# Detect motion by comparing consecutive frames

import cv2

cap = cv2.VideoCapture(0)
ret, prev_frame = cap.read()
prev_gray = cv2.GaussianBlur(cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY), (21, 21), 0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    gray = cv2.GaussianBlur(cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY), (21, 21), 0)
    diff = cv2.absdiff(prev_gray, gray)                         # frame difference
    ret, thresh = cv2.threshold(diff, 25, 255, cv2.THRESH_BINARY)
    thresh = cv2.dilate(thresh, None, iterations=2)

    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for cnt in contours:
        if cv2.contourArea(cnt) < 500:  # ignore small movements
            continue
        x, y, w, h = cv2.boundingRect(cnt)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    cv2.imshow("Motion Detection", frame)
    prev_gray = gray
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
```

### Exercise 3: Document Scanner

```python
# Detect document edges and apply perspective transform

import cv2
import numpy as np

def order_points(pts):
    rect = np.zeros((4, 2), dtype="float32")
    s = pts.sum(axis=1)
    rect[0] = pts[np.argmin(s)]   # top-left
    rect[2] = pts[np.argmax(s)]   # bottom-right
    d = np.diff(pts, axis=1)
    rect[1] = pts[np.argmin(d)]   # top-right
    rect[3] = pts[np.argmax(d)]   # bottom-left
    return rect

img = cv2.imread("document.jpg")
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
edges = cv2.Canny(cv2.GaussianBlur(gray, (5, 5), 0), 75, 200)

contours, _ = cv2.findContours(edges, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
contours = sorted(contours, key=cv2.contourArea, reverse=True)

for cnt in contours:
    approx = cv2.approxPolyDP(cnt, 0.02 * cv2.arcLength(cnt, True), True)
    if len(approx) == 4:  # found a quadrilateral
        pts = order_points(approx.reshape(4, 2))
        dst = np.array([[0, 0], [500, 0], [500, 700], [0, 700]], dtype="float32")
        M = cv2.getPerspectiveTransform(pts, dst)
        scanned = cv2.warpPerspective(img, M, (500, 700))
        cv2.imwrite("scanned.jpg", scanned)
        break
```

---

## Summary

These notes cover the fundamental concepts of OpenCV for computer vision in Python:

1. **Reading/Writing Images**: `imread`, `imwrite`, `imshow`, pixel access with NumPy slicing
2. **Color Spaces**: BGR to RGB, grayscale, HSV with `cvtColor`; color filtering with `inRange`
3. **Drawing**: Lines, rectangles, circles, ellipses, polylines, and text
4. **Transformations**: `resize`, crop via slicing, `rotate`, `flip`, `warpAffine`, `warpPerspective`
5. **Filtering**: Blur, Gaussian, median, bilateral; Canny and Sobel edge detection
6. **Thresholding**: Binary, adaptive (mean/Gaussian), and Otsu's automatic thresholding
7. **Contours**: `findContours`, `drawContours`, area, perimeter, bounding shapes, moments
8. **Features**: Harris corners, SIFT, ORB; brute-force feature matching
9. **Template Matching**: `matchTemplate` for locating objects in images
10. **Video**: `VideoCapture`, frame-by-frame processing, `VideoWriter`
11. **Cascades**: Haar cascade classifiers for face and eye detection

### Next Steps

1. Explore deep learning-based object detection with OpenCV's DNN module
2. Learn about optical flow for motion tracking
3. Study image stitching and panorama creation
4. Experiment with OpenCV's ArUco marker detection
5. Integrate OpenCV with machine learning frameworks like PyTorch

### Additional Resources

- **OpenCV Documentation**: <https://docs.opencv.org/>
- **OpenCV-Python Tutorials**: <https://docs.opencv.org/4.x/d6/d00/tutorial_py_root.html>
- **PyImageSearch**: <https://pyimagesearch.com/>
- **Learn OpenCV**: <https://learnopencv.com/>
