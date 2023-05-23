
import cv2
import numpy as np
import imutils

def image_warp(name):
    frame = cv2.imread(name)
        
    x1 = 520
    x2 = 1399
    y1 = 53
    y2 = 920

    frame = frame[y1:y2, x1:x2]

    cv2.imwrite('test.png', frame)

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
        if area > 1000:
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

    rotate_vertical = imutils.rotate(frame, angle=270)
    rotate_horizontal = cv2.flip(rotate_vertical, 1)

    cv2.imwrite('images/warped.png', rotate_horizontal)

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
    global corners
    corners = cv2.cornerSubPix(gray,np.float32(centroids),(5,5),(-1,-1),criteria)

    cv2.imwrite('all-points.png',frame)

    return square_detection()

def board_array_creation(x):
    mat = np.zeros((9,9),dtype=object) 

    # i dont care how fucking redundant and schizophrinic this is, i just need it to work <3

    if x == True:
        for i in range(0,9,+1):
            for j in range(0,9,+1):
                if j == 0:
                    mat[i][j] = 3
                elif j == 1:
                    mat[i][j] = 80
                elif j == 2:
                    mat[i][j] = 151
                elif j == 3:
                    mat[i][j] = 228
                elif j == 4:
                    mat[i][j] = 298
                elif j == 5:
                    mat[i][j] = 375
                elif j == 6:
                    mat[i][j] = 445
                elif j == 7:
                    mat[i][j] = 520
                elif j == 8:
                    mat[i][j] = 595
    else:
        for i in range(0,9,+1):
            for j in range(0,9,+1):
                if i == 0:
                    mat[i][j] = 3
                elif i == 1:
                    mat[i][j] = 78
                elif i == 2:
                    mat[i][j] = 150
                elif i == 3:
                    mat[i][j] = 225
                elif i == 4:
                    mat[i][j] = 298
                elif i == 5:
                    mat[i][j] = 372
                elif i == 6:
                    mat[i][j] = 446
                elif i == 7:
                    mat[i][j] = 520
                elif i == 8:
                    mat[i][j] = 596
    return mat

def color_detection(x1, x2, y1, y2):
    new_frame = cv2.imread('images/warped.png') # update this to intially start with an image
    new_frame = new_frame[y1+10:y2-10 , x1+10:x2-10]
    #new_frame = new_frame[30:50 , 30:40]
    cv2.imwrite('images/square.png', new_frame)
    hsv = cv2.cvtColor(new_frame, cv2.COLOR_BGR2HSV)

    # Define the range of purple color in HSV
    lower_purple = (120, 50, 50)
    upper_purple = (150, 255, 255)

    # Define the range of red color in HSV
    lower_red1 = (0, 50, 50)
    upper_red1 = (10, 255, 255)
    lower_red2 = (170, 50, 50)
    upper_red2 = (180, 255, 255)

    # Threshold the HSV image to get purple and red colors
    mask_purple = cv2.inRange(hsv, lower_purple, upper_purple)
    mask_red1 = cv2.inRange(hsv, lower_red1, upper_red1)
    mask_red2 = cv2.inRange(hsv, lower_red2, upper_red2)

    # Combine the masks for purple and red colors
    mask = cv2.bitwise_or(mask_purple, mask_red1)
    mask = cv2.bitwise_or(mask, mask_red2)

    # cv2.imshow('yes',new_frame)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    # Check if any purple pixels were found
    if cv2.countNonZero(mask) > 0:
        return "o"
    else:
        return "e"

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
            # print(x1_coord,y1_coord)
            # print(x2_coord, y2_coord)
            rgb_val = color_detection(x1_coord, x2_coord, y1_coord, y2_coord)
            k+=1
            board_mat[i][j] = rgb_val
    print("-------------------------------------")
    print(board_mat)
    print("-------------------------------------")
    return board_mat

cap = cv2.VideoCapture(0)

while(True):
    ret, frame = cap.read()

    if ret:
        break

    else:
        print("No images detected!")

cv2.imwrite('images/capture.png', frame)

image_warp('images/capture.png')
