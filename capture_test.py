import cv2
import os
# import datetime

def save_frame_camera_key(device_num, dir_path, basename,cycle, ext='jpg', delay=1, window_name='frame'):
    cap = cv2.VideoCapture(device_num)
    base_path="/home/user/Documents/data/"
    id = 35
    if not cap.isOpened():
        return

    os.makedirs(dir_path, exist_ok=True)
    base_path = os.path.join(dir_path, basename)

    while True:
        ret, frame = cap.read()
        cv2.imshow(window_name, frame)
        key = cv2.waitKey(delay)
        if  key == ord('q'):
                break
        elif key == ord('c'):
                strngr = "CYM"
                print("座標は-->")
                xy = input()
                print("画像を保存します。ファイル名" + base_path + strngr + "_" + xy + "_"+str(id)+"." + ext)
                cv2.imwrite('{}{}_{}_{}.{}'.format(base_path,strngr, xy, id, ext), frame)
                id += 1
    cv2.destroyWindow(window_name)

#データの保存場所
#3つ目の項目が撮影間隔（cycle）fps30で撮影しているため、cycle/30=撮影間隔（秒）となる　例cycle=60 60/30= 2 (秒間隔)
save_frame_camera_key(0, 'data', 'xK_',60)
