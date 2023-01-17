# pop up a window with a button

# -*- coding:utf-8 -*-


import tkinter as tk
from tkinter import filedialog
import cv2
# import re
import numpy as np
# import pdf2image
from pdf2image import convert_from_path
import os
from datetime import datetime
#from skimage import io
#from skimage import transform as tf

global saving_path

def read_config():
    # check there is config.ini
    global saving_path
    if os.path.isfile('.\\config.ini') == False:
        config = open("config.ini", "w")
        config.write(".")
        config.close()
        config = open("config.ini", "r")
        saving_path = config.read()
        config.close()

    else:
        config = open("config.ini", "r")
        saving_path = config.read()
        config.close()
    # label.destroy()

    return saving_path


def time():
    now = datetime.now()
    now_time = now.strftime('%Y-%m-%d-%H-%M-%S')
    label = tk.Label(window, text=now_time, font=("Arial", 12), fg="red")
    label.place(x=630, y=570)
    window.after(1000, time)


# create the window
window = tk.Tk()
# the window has a title of "OMR Reader"
window.title("PDF to PNG with Student ID Number and Date")

# resolution of the window is 800*600
window.geometry("800x600")

time()
read_config()
os.chdir(os.path.dirname(__file__))
logo = tk.PhotoImage(file="4al.png")
label = tk.Label(window, image=logo)
label.configure(image=logo)
label.pack(side="left")
button1 = tk.Button(window, text="Set Folder", width=10, height=2)
button1.place(x=700, y=10)
# create a button to the rightmost of the window
button2 = tk.Button(window, text="Open", width=10, height=2)
# place the button to the rightmost of the window
button2.place(x=700, y=70)
# place the current time on the window

f1 = tk.Label(window, text=saving_path, font=("Arial", 12), fg="red")
f1.place(x=10, y=570)

def choose_path():

    saving_path = filedialog.askdirectory()
    # if not chosen, return
    if saving_path == "":
        return
    else:
        config = open("config.ini", "w")
        config.write(str(saving_path))
        config.close()
        config = open("config.ini", "r")
        saving_path = config.read()
        config.close()

    # delete the previous label
    # create a new label
    f1.config(text=saving_path)
    window.update()
    window.mainloop()

    return saving_path

"""
def isKorean(text):
    hangul = re.compile('[\u3131-\u3163\uac00-\ud7a3]+')
    result = hangul.findall(text)
    if len(result) > 0:
        return True
    else:
        return False
"""
def renaming(saving_path):
    path = '.\\extract'
    file_list = os.listdir(path)
    for file in file_list:
        img = cv2.imread(path + '\\' + file)

        # if img is existing
        if img is not None:
            print("File opened")
            # resize the image into 992*1403

            #img = cv2.resize(img, (992, 1403))
            # find a rectangle with the largest area
            # and cut out the rectangle
            # correct the distortion of img
            #afine_tf = tf.AffineTransform(scale=(1, 1), rotation=0, shear=0, translation=(0, 0))
            #warped = tf.warp(warped, inverse_map=afine_tf)
            #cv2.imshow("warped", warped)
            #cv2.waitKey(0)
            #cv2.destroyAllWindows()


            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            gray = cv2.GaussianBlur(gray, (5, 5), 0)
            #edged = cv2.Canny(gray, 75, 200)
            edged = cv2.Canny(gray, 75, 200)
            #cv2.imshow("edged", edged)
            #cv2.waitKey(0)
            #cv2.destroyAllWindows()

            contours, hierarchy = cv2.findContours(edged, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            contours = sorted(contours, key=cv2.contourArea, reverse=True)
            for c in contours:
                peri = cv2.arcLength(c, True)
                approx = cv2.approxPolyDP(c, 0.02 * peri, True)
                # approx = cv2.approxPolyDP(c, 0.1 * peri, True)
                if len(approx) == 4:
                    screenCnt = approx
                    break
            #print(screenCnt)
            cv2.drawContours(img, [screenCnt], -1, (0, 255, 255), 2)
            pts = screenCnt.reshape(4, 2)
            rect = np.zeros((4, 2), dtype="float32")
            s = pts.sum(axis=1)
            rect[0] = pts[np.argmin(s)]
            rect[2] = pts[np.argmax(s)]
            diff = np.diff(pts, axis=1)
            rect[1] = pts[np.argmin(diff)]
            rect[3] = pts[np.argmax(diff)]
            (tl, tr, br, bl) = rect
            widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
            widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
            maxWidth = max(int(widthA), int(widthB))
            heightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
            heightB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
            maxHeight = max(int(heightA), int(heightB))
            dst = np.array([[0, 0], [maxWidth - 1, 0], [maxWidth - 1, maxHeight - 1], [0, maxHeight - 1]], dtype="float32")
            M = cv2.getPerspectiveTransform(rect, dst)
            warped = cv2.warpPerspective(img, M, (maxWidth, maxHeight))

            # show image on the window dialog box

            cv2.imwrite("scanned.png", warped)
            logo = tk.PhotoImage(file="scanned.png")
            #label = tk.Label(window, image=logo)
            label.config(image=logo)
            #label.pack(side="left")


            # cv2.imwrite("scanned.png", warped)
            # cv2.imwrite("original.png", img)
            # cv2.imwrite("edged.png", edged)
            # cv2.imwrite("gray.png", gray)
            # cv2.imwrite("contours.png", img)

            """
            
            # Cut out the box (627, 85, 880, 210) from the image
            # and make it in black and white
            omr_ID = img[85:220, 620:880]
            omr_ID = cv2.cvtColor(omr_ID, cv2.COLOR_BGR2GRAY)
            omr_ID = cv2.threshold(omr_ID, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

            #cv2.imshow("omr_ID", omr_ID)
            #cv2.waitKey(0)
            """



            #cv2.imshow('img', img)
            #cv2.waitKey(0)
            #cv2.destroyAllWindows()

            warped = cv2.cvtColor(warped, cv2.COLOR_BGR2GRAY)
            warped = cv2.threshold(warped, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
            # split the image into 5 lines

            Width = int(warped.shape[1])
            Height = int(warped.shape[0]/5)
            Width2 = int(warped.shape[1]/10)

            #print(Width, Height, Width2)
            omr_ID_1 = warped[0:(Height), 0:(Width)]
            omr_ID_2 = warped[(Height):(2*Height), 0:(Width)]
            omr_ID_3 = warped[(2*Height):(3*Height), 0:(Width)]
            omr_ID_4 = warped[(3*Height):(4*Height), 0:(Width)]
            omr_ID_5 = warped[(4*Height):(5*Height), 0:(Width)]
            """
            cv2.imshow("omr_ID_1", omr_ID_1)
            cv2.imshow("omr_ID_2", omr_ID_2)
            cv2.imshow("omr_ID_3", omr_ID_3)
            cv2.imshow("omr_ID_4", omr_ID_4)
            cv2.imshow("omr_ID_5", omr_ID_5)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
            """
            # define one dimension array with 9 elements
            ID_1 = np.zeros(10)
            ID_2 = np.zeros(10)
            ID_3 = np.zeros(10)
            ID_4 = np.zeros(10)
            ID_5 = np.zeros(10)

            # split the image into 9 columns
            for i in range(10):
                ID_1[i] = cv2.countNonZero(omr_ID_1[0:Height, i * Width2:(i + 1) * Width2])
                ID_2[i] = cv2.countNonZero(omr_ID_2[0:Height, i * Width2:(i + 1) * Width2])
                ID_3[i] = cv2.countNonZero(omr_ID_3[0:Height, i * Width2:(i + 1) * Width2])
                ID_4[i] = cv2.countNonZero(omr_ID_4[0:Height, i * Width2:(i + 1) * Width2])
                ID_5[i] = cv2.countNonZero(omr_ID_5[0:Height, i * Width2:(i + 1) * Width2])

            # calculate the number of black pixels in each column
            # and print the result
            print("ID_1: ", ID_1)
            print("ID_2: ", ID_2)
            print("ID_3: ", ID_3)
            print("ID_4: ", ID_4)
            print("ID_5: ", ID_5)

            # find the column with the least black pixels
            # and assign it to the variable "answer"
            answer = np.zeros(5)
            answer[0] = np.argmin(ID_1)
            #print("ID_1: ", answer)
            answer[1] = np.argmin(ID_2)
            #print("ID_2: ", answer)
            answer[2] = np.argmin(ID_3)
            #print("ID_3: ", answer)
            answer[3] = np.argmin(ID_4)
            #print("ID_4: ", answer)
            answer[4] = np.argmin(ID_5)
            #print("ID_5: ", answer)

            # consolidate the result into a string
            answer = answer.astype(np.int64)
            # result is integer
            result = answer[0] * 10000 + answer[1] * 1000 + answer[2] * 100 + answer[3] * 10 + answer[4]
            print("Result: ", result)
            # show the result on the window dialog box
            label2 = tk.Label(window, text="Result: " + str(result), font=("Helvetica", 16))
            # place label2 at (100,500)
            label2.place(x=150, y=500)

            cv2.waitKey(500)

            # rename the file with the result and hyphen and the current time
            now = datetime.now()
            now = now.strftime('%Y-%m-%d-%H-%M-%S')
            config = open("config.ini", "r")
            saving_path = config.read()
            config.close()
            new_file = os.path.join(str(saving_path), str(result) + '(' + now + ').png')
            os.rename(path + '\\' + file, new_file)

            """
            os.rename(path + '\\' + file, path + '\\' + str(result) + '-' + file[1:9] + '.png')
            # if the file is already existing in the folder, add hyphen and number

            if os.path.isfile(path + '\\' + str(result) + '-' + file[1:9] + '.png'):
                for i in range(1, 100):
                    if os.path.isfile(path + '\\' + str(result) + '-' + str(i).zfill(3) + '.png')==False:
                        os.rename(path + '\\' + file, path + '\\' + str(result) + '-' + str(i).zfill(3) + '.png')
                        break
            """
            window.update()
            label2.destroy()


        else:
            tk.messagebox.showinfo("Error", "File not opened")



def open_file():
    file = filedialog.askopenfilename(filetypes=[("pdf files", "*.pdf")])
    if file:
        #import poppler
        pop_path =".\\poppler\\bin\\"
        images = convert_from_path(file, poppler_path=pop_path)
        if os.path.isdir('.\\extract')==False:
            os.mkdir('.\\extract')
        for idx, img in enumerate(images):
            img.save('.\\extract\\c' + str(idx + 1).zfill(4) + '.png', 'png')

    else:
        window.mainloop()

    renaming(saving_path)
    # pop up a message box to show the result
    tk.messagebox.showinfo("Result", "Done")
    os.remove('.\\scanned.png')
    os.rmdir('.\\extract')
    # window goes default design


    logo = tk.PhotoImage(file="4al.png")
    label.configure(image=logo)
    label.pack(side="left")
    window.mainloop()

    #return file


button1.config(command=choose_path)
button2.config(command=open_file)

window.update()
window.mainloop()

