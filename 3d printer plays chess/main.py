from octo import Octoprint
from detection import *
import chess
import cv2
import numpy as np
import tkinter as tk
from stockfish import Stockfish
import time

def center(frame):
    image = cv2.imread(frame)

    gray  = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    blur = cv2.GaussianBlur(gray, (5,5), cv2.BORDER_DEFAULT)

    ret, thresh = cv2.threshold(blur, 200, 255, cv2.THRESH_BINARY_INV)

    contours, hierarchies = cv2.findContours(thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)


    blank = np.zeros(thresh.shape[:2],dtype='uint8')
    coords = np.zeros((1,32),dtype=object)
    
    cv2.drawContours(blank, contours, -1,(255, 0, 0), 1)

    j = -1
    for i in contours:
        M = cv2.moments(i)
        if M['m00'] != 0:
            j += 1
            cx = int(M['m10']/M['m00'])
            cy = int(M['m01']/M['m00'])
            if cx != 109 and j < 33:
                coords[0][j] = (cx,cy)
            
    return coords


def main():
    o = Octoprint()

    stockfishOld = None
    stockfishNew = None

    center_w = center('images/220px.png')
    center_b = center('images/220pxR.png')

    center_w = np.flip(center_w)
    center_b = np.flip(center_b)

    all_centers = np.zeros((1,64),dtype=object)

    k = 0
    q = 0
    x = 0
    for i in range(0,8,1):
        if i % 2 == 0:
            for j in range(0,8,1):
                if j % 2 == 0:
                    all_centers[0][x] = center_w[0][k]
                    k += 1
                else:
                    all_centers[0][x] = center_b[0][q]
                    q += 1
                x += 1
        else:
            for a in range(0,8,1):
                if a % 2 == 0:
                    all_centers[0][x] = center_b[0][k]
                    k += 1
                else:
                    all_centers[0][x] = center_w[0][q]
                    q += 1
                x += 1

    stockfish = Stockfish('/opt/homebrew/Cellar/stockfish/15.1/bin/stockfish')
    stockfish.set_depth(20)
    stockfish.set_skill_level(20)

    fen_mat = np.zeros((8,8),dtype=object)

    letters = ["a","b","c","d","e","f","g","h"]

    for i in range(0, 8, 1):
        for j in range(0, 8, 1):
            fen_mat[i][j] = letters[7-i] + str(abs(j-8))

    updated_mat = np.zeros((8,8),dtype=object)
    board = chess.Board()
    cap = cv2.VideoCapture(0)

    while(True):
        ret, frame = cap.read()

        if ret:
            break

        else:
            print("No images detected!")

    cv2.imwrite('images/capture.png', frame)

    initial_mat = image_warp('images/capture.png')

    print("game begins")
    print("grabbing image of board")

    while not board.is_game_over():
        def button_click():
            print("Move recognized")
            #updated_mat = image_warp('')
            window.destroy()
        print("make move")

        # present the button
        window = tk.Tk()
        button = tk.Button(window, text="Click me!", command=button_click)
        button.pack()
        window.mainloop() 

        cap = cv2.VideoCapture(0)

        while(True):
            ret, frame = cap.read()

            if ret:
                break

            else:
                print("No images detected!")

        cv2.imwrite('images/move.png', frame)

        updated_mat = image_warp('images/move.png')

        #logic for pieces
        newPos = None
        oldPos = None

        moveDestinationOld = None
        moveDestinationNew = None

        # checks for changes in the board
        x = 0
        y = 0
        for i in range(0, 8, +1):
            for j in range(0, 8, +1):                
                if initial_mat[i][j] != updated_mat[i][j]:
                    if x == 0:
                        newPos = fen_mat[i][j]
                        x += 1
                        moveDestinationNew = 64 - y
                    else:
                        oldPos = fen_mat[i][j]
                        moveDestinationOld = 64 - y
                y += 1
        
        print("old:", moveDestinationOld, "new:", moveDestinationNew)

        pos = "{0}{1}".format(oldPos, newPos)
        print(pos)

        board.push_san(pos)

        stockfish.set_fen_position(board.fen())
        stockfish.get_evaluation()
        best_move = stockfish.get_top_moves(1)
        board.push_san(best_move[0]['Move'])

        bm = best_move[0]['Move']

        # returns stock fish positions in terms of which square (0-63)
        y = 0
        for i in range(0, len(fen_mat), 1):
            for j in range(0, len(fen_mat), 1):
                if fen_mat[i][j] == bm[0:2]:
                    stockfishOld = 64 - y
                elif fen_mat[i][j] == bm[2:4]:
                    stockfishNew = 64 - y
                y += 1

        print("old:", stockfishOld, "new:", stockfishNew)

        #  makes move based off occupancy of square
        x = 0
        for i in range(0,8,1):
            for j in range(0,8,1):
                if stockfishNew == x:
                    if updated_mat[i][j] == "e":
                        o.move(all_centers[0][stockfishOld][0], all_centers[0][stockfishOld][1],all_centers[0][stockfishNew][0], all_centers[0][stockfishNew][1])
                    if updated_mat[i][j] == "O":
                        o.remove(all_centers[0][x][0], all_centers[0][x][1],all_centers[0][stockfishNew][0], all_centers[0][stockfishNew][1])
        
        print(board)
        print("-----------------")

if __name__ == '__main__':
    main()