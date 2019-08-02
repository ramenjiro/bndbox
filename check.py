# check.py
# 2019/07/29 created by kwhtsng
#

# import libraries
import os
import sys
import glob
import xml.etree.ElementTree as et
import xml.dom.minidom as md
import cv2

# get 'xml' files
def GetFile():

    # read *.xml files by cwd
    x_files = glob.glob("xml/*.xml")

    # exit if no files
    if not (x_files or files):
        exit("XML形式のファイルが見つかりませんでした。")

    # sort
    x_files.sort()

    # return
    return x_files

# read 'xml' files and get parameter
def ReadXml(x_file):
    # parse x_file
    tree = et.parse(x_file)

    # get root
    root = tree.getroot()

    # get filename
    filename = root.find("filename").text

    # init coord
    coords = []

    # get bndbox
    for bndbox in root.iter("bndbox"):
        coords.append([[int(bndbox.find("xmin").text), int(bndbox.find("ymin").text)],
                       [int(bndbox.find("xmax").text), int(bndbox.find("ymax").text)]])
    # return
    return filename, coords

# show img to cv2 window
def ShowImg(filename, coords):
    image  = "data/" + filename + ".jpg"
    img    = cv2.imread(image)
    wname  = image
    cv2.namedWindow(wname)
    for coord in coords:
        cv2.rectangle(img,
                      (coord[0][0],coord[0][1]),
                      (coord[1][0],coord[1][1]),
                      (0,255,0),
                      1)
    cv2.imshow(wname, img)
    key = cv2.waitKey(0) & 0xFF
    if key == ord("q"):
        cv2.destroyAllWindows()
        exit("終了します。")
    elif key == ord("n"):
        cv2.destroyAllWindows()
        print("次の画像を表示します")

# main
if __name__ == "__main__":
    x_files = GetFile()
    for x_file in x_files:
        filename, coords = ReadXml(x_file)
        print("画像ファイル名 => " + filename + ".jpg")
        ShowImg(filename, coords)
    print("すべての画像を表示し終えました。")
