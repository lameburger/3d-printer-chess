import cv2
import numpy as np
import imutils
from color_detection.detect import Mask
import webcolors
from matplotlib import pyplot as plt
import chess

frame = cv2.imread('savedImage.jpg')

x1 = 606
x2 = 795
y1 = 102
y2 = 733

frame = frame[y1:y1+y2, x1:x1+x2]

gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
img_blurred = cv2.GaussianBlur(gray_frame, (5, 5), 1)
edge_image_blurred = cv2.Canny(img_blurred, 60, 180)

kernel = np.ones((5, 5))
imgDil = cv2.dilate(edge_image_blurred, kernel, iterations=2)

key_points = cv2.findContours(imgDil, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
contours = imutils.grab_contours(key_points)

biggest_contour = np.array([])
for contour in contours:
    area = cv2.contourArea(contour)
    if area > 100:
        perimeter = cv2.arcLength(contour, True)
        approximation = cv2.approxPolyDP(contour, 0.05 * perimeter, True)
        if len(approximation) == 4:
            biggest_contour = approximation
if biggest_contour.size != 0:
    cv2.drawContours(frame, biggest_contour, -1, (0, 255, 0), 15)

def index(x,y):
    return biggest_contour[x][0][y]

width,height = 600,600

pts1 = np.float32([[index(2,0),index(2,1)],[index(3,0),index(3,1)],[index(1,0),index(1,1)],[index(0,0),index(0,1)]])
pts2 = np.float32([[0,0],[width,0],[0,height],[width,height]])

matrix = cv2.getPerspectiveTransform(pts1,pts2)

frame = cv2.warpPerspective(frame,matrix,(width,height))

cv2.imwrite('warped.png', frame)

gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

harris_corners= cv2.cornerHarris(gray, 3, 3, 0.05)

kernel= np.ones((7,7), np.uint8)

harris_corners= cv2.dilate(harris_corners, kernel, iterations= 2)


frame[harris_corners > 0.025 * harris_corners.max()]= [255,127,127]
harris_corners = cv2.dilate(harris_corners, None)
ret, harris_corners = cv2.threshold(harris_corners,0.1*harris_corners.max(),255,0)

harris_corners = np.uint8(harris_corners)
ret, labels, stats, centroids = cv2.connectedComponentsWithStats(harris_corners)

criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 0.1)
corners = cv2.cornerSubPix(gray,np.float32(centroids),(5,5),(-1,-1),criteria)

def independent_shift(arr, row, shifts):
    i=0
    while i < shifts:
        last_element = arr[row, -1]

        # Move the last element to the front
        shifted_row = np.concatenate(([last_element], arr[row, :-1]))

        # Replace the second row of the original array with the shifted row
        arr[row, :] = shifted_row
        i+=1
    return arr

def board_array_creation(x):
    mat = np.zeros((9,9),dtype=object)

    x_iterations = 1
    y_iterations = 1
    if x == True:
        for i in range((len(mat)), 0, -1):
            i -= 1
            for j in range(0, (len(mat))):
                mat[i][j] = int(corners[x_iterations][0])
                x_iterations += 1
    elif x == False:
        for i in range(0, (len(mat)), +1):
            for j in range(0, len(mat)):
                mat[i][j] = int(corners[y_iterations][1])
                y_iterations += 1

    for i in range(0, len(mat)):
        if i == 1:
            independent_shift(mat, i,1)
        elif i == 3:
            independent_shift(mat, i,1)
        elif i == 5:
            independent_shift(mat, i,1)
        elif i == 7:
            independent_shift(mat, i,1)
        elif i == 2:
            mat[2].sort()
        elif i == 4:
            mat[4].sort()
    return mat

def color_detection(x1, x2, y1, y2):

    new_frame = cv2.imread('red.png') #update this to intially start with an image
    new_frame = new_frame[y1:y2 , x1:x2]

    color = Mask.detect_dominant(new_frame)
    # print(color)

    if color[0] in range(200, 240, +1) and color[1] in range(200, 250, +1):
        return "e"
    elif color[0] in range(0, 100, +1) and color[1] in range(10, 50, +1):
        return "e"
    elif color[0] in range(240, 250, +1) and color[1] in range(0, 50, +1):
        return("w")
    elif color[0] in range(20, 70, + 1) and color[1] in range(20, 70, + 1):
        return ("b")

def square_detection():
    x_arr = board_array_creation(True)
    y_arr = board_array_creation(False)

    board_mat = np.zeros((8,8),dtype=object)

    k = 0

    for i in range(0, len(x_arr) - 1, 1):
        for j in range(0, len(y_arr)- 1,1):
            x1_coord = x_arr[i][j]
            y1_coord = y_arr[i][j]
            x2_coord = x_arr[i+1][j+1]
            y2_coord = y_arr[i+1][j+1]
            rgb_val = color_detection(x1_coord, x2_coord, y1_coord, y2_coord)
            k+=1
            board_mat[i][j] = rgb_val, k
    print(board_mat)
    return board_mat

def movement_update(old_mat, new_mat):
    new_mat = np.zeros((8,8), dtype=object)

    p = 0

    for i in range(0, 8, 1):
        for j in range(0, 8, 1):
            p += 1
            if old_mat[i][j] != new_mat[i][j]:
                break